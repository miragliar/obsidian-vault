#!/usr/bin/env python3
"""Live Graph search using the existing MSAL token cache (silent refresh)."""
import sys, time
from pathlib import Path
import requests

SCRIPT_DIR = Path(__file__).resolve().parent
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.Read", "Mail.Read.Shared", "Contacts.Read", "User.Read"]


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def search_messages(token, query, top=25):
    url = (f"{GRAPH}/me/messages?$search=\"{query}\""
           f"&$select=from,toRecipients,subject,bodyPreview,receivedDateTime,webLink&$top={top}")
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5)))
        r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    r.raise_for_status()
    return r.json().get("value", [])


def search_contacts(token, query):
    url = f"{GRAPH}/me/contacts?$search=\"{query}\"&$top=25"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    if r.status_code >= 400:
        return []
    return r.json().get("value", [])


def fmt(m):
    frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "")
    tos = ", ".join(((r.get("emailAddress") or {}).get("address") or "")
                    for r in (m.get("toRecipients") or []))
    return (f"{m.get('receivedDateTime','')[:16]} | from: {frm} | to: {tos}\n"
            f"  SUBJ: {m.get('subject','')}\n"
            f"  PREV: {(m.get('bodyPreview','') or '').strip()[:280].replace(chr(10),' ')}")


def main():
    token = get_token()
    queries = sys.argv[1:] or ["arai"]
    for q in queries:
        print("\n" + "=" * 70)
        print(f"QUERY: {q}")
        print("=" * 70)
        msgs = search_messages(token, q)
        if not msgs:
            print("  (keine Treffer)")
        for m in msgs:
            print(fmt(m))
            print()


if __name__ == "__main__":
    main()
