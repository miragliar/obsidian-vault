#!/usr/bin/env python3
"""
teams_digest.py
---------------
Scannt deine Microsoft-Teams-Chats (1:1 + Gruppen) via Graph (delegiert, Chat.Read),
aggregiert pro Gesprächspartner Häufigkeit + Nachrichten-Vorschauen und leitet die
Firmenzugehörigkeit aus der E-Mail-Domain ab. Schreibt LOKAL teams_digest.json.

Voraussetzung: App-Registrierung um delegierte Permission **Chat.Read** erweitern
(+ Admin consent). Beim ersten Lauf neuer Device-Code-Login (neue Scopes).

Aufruf:
  python3 teams_digest.py
  python3 teams_digest.py --max-chats 300 --per-chat 80
"""
import argparse
import html
import json
import os
import re
import sys
import time
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "<<HIER_APPLICATION_CLIENT_ID>>")
TENANT_ID = os.environ.get("M365_TENANT_ID", "<<HIER_DIRECTORY_TENANT_ID>>")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Chat.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".token_cache.bin"
OUT = SCRIPT_DIR / "teams_digest.json"


def get_token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    result = None
    for acc in app.get_accounts():
        result = app.acquire_token_silent(SCOPES, account=acc)
        if result:
            break
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60 + f"\n{flow['message']}\n" + "=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE_FILE.write_text(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"Login fehlgeschlagen: {result.get('error_description')}")
    return result["access_token"]


class SkipChat(Exception):
    pass


def gget(token, url, soft=False):
    """GET mit Throttling-Handling; gibt JSON dict zurück.
    soft=True: bei 403/404 (einzelner unzugänglicher Chat) -> SkipChat statt Abbruch."""
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        if r.status_code in (403, 404):
            if soft:
                raise SkipChat()
            sys.exit(f"{r.status_code} – fehlt die Permission 'Chat.Read' (mit Admin consent)? "
                     "App-Registrierung erweitern und neu anmelden.")
        r.raise_for_status()
        return r.json()


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return " ".join(html.unescape(s).split())


def me_identity(token):
    d = gget(token, f"{GRAPH}/me?$select=id,mail,userPrincipalName")
    return d["id"], (d.get("mail") or d.get("userPrincipalName") or "").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-chats", type=int, default=300)
    ap.add_argument("--per-chat", type=int, default=80, help="max. Nachrichten pro Chat")
    ap.add_argument("--per-person", type=int, default=20, help="max. gespeicherte Vorschauen je Person")
    args = ap.parse_args()
    if "<<HIER" in CLIENT_ID:
        sys.exit("CLIENT_ID/TENANT_ID nicht gesetzt.")

    token = get_token()
    my_id, my_email = me_identity(token)
    print(f"Eigene Adresse: {my_email}")

    # 1) Chats auflisten (mit Mitgliedern)
    chats = []
    url = f"{GRAPH}/me/chats?$top=50&$expand=members"
    while url and len(chats) < args.max_chats:
        data = gget(token, url)
        chats.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    chats = chats[:args.max_chats]
    print(f"{len(chats)} Chats gefunden. Lese Nachrichten …")

    people = {}   # id -> record
    groups = []
    scanned_msgs = 0
    skipped_chats = 0

    for ci, chat in enumerate(chats, 1):
        ctype = chat.get("chatType", "")
        members = chat.get("members", []) or []
        # id -> (name, email)
        idmap = {}
        for m in members:
            uid = m.get("userId")
            if uid:
                idmap[uid] = (m.get("displayName") or "", (m.get("email") or "").lower())
        # Nachrichten des Chats (einzelne unzugängliche Chats überspringen)
        msgs = []
        murl = f"{GRAPH}/me/chats/{chat['id']}/messages?$top=50"
        got = 0
        try:
            while murl and got < args.per_chat:
                data = gget(token, murl, soft=True)
                for m in data.get("value", []):
                    if m.get("messageType") != "message" or m.get("deletedDateTime"):
                        continue
                    got += 1; scanned_msgs += 1
                    frm = ((m.get("from") or {}).get("user") or {})
                    msgs.append({
                        "from_id": frm.get("id"),
                        "from_name": frm.get("displayName") or "",
                        "d": (m.get("createdDateTime") or "")[:10],
                        "text": strip_html((m.get("body") or {}).get("content", ""))[:400],
                    })
                murl = data.get("@odata.nextLink") if got < args.per_chat else None
        except SkipChat:
            skipped_chats += 1
            continue

        if ctype == "group":
            topic = chat.get("topic") or "(ohne Titel)"
            last = max([x["d"] for x in msgs], default="")
            groups.append({
                "topic": topic, "members": [idmap[u][0] for u in idmap if u != my_id],
                "emails": sorted({idmap[u][1] for u in idmap if u != my_id and idmap[u][1]}),
                "msg_count": len(msgs), "last": last,
            })

        # pro Person aggregieren
        for m in msgs:
            fid = m["from_id"]
            if not fid or fid == my_id:
                continue
            name, email = idmap.get(fid, (m["from_name"], ""))
            rec = people.setdefault(fid, {
                "name": name, "email": email, "msgs_from": 0, "my_replies_1to1": 0,
                "chats": 0, "last": "", "in_group": 0, "in_1to1": 0, "samples": [],
            })
            rec["name"] = rec["name"] or name
            rec["email"] = rec["email"] or email
            rec["msgs_from"] += 1
            rec["in_group" if ctype == "group" else "in_1to1"] += 1
            if m["d"] > rec["last"]:
                rec["last"] = m["d"]
            if len(rec["samples"]) < args.per_person and m["text"]:
                rec["samples"].append({"d": m["d"], "type": ctype, "text": m["text"]})
        # meine Antworten in 1:1
        if ctype == "oneOnOne":
            other = next((u for u in idmap if u != my_id), None)
            if other:
                r = people.setdefault(other, {
                    "name": idmap[other][0], "email": idmap[other][1], "msgs_from": 0,
                    "my_replies_1to1": 0, "chats": 0, "last": "", "in_group": 0,
                    "in_1to1": 0, "samples": []})
                r["my_replies_1to1"] += sum(1 for m in msgs if m["from_id"] == my_id)
                r["chats"] += 1
        if ci % 25 == 0:
            print(f"  … {ci}/{len(chats)} Chats, {scanned_msgs} Nachrichten", flush=True)

    rows = []
    for fid, r in people.items():
        email = r["email"]
        domain = email.split("@")[1] if "@" in email else ""
        total = r["msgs_from"] + r["my_replies_1to1"]
        rows.append({**r, "domain": domain, "interactions": total})
    rows.sort(key=lambda x: x["interactions"], reverse=True)

    OUT.write_text(json.dumps({
        "me": my_email, "chats_scanned": len(chats), "messages_scanned": scanned_msgs,
        "people": rows, "group_chats": sorted(groups, key=lambda g: g["msg_count"], reverse=True),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✓ {scanned_msgs} Nachrichten · {len(rows)} Chat-Partner · {len(groups)} Gruppenchats "
          f"· {skipped_chats} Chats übersprungen (403/404) → {OUT.name}")
    print("\nTop Chat-Partner:")
    for r in rows[:30]:
        print(f"  {r['interactions']:4d}  ({r['in_1to1']}×1:1 / {r['in_group']}×Gruppe)  "
              f"{(r['name'] or r['email'])[:28]:28s}  {r['domain']:22s} letzter {r['last']}")


if __name__ == "__main__":
    main()
