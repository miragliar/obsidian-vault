---
source: chat-context 2026-06-19
imported: 2026-06-19
type: pattern
tags: [power-platform, power-automate, ai-builder, architecture, error-handling, dataverse, optionset]
related_projects: ["[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"]
trigger_case: "Subunternehmerflow 02 v14 → v15 — Fail-Branch-Differenzierung (Koster AG, 2026-06-19)"
---

# Power Automate — Fail-Branch-Strategie bei KI-Pipelines

Wie strukturiert man die Fail-Pfade eines Flows, der eine KI-Pipeline orchestriert (AI Builder → Parse → ggf. Splitten → Dataverse-Insert) so, dass jede Fail-Ursache einen passenden Handler bekommt und nichts stillschweigend verschwindet?

## Problem

In einem Flow mit Pipeline-Charakter (Step1 → Step2 → Step3, jeder kann failen) ist die intuitive Reaktion, alle Steps in einen **gemeinsamen Scope** zu wrappen und einen Sammel-Failure-Handler dranzuhängen:

```
Scope_Bereich:
  Run_a_prompt
  Parse_JSON
  Condition_Split:
    if length > 1: PDF_Split
  ...

runAfter Scope_Bereich [Failed, TimedOut]:
  → Sammel-Failure-Handler (z.B. Generic-Mail)
```

**Was dabei verloren geht:**

1. **Semantik der Fail-Ursache** — der Handler weiss nicht, ob `Parse_JSON` failed (= KI-Output unbrauchbar) oder `PDF_Split` failed (= KI war ok, aber Multi-Doc-Splitter streikt). Beide brauchen unterschiedliche Reaktionen und unterschiedlichen Triage-Aufwand.
2. **Differenzierte Triage-Hilfen** — z.B. bei `PDF_Split: Failed` kennen wir bereits die Anzahl erkannter Dokumente und die Page-Ranges aus dem `Parse_JSON?['result']`. Diese Info kann in der Fail-Mail / im Audit-Eintrag stehen und spart 80% Triage-Zeit. Im Sammel-Handler geht sie verloren.
3. **Drill-Down im Designer** — beim späteren Lesen muss man in den Scope reinklicken, um zu sehen, „welche Action failt, wenn der Scope failt". Klar benannte Branches sind selbst-dokumentierend.

## Lösung — Granulare Fail-Handler pro semantische Einheit

**Kernprinzip:** Pro semantische Pipeline-Stufe einen eigenen `runAfter: Failed`-Branch. Keinen Sammel-Wrapper, der die Fail-Ursache verschleiert.

```
Scope_KI:                          ← legitimer Scope: 2 Actions, gehören semantisch zusammen
  Run_a_prompt
  Parse_JSON  (runAfter Run_a_prompt: Succeeded)

Condition_Split:                   ← keine Scope, nur die Aktion selbst
  expression: length(body('Parse_JSON')?['result']) > 1
  if true: PDF_Split
  else: leer
  runAfter: Scope_KI: Succeeded

Apply_to_each:                     ← Happy Path
  foreach: body('Parse_JSON')?['result']
  runAfter: Condition_Split: Succeeded
  actions: [...]

# Fail-Handler:
Send_an_email_Parse_Fail:
  runAfter: Scope_KI: Failed       ← KI-Output unbrauchbar
  
Send_an_email_Split_Fail:
  runAfter: Condition_Split: Failed ← PDF4me konnte nicht splitten
  body: kann "@length(body('Parse_JSON')?['result'])" + "@body('Parse_JSON')?['Seite_von_bis_concat']" verwenden
```

### Wann ein Scope sinnvoll ist — wann nicht

