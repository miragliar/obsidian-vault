---
source: claude-import
imported: 2026-06-05
from: giovanni@miraglia-bi.com
to: michael@kipfer-dp.com
cc: raoul@miraglia-bi.com
date: 2026-06-04
type: email-archiv
tags: [miraglia, mail, m365, setup-auftrag, v2-toolkit]
status: importiert-juni-2026
---

# Mail Giovanni — M365-Toolkit v2 (Juni 2026, CC an Raoul)

Mail mit dem v2-Toolkit als Anhang, primär an Michael, CC an Raoul. Da Raoul **dieselbe Azure-App wie Giovanni** nutzt, ist alles was Giovanni an Michael delegiert (App-Berechtigungen, Admin-Consent) für Raoul bereits erledigt.

→ Importiert nach `50.work/m365-graph/scripts/` am 2026-06-05.

## Anhänge (28 Stück, gezogen via Graph)

Liste & SHA256-Hashes: siehe `scripts/_staging-v2/_manifest.json` (lokal, gitignored).

Kategorien:
- **Auth & Infrastruktur:** `auth_common.py`, `requirements.txt`
- **Mail/Teams/Personen-Sync:** `mail_digest.py`, `teams_digest.py`, `m365_people_sync.py`, `apply_mail_summaries.py`, `first_contact.py`, `teams_first_contact.py`, `create_teams_people.py`, `contact_stats.py`
- **Kunden-Akten:** `link_people_to_clients.py`, `fill_stakeholders.py`, `apply_firmenprofile.py`
- **Mail-Werkzeuge:** `live_search.py`, `fetch_body.py`, `draft_mail.py`, `draft_with_attach.py`
- **Kalender:** `create_event.py`
- **OneNote:** `onenote_export.py`, `onenote_batch_export.py`, plus `_distill_playbook.md` (Destillations-Strategie)
- **Wochen-Pipeline:** `weekly_refresh.sh`, `weekly_report.py`
- **Dataverse (optional):** `dataverse_query.py`
- **Doku:** `ANLEITUNG.md` (Hauptanleitung), `IMPORT-ANLEITUNG-Michael.md` (Adressaten-spezifisch), `README.md` (Kurz-Setup)
- **Assets:** `miraglia-bi.png`

## Original-Mail-Body (verbatim)

> Lieber Michael,
>
> super, dass das erste Paket so reibungslos lief! 🎉 Ich habe inzwischen die Azure-/Entra-App-Berechtigungen deutlich erweitert und das Skript-Toolkit ausgebaut. Damit du alles 1:1 übernehmen kannst, hängt hier das komplette, aktualisierte Toolkit als Anhang.
>
> Neu dazugekommen:
> - 📅 Kalender-Termine (`create_event.py`)
> - 📓 OneNote → Markdown, inkl. Team-/Kunden-Notizbücher (`onenote_export.py`)
> - 👤 Personen-/Kunden-Sync, Interaktions-Statistik, Erstkontakt, Stakeholder
> - ✉️ Entwürfe mit Anhängen (`draft_with_attach.py`)
> - 🔄 Wöchentlicher Auto-Job · 🗄️ optional Dataverse-Abfrage
> - 🔐 Token jetzt verschlüsselt im macOS-Keychain (statt Klartext-Datei)
>
> Neue Berechtigungen (in deiner App ergänzen + Admin-Consent): `People.Read`, `Contacts.Read`, `Mail.Read.Shared`, `Calendars.ReadWrite`, `Notes.Read.All`, `Team.ReadBasic.All`, optional `Sites.Read.All`.

## Was bei Raoul anders ist als in der Anleitung

Die Anleitung wurde für Michaels Vault-Struktur geschrieben (PARA mit Unterstrich: `25_People/`, `20_Clients/`, `40_Resources/scripts/`, `00_Inbox/`). Bei Raoul:

