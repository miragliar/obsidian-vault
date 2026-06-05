---
name: Subunternehmer-Dokumentenverwaltung
slug: Subunternehmerprozess-Koster
klient: Koster AG
klient_link: "[[50.work/26_Firmen/Koster-AG|Koster AG]]"
status: produktiv / Wartung
zeitraum: März 2026 — laufend
kategorie: kunde
tags: [miraglia, projekt, koster-ag, power-apps, ai-builder]
type: projekt-hub
source: claude-import + m365-graph
created: 2026-06-01
---

# Subunternehmer-Dokumentenverwaltung

**Klient:** [[50.work/26_Firmen/Koster-AG|Koster AG]]  
**Status:** produktiv / Wartung  
**Zeitraum:** März 2026 — laufend

## Worum geht es

Power-Apps-Lösung zur automatisierten Verwaltung von Subunternehmer-Dokumenten (Verträge, Deklarationen, Zeugnisse) mit KI-gestützter Datenextraktion via AI Builder und Power-Automate-Flows.

## Beteiligte

- [[50.work/25_People/H.-Baumann|H. Baumann]]
- [[50.work/25_People/Monika-Kuhn|Monika Kuhn]]

## Kontext / Architektur

- Subunternehmer schicken Dokumente, die in einem komplexen Workflow verarbeitet, klassifiziert und archiviert werden müssen.
- Status-Maschine pro Dokument (Eingang → Prüfung → Freigabe / Rückfrage / Ablage).
- AI Builder Prompt extrahiert Positionsdaten / Deklarations-Felder aus PDFs, Power Automate orchestriert die Folge-Schritte.
- Wöchentliche Erinnerungs-Flows an säumige Subunternehmer.

## Quell-Conversations (Claude-Export)

Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). Die destillierten Pattern-Notizen sind unter „Verwandte Patterns“.

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 206 | 2026-04-08 | Subunternehmer-Dokumentenverwaltung mit KI und Power Apps | `8e6798fb…` |
| 18 | 2026-04-29 | Unterstrich in Deklarations_ID verschwindet | `b476d092…` |
| 8 | 2026-03-19 | Subunternehmerprozess automatisiert und vereinfacht | `74779f30…` |
| 8 | 2026-03-12 | Wöchentliche Erinnerung zu ausstehenden Zeugnissen | `6beaaba8…` |
| 6 | 2026-03-26 | Deklaration ID Leerfeld-Prüfung funktioniert nicht | `7d4fb25c…` |
| 4 | 2026-04-02 | Subunternehmerprozess und Dokumentenstatus | `0c6f8de5…` |

## Verwandte Pattern-Notizen

- [[50.work/power-platform/ai-prompt-json-output|AI Prompt für strukturierte JSON-Extraktion]]
- [[50.work/power-platform/powerfx-filter-search-combobox|Filter+Search Combobox]]
- [[50.work/power-platform/power-automate-string-expressions|String-Expressions]]
- [[50.work/power-platform/powerfx-hidden-datacard-submitform|Hidden Datacard SubmitForm]]
- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline — Komplette Bug-Klasse]] — Trigger-Case 2026-06-05, alle finalen Lehren
- [[50.work/power-platform/power-automate-variable-binary-damage|Power Automate Variable Binary Damage]] — abgeleitet aus Cluster A2
- [[50.work/power-platform/ai-builder-doppel-branch-vermeiden|AI Builder — Doppel-Branch vermeiden]] — abgeleitet aus Cluster D

## Erkenntnisse / Lessons Learned

- Deklarations-IDs mit Unterstrich brauchen besondere Behandlung — Display vs. Internal Name (siehe Pattern Power-Automate-String).
- Wöchentliche Reminder als scheduled Flow, mit Filter auf säumige Dokumente.
- JSON-Schema fix halten — bei Datentyp-Drift schlägt Parse-JSON-Action fehl (siehe AI-Prompt-Pattern).

### Bug-Analyse Flow 02 — Komplette Debug-Session 2026-06-05

Ausgangslage: H. Baumann meldet zwei Bug-Klassen — Files an falschen Orten + leere PDFs mit korrekter Seitenanzahl.

**Sechs Bug-Cluster identifiziert und behoben:**

