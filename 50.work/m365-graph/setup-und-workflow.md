---
source: claude-import
imported: 2026-06-01
related_emails: [Giovanni Miraglia 2026-06-01]
tags: [miraglia, m365, microsoft-graph, outlook, teams, automation, obsidian-integration]
---

# M365 Graph → Vault: Setup und Workflow

Setup-Notiz zum Anreichern des Obsidian-Vaults mit Outlook-Mail- und Teams-Chat-Daten via Microsoft Graph. Stammt aus dem Miraglia-Tooling von Giovanni Miraglia (Mail Juni 2026).

## Problem

Personen-/Klienten-Notizen im Vault (`25_People/<Name>.md`) sollen automatisch mit den letzten Mail- und Chat-Verläufen angereichert werden. Manuell pro Kontakt ist nicht skalierbar, und das wirkliche Wissen über Kunden/Kolleg:innen sitzt verstreut in:

- Outlook-Mail-Verlauf (eingehend + ausgehend)
- Teams-1:1-Chats und Gruppenchats
- Verschiedenen Inhaltskanälen ohne strukturierte Aggregation

## Lösung

Zwei Python-Skripte lesen via Microsoft Graph **delegiert** (nur deine eigenen Daten) die Mails und Chats aus, aggregieren pro Kontakt und schreiben strukturiertes JSON in `scripts/`. Das JSON wird dann an Claude/Claudian gegeben, um Personen-Notizen automatisch zu erweitern.

```
Outlook + Teams              JSON-Aggregation               Vault
─────────────                ────────────────              ─────
mail_digest.py    ─────►     mail_digest.json   ─────►    25_People/*.md
teams_digest.py   ─────►     teams_digest.json  ─────►    (mit <!-- mail-summary --> Marker)
```

## Voraussetzungen

- **Python 3.10+**
- Pakete `msal` und `requests`
- M365-Konto im **gleichen Tenant** wie die App-Registrierung (Miraglia-BI)
- App-Registrierung mit delegierten Permissions:
  - `User.Read` (Standard)
  - `Mail.Read` (für mail_digest.py)
  - `Chat.Read` (für teams_digest.py)
  - 🆕 `Mail.ReadWrite` (für `draft_replies_mvm.py` — Reply-Drafts erstellen + Body patchen + Inline-Attachments)
- Admin-Consent für die App-Registrierung — **bereits erteilt** von Giovanni (alle obigen Scopes, inkl. Mail.ReadWrite, Stand 2026-06-04 verifiziert)

## Einmalige Einrichtung

### 1. Virtuelle Umgebung & Pakete

```bash
cd "/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul/50.work/m365-graph/scripts"

python3 -m venv .venv
source .venv/bin/activate           # macOS/Linux
# Windows PowerShell:  .venv\Scripts\Activate.ps1

pip install msal requests
```

### 2. Umgebungsvariablen setzen

Werte aus der separaten Mail von Giovanni (siehe [[02-zugangsdaten-secrets]] — **nicht extern teilen**).

```bash
# macOS / Linux (z.B. in ~/.zshrc oder direkt im Terminal pro Session):
export M365_CLIENT_ID="<<aus separater Mail>>"
export M365_TENANT_ID="<<aus separater Mail>>"

# Alternative: .env-Datei (siehe scripts/.env.example) und mit
# `source .env` oder via Tool wie `direnv` automatisch laden
```

```powershell
# Windows PowerShell:
$env:M365_CLIENT_ID="<<aus separater Mail>>"
$env:M365_TENANT_ID="<<aus separater Mail>>"
```

### 3. Erstmalige Anmeldung (Device-Code)

```bash
python3 mail_digest.py
```

Beim ersten Lauf:

1. Skript zeigt einen **Device-Code** + URL `https://microsoft.com/devicelogin`
2. URL im Browser öffnen, Code eingeben
3. Mit **eigenem M365-Konto** anmelden (Raoul, `raoul@miraglia-bi.com`)
4. Permissions bestätigen (Mail.Read bzw. Chat.Read)
5. Token wird verschlüsselt im **macOS Keychain** gecacht (`MiragliaBI-M365` / `graph-token-cache`, via `msal_extensions.KeychainPersistence`) → folgende Aufrufe ohne erneutes Login. **NICHT** mehr als Klartext-`.bin`-Datei im Vault.

Bei `teams_digest.py` erscheint ein **separater** Device-Code, weil andere Scopes (`Chat.Read`) gebraucht werden.

## Verwendung

### Mail-Digest

