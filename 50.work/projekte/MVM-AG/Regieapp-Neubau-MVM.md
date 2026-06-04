---
name: Regie-Rapport-App (Neubau)
slug: Regieapp-Neubau-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Live / Wartung
zeitraum: April 2026 — Juni 2026 Live-Schaltung
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, power-apps, dataverse, offline, sharepoint]
type: projekt-hub
source: claude-import + m365-graph + chat-context 2026-06-04
created: 2026-06-01
updated: 2026-06-04
---

# Regie-Rapport-App (Neubau)

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]]  
**Status:** Live / Wartung (produktiv aufgeschaltet 01.06.2026)
**Zeitraum:** April 2026 — Juni 2026 Live-Schaltung

## Worum geht es

Neukonzeption und Aufbau einer Power-Apps-Regie-Rapport-App für die mobile Erfassung von Arbeits-, Material- und Personenzeilen auf Baustellen. Dataverse-Datenmodell mit Offline-Profile für Außendienst, Filter+Search-UI, Form-Submit-Logik.

## Beteiligte

### Geschäftsleitung / Ansprechpartner
- [[50.work/25_People/Remo-Pfister|Remo Pfister]] — Power-Platform-Lead, Mitglied GL
- [[50.work/25_People/M.-Schärli|Manuel Schärli]] — Test-/Live-Feedback Gipserei

### PL-Gruppe „Power Apps PL" (Entra-Gruppe `2effe64a-6339-4c83-bfef-663590883137`)
- [[50.work/25_People/Richy-Schön|Richy Schön]] — rein 06.2026
- [[50.work/25_People/Jan-Schwitter|Jan Schwitter]] — rein 06.2026
- [[50.work/25_People/Reto-Limacher|Reto Limacher]] — raus 06.2026 (bleibt aber Offertwesen Lead)

### Standort Meggen
- [[50.work/25_People/Stefanie-Furrer|Stefanie Furrer]] — PL Meggen
- [[50.work/25_People/Antonio-De-Finis|Antonio De Finis]] — Maler Meggen, seit 01.05.2026

### Hybrid-Mitarbeiter
- [[50.work/25_People/Christoph-Räber|Christoph Räber]] — Kundendienst Fassade

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
- 🆕 **SharePoint-Berechtigung auf Speicherort = Pflicht-Voraussetzung** für jeden User der Rapporte erfasst. Wenn der Flow das PDF dort nicht ablegen kann, schlägt Save+Send fehl — und es entsteht eine irreführende „an ihn selbst gesendet"-Bestätigung. → Pattern: [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Flow-Save-Voraussetzung]]
- 🆕 **User-Onboarding-Checkliste:** (a) Aufnahme in Entra-Gruppe „Power Apps PL", (b) SharePoint-Speicherort-Berechtigung, (c) Bei Mitarbeitern eines Standorts: Baustellen-Freischaltung am Mandanten (Meggen / Emmen / Cham).
- 🆕 **Hybrid-Mitarbeiter** (selbständige Annahme + Rechnungsstellung an Kunden — z.B. Christoph Räber): brauchen identisches PDF/Mail-Setup wie PL.

## Onboarding-Log (User-Liste Stand Juni 2026)

| Datum | Aktion | User | Quelle |
|---|---|---|---|
| 06.2026 | + Richy Schön → PL-Gruppe | [[50.work/25_People/Richy-Schön\|Richy Schön]] | Remo 2026-06-01 |
| 06.2026 | + Jan Schwitter → PL-Gruppe | [[50.work/25_People/Jan-Schwitter\|Jan Schwitter]] | Remo 2026-06-01 |
| 06.2026 | – Reto Limacher → raus PL-Gruppe | [[50.work/25_People/Reto-Limacher\|Reto Limacher]] | Remo 2026-06-01 |
| 06.2026 | + Antonio De Finis → User, Baustellen Meggen pending | [[50.work/25_People/Antonio-De-Finis\|Antonio De Finis]] | Remo 2026-05-29 |
| 06.2026 | + Christoph Räber → SharePoint-Permission Fix | [[50.work/25_People/Christoph-Räber\|Christoph Räber]] | Remo 2026-06-03 |

## Bekannte Bugs / Resolutions

### Rapport Nr. 26-1039 — „an ihn selbst gesendet" (gelöst 06.2026)
- **Symptom:** Christoph Räber finalisierte Rapport am Laptop in PDF-Ansicht (Button „Beendet" rechts unten). Bestätigungsmeldung: „Rapport an ihn selbst gesendet".
- **Root Cause:** Christoph hatte zu dem Zeitpunkt **keine SharePoint-Berechtigung** auf den Ziel-Speicherort. Flow rechnete korrekt, PDF wurde generiert — Save-Step schlug fehl → daraus folgend kein Mail-Versand möglich → Bestätigung war falsch.
- **Fix:** Berechtigung nachgetragen. Rapport lief sauber durch.
- → Pattern dokumentiert: [[50.work/power-platform/sharepoint-berechtigung-flow-save]]

### PDF-Generation Manuel Schärli (05.2026, Stabilisierung)
- Symptom: „Heute Morgen hat es wieder nicht funktioniert" + keine Produktnamen (nur Menge/Einheit/Preis).
- Fix: Solution nochmals neu eingespielt, in eine konsistente Version gebracht.
- Stand 06.2026: stabil, abschließende Bestätigung von Manu ausstehend.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]