---
name: Aestico v2 — JSON-Schnittstellen-Spec
slug: aestico-v2-spec
parent_project: "[[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import|Regieapp-Aestico-Domus-Import]]"
klient: MVM AG
typ: spezifikation
tags: [miraglia, mvm-ag, aestico, optiwork, domus, schnittstelle, spec, json]
status: dokumentiert
schema_version: 2
schema_stand: 2023-12-04
created: 2026-06-16
updated: 2026-06-16
quelle: /Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/MVM/Aestico/aestico_v2_doc/
---

# Aestico v2 — JSON-Schnittstellen-Spec

Technische Zusammenfassung der Aestico-Schnittstelle, aus der Optiwork-Doku extrahiert. Grundlage für die Regie-App → Domus-Rechnungsautomatisierung.

> **Originaldoku (ausserhalb Vault):** `Dropbox/Miraglia-BI/MVM/Aestico/aestico_v2_doc/`
> Enthält: `README.html`, `aestico_quote_schema_v2.json`, `schema_doc.html`, plus `Examples.zip` mit Beispiel-`.aest`-Dateien.

## Format-Eckdaten

| Eigenschaft | Wert |
|---|---|
| Format | **JSON** (UTF-8) |
| Datei-Endung | `.aest` |
| Schema | JSON Schema Draft-07 |
| Schema-Version | `2` (konstant erzwungen via `Header.Version: const 2`) |
| Schema-Datei | `aestico_quote_schema_v2.json` |
| Richtung | Aestico **exportiert** → empfangendes System (Domus) **importiert** |
| Transport | **NICHT spezifiziert** in der Doku — separat mit Turnkey / MVM-IT klären |

> Klarstellung: es ist **keine REST-API**, **kein CSV**, **kein XLSX**, **kein XML**. Reines JSON-File-Format.

## Root-Struktur

```json
{
  "Title":          "string",          // Pflicht
  "Notes":          "string|null",
  "Header":         { ... },           // Pflicht
  "Customer":       { ... } | null,
  "Owner":          { ... } | null,
  "InvoiceContact": { ... } | null,
  "Pictures":       [ ... ],           // optional
  "Entries":        [ ... ]            // Pflicht
}
```

### `Header` (Pflicht)

| Feld | Typ | Bemerkung |
|---|---|---|
| `GeneratedAt` | string ISO-8601 | `"2026-06-16T14:23:45.123+02:00"` |
| `Version` | number `const 2` | **Muss** `2` sein |
| `ClientUserAgent` | string | freier Text, z. B. `"MVM-RegieApp/PowerPlatform"` (TBC: ob Optiwork das whitelisten will) |
| `ClientVersion` | string | z. B. `"1.0.0.26"` aus Solution-Version |
| `UserEmail` | string (email) | aktueller PL |
| `GenerationOptions` | object | optional — siehe unten |

`GenerationOptions` (gemäss Schema):
- `AggregationOption` (int): `0` room-by-room, `1` summarizing, `2` workstep first, `3` workstep catalogs
- `PositionNumberingOption` (int): `0` user-set, `1` progressiv
  - Hinweis: in echten Examples kommen auch `2`, `OrderingOption`, `NeutralizeQuote` vor — Schema-Doku ist enger als echte Files. Bei Validierungs-Fehlern prüfen.

### Contact-Block (Customer / Owner / InvoiceContact)

Alle drei haben dieselbe Struktur:

```json
{
  "ContactRole":    0,
  "Title":          "Herr",
  "FirstName":      "Peter",
  "LastName":       "Marbach",
  "CompanyName":    null,
  "AddressStreet":  "Zwingli",
  "AddressNumber":  "17",
  "FloorLabel":     null,
  "PostalCode":     "8004",
  "City":           "Zürich",
  "Country":        null,
  "Homepage":       null,
  "PhoneNumber":    "...",
  "MobileNumber":   null,
  "FaxNumber":      null,
  "EmailAddress":   "...",
  "VAT":            null,
  "Bank":           null,
  "IBAN":           null,
  "Figure":         null,
  "RemarksField":   null
}
```

- **Alle Felder Pflicht im Objekt**, dürfen aber `null` sein.
- **Block selbst** darf `null` sein (kein Customer/Owner/InvoiceContact).

## Die 7 Entry-Typen

