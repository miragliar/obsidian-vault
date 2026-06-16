#!/usr/bin/env python3
"""
download_attachments.py — Anhänge einer Mail (per Betreff-Suche) herunterladen.

Nutzt den gemeinsamen MSAL-Keychain-Token (auth_common). Reine Lese-Operation.

Usage:
    ./.venv/bin/python download_attachments.py "betreff-suche" "ziel-ordner" ["betreff-filter"]
    ./.venv/bin/python download_attachments.py --list "betreff-suche" ["betreff-filter"]   # nur auflisten
"""
import sys
import os
import base64
from pathlib import Path
import requests
from auth_common import get_token, GRAPH

list_only = False
args = sys.argv[1:]
if args and args[0] == "--list":
    list_only = True
    args = args[1:]

query = args[0]
if list_only:
    out_dir = None
    subj_filter = (args[1].lower() if len(args) > 1 else "")
else:
    out_dir = Path(args[1])
    subj_filter = (args[2].lower() if len(args) > 2 else "")

tok = get_token(["Mail.Read", "User.Read"])
H = {"Authorization": f"Bearer {tok}"}

url = (f'{GRAPH}/me/messages?$search="{query}"'
       f'&$select=subject,from,receivedDateTime,hasAttachments&$top=10')
r = requests.get(url, headers=H, timeout=60)
r.raise_for_status()
msgs = r.json().get("value", [])

picked = None
for m in msgs:
    if subj_filter and subj_filter not in (m.get("subject") or "").lower():
        continue
    if not m.get("hasAttachments"):
        continue
    picked = m
    break

if not picked:
    sys.exit("Keine passende Mail mit Anhang gefunden.")

mid = picked["id"]
print(f"MSG: {picked.get('receivedDateTime')} | {picked.get('subject')}")
print(f"FROM: {((picked.get('from') or {}).get('emailAddress') or {}).get('address','')}")

a = requests.get(
    f"{GRAPH}/me/messages/{mid}/attachments",
    headers=H, timeout=120)
a.raise_for_status()
atts = a.json().get("value", [])
print(f"ATTACHMENTS: {len(atts)}")

if out_dir:
    out_dir.mkdir(parents=True, exist_ok=True)

for att in atts:
    name = att.get("name", "unnamed")
    size = att.get("size", 0)
    ctype = att.get("contentType", "")
    inline = att.get("isInline", False)
    odata = att.get("@odata.type", "")
    print(f"  - {name}  [{ctype}]  {size} bytes  inline={inline}  {odata}")
    if list_only:
        continue
    if odata != "#microsoft.graph.fileAttachment":
        print(f"    (übersprungen: kein fileAttachment, sondern {odata})")
        continue
    full = requests.get(
        f"{GRAPH}/me/messages/{mid}/attachments/{att['id']}",
        headers=H, timeout=120)
    full.raise_for_status()
    content_b64 = full.json().get("contentBytes")
    if not content_b64:
        print("    (kein contentBytes — übersprungen)")
        continue
    dest = out_dir / name
    dest.write_bytes(base64.b64decode(content_b64))
    print(f"    -> gespeichert: {dest}")
