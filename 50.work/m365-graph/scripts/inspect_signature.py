#!/usr/bin/env python3
"""
inspect_signature.py
--------------------
Holt die jüngste Mail von Giovanni Miraglia (giovanni@miraglia-bi.com) im
HTML-Format und schreibt den Body als giovanni_sample.html ins Script-Verzeichnis.

So sehen wir die echte HTML-Struktur seiner Signatur (inkl. Logo, Tabellen, etc.)
und können sie 1:1 für Raoul adaptieren.
"""
import os
import sys
from pathlib import Path
from urllib.parse import quote

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".token_cache.bin"
OUT_HTML = SCRIPT_DIR / "giovanni_sample.html"


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
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60)
        print(flow["message"])
        print("=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE_FILE.write_text(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"Login fehlgeschlagen: {result.get('error_description')}")
    return result["access_token"]


def main():
    if not CLIENT_ID or not TENANT_ID:
        sys.exit("M365_CLIENT_ID / M365_TENANT_ID nicht gesetzt.")
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Letzte 50 Mails durchgehen, erste von Giovanni nehmen
    url = (
        f"{GRAPH}/me/messages"
        f"?$select=id,subject,receivedDateTime,from,body"
        f"&$top=50"
        f"&$orderby=receivedDateTime desc"
    )
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    for m in r.json().get("value", []):
        frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
        if frm == "giovanni@miraglia-bi.com":
            html = m.get("body", {}).get("content", "")
            OUT_HTML.write_text(html, encoding="utf-8")
            print(f"✓ Mail von {frm} gefunden:")
            print(f"  Subject: {m.get('subject')}")
            print(f"  Datum:   {m.get('receivedDateTime')}")
            print(f"  Body:    {OUT_HTML} ({len(html)} chars)")
            return
    print("Keine Mail von Giovanni in den letzten 50 gefunden.")


if __name__ == "__main__":
    main()