Jeder Entry hat ein Diskriminator-Feld `EntryType`. Daran lesen Empfänger den Typ ab.

### 1. `PositionEntry` — die Hauptzeile

```json
{
  "EntryType":   "PositionEntry",
  "Text":        "Maurerarbeiten",
  "Title":       "Maurerarbeiten",
  "Description": "Verputzarbeiten EG, Wand W2",
  "Subtext1":    "Pos. 1.1",
  "Subtext2":    null,
  "Unit":        "Std",
  "UnitPrice":   78.50,
  "Quantity":    6.5,
  "Value":       510.25,
  "MetaInfo":    null,
  "Pictures":    [],
  "Optional":    false
}
```

- **`Value` muss konsistent zu `Quantity * UnitPrice` sein.** Verantwortung der erzeugenden Seite.
- `Text` ist Pflicht — fallback auf `Title`, wenn `Description` leer.
- `Subtext1` / `Subtext2` — interpretationsoffen, übliche Nutzung: Positionscode.
- `Optional: true` markiert Zusatz-Optionen für den Endkunden.

### 2. `UnitaryPriceEntry` — Per-Position (Einheitspreis ohne Menge)

Wie `PositionEntry`, **aber ohne** `Quantity` und `Value`. Für Offerten, in denen die Menge erst später bekannt ist.

> Für Regie-Rapporte (= Std × Ansatz, Material × Preis) **vermutlich nicht relevant**.

### 3. `TextEntry` — reine Textzeile

```json
{ "EntryType": "TextEntry", "Text": "Allgemeine Bemerkung des PL." }
```

### 4. `SeparatorEntry` — Formatierung

```json
{ "EntryType": "SeparatorEntry", "Style": 0 }
```
- `Style: 0` → dünn, `1` → dick.

### 5. `GroupEntry` — Container (verschachtelbar)

```json
{
  "EntryType":   "GroupEntry",
  "Name":        "Regie 12345 — BS Wengi",
  "Value":       1234.50,
  "ShowTotal":   true,
  "Entries":     [ /* Position/Text/Separator/UnitaryPrice/GroupEntry */ ],
  "Pictures":    [],
  "Optional":    false
}
```

- **Max-Tiefe:** Root → Group → Group → Positionen (Tiefe 2). Reicht für Sammelrechnung.
- `Value` = Summe der inneren Entries (Verantwortung der erzeugenden Seite).
- `ShowTotal` (bool) — ob die Gruppe ihren Wert anzeigt. Historisches Pendant: `ShowTotals` (Tippfehler, in alten Clients präsent).

### 6. `QuoteConditionEntry` — Rabatt / Zuschlag

```json
{
  "EntryType":     "QuoteConditionEntry",
  "Text":          "Skonto 2%",
  "IsPercentual":  true,
  "ConditionValue": -2.0
}
```

- Negative `ConditionValue` = Rabatt, positive = Zuschlag.
- `IsPercentual: false` → flat-Wert in Franken.

### 7. `VATEntry` — MwSt

```json
{
  "EntryType":      "VATEntry",
  "Text":           "MwSt 8.1 %",
  "IsPercentual":   true,
  "ConditionValue": 8.1,
  "IsVat":          true
}
```

- **Immer dabei** in v2-Files.
- Empfänger kann ignorieren, wenn er MwSt selbst rechnet — **mit Domus klären** (offene Frage 4 im Hauptprojekt).

## Verschachtelungs-Beispiel (Sammelrechnung)

```
Root
├─ GroupEntry "Regie 12345 — BS Wengi"
│  ├─ PositionEntry  (Std Lohn — 6.5 × 78.50)
│  ├─ PositionEntry  (Material)
│  └─ PositionEntry  (Spesen)
├─ GroupEntry "Regie 12346 — BS Frohburg"
│  └─ PositionEntry  (Std Lohn — 3.0 × 78.50)
└─ VATEntry (MwSt 8.1 %)
```

