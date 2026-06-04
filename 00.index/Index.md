---
source: claude-import
imported: 2026-06-01
type: master-index
---

# Index

Master-Übersicht aller importierten Themen-Hubs und Pattern-Bibliotheken aus dem Claude-Datenexport.

## 20.studies — Universität Zürich

### Projekt-Hubs (Seminararbeiten, Gruppenarbeiten)

- [[20.studies/Anneliese-Michel/Hub|Anneliese Michel — Seminararbeit]] (7 Arbeits- + 8 Literatur-Notizen)
- [[20.studies/Religionsoekonomie/Hub|Religionsökonomie — Seminararbeit]] (4 Arbeits- + 13 Literatur-Notizen, Walthert FS 2026)
- [[20.studies/Working-Poor-Gesundheit/Hub|Working Poor & Gesundheit — Gruppenarbeit]] (6 Notizen)

### Studien-Hubs (Vorlesungen, Prüfungen)

- [[20.studies/Organizational-Economics/Hub|Organizational Economics]] (6 Notizen, Prüfung 19. Juni)
- [[20.studies/Aegyptologie/Hub|Ägyptologie]] (5 Notizen)

### Studien-Techniken

- [[20.studies/r-statistik/_README|R & Statistik]] (5 Notizen, UZH EBPI)
- [[20.studies/wissenschaftliches-schreiben/_README|Wissenschaftliches Schreiben]] (5 Notizen)
- [[20.studies/video-media/_README|Video & Media Production]] (3 Notizen)

## 30.patterns — Cross-Cutting Techniken

- [[30.patterns/text-formatting/_README|Text Formatting / Unicode]] (3 Notizen)

## 40.meta — Tools & Workflows

- [[40.meta/Claude-Workflows|Claude Workflows & Obsidian Meta]] (5 Notizen)

## 50.work — Miraglia Business-Intelligence

→ Cluster-Landing: [[50.work/_README|50.work/_README]]

### CRM (Personen & Firmen)
- [[50.work/25_People/_Index|Personen-Index]] (**18 Kontakte** — Kollegen, Partner, Kunden)
- [[50.work/26_Firmen/_Index|Firmen-Index]] (**12 Firmen** mit Steckbrief, Statistik, Projekt-Mapping)

### Projekte (9 Hubs)
- [[_Index|Projekt-Index]]
- Top-Aktiv: [[Subunternehmerprozess-Koster|Subunternehmer-Koster]] · [[Regieapp-Neubau-MVM|Regieapp-MVM]] · [[Telemarketing-App-Nahrin|Telemarketing-Nahrin]]
- Weitere Kunden-Projekte: Averecura (Hauswäckerling), Zeugnis-App (Obrist), Einfassbänder (Hunnenberg), Support Powerplattform (Nahrin)
- Intern/Partner: PowerTeam, RPA-Monitoring

### Tech-Wissen
- [[50.work/power-platform/_README|Power Platform]] (10 Pattern-Notizen)
- [[50.work/m365-graph/_README|M365 Graph → Vault-Anreicherung]] (6 Notizen + 3 Scripts)

---

## Import-Bilanz

| Kennzahl | Wert |
|---|---|
| Quelle | Claude Export, 10.03.2026 – 01.06.2026 |
| Conversations gesamt | 255 |
| Davon mit Inhalt | 250 |
| **Verarbeitet** | **196 Conversations → 61 destillierte Notizen** |
| Übersprungen | 54 (38 privat, 16 leer) |
| Cluster verarbeitet | 11/11 ✓ |

### Notizen-Verteilung pro Cluster

| Cluster | Conv | Notizen | Ziel-Ordner |
|---|---:|---:|---|
| power-platform | 63 | 10 | `50.work/power-platform/` |
| anneliese-michel | 27 | 7 | `20.studies/Anneliese-Michel/` |
| claude-meta | 23 | 5 | `40.meta/` |
| working-poor | 16 | 6 | `20.studies/Working-Poor-Gesundheit/` |
| r-statistik | 14 | 5 | `20.studies/r-statistik/` |
| org-economics | 14 | 6 | `20.studies/Organizational-Economics/` |
| religionsoekonomie (ehem. bourdieu-theorie) | 13 | 4 Arbeits- + 13 Literatur- | `20.studies/Religionsoekonomie/` (fusioniert mit eigener Seminararbeit) |
| wiss-schreiben | 9 | 5 | `20.studies/wissenschaftliches-schreiben/` |
| aegyptologie | 9 | 5 | `20.studies/Aegyptologie/` |
| video-media | 5 | 3 | `20.studies/video-media/` |
| text-formatting | 3 | 3 | `30.patterns/text-formatting/` |
| **Summe** | **196** | **61** | |

### Quellen-Rückverfolgung

Jede importierte Notiz trägt:
- `source: claude-import` im Frontmatter
- `imported: 2026-06-01`
- `conv_uuids: [...]` mit allen Quell-Konversation-UUIDs
- Verweis auf das jeweilige `_conversation-index.md` des Clusters

Über die UUID lässt sich jede Conv im Original-Export per `jq` extrahieren:

```bash
jq -r '.[] | select(.uuid=="<UUID>") | .chat_messages[] | "[\(.sender)] \(.text)"' \
   ~/Downloads/data-748e.../conversations.json
```

## Schreib-Schema (Standard)

Pattern-Notizen folgen:

```
## Problem
## Lösung
## Wann nicht
## Verwandt
```

Projekt-Notizen (z.B. Anneliese-Michel, Working-Poor) sind themenspezifisch strukturiert (Forschungsfrage, Quellen, Architektur).

## Resumability

`_imports/progress.json` zeigt den Status pro Cluster. Aktuell alle auf `done`. Falls neue Conversations dazukommen:

1. Export neu laden
2. `bash _imports/classify.sh` ausführen (Manifest neu erzeugen)
3. Pro neuen Cluster Notizen ergänzen
4. Index hier aktualisieren

## Privates / Übersprungenes

Aus dem Export wurden **38 Conversations als „privat"** und **16 als „leer"** klassifiziert und nicht importiert. Sie sind im `_imports/manifest.json` mit `cluster: privat` bzw. `cluster: empty` markiert, falls bei Bedarf doch einzelne nachgezogen werden sollen.

Beispiele übersprungener Bereiche:
- Persönliche E-Mails, Bewerbungen, Spontanbewerbungen
- Krankenversicherung / Zahnbehandlung / Steuererklärung
- Reise- / Netflix- / Geburtstagsfragen
- Karriereempfehlungen, Lehrdiplom-Anfragen
- Putzroutinen, Maschinen-Haltbarkeit
