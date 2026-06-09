#!/usr/bin/env python3
"""Listet alle aktuellen Drafts im Outlook-Postfach (Subject + Created)."""
import requests

# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr als
# Klartext-.bin im Vault/Dropbox. Regel: Tokens IMMER verschlüsselt im Keystore.
from auth_common import GRAPH, get_token

SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]

t = get_token(SCOPES)
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
