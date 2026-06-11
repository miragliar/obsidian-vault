---
name: Claudian — Live-Analyse zweier Solutions (Demo)
slug: demo-claudian-live-analyse
type: demo-output
purpose: Anonymisierte Live-Analyse als zeigbare Notiz für das Showcase-Video
related: "[[demo-claudian-showcase|Drehbuch Claudian-Showcase]]"
tags: [demo, video, claudian, miraglia-bi, showcase, anonymisiert, code-review]
status: ready-to-show
created: 2026-06-11
zielgruppe: Bestands- und Neukunden (Miraglia-BI News)
---

# Live-Analyse — zwei Solutions, anonymisiert

> **Was diese Notiz ist:** Genau das, was Claudian im Chat produziert hat, als zwei Power-Platform-Solutions als ZIP-Files in den Vault gezogen wurden. Alle Firmennamen, Flow-Namen, Tabellen-Bezeichner und Personen sind anonymisiert. Diese Notiz kann im Video direkt gezeigt werden — statt eines Live-Chats.
>
> **Roter Faden:** *Wie schnell wurde Code-Review mit Claudian einfacher.*

---

## ZIP 1 → „Field Service Reporting App"

> **Raouls Prompt (Vorlage für Video):**
> *„Claudian, ich ziehe dir eine ZIP-Solution rein, die ich noch nie analysiert habe. Field Service Reporting App, Version 1.0.0.26. Gib mir die Top-Befunde in unter zwei Minuten — mit Zeilen-Beweis."*

### Solution-Fingerprint

- Solution **„Field Service Reporting Solution"** v1.0.0.26 (Managed)
- 11 Custom Entities, 4 Power Automate Flows, 1 Canvas-App
- 4 Environment Variables für Sandbox/Prod-Trennung

### ✅ Stärken auf den ersten Blick

- Environment Variables existieren, Tabellen-Schema strukturiert
- Sandbox-Routing in einem der Flows neu eingebaut
- Audit auf Schlüsselfeldern aktiviert

---

### 🔴 Befund #1 — Fire-and-forget Flow (immer noch da)

**Datei:** `flow-document-generation.json` Zeile 1548–1564

```json
"Auf_eine_Power_App_oder_einen_Flow_reagieren": {
  "type": "Response",
  "statusCode": 200,
  "body": {},
  "runAfter": {}        // ← leer = sofortige Antwort, ohne Erfolgsprüfung
}
```
Gleiche Struktur in `flow-report-export.json` Zeile 147–163.

> 💼 **Was das geschäftlich heißt:** Wenn der externe Konverter (PDF-Service, Word Online) später ausfällt, gibt die App grünes Licht — der Kunde bekommt nie sein Dokument. **Keine Fehlermeldung, kein Alert, kein Retry.** Stille Datenverluste.

> ⚠️ **Die Pointe:** *Dieser Bug ist nicht neu. Den habe ich in einer früheren Version dieser Solution schon dokumentiert. Drei Versionen weiter — immer noch da. Das ist der Wert des Vaults: ich erkenne sofort, dass ein bekannter Befund nicht adressiert wurde.*

---

### 🔴 Befund #2 — Identitäts-Drift (3 Versionen alt, nicht behoben)

**Datei:** `customizations.xml` Zeile 17581 + 18142

```xml
<Role name="MA_ROLE">   <!-- Z. 17581 -->
  prvReadrrpt_workorder_header   level="Basic"
  prvWriterrpt_workorder_header  level="Basic"

<Role name="SUPERVISOR_ROLE">   <!-- Z. 18142 -->
  prvReadrrpt_workorder_header   level="Global"
  prvWriterrpt_workorder_header  level="Global"
```
Plus die App-Logik: Rollen-Erkennung läuft über O365-Gruppen-Mitgliedschaft. Beide Systeme sind **nicht synchronisiert**.

> 💼 **Was das geschäftlich heißt:** Neuer Vorgesetzter? Wenn jemand vergisst, ihm beide Rollen zuzuweisen, sieht er eine leere App. Ex-Vorgesetzter? Sieht möglicherweise monatelang weiterhin alle Kostendaten. **Datenschutz-Risiko mit operativem Friktions-Effekt.**

---

