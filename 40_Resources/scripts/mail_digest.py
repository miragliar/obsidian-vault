#!/usr/bin/env python3
"""
mail_digest.py
--------------
Scannt die letzten Mails (delegiert, Mail.Read), ermittelt die häufigsten
Kontakte und sammelt pro Person Betreff + Vorschau der letzten Mails.
Schreibt das Ergebnis in mail_digest.json (LOKAL, per .gitignore ausgeschlossen).

Aufruf:
  python3 mail_digest.py                 # Top 20, letzte 2500 Mails
  python3 mail_digest.py --top 30 --max 4000
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", SCRIPT_DIR.parent.parent))
PEOPLE = VAULT_ROOT / "25_People"
OUT = SCRIPT_DIR / "mail_digest.json"


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def me_email(token):
    r = requests.get(f"{GRAPH}/me?$select=mail,userPrincipalName",
                     headers={"Authorization": f"Bearer {token}"}, timeout=30)
    r.raise_for_status()
    d = r.json()
    return (d.get("mail") or d.get("userPrincipalName") or "").lower()


def person_email_map():
    """email (lower) -> notizdatei-name."""
    m = {}
    for note in PEOPLE.glob("*.md"):
        for line in note.read_text(encoding="utf-8").splitlines():
            if line.startswith("email:"):
                m[line[6:].strip().lower()] = note.name
                break
    return m


def scan(token, me, max_msgs, per_person):
    sel = "from,toRecipients,subject,bodyPreview,receivedDateTime"
    url = f"{GRAPH}/me/messages?$select={sel}&$top=50&$orderby=receivedDateTime desc"
    headers = {"Authorization": f"Bearer {token}"}
    agg = {}   # email -> {recv, sent, last, msgs:[]}
    seen = 0
    while url and seen < max_msgs:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        r.raise_for_status()
        data = r.json()
        for m in data.get("value", []):
            seen += 1
            dt = m.get("receivedDateTime", "")
            frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
            tos = [((r.get("emailAddress") or {}).get("address") or "").lower()
                   for r in (m.get("toRecipients") or [])]
            if frm == me:
                direction, others = "out", tos
            else:
                direction, others = "in", [frm]
            for o in others:
                if not o or o == me:
                    continue
                a = agg.setdefault(o, {"recv": 0, "sent": 0, "last": "", "msgs": []})
                a["sent" if direction == "out" else "recv"] += 1
                if dt > a["last"]:
                    a["last"] = dt
                if len(a["msgs"]) < per_person:
                    a["msgs"].append({"d": dt[:10], "dir": direction,
                                      "subj": (m.get("subject") or "").strip(),
                                      "prev": (m.get("bodyPreview") or "").strip()[:400]})
        url = data.get("@odata.nextLink") if seen < max_msgs else None
        print(f"  … {seen} Mails gescannt", end="\r", flush=True)
    print(f"\n✓ {seen} Mails gescannt, {len(agg)} Korrespondenten.")
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=20, help="0 = alle (kein Cap)")
    ap.add_argument("--max", type=int, default=2500)
    ap.add_argument("--per-person", type=int, default=18)
    ap.add_argument("--min-total", type=int, default=0, help="nur Kontakte mit >= so vielen Mails")
    ap.add_argument("--min-sent", type=int, default=0, help="nur Kontakte, denen du >= so oft geantwortet hast")
    ap.add_argument("--sort", choices=["total", "sent"], default="total")
    args = ap.parse_args()

    token = get_token()
    me = me_email(token)
    print(f"Eigene Adresse: {me}")
    pmap = person_email_map()
    agg = scan(token, me, args.max, args.per_person)

    def has_summary(fname):
        try:
            return "<!-- mail-summary -->" in (PEOPLE / fname).read_text(encoding="utf-8")
        except OSError:
            return False

    rows = []
    without_note = []
    for email, a in agg.items():
        total = a["recv"] + a["sent"]
        if email in pmap:
            rows.append({"file": pmap[email], "email": email, "total": total,
                         "recv": a["recv"], "sent": a["sent"], "last": a["last"][:10],
                         "has_summary": has_summary(pmap[email]),
                         "msgs": sorted(a["msgs"], key=lambda x: x["d"], reverse=True)})
        else:
            without_note.append({"email": email, "total": total})

    rows = [r for r in rows if r["total"] >= args.min_total and r["sent"] >= args.min_sent]
    keyf = (lambda x: (x["sent"], x["total"])) if args.sort == "sent" else (lambda x: x["total"])
    rows.sort(key=keyf, reverse=True)
    without_note.sort(key=lambda x: x["total"], reverse=True)
    top = rows if args.top == 0 else rows[:args.top]

    OUT.write_text(json.dumps({
        "me": me, "scanned_max": args.max, "top_n": args.top,
        "people": top,
        "frequent_without_note": without_note[:25],
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✓ {len(top)} Kontakte (mit Notiz) → {OUT.name}")
    print(f"\nAusgewählt (sortiert nach {args.sort}):")
    for r in top:
        print(f"  {r['total']:3d}  ({r['recv']}↓/{r['sent']}↑)  {r['file'][:-3]:30s}  letzter: {r['last']}")
    print("\nHäufig, aber OHNE Notiz (evtl. anlegen?):")
    for w in without_note[:12]:
        print(f"  {w['total']:3d}  {w['email']}")


if __name__ == "__main__":
    main()
