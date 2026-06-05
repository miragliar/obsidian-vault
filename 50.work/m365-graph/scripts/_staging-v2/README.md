# M365 → Obsidian: Personen-Sync

Zieht via Microsoft Graph (delegiert) deine Kontaktpersonen aus M365 und erzeugt
pro Person eine Notiz in `25_People/`.

## Voraussetzung: App-Registrierung (Entra ID)

1. [entra.microsoft.com](https://entra.microsoft.com) → *App registrations → New registration*
   - Name: `Obsidian Knowledge Sync`, Single tenant, Redirect URI leer.
2. **API permissions → Microsoft Graph → Delegated:** `User.Read`, `People.Read`,
   `Contacts.Read`, (optional) `Mail.Read` → **Grant admin consent**.
3. **Authentication → Allow public client flows → Yes**.
4. **Application (client) ID** und **Directory (tenant) ID** notieren.

## Setup (Terminal, im Ordner dieses Scripts)

```bash
cd "40_Resources/scripts"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export M365_CLIENT_ID="<deine-client-id>"
export M365_TENANT_ID="<deine-tenant-id>"
```

(Alternativ die beiden IDs direkt oben im `.py` eintragen.)

## Ausführen

```bash
python3 m365_people_sync.py             # People + Contacts
python3 m365_people_sync.py --with-mail # + letzter Kontakt/Häufigkeit aus Mails
python3 m365_people_sync.py --force     # bestehende Notizen überschreiben
```

Beim ersten Lauf erscheint ein Device-Code → im Browser unter
`microsoft.com/devicelogin` eingeben und als `giovanni@miraglia-bi.com` anmelden.
Der Token wird in `.token_cache.bin` gecacht (per `.gitignore` vom Commit ausgeschlossen).

## Sicherheit

- Kein Client-Secret nötig (Public Client + Device-Code).
- `.token_cache.bin` enthält ein Zugriffstoken → **nicht** committen/teilen (ist ignoriert).
- Bestehende Notizen werden standardmäßig **nicht** überschrieben (manuelle Edits bleiben).
