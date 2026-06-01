---
name: Telemarketing-App
slug: Telemarketing-App-Nahrin
klient: Nahrin AG
klient_link: "[[50.work/26_Firmen/Nahrin-AG|Nahrin AG]]"
status: produktiv / Wartung
zeitraum: März 2026 — laufend
kategorie: kunde
tags: [miraglia, projekt, nahrin, power-apps]
type: projekt-hub
source: claude-import + m365-graph
created: 2026-06-01
---

# Telemarketing-App

**Klient:** [[50.work/26_Firmen/Nahrin-AG|Nahrin AG]]  
**Status:** produktiv / Wartung  
**Zeitraum:** März 2026 — laufend

## Worum geht es

Power-Apps-Lösung für das Nahrin-Telemarketing-Team: Kundenliste mit Anruf-Logik, Notizen, Nachverfolgung.

## Beteiligte

- [[50.work/25_People/Stefanie-Ringwald|Stefanie Ringwald]]
- [[50.work/25_People/Christoph-Kübler|Christoph Kübler]]

## Kontext / Architektur

- Hauptkanal: Teams-Gruppe „Telemarketing App - Nahrin“ mit 71 Nachrichten.
- Stakeholder: Christoph Kübler (Nahrin), Stefanie Ringwald (Nahrin), Giovanni (Miraglia).
- Inaktive Kunden tauchten ungewollt in der App auf → Filter-Logik-Bug.

## Quell-Conversations (Claude-Export)

Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). Die destillierten Pattern-Notizen sind unter „Verwandte Patterns“.

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 4 | 2026-03-12 | Inaktive Kunden erscheinen in Telemarketing-App | `0b5ececa…` |

## Teams-Gruppen-Chats

- **Telemarketing App - Nahrin** — 71 Nachrichten (letzter 2026-02-13)
  - Mitglieder: Christoph Kübler, Giovanni Miraglia, Stefanie Ringwald

## Verwandte Pattern-Notizen

- [[50.work/power-platform/powerfx-filter-search-combobox|Filter / inaktive-Filter-Logik]]

## Erkenntnisse / Lessons Learned

- Inaktive Kunden müssen aktiv ausgefiltert werden — `inactive = false` als Default-Filter im Galerie-Items-Property.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[50.work/projekte/_Index|Projekt-Index]]
- [[50.work/26_Firmen/Nahrin-AG|Klient: Nahrin AG]]