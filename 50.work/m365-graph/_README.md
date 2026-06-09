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
- 🆕 [[05-draft-replies-pattern|Antwort-Entwürfe mit Inline-Signatur Pattern]] (createReply + Logo-Inline-Attachment, Scope `Mail.ReadWrite`)

## Scripts

```
scripts/
├─ mail_digest.py          — Outlook-Mails (Scope Mail.Read)
├─ teams_digest.py         — Teams-Chats 1:1 + Gruppen (Scope Chat.Read)
├─ company_enrich.py       — Webseite + Zefix Firmen-Steckbrief
├─ 🆕 mvm_extras.py        — Fokus-Suche letzte 500 Mails: @mvm-ag.ch / Filliger /
│                            Subject-Keyword / Personen-Namen (für Fälle wo keine
│                            Personen-Notiz existiert)
├─ 🆕 inspect_signature.py — speichert jüngste HTML-Mail einer Person als Sample
├─ 🆕 extract_logo.py      — extrahiert Inline-Attachment per contentId
├─ 🆕 draft_replies_mvm.py — batch Reply-Drafts mit Signatur + Inline-Logo
│                            (Scope Mail.ReadWrite!)
├─ 🆕 preview_draft.py     — Debug: HTML eines Drafts als preview_draft.html
├─ 🆕 list_drafts.py       — Debug: Drafts-Übersicht mit Subject + Empfänger
├─ auth_common.py          — gemeinsame Auth, Token-Cache im **macOS Keychain**
│                            (`MiragliaBI-M365` / `graph-token-cache`); zusätzlich
│                            `build_pbi_cache(tenant)` für Power-BI-Multi-Tenant
├─ .env.example            — Vorlage für Umgebungsvariablen
└─ .gitignore              — schließt *.bin / .token_cache* / .pbi_token_cache_* /
                             *.json / .env / Samples aus (Defense-in-Depth)
```

### Beim Re-Run der Drafts-Pipeline

```bash
# 1× pro Tenant / pro Update der Signatur
python3 inspect_signature.py     # → giovanni_sample.html
python3 extract_logo.py          # → miraglia_logo.png

# Pro Antwort-Batch
python3 draft_replies_mvm.py     # ggf. DRAFTS-Liste in der Datei anpassen
python3 list_drafts.py           # Sichtkontrolle
```

Wrapper-Skripte in `_imports/`:

```
_imports/
├─ build_people_notes.py     — JSONs → 25_People/*.md (Personen-Notizen)
└─ enrich_companies.py       — Batch company_enrich für alle Firmen
```

Beim Lauf erstellt:

```
macOS Keychain (verschlüsselt!)
  Service=MiragliaBI-M365 / Account=graph-token-cache   — MSAL-Token-Cache
  Service=MiragliaBI-PowerBI / Account=<tenant-slug>    — pro PBI-Tenant
scripts/mail_digest.json       — Mail-Aggregation pro Kontakt
scripts/teams_digest.json      — Teams-Aggregation pro Kontakt
scripts/company_profiles.json  — Webseiten-/Zefix-Steckbriefe pro Firma
```

> 🔐 **Token-Regel (Giovanni 2026-06-09):** Tokens IMMER verschlüsselt im
> OS-Keystore (macOS Keychain / Windows DPAPI), NIE als Klartext-`.bin`-Datei
> im Vault/Dropbox. Implementiert via `msal_extensions` (`PersistedTokenCache`
> + `KeychainPersistence`). Siehe `02-zugangsdaten-secrets` für die Regel im
> Detail.

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
- [x] **2026-06-04:** Draft-Replies-Pipeline produktiv (createReply + Inline-Logo) — Scope `Mail.ReadWrite` ergänzt
- [x] **2026-06-04:** `mvm_extras.py` zur Fokus-Suche (Domain/Keyword/Name) — fand 3 zusätzliche MVM-Quellen (Personal-Gruppe, Filliger Partner, Nicole Scherrer)
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
