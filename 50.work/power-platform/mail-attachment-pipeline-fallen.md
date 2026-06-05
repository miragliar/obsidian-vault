---
source: chat-context 2026-06-05
imported: 2026-06-05
type: pattern
tags: [power-platform, power-automate, sharepoint, dataverse, pdf, base64, ai-builder, troubleshooting]
related_projects: ["[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"]
trigger_case: "Subunternehmerflow 02 / H. Baumann (Koster AG, 2026-06-05)"
---

# Mail-Attachment-Pipeline — Counter-, Encoding- und Duplicate-Fallen

Power-Automate-Flows, die **eingehende Mail-Anhänge** durch eine KI-Klassifikation schicken, in **SharePoint** ablegen und in **Dataverse** referenzieren, haben eine wiederkehrende Klasse von Bugs. Die hier dokumentierten stammen aus dem Koster-„Subunternehmerflow 02" — die Pattern sind aber generisch.

Pipeline-Skelett:

```
Mail-Trigger (Outlook V2)
  For_each Attachment
    Add_a_new_row     →  ks_eingangsqueues (initialer Eintrag, Status = "Neu")
    Run_a_prompt      →  AI Builder Custom Prompt (mal structured, mal raw text)
    Condition         →  structured vs. raw Branch
    PDF_-_Split       →  PDF4me (bei Multi-Doc-PDFs)
    Set variable      →  File Content (string, base64)
    Create_file       →  SP /03_Eingang_Temp (initial-Ablage)
    [optional] Move_file  →  SP /02_Kunden/<Sub>/<Auftrag>/  (bei Erfolg)
    Update_a_row      →  ks_eingangsqueues (Status) + ks_deklarationens (final-Pfad)
```

## Was das **nicht** ist (Diagnose-Hygiene)

Zwei Verdachtsmomente, die naheliegen, aber im echten Setup **kein** Bug sind:

1. **`@{...}`-String-Interpolation vs. `@...`-Expression** im exportierten Solution-JSON
   Im **Designer** sieht die Expression korrekt aus. Der Solution-Export-ZIP rendert manche Expressions inkonsistent (mit/ohne Curly Braces). Vor einer Hypothese auf Basis des exportierten JSON **immer** im Designer die tatsächliche Expression verifizieren. Sonst jagt man Export-Artefakte statt Bugs.

2. **`ks_eq_dateipfad_manuell` ist leer bei erfolgreichem Move** — by design
   Das `_manuell`-Feld ist **nur** für den Fall gedacht, dass der User manuell taggen muss (Status `Manuell`). Im Erfolgsfall (Klassifikation gelingt, Datei wandert in den Kunden-Ordner) liegt der finale SP-Pfad in `ks_deklarationens.ks_antwort_sp_pfad`. Die Eingangsqueue ist eine **Bearbeitungs-Queue**, kein Archiv-Index. Wer die Datei sucht, geht über die Deklaration.

→ Wenn ein User-Report behauptet „Pfad in Eingangsqueue stimmt nicht mit SP überein", ist das **nicht** Schema-Lücke, sondern ein Hinweis auf eine **andere** Ursache (siehe Cluster B).

## Problem

### Cluster A — Leere PDFs (korrekte Seitenanzahl, weiße Seiten)

Symptom: das resultierende PDF in SharePoint hat die **richtige Seitenzahl**, jede Seite ist **leer**. Schließt aus: „Variable war null" (dann wäre das File 0 Bytes oder nicht erstellt). Bestätigt: **Page-Catalog intakt, Page-Streams beschädigt**.

Typische Quellen:

1. **Counter-Variable nicht resettet** zwischen Iterationen des **äußeren** `For_each` (über alle Attachments einer Mail).
   Beispiel: `PDF` (integer-Counter für den Split-Index) wird via `Initialize_variable` einmalig auf 0 gesetzt — am **Flow-Start**, nicht pro Attachment. Im Inner-Loop wird er via `Increment_variable` hochgezählt (`splitedDocuments[0..n]`). Wenn die Mail mehrere Attachments hat, beginnt die zweite Iteration mit dem **alten** Wert. → `splitedDocuments[3]` für ein PDF mit nur 2 Sub-Docs = `null` → leere Datei mit korrektem Header.

