---
source: claude-import + m365-graph
imported: 2026-06-01
type: cluster-readme
tags: [miraglia, work]
---

# 50.work — Miraglia Business-Intelligence

Komplette Arbeits-Ebene des Vaults. Vier Bereiche:

## CRM

- **[[50.work/25_People/_Index|25_People]]** — Personen-Notizen
  (18 Kontakte: Kollegen, Partner, Kunden)
- **[[50.work/26_Firmen/_Index|26_Firmen]]** — Firmen-Notizen
  (12 Firmen mit Webseiten-Steckbrief, Statistik, Projekt-Mapping)

## Projekte

- **[[_Index|projekte]]** — 9 Projekt-Hubs
  (7 Kunden-Projekte + 2 interne Kollaborationen)
  - Aus Claude-Conversation-Index + Teams-Gruppenchats + Mail-Aggregation destilliert
  - Pro Projekt: Klient · Beteiligte · Quellen · Verwandte Pattern-Notizen · Lessons Learned

## Tech-Wissen

- **[[50.work/power-platform/_README|power-platform]]** — Pattern-Bibliothek (10 Notizen)
  PowerFx, Power Automate, Dataverse, AI Builder, Azure RBAC
- **[[50.work/m365-graph/_README|m365-graph]]** — Vault-Anreicherungs-Tooling (6 Notizen)
  Outlook-Mail / Teams-Chat / Webseiten-Steckbrief Aggregation (Setup Giovanni Juni 2026)

## Quervernetzung

Die Daten sind drei-dimensional verlinkt:

```
Person  ─►  Firma  ─►  Projekt
  ▲          ▲           │
  └──────────┴───────────┘
       (Backlinks)
```

- Eine **Personen-Notiz** verlinkt im Frontmatter (`firma:`) auf die Firmen-Notiz
- Eine **Firmen-Notiz** listet alle Personen + alle Projekte des Klienten
- Ein **Projekt-Hub** listet Klient + Beteiligte + Quell-Conversations + Verwandte Patterns

Beispiel-Pfad: [[50.work/25_People/Remo-Pfister|Remo Pfister]] → [[50.work/26_Firmen/MVM-AG|MVM AG]] → [[Regieapp-Neubau-MVM|Regie-Rapport-App-Neubau]] → [[50.work/power-platform/dataverse-offlineprofile|Mobile Offline-Profile]] (Pattern)

## Generatoren in `_imports/`

Alle CRM/Projekt-Notizen sind generierte Output-Files (idempotent re-runbar):

- `build_people_notes.py` — aus `mail_digest.json` + `teams_digest.json`
- `build_firmen_notes.py` — aus `company_profiles.json` + Aggregation
- `enrich_companies.py` — Webseite/Zefix für Firmen
- `build_projects.py` — aus Manifest + Teams-Gruppen
- Plus die Source-Scripts in `50.work/m365-graph/scripts/`

Bei Refresh (neuer Claude-Export oder M365-Lauf): Generators neu starten → Marker-Blöcke werden überschrieben, manuelle Notizen außerhalb der Marker bleiben unangetastet.
