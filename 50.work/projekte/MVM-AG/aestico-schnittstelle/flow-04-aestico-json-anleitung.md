---
name: Flow 04 — Aestico-JSON Compose (Schritt-für-Schritt)
slug: flow-04-aestico-json-anleitung
parent_project: "[[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import|Regieapp-Aestico-Domus-Import]]"
spec: "[[aestico-v2-spec|Aestico v2 — JSON-Spec]]"
flow_file: "04-rrpt-RechnungsgenerierungBRZ-051064C6-6269-F111-A826-002248A05689.json"
solution_version: "1.0.0.29 (managed)"
klient: MVM AG
typ: anleitung
tags: [miraglia, mvm-ag, aestico, power-automate, regie-app, anleitung]
status: draft
created: 2026-06-16
updated: 2026-06-16
---

# Flow 04 — Aestico-JSON Compose (Schritt-für-Schritt)

Ziel: Am Ende des bestehenden Flows `04-rrpt-RechnungsgenerierungBRZ` **EINE einzige Aestico-v2-konforme JSON** erzeugen, deren `Entries`-Array **N `GroupEntry`-Blöcke** enthält — einen pro Regie-Rapport, plus ein VATEntry am Schluss. So bekommst du sowohl Einzelrechnung (= 1 GroupEntry) als auch Sammelrechnung (= N GroupEntries) aus demselben Mechanismus. Noch nicht speichern, nicht senden — nur im Run-Inspector sichten.

> **Architektur-Idee:** Eine Compose **innerhalb** `For_each_1` würde pro Iteration eine separate JSON erzeugen — falsch für Aestico, weil Aestico eine Quote-Datei mit N Gruppen erwartet, nicht N getrennte Dateien. Lösung: Array-Variable `Aestico_Entries` füllt sich pro Iteration via *„An Array-Variable anfügen"*, und **nach** dem For_each baut **eine** Compose die Root-Struktur drumherum.

> **WDL ≠ PowerFx.** Die Expressions in Power-Automate-Flows sind **Workflow Definition Language (WDL)** — englische Funktionen, **Komma** als Trenner. Die [[40.meta/schreibstil-raoul-wissenschaftlich|deutsche PowerFx-Lokalisierung]] (`;` / `;;`) gilt **nur in Canvas-Apps**, nicht hier.

## Ausgangslage — was der Flow heute schon macht

Der Flow läuft pro RegiekopfID. Diese Aktionen sind bereits drin und liefern alles, was du brauchst:

| Vorhandene Action | Output, den du nutzen kannst |
|---|---|
| `JSON_analysieren` | Array der RegiekopfIDs aus PowerApp-Trigger |
| `For_each_1` | iteriert über jede RegiekopfID |
| `Regiekopf_holen` | `body/cr19a_mvmrapportnummer` → MVM-Rapport-Nr |
| `Baustelle_holen` | `body/rrpt_bezeichnung` → Baustellen-Bezeichnung |
| `Select_-_Personen` | Array mit `{Person, Anzahl, Mo…So, Ansatz, Total, Total Stunden}` |
| `Select_-_Material` | Array mit `{Material, Menge, Materialpreis, Total Material, Einheit}` |
| Variablen `total_pers`, `total_mat`, `total_rap` | float, gerechnet im `Total_-_Berechnung`-Scope |
| Trigger-Input `text_3` | E-Mail des aufrufenden PL |

Du brauchst **keine** dieser Aktionen anzufassen. Wir hängen einfach drei neue Aktionen rein.

## Was du jetzt einbaust — 5 Aktionen

| # | Aktion | Position |
|---|---|---|
| **0** | **Variable initialisieren** — `Aestico_Entries` (Array) | **vor** `For_each_1`, am Ende des Init-Blocks |
| **1** | **Auswählen** — Personenzeilen → Aestico-`PositionEntry` | **in** `For_each_1` / Scope `Rapportpositionen_holen`, nach `Select_-_Personen` |
| **2** | **Auswählen** — Materialzeilen → Aestico-`PositionEntry` | **in** `For_each_1` / Scope `Rapportpositionen_holen`, nach `Select_-_Material` |
| **3** | **An Array-Variable anfügen** — GroupEntry für diesen Rapport | **in** `For_each_1`, **letzte Aktion** der Iteration |
| **4** | **An Array-Variable anfügen** — VATEntry (1x am Schluss) | **nach** `For_each_1` |
| **5** | **Verfassen** — finale Aestico-JSON `Aestico_JSON_Final` | **nach** `For_each_1` + Schritt 4, **vor** `Beenden` |

