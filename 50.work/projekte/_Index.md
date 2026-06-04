---
source: claude-import + m365-graph
imported: 2026-06-01
updated: 2026-06-04
type: projekte-index
tags: [projekte, index, miraglia]
---

# Projekt-Index

Projekte gruppiert nach Klient. Ordnerstruktur unter `50.work/projekte/<Klient>/<Projekt>`.

## 🏗️ MVM AG → [[MVM-AG|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Regieapp-Neubau-MVM\|Regie-Rapport-App (Neubau)]] | Remo Pfister, M. Schärli, PL-Gruppe | **Live ab 06.2026** |
| [[Magazin-App-MVM\|Magazin-App MVM]] | Remo Pfister, Nicole Scherrer, Kanita | Wartung + Erweiterung |
| [[Mahnprozess-MVM\|Mahnprozess MVM]] | Remo Pfister, Hybrid-Mitarbeiter | Live ab 06.2026 |
| [[Zeugnis-App-MVM\|Zeugnis-App MVM]] (+ Prompt-Sub-Notizen) | Nicole Lötscher (HR), PL | Live + Bugfixes |
| [[KI-Ausmass-MVM\|KI-Ausmass MVM (Devis-Copilot)]] (mit Code-Repo) | Reto Limacher, Sascha Ziswiler | Daten-Analyse → Prototyp |

## 🥬 Nahrin AG → [[Nahrin-AG|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Telemarketing-App-Nahrin\|Telemarketing-App]] | Stefanie Ringwald, Christoph Kübler | produktiv / Wartung |
| [[Support-Powerplattform-Nahrin\|Support Powerplattform]] | Stefanie Ringwald, Christoph Kübler, Alessandro Castelli | laufend |

## 🏢 Koster AG → [[Koster-AG|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Subunternehmerprozess-Koster\|Subunternehmer-Dokumentenverwaltung]] | H. Baumann, Monika Kuhn | produktiv / Wartung |

## 🏥 Hauswäckerling → [[Hauswaeckerling|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Averecura-Hauswaeckerling\|Averecura (Pflegezentrum-Lösung)]] | Andreas Funke, Alessandro Castelli | laufend |

## 🛋️ Obrist Interior → [[Obrist-Interior|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Zeugnis-App-Obrist\|Zeugnis-Test-App]] | Barbara Gilli, Tobias Lamprecht, Bianca Tschuppert | produktiv / Test |

## 🧵 Hunnenberg → [[Hunnenberg|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[Einfassbaender-Hunnenberg\|Einfassbänder / AI-Prompt-Auftragserstellung]] | TH Hunnenberg | produktiv |

## 🛠️ Intern / Miraglia-BI → [[Miraglia-Business-Intelligence|Klient-Hub]]

| Projekt | Beteiligte | Status |
|---|---|---|
| [[PowerTeam-intern\|PowerTeam (Partner-Kollaboration)]] | Giovanni Miraglia, Michael Kipfer, Alessandro Castelli | laufend |
| [[RPA-Monitoring-intern\|RPA-Monitoring]] | Giovanni Miraglia, Michael Kipfer | produktiv |

---

## Ordnerstruktur

```
50.work/projekte/
├── _Index.md                            ← diese Datei
├── MVM-AG/
│   ├── KI-Ausmass MVM/                  ← Sub-Ordner mit Code-Repo + Notiz
│   ├── Magazin-App-MVM.md
│   ├── Mahnprozess-MVM.md
│   ├── Regieapp-Neubau-MVM.md
│   └── Zeugnis-App/                     ← Sub-Ordner für 3 verwandte Notizen
│       ├── Zeugnis-App-MVM.md
│       ├── Zeugnis-App-MVM-prompt.md
│       └── Zeugnis-App-MVM-prompt-arbeitsbestaetigung.md
├── Nahrin-AG/
├── Koster-AG/
├── Hauswaeckerling/
├── Hunnenberg/
├── Obrist-Interior/
└── Miraglia-BI/                         ← interne Projekte
```

**Konventionen:**
- Ein Unterordner pro Klient (Name = Klient-Hub-Name aus `26_Firmen/`)
- Sub-Ordner pro Projekt, wenn mehrere Notizen zum gleichen Projekt gehören (z.B. Hub + Prompt-Versionen)
- Sub-Ordner pro Projekt auch wenn ein Code-Repo dazugehört (siehe `KI-Ausmass MVM/`)
- Wikilinks sind path-less (`[[Notiz-Name|Display]]`) — Obsidian löst über den Notiz-Namen auf, robust gegen Umstrukturierung

---

_Index zuletzt aktualisiert 2026-06-04 nach Reorganisation in Klient-Unterordner._
