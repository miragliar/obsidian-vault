#!/usr/bin/env python3
"""
first_contact.py
----------------
Ermittelt pro Person das früheste ein- ODER ausgehende E-Mail-Datum ("Kontakt seit")
und schreibt es als `kontakt_seit` ins Frontmatter der Personen-Notiz (25_People).

Logik: **frühestes Datum gewinnt** — ein bestehendes `kontakt_seit` wird nur
überschrieben, wenn das neu gefundene Datum FRÜHER ist (so kann Teams später
nur verbessern, nie verschlechtern).

Scannt das GANZE Postfach (Mail.Read). Standard = Trockenlauf; --apply schreibt.

Aufruf:
  python3 first_contact.py                 # Trockenlauf
  python3 first_contact.py --apply
  python3 first_contact.py --max 30000     # Sicherheits-Cap (0 = unbegrenzt, Default)
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path

import requests

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent
PEOPLE = ROOT / "25_People"


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def person_email_map():
    """email(lower) -> notizpfad."""
    m = {}
    for note in PEOPLE.glob("*.md"):
        for line in note.read_text(encoding="utf-8").splitlines():
            if line.startswith("email:"):
                m[line[6:].strip().lower()] = note
                break
    return m


def scan_first(token, targets, max_msgs):
    """Gibt {email: frühestes_datum 'YYYY-MM-DD'} für Ziele zurück."""
    sel = "from,toRecipients,ccRecipients,receivedDateTime,sentDateTime"
    url = f"{GRAPH}/me/messages?$select={sel}&$top=50&$orderby=receivedDateTime asc"
    headers = {"Authorization": f"Bearer {token}"}
    earliest = {}
    seen = 0
    while url and (max_msgs == 0 or seen < max_msgs):
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        r.raise_for_status()
        data = r.json()
        for m in data.get("value", []):
            seen += 1
            dt = (m.get("receivedDateTime") or m.get("sentDateTime") or "")[:10]
            if not dt:
                continue
            parties = []
            frm = (m.get("from") or {}).get("emailAddress", {}).get("address")
            if frm:
                parties.append(frm)
            for grp in ("toRecipients", "ccRecipients"):
                for rc in (m.get(grp) or []):
                    a = rc.get("emailAddress", {}).get("address")
                    if a:
                        parties.append(a)
            for addr in parties:
                e = addr.lower()
                if e in targets and (e not in earliest or dt < earliest[e]):
                    earliest[e] = dt
        url = data.get("@odata.nextLink")
        # Da aufsteigend sortiert: sobald ALLE Ziele gefunden sind, ist deren erstes
        # Auftreten = Erstkontakt -> wir können stoppen.
        if len(earliest) >= len(targets):
            break
        if seen % 1000 == 0:
            print(f"  … {seen} Mails gescannt, {len(earliest)}/{len(targets)} Erstkontakte", flush=True)
    print(f"\n✓ {seen} Mails gescannt, {len(earliest)}/{len(targets)} Personen mit Erstkontakt-Datum.")
    return earliest


def set_kontakt_seit(note, date):
    """Setzt/aktualisiert kontakt_seit (frühestes gewinnt). Gibt 'set'|'update'|'keep'."""
    t = note.read_text(encoding="utf-8")
    m = re.search(r"^kontakt_seit:\s*(\S+)\s*$", t, re.M)
    if m:
        if date < m.group(1):
            t = t[:m.start()] + f"kontakt_seit: {date}" + t[m.end():]
            note.write_text(t, encoding="utf-8"); return "update"
        return "keep"
    # nach email: einfügen, sonst nach created:
    anchor = "email:" if re.search(r"^email:", t, re.M) else "created:"
    t2 = re.sub(rf"(^{anchor}.*$)", rf'\1\nkontakt_seit: {date}', t, count=1, flags=re.M)
    if t2 != t:
        note.write_text(t2, encoding="utf-8"); return "set"
    return "keep"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max", type=int, default=0, help="Cap an Mails (0 = unbegrenzt)")
    args = ap.parse_args()

    token = get_token()
    pmap = person_email_map()
    print(f"{len(pmap)} Personen mit Email. Scanne Postfach (aufsteigend) …")
    earliest = scan_first(token, set(pmap), args.max)

    s = u = k = 0
    for email, date in sorted(earliest.items(), key=lambda x: x[1]):
        note = pmap[email]
        if args.apply:
            res = set_kontakt_seit(note, date)
            s += res == "set"; u += res == "update"; k += res == "keep"
        print(f"  {date}  {note.stem[:34]:34s}  {email}")
    if args.apply:
        print(f"\n✓ kontakt_seit: {s} neu, {u} verfrüht-aktualisiert, {k} unverändert.")
    else:
        print("\n(Trockenlauf — nichts geschrieben. Mit --apply schreiben.)")


if __name__ == "__main__":
    main()