2. **`base64ToBinary()` Fehl-Wrap im Create_file body**
   PDF4me's `streamFile` ist ein base64-String. SharePoint `Create_file` akzeptiert beide Formate — aber nicht über alle Encoding-Pfade hinweg konsistent. Wenn die Variable als `type: string` deklariert ist und der String durch eine `if()`-Branch-Auswahl geht, ist das Verhalten implementation-defined. Sicheres Pattern: **base64-String halten**, am Create_file explizit dekodieren.

3. **`if()` mit Typ-Mismatch zwischen den Branches**
   ```
   "body": "@if(<cond>, variables('File Content'), variables('File Content Binary'))"
   //                    ↑ type: string              ↑ type: object
   ```
   Power Automate evaluiert beide Branches. Wenn eine string und die andere object ist, kann die nicht-gewählte Variable trotzdem einen Type-Cast triggern, der die gewählte beeinflusst. Sauber: **beide Variablen denselben Typ**.

### Cluster B — Datei landet im falschen Ordner

Symptom: User-Report sagt „die Datei sollte in `03_Eingang_Temp` sein (Status `Manuell`), liegt aber in `02_Kunden/<Sub>/...`". Die Eingangsqueue zeigt einen `_manuell`-Pfad, der ins Leere führt.

Zwei wahrscheinlichste Ursachen:

1. **Duplicate-Trigger** vom Outlook-V2-Connector — **Top-Verdacht**
   Bei Forwards/Replys/Re-Delivery feuert der Mail-Trigger denselben `internetMessageId` mehrmals. Ohne Dedup landen **zwei `ks_eingangsqueues`-Einträge** mit derselben MailID:
   - Run #1: KI klassifiziert erfolgreich → `Move_file` nach `02_Kunden/<Sub>/...` → EQ-Eintrag mit Status `Verarbeitet` (kein `_manuell`-Pfad, by design).
   - Run #2: gleiche Mail, KI-Output diesmal anders (Custom Prompts sind nicht deterministisch) → kein Match → kein Move → EQ-Eintrag mit Status `Manuell` + `_manuell`-Pfad = `03_Eingang_Temp` (Create_file-Output, aber die Datei wurde von Run #1 schon weggemoved → der Pfad ist **stale**).
   - User sieht Run #2's Eintrag → klickt → 404.

2. **Falsches Move-Ziel durch fragiles `split('/K20')[0]`**
   ```
   "destinationFolderPath": "@split(items('For_each')?['ks_versendet_sp_pfad'], '/K20')[0]"
   ```
   Nimmt den Pfad einer **Deklaration**, splittet am Auftrags-Prefix (`/K20...`), nimmt Teil [0]. Bricht:
   - Bei Pfaden ohne `/K20` → `split()[0]` = ganzer Pfad inkl. Dateinamen → Move-Ziel = unsinniger Ordner (oder Move schlägt fehl).
   - **Beim Jahres-Wechsel auf K27** (2027): splittet plötzlich an einer Stelle, die nicht mehr existiert.
   - Wenn `ks_versendet_sp_pfad` der Deklaration **stale** ist (z.B. vom Vorjahres-Auftrag) → Move-Ziel ist ein alter Ordner.

### Cluster C — `attachmenthash` ist kein Hash

Kosmetisch, aber irreführend bei Debug-Reports:

```
"item/ks_eq_attachmenthash": "@item()?['contentType']"
```

Schreibt `application/pdf` ins Hash-Feld. Wer auf Hash-Basis dedupen will (gleicher Anhang, andere MailID), hat hier nichts.

## Lösung

### Cluster A

**A1 — Counter-Reset am Anfang jeder äußeren Iteration:**

Direkt nach `Add_a_new_row` (also für jedes Mail-Attachment einmal) einen `Set variable PDF = 0` einbauen. Sonst wandert der Index in die nächste Attachment-Iteration.

**A2 — Create_file body explizit dekodieren:**

```
"body": "@base64ToBinary(
  if(
    greater(length(outputs('Run_a_prompt')?['body/responsev2/predictionOutput/structuredOutput/result']), 1),
    variables('File Content'),
    base64(string(variables('File Content Binary')))
  )
)"
```

Sauberer: beide Variablen als `type: string` (base64) halten, am Create_file einmal `base64ToBinary()`.

**A3 — Diagnostik vor jedem Create_file:**

Compose-Steps mit:

| Compose | Wert | Erwartet |
|---|---|---|
| `DEBUG_length` | `length(<file content expr>)` | ~30k+ für mehrseitige PDFs |
| `DEBUG_head` | `substring(<expr>, 0, 8)` | `JVBERi0x` (base64-PDF) oder `%PDF-1.x` (binary) |

