#!/usr/bin/env python3
"""
mvm_extras.py
-------------
Sucht in den letzten 500 Mails alle MVM-relevanten Treffer, die nicht in
mail_digest.json auftauchen, weil dort kein Personen-Notiz-Match war:
- @mvm-ag.ch Mails (alle Adressen)
- Filliger / filliger-partner.ch / filligerpartner.ch
- Subject enthält "9186" (Materialbezug)
- Scherrer Nicole

Speichert nach mvm_extras.json.
"""
import json
import os
import sys
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]
SCRIPT_DIR = Path(__file__).resolve().parent
CACHE = SCRIPT_DIR / ".token_cache.bin"
OUT = SCRIPT_DIR / "mvm_extras.json"


def token():
    c = msal.SerializableTokenCache()
    if CACHE.exists():
        c.deserialize(CACHE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=c)
    for a in app.get_accounts():
        r = app.acquire_token_silent(SCOPES, account=a)
        if r:
            if c.has_state_changed:
                CACHE.write_text(c.serialize())
            return r["access_token"]
    sys.exit("kein cache")


MVM_DOMAINS = {"mvm-ag.ch"}
FILLIGER_HINTS = ("filliger", "filiger")  # robust gegen Tippfehler
SUBJECT_HINTS = ("9186",)
NAME_HINTS = ("scherrer", "nicole scherrer", "scherrer nicole")


def matches(m):
    """True wenn Mail MVM-Kontext hat."""
    frm = ((m.get("from") or {}).get("emailAddress") or {})
    frm_addr = (frm.get("address") or "").lower()
    frm_name = (frm.get("name") or "").lower()
    subj = (m.get("subject") or "").lower()
    prev = (m.get("bodyPreview") or "").lower()
    tos = [
        ((r.get("emailAddress") or {}).get("address") or "").lower()
        for r in (m.get("toRecipients") or [])
    ]
    ccs = [
        ((r.get("emailAddress") or {}).get("address") or "").lower()
        for r in (m.get("ccRecipients") or [])
    ]
    all_addrs = [frm_addr] + tos + ccs
    # 1) jede @mvm-ag.ch Adresse
    if any(a.endswith("@mvm-ag.ch") for a in all_addrs):
        return "mvm-ag.ch"
    # 2) filliger
    for hint in FILLIGER_HINTS:
        if hint in frm_addr or hint in frm_name or hint in subj or hint in prev:
            for a in all_addrs:
                if hint in a:
                    return f"filliger ({a})"
            return "filliger (text)"
    # 3) subject hints (9186)
    for hint in SUBJECT_HINTS:
        if hint in subj:
            return f"subject:{hint}"
    # 4) Name hints
    for hint in NAME_HINTS:
        if hint in frm_name or hint in subj or hint in prev:
            return f"name:{hint}"
    return None


def main():
    t = token()
    h = {"Authorization": f"Bearer {t}"}
    url = (
        f"{GRAPH}/me/messages"
        f"?$select=id,subject,bodyPreview,receivedDateTime,from,toRecipients,ccRecipients"
        f"&$top=50"
        f"&$orderby=receivedDateTime desc"
    )
    hits = []
    by_sender = {}
    seen = 0
    while url and seen < 500:
        r = requests.get(url, headers=h, timeout=30)
        if not r.ok:
            print(f"HTTP {r.status_code}: {r.text[:300]}")
            break
        data = r.json()
        for m in data.get("value", []):
            seen += 1
            tag = matches(m)
            if not tag:
                continue
            frm = ((m.get("from") or {}).get("emailAddress") or {})
            hit = {
                "d": (m.get("receivedDateTime") or "")[:10],
                "from_addr": (frm.get("address") or "").lower(),
                "from_name": frm.get("name") or "",
                "subj": (m.get("subject") or "").strip(),
                "prev": (m.get("bodyPreview") or "").strip()[:500],
                "tag": tag,
            }
            hits.append(hit)
            by_sender.setdefault(hit["from_addr"], 0)
            by_sender[hit["from_addr"]] += 1
        url = data.get("@odata.nextLink")
        print(f"  … {seen} gescannt, {len(hits)} Treffer", end="\r", flush=True)
    print(f"\n✓ {seen} Mails gescannt, {len(hits)} Treffer.\n")

    print("Treffer-Verteilung nach Absender:")
    for addr, n in sorted(by_sender.items(), key=lambda x: -x[1]):
        print(f"  {n:3d}  {addr}")

    OUT.write_text(json.dumps({"scanned": seen, "hits": hits}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"\n→ {OUT}")


if __name__ == "__main__":
    main()
