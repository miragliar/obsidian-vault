#!/usr/bin/env python3
"""Listet alle aktuellen Drafts im Outlook-Postfach (Subject + Created)."""
import os
import sys
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]
CACHE_FILE = Path(__file__).resolve().parent / ".token_cache.bin"


def token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=cache)
    for acc in app.get_accounts():
        r = app.acquire_token_silent(SCOPES, account=acc)
        if r:
            if cache.has_state_changed:
                CACHE_FILE.write_text(cache.serialize())
            return r["access_token"]
    sys.exit("Kein Token-Cache.")


t = token()
h = {"Authorization": f"Bearer {t}"}
folder = requests.get(f"{GRAPH}/me/mailFolders/drafts?$select=id,totalItemCount", headers=h).json()
print(f"Drafts-Folder: id={folder.get('id')[:30]}…  total={folder.get('totalItemCount')}")
r = requests.get(
    f"{GRAPH}/me/mailFolders/drafts/messages"
    f"?$select=id,subject,createdDateTime,toRecipients"
    f"&$top=20&$orderby=createdDateTime desc",
    headers=h,
)
for m in r.json().get("value", []):
    to = [((x.get("emailAddress") or {}).get("address") or "") for x in (m.get("toRecipients") or [])]
    print(f"  {m['createdDateTime'][:19]}  „{m['subject']}\"  → {to}")