Datenfluss:
```
Init Aestico_Entries = []
For each Regiekopf-ID:
    ├─ Regiekopf holen, Baustelle holen, Personen+Material laden
    ├─ Select-Aestico-Personen, Select-Aestico-Material  ← Schritte 1+2
    └─ Append GroupEntry → Aestico_Entries               ← Schritt 3
Append VATEntry → Aestico_Entries                         ← Schritt 4
Compose Aestico_JSON_Final  { Entries: Aestico_Entries }  ← Schritt 5
Beenden
```

---

## Schritt 0 — Array-Variable initialisieren

**Position im Flow:** ganz am Anfang im Init-Block, **direkt nach** `Variable_initialisieren_-_Total_Rapport`, **vor** `JSON_analysieren`.

**So fügst du ein:**
1. Im Studio den Flow öffnen, runterscrollen bis zur Action `Variable_initialisieren_-_Total_Rapport`
2. Darunter auf `+` → **Aktion hinzufügen** → suche **„Variable initialisieren"**
3. Konfiguration:

| Feld | Wert |
|---|---|
| **Name** | `Aestico_Entries` |
| **Typ** | `Array` |
| **Wert** | `[]` |

4. Action umbenennen auf **`Variable_initialisieren_-_Aestico_Entries`** (für sauberen Ablauf-Namen).

---

## Schritt 1 — Neue Select-Action „Auswählen — Aestico-Positionen Personen"

**Position im Flow:** im Bereich `Rapportpositionen_holen`, **direkt nach** der bestehenden Action `Select_-_Personen`, **vor** `Materialzeile`.

**So fügst du ein:**
1. Im Studio öffne den Flow, klick in den Scope `Rapportpositionen_holen` rein
2. Zwischen `Select_-_Personen` und `Materialzeile` auf das `+` klicken → **Aktion hinzufügen**
3. Suche **„Auswählen"** (engl. *Select*) — *Data Operation → Select*
4. Action umbenennen auf: **`Select_-_Aestico_Personen`**

**Konfiguration:**

| Feld                 | Wert                                                            |
| -------------------- | --------------------------------------------------------------- |
| **Von** (`From`)     | `@outputs('Personenzeile')?['body/value']`                      |
| **Zuordnen** (`Map`) | im **Modus „Schlüssel/Wert"** (Key/Value) — siehe Tabelle unten |

**Key-Value-Zuordnung** (jede Zeile ist ein eigenes Key/Value-Paar im Map-Editor):

```
EntryType    PositionEntry
Text         @item()?['rrpt_mitarbeiter']
Title        @item()?['rrpt_mitarbeiter']
Description  @concat('Std-Total: ', string(item()?['cr19a_stundentotal']))
Subtext1     @item()?['rrpt_mitarbeiter']
Subtext2     
Unit         Std
UnitPrice    @float(formatNumber(item()?['rrpt_regieansatz'], 'N2'))
Quantity     @float(formatNumber(item()?['cr19a_stundentotal'], 'N2'))
Value        @float(formatNumber(item()?['rrpt_personentotal'], 'N2'))
MetaInfo     
Optional     @false
```

> **Hinweis:** `EntryType` und `Unit` sind als **statische Strings** einzutragen (ohne `@`). Alle anderen Werte mit `@` (= Expression). Bei `Subtext2` / `MetaInfo` lass das Wert-Feld **leer** — Aestico akzeptiert dort `null`.

---

## Schritt 2 — Neue Select-Action „Auswählen — Aestico-Positionen Material"

**Position im Flow:** **direkt nach** `Select_-_Material`, **vor** `Total_-_Berechnung`.

**So fügst du ein:**
1. Zwischen `Select_-_Material` und `Total_-_Berechnung` auf `+` → **Aktion hinzufügen**
2. Suche **„Auswählen"** → *Select*
3. Umbenennen auf: **`Select_-_Aestico_Material`**

**Konfiguration:**

| Feld         | Wert                                       |
| ------------ | ------------------------------------------ |
| **Von**      | `@outputs('Materialzeile')?['body/value']` |
| **Zuordnen** | Schlüssel/Wert-Modus — siehe Tabelle       |

