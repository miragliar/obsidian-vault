#!/usr/bin/env python3
"""
contact_stats.py
----------------
Zählt pro Person die Interaktionen und schreibt sie als Relevanz-Kennzahlen ins
Frontmatter der Personen-Notizen (25_People):

  mail_in / mail_out  – erhaltene / gesendete Mails (LEBENSLANG)
  teams_total         – Teams-Nachrichten der Person (LEBENSLANG)
  interaktionen       – Summe lebenslang (mail_in + mail_out + teams_total)
  interaktionen_12m   – Summe der letzten 12 Monate (rollierend)
  stats_stand         – Datum der Berechnung

Robust für lange Läufe: Token-Refresh bei 401, Throttling-Handling, überspringt
Meeting-Chats und kappt sehr lange Chats. Standard = Trockenlauf; --apply schreibt.
"""
import argparse
import os
import re
import sys
import time
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import requests

GRAPH = "https://graph.microsoft.com/v1.0"
SCRIPT_DIR = Path(__file__).resolve().parent
PEOPLE = SCRIPT_DIR.parent.parent / "25_People"
TODAY = date.today()
CUT12 = (TODAY - timedelta(days=365)).isoformat()
PER_CHAT_CAP = 1500   # max. Nachrichten je Chat (bremst Riesen-Chats)

_TOK = None
_SCOPES = ["User.Read", "Mail.Read", "Chat.Read"]


class SkipChat(Exception):
    pass


def refresh_token():
    global _TOK
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    _TOK = _ac_get_token(_SCOPES)
    return _TOK


def gget(url, soft=False):
    for attempt in range(3):
        r = requests.get(url, headers={"Authorization": f"Bearer {_TOK}"}, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        if r.status_code == 401 and attempt < 2:
            refresh_token(); continue          # Token erneuern und nochmal
        if r.status_code in (403, 404) and soft:
            raise SkipChat()
        r.raise_for_status()
        return r.json()
    r.raise_for_status()


def email_map():
    m = {}
    for n in PEOPLE.glob("*.md"):
        mm = re.search(r"^email:\s*(.+)$", n.read_text(encoding="utf-8"), re.M)
        if mm:
            m[mm.group(1).strip().lower()] = n
    return m


def scan_mail(targets):
    mi, mo, mi12, mo12 = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)
    me = gget(f"{GRAPH}/me?$select=mail,userPrincipalName")
    me = (me.get("mail") or me.get("userPrincipalName") or "").lower()
    url = f"{GRAPH}/me/messages?$select=from,toRecipients,receivedDateTime,sentDateTime&$top=50&$orderby=receivedDateTime desc"
    seen = 0
    while url:
        d = gget(url)
        for m in d.get("value", []):
            seen += 1
            dt = (m.get("receivedDateTime") or m.get("sentDateTime") or "")[:10]
            frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
            tos = [((r.get("emailAddress") or {}).get("address") or "").lower() for r in (m.get("toRecipients") or [])]
            recent = dt >= CUT12
            if frm == me:
                for o in tos:
                    if o in targets:
                        mo[o] += 1
                        if recent: mo12[o] += 1
            elif frm in targets:
                mi[frm] += 1
                if recent: mi12[frm] += 1
        url = d.get("@odata.nextLink")
        if seen % 10000 == 0:
            print(f"  … {seen} Mails", flush=True)
    print(f"✓ Mail: {seen} Nachrichten gescannt.")
    return mi, mo, mi12, mo12


def scan_teams(targets):
    tt, t12 = defaultdict(int), defaultdict(int)
    me_id = gget(f"{GRAPH}/me?$select=id")["id"]
    chats = []
    url = f"{GRAPH}/me/chats?$top=50&$expand=members"
    while url:
        d = gget(url)
        chats.extend(d.get("value", []))
        url = d.get("@odata.nextLink")
    skipped = meetings = 0
    for ci, ch in enumerate(chats, 1):
        if ch.get("chatType") == "meeting" or str(ch.get("id", "")).startswith("19:meeting_"):
            meetings += 1; continue
        idmap = {m.get("userId"): (m.get("email") or "").lower() for m in (ch.get("members") or []) if m.get("userId")}
        if not any(e in targets for e in idmap.values()):
            continue
        murl = f"{GRAPH}/me/chats/{ch['id']}/messages?$top=50"
        got = 0
        try:
            while murl and got < PER_CHAT_CAP:
                d = gget(murl, soft=True)
                for m in d.get("value", []):
                    got += 1
                    if m.get("messageType") != "message":
                        continue
                    fid = ((m.get("from") or {}).get("user") or {}).get("id")
                    e = idmap.get(fid, "")
                    if e in targets and fid != me_id:
                        tt[e] += 1
                        if (m.get("createdDateTime") or "")[:10] >= CUT12:
                            t12[e] += 1
                murl = d.get("@odata.nextLink") if got < PER_CHAT_CAP else None
        except SkipChat:
            skipped += 1
        if ci % 50 == 0:
            print(f"  … {ci}/{len(chats)} Chats", flush=True)
    print(f"✓ Teams: {len(chats)} Chats ({meetings} Meeting-Chats übersprungen, {skipped} ohne Zugriff).")
    return tt, t12


def set_fm(text, key, val):
    line = f"{key}: {val}"
    if re.search(rf"^{key}:.*$", text, re.M):
        return re.sub(rf"^{key}:.*$", line, text, count=1, flags=re.M)
    m = re.search(r"^---\n.*?\n(---)\n", text, re.S)
    return text[:m.start(1)] + line + "\n" + text[m.start(1):] if m else text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--no-teams", action="store_true")
    ap.add_argument("--no-mail", action="store_true")
    args = ap.parse_args()
    global _SCOPES
    _SCOPES = ["User.Read"] + ([] if args.no_mail else ["Mail.Read"]) + ([] if args.no_teams else ["Chat.Read"])
    refresh_token()

    pmap = email_map()
    targets = set(pmap)
    print(f"{len(targets)} Personen · 12-Monats-Grenze: {CUT12}")

    mi = mo = mi12 = mo12 = defaultdict(int)
    tt = t12 = defaultdict(int)
    if not args.no_mail:
        mi, mo, mi12, mo12 = scan_mail(targets)
    if not args.no_teams:
        tt, t12 = scan_teams(targets)

    rows = []
    for e in targets:
        life = mi[e] + mo[e] + tt[e]
        m12 = mi12[e] + mo12[e] + t12[e]
        if life:
            rows.append((e, mi[e], mo[e], tt[e], life, m12))
    rows.sort(key=lambda x: x[4], reverse=True)

    written = 0
    for e, a, b, c, life, m12 in rows:
        n = pmap[e]; t = n.read_text(encoding="utf-8")
        for k, v in [("mail_in", a), ("mail_out", b), ("teams_total", c),
                     ("interaktionen", life), ("interaktionen_12m", m12),
                     ("stats_stand", TODAY.isoformat())]:
            t = set_fm(t, k, v)
        if args.apply:
            n.write_text(t, encoding="utf-8"); written += 1

    print("\nTop 15 nach Interaktionen (lebenslang / 12M):")
    for e, a, b, c, life, m12 in rows[:15]:
        print(f"  {life:5d} / {m12:4d}   {pmap[e].stem[:30]:30s}  (Mail {a}<-/{b}-> · Teams {c})")
    print(f"\n{('✓ ' + str(written) + ' Notizen aktualisiert') if args.apply else '(Trockenlauf)'} · {len(rows)} mit Interaktionen.")


if __name__ == "__main__":
    main()
