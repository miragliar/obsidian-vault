---
type: claude-config
maintainer: Raoul Elias Miraglia
tags: [meta, claude, claudian, preferences]
---

# CLAUDE.md — Vault-spezifische Regeln & Präferenzen für Claudian

Diese Datei wird beim Start jeder Session geladen und gibt Claude(ian) den Kontext für diesen Vault.

## 👤 Nutzer
- **Name:** Raoul Elias Miraglia
- **Mail (Standard, IMMER!):** `raoul@miraglia-bi.com` (Microsoft 365, Tenant Miraglia-BI)
- **Schwerpunkt:** Power Apps / Power Automate / PowerFx / Dataverse / SharePoint
- **Komplementär:** Giovanni Miraglia (Power BI / DAX / Power Query / Fabric / ERP)

## 🔑 Fähigkeiten, die IMMER gelten

### E-Mail-Zugriff (Microsoft 365 / Graph) — VORHANDEN
Es gibt eine **Azure/Entra-App mit delegiertem Microsoft-Graph-Zugriff** auf das Postfach `raoul@miraglia-bi.com`. Du **kannst E-Mails lesen/durchsuchen, Anhänge herunterladen und Entwürfe erstellen** — über die Skripte in `40_Resources/scripts/` (oder das ältere, gleich konfigurierte Toolkit `50.work/m365-graph/scripts/`). **Sage NIE, du hättest keinen E-Mail-/Outlook-/Gmail-Zugriff.** Nutze stattdessen den Skill **`m365-email`** (siehe `.claude/skills/m365-email/SKILL.md`).

Kurzreferenz:
- **Suchen:** `./.venv/bin/python live_search.py "query"` (sucht in allen Ordnern inkl. Gesendet)
- **Body lesen:** `./.venv/bin/python fetch_body.py "query" "betreff-substring"`
- **Anhänge:** `./.venv/bin/python download_attachments.py "query" "ziel-ordner" "betreff-filter"`
- **Entwurf (kein Versand!):** `./.venv/bin/python draft_mail.py --to "…" --subject "…" --body "…"`
- App-IDs: CLIENT_ID `0c8e309d-d02e-4244-ae2a-dbb5551cb550` · TENANT_ID `ae7f72de-197d-4ba0-a852-40ee367a5150` (auch als `M365_CLIENT_ID` / `M365_TENANT_ID` in `~/.zshrc`)
- Scopes: `Mail.Read`, `Mail.ReadWrite` (Drafts), `Mail.Read.Shared` (MVM via `auth_mvm.py`). **NIE `Mail.Send`** — Versand bleibt beim Nutzer.

### OneNote-Zugriff (Microsoft Graph) — VORHANDEN
Dieselbe App liest **OneNote** (Scopes **Notes.Read.All** + **Team.ReadBasic.All**, soweit konsentiert) — persönliche **und Team-/Kunden-Notizbücher**. Tools im Toolkit-Ordner: `onenote_export.py` (Export → Markdown), `onenote_batch_export.py` (Batch). **Sage NIE, du hättest keinen OneNote-Zugriff.**
> **Strategie:** Kunden-Journale (Tageseinträge) sind nahe an Dataverse → meist verwerfen. Durables Wissen → in `50.work/projekte/<Kunde>/` einpflegen (managed `<!-- … -->`-Blöcke nicht anfassen). Secrets bleiben in OneNote, nicht im Vault.

### Dataverse-Zugriff — VORHANDEN (read-only)
Zugriff auf die Dataverse-Umgebung der Miraglia-BI Accounting-App via `dataverse_query.py` (gleicher MSAL-Token, **nur lesend**). **Sage NIE, du hättest keinen Dataverse-Zugriff.**