**Key-Value-Zuordnung:**

```
EntryType    PositionEntry
Text         @item()?['rrpt_materialname']
Title        @item()?['rrpt_materialname']
Description  
Subtext1     
Subtext2     
Unit         @item()?['rrpt_einheit']
UnitPrice    @float(formatNumber(item()?['rrpt_einheitspreis'], 'N2'))
Quantity     @float(formatNumber(item()?['rrpt_menge'], 'N2'))
Value        @float(formatNumber(item()?['rrpt_materialtotal'], 'N2'))
MetaInfo     
Optional     @false
```

---

## Schritt 3 — Compose „Aestico-JSON-Test"

**Position im Flow:** **innerhalb `For_each_1`**, **nach** der Action `Variable_festlegen_-_total_auf_0_mat` (= als letzte Action der Iteration, direkt vor dem Ende der Schleife).

**So fügst du ein:**
1. Unter `Variable_festlegen_-_total_auf_0_mat` auf `+` → **Aktion hinzufügen**
2. Suche **„Verfassen"** (engl. *Compose*) — *Data Operation → Compose*
3. Umbenennen auf: **`Aestico_JSON_Test`**

**Konfiguration — Eingaben (Inputs):**

Klick rechts oben in der Compose-Box auf **„Ausdruck"** (oder schalt sie via „Code-Ansicht" um) und füge folgenden **JSON-Block** ein. Die `@{…}`-Ausdrücke werden von Power Automate beim Lauf evaluiert.

```json
{
  "Title": "@{concat('Regie-Rapport ', outputs('Regiekopf_holen')?['body/cr19a_mvmrapportnummer'], ' — ', outputs('Baustelle_holen')?['body/rrpt_bezeichnung'])}",
  "Notes": null,
  "Header": {
    "GeneratedAt": "@{utcNow()}",
    "Version": 2,
    "ClientUserAgent": "MVM-RegieApp/PowerPlatform",
    "ClientVersion": "1.0.0.29",
    "UserEmail": "@{triggerBody()?['text_3']}",
    "GenerationOptions": {
      "AggregationOption": 1,
      "PositionNumberingOption": 0
    }
  },
  "Customer": null,
  "Owner": {
    "ContactRole": 0,
    "Title": null,
    "FirstName": null,
    "LastName": null,
    "CompanyName": "MVM AG",
    "AddressStreet": "Kirchfeldstrasse",
    "AddressNumber": "44",
    "FloorLabel": null,
    "PostalCode": "6032",
    "City": "Emmen",
    "Country": "CH",
    "Homepage": "https://www.mvm-ag.ch",
    "PhoneNumber": null,
    "MobileNumber": null,
    "FaxNumber": null,
    "EmailAddress": null,
    "VAT": null,
    "Bank": null,
    "IBAN": null,
    "Figure": null,
    "RemarksField": null
  },
  "InvoiceContact": null,
  "Entries": [
    {
      "EntryType": "GroupEntry",
      "Name": "@{concat('Rapport ', outputs('Regiekopf_holen')?['body/cr19a_mvmrapportnummer'], ' — ', outputs('Baustelle_holen')?['body/rrpt_bezeichnung'])}",
      "ShowTotal": true,
      "Value": "@{variables('total_rap')}",
      "Entries": "@{union(body('Select_-_Aestico_Personen'), body('Select_-_Aestico_Material'))}"
    },
    {
      "EntryType": "VATEntry",
      "Text": "MwSt 8.1 %",
      "IsPercentual": true,
      "ConditionValue": 8.1,
      "IsVat": true
    }
  ]
}
```

> **`union()` statt `concat()`:** WDL hat `union(arr1, arr2)` für Array-Verkettung. `concat` funktioniert für Strings, **nicht** für Arrays. Falls du Duplikate erwartest (sollte hier nicht passieren, weil Personen ≠ Material), nutze `addProperty`/`createArray`-Tricks — für unseren Fall reicht `union` sauber.

> **Quotes um `@{variables('total_rap')}`:** Power Automate parst `@{…}` innerhalb von Quotes als String. Beim **Speichern als JSON** rendert es aber als Zahl, **wenn** die Variable vom Typ `float` ist (was sie ist — siehe Init-Block). Wenn du beim Output siehst, dass `Value` als String reinkommt, ersetze `"@{variables('total_rap')}"` durch `@variables('total_rap')` (ohne Quotes, ohne geschweifte Klammern) — dann sendet Power Automate die Variable als nativer Float.

