---
name: Einfassbänder / AI-Prompt-Auftragserstellung
slug: Einfassbaender-Hunnenberg
klient: Hunnenberg
klient_link: "[[50.work/26_Firmen/Hunnenberg|Hunnenberg]]"
status: produktiv
zeitraum: April 2026
kategorie: kunde
tags: [miraglia, projekt, hunnenberg, power-automate, ai-builder]
type: projekt-hub
source: claude-import + m365-graph
created: 2026-06-01
---

# Einfassbänder / AI-Prompt-Auftragserstellung

**Klient:** [[50.work/26_Firmen/Hunnenberg|Hunnenberg]]  
**Status:** produktiv  
**Zeitraum:** April 2026

## Worum geht es

Power-Automate-Flow + AI-Builder-Prompt für die automatische Auftragserstellung im Teppich- und Bodenbelag-Großhandel: aus PDF-Dokumenten + Mail werden Positionen + Lieferinfo extrahiert und in eine Strukturierte Auftragsdaten-JSON überführt.

## Beteiligte

- [[50.work/25_People/TH-Hunnenberg|TH Hunnenberg]]

## Kontext / Architektur

- Klient: Hunnenberg, Düsseldorf — Großhandel für Bodenbeläge und Teppich-Kettelei.
- Workflow: Mehrseitiges Dokument + Mail mit Lieferinfo → AI Builder Prompt → JSON mit Positionen (Artikel-Nr., Beschreibung, Menge, Form, Länge, Breite, Einfassung, Farbe, Breite, Rückenbeschichtung) + Lieferdatum / Spedition.
- Komplexer Fall: Positionen können über zwei Seiten verteilt sein (Marker „Warenausgangsnr.“ als Fortsetzungs-Header).
- Domain-Wissen: Einfassbreite = 1cm → Farbe = Konkatenation aus Einfassfarbe-PDF + letzten 2 Ziffern; sonst Nummer ohne Präfix.
- Float-Cast benötigt Komma → Punkt Replace (siehe Pattern Power-Automate-String).

## Quell-Conversations (Claude-Export)

Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). Die destillierten Pattern-Notizen sind unter „Verwandte Patterns“.

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 42 | 2026-04-23 | Prompt zur Formelberechnung mit JSON-Ausgabe | `2a3604c1…` |
| 14 | 2026-04-30 | Filter für Einfassbänder und Teppichkanten | `7c1d0fc3…` |
| 2 | 2026-04-22 | Formelberechnung mit Wertsubstitution | `f4c08cc2…` |

## Verwandte Pattern-Notizen

- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — strukturierte JSON-Ausgabe]]
- [[50.work/power-platform/power-automate-string-expressions|String-Expressions & Locale-Fallen (Komma vs. Punkt)]]
- [[50.work/power-platform/powerfx-filter-search-combobox|PowerFx Filter]]

## Erkenntnisse / Lessons Learned

- AI-Prompts: „Vorgehensweise intern, nicht ausgeben“ → step-by-step-Rechnen reduziert Klammer-Fehler im JSON-Output.
- Bei seitenübergreifenden Positionen den Fortsetzungs-Marker explizit im Prompt benennen, sonst entstehen halbe Duplikat-Einträge.
- Locale: deutsche Komma-Notation muss vor `float()` zu Punkt-Notation gemapped werden.
- Bedingungslogik (z.B. „Wenn Einfassbreite = 1cm dann …“) gehört in Power Automate `Condition` + `concat`, NICHT in den LLM-Prompt.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/Hunnenberg|Klient: Hunnenberg]]