Tiefe 2 reicht für Pro-Rapport-Gruppierung. Mehr Tiefe nicht garantiert vom Schema-v2-Doku unterstützt (README: *„currently v1 max nesting level 2"*, v2 nicht klargestellt).

## Field-Mapping Regie-App → Aestico (Skeleton)

| Aestico-Feld | Quelle Dataverse | Bemerkung |
|---|---|---|
| `Title` | `Regiekopf.RapportNr` + Baustelle | z. B. *„Regie 12345 — BS Wengi"* |
| `Notes` | `Regiekopf.Bemerkungen` | optional |
| `Header.GeneratedAt` | `utcNow()` ISO-8601 | Power Automate |
| `Header.Version` | konstant `2` | |
| `Header.ClientUserAgent` | konstant z. B. `"MVM-RegieApp/PowerPlatform"` | TBC mit Optiwork |
| `Header.ClientVersion` | aus Solution-Version | |
| `Header.UserEmail` | aktueller PL (Trigger-User) | |
| `Customer` | Baustellen-Empfänger / Domus-Kunde | **aus Domus-Stammdaten** — Mapping offen |
| `Owner` | MVM AG | konstant |
| `InvoiceContact` | Rechnungs-Empfänger | meist = Customer |
| `Entries[]` | Regie-Detail-Tabellen | pro Detail-Zeile ein `PositionEntry` |

## Validierung — Pflicht vor jedem Domus-Import

Python (lokal oder als separater Power-Automate-Schritt via Azure Function):

```python
import json, jsonschema
schema = json.load(open("aestico_quote_schema_v2.json"))
quote  = json.load(open("mein-test.aest"))
jsonschema.validate(quote, schema)   # wirft Exception bei Fehler
```

Alternativ: JSON-Schema-Validierung in Power Automate via Connector `Validate JSON` oder einer Compose-/Run-Script-Action.

## Offene Punkte (nicht in der Doku)

Die Aestico-Doku spezifiziert **nur das Format**. Folgende Punkte sind separat mit Turnkey/Optiwork/MVM-IT zu klären (Phase 1):

1. **Transport-Mechanismus:** Wie kommt die `.aest`-Datei zu Domus? Watch-Folder? SharePoint-Sync? T-Laufwerk? Manueller Upload-Button? → [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl]] / [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]]
2. **Customer-Mapping:** Wie identifiziert Domus den Kunden? Per `VAT` / `IBAN` / `EmailAddress` / `CompanyName`? Oder eine Domus-Kunden-Nr. in `Subtext1`/`MetaInfo`? → Turnkey
3. **Rechnung vs. Offerte:** Aestico nennt's *Quote*. Verarbeitet Domus-Rev. 28 das als **Rechnung** oder nur als **Offert-Vorlage**? → Remo / Turnkey
4. **MwSt-Behandlung:** Liest Domus den `VATEntry` oder rechnet selbst? README erlaubt beides.
5. **Rückgabe-Identifier:** Bekommt der Aufrufer nach Import einen Domus-Beleg-Identifier zurück (für Rückspiegelung in Regie-App), oder Einbahnstrasse?
6. **`ClientUserAgent` / `ClientVersion`:** muss Optiwork das whitelisten, oder darf frei `"MVM-RegieApp/1.0"` stehen?
7. **`OrderingOption` / `NeutralizeQuote`** (in Examples, nicht in Schema-v2-Doku) — welche Version ist autoritativ?

## Beispiel-Dateien (in `Examples.zip`)

| Datei | Inhalt |
|---|---|
| `non-summarizing.aest` | Quote room-by-room |
| `quote-nest-A.aest` … `quote-nest-D.aest` | Verschiedene Verschachtelungs-Varianten (+ PDF-Render zum Vergleich) |
| `quote-optA.aest` … `quote-optD.aest` | Quote mit optionalen Positionen |
| `per.aest` | UnitaryPriceEntry / Per-Position-Beispiel |
| `note.aest` | TextEntry-Beispiel |
| `picture.aest` | Position mit Bild |
| `optional.aest` | Optional-Markierung |

**Empfehlung:** vor eigener Generierung `quote-nest-A.aest` durchlesen — beste Vorlage für eine verschachtelte Sammelrechnung.

## Verwandt

- [[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import|Hauptprojekt: Regieapp → Aestico → Domus]]
- [[50.work/26_Firmen/Optiwork-AG|Optiwork AG (Aestico-Hersteller)]]
- [[50.work/26_Firmen/Turnkey|Turnkey AG (Domus-Anbieter)]]
- [[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regie-Rapport-App (Hauptprojekt-Hub)]]
