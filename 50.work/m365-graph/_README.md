---
source: claude-import
imported: 2026-06-01
type: cluster-readme
context: Miraglia Business-Intelligence
tags: [m365, microsoft-graph, automation, miraglia]
---

# M365 Graph → Vault-Anreicherung

Tooling zur automatischen Anreicherung von Personen-/Klienten-Notizen mit Outlook-Mail- und Teams-Chat-Daten via Microsoft Graph. Initiiert durch Giovanni Miraglia (Mail Juni 2026).

## Inhalt

- [[setup-und-workflow|Setup-und-Workflow]] — vollständige Anleitung (Voraussetzungen, Einrichtung, Verwendung, Sicherheit, Troubleshooting)
- [[01-chef-mail-juni-2026|Chef-Mail (Original-Wortlaut + To-Dos)]]
- [[02-zugangsdaten-secrets|Zugangsdaten — CLIENT_ID / TENANT_ID]] (intern, nicht extern teilen)
- [[03-personen-notiz-vorlage|Personen-Notiz-Vorlage]] für `25_People/`
- [[04-company-enrich-workflow|Firmen-Steckbrief Workflow (Webseite + Zefix)]]

## Scripts

```
scripts/
├─ mail_digest.py        — Outlook-Mails (Scope Mail.Read)
├─ teams_digest.py       — Teams-Chats 1:1 + Gruppen (Scope Chat.Read)
├─ company_enrich.py     — Webseite + Zefix Firmen-Steckbrief
├─ .env.example          — Vorlage für Umgebungsvariablen
└─ .gitignore            — schließt .token_cache.bin + *.json + .env aus
```

Wrapper-Skripte in `_imports/`:

```
_imports/
├─ build_people_notes.py     — JSONs → 25_People/*.md (Personen-Notizen)
└─ enrich_companies.py       — Batch company_enrich für alle Firmen
```

Beim Lauf erstellt:

```
scripts/.token_cache.bin       — lokaler MSAL-Token-Cache
scripts/mail_digest.json       — Mail-Aggregation pro Kontakt
scripts/teams_digest.json      — Teams-Aggregation pro Kontakt
scripts/company_profiles.json  — Webseiten-/Zefix-Steckbriefe pro Firma
```

## Quickstart

```bash
cd 50.work/m365-graph/scripts
python3 -m venv .venv && source .venv/bin/activate
pip install msal requests
source .env                                   # oder export-Befehle (siehe 02-zugangsdaten-secrets)
python3 mail_digest.py
python3 teams_digest.py
```

Erstes Mal: Device-Code → `https://microsoft.com/devicelogin` → mit `raoul@miraglia-bi.com` anmelden.

## Status

- [x] Setup nachvollzogen (2026-06-01)
- [x] Erste Ausführung erfolgreich:
  - `mail_digest.py`: 2'500 Mails → 134 Korrespondenten
  - `teams_digest.py`: 1'621 Nachrichten in 300 Chats → 87 Partner + 17 Gruppenchats
- [x] 10 Personen-Notizen in `25_People/` erstellt + befüllt (Metadaten-Modus)
- [x] `company_enrich.py` getestet (Nahrin → ok)
- [x] Batch-Anreicherung 9 Firmen → Personen-Notizen erweitert um `<!-- firmenprofil -->` Block
- [ ] Zefix-API-Account anlegen (https://www.zefix.ch → API) + Profile mit UID/Rechtsform ergänzen
- [ ] Feedback an Giovanni gegeben
- [ ] In Standard-Setup integriert

## Generator-Skript

Die Personen-Notizen wurden mit `_imports/build_people_notes.py` aus den JSONs gebaut. Bei späterem Refresh (digest neu laufen lassen) kann das Skript erneut ausgeführt werden — es überschreibt die `<!-- mail-summary -->`-Blöcke, lässt aber den restlichen Notizinhalt unangetastet.

Achtung: aktuelle Version überschreibt **die ganze Datei** (auch persönliche Notizen). Vor Re-Run die Persönlichen-Notizen-Blöcke sichern oder das Skript auf reines Marker-Replace umbauen.

## Verwandt

- [[50.work/power-platform/_README]] — restlicher Miraglia-Tech-Stack
- [[40.meta/claude-projekte-und-custom-ai]] — Claude/Claudian-Integration
- [[40.meta/dokumentenanalyse-vorlesung-zusammenfassen]] — verwandtes Pattern (Notizen-Anreicherung)
