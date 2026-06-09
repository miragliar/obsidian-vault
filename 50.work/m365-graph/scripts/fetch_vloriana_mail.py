#!/usr/bin/env python3
"""Holt den vollen Body von Vlorianas Mail (personal@mvm-ag.ch, 2026-06-03)."""
import sys
from pathlib import Path

import requests

# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr als
# Klartext-.bin im Vault/Dropbox. Regel: Tokens IMMER verschlüsselt im Keystore.
from auth_common import GRAPH, get_token

SCOPES = ["User.Read", "Mail.Read"]
OUT = Path(__file__).resolve().parent / "vloriana_mail.html"

t = get_token(SCOPES)
h = {"Authorization": f"Bearer {t}"}
# Letzte 100 Mails durchgehen, Mail von personal@mvm-ag.ch am 2026-06-03 finden
url = (
    f"{GRAPH}/me/messages"
    f"?$select=id,subject,receivedDateTime,from,body"
    f"&$top=100&$orderby=receivedDateTime desc"
)
r = requests.get(url, headers=h).json()
for m in r.get("value", []):
    frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
    dt = m.get("receivedDateTime", "")
    subj = m.get("subject", "")
    if frm == "personal@mvm-ag.ch" and dt.startswith("2026-06-03") and "Abschlusszeugnis" in subj:
        html = m.get("body", {}).get("content", "")
        OUT.write_text(html, encoding="utf-8")
        print(f"✓ Gefunden: {dt[:19]}  „{subj}\"")
        print(f"  → {OUT} ({len(html)} chars)")
        # Letzte 800 chars zeigen — meist Signatur
        text = html.replace("<br>", "\n").replace("</p>", "\n").replace("&nbsp;", " ")
        import re
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\n+", "\n", text)
        print("\n--- Letzte ca. 1000 Zeichen (Signatur-Bereich) ---")
        print(text[-1200:])
        sys.exit(0)
print("Mail nicht gefunden.")
