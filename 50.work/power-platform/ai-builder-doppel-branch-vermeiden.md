---
source: chat-context 2026-06-05
imported: 2026-06-05
type: pattern
tags: [power-platform, power-automate, ai-builder, architecture, refactoring, troubleshooting]
related_projects: ["[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"]
trigger_case: "Subunternehmerflow 02 — structured + raw Doppel-Branch (Koster AG, 2026-06-05)"
---

# AI Builder — Doppel-Branch bei nicht-deterministischem Output vermeiden

## Problem

AI Builder Custom Prompts mit JSON-Output sind **nicht deterministisch**: mal kommt das JSON sauber im `structuredOutput`-Feld, mal nur als Rohtext im `text`-Feld umgeben von Erklärtext oder Markdown-Fences.

Die intuitive Reaktion: zwei Branches im Flow, einer für jeden Fall. Bedingung wie:

```
Condition: length(outputs('Run_a_prompt')?['body/.../structuredOutput/result']) > 1
  IF:   verarbeite via structuredOutput (For_each über result)
  ELSE: verarbeite via raw text (Parse_JSON über text + Apply_to_each)
```

**Folgen, die sich nicht vermeiden lassen:**
- Jede Bug-Klasse existiert **zweimal** (jeder Branch hat eigene Set-Variables, Conditions, Updates)
- Maintenance-Aufwand verdoppelt sich: jede Änderung muss synchron in beiden Branches gemacht werden
- Bug-Diagnose verzweigt: „funktioniert für manche Mails, für andere nicht" — meist weil ein Branch upgedated wurde und der andere nicht
- Der äußere Scope hat plötzlich `runAfter: Condition Succeeded` vs `runAfter: Condition Failed` als Branching-Mechanismus → noch eine Ebene Komplexität
- `_1`, `_V2_1`, `_3_3` Duplikat-Namen vermehren sich

## Lösung — Lowest-Common-Denominator nehmen

Bei AI Builder Custom Prompts ist der **Lowest-Common-Denominator** immer `predictionOutput/text`. Dieses Feld ist garantiert befüllt (= roher LLM-Output), egal ob der LLM structured oder raw geliefert hat. Wenn structured kam, ist das JSON auch als String im `text`-Feld.

→ **Single-Branch via Parse_JSON aus dem text-Feld**. Damit wird der structured-Pfad obsolet.

```
Run_a_prompt:
  → predictionOutput/text  ← immer da

Bereich (Scope):
  Compose_clean_json:        ← Härtung: extrahiert Substring zwischen erstem { und letztem }
    @substring(
      outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text'],
      indexOf(<text>, '{'),
      add(sub(lastIndexOf(<text>, '}'), indexOf(<text>, '{')), 1)
    )
  
  Parse_JSON:
    content: @outputs('Compose_clean_json')
    schema: {...mit [string, null] für alle optionalen Felder...}

Apply_to_each (über Parse_JSON?['result']):
  → einheitliche Verarbeitung
```

## Voraussetzungen — Parse_JSON-Härtung

Wenn alles über `text` läuft, ist Parse_JSON ein Single-Point-of-Failure. Drei Härtungen:

### 1. Prompt-Härtung
- Klare Anweisung: „Gib NUR JSON aus, kein Erklärtext, kein Markdown-Fence"
- Ein vollständiges Few-Shot-Beispiel mit der exakten Output-Struktur im Prompt
- Reihenfolge-Garantie explizit machen wenn Folge-Logik darauf basiert (siehe [[50.work/power-platform/ai-prompt-json-output]])

