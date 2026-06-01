---
name: Regie-Rapport-App (Neubau)
slug: Regieapp-Neubau-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Test- / Rollout-Phase
zeitraum: April 2026 — Mai 2026
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, power-apps, dataverse, offline]
type: projekt-hub
source: claude-import + m365-graph
created: 2026-06-01
---

# Regie-Rapport-App (Neubau)

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]]  
**Status:** Test- / Rollout-Phase  
**Zeitraum:** April 2026 — Mai 2026

## Worum geht es

Neukonzeption und Aufbau einer Power-Apps-Regie-Rapport-App für die mobile Erfassung von Arbeits-, Material- und Personenzeilen auf Baustellen. Dataverse-Datenmodell mit Offline-Profile für Außendienst, Filter+Search-UI, Form-Submit-Logik.

## Beteiligte

- [[50.work/25_People/Remo-Pfister|Remo Pfister]]
- [[50.work/25_People/M.-Schärli|M. Schärli]]

## Kontext / Architektur

- Architektur: Master-Tabelle `Regiekopf` + drei N:1-Detail-Tabellen (Arbeitsbeschriebzeile, Materialzeile, Personenzeile).
- Stammdaten-Lookups: Baustelle, Materialkatalog, Mitarbeitertypen.
- Mobile-First: Außendienst erfasst auf der Baustelle, oft ohne Netz → Offline-Profil als zentrale Anforderung.
- UI mit Combobox-Mehrfachauswahl (Baustelle) + Volltextsuche über Empfänger, Kalenderwoche, PL-Kommentar.

## Quell-Conversations (Claude-Export)

Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). Die destillierten Pattern-Notizen sind unter „Verwandte Patterns“.

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 46 | 2026-05-20 | Offlineprofil Fehler beim Speichern und Öffnen | `ad2297d4…` |
| 42 | 2026-04-09 | Filter mit Combobox und Textsuche erweitern | `46548c10…` |
| 9 | 2026-04-08 | Neukonzeption einer Regie-Rapport-App für Power Platform | `47b30ad6…` |
| 2 | 2026-04-16 | Regieapp-Testphase und Zugriffsverwaltung | `f58e17d1…` |
| 2 | 2026-05-03 | Neue Regie-App und Power Apps Installation | `a6b53a21…` |

## Verwandte Pattern-Notizen

- [[50.work/power-platform/powerfx-filter-search-combobox|Filter + Search + Combobox kombinieren]]
- [[50.work/power-platform/powerfx-hidden-datacard-submitform|Hidden Datacard SubmitForm]]
- [[50.work/power-platform/dataverse-offlineprofile|Mobile Offline-Profile]]
- [[50.work/power-platform/dataverse-mysterious-deletes|Cascade-Delete-Diagnose]]

## Erkenntnisse / Lessons Learned

- Auto-generiertes Offline-Profil → nutzlos. Eigenes Profil in Solution anlegen, sonst Schema-Drift bei jeder Spaltenänderung.
- Lookup-Filter ohne `.Id`-Suffix verwenden: `Baustellelookup in ComboBox1.SelectedItems` ist delegierbar und sauberer.
- `Search()` außen, `Filter()` innen — UI-Pattern für Combobox + Volltext.
- Hidden Datacards mit `Visible = false` schreiben NICHT in Dataverse → stattdessen `Height: 0, Visible: true`.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[50.work/projekte/_Index|Projekt-Index]]
- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]