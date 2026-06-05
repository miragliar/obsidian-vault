#!/usr/bin/env python3
"""
teams_first_contact.py
----------------------
Ermittelt pro Person das früheste Teams-Nachrichtendatum (blättert jeden Chat bis
zur ältesten Nachricht) und aktualisiert `kontakt_seit` in den Personen-Notizen —
**nur wenn früher** als ein bereits gesetztes (Mail-)Datum ("frühestes gewinnt").

Voraussetzung: Chat.Read (mit Admin consent). Standard = Trockenlauf; --apply schreibt.
"""
import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests
import os

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Chat.Read"]
SCRIPT_DIR = Path(__file__).resolve().parent
PEOPLE = SCRIPT_DIR.parent.parent / "25_People"


class SkipChat(Exception):
    pass


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def gget(token, url, soft=False):
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        if r.status_code in (403, 404):
            if soft:
                raise SkipChat()
            sys.exit(f"{r.status_code} – Permission 'Chat.Read'?")
        r.raise_for_status()
        return r.json()


def nfc(s):
    return unicodedata.normalize("NFC", s)


def person_email_map():
    m = {}
    for note in PEOPLE.glob("*.md"):
        mm = re.search(r"^email:\s*(.+)$", note.read_text(encoding="utf-8"), re.M)
        if mm:
            m[mm.group(1).strip().lower()] = note
    return m


def set_kontakt_seit(note, date):
    t = note.read_text(encoding="utf-8")
    m = re.search(r"^kontakt_seit:\s*(\S+)\s*$", t, re.M)
    if m:
        if date < m.group(1):
            note.write_text(t[:m.start()] + f"kontakt_seit: {date}" + t[m.end():], encoding="utf-8")
            return "update"
        return "keep"
    anchor = "email:" if re.search(r"^email:", t, re.M) else "created:"
    t2 = re.sub(rf"(^{anchor}.*$)", rf'\1\nkontakt_seit: {date}', t, count=1, flags=re.M)
    note.write_text(t2, encoding="utf-8")
    return "set"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-chats", type=int, default=400)
    args = ap.parse_args()

    token = get_token()
    pmap = person_email_map()
    targets = set(pmap)

    chats = []
    url = f"{GRAPH}/me/chats?$top=50&$expand=members"
    while url and len(chats) < args.max_chats:
        data = gget(token, url)
        chats.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    print(f"{len(chats)} Chats. Suche je Chat die älteste Nachricht …")

    earliest = {}   # email -> 'YYYY-MM-DD'
    skipped = 0
    for ci, chat in enumerate(chats, 1):
        idmap = {m.get("userId"): (m.get("email") or "").lower()
                 for m in (chat.get("members") or []) if m.get("userId")}
        # nur Chats mit mind. einem Ziel-Teilnehmer voll durchblättern
        if not any(e in targets for e in idmap.values()):
            continue
        murl = f"{GRAPH}/me/chats/{chat['id']}/messages?$top=50"
        try:
            while murl:
                data = gget(token, murl, soft=True)
                for m in data.get("value", []):
                    if m.get("messageType") != "message":
                        continue
                    fid = ((m.get("from") or {}).get("user") or {}).get("id")
                    email = idmap.get(fid, "")
                    dt = (m.get("createdDateTime") or "")[:10]
                    if email in targets and dt and (email not in earliest or dt < earliest[email]):
                        earliest[email] = dt
                murl = data.get("@odata.nextLink")
        except SkipChat:
            skipped += 1
        if ci % 25 == 0:
            print(f"  … {ci}/{len(chats)} Chats, {len(earliest)} Teams-Erstkontakte", flush=True)

    print(f"\n✓ {len(earliest)} Personen mit Teams-Erstkontakt ({skipped} Chats übersprungen).")
    s = u = k = 0
    for email, date in sorted(earliest.items(), key=lambda x: x[1]):
        if args.apply:
            res = set_kontakt_seit(pmap[email], date)
            s += res == "set"; u += res == "update"; k += res == "keep"
            tag = {"set": "NEU", "update": "FRÜHER", "keep": "—"}[res]
        else:
            tag = "?"
        print(f"  {date}  [{tag:6s}] {pmap[email].stem[:30]:30s} {email}")
    if args.apply:
        print(f"\n✓ kontakt_seit: {s} neu gesetzt, {u} auf früheres Teams-Datum korrigiert, {k} unverändert.")
    else:
        print("\n(Trockenlauf — mit --apply schreiben.)")


if __name__ == "__main__":
    main()