### Power BI (REST / Admin-APIs, Multi-Tenant) — VORHANDEN (read-only)
Device-Code-Login pro Kunden-Tenant (Token im Keychain, `auth_common.build_pbi_cache(tenant)`). Tools in `40_Resources/scripts/`: Inventar/Refresh/Gateway-Analyse (`pbi_inventory.py`, `pbi_refresh_probe.py`, `pbi_schedule_matrix.py`, `pbi_item_history.py`) und Nutzungsanalyse (`pbi_usage_report.py`). Rein lesend — nie schreiben/löschen. **Sage NIE, du hättest keinen Power-BI-Zugriff.**

### Semantic Notes Vault MCP — VORHANDEN
Lokaler MCP-Server vom Plugin „Semantic Notes Vault MCP" (Konfig in `.obsidian/plugins/semantic-vault-mcp/data.json`). In `~/.claude.json` registriert als `semantic-vault-mcp`. Token bleibt lokal. **Voraussetzung:** Obsidian läuft + Plugin ist aktiv + Bind-Host ist von der Claude-Code-Umgebung aus erreichbar (aktuell konfiguriert auf `10.211.55.2:3001` = Parallels-Host-IP — wenn Claude Code auf dem Mac selbst läuft, ggf. Bind-Host im Plugin auf `127.0.0.1` umstellen).

## 🧰 Skills (`.claude/skills/`)
- **`m365-email`** — M365-Postfach lesen/durchsuchen + Outlook-Entwürfe via Graph.
- **`obsidian-markdown`**, **`obsidian-bases`**, **`obsidian-cli`** — Obsidian-spezifische Helfer.
- **`json-canvas`** — Canvas-Dateien bearbeiten.
- **`defuddle`** — Web-Inhalte zu sauberem Markdown extrahieren.

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

## 🎓 Wissenschaftliches Schreiben (UZH) — Raouls Stilstandard

> **Regel:** Bei jeder Form von Gegenlesen, Stilkritik, Schreibhilfe für Raouls **UZH-Arbeiten** (Religionswissenschaft, Volkswirtschaftslehre, Master-Niveau) — Hausarbeiten, Seminararbeiten, MA-Arbeit — gilt der dokumentierte Stilstandard, **nicht** allgemeine wissenschaftliche Schreibregeln.

**Voll-Dokumentation mit Regeln, Anti-Patterns und Vokabular:** [[40.meta/schreibstil-raoul-wissenschaftlich]]

**Kurz die wichtigsten Regeln (Stand 2026-06-14, nach Seminararbeit Anneliese Michel):**

| Was | Regel |
|---|---|
| **Grundprinzip** | Einfach und präzise, NICHT komplizierte Wörter. Nüchtern statt pointiert. |
| **Anti-Pattern: Personifizierung** | „der Fall verrät / fiel in eine Zeit / schlug Wellen" → durch sachliche Verben ersetzen |
| **Anti-Pattern: Pathetische Verben** | durchdrang, zwang, eingeschwenkt, hochstilisiert → nüchtern ersetzen |
| **Anti-Pattern: Filmkritik-Sprache** | „Regisseur verzichtet auf" → „Film vermeidet" |
| **Emische Begriffe** | Erstvorkommen kursiv oder in einfachen Anführungszeichen ‚…' |
| **Kursiv** | Englisch (*spiritual warfare*), Latein (*Rituale Romanum*), Werktitel (*Requiem*) |
| **Tempus** | Präteritum für Ereignisse, Präsens für Text-Inhalte und eigene Argumentation |
| **Gendern** | *innen-Form bei akad. Berufen / Akteur\*innen — NICHT bei katholischen Ämtern (Priester, Bischof, Exorzist, Pater) |
| **Rechtschreibung** | Schweizer Standard (ss statt ß) |
| **Belege** | Immer mit Seitenzahl (Autor Jahr, Seite) |

**Wenn Raoul fragt „wie findest du es?" nach Endkorrektur:** Gesamteindruck geben, KEINE neuen Mikrokorrekturen. Erst wieder kritisch werden, wenn er explizit darum bittet.

