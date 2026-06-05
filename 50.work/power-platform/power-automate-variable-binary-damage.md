---
source: chat-context 2026-06-05
imported: 2026-06-05
type: pattern
tags: [power-platform, power-automate, binary, encoding, utf-8, variables, troubleshooting]
related_projects: ["[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"]
trigger_case: "PDF4me-Output via Variable in SharePoint Create_file (Koster AG, 2026-06-05)"
---

# Power Automate — Variablen sind nicht binary-safe

## Problem

Jeder Power-Automate-Flow, der **Binary-Content** (PDF, ZIP, Image, irgendetwas was nicht reines ASCII ist) durch eine Variable schleift, läuft Gefahr, ihn zu zerstören. Das Symptom ist tückisch: das File wird erstellt, der nachfolgende Connector meldet keinen Fehler, der Reader öffnet die Datei sogar — aber der **Inhalt ist beschädigt**.

Typisches Beispiel für PDFs:
- Struktur intakt: Header, Catalog, Page-Tree, Cross-Reference, EOF — alles korrekt
- Page-Count korrekt: der Reader zeigt "6 Pages" oder "9 Pages"
- Aber: **alle Seiten visuell leer**

Für ZIPs:
- File-Listing zeigt korrekte Entry-Namen
- Aber: jedes Entry beim Entpacken „Corrupted"

## Der diagnostische Goldstandard — `EF BF BD`

Lauf `pdftotext` (oder ein vergleichbares Tool) auf das verdächtige File. Wenn du in den Fehlermeldungen siehst:

```
Syntax Error: Illegal character <ef> <bf> <bd> in hex string
Bad FCHECK in flate stream
```

…dann ist die Diagnose eindeutig: **`EF BF BD` ist die UTF-8-Sequenz für das Unicode-Replacement-Character (U+FFFD)** — das Zeichen, das angezeigt wird, wenn beim UTF-8-Decoding ein ungültiges Byte gefunden wird.

Übersetzt: irgendwo zwischen Connector-Output und Connector-Input wurde der Binary-Stream als UTF-8-String interpretiert und alle Bytes ≥ `0x80`, die keine gültigen UTF-8-Multi-Byte-Sequenzen bilden, wurden durch `EF BF BD` ersetzt.

Bei einem PDF heißt das: die ASCII-Teile (Header, Catalog, Pages-Tree) bleiben intakt. Aber die **Flate-komprimierten Page-Streams** (mit ZLIB-Headers wie `78 9C` oder `78 DA`, beide ≥ `0x80`) werden verstümmelt → der Reader kann sie nicht dekomprimieren → leere Seiten.

## Warum Variablen das Problem sind

Power Automate hält Variablen intern als **UTF-8-Strings**, unabhängig vom deklarierten Type:

| Variable Type | Verhalten bei Binary-Content |
|---|---|
| `string` | Direkter UTF-8-Cast — alle non-UTF-8-Bytes werden zu `EF BF BD` |
| `object` | JSON-Object-Wrapper, aber Inhalt geht auch durch UTF-8-Stringification → gleicher Damage |
| `array` | Wie object |

**Es gibt keine binary-safe Variable in Power Automate.** Auch nicht `object`. Das ist eine fundamentale Eigenschaft der Plattform.

## Lösung — Variablen für Binary komplett vermeiden

Connector-Output **direkt** in den nächsten Connector-Input durchschleifen. Kein Set-Variable, kein Compose, kein Zwischenschritt.

```
// FALSCH:
Set variable: File Content = @outputs('PDF4me_Split')?['body/splitedDocuments']?[index]?['streamFile']
Create_file body: @variables('File Content')

// RICHTIG:
Create_file body: @outputs('PDF4me_Split')?['body/splitedDocuments']?[index]?['streamFile']
```

Power Automate erkennt Connector-zu-Connector-Pass-Through und behält die internen Binary-Wrapper-Referenzen bei — ohne UTF-8-Konvertierung. Der Binary-Stream wandert byte-genau weiter.

### Wenn du eine if()-Logik brauchst

Statt:
```
Set variable: File Content = @if(<cond>, <binary1>, <binary2>)
Create_file body: @variables('File Content')
```

Lieber **zwei separate Create_file Actions** in zwei Branches einer Condition:
```
Condition:
  IF: Create_file_A   body: @<binary1>
  ELSE: Create_file_B body: @<binary2>
```

Und für nachgelagerte Actions, die einen einheitlichen Output brauchen (z.B. File-ID für Move), eine Compose-Bridge mit if() über die **String-Felder** der jeweiligen Create_file-Outputs (Ids, Paths, ItemIds sind alle Strings — safe):

```
Compose_SP_File_Id:
  @if(<cond>, outputs('Create_file_A')?['body/Id'], outputs('Create_file_B')?['body/Id'])
```

## Diagnose-Composes

Vor jedem Create_file (oder anderem Binary-Konsumenten) drei Composes einbauen — kostet nichts, deckt 90 % der Encoding-Bugs in 2 Minuten auf:

```
DEBUG_length: @length(<file content expr>)
DEBUG_head:   @substring(<file content expr>, 0, 12)
DEBUG_tail:   @substring(<file content expr>, sub(length(<file content expr>), 12), 12)
```

Erwartungen für PDF:

| `head` | `tail` | Interpretation |
|---|---|---|
| `%PDF-1.4` / `%PDF-1.7` | `%%EOF\n` | Binary PDF — direkt durchschleifen, kein decode |
| `JVBERi0xLjQK` | endet auf `=` / `==` | Base64 PDF — `base64ToBinary()` nötig |
| `{"$content"` | endet auf `}` | Object/JSON gewrappt — `?['$content']` oder Connector-Output direkt |
| `null` (4 Bytes) | — | Variable war undefiniert — Reference-Bug, nicht Encoding |
| irgendwas mit `\xef\xbf\xbd` darin | — | **UTF-8-Damage** — Variable rausnehmen |

## Falsche Verdachtsmomente (was es NICHT ist)

Wenn du das `EF BF BD`-Pattern siehst, kannst du folgende Hypothesen sofort ausschließen:

- ❌ **`base64ToBinary()` fehlt oder ist falsch platziert** — der Damage ist schon passiert, bevor du dekodierst
- ❌ **`base64ToBinary()` ist überflüssig** — geht in dieselbe Richtung
- ❌ **Variable Type ist falsch (string vs object)** — beide haben das Problem
- ❌ **PDF4me-Quota / Connector-Bug** — die liefern korrekten Output, Power Automate zerstört ihn
- ❌ **Curly Braces `@{...}` vs `@...`** — kann zusätzlich Schäden anrichten, aber die UTF-8-Konvertierung passiert auch ohne Braces
- ❌ **Encoding-Funktionen (`base64`, `string`, `encodeUriComponent`)** — alle gehen durch dieselbe String-Pipeline

Der **einzige** zuverlässige Fix: **Variable raus**.

## Wann nicht relevant

- **Reines ASCII-Content** (CSV, JSON, XML mit ASCII-Strings): Variablen sind OK. UTF-8 ist ASCII-kompatibel für Bytes < `0x80`.
- **Content der schon Base64-String ist und Base64-String bleiben soll**: auch OK, weil Base64 ist ASCII.
- **Wenn du `base64ToBinary` ganz am Ende machst, kurz vor dem Connector-Konsumenten**: technisch korrekt, aber zerbrechlich (jede Refactoring kann das wieder brechen). Lieber Connector-Output direkt durchschleifen.

## Verwandt

- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline]] — Trigger-Case mit Cluster A2
- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]] — konkreter Projekt-Kontext
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