Wenn `head` etwas anderes ist → Variable ist null/leer/falsch befüllt.

### Cluster B

**B1 — Duplicate-Detection direkt nach Trigger:**

Vor `Add_a_new_row`:

```
List_rows
  entityName: ks_eingangsqueues
  $filter: ks_eq_mailid eq '@{triggerOutputs()?['body/internetMessageId']}'
  $top: 1

Condition: length(outputs('List_rows')?['body/value']) eq 0
  IF: weiter mit Add_a_new_row + ganzer Verarbeitung
  ELSE: Terminate (Cancelled) mit Nachricht „bereits verarbeitet"
```

Schließt **Duplicate-Trigger, Mail-Forward, Re-Delivery** in einem aus.

**B2 — Move-Destination via Lookup, nicht via `split`:**

Statt aus `ks_versendet_sp_pfad` einer Deklaration zu splitten: expliziter `Get_a_row_by_ID` auf die Subunternehmer-Entity, mit einer Spalte `ks_root_folder` (= `/02_Kunden/<Sub>/`). Der Auftrag-Sub-Folder kommt aus dem Auftrag-Lookup. Robust gegen Jahres-Wechsel und Strukturänderungen.

### Cluster C

**C1 — Echten Hash schreiben oder Feld umbenennen:**

```
// Variante 1: Hash für Inhalts-Dedup
"item/ks_eq_attachmenthash": "@{base64(sha256(item()?['contentBytes']))}"

// Variante 2: Feld umbenennen zu ks_eq_contenttype
```

Mit echtem Hash wird inhalts-basierte Dedup möglich (gleicher Anhang, andere MessageID — auch nützlich gegen Re-Delivery, falls B1 mal Subject-statt-MessageID nimmt).

## Diagnose-Reihenfolge bei Bug-Report

Wenn der Report lautet „Datei nicht da wo der EQ-Eintrag sagt" oder „PDF ist leer":

1. **Dataverse-Query auf `ks_eq_mailid`** des betroffenen Eintrags → wie viele Treffer?
   - `>1` = Duplicate-Trigger bestätigt → Cluster B1
   - `==1` → weiter mit 2.
2. **Flow-Run-History** nach `internetMessageId` filtern → wie viele Runs?
   - `>1` ohne Duplicate-EQ → ein Run hat `Add_a_new_row` failed, der nächste erfolgreich; trotzdem könnten beide ein Move ausgeführt haben → Race-Analyse.
3. **`ks_deklarationens` mit `ks_antwort_sp_pfad like '%<filename>%'`** → wenn Treffer → Datei wurde gemoved (Cluster B1 oder B2 hat zugeschlagen).
4. **File-Size-Vergleich** Original-Anhang ↔ SharePoint-Datei →
   - identisch → eher Pfad-/Verwirrungs-Problem (Cluster B)
   - deutlich kleiner / ähnliche Header → Encoding-Bug (Cluster A2)
   - 0 Bytes / Default-Größe → Variable war null (Cluster A1: Counter-Bug)

## Wann nicht relevant

- **Nur ein Eingangs-Mail-Postfach pro Mandant, keine Forwards**: dann ist Cluster B1 (Duplicate-Detection) optional. Trotzdem empfehlenswert als Defense-in-Depth.
- **Wenn kein PDF-Split nötig** (jeder Anhang = ein Dokument): dann reicht eine einzige `File Content`-Variable als `type: string` mit dem base64 direkt aus `item()?['contentBytes']`. Kein Counter, kein Cluster A1.
- **Wenn der KI-Output deterministisch structured ist** (z.B. AI Builder Classification statt Custom Prompt): dann fällt der gesamte Raw-Text-Fallback-Branch weg → das Doppel-Branch-Pattern (For_each_-_Document_in_Prompt vs. Apply_to_each) verschwindet → weniger Stellen, wo Cluster A zuschlagen kann.

## Verwandt

- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]] — Trigger-Case
- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — JSON-Output]] — warum der Custom Prompt mal structured, mal raw liefert
- [[50.work/power-platform/power-automate-string-expressions|String-Expressions & Locale-Fallen]] — Pfad-Split-Patterns mit `split()`/`indexOf`
- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Save-Voraussetzung]] — verwandtes Symptom „File scheinbar nicht da"
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