| Anleitung | Raouls Vault |
|---|---|
| `40_Resources/scripts/` | `50.work/m365-graph/scripts/` |
| `25_People/` | `50.work/25_People/` ✓ (Pfad-Auto-Detect über `SCRIPT_DIR.parent.parent = 50.work/` greift) |
| `20_Clients/` | `50.work/26_Firmen/` ⚠️ **Mapping nötig** für Phase-3-Skripte |
| `00_Inbox/` | (nicht vorhanden) ⚠️ **Mapping nötig** für Wochen-Report |
| `30_Domains/` | (nicht vorhanden) — nur für OneNote-Knowledge-Notebooks relevant |

## Import-Status (Stand 2026-06-05)

- ✅ **Phase 1** — Auth-Refactor + Keychain-Migration abgeschlossen (`auth_common.py`, `mail_digest.py v2`, `teams_digest.py v2`, Token im Keychain `MiragliaBI-M365 / graph-token-cache`).
- ✅ **Phase 2** — 8 strukturneutrale Skripte installiert (`live_search`, `fetch_body`, `draft_mail`, `draft_with_attach`, `create_event`, `onenote_export`, `onenote_batch_export`, `dataverse_query`).
- ✅ **Phase 3** — 11 struktur-abhängige Skripte mit Env-Var-Patch für Pfade installiert. Vault-spezifische Werte in `scripts/.env`:
  - `PEOPLE_DIR=25_People` (Default, passt zufällig)
  - `CLIENTS_DIR=26_Firmen` (statt Michaels `20_Clients`)
  - `INBOX_DIR=m365-graph/_inbox` (statt Michaels `00_Inbox` — Wochen-Report landet im Tech-Bereich; ggf. später auf `60.daily` umstellen)
  - `weekly_refresh.sh` lädt `.env` automatisch via `source .env`. Manuelle CLI-Aufrufe brauchen `set -a && source .env && set +a` im scripts-Ordner.

## Verifizierter End-to-End-Test (2026-06-05)

```
Env-Vars: PEOPLE_DIR=25_People  CLIENTS_DIR=26_Firmen  INBOX_DIR=m365-graph/_inbox
fill_stakeholders.py (Trockenlauf) → 25_People: 29 Notizen, 26_Firmen: 14 Notizen → "nichts geschrieben"
```

## Nächste Schritte (optional)

1. **Erste echte Pipeline-Runs** — empfohlene Reihenfolge laut [[07-anleitung-v2-toolkit]] TEIL 3:
   ```bash
   cd 50.work/m365-graph/scripts
   set -a && source .env && set +a
   ./.venv/bin/python m365_people_sync.py --with-mail        # neue Kontakte aus People/Contacts/Mail
   ./.venv/bin/python mail_digest.py --top 0 --max 5000 --min-total 4 --sort sent
   ./.venv/bin/python first_contact.py --apply               # kontakt_seit
   ./.venv/bin/python teams_digest.py --max-chats 600
   ./.venv/bin/python teams_first_contact.py --apply
   ./.venv/bin/python contact_stats.py --apply               # Interaktions-Stats
   ./.venv/bin/python link_people_to_clients.py --apply      # 26_Firmen-Linking
   ./.venv/bin/python fill_stakeholders.py --apply
   ```
2. **launchd-Job** (Wochen-Refresh) — vor Aktivierung `weekly_refresh.sh` einmal manuell testen.
3. **Claude-gestützte Schritte** (TEIL 4 der Anleitung) — `mail_summaries*.json`, `teams_people.json`, `firmenprofile.json` in scripts/ ablegen, danach `apply_*` Skripte.

## Verwandt

- [[01-chef-mail-juni-2026]] — erstes Toolkit (v1), April–Juni 2026
- [[02-zugangsdaten-secrets]] — Client/Tenant-IDs (= Giovannis App)
- [[07-anleitung-v2-toolkit]] — Hauptanleitung v2 (volltext)
- [[08-distill-playbook-onenote]] — OneNote → Obsidian-Destillation
- [[setup-und-workflow]] — Bestehender v1-Workflow
