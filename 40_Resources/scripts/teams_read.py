#!/usr/bin/env python3
"""
teams_read.py — LIVE einen 1:1-Teams-Chat einer Person lesen (Pendant zu live_search.py für Mail).

Findet den oneOnOne-Chat anhand Name/E-Mail-Filter, gibt die letzten N Nachrichten
chronologisch aus und lädt inline-Bilder (Graph hostedContents) + Datei-Anhänge herunter.

Aufruf:
  ./.venv/bin/python teams_read.py "patrick.cruz" --limit 40 --save-images ../../_Attachments
  ./.venv/bin/python teams_read.py "cruz" --since 2026-06-05
"""
import argparse
import html
import json
import re
import sys
import time
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from auth_common import get_token, GRAPH  # noqa: E402

SCOPES = ["User.Read", "Chat.Read"]


def gget(token, url, raw=False):
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        r = requests.get(url, headers=headers, timeout=60)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        r.raise_for_status()
        return r if raw else r.json()


def strip_html(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return " ".join(html.unescape(s).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="Name- oder E-Mail-Teil des Chatpartners")
    ap.add_argument("--limit", type=int, default=40, help="max. Nachrichten")
    ap.add_argument("--since", default=None, help="nur Nachrichten ab Datum YYYY-MM-DD")
    ap.add_argument("--save-images", default=None, help="Zielordner für inline-Bilder/Anhänge")
    args = ap.parse_args()
    q = args.query.lower()

    token = get_token(SCOPES)
    me = gget(token, f"{GRAPH}/me?$select=id,mail,userPrincipalName")
    my_id = me["id"]

    # passenden Chat finden
    chats, url = [], f"{GRAPH}/me/chats?$top=50&$expand=members"
    while url:
        d = gget(token, url)
        chats.extend(d.get("value", []))
        url = d.get("@odata.nextLink")

    target = None
    for c in chats:
        for m in c.get("members", []) or []:
            name = (m.get("displayName") or "").lower()
            email = (m.get("email") or "").lower()
            if q in name or q in email:
                target = c
                target["_match"] = (m.get("displayName"), m.get("email"))
                break
        if target:
            break
    if not target:
        sys.exit(f"Kein Chat mit '{args.query}' gefunden (durchsucht: {len(chats)} Chats).")

    print(f"Chat: {target.get('chatType')} mit {target['_match'][0]} <{target['_match'][1]}>")
    print(f"chatId: {target['id']}\n" + "=" * 80)

    # Nachrichten holen
    msgs, murl, got = [], f"{GRAPH}/me/chats/{target['id']}/messages?$top=50", 0
    while murl and got < args.limit:
        d = gget(token, murl)
        for m in d.get("value", []):
            if m.get("messageType") != "message" or m.get("deletedDateTime"):
                continue
            if args.since and (m.get("createdDateTime") or "")[:10] < args.since:
                continue
            msgs.append(m); got += 1
        murl = d.get("@odata.nextLink") if got < args.limit else None

    msgs = sorted(msgs, key=lambda m: m.get("createdDateTime") or "")
    save_dir = Path(args.save_images).resolve() if args.save_images else None
    if save_dir:
        save_dir.mkdir(parents=True, exist_ok=True)
    img_idx = 0

    for m in msgs:
        when = (m.get("createdDateTime") or "")[:16].replace("T", " ")
        who = ((m.get("from") or {}).get("user") or {}).get("displayName") or "(system)"
        body = (m.get("body") or {}).get("content", "")
        text = strip_html(body)
        edited = " (bearbeitet)" if m.get("lastEditedDateTime") else ""
        print(f"\n[{when}] {who}{edited}:")
        if text:
            print(f"  {text}")

        # Datei-Anhänge
        for a in m.get("attachments", []) or []:
            print(f"  📎 Anhang: name={a.get('name')} type={a.get('contentType')} url={a.get('contentUrl')}")

        # inline-Bilder (hostedContents)
        if "hostedContents" in body or "graph.microsoft.com" in body:
            hc = gget(token, f"{GRAPH}/me/chats/{target['id']}/messages/{m['id']}/hostedContents")
            for h in hc.get("value", []):
                hid = h["id"]
                ct = (h.get("contentType") or "image/png")
                ext = ct.split("/")[-1].split("+")[0] or "png"
                print(f"  🖼️  inline-Bild: id={hid} type={ct}")
                if save_dir:
                    r = gget(token,
                             f"{GRAPH}/me/chats/{target['id']}/messages/{m['id']}/hostedContents/{hid}/$value",
                             raw=True)
                    img_idx += 1
                    fn = save_dir / f"Teams_{args.query}_{(m.get('createdDateTime') or '')[:10]}_{img_idx}.{ext}"
                    fn.write_bytes(r.content)
                    print(f"      → gespeichert: {fn}")

    print("\n" + "=" * 80)
    print(f"{len(msgs)} Nachrichten ausgegeben"
          + (f", {img_idx} Bild(er) gespeichert nach {save_dir}" if save_dir else ""))


if __name__ == "__main__":
    main()
