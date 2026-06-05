---
source: chat-context 2026-06-05
imported: 2026-06-05
updated: 2026-06-05
type: pattern
tags: [power-platform, power-automate, sharepoint, dataverse, pdf, base64, ai-builder, pdf4me, outlook, troubleshooting]
related_projects: ["[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"]
trigger_case: "Subunternehmerflow 02 / H. Baumann (Koster AG, 2026-06-05)"
related_patterns: ["[[50.work/power-platform/power-automate-variable-binary-damage]]", "[[50.work/power-platform/ai-builder-doppel-branch-vermeiden]]"]
---

# Mail-Attachment-Pipeline — Komplette Bug-Klasse

Power-Automate-Flows, die **eingehende Mail-Anhänge** durch eine KI-Klassifikation schicken, in **SharePoint** ablegen und in **Dataverse** referenzieren, haben eine wiederkehrende Klasse von Bugs. Diese Notiz dokumentiert die komplette Reise einer Debugging-Session am Koster-Subunternehmer-Flow 02 — mit allen Sackgassen, finalen Lösungen und Diagnose-Reihenfolgen.

Pipeline-Skelett (final, nach allen Fixes):

```
Mail-Trigger (Outlook V2)
  For_each Attachment                              ← iteriert über E-Mail-Anhänge
    Condition - PNG Filter
      Run a prompt                                 ← AI Builder Custom Prompt (raw text)
      Bereich (Scope)
        [Compose_clean_json — Markdown-Fence-Strip]
        Parse_JSON                                  ← gegen predictionOutput/text
        Condition_Split
          IF: PDF4me Split_Document_2              ← bei Multi-Doc-PDFs
      Apply_to_each (über Parse_JSON?['result'])    ← iteriert über KI-Sub-Docs
        Add_a_new_row                              ← EQ-Eintrag PRO Sub-Doc
        Condition 2 (length(result) > 1?)
          IF (Multi-Doc):
            Create_file_Multi
              body: @outputs('PDF_-_Split_Document_2')?['body/splitedDocuments']?[iterationIndexes('Apply_to_each')]?['streamFile']
          ELSE (Single-Doc):
            Create_file_Single
              body: @items('For_each')?['contentBytes']
        Compose_SP_File_Id      ← URL-encoded für Move_file
        Compose_SP_File_ItemId  ← numeric für Dataverse
        Compose_SP_File_Path    ← lesbarer Pfad für Display
        Condition - hat Deklaration ID?
          → 4 Endzustände, 4 Updates (siehe unten)
      [Failure-Branch wenn Parse_JSON failt: separater Add_a_new_row mit Status "Verarbeiten fehlgeschlagen"]
```

---

## Was es nicht ist (Diagnose-Hygiene)

**Diese Verdachtsmomente wurden geprüft und ausgeschlossen** — nicht erneut verfolgen, wenn ein ähnlicher Bug-Report kommt:

1. **Duplicate-Trigger vom Outlook-V2-Connector** — bei eindeutigen `internetMessageId`s pro Mail ist es das nicht. Selbst bei Forwards/Re-Delivery feuert der Connector mit jeweils unterschiedlichen MessageIDs.

2. **PDF4me-Quota** — würde einen HTTP-Error werfen (`429 Too Many Requests` o.ä.), nicht stillschweigend strukturell intakte aber leere PDFs liefern. Bei sichtbaren DEBUG-Längen im Multi-KB-Range ist das Quota nicht das Problem.

3. **Solution-Export-Artefakte ≠ Designer-Realität** — der Solution-Export rendert manche Expressions inkonsistent (z.B. mit/ohne Curly Braces). **ABER**: wenn ein User sagt „im Designer sieht es normal aus", trotzdem die **roh kopierte Expression** aus dem Designer-Eingabefeld sehen lassen. Die Designer-UI rendert visuell ohne Braces, aber das Token kann sie tragen. Beim Koster-Case **war** das `@{...}` real und KEIN Export-Artefakt.

4. **`ks_eq_dateipfad_manuell` leer im Erfolgsfall** ist **by design** — die Eingangsqueue ist eine Bearbeitungs-Queue, kein Archiv-Index. Im Erfolgsfall lebt der finale Pfad in `ks_deklarationens.ks_antwort_sp_pfad`. Wer die Datei sucht, geht über die Deklaration.