```bash
# Standard: Top 20 Kontakte, letzte 2'500 Mails
python3 mail_digest.py

# Mehr scannen, mehr Kontakte ausgeben
python3 mail_digest.py --top 30 --max 4000

# Nur Kontakte, denen du ≥10x geantwortet hast (relevante Mit-Aktivität)
python3 mail_digest.py --min-sent 10 --sort sent

# Alle Kontakte (kein Cap)
python3 mail_digest.py --top 0
```

**Output:** `scripts/mail_digest.json` mit Struktur:

```json
{
  "me": "raoul@miraglia-bi.com",
  "scanned_max": 2500,
  "top_n": 20,
  "people": [
    {
      "file": "<Notiz-Dateiname>",
      "email": "...",
      "total": 42, "recv": 25, "sent": 17,
      "last": "2026-05-29",
      "has_summary": false,
      "msgs": [
        { "d": "2026-05-29", "dir": "in", "subj": "...", "prev": "..." },
        ...
      ]
    }
  ],
  "frequent_without_note": [
    { "email": "...", "total": 33 }
  ]
}
```

### Teams-Digest

```bash
# Standard: 300 Chats, 80 Nachrichten pro Chat
python3 teams_digest.py

# Mehr Chats / weniger pro Chat
python3 teams_digest.py --max-chats 500 --per-chat 50
```

**Output:** `scripts/teams_digest.json` mit Struktur:

```json
{
  "me": "raoul@miraglia-bi.com",
  "chats_scanned": 280,
  "messages_scanned": 12450,
  "people": [
    {
      "name": "...", "email": "...", "domain": "kunde.ch",
      "interactions": 87,
      "msgs_from": 50, "my_replies_1to1": 37,
      "in_1to1": 65, "in_group": 22,
      "last": "2026-05-30",
      "samples": [ { "d": "...", "type": "oneOnOne", "text": "..." } ]
    }
  ],
  "group_chats": [
    { "topic": "...", "members": [...], "msg_count": 142, "last": "..." }
  ]
}
```

## Vault-Integration

### Personen-Notizen-Konvention

Das Skript erwartet:

```
<Vault>/25_People/<Name>.md
```

Mit Frontmatter inkl. `email:`-Zeile:

```markdown
---
name: Max Muster
email: max@kunde.ch
firma: Kunde AG
tags: [kunde, miraglia]
---

# Max Muster

…Notizen…

<!-- mail-summary -->
…Hier kommt die KI-generierte Zusammenfassung rein…
<!-- /mail-summary -->
```

Der `<!-- mail-summary -->`-Marker ist die Anker-Stelle, an der Claude die generierte Kurz-Zusammenfassung einfügt. So bleibt der Rest der Notiz unangetastet.

→ Eine **Vorlage** für diese Notizen liegt unter [[03-personen-notiz-vorlage]].

### Workflow: Anreicherung via Claude/Claudian

Nach Lauf der Skripte:

```
@Claudian: Lies 50.work/m365-graph/scripts/teams_digest.json und 
50.work/m365-graph/scripts/mail_digest.json. Erweitere die Personen-Notizen 
in 25_People/ um eine Kurz-Zusammenfassung der wichtigsten Kontakte. 
Schreibe zwischen <!-- mail-summary --> und <!-- /mail-summary -->:
- Anzahl Interaktionen (Mail + Teams)
- Top 3 Themen der letzten Wochen
- Offene Punkte / Erwartete Antworten
- Datum letzter Kontakt
Existierende Notizinhalte außerhalb der Marker bleiben unverändert.
```

### Refresh-Strategie

| Frequenz | Aktion |
|---|---|
| **Wöchentlich** | `mail_digest.py` + `teams_digest.py` neu laufen lassen, Claudian erneut anreichern |
| **Pro Klient-Meeting** | Vor dem Meeting digest neu generieren, Personen-Notiz öffnen |
| **Bei neuem Kontakt** | Notiz in `25_People/` anlegen → beim nächsten Lauf wird sie automatisch in `people:` aufgenommen |

`frequent_without_note` im Output zeigt **häufige Kontakte ohne Notiz** — Hinweis, wo eine neue Personen-Notiz Sinn machen würde.

## Sicherheit & Datenschutz

> 🔐 **Regel (Giovanni 2026-06-09):** Tokens IMMER verschlüsselt im OS-Keystore
> (macOS Keychain / Windows DPAPI), NIE als Klartext-`.bin` im Vault/Dropbox.
> Implementiert via `auth_common.build_cache()` (M365) und
> `auth_common.build_pbi_cache(tenant)` (Power BI multi-tenant). Beides nutzt
> `msal_extensions.PersistedTokenCache` mit `KeychainPersistence`. Auf Windows
> wählt `msal_extensions.build_encrypted_persistence()` automatisch DPAPI.