### 2. Cleanup-Compose vor Parse_JSON
Fängt LLM-Übergriffe ab (Markdown-Fences, „Hier ist das JSON:"-Präambeln, Trailing-Whitespace):

```
Compose_clean_json:
  @substring(
    outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text'],
    indexOf(outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text'], '{'),
    add(
      sub(
        lastIndexOf(outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text'], '}'),
        indexOf(outputs('Run_a_prompt')?['body/responsev2/predictionOutput/text'], '{')
      ),
      1
    )
  )
```

### 3. Schema-Flexibilität
Alle Felder, die der LLM mal weglassen kann, als `["string", "null"]` deklarieren:

```json
{
  "deklaration_id": { "type": ["string", "null"] },
  "dokumententyp":  { "type": ["string", "null"] },
  ...
}
```

Sonst failt Parse_JSON bei jedem nicht-übergebenen Feld.

## Failure-Branch wird umso wichtiger

Wenn Parse_JSON failt (LLM hat sich entschuldigt statt JSON zu liefern, oder Format völlig anders), muss der Failure-Pfad sauber greifen:

```
Scope: Bereich
  Compose_clean_json
  Parse_JSON
  ...

→ runAfter Bereich [Failed, TimedOut]:
   Add_a_new_row → Status "Verarbeiten fehlgeschlagen"
                 + ks_eq_fehlertext = "Parse_JSON failed — LLM output war kein gültiges JSON"
                 + Mail an Admin
   Create file in Temp-Ordner (Original-Attachment direkt aus items('For_each')?['contentBytes'])
```

Und für den Fall „Parse_JSON erfolgreich, aber `result` ist leeres Array":
```
Condition nach Apply_to_each:
  empty(body('Parse_JSON')?['result'])
    True: Add_a_new_row mit Status "Verarbeiten fehlgeschlagen"
          + Fehlertext "KI hat keine Dokumente erkannt"
```

## Migration in 3 Schritten

1. **Cleanup-Compose + Schema-Härtung** in den raw-Branch einbauen. Structured-Branch lassen.
2. **Eine Woche im Produktiv-Modus** überwachen: Parse_JSON-Fail-Rate? Wenn niedriger als die alte „structured-output-fehlt"-Rate → grünes Licht.
3. **Structured-Branch löschen**: alle `_1`, `_V2_1`, `_3_3` Duplikate, der structured-side Condition-Check, `For_each_-_Document_in_Prompt` mit ganzem Subtree. Mindestens halber Flow weg.

## Wann doch zwei Branches sinnvoll sind

- **Wenn die zwei Pfade fundamental verschiedene Logik brauchen** — z.B. structuredOutput hat zusätzliche Felder, die im text-Output fehlen, und du brauchst beide. Selten der Fall.
- **Wenn der Custom Prompt mehrere Versionen haben muss** (z.B. „strikte JSON-Mode" vs „natürlichsprachlich") und beide Varianten produktiv koexistieren. Auch selten.
- **Wenn Parse_JSON aus regulatorischen Gründen verboten ist** (z.B. structured ist garantiert validiert, raw nicht). Dann lieber das structured erzwingen via Prompt-Engineering, statt zwei Pfade.

In den meisten Fällen: **Single-Path über `text` ist die richtige Wahl**, mit gehärtetem Parse_JSON.

## Trigger-Case 2026-06-05

Im Koster-Subunternehmer-Flow 02 hat das Doppel-Branch-Pattern direkt zu mehreren Bug-Klassen beigetragen:

- 10+ duplicate Update-Actions (`Update_a_row__-_Eingangsqueue_verarbeitet_1` bis `_6`)
- Doppelte Move-Logik mit eigenen `_V2_1` Suffixen
- Bug-Diagnose war doppelt: jeder Fix musste in beiden Branches gemacht werden
- Nach Reduktion auf Single-Path (raw text only) ist der Flow **physisch um die Hälfte kleiner**, Maintenance-Aufwand merklich reduziert

Lehre: **die Heterogenität des AI-Outputs gehört in den Parse-Schritt, nicht in die Branch-Logik des ganzen Flows.**

## Verwandt

- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline]] — Trigger-Case mit Cluster D
- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — strukturierte JSON-Ausgabe]] — Prompt-Härtungen
- [[50.work/power-platform/power-automate-variable-binary-damage|Power Automate Variable Binary Damage]] — verwandte Lehre
- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]] — konkreter Projekt-Kontext
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