---

## Cluster A — Encoding & Binary-Damage

### A1 — `@{expression}` mit Curly Braces zerstört Base64/Binary

**Symptom**: leere PDFs mit korrekter Page-Count, oder `base64ToBinary` Error „cannot be decoded from base64 representation".

**Ursache**: `@{...}` forciert String-Interpolation. Bei langen Base64-Werten (>100 KB) injiziert das Linefeeds/Whitespace/Escape-Artefakte → Base64-Parser steigt aus oder dekodiert zu beschädigtem Binary.

**Fix**: `@{expression}` → `@expression` (ohne Curly Braces).

```
// FALSCH:
"value": "@{outputs('PDF_-_Split_Document_2')?['body/splitedDocuments']?[variables('PDF')]?['streamFile']}"

// RICHTIG:
"value": "@outputs('PDF_-_Split_Document_2')?['body/splitedDocuments']?[variables('PDF')]?['streamFile']"
```

### A2 — Variablen sind NICHT binary-safe (auch nicht als `object`)

**Symptom**: PDF strukturell ok (Header, Catalog, Page-Tree, EOF), aber alle Seiten visuell leer. `pdftotext` zeigt:
```
Syntax Error: Illegal character <ef> <bf> <bd> in hex string
Bad FCHECK in flate stream
```

**Diagnostischer Goldstandard**: `EF BF BD` ist die UTF-8-Sequenz für das Unicode-Replacement-Character (U+FFFD). Sobald du diese Bytes in einem geschriebenen Binary-File siehst, **war ein UTF-8-Roundtrip dazwischen**.

**Ursache**: Power Automate hält Variablen intern als UTF-8-Strings. Sobald Binary-Content (PDF page streams, ZIP-Header etc.) durch eine Variable wandert, werden alle Bytes ≥ `0x80` (die kein gültiges UTF-8-Startbyte sind) durch `EF BF BD` ersetzt. **Auch der Variable-Type `object` schützt nicht** — er ist ein JSON-Object-Container, kein Binary-Container.

**Fix**: Variablen für Binary-Content **komplett vermeiden**. Connector-Output direkt in den nächsten Connector-Input durchschleifen.

Statt:
```
Set variable: File Content = @outputs('PDF4me_Split')?['body/splitedDocuments']?[...]?['streamFile']
Create_file body: @variables('File Content')
```

Direkt:
```
Create_file body: @outputs('PDF4me_Split')?['body/splitedDocuments']?[...]?['streamFile']
```

Power Automate erkennt Connector-zu-Connector-Pass-Through und behält die internen Binary-Wrapper-Referenzen bei. Kein String-Cast, kein UTF-8-Damage.

### A3 — Diagnose-Composes (vor jedem Create_file einbauen)

```
DEBUG_length: @length(<file content expr>)
DEBUG_head:   @substring(<file content expr>, 0, 12)
DEBUG_tail:   @substring(<file content expr>, sub(length(<file content expr>), 12), 12)
```

Erwartung:
| `head` | `tail` | Interpretation |
|---|---|---|
| `%PDF-1.4` / `%PDF-1.7` | `%%EOF\n` | Binary PDF — direkt in Create_file, kein decode |
| `JVBERi0xLjQK` | endet auf `=` oder `==` | Base64 PDF — `base64ToBinary()` nötig |
| `{"$content"` | endet auf `}` | Object/JSON gewrappt — `?['$content']` zugreifen oder Connector-Output direkt |
| `null` (literal 4 Bytes) | — | Variable war undefiniert — siehe Cluster B |

---

## Cluster B — Index- und Reference-Falle

### B1 — `items('Apply_to_each')` vs `items('For_each')`

**Symptom**: Single-Doc-Files in SharePoint sind 4 Bytes groß, Inhalt ist literal `null` (ASCII n-u-l-l).

**Ursache**: Im inneren `Apply_to_each` iterierst du über `body('Parse_JSON')?['result']` — das sind **KI-Klassifikations-Objects** mit Feldern wie `deklaration_id`, `dokumententyp`, `firmenname`. Es gibt da kein `contentBytes`.

```
// FALSCH (im inneren Loop):
@items('Apply_to_each')?['contentBytes']   ← greift auf KI-Object, kein contentBytes → null

// RICHTIG:
@items('For_each')?['contentBytes']         ← greift auf das äußere Mail-Attachment
```