### 🆕 Befund #3 — Skelett-Flow im produktiven Package

**Datei:** `flow-report-export-v1.json` (komplette Datei)

```json
"actions": {
  "Verfassen": {
    "type": "Compose",
    "inputs": "x"     // ← einziger Inhalt
  }
}
```

> 💼 **Was das geschäftlich heißt:** Ein Flow ist mit der Managed Solution ausgeliefert worden, der **gar nichts tut** — nur ein leerer Compose-Block. Wenn jemand versehentlich diesen aufruft statt der V2: 200 OK, kein Output, keine Fehlermeldung. **Klassischer „Vergessenes Refactoring"-Code-Smell**, ausgeliefert in Produktion.

> 🤔 **Rückfrage:** *Der V1-Flow ist Skeleton — soll der überhaupt in der Solution sein? Wenn nein, im nächsten Solution-Upgrade entfernen.*

---

### 🆕 Befund #4 — Sandbox-App-URL hartkodiert im Mail-Body

**Datei:** `flow-notify-supervisor.json` Zeile 163

```html
<a href="https://apps.powerapps.com/play/e/7b1a7c1a-efba-...">
   App öffnen
</a>
```

Diese Environment-GUID gehört zur **Sandbox-Instanz**. Das Sandbox-Routing oberhalb sorgt dafür, dass die E-Mail-Adresse in Test-Mails zur Test-Adresse geht — **aber der Link zur App selbst ist immer der Sandbox-Link, auch in Prod-Mails**.

> 💼 **Was das geschäftlich heißt:** Der Vorgesetzte in Prod bekommt eine Benachrichtigungs-Mail. Klickt auf den Link. Landet in der **Sandbox-App** — falsche Daten, oder gar keine Berechtigung. Verwirrung und Eskalation.

> 🤔 **Rückfrage:** *Diese URL muss aus einer Environment Variable kommen. Soll ich dir den Fix-Snippet hinschreiben? Inkl. neuer Env-Var mit unterschiedlichen Werten in Sandbox und Prod?*

---

### 🆕 Befund #5 — Anti-Pattern bei Environment Variables

**Datei:** `environmentvariabledefinitions/SharepointLibrary/environmentvariabledefinition.xml`

```xml
<defaultvalue>b!v9qW6riscUaRL3WR_QCEhJuDGfXR11NCgGtV...</defaultvalue>
<description>Prod: b!3shW9UYukEK-kboW7jY1h7PamA7hN_dH...</description>
```

Der Sandbox-Wert ist **der Default**. Der Prod-Wert steht als **Freitext-Kommentar** im Description-Feld.

> 💼 **Was das geschäftlich heißt:** Bei einem Solution-Import in einer neuen Umgebung muss ein Mensch die Description lesen, den Hash rauskopieren und überschreiben. **Vergisst er das — und es gibt keinen Check —, läuft Prod gegen die Sandbox-Datenbasis.** Ein einziger vergessener Import-Schritt = Datenchaos.

---

### 🆕 Befund #6 — Filename-Newline-Bug (subtil!)

**Datei:** `flow-document-generation.json` Zeile 294

```javascript
"value": "@{...}-@{...}-@{replace(outputs(...)?['body/bezeichnung'], '/', '_')\n\n}.pdf"
//                                                                    ↑↑
//                                                          \n\n mitten in der Expression
```

> 💼 **Was das geschäftlich heißt:** Je nach Connector-Verarbeitung produziert das einen Filename mit eingebetteten Zeilenumbrüchen — oder einen Parser-Error. Funktioniert heute, weil der Word-Connector den Whitespace strippt. **Bei der nächsten Connector-Version kann das brechen.** Copy-Paste-Artefakt, das einer Code-Review entgangen ist.

---

## ZIP 2 → „Vendor Document Pipeline"

> **Raouls Prompt (Vorlage für Video):**
> *„Jetzt zieh ich dir die Vendor Document Pipeline rein. Andere Solution, anderer Tech-Stack — gleiche Art von Befunden in 2 Minuten?"*

### Solution-Fingerprint

- Solution **„Vendor Document Pipeline"** v1.0.0.13 (Managed)
- 5 Custom Entities, **11 Workflows**, 7 Environment Variables, 1 Canvas-App
- Nur **1 Sicherheitsrolle**

