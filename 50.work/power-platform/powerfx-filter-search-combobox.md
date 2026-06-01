---
source: claude-import
imported: 2026-06-01
conv_uuids: [46548c10-c314-4be6-ba48-5743f4f4c181, 2a3604c1-b39e-4936-b083-33cbf2e5bd33]
tags: [power-fx, power-apps, filter, search, combobox, lookup, dataverse]
---

# PowerFx — Filter + Search + Combobox kombinieren

## Problem

Eine Galerie soll mehrere Filter gleichzeitig anwenden:

- **Combobox** mit Mehrfachauswahl (z.B. mehrere Baustellen-Lookups)
- **TextInput** für Volltextsuche über mehrere Spalten
- **Statisches Filter-Kriterium** (z.B. nur „Archivierte" zeigen)

Naive Versuche scheitern, weil:

- `Baustellelookup.Id In ComboBox1.SelectedItems.Id` wirft Delegation-Warnungen oder rote Wellen
- `Filter` mit `||`-Verkettung von Text-Suchen wird unleserlich und nicht-delegierbar
- Wenn die Combobox **leer** ist, soll der Filter ignoriert werden (nicht: „leere Auswahl = nichts zeigen")
- Lookups verhalten sich anders als Choice-Spalten

## Lösung

**Goldstandard-Muster**: `Search()` außen, `Filter()` innen.

```powerfx
Search(
    Filter(
        Regiekopf;
        'Status (rrpt_status)' = 'Status (Regiekopf)'.Archiviert
        && (IsEmpty(ComboBox1.SelectedItems) || Baustellelookup in ComboBox1.SelectedItems)
    );
    TextInput5.Text;
    "rrpt_empfänger";
    "rrpt_kalenderwoche";
    "rrpt_plkommentar"
)
```

**Schlüssel-Insights:**

1. **Lookup-Record-Vergleich ohne `.Id`** — PowerFx kann ganze Records vergleichen, wenn beide aus derselben Quelle stammen. `Baustellelookup in ComboBox1.SelectedItems` ist sauberer und delegierbarer als `.Id in .Id`.
2. **`IsEmpty(ComboBox.SelectedItems) ||`** — der „kein Filter aktiv"-Default. Ohne diesen Guard zeigt die Galerie nichts, sobald die Combobox leer ist.
3. **`Search()` für Volltext** — nimmt **Spaltennamen als Strings** (`"rrpt_empfänger"`), nicht als Identifier. Pflicht: die **logischen Dataverse-Namen** verwenden, nicht die Anzeigenamen.
4. **`in` bei Strings = enthält-Suche** (case-insensitive). Für exakte Matches `=` verwenden.
5. **Datentyp-Konvertierung im Search** — wenn eine Spalte numerisch ist (`Kalenderwoche` als Zahl), aber per Text durchsucht wird, muss sie in der Quelle als Text-Spalte vorliegen. `Search()` kann nicht implicit casten.

### Mit ComboBox.SelectedItems als Filter-Quelle

```powerfx
// In ComboBox1.Items:
Distinct(Baustellen; 'Baustelle Bezeichnung')

// In Filter:
(IsEmpty(ComboBox1.SelectedItems) || Baustellelookup.'Baustelle Bezeichnung' in ComboBox1.SelectedItems.Value)
```

Achtung: `Distinct` liefert eine Tabelle mit einer `Value`-Spalte — daher `.Value` beim Vergleich.

### Mehrfacher Statusfilter (z.B. zwei Status erlauben)

```powerfx
Filter(
    Regiekopf;
    'Status (rrpt_status)' in [
        'Status (Regiekopf)'.Eröffnet;
        'Status (Regiekopf)'.'In Bearbeitung'
    ]
)
```

`in [...]` bei Choice-Spalten ist sauber und delegierbar (Dataverse).

### CountIf für ThisItem-Relationen (Galerie-Footer)

Beim Zählen verwandter Records — z.B. „wie viele Materialzeilen zu diesem Regiekopf?":

```powerfx
// FALSCH (vergleicht ThisItem mit sich selbst):
CountIf(Materialzeilen; ThisItem.Regiekopf = ThisItem.Regiekopf)

// RICHTIG (über echte Lookup-ID):
CountIf(Materialzeilen; Regiekopf.Id = ThisItem.rrpt_regiekopfid)
```

Faustregel: `ThisItem` ist die **aktuelle Galerie-Zeile**, das `ThisItem.X` außerhalb des Predicates ist konstant — drinnen vergleichst du **die zu zählende Zeile** (`Regiekopf.Id`) mit dieser Konstante.

### Zeilenumbruch in Strings

Nicht `%2F` (das ist URL-encoded `/`), sondern `Char(10)`:

```powerfx
"Personenpositionen: " & CountIf(...) & Char(10) & "Materialpositionen: " & CountIf(...)
```

## Wann nicht

- **Bei >2000 Zeilen ohne Delegation:** `Search()` ist nicht für alle Datenquellen delegierbar (SharePoint: nein, Dataverse: ja). Bei großen Listen mit non-delegable Search → blau unterstrichene Warnung → ergebnislücken. Stattdessen: Filter via delegierbare `StartsWith` / `=` Operatoren, oder Server-Side Search (Dataverse Quick-Find).
- **Bei einfachem Single-Field-Filter:** Wenn nur eine ComboBox **ohne** Mehrfachauswahl und **ohne** Volltext nötig ist → `Filter(Tabelle; Feld = ComboBox.Selected.Value)` reicht, ohne den ganzen Apparat.
- **Wenn die ComboBox die Quelle = Galerie-Quelle ist:** Dann reicht ein einfacher Lookup-Vergleich (`Baustellelookup = ComboBox.Selected`), keine `in`-Logik nötig.
- **Beim Schreiben (Patch / SubmitForm):** Diese Filter-Muster sind **Lese-Patterns**. Filterbedingungen in Patch-Aufrufen hat eine andere Syntax (`LookUp` statt `Filter`).

## Verwandt

- [[50.work/power-platform/powerfx-hidden-datacard]] — Hidden Datacards & SubmitForm
- [[50.work/power-platform/dataverse-mysterious-deletes]] — wenn Filter-Logik versehentlich löscht
- [[50.work/power-platform/_conversation-index]]
