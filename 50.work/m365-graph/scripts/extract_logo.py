#!/usr/bin/env python3
"""
extract_logo.py
---------------
Sucht die jüngste Mail von Giovanni mit Inline-Bild contentId 'miragliabi-logo'
und speichert die Bytes als miraglia_logo.<ext> im Script-Verzeichnis.
"""
import base64
import os
import sys
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".token_cache.bin"


def get_token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    result = None
    for acc in app.get_accounts():
        result = app.acquire_token_silent(SCOPES, account=acc)
        if result:
            break
    if not result:
        sys.exit("Kein Token im Cache — vorher inspect_signature.py / mail_digest.py laufen lassen.")
    if "access_token" not in result:
        sys.exit(f"Login fehlgeschlagen: {result.get('error_description')}")
    return result["access_token"]


def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Letzte 50 Mails durchsuchen, Mails von Giovanni mit Anhang
    url = (
        f"{GRAPH}/me/messages"
        f"?$select=id,subject,receivedDateTime,from,hasAttachments"
        f"&$top=50"
        f"&$orderby=receivedDateTime desc"
    )
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    for m in r.json().get("value", []):
        frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
        if frm != "giovanni@miraglia-bi.com":
            continue
        # Auch ohne hasAttachments=True versuchen (Inline-Images sind manchmal nicht geflagged)
        r2 = requests.get(
            f"{GRAPH}/me/messages/{m['id']}/attachments",
            headers=headers, timeout=30,
        )
        if not r2.ok:
            continue
        atts = r2.json().get("value", [])
        if not atts:
            continue
        print(f"  Mail {m['subject'][:50]}: {len(atts)} Anhänge")
        for att in atts:
            cid = att.get("contentId") or ""
            name = att.get("name") or ""
            is_inline = att.get("isInline", False)
            ctype = att.get("contentType", "")
            if "miragliabi-logo" in cid.lower() or (is_inline and "image" in ctype):
                data_b64 = att.get("contentBytes")
                if not data_b64:
                    continue
                data = base64.b64decode(data_b64)
                ext = "png"
                if "jpeg" in ctype or "jpg" in ctype:
                    ext = "jpg"
                elif "gif" in ctype:
                    ext = "gif"
                out = SCRIPT_DIR / f"miraglia_logo.{ext}"
                out.write_bytes(data)
                print(f"✓ Logo gespeichert: {out}")
                print(f"  Source-Mail: {m.get('subject')} ({m.get('receivedDateTime')[:10]})")
                print(f"  contentId:   {cid}")
                print(f"  contentType: {ctype}")
                print(f"  isInline:    {is_inline}")
                print(f"  Size:        {len(data)} bytes")
                return
    print("Kein Logo gefunden.")


if __name__ == "__main__":
    main()