**Regel**: `items('<loopname>')` greift IMMER auf das aktuelle Item des **benannten** Loops. In Nested-Loops muss man den richtigen Loop-Namen referenzieren — `items('For_each')` für Attachments, `items('Apply_to_each')` für KI-Sub-Docs.

### B2 — PDF-Split-Counter Off-by-One

**Symptom**: Bei gesplitteten PDFs sind Filename und Content vertauscht. Beispiel: Rahmenvertrag (RV)-Inhalt wird mit MINARB-Filename gespeichert, MINARB-Datei ist null/kaputt.

**Ursache**: `Increment variable` läuft vor `Create_file`. Sequenz:
- Iteration 1: PDF=0 → Increment → PDF=1 → Create_file mit `splitedDocuments[1]` (= RV-Content) aber Filename aus `result[0]` (= MINARB) → Vertauschung
- Iteration 2: PDF=1 → Increment → PDF=2 → `splitedDocuments[2]` ist out-of-bounds → null

Im Original-Flow fiel das nicht auf, weil dort `Set variable 3` **vor** `Increment` lief und den richtigen Wert (PDF=0) schnappte. Nach Variable-Elimination wandert der Index-Lookup hinter den Increment.

**Fix — minimal**: Increment-Action nach Create_file verschieben (`runAfter: Create_file: Succeeded`).

**Fix — sauber**: Counter-Variable komplett raus, `iterationIndexes('Apply_to_each')` verwenden:

```
Create_file_Multi body:
  @outputs('PDF_-_Split_Document_2')?['body/splitedDocuments']?[iterationIndexes('Apply_to_each')]?['streamFile']
```

Damit fallen weg:
- `Initialize variable - PDF`
- `Set variable - PDF auf 0` (Counter-Reset im outer For_each)
- `Increment variable 2`

Voraussetzung: die Reihenfolge in `Parse_JSON?['result']` muss mit der Reihenfolge in `splitedDocuments` übereinstimmen. Das ist der Fall, wenn `Seite_von_bis_concat` (der splitRanges-Input für PDF4me) in derselben Reihenfolge generiert wird wie `result` — im AI-Prompt explizit fordern: „`Seite_von_bis_concat` enthält die Page-Ranges in derselben Reihenfolge wie die Dokumente in `result`".

### B3 — Counter-Reset zwischen Attachment-Iterationen

**Nur relevant wenn man trotzdem einen Counter behalten muss** (z.B. weil mehrere Apply_to_each parallel laufen):

`Initialize variable: PDF = 0` läuft **einmal** beim Flow-Start, nicht pro Attachment. Im outer `For_each` (über Attachments) wandert der Counter-Wert in die nächste Attachment-Iteration → bei zweitem Multi-Doc-PDF läuft der Index out-of-bounds.

Fix: `Set variable PDF = 0` direkt nach Beginn jeder outer-For_each-Iteration.

---

## Cluster C — Architektur-Falle: Add_a_new_row außerhalb innerer Loops

### C1 — Multi-Iteration-Update-Override

**Symptom**: User sieht in der EQ einen Status/Pfad, der nicht zur physischen Datei passt. Bei Multi-Doc-PDF sieht die EQ `Manuell` + `03_Eingang_Temp/...`, obwohl die Datei real in `02_Kunden/<Sub>/...` liegt.

**Ursache**: `Add_a_new_row` läuft **außerhalb** der inneren Loops (`For_each_-_Document_in_Prompt` bzw. `Apply_to_each`) → pro Mail-Attachment gibt es **einen** EQ-Eintrag, auch wenn PDF4me daraus N Sub-Docs macht. Alle N Iterationen updaten denselben Record (`recordId = outputs('Add_a_new_row')?['body/ks_eingangsqueueid']`) — **der letzte gewinnt**.

Wenn ein Anhang gemischte Klassifikations-Ergebnisse produziert (Sub-Doc 1 erfolgreich, Sub-Doc 2 fehlgeschlagen), zeigt der EQ-Eintrag am Ende den Status von Sub-Doc 2 — aber Sub-Doc 1's Datei liegt real im Kundenordner.