---

## Test — wie du das jetzt sichten kannst

1. Solution importieren / Flow auf neueste Version → **Speichern**
2. Im Flow oben rechts **„Testen"** → **„Manuell"**
3. PowerApp-Trigger-Inputs simulieren:
   - **text** (RegiekopfID-Array): `[{"rrpt_regiekopfid": "<eine echte GUID aus rrpt_regiekopfs>"}]`
   - **text_1**: irgendwas (BaustelleID — wird im Flow nicht genutzt)
   - **text_2**: irgendwas (ArbeitsbeschriebID)
   - **text_3**: deine E-Mail z. B. `raoul@miraglia-bi.com`
4. **„Flow ausführen"** → warte den Lauf ab
5. Run-Detail öffnen → in **For_each_1** klicken → die Iteration aufklappen → **Aestico_JSON_Test** anklicken
6. Im Bereich **„Ausgaben"** liegt deine fertige Aestico-JSON

**Sammelrechnung testen:** im Trigger-Input `text` mehrere Objekte reingeben:
```json
[
  {"rrpt_regiekopfid": "<guid-1>"},
  {"rrpt_regiekopfid": "<guid-2>"}
]
```
Im Run-Inspector hat `For_each_1` dann zwei Iterationen — pro Iteration eine eigene `Aestico_JSON_Test`-Output. Für ein **einziges** zusammengefasstes Aestico-JSON (alle Rapporte in einem File) brauchst du den Ausbau weiter unten.

---

## Validierung — vor jedem ersten Test sinnvoll

Kopier den JSON-Output aus dem Run-Inspector in eine lokale Datei und validier gegen das Schema:

```bash
cd /Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/MVM/Aestico/aestico_v2_doc
python3 -c "
import json, jsonschema
schema = json.load(open('aestico_quote_schema_v2.json'))
quote  = json.load(open('/tmp/mein-output.aest'))
jsonschema.validate(quote, schema)
print('✓ Schema-konform')
"
```

Bei Schema-Fehlern → siehe „Häufige Stolpersteine" unten.

---

## Field-Coverage — was wir füllen, was noch fehlt

