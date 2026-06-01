---
name: Zeugnis-Test-App
slug: Zeugnis-App-Obrist
klient: Obrist Interior
klient_link: "[[50.work/26_Firmen/Obrist-Interior|Obrist Interior]]"
status: produktiv / Test
zeitraum: Sept – Okt 2025
kategorie: kunde
tags: [miraglia, projekt, obrist-interior, power-apps, zeugnis]
type: projekt-hub
source: claude-import + m365-graph
created: 2026-06-01
---

# Zeugnis-Test-App

**Klient:** [[50.work/26_Firmen/Obrist-Interior|Obrist Interior]]  
**Status:** produktiv / Test  
**Zeitraum:** Sept – Okt 2025

## Worum geht es

Power-Apps-Lösung bei Obrist Interior für die Verwaltung von (Mitarbeiter-?)Zeugnissen. Test-Phase mit drei Stakeholderinnen — Barbara Gilli, Tobias Lamprecht und Bianca Tschuppert.

## Beteiligte

- [[50.work/25_People/Barbara-Gilli|Barbara Gilli]]
- [[50.work/25_People/Tobias-Lamprecht|Tobias Lamprecht]]
- [[50.work/25_People/Bianca-Tschuppert|Bianca Tschuppert]]

## Kontext / Architektur

- Chat-Samples zeigen: Diskussion um Zeugnis-Links, Sichtbarkeit der Zeugnisse, Test-Zeugnisse für „Andreas Walser“.
- Mögliche Verbindung zu Conv „Wöchentliche Erinnerung zu ausstehenden Zeugnissen“ (2026-03-12, 8msg) — andere Klientenbeziehung, evtl. parallele Logik.
- Tobias Lamprecht: „Wenn ich auf den Link von Barbara klicke, sehe ich kein Zeugnis mehr.“
- Bianca Tschuppert: „Hallo Raoul, auch ich habe das Test Zeugnis für Andreas Walser erhalten.”
- **„Andreas Walser”** = Test-Datensatz im System, nicht ein realer Mitarbeiter (keine eigene Personen-Notiz angelegt).

## Verwandte Pattern-Notizen

- [[50.work/power-platform/powerfx-filter-search-combobox|Filter-Logik für Zeugnis-Liste]]
- [[50.work/power-platform/dataverse-mysterious-deletes|Sichtbarkeits-/Berechtigungs-Probleme]]

## Erkenntnisse / Lessons Learned

- Sichtbarkeits-Bug („sehe kein Zeugnis“) deutet auf Security-Role / Owner-Filter hin — Standard-Diagnose-Pfad: Dataverse-Berechtigung + Filter-Predicates prüfen.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[50.work/projekte/_Index|Projekt-Index]]
- [[50.work/26_Firmen/Obrist-Interior|Klient: Obrist Interior]]