**Fix**: `Add_a_new_row` **in den inneren Loop verschieben** → ein EQ-Eintrag pro Sub-Doc. Jede Iteration hat ihren eigenen Record, kein Override.

### C2 — Status-Matrix pro Endzustand

Nach C1-Fix gibt es pro Iteration vier mögliche Endzustände, also 4-5 Update-Aktionen pro Branch:

| # | Klassifikations-Ergebnis | Status-Code | `ks_eq_dateipfad_manuell` | `ks_eq_fehlertext` |
|---|---|---|---|---|
| 1 | Deklaration-ID gefunden + in DB → Move erfolgreich | `124080001` Verarbeitet | — (leer, by design) | — |
| 2 | Deklaration-ID gefunden, aber NICHT in DB | `124080003` Manuell | `Compose_SP_File_Path` | `"Deklaration-ID '<id>' nicht in Dataverse"` |
| 3 | Keine ID, aber Sub-Name → Move erfolgreich | `124080001` Verarbeitet | — | — |
| 3b | Keine ID, Sub-Name, aber Scope failed | `124080003` Manuell | `Compose_SP_File_Path` | `"Sub-Name-Verarbeitung fehlgeschlagen"` |
| 4 | Weder ID noch Sub-Name | `124080003` Manuell | `Compose_SP_File_Path` | `"Kein Subunternehmer und keine DeklarationsID erkannt"` |

Plus außerhalb der Loops bei komplettem KI-Fail:

| # | Wann | Status | Notiz |
|---|---|---|---|
| 5 | `Parse_JSON` failed oder `result` leer | `124080002` Verarbeiten fehlgeschlagen | Separater `Add_a_new_row` mit fehlertext "KI hat weder structured noch raw output geliefert" |

---

## Cluster D — Single-Path statt Doppel-Branch

### D1 — Doppel-Branch (structured + raw) bei nicht-deterministischem AI-Output vermeiden

**Symptom**: Custom Prompts liefern mal `structuredOutput`, mal nur `text`. Der ursprüngliche Flow hatte zwei parallele Branches — strukturell identisch, aber doppelt zu pflegen.

**Fix**: Den **Lowest-Common-Denominator** wählen — bei AI Builder Custom Prompts ist das immer `predictionOutput/text` (= roher LLM-Output, immer gefüllt). Über `Parse_JSON` aus dem text-Feld bekommt man identische Daten, egal ob structured kam oder nicht.

Vorteile:
- Bug-Surface halbiert
- Single-Path-Diagnose statt verzweigt
- Multi-Iteration-Override-Risiko (Cluster C) bleibt strukturell unter Kontrolle
- Alle `_1`, `_V2_1`, `_3_3` Duplikate kollabieren auf eine Version

Voraussetzung: **Parse_JSON-Härtung** — siehe [[50.work/power-platform/ai-prompt-json-output]]:
- Prompt schreibt „NUR JSON, kein Markdown-Fence, kein Erklärtext"
- Cleanup-Compose vor Parse_JSON: extrahiert Substring zwischen erstem `{` und letztem `}` (fängt Präambeln und Trailing-Whitespace ab)
- Schema mit `["string", "null"]` für alle optionalen Felder

---

## Cluster E — SharePoint-Identifier-Verwirrung

### E1 — Drei verschiedene IDs aus Create_file

SharePoint Create_file Output enthält drei verschiedene Identifier, die verschiedene nachgelagerte Connector-Calls erwarten:

| Feld | Beispiel | Wofür |
|---|---|---|
| `body/Id` | `%252fFreigegebene%2bDokumente%252f03_Eingang_Temp%252fdatei.pdf` | URL-encoded File-Identifier — für `Move_file.sourceFileId` |
| `body/ItemId` | `630` | Numerische SP Item-ID — für Dataverse-Lookups, REST APIs |
| `body/Path` | `/Freigegebene Dokumente/03_Eingang_Temp/datei.pdf` | Lesbarer Pfad — für Display, `ks_eq_dateipfad_manuell` |

**Pattern**: nach Create_file drei Compose-Bridges, die per `iterationIndexes` oder Condition den richtigen Wert liefern. Folge-Actions referenzieren die Composes, nicht die Create_file-Outputs direkt — das macht den Wechsel zwischen mehreren Create_file Branches transparent.

### E2 — Move vs. Create-File-Output für Dataverse

| Folge-Action | Feld | Quelle |
|---|---|---|
| `Move_file` | `sourceFileId` | `Compose_SP_File_Id` (URL-encoded vom Create_file) |
| `Update_a_row` mapped via ID (Deklaration) | `ks_antwort_sp_id` | `outputs('Move_file_X')?['body/ItemId']` (nach Move!) |
| `Update_a_row` mapped via ID (Deklaration) | `ks_antwort_sp_pfad` | `outputs('Move_file_X')?['body/Path']` (NEUER Pfad nach Move) |
| `Update_a_row` EQ Manuell-Pfade | `ks_eq_dateipfad_manuell` | `Compose_SP_File_Path` (Initial-Pfad in 03_Eingang_Temp, kein Move) |

ItemId bleibt typischerweise stabil beim Move innerhalb derselben SP-Library, aber **`body/Path` ändert sich** beim Move. Im Erfolgsfall die Move-Outputs nehmen — sicherer und semantisch korrekt.

---

## Cluster F — Pfad-Sync (Latente Risiken)

### F1 — Move-Destination via `split('/K20')[0]`

**Symptom**: Aktuell funktioniert es, könnte aber zukünftig brechen.

```
"destinationFolderPath": "@split(items('For_each')?['ks_versendet_sp_pfad'], '/K20')[0]"
```

Bricht:
- Beim Jahres-Wechsel auf K27 (2027) — splittet plötzlich an einer Stelle, die nicht existiert
- Bei Pfaden ohne `/K20` — gibt ganzen Pfad zurück, Move ins Leere
- Wenn `ks_versendet_sp_pfad` stale ist (Vorjahres-Auftrag) — falsches Ziel

**Fix**: Subunternehmer-Folder-Lookup. Expliziter `Get_a_row_by_ID` auf `crb4b_subunternehmers` mit einer Spalte `ks_root_folder` (= `/02_Kunden/<Sub>/`). Auftrag-Sub-Folder kommt aus dem Auftrag-Lookup.

### F2 — `ks_eq_attachmenthash` ist kein Hash

```
"item/ks_eq_attachmenthash": "@item()?['contentType']"
```

Schreibt MIME-Type (`application/pdf`) ins Hash-Feld. Kosmetisch, aber irreführend bei Debug — und blockiert echten Content-Hash-Dedup (z.B. für Forwards/Re-Delivery mit unterschiedlichen MessageIDs).

**Fix**: Echten Hash schreiben oder Feld umbenennen:
```
"item/ks_eq_attachmenthash": "@{base64(sha256(item()?['contentBytes']))}"
```

---

## Diagnose-Reihenfolge bei Bug-Report

Wenn der Report lautet „Datei nicht da wo der EQ-Eintrag sagt", „PDF ist leer", oder „Filename passt nicht zum Inhalt":

