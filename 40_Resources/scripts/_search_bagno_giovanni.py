#!/usr/bin/env python3
"""Suche nach Bagno-Lieferanten-Korrespondenz in GIOVANNIS Postfach.

Die Koordinations-Mail vom 01.06.2026 wurde von giovanni@miraglia-bi.com
geschickt; Raoul ist NICHT im Verteiler. Daher Zugriff via Mail.Read.Shared
auf Giovannis Postfach.
"""
import time, json
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).resolve().parent
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.Read", "Mail.Read.Shared"]
GIOVANNI = "giovanni@miraglia-bi.com"

SUPPLIERS = {
    "Bazzi":     ["from:e.cappucci@bazzi.ch", "from:m.trunzo@bazzi.ch", "from:info@bazzi.ch",
                  "to:e.cappucci@bazzi.ch", "to:info@bazzi.ch", "to:m.trunzo@bazzi.ch"],
    "Badasci":   ["from:spaions@bluewin.ch", "to:spaions@bluewin.ch",
                  "from:info@badascifabiosagl.ch", "to:info@badascifabiosagl.ch", "Badasci"],
    "Pasinelli": ["from:info@pasinelli.ch", "to:info@pasinelli.ch", "Pasinelli"],
    "DELO":      ["from:info@delo.ch", "to:info@delo.ch",
                  "from:n.mossetti@delo.ch", "to:n.mossetti@delo.ch",
                  "from:s.mossetti@delo.ch", "to:s.mossetti@delo.ch",
                  "from:elia@delo.ch", "to:elia@delo.ch"],
}


def get_token():
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def search_in_mailbox(token, mailbox, q, top=50):
    url = (f"{GRAPH}/users/{mailbox}/messages?$search=\"{q}\""
           f"&$select=from,toRecipients,ccRecipients,subject,bodyPreview,receivedDateTime,webLink,hasAttachments"
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
    prev = (m.get('bodyPreview','') or '').strip()[:400].replace(chr(10), ' ')
    if prev:
        out.append(f"    PREV: {prev}")
    return "\n".join(out)


def main():
    token = get_token()
    print(f"Suche in Postfach: {GIOVANNI}")
    out_json = {}
    for supplier, terms in SUPPLIERS.items():
        print("\n" + "=" * 80)
        print(f" LIEFERANT: {supplier}")
        print("=" * 80)
        seen_ids = set()
        all_msgs = []
        for term in terms:
            msgs, code, err = search_in_mailbox(token, GIOVANNI, term)
            if code != 200:
                print(f"  ! search failed for term '{term}': {code} {err}")
                continue
            for m in msgs:
                mid = m.get("id") or (m.get("subject","") + str(m.get("receivedDateTime","")))
                if mid in seen_ids:
                    continue
                seen_ids.add(mid)
                all_msgs.append(m)
        all_msgs.sort(key=lambda x: x.get("receivedDateTime",""), reverse=True)
        if not all_msgs:
            print("  (keine Treffer)")
        else:
            print(f"  --- {len(all_msgs)} Treffer ---")
            for m in all_msgs:
                print(fmt(m))
                print()
        out_json[supplier] = [
            {
                "id": m.get("id",""),
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
    Path(SCRIPT_DIR / "_bagno_giovanni_search.json").write_text(json.dumps(out_json, indent=2, ensure_ascii=False))
    print(f"\nJSON-Dump: {SCRIPT_DIR / '_bagno_giovanni_search.json'}")


if __name__ == "__main__":
    main()