1. **Cluster A1 — `@{expression}` mit Curly Braces zerstört Binary** (war ursprünglich als Export-Artefakt verworfen, **war aber real**). Set_variable mit `@{...}` macht String-Interpolation, die bei langen Binary-Werten Whitespace/Escape-Artefakte injiziert. Fix: `@expression` ohne Braces.

2. **Cluster A2 — Power Automate Variablen sind nicht binary-safe**. Diagnostischer Beweis: `EF BF BD` (UTF-8 Replacement Character) in den Page-Streams der gesplitteten PDFs, plus `Bad FCHECK in flate stream` von `pdftotext`. Auch Variable-Type `object` schützt nicht. Fix: Variablen für File Content **komplett entfernen**, Connector-Output direkt in Create_file body referenzieren (zwei separate Create_file Actions pro Branch). Eigene Pattern-Notiz: [[50.work/power-platform/power-automate-variable-binary-damage]].

3. **Cluster B1 — `items('Apply_to_each')` vs `items('For_each')`**. Single-Doc-Files landeten als 4 Bytes `null` in SP, weil `items('Apply_to_each')?['contentBytes']` auf das KI-Klassifikations-Object greift, das kein `contentBytes`-Feld hat. Fix: `items('For_each')?['contentBytes']` (outer Loop, Attachment-Level).

4. **Cluster B2 — PDF-Split Off-by-One**. Rahmenvertrag-Inhalt mit MINARB-Filename + zweite Split-Datei kaputt, weil `Increment variable 2` vor `Create_file` lief. Fix: `iterationIndexes('Apply_to_each')` statt manuellem PDF-Counter — Counter-Variable komplett raus.

5. **Cluster C1 — Multi-Iteration-Update-Override**. `Add_a_new_row` außerhalb des inneren `Apply_to_each` → ein EQ-Eintrag pro Mail-Attachment, alle Sub-Doc-Iterationen überschreiben ihn. Fix: `Add_a_new_row` in den inneren Loop → ein EQ-Eintrag pro Sub-Doc.

6. **Cluster D — Doppel-Branch (structured + raw) eliminiert**. Custom Prompt war nicht-deterministisch. Bug-Surface halbiert durch Reduktion auf Single-Path über `predictionOutput/text` + Parse_JSON mit Cleanup-Compose. Eigene Pattern-Notiz: [[50.work/power-platform/ai-builder-doppel-branch-vermeiden]].

**By design (nicht Bugs)**:
- `ks_eq_dateipfad_manuell` bleibt leer im Erfolgsfall — finaler Pfad lebt in `ks_deklarationens.ks_antwort_sp_pfad`.
- 5 Update_a_row-EQ-Actions pro Branch sind alle nötig (4 Endzustände + 1 Scope-Failure-Pfad).

**Architektur-Pattern für SP-Output-Wiederverwendung**: drei Compose-Bridges nach Create_file (`Compose_SP_File_Id` für Move, `Compose_SP_File_ItemId` für Dataverse, `Compose_SP_File_Path` für Display) — abstrahiert die Multi-vs-Single-Create_file-Doppelung weg.

**Latente Risiken nicht akut, aber dokumentiert**:
- Move-Destination via `split(ks_versendet_sp_pfad, '/K20')[0]` bricht beim Jahreswechsel auf K27 (2027). Fix: Subunternehmer-Folder-Lookup statt String-Split.
- `ks_eq_attachmenthash` speichert MIME-Type statt SHA256 — kosmetisch, aber blockiert Content-basierten Dedup.

**Falsche Spuren, die geprüft und verworfen wurden** (nicht erneut verfolgen):
- Duplicate-Trigger vom Outlook-V2-Connector — MessageIDs sind eindeutig in dieser Umgebung.
- PDF4me-Quota — bei sichtbaren DEBUG-Längen im KB-Bereich ist es nie das Quota.
- `base64ToBinary()` als Fix bei UTF-8-Damage — Damage passiert vor jeder Dekodierung.
- Variable-Type `object` als Fix — auch object geht durch UTF-8-Pipeline.

→ **Vollständige Anleitung mit allen Lösungs-Snippets, Diagnose-Reihenfolge und Test-Setup**: [[50.work/power-platform/mail-attachment-pipeline-fallen|Pattern-Notiz Mail-Attachment-Pipeline]].

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/Koster-AG|Klient: Koster AG]]