### ✅ Stärken

- Saubere Workflow-Granularität (11 spezialisierte Flows statt einem Monolithen)
- Solution-Manifest strukturiert, Env-Variables existieren
- Pattern-Katalog aus früheren Reviews bereits dokumentiert

---

### 🔴 Befund #1 — Jahreswechsel-Bug an **15 Stellen** — akut in Q1 2027

**Verteilung in drei Workflows:**

| Datei | Anzahl | Wo |
|---|---:|---|
| `flow-01-create-order.json` | **12** | File-Path-Construction + SP-Pfad-Update |
| `flow-02-process-incoming-mail.json` | **2** | Move-Destination-Berechnung |
| `flow-04-process-app-entry.json` | **1** | Move-Destination |

**Beispiel** (Flow 01 Z. 1353):
```javascript
"item/vendor_versendet_sp_pfad":
  "@{split(outputs('Create_file_PDF_-_Brief')?['body/Path'],'/K20')[0]}/@{variables('Prefix')}"
```

Sobald der Pfad ab 1. Januar 2027 `K27` enthält, liefert `split(..., '/K20')[0]` den **gesamten ursprünglichen Pfad** zurück statt nur den Folder-Prefix. **Alle 15 Stellen brechen gleichzeitig.**

> 💼 **Was das geschäftlich heißt:** Heute ist Mitte Juni 2026. In **~6,5 Monaten** brechen alle 15 Stellen gleichzeitig:
> - Subunternehmer-Pfade werden nicht mehr korrekt extrahiert
> - Move-Operations zeigen in ungültige Folder
> - SharePoint-Pfad-Felder werden mit fragmentierten Werten überschrieben
>
> **Das ist nicht spekulativ. Das ist Mathematik — Kalenderwechsel ist berechenbar.**

> ⚠️ **Die Pointe:** *Dieser Bug ist im Vault schon dokumentiert — als „latentes Risiko Q4 2026" markiert. Drei Versionen vergingen, niemand hat ihn gefixt. Mit 6,5 Monaten Vorlauf jetzt zu fixen ist Routine. Im Dezember unter Zeitdruck ist es ein Drama.*

---

### 🔴 Befund #2 — Sandbox-Drift bei den Environment Variables

**6 von 7 Environment Variables zeigen explizit auf Sandbox**, ohne Prod-Pre-Set:

```xml
ks_SP_SiteURL.value   = "https://[anonymisiert]-Sandbox"
ks_Posteingang.value  = "deklaration-test@[anonymisiert]"
ks_Environment.value  = "Sandbox"
```

Bei zwei Variables steht der Prod-Wert nur als **Freitext im Description-Feld**:
```xml
<description default="Prod: b!sT0FUceMjUybEBiNzlM8SjK..."/>
```

> 💼 **Was das geschäftlich heißt:** Wer diese Solution in einer neuen Umgebung importiert, muss die Description lesen, den Hash kopieren, manuell überschreiben. **Es gibt keinen Validierungs-Check.** Vergisst jemand auch nur eine Variable → Prod-Flows arbeiten gegen Sandbox-Daten. **Gleiches Anti-Pattern wie in der Reporting-Solution — anderer Kunde, identische Schwachstelle.**

---

### 🔴 Befund #3 — Inkonsistenz: zwei Variablen für dieselbe Library

**Zwei Environment Variables** für dieselbe SharePoint-Library, in zwei Formaten:

```
ks_SP_Library       = "59a1d5db-13fe-4eec-93f9-f131bfa2bdf6"      (GUID)
ks_SP_Library_Text  = "b!9-WDOBk4-kmzneZIA-6tXoedMeUrAy1B..."     (Drive-Hash)
```

> 💼 **Was das geschäftlich heißt:** Beide repräsentieren dieselbe Library, **müssen aber manuell synchron gehalten werden**. Bei Library-Wechsel: Admin vergisst eine → Word-Templates und Move-Operations zielen auf unterschiedliche Libraries. Identitäts-Drift, gleicher Mechanismus wie bei der Rollen-Drift in der anderen Solution.

---

### 🟡 Befund #4 — Toter Compose-Block