1. **EF-BF-BD-Check für leere PDFs**: `pdftotext <file>` ausführen. Wenn `Illegal character <ef> <bf> <bd> in hex string` und `Bad FCHECK in flate stream` → **Cluster A2** (Variable-Roundtrip mit Binary-Damage). Variablen für Content rauswerfen.
2. **`null`-Body-Check für 4-Byte-Files**: `xxd <file>` ausführen. Wenn `6e75 6c6c` (= „null") → **Cluster B1** (falsche Loop-Reference). `items('For_each')` statt `items('Apply_to_each')` verwenden.
3. **Filename-Content-Mismatch**: wenn ein PDF öffnet aber den falschen Inhalt zeigt, plus ein anderes File ist kaputt → **Cluster B2** (Counter Off-by-One). `iterationIndexes('Apply_to_each')` statt manuellem Counter.
4. **Pfad-vs-Lage-Diskrepanz** ohne der obigen Symptome: **Cluster C1** (Multi-Iteration-Override). Add_a_new_row in den inneren Loop verschieben.
5. **EQ-Eintrag fehlt komplett**: wahrscheinlich Parse_JSON gescheitert → Failure-Branch fehlt. Cluster C2 Punkt 5 einbauen.
6. **Multi-Doc-Check als Sanity**: ist `length(Parse_JSON?['result'])` > 1? Dann mehr Diagnostik nötig, weil mehrere Iterationen interagieren.

---

## Test-Setup für Mail-Attachment-Pipeline

Minimum-Test-Suite, die alle Cluster abdeckt:

| Test-Mail | Anhänge | Was getestet wird |
|---|---|---|
| (1) Single PDF (1 Sub-Doc) | 1 PDF, 1-5 Seiten | Single-Doc-Branch, Apply_to_each mit 1 Iteration |
| (2) Multi-PDF (1 Anhang, 2 Sub-Docs) | 1 PDF, 6-15 Seiten | Multi-Doc-Branch, PDF4me-Split, iterationIndexes |
| (3) Multi-Attachment | 2-3 PDFs | Counter-Reset im outer For_each, items('For_each')-Reference |
| (4) Mixed | 1 PDF Single + 1 PDF Multi-Doc | Beide Branches in einem Run, Variable-State zwischen Iterationen |
| (5) PNG | 1 PNG | PNG-Filter |
| (6) Korrupte/leere PDF | 1 leeres PDF | Failure-Branch (Parse_JSON failed) |

Pro Test verifizieren:
- Anzahl EQ-Einträge stimmt mit Anzahl Sub-Docs
- Jede SP-Datei öffnet sich als gültiges PDF
- Filename und Inhalt passen zusammen
- EQ-Pfad zeigt auf die echte Datei (bei Manuell-Status) bzw. ist leer (bei Verarbeitet-Status)
- Bei Multi-Doc: kein Update-Override zwischen Iterationen

---

## Wann nicht relevant

- **Single-Path-Flows ohne KI-Klassifikation** (z.B. „Mail-Anhang direkt in SharePoint speichern"): kein Loop, kein Counter, keine Variable nötig. `Create_file` body direkt mit `@triggerOutputs()?['body/attachments'][0]?['contentBytes']`.
- **Wenn der KI-Output deterministisch structured ist** (z.B. AI Builder Classification statt Custom Prompt): kein Doppel-Branch-Pattern nötig (Cluster D entfällt).
- **Wenn keine Multi-Doc-PDFs vorkommen**: kein PDF4me-Split, kein Counter (Cluster B2/B3 entfällt).
- **Wenn nur ein Anhang pro Mail garantiert ist**: kein outer `For_each` über Attachments → einige Bug-Klassen entfallen, aber das Pattern für Architektur (Add_a_new_row pro Sub-Doc) bleibt.

---

## Trigger-Case 2026-06-05 — Was real bestätigt wurde

Im Koster-Subunternehmer-Flow 02:
- **Cluster A2 bestätigt** durch `EF BF BD` in `pdftotext`-Output der gesplitteten PDFs → Variablen für Content entfernt
- **Cluster B1 bestätigt** durch 4-Byte `null`-File beim Single-Doc → `items('For_each')` Reference-Fix
- **Cluster B2 bestätigt** durch RV-Content mit MINARB-Filename + kaputte zweite Split-Datei → `iterationIndexes` statt manuellem Counter
- **Cluster C1 bestätigt** durch Multi-Doc-PDF mit gemischten Klassifikations-Ergebnissen → Add_a_new_row im inneren Loop
- **Cluster D umgesetzt** (Doppel-Branch entfernt, nur noch raw-text-path)
- **Cluster A1 bestätigt** als realer Bug — `@{...}` war im Designer wirklich da, kein Export-Artefakt

Was als latent identifiziert wurde aber nicht akut war:
- **Cluster F1**: `split('/K20')` läuft, wird aber beim Jahres-Wechsel auf K27 brechen
- **Cluster F2**: `attachmenthash` schreibt MIME-Type statt Hash

---

## Verwandt

- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]] — Trigger-Case
- [[50.work/power-platform/power-automate-variable-binary-damage|Power Automate Variable Binary Damage]] — universelles Pattern, abgeleitet aus Cluster A2
- [[50.work/power-platform/ai-builder-doppel-branch-vermeiden|AI Builder — Doppel-Branch vermeiden]] — universelles Pattern, abgeleitet aus Cluster D
- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — JSON-Output]] — Prompt-Härtung für Parse_JSON-Robustheit
- [[50.work/power-platform/power-automate-string-expressions|String-Expressions & Locale-Fallen]] — Pfad-Split-Patterns
- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Save-Voraussetzung]] — verwandtes Symptom „File scheinbar nicht da"
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