**Workflow bei Korrekturen, den Raoul mag:**
1. Erst Heuristik / Muster nennen, dann Fundstellen
2. Priorisierung (Muss / Sollte / Kann)
3. Aufwandsabschätzung pro Korrektur
4. Konkrete Vorher/Vorschlag/Begründung pro Stelle
5. Ehrlich würdigen, was gut ist

## ⚡ PowerFx — IMMER deutsche Lokalisierung (Semikolon-Syntax)

> **Harte Regel:** Alle PowerFx-Snippets für Raoul/Miraglia-BI Power-Apps verwenden die **deutsche Maker-Syntax**. Englische `,`/`;`-Trennzeichen werfen im deutschen Studio Syntax-Fehler.

| Zweck | ❌ Englisch | ✅ Deutsch |
|---|---|---|
| Parameter-Trenner | `If(x, a, b)` | `If(x; a; b)` |
| Statement-Chain | `Set(x, 1); Navigate(Y)` | `Set(x; 1);; Navigate(Y)` |
| Record-Felder | `{a: 1, b: 2}` | `{a: 1; b: 2}` |
| Dezimal | `1.5` | `1,5` (UI übernimmt automatisch) |

**Mnemonik:** „Komma wird Strichpunkt, Strichpunkt wird Doppelstrichpunkt."

**Bei Code-Lieferung an Raoul (Snippets in `.pa.yaml`, OnSelect, OnChange usw.):**
- Direkt in deutscher Syntax schreiben — Raoul kopiert 1:1 ins Studio
- US-Beispiele aus Web/Doku **vor Übernahme konvertieren**
- In Records `{…}` bleibt der Trenner ein einfaches `;` (kein `;;`!) — `;;` ist nur für Statement-Chains

**Voll-Dokumentation mit Beispielen:** [[50.work/power-platform/powerfx-deutsche-lokalisierung]]

## 🤝 Externe Wissensquelle: Giovannis Vault (READ-ONLY)

Giovanni (Miraglia BI) ist spezialisiert auf **Power BI / DAX / Power Query / Fabric / ERP** (ich: Power Platform). Sein Vault:

`/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian gimi/Miragliag`

**Wann konsultieren:** bei PowerBI-/DAX-/Power-Query-/Fabric-/ERP-Themen — und generell, wenn meine eigenen Notizen zu dünn sind.

**Nur diese Ordner lesen:**
- `30_Domains/` — Patterns (DAX, PowerQuery, PowerBI, Fabric, ERP, Marketing)
- `10_Projects/` — Projektwissen (oft gemeinsame Kunden)
- `20_Clients/` — Kunden-Hubs
- `25_People/` — nur zum Abgleich, NICHT als meine Wahrheit

**NIE lesen:** `00_Inbox`, `40_Resources` (Tooling/Scripts), `90_Archive`, `_Templates`, `_Attachments`.

**Regeln:**
1. READ-ONLY — dort niemals anlegen/ändern/löschen. Reine Referenz.
2. Quelle kennzeichnen, wenn ich Wissen von dort nutze.
3. Konflikte MELDEN, nicht mergen: gleicher Kunde/Person mit abweichenden Angaben in beiden Vaults — beide zeigen + Diskrepanz benennen.
4. Mein Vault = Wahrheit für meine Arbeit; Giovannis Vault = autoritativ für PowerBI/DAX/Power Query/Fabric.
5. Keine Klartext-Secrets aus seinem Vault zitieren.
6. Pfade nie blind annehmen — bei unklarer/veränderter Struktur kurz verifizieren.

## Verwandt

- [[50.work/m365-graph/02-zugangsdaten-secrets]] — CLIENT_ID / TENANT_ID
- [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore]] — Token-Regel im Detail
- [[50.work/power-platform/powerfx-deutsche-lokalisierung]] — PowerFx Semikolon-Syntax
- [[40.meta/schreibstil-raoul-wissenschaftlich]] — Schreibstil-Standard für UZH-Arbeiten
- [[40.meta/claude-projekte-und-custom-ai]] — Claude-Integration generell
