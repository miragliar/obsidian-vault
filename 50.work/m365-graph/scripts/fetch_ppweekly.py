#!/usr/bin/env python3
"""
fetch_ppweekly.py
-----------------
Holt alle Mails von ppweekly@substack.com (Power Platform Weekly News)
aus dem Mailordner "0_Emails" und legt sie als JSON-Digest ab.

Aufruf:
  ./.venv/bin/python fetch_ppweekly.py

Schreibt:
  ppweekly_digest.json  — Liste aller gefundenen Mails (Subject, Datum, Body als Text)
"""
import html
import json
import re
import sys
import time
from pathlib import Path

import requests

from auth_common import GRAPH, get_token

SD = Path(__file__).resolve().parent
OUT = SD / "ppweekly_digest.json"
SENDER = "ppweekly@substack.com"
FOLDER_NAME = "0_Emails"


def find_folder(token: str, name: str) -> str:
    """Sucht rekursiv den Mailordner mit dem gegebenen Anzeigenamen und gibt dessen ID zurück."""
    h = {"Authorization": f"Bearer {token}"}

    def search_in(folder_id):
        base = f"{GRAPH}/me/mailFolders" if folder_id is None else f"{GRAPH}/me/mailFolders/{folder_id}/childFolders"
        url = f"{base}?$select=id,displayName,childFolderCount&$top=200"
        while url:
            r = requests.get(url, headers=h, timeout=30)
            r.raise_for_status()
            data = r.json()
            for f in data.get("value", []):
                if f.get("displayName") == name:
                    return f["id"]
                if f.get("childFolderCount", 0) > 0:
                    hit = search_in(f["id"])
                    if hit:
                        return hit
            url = data.get("@odata.nextLink")
        return None

    fid = search_in(None)
    if not fid:
        sys.exit(f"Ordner '{name}' nicht gefunden.")
    return fid


def strip_html(s: str) -> str:
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>", "\n\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n\n", s)
    return s.strip()


def fetch_messages(token: str, folder_id: str):
    h = {"Authorization": f"Bearer {token}"}
    sel = "id,subject,from,receivedDateTime,bodyPreview,webLink,body"
    flt = f"from/emailAddress/address eq '{SENDER}'"
    # Graph erlaubt $filter + $orderby auf "from" nicht — wir sortieren am Ende lokal.
    url = (f"{GRAPH}/me/mailFolders/{folder_id}/messages"
           f"?$filter={flt}&$select={sel}&$top=100")
    items = []
    while url:
        r = requests.get(url, headers=h, timeout=60)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 5))); continue
        r.raise_for_status()
        data = r.json()
        for m in data.get("value", []):
            body = (m.get("body") or {}).get("content", "")
            ct = (m.get("body") or {}).get("contentType", "text")
            text = strip_html(body) if ct == "html" else body
            items.append({
                "id": m["id"],
                "subject": (m.get("subject") or "").strip(),
                "received": m.get("receivedDateTime", ""),
                "preview": (m.get("bodyPreview") or "").strip(),
                "webLink": m.get("webLink", ""),
                "body_text": text,
            })
        url = data.get("@odata.nextLink")
        print(f"  ... {len(items)} Mails geladen", end="\r", flush=True)
    print(f"\n{len(items)} Mails von {SENDER} aus '{FOLDER_NAME}' geladen.")
    return items


def main():
    token = get_token(["Mail.Read", "User.Read"])
    fid = find_folder(token, FOLDER_NAME)
    print(f"Folder '{FOLDER_NAME}' -> {fid}")
    msgs = fetch_messages(token, fid)
    msgs.sort(key=lambda m: m["received"], reverse=True)
    OUT.write_text(json.dumps(msgs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Geschrieben: {OUT}  ({len(msgs)} Mails)")


if __name__ == "__main__":
    main()
