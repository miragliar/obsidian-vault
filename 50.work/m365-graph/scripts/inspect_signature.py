#!/usr/bin/env python3
"""
inspect_signature.py
--------------------
Holt die jüngste Mail von Giovanni Miraglia (giovanni@miraglia-bi.com) im
HTML-Format und schreibt den Body als giovanni_sample.html ins Script-Verzeichnis.

So sehen wir die echte HTML-Struktur seiner Signatur (inkl. Logo, Tabellen, etc.)
und können sie 1:1 für Raoul adaptieren.
"""
from pathlib import Path

import requests

# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr als
# Klartext-.bin im Vault/Dropbox. Regel: Tokens IMMER verschlüsselt im Keystore.
from auth_common import GRAPH, get_token

SCOPES = ["User.Read", "Mail.Read"]

SCRIPT_DIR = Path(__file__).resolve().parent
OUT_HTML = SCRIPT_DIR / "giovanni_sample.html"


def main():
    token = get_token(SCOPES)
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
