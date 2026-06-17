#!/usr/bin/env python3
"""Gezielte Suche nach Mailverkehr zu Bagno-Lieferanten (Bazzi, Badasci, Pasinelli, DELO).

Sucht in allen Ordnern (inkl. Gesendet) nach `from:`/`to:`/`cc:`-Treffern mit den
relevanten Domains und Sub-Adressen. Verzichtet auf breite Body-Suche, um Rauschen
zu vermeiden.
"""
import sys, time, json
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).resolve().parent
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.Read", "Mail.Read.Shared", "User.Read"]

# Lieferanten-Adressen / Domains (KQL-Form, jeweils mit '@' oder konkrete Adresse)
SUPPLIERS = {
    "Bazzi":     ["e.cappucci@bazzi.ch", "m.trunzo@bazzi.ch", "info@bazzi.ch", "@bazzi.ch"],
    "Badasci":   ["spaions@bluewin.ch", "badasci@bluewin.ch", "Badasci"],
    "Pasinelli": ["info@pasinelli.ch", "@pasinelli.ch"],
    "DELO":      ["info@delo.ch", "@delo.ch", "n.mossetti@delo.ch", "s.mossetti@delo.ch"],
}


def get_token():
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def search_participants(token, term, top=25):
    """KQL participants: matcht from/to/cc/bcc gleichzeitig."""
    q = f'participants:{term}'
    url = (f"{GRAPH}/me/messages?$search=\"{q}\""
           f"&$select=from,toRecipients,ccRecipients,subject,bodyPreview,receivedDateTime,webLink,hasAttachments,parentFolderId"
           f"&$top={top}")
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5)))
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    if r.status_code >= 400:
        return [], r.status_code, r.text[:200]
    return r.json().get("value", []), 200, ""


def fmt(m):
    frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "") or "-"
    tos = ", ".join(((r.get("emailAddress") or {}).get("address") or "")
                    for r in (m.get("toRecipients") or []))
    ccs = ", ".join(((r.get("emailAddress") or {}).get("address") or "")
                    for r in (m.get("ccRecipients") or []))
    attach = " 📎" if m.get("hasAttachments") else ""
    out = [f"  {m.get('receivedDateTime','')[:16]} | from: {frm}{attach}",
           f"    to: {tos}"]
    if ccs:
        out.append(f"    cc: {ccs}")
    out.append(f"    SUBJ: {m.get('subject','')}")
    prev = (m.get('bodyPreview','') or '').strip()[:300].replace(chr(10), ' ')
    if prev:
        out.append(f"    PREV: {prev}")
    return "\n".join(out)


def main():
    token = get_token()
    out_json = {}
    for supplier, terms in SUPPLIERS.items():
        print("\n" + "=" * 78)
        print(f" LIEFERANT: {supplier}")
        print("=" * 78)
        seen_ids = set()
        all_msgs = []
        for term in terms:
            msgs, code, err = search_participants(token, term)
            if code != 200:
                print(f"  ! search failed for term '{term}': {code} {err}")
                continue
            for m in msgs:
                mid = m.get("id") or m.get("internetMessageId") or (m.get("subject","") + str(m.get("receivedDateTime","")))
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                all_msgs.append(m)
        # sort by date desc
        all_msgs.sort(key=lambda x: x.get("receivedDateTime",""), reverse=True)
        if not all_msgs:
            print("  (keine Treffer)")
        else:
            for m in all_msgs:
                print(fmt(m))
                print()
        out_json[supplier] = [
            {
                "received": m.get("receivedDateTime",""),
                "from": ((m.get("from") or {}).get("emailAddress") or {}).get("address",""),
                "to": [((r.get("emailAddress") or {}).get("address") or "") for r in (m.get("toRecipients") or [])],
                "cc": [((r.get("emailAddress") or {}).get("address") or "") for r in (m.get("ccRecipients") or [])],
                "subject": m.get("subject",""),
                "preview": (m.get("bodyPreview","") or "").strip(),
                "hasAttachments": m.get("hasAttachments", False),
                "webLink": m.get("webLink",""),
            } for m in all_msgs
        ]
    Path(SCRIPT_DIR / "_bagno_suppliers_search.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False))
    print(f"\nJSON-Dump: {SCRIPT_DIR / '_bagno_suppliers_search.json'}")


if __name__ == "__main__":
    main()