| Aestico-Feld | Quelle im Flow | Status |
|---|---|---|
| `Title` | `cr19a_mvmrapportnummer` + `rrpt_bezeichnung` | ✅ |
| `Header.GeneratedAt` | `utcNow()` | ✅ |
| `Header.Version` | konstant `2` | ✅ |
| `Header.UserEmail` | `triggerBody()?['text_3']` | ✅ |
| `Header.ClientUserAgent/Version` | hartcodiert | ✅ (TBC mit Optiwork ob Whitelisting nötig) |
| `Customer` | — | ❌ **offen** — Baustelle/Domus-Kundenstamm-Mapping fehlt |
| `Owner` | hartcodiert MVM AG | ✅ (statisch, könnte aus Env-Var kommen) |
| `InvoiceContact` | — | ❌ offen — meist = Customer |
| `Entries[].GroupEntry` | pro Iteration | ✅ |
| `Entries[].PositionEntry` Personen | `Select_-_Aestico_Personen` | ✅ |
| `Entries[].PositionEntry` Material | `Select_-_Aestico_Material` | ✅ |
| `VATEntry` | hartcodiert 8.1 % | ⚠️ MwSt-Logik mit Domus klären (siehe [[aestico-v2-spec#Offene Punkte (nicht in der Doku)|Spec offene Punkte]]) |

---

## Erweiterung Phase 2 — Sammelrechnung als EINE JSON

Wenn du später aus mehreren Regie-Rapporten **eine einzige** Aestico-JSON willst, statt N getrennten:

### Vorbereitung
1. **Neue Variable initialisieren** „**`Aestico_Entries`**" als **Array** — ans Ende des Init-Blocks am Flow-Anfang, **nach** `Variable_initialisieren_-_Total_Rapport`, **vor** `JSON_analysieren`:
   ```
   Name:  Aestico_Entries
   Typ:   Array
   Wert:  []
   ```

### Im For_each_1
2. Statt `Aestico_JSON_Test` als Compose → **Aktion „An Array-Variable anfügen"** (`Append to array variable`):
   - **Name:** `Aestico_Entries`
   - **Wert:** das `GroupEntry`-Objekt (= der innere `GroupEntry`-Block aus Schritt 3, ohne das umgebende Root-Objekt)

### Nach For_each_1, vor `Beenden`
3. **Verfassen** „**`Aestico_JSON_Final`**" mit der Root-Struktur — `Entries` ist jetzt `@variables('Aestico_Entries')` plus angehängter `VATEntry`:

```json
{
  "Title": "Sammelrechnung Regie",
  "Header": { … wie oben … },
  "Customer": null,
  "Owner": { … wie oben … },
  "InvoiceContact": null,
  "Entries": "@{union(variables('Aestico_Entries'), createArray(json('{\"EntryType\":\"VATEntry\",\"Text\":\"MwSt 8.1 %\",\"IsPercentual\":true,\"ConditionValue\":8.1,\"IsVat\":true}')))}"
}
```

Diese Compose siehst du im Run-Inspector **einmal** mit dem fertigen Sammel-JSON.

---

## Häufige Stolpersteine

| Symptom | Ursache & Fix |
|---|---|
| Compose zeigt `Value` als String `"1234.5"` statt Zahl `1234.5` | Quotes um `@{variables('total_rap')}` weg. Variable ist `float`, Output dann nativer Number. |
| `union(...)` schlägt fehl mit *„cannot union null"* | `Select_-_Aestico_Personen` oder `…_Material` hat ein leeres `from`. Setze `from: @{coalesce(outputs('Personenzeile')?['body/value'], json('[]'))}`. |
| Schema-Validierung: *„'PositionEntry' is required field 'Text' missing"* | In Map vergessen — `Text` ist Pflicht in `PositionEntry`. Auf Tippfehler im Key prüfen (`Text` ≠ `text`). |
| Schema: *„additional property … not allowed"* | Du hast `MetaInfo` o. Ä. mit leerem String statt `null`. Lass den Wert komplett leer (UI rendert dann `null`). |
| Im Run-Output sehe ich **kein** `Aestico_JSON_Test` | Action liegt ausserhalb von `For_each_1`. Sie muss **innerhalb** sein, weil sie `outputs('Regiekopf_holen')` etc. referenziert (= scoped). |
| `body('Select_-_Aestico_Personen')` liefert nichts im Compose | In WDL ist's `body('…')` für `Select`-Actions, **nicht** `outputs('…')?['body/value']` wie bei List Rows. Bei Select reicht `body('Select_-_Aestico_Personen')`. |

---

## Mapping-Übersicht (für deinen Backlog)

Diese Felder kommen aktuell **nicht** in die Aestico-JSON — sind aber im Dataverse bereits da. Backlog für Phase 1:

| Datenpunkt | Dataverse | Aestico-Ziel |
|---|---|---|
| Baustellen-Adresse | `rrpt_baustelles.…Adresse?` | `Customer.AddressStreet/AddressNumber/PostalCode/City` |
| Domus-Kundennummer | TBC — vermutlich in Baustelle | `Customer.Subtext1` oder eigenes `MetaInfo`-Feld |
| Skonto / Sondertarif | TBC | `QuoteConditionEntry` |
| Kleinauftrag-Flag (`CheckKleinauftrag`) | bereits Variable im Flow | evtl. als `Notes` oder eigenes `MetaInfo` |
| ArbeitsbeschriebID (Trigger `text_2`) | aktuell nicht genutzt im Flow | evtl. `Notes` oder `Subtext2` |

---

## Verwandt

- [[aestico-v2-spec|Aestico v2 — JSON-Schnittstellen-Spec]] (Grundlage für die Feldnamen)
- [[../Regieapp-Aestico-Domus-Import|Regieapp-Aestico-Domus-Import (Projekt-Hub)]]
- [[../Regieapp-Neubau-MVM|Regie-Rapport-App (Hauptprojekt)]]
- Original-Flow-Datei: `/Users/raouleliasmiraglia/Downloads/RegieRapportProzess_1_0_0_29_managed.zip` → `Workflows/04-rrpt-RechnungsgenerierungBRZ-*.json`
- [[../../power-platform/powerfx-deutsche-lokalisierung|PowerFx-Lokalisierung]] — gilt **nicht** in Flow-WDL, nur in Canvas Apps