| Risiko | Mitigation |
|---|---|
| Access-/Refresh-Token könnte als Klartext im Vault landen | **Keychain-Cache** via `auth_common.py` (Service `MiragliaBI-M365`, Account `graph-token-cache`). Klartext-`.bin` ist im Repo verboten. |
| Falls doch eine `.bin` entsteht (alter Skript-Stand) | `.gitignore` blockiert `*.bin`, `.token_cache*`, `.pbi_token_cache_*` — Defense-in-Depth. Vor jedem Commit `git status` checken. |
| `mail_digest.json` / `teams_digest.json` enthalten echte Mail-/Chat-Inhalte | `.gitignore`, **bleiben lokal**, kein Cloud-Sync außerhalb Dropbox-Privatordner |
| `M365_CLIENT_ID` / `M365_TENANT_ID` | Public Client (kein Secret), aber Tenant-Identifier — nicht öffentlich teilen |
| Sensitive Mails versehentlich von Claude/KI verarbeitet | Vor Anreicherung prüfen, ob jeder Kontakt für KI-Zusammenfassung geeignet ist |
| Token-Cache zurücksetzen | macOS: Schlüsselbund.app → Eintrag `MiragliaBI-M365` löschen (nicht `rm .token_cache.bin` — die Datei gibt es nicht mehr). |

**Wichtig:** Der Vault liegt in Dropbox-Sync (`Miraglia-BI/0_Internal/`). Genau darum sind Klartext-Token-Caches im Vault verboten — sie würden über Dropbox effektiv in die Cloud kopiert. Der Keychain-Cache lebt außerhalb von Dropbox/iCloud/OneDrive (verschlüsselt, ACL-geschützt).

## Troubleshooting

| Symptom | Wahrscheinliche Ursache | Fix |
|---|---|---|
| `CLIENT_ID/TENANT_ID nicht gesetzt` | Env-Vars in der aktuellen Shell nicht aktiv | `echo $M365_CLIENT_ID` prüfen, Shell-Profile neu sourcen |
| `Device-Flow fehlgeschlagen` | App-Registrierung erlaubt Device-Flow nicht | bei Giovanni rückfragen, `Public Client Flow` muss aktiv sein |
| `403 – fehlt Permission` | Admin-Consent fehlt oder neue Scope nicht freigegeben | bei Giovanni rückfragen |
| `429` (Rate Limit) | zu viele Requests | Skript wartet automatisch; im Notfall `--max` reduzieren |
| Login schlägt wiederholt fehl | falsches Konto verwendet (z.B. privates Outlook) | nur mit `raoul@miraglia-bi.com` anmelden |
| Wenige Kontakte gefunden | `--max` zu niedrig oder lange keine neuen Mails | `--max 5000` + Filterung über `--min-total` |
| Token-Cache korrupt | Cache überlebt App-Reg-Änderungen nicht | macOS: Schlüsselbund-Eintrag `MiragliaBI-M365` löschen + neu anmelden (`./.venv/bin/python live_search.py test`) |

## Wann nicht

- **Wenn du in einem anderen Tenant arbeitest:** Eigene App-Registrierung nötig, neuer Admin-Consent
- **Bei Personen-DSGVO-sensitiven Mails** (Patientenakten, anwaltliche Korrespondenz): nicht durch generische KI-Zusammenfassung schicken — Personen-Notiz dann manuell ohne Marker
- **Bei reiner Read-only-Recherche** zum Setup: Microsoft 365 Admin Center / Graph Explorer kennt die Daten auch — Skripte erst wenn Aggregation gewünscht
- **Bei großen Mengen** (>100k Mails, >1k Chats): bewusst über `--max` begrenzen, nicht alle auf einmal

## Verwandt

- [[50.work/m365-graph/01-chef-mail-juni-2026|Original-Mail Giovanni 2026-06-01]] — Auftrag im Wortlaut
- [[50.work/m365-graph/02-zugangsdaten-secrets|Zugangsdaten]] — CLIENT_ID / TENANT_ID (nicht extern!)
- [[50.work/m365-graph/03-personen-notiz-vorlage|Personen-Notiz-Vorlage]] — Template für 25_People/
- [[50.work/power-platform/_README]] — verwandter Miraglia-Tech-Stack
- [[40.meta/claude-projekte-und-custom-ai]] — Anreicherung via Claude
