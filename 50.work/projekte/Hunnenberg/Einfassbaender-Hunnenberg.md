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

## Backlog / offene Punkte

> **Stand 2026-06-17 — Claudian-Sortier-Session, noch nicht verifiziert.**
> Punkte abgeleitet aus Prompt-Snapshot [[Prompt-Auftragserstellung-2026-06-09]] + Hub-Inhalt + Inbox-Stand (keine offenen Mails von TH-Hunnenberg seit 2026-06-09). Status: jeder Punkt muss von Raoul triagiert werden — `🤔` = verifizieren, `📋` = Backlog bestätigt, `✅` = erledigt/verworfen.

### Verifikation gegen Live-System (kann längst gefixt sein)

- [ ] 🤔 **B1 — Drift Snapshot ↔ AI Builder.** Snapshot ist vom 2026-06-09. Wurde der produktive Prompt seither geändert (Live-Tuning mit Tatjana am 2026-06-09 hatte 5 Iterationen — Snapshot deckt die letzte ab, aber spätere Edits?). Aktion: produktiven Prompt aus AI Builder ziehen + gegen Snapshot diffen, ggf. „Update 6" im Changelog ergänzen.
- [ ] 🤔 **B2 — Fallstrick #2 nachhaltige Lösung.** Im Snapshot dokumentiert: defensive `empty()`-Klausel in der Power-Automate-Expression *und* Vorschlag, dem Formelberechnungs-Prompt davor „Resultat=0 statt leerer String" beizubringen. Welche Variante läuft? Beide? Aktion: Vorgänger-Prompt prüfen, redundante defensive Logik ggf. zurückbauen.
- [ ] 🤔 **B3 — Sage-Quoting-Variante.** Pipeline-Abschnitt nennt Variante A (Sage-Import-Mapping als „Memo"/„Multi-Line") und Variante B (eigenes Quoting im Compose). Welche ist produktiv? Aktion: festhalten + Caveat im Snapshot präzisieren.

### Spec-Lücken im Prompt

- [ ] 📋 **B4 — `filterbez` Fallback bei unbekanntem Wert.** Tabelle hat 17 Mappings (inkl. Object-Carpet-Linien Corfu/Malta/Menorca/Capri/Rodi/Milo). Was passiert bei einem neuen Produktnamen, der noch nicht in der Tabelle steht? Aktuelle Konvention nur für „Gekettelt → null". Vorschlag: explizite Fallback-Klausel „unbekannt → null + `mapping_hinweis`" (analog zu `form`/`art_einfassung`).
- [ ] 📋 **B5 — `geschorene_Teppiche` Sortiments-Pflege.** 30 hardcoded Produktnamen. Wer aktualisiert wenn Object Carpet ein neues Modell rausbringt? Aktion: kurze Pflege-Anleitung im Snapshot + Verantwortlichen festlegen (Raoul vs. Tatjana liefert Updates).

### Test-Lücken

- [ ] 📋 **B6 — Regressions-Test-Mappe fehlt.** Bei 5 Prompt-Updates an einem Tag (2026-06-09) lief kein systematischer Diff über echte Vorgänger-Aufträge. Vorschlag: `50.work/projekte/Hunnenberg/test-corpus/` mit 5–10 anonymisierten PDFs + erwarteten JSON-Outputs als Goldfile-Tests. Baseline könnte `build_anon_verkaufsauftrag.py` (ORD0001560) plus 4–5 weitere sein.
- [ ] 📋 **B7 — `Rutschhemmung`-Flag (neu seit 2026-06-09) live-verifiziert?** Update 1 vom 09.06. eingeführt: `breite_m > 4` UND `rueckenbeschichtung` enthält Rutschhemmung. Gibt es einen echten Auftrag, der das triggert? Aktion: einen Stichproben-Lauf gegen Aufträge der letzten Wochen.

### Architektur / Refactor

- [ ] 📋 **B8 — Lessons-Learned-Konflikt: „Bedingungslogik gehört in Power Automate".** Der aktuelle Prompt bricht diese Regel mehrfach (P-Präfix-Substitution 43→38/52→48, alle 5 Flags). Bewusste Akzeptanz (LLM ist gut genug, Power-Automate-Conditions wären unleserlich) oder Refactor-Backlog? Aktion: Lessons-Learned-Bullet entweder präzisieren („gilt nur für nicht-textuelle Bedingungen") oder Refactor-Ticket öffnen.
- [ ] 📋 **B9 — Caveat #1 Trenner-Kollisionsschutz.** Pipe ` | ` ist „in Teppich-Artikelbeschreibungen praktisch nie natürlich" — aber „praktisch nie" ist kein Beweis. Aktion: einmalige Grep-Analyse über bestehende Object-Carpet-Artikelbeschreibungen → falls 0 Treffer, Caveat zu „verifiziert sauber" upgraden; sonst auf `<<NL>>`-Trenner wechseln.

### Process

- [ ] 📋 **B10 — Anwender-Feedback-Kanal.** Tatjana korrigiert vermutlich AI-Outputs manuell, bevor sie nach Sage gehen. Wo fliesst das zurück in den Prompt? Aktion: einfacher Workflow definieren (z. B. Outlook-Kategorie „AI-Output korrigiert" → wöchentlicher Sichtbar-Macher).

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/Hunnenberg|Klient: Hunnenberg]]