#!/usr/bin/env python3
"""Speichert den HTML-Body des jüngsten MVM-Drafts als preview_draft.html für Sichtkontrolle."""
import sys
from pathlib import Path

import requests

# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr als
# Klartext-.bin im Vault/Dropbox. Regel: Tokens IMMER verschlüsselt im Keystore.
from auth_common import GRAPH, get_token

SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]
OUT = Path(__file__).resolve().parent / "preview_draft.html"

t = get_token(SCOPES)
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