- **Sinnvoll:** Mehrere Actions, die als **Einheit** gemeinsam fehlschlagen sollen (z.B. `Run_a_prompt` + `Parse_JSON` als „KI-Pipeline"). Der Scope hat Mehrwert: ein einziger Fail-Trigger für die gesamte Sub-Pipeline.
- **Nicht sinnvoll:** Eine einzelne Action in einen Scope wrappen. Das ist Indirection ohne Mehrwert. Die `runAfter`-Bedingung lässt sich direkt auf die Action setzen.

### Apply_to_each schützen vor `Condition Failed`

`Apply_to_each` braucht `body('Parse_JSON')?['result']` — wenn die KI-Pipeline failt, ist dieser Wert null und das ForEach kann nicht sinnvoll iterieren. Lösung: `Apply_to_each runAfter: Condition_Split: Succeeded`.

Trick mit der `Condition` als Gate: Wenn `Condition_Split` den Else-Branch nimmt (Single-Doc, length = 1, keine inneren Actions), gilt sie als **Succeeded** → ForEach läuft normal. Wenn `PDF_Split` innen failt, propagiert das → `Condition_Split: Failed` → ForEach läuft **nicht** (genau richtig, weil ohne Split-Files keine einzelnen Sub-Docs in SP).

## Status-Code-Strategie — Manuell-Queue vs Audit-only-Bucket

Wenn das Optionset `ks_eq_status` mehrere „nicht-erfolgreich"-Werte hat (z.B. „Manuell", „Fehlgeschlagen"), lohnt es sich, **eine semantische Trennung** zu etablieren statt beide synonym zu verwenden:

| Status | Semantik | App-Sichtbarkeit |
|---|---|---|
| **„Manuell"** | KI/Flow hat es nicht eindeutig zugewiesen, **Mensch entscheidet in der App** | App-Manuell-Queue (Filter darauf) |
| **„Fehlgeschlagen"** | Technischer Pipeline-Fehler, **Mensch arbeitet aus der Mail heraus** | Keine View (toter Bucket, nur Audit) |

Diese Trennung erlaubt:
- **Mail-zentrierter Triage-Workflow** für Pipeline-Fails (Parse_JSON / PDF_Split): Mail kommt → MA macht händisches Triage / Splitting → MA schickt zurück an Inbox → Flow läuft neu durch. Der „Fehlgeschlagen"-Eintrag in der Tabelle ist nur Audit-Spur, kein operatives Element.
- **App-zentrierter Triage-Workflow** für Logik-Fails (KI hat Sub-Name + Doku-Typ erkannt, aber kein Match in Dataverse): Eintrag landet in der Manuell-Queue, MA klickt sich durch.

**Voraussetzung:** Die Manuell-Queue-Views in der App **dürfen nicht** auf alle „nicht-Verarbeitet"-Status filtern, sondern explizit auf den „Manuell"-Wert. Sonst landet der „Fehlgeschlagen"-Audit-Eintrag mit unvollständigen Feldern (kein Pfad, kein Doku-Typ, etc.) in der App und stört die UX.

### Wenn man einen „toten Bucket" bewusst nutzt

Vor dem Setzen eines Status-Wertes prüfen, ob ihn irgendetwas anderes liest:

```bash
# In allen Workflows der Solution greppen:
grep -rn "eq '<status-wert>'" Workflows/
grep -rn "ks_eq_status.*<status-wert>" Workflows/
```

Wird er nirgendwo gelesen, ist er funktional inert — das ist eine **Feature**, kein Bug, wenn man ihn als Audit-Marker nutzen will. Nur **bewusst** dokumentieren, dass der Wert „tot" ist, damit nicht später jemand eine View darauf baut und ungewollt Records sieht.

## Reihenfolge im Fail-Pfad — Mail vs Audit

Wenn beide gewünscht sind (Mail an Admin + Audit-Eintrag in Dataverse), zwei Reihenfolgen denkbar:

| Variante | Vorteil | Nachteil |
|---|---|---|
| **Mail → Audit** | Mail ist garantiert priorisiert, läuft als erstes | Wenn Mail (transient) failt, kein Audit-Eintrag |
| **Audit → Mail** | Audit garantiert auch bei Mail-Fail | Mail kann minimal verzögert sein (nicht relevant) |
| **Parallel** | Beide unabhängig | Doppelte Lese-Last bei Auswertung, etwas mehr Designer-Aufwand |

**Empfehlung — abhängig vom Use Case:**
- Wenn die Mail der **primäre Reaktions-Kanal** ist und der Admin-User der einzige Beobachter: **Mail → Audit** ist OK. Wenn Mail failt, fängt Power Automate's Owner-Notification das auf (über das Flow-Run-History).
- Wenn der Audit-Eintrag **operativ** wichtig ist (z.B. weil Folge-Flows oder Reports darauf zugreifen): **Audit → Mail** oder **Parallel**.

## Static Results — Test-Mock NIE in Prod aktiv lassen

`runtimeConfiguration.staticResult.staticResultOptions: "Enabled"` ist eine Designer-Funktion zum Mocken von Action-Outputs, ohne den Connector wirklich aufzurufen. Sehr nützlich zum Testen von Fail-Pfaden (z.B. PDF_Split mit Status „Failed" mocken, um den Mail-Fail-Branch zu testen).

**Falle:** Diese Konfiguration bleibt im Solution-Export drin und ist nach dem Import in der Ziel-Umgebung weiter aktiv. Resultat: Die Action wird in Prod **niemals** wirklich ausgeführt, sondern liefert immer das gemockte Ergebnis.

```json
"staticResults": {
  "PDF_-_Split_Document_20": {
    "status": "Failed",
    "error": { "code": "NotSpecified", "message": "Unknown error" }
  }
}

// und auf der Action selbst:
"runtimeConfiguration": {
  "staticResult": {
    "staticResultOptions": "Enabled",   // ← muss vor Prod-Deploy auf "Disabled"
    "name": "PDF_-_Split_Document_20"
  }
}
```

**Checkliste vor Prod-Deploy / Solution-Export:**
1. Im Designer pro Action: „Static result" → Off
2. Im exportierten JSON: `staticResults`-Block sollte leer sein und keine Action sollte `staticResultOptions: "Enabled"` haben
3. Grep-Sanity-Check:
   ```bash
   grep -rn "staticResultOptions" Workflows/
   ```
   Wenn nichts gefunden wird oder nur `"Disabled"` vorkommt → safe.

## Trigger-Case 2026-06-19 — Koster AG Subunternehmer-Flow 02

Im Flow `02 - SUB - Eingehende E-Mail verarbeiten` gab es ursprünglich eine Sammel-Mail bei `Bereich Failed` (= `Parse_JSON` OR `PDF_Split` failt) — beide Ursachen liefen in denselben Mail-Handler mit identischem Subject. Refactor:

1. `Bereich`-Scope aufgelöst, durch `Scope_KI` (Run_a_prompt + Parse_JSON) + freistehende `Condition_Split` ersetzt
2. Zwei separate Fail-Branches mit unterschiedlichen Subjects:
   - `Scope_KI: Failed` → Mail „KI-Parse fehlgeschlagen — kein strukturierter Output"
   - `Condition_Split: Failed` → Mail „PDF-Split fehlgeschlagen — Multi-Doc muss händisch gesplittet werden" (mit Page-Ranges aus `Parse_JSON?['Seite_von_bis_concat']` im Body)
3. Zusätzlich pro Fail-Branch ein Add_a_new_row in `ks_eingangsqueues` mit Status **„Fehlgeschlagen" (124080002)** als Audit-Spur (bewusst nicht „Manuell" 124080003 — der Triage läuft über die Mail, nicht über die App)

Lehre: **Heterogenität der Fail-Ursachen gehört in differenzierte Branches, nicht in einen Sammel-Handler.**

Siehe konkrete Diff-Doku: [[50.work/projekte/Koster-AG/Subunternehmer-Flow02-Fail-Branch-Refactor-2026-06-19]].

## Verwandt

- [[50.work/power-platform/ai-builder-doppel-branch-vermeiden|AI Builder — Doppel-Branch vermeiden]] — verwandte Lehre auf Branch-Ebene des Happy Path
- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline]] — Komplette Bug-Klasse aus demselben Flow
- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — strukturierte JSON-Ausgabe]] — wie man Parse_JSON robust macht
- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]] — Projekt-Hub
- [[50.work/projekte/Koster-AG/Subunternehmer-Flow02-Fail-Branch-Refactor-2026-06-19|v14 → v15 Refactor-Diff]] — konkrete Anwendung
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