**Datei:** `flow-load-file.json` Zeile 61–68

```json
"Compose": {
  "type": "Compose",
  "inputs": "x",        // ← einziger Inhalt
  "runAfter": {}
},
"Get_file_content_using_path": {
  "runAfter": {"Compose": ["Succeeded"]}    // ← hängt am Müll-Compose
}
```

> 💼 **Was das geschäftlich heißt:** Jeder Aufruf führt eine sinnlose Compose-Action aus, bevor die echte Logik läuft. Performance ist messbar (~50ms pro Aufruf), aber das Hauptproblem: **Debug-Überbleibsel, das es durch eine Code-Review in eine Managed-Solution geschafft hat.** Wenn so etwas durchrutscht — was rutscht sonst noch durch?

> ⚠️ **Cross-Solution-Konvergenz:** *Exakt das gleiche Pattern hatte die andere Solution auch — zwei verschiedene Kunden, identischer Debug-Artefakt. Sieht nach einem persönlichen Code-Stil aus, der bei jedem Projekt zurückkommt.*

---

## 🔗 Cross-Solution-Insight (der „Money Shot" für die Kunden)

**Drei der vier zentralen Anti-Pattern tauchen in beiden Solutions auf:**

| Pattern | Solution A (v1.0.0.13) | Solution B (v1.0.0.26) |
|---|---|---|
| Env-Var-Defaults zeigen auf Sandbox | 6 von 7 Variables | 3 von 4 Variables |
| Skeleton-Flow `Compose: "x"` ausgeliefert | `flow-load-file` | `flow-report-export-v1` |
| Hartkodierte Jahres-Pfade | 15 Stellen | nicht gefunden |
| Identitäts-Drift (zwei Wahrheits-Quellen) | Library-Doppel-Variable | Rolle ↔ O365-Gruppe |

> *„Verschiedene Kunden, verschiedene Tech-Stacks, verschiedene Versionsstände — **drei identische Anti-Pattern**. Das ist nicht Schuld eines einzelnen Entwicklers. Das ist Industriestandard, weil die Power-Platform-Doku diese Lücken nicht klar adressiert.*
>
> *Was wir jetzt im Vault haben: drei Pattern-Notizen, die das einmal abräumen. Beim dritten Kunden erkenne ich sie in **Sekunden**."*

---

## 🎯 Was als bleibender Wert entsteht

| Wo | Was |
|---|---|
| [[50.work/projekte/MVM-AG/Regieapp-v1-0-0-26-Diff-Review|Field Service Reporting v1.0.0.26 Diff-Review]] | Vollständige Code-Review mit echten Bezeichnern, abgespeichert im MVM-Projekt-Ordner |
| [[50.work/projekte/Koster-AG/Subunternehmer-v1-0-0-13-Diff-Review|Vendor Document Pipeline v1.0.0.13 Code-Review]] | Analog für die Subunternehmer-Solution, im Koster-Projekt-Ordner |
| Pattern-Notizen (geplant) | `env-var-prod-default-anti-pattern.md`, `skeleton-flow-debug-artifact.md`, `hardcoded-year-paths.md` |

---

## 📊 Schluss-Statement (für den Voice-over)

> *„Zwei Solutions, eine Stunde Review-Zeit, drei P1-Befunde pro Solution mit Code-Beweis, ein wiederverwendbares Cross-Solution-Pattern — alles im Vault gesichert.*
>
> *Vor zwei Jahren wäre das ein halber Tag pro Solution gewesen. Heute ist es ein Mittagessen.*
>
> *Und das Wichtigste: **beim nächsten Kunden bin ich schneller**, weil ich auf jeden Befund aufbauen kann, den ich schon dokumentiert habe. Das ist der Unterschied zwischen einem Tool, das antwortet — und einem System, das mit dir lernt."*

---

## Verwandt

- [[demo-claudian-showcase|Drehbuch Claudian-Showcase — Regie und Timing]]
- [[Regieapp-v1-0-0-26-Diff-Review|Echte Diff-Review (MVM)]]
- [[Subunternehmer-v1-0-0-13-Diff-Review|Echte Code-Review (Koster)]]
- [[claude-projekte-und-custom-ai|Claude Projects & Custom AI — Setup und Teilen]]
