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
- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline — Encoding-, Counter- und Pfad-Sync-Fallen]] — Trigger-Case 2026-06-05

## Erkenntnisse / Lessons Learned

- Deklarations-IDs mit Unterstrich brauchen besondere Behandlung — Display vs. Internal Name (siehe Pattern Power-Automate-String).
- Wöchentliche Reminder als scheduled Flow, mit Filter auf säumige Dokumente.
- JSON-Schema fix halten — bei Datentyp-Drift schlägt Parse-JSON-Action fehl (siehe AI-Prompt-Pattern).
- **Bug-Analyse 2026-06-05** (Flow 02 — eingehende Mail verarbeiten):
  - **Leere PDFs**: heißester Verdacht ist der nicht-resettete `PDF`-Counter zwischen Iterationen des äußeren `For_each` (über Mail-Attachments). Bei Mails mit mehreren Multi-Doc-Anhängen läuft der Index out-of-bounds → leere Files mit korrekter Header-Struktur. Sekundär: `base64ToBinary()`-Wrap am Create_file fehlt.
  - **Pfad „nicht passt"**: Es ist **by design**, dass `ks_eq_dateipfad_manuell` im Erfolgsfall leer bleibt — der finale Pfad lebt in `ks_deklarationens.ks_antwort_sp_pfad`. Wenn ein User trotzdem einen Pfad in der EQ sieht, der nicht stimmt, ist der **Top-Verdacht Duplicate-Trigger**: Outlook-V2-Connector feuert denselben Trigger mehrfach (Forwards, Re-Delivery), ein Run klassifiziert erfolgreich + moved, ein zweiter Run schreibt einen Manuell-Eintrag mit stale `03_Eingang_Temp`-Pfad. Fix: Dedup via `ks_eq_mailid`-Lookup vor `Add_a_new_row`.
  - **Latentes Risiko**: Move-Destination via `split(ks_versendet_sp_pfad, '/K20')[0]` ist fragil (bricht beim Jahreswechsel auf K27 und bei Pfaden ohne K20-Prefix). Ersetzen durch expliziten Subunternehmer-Folder-Lookup.
  - Siehe [[50.work/power-platform/mail-attachment-pipeline-fallen|Pattern-Notiz Mail-Attachment-Pipeline]] für vollständige Lösungs-Snippets und Diagnose-Reihenfolge.

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/Koster-AG|Klient: Koster AG]]