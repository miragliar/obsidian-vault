---
type: claude-config
maintainer: Raoul
tags: [meta, claude, claudian, preferences]
---

# CLAUDE.md — Vault-spezifische Regeln & Präferenzen für Claudian

Diese Datei wird beim Start jeder Session geladen und gibt Claude(ian) den Kontext für diesen Vault.

## 📧 E-Mail — bedeutet IMMER `raoul@miraglia-bi.com` (Microsoft 365)

> **HARTE REGEL:** Wenn Raoul „Mail", „E-Mail", „Posteingang", „Inbox", „Nachricht von X", „hat mir geschrieben", „mein Postfach" o. ä. sagt — **immer und ausschließlich** das Office-365-Postfach `raoul@miraglia-bi.com`. NIE Gmail, NIE Google Mail, NIE Hotmail, NIE iCloud, NIE irgendein anderer Provider.
>
> Falls Claude unsicher ist, was gemeint sein könnte: **nicht raten, nicht „Other Provider" anbieten** — direkt das M365-Toolkit benutzen.

**Warum:** Die Geschäfts-Mail von Raoul (und damit alle relevanten Mails von Giovanni, Kunden, MVM-AG, Reto, Remo, Vloriana, etc.) läuft ausschließlich über **`raoul@miraglia-bi.com`** (Microsoft 365 / Tenant Miraglia-BI). Es gibt kein Gmail-Konto, das geschäftlich relevant wäre.

**Wie zugreifen — IMMER über das bestehende M365-Toolkit:**
```bash
cd 50.work/m365-graph/scripts

# Volltext-Suche im Postfach
./.venv/bin/python live_search.py "stichwort"

# Mail-Body inkl. Body-Text holen
./.venv/bin/python fetch_body.py "betreff-substring"

# Programmatisch (für komplexere Operationen)
./.venv/bin/python -c "
from auth_common import get_token, GRAPH
import requests
tok = get_token(['Mail.Read'])
r = requests.get(GRAPH + '/me/messages?\$search=\"foo\"', headers={'Authorization': f'Bearer {tok}'})
"
```

**Tenant-Mapping:**
| Tenant / Postfach | Wer | Auth |
|---|---|---|
| `raoul@miraglia-bi.com` (Standard!) | Raoul, Giovanni, alle Miraglia-BI-Mails | `from auth_common import get_token` |
| MVM-AG Tenant (Reto, Remo, Christoph, …) | Shared Mailbox `personal@mvm-ag.ch` etc. via Mail.Read.Shared | `from auth_mvm import get_token` |

**Anti-Pattern — was nie zu tun ist:**
- ❌ `mcp__claude_ai_Gmail__*` — gar nicht erst ansprechen, kein `authenticate`-Versuch
- ❌ Den User fragen „welcher Mail-Provider?" / „welches Konto?" — die Antwort ist IMMER miraglia-bi.com
- ❌ Annahme, die Mail liege auf Gmail, weil im Mail-Text ein `@gmail.com` vorkommt (das wäre nur ein Kontakt-Empfänger, nicht der Speicherort)
- ❌ Wenn `mcp__claude_ai_Gmail__*` Tools sichtbar werden: **ignorieren**, sie sind irrelevant für diesen Vault
- ❌ Mail-Inhalt erfinden („wahrscheinlich steht da X drin") — stattdessen sofort `live_search.py` / `fetch_body.py` aufrufen

## 🔐 Token-Storage — IMMER verschlüsselt im OS-Keystore

> **Regel (Giovanni 2026-06-09):** Tokens / Secrets **immer verschlüsselt** im OS-Keystore (macOS Keychain / Windows DPAPI), **nie** als Klartext-`.bin`/`.json` im Vault.

Voll-Dokumentation: [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore.md]]

**Implementiert via:** `msal_extensions.KeychainPersistence` (Mac) bzw. `build_encrypted_persistence()` (Windows, DPAPI).

**Konkret bei neuem Code:**
- M365 → `from auth_common import get_token; tok = get_token(SCOPES)`
- MVM-AG → `from auth_mvm import get_token; tok = get_token(SCOPES)`
- Power BI → `from auth_common import build_pbi_cache; cache = build_pbi_cache(tenant)`
- **Nie** `msal.SerializableTokenCache()` mit `.write_text(cache.serialize())` und einer `.bin`-Datei
- `.gitignore` muss `*.bin`, `.token_cache*`, `.pbi_token_cache_*` blockieren
- Vor jedem Commit: `git status` + Diff auf Secrets prüfen

## 🗂️ Vault-Struktur (PARA-ähnlich)

| Pfad | Inhalt |
|---|---|
| `00.index/` | Index- / Übersichtsnotizen |
| `20.studies/` | Studien / Recherchen |
| `30.patterns/` | Code- und Konzept-Patterns |
| `40.meta/` | Vault- / Workflow-Meta |
| `50.work/` | Aktive Projekte (MVM-AG, Koster, Power Platform, M365 Graph) |
| `60.daily/` | Tägliche Notizen |
| `_imports/` | Import-Skripte / Datenströme |

**Wichtige Unterordner:**
- `50.work/m365-graph/` — Microsoft Graph Toolkit (Auth, Mail, Teams, Personen-Sync)
- `50.work/power-platform/` — Power Automate / Power Apps / Power BI
- `50.work/projekte/MVM-AG/` — MVM-AG Projektarbeit (KI-Ausmass, Lohnsystem, …)

## 📝 Notiz-Konventionen

- **Frontmatter** in YAML (zwischen `---`-Linien) für Metadaten, Tags, Quellen-Tracking
- **Wiki-Links** `[[note]]` oder `[[ordner/note]]` (statt plain Pfaden)
- **Tags** mit `#tag` oder im Frontmatter `tags: [tag1, tag2]`
- **Mail-Archive** in eigenen Notizen mit `type: email-archiv` im Frontmatter und Verweis auf importierten Body

## 🔧 Skript-Konventionen

- **Python venv** pro Skript-Ordner (`.venv/`)
- **Default-Tenant/Client-IDs** in `auth_common.py` als Env-Var-Overrides
- **`.env`** im Skript-Ordner für lokale Overrides (in `.gitignore`)
- **`requirements.txt`** für Reproduzierbarkeit
- **Idempotenz** (z. B. alte Drafts mit gleichem Subject löschen vor Neuanlage)

## Verwandt

- [[50.work/m365-graph/02-zugangsdaten-secrets]] — CLIENT_ID / TENANT_ID
- [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore]] — Token-Regel im Detail
- [[40.meta/claude-projekte-und-custom-ai]] — Claude-Integration generell
