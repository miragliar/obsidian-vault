#!/usr/bin/env python3
"""Speichert den HTML-Body des jüngsten MVM-Drafts als preview_draft.html für Sichtkontrolle."""
import os
import sys
from pathlib import Path
import msal, requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]
CACHE_FILE = Path(__file__).resolve().parent / ".token_cache.bin"
OUT = Path(__file__).resolve().parent / "preview_draft.html"


def tok():
    c = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        c.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}", token_cache=c)
    for a in app.get_accounts():
        r = app.acquire_token_silent(SCOPES, account=a)
        if r:
            return r["access_token"]
    sys.exit("kein cache")


t = tok()
h = {"Authorization": f"Bearer {t}"}
msgs = requests.get(
    f"{GRAPH}/me/mailFolders/drafts/messages"
    f"?$select=id,subject,body,hasAttachments"
    f"&$top=1&$orderby=createdDateTime desc",
    headers=h,
).json().get("value", [])
if not msgs:
    sys.exit("keine Drafts")
m = msgs[0]
print(f"Subject:        {m['subject']}")
print(f"hasAttachments: {m['hasAttachments']}")
html = m.get("body", {}).get("content", "")
print(f"Body length:    {len(html)} chars")
# Anhänge listen
atts = requests.get(f"{GRAPH}/me/messages/{m['id']}/attachments", headers=h).json().get("value", [])
print(f"Attachments:    {len(atts)}")
for a in atts:
    print(f"  - {a.get('name')}  contentId={a.get('contentId')}  isInline={a.get('isInline')}  size={a.get('size')}B")
OUT.write_text(html, encoding="utf-8")
print(f"\nHTML → {OUT}")
