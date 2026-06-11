---
name: PowerFx — Disambiguation [@…] und As-Operator (Master-Detail Patches)
slug: powerfx-disambiguation-und-as-operator
type: pattern
kategorie: power-platform
tags: [miraglia, power-apps, powerfx, dataverse, master-detail, forall, lookup, scope]
status: aktiv
created: 2026-06-11
quelle: MVM-AG Regieapp Kopierfunktion (2026-06-11)
verwandt: [powerfx-deutsche-lokalisierung]
---

# PowerFx — Disambiguation `[@…]` und `As`-Operator

> **Wann brauchst du das:** Sobald du in Power Apps mit **Dataverse Master-Detail-Beziehungen** arbeitest und Felder einer Detail-Tabelle in `ForAll` / `Filter` / `LookUp` ansprichst — sonst läufst du in den klassischen Fehler **„Ungültiger Argumenttyp (GUID). Stattdessen wird ein Table-Wert erwartet"**.

## Das zugrundeliegende Problem: Schatten-Konflikt

In Dataverse ist eine 1:N-Beziehung von `Regiekopf` → `Personenzeilen` immer **doppelt sichtbar**:

| Zugriff | Bedeutung | Typ |
|---|---|---|
| `Personenzeilen` (global) | Die Datenquelle (alle Personenzeilen aller Rapporte) | Table |
| `<Regiekopf-Record>.Personenzeilen` | Navigation-Property: alle Personenzeilen **dieses** Rapports | Table |

Sobald PowerFx in einem **Scope** ist, in dem ein Regiekopf-Record verfügbar ist (z.B. innerhalb von `Filter(Personenzeilen; …)`, wo `ThisRecord` ein Detail-Record ist und über sein Lookup-Feld `Regiekopf` einen Regiekopf-Record bringt), entsteht eine **Mehrdeutigkeit**:

```powerfx
// In diesem Filter-Body:
Filter(Personenzeilen; Regiekopf = varSource)
//     ^^^^^^^^^^^^^^
// Ist 'Personenzeilen' die globale Datenquelle?
// Oder die Navigation-Property 'Regiekopf.Personenzeilen' aus dem Scope?
```

PowerFx versucht die zweite Variante (Lookup-Feld auflösen, das intern eine GUID ist) und scheitert dann mit dem GUID/Table-Fehler.

## Lösung 1: Disambiguation-Operator `[@TableName]`

Der `[@…]`-Operator **erzwingt die globale Datenquelle**, ignoriert den lokalen Scope:

```powerfx
// ❌ Mehrdeutig — kann GUID/Table-Fehler werfen:
Patch(Personenzeilen; Defaults(Personenzeilen); { … })

// ✅ Eindeutig — referenziert die globale Tabelle:
Patch([@Personenzeilen]; Defaults([@Personenzeilen]); { … })
```

**Regel:** In jedem `ForAll`-Body, in dem du Patches/Refreshs/Filter auf eine Datenquelle machst, **immer mit `[@…]`** referenzieren, sobald die Datenquelle auch als Navigation-Property eines im Scope sichtbaren Records existieren könnte.

## Lösung 2: `As`-Operator für Iteration-Variablen

Der `As`-Operator gibt der Iteration-Variable in `ForAll` / `Filter` / `LookUp` einen **expliziten Namen** und verhindert, dass Feld-Identifier im Body mit Datenquellen-Spalten oder anderen Scope-Variablen kollidieren.

```powerfx
// ❌ Mehrdeutig — was bedeutet 'Mitarbeiter' im Body?
ForAll(varSource;
    Patch([@Personenzeilen]; Defaults([@Personenzeilen]); {
        Mitarbeiter: Mitarbeiter   // <- Schatten-Konflikt möglich
    })
)

// ✅ Eindeutig — src.Mitarbeiter ist klar auf Source-Iteration bezogen:
ForAll(varSource As src;
    Patch([@Personenzeilen]; Defaults([@Personenzeilen]); {
        Mitarbeiter: src.Mitarbeiter
    })
)
```

## Lösung 3: Navigation-Property nutzen (semantischer Master-Detail)

Statt reverse Lookup-Vergleich (`Filter(Details; Master = X)`) direkt die **Master-side Navigation-Property** verwenden — das ist sauberer, semantisch korrekt und delegierbar:

```powerfx
// ❌ Reverse-Lookup-Filter — anfällig für Scope-Konflikte:
Filter(Personenzeilen; Regiekopf = varConfirmDuplicateSource)

// ✅ Master-side Navigation-Property — semantisch eindeutig:
varConfirmDuplicateSource.Personenzeilen
```

## Vollständiges Muster: Master-Detail-Duplizieren

Genau das Pattern, das aus dem MVM-Regieapp-Kopierfunktion-Fall hervorgegangen ist:

```powerfx
// 1. Master-Record duplizieren (mit [@] und Defaults)
Set(varNewKopf;
    Patch([@Regiekopf]; Defaults([@Regiekopf]); {
        Baustellenbezeichnung: varConfirmDuplicateSource.Baustellenbezeichnung;
        // … weitere Felder
        'Status (rrpt_status)': 'Status (Regiekopf)'.Entwurf;
        Datum: Today()
    })
);;

// 2. Detail-Tabellen via Navigation-Property iterieren + Patchen
ForAll(
    varConfirmDuplicateSource.Personenzeilen As src;
    Patch([@Personenzeilen]; Defaults([@Personenzeilen]); {
        Regiekopf: varNewKopf;
        Mitarbeiter: src.Mitarbeiter;
        Mitarbeitertypen: src.Mitarbeitertypen;
        Regieansatz: src.Regieansatz;
        Mo: src.Mo; Di: src.Di; Mi: src.Mi; Do: src.Do;
        Fr: src.Fr; Sa: src.Sa; So: src.So
    })
);;
ForAll(
    varConfirmDuplicateSource.Materialzeile As src;
    Patch([@Materialzeile]; Defaults([@Materialzeile]); {
        Regiekopf: varNewKopf;
        'Material Name': src.'Material Name';
        Materialkatalog: src.Materialkatalog;
        Einheitspreis: src.Einheitspreis;
        Einheit: src.Einheit;
        Menge: src.Menge;
        Bemerkung: src.Bemerkung
    })
)
```

**Drei kombinierte Patterns in einem Block:**
1. `[@TableName]` für jede Tabellen-Referenz im Patch
2. `As src` benennt die Iteration-Variable
3. Navigation-Property (`Master.Details`) statt Reverse-Filter

## Wann brauchst du das NICHT?

- In **einfachen Galerie-Bindings** (`Items = Filter(…)`) ohne verschachteltes Scope → meistens kein Konflikt
- In **Patches ohne ForAll**, wenn die Datenquelle und der Body keine Namens-Kollision haben
- Bei **SharePoint-Listen**, weil dort keine Navigation-Properties existieren — Reverse-Filter ist dort der einzige Weg

## Häufige Fehlermeldungen, die genau auf dieses Pattern hindeuten

| Meldung | Übersetzung des Compilers |
|---|---|
| „Ungültiger Argumenttyp (GUID). Stattdessen wird ein Table-Wert erwartet." | Du hast eine Datenquelle angesprochen, die im Scope auch als Lookup-Feld existiert. Lookup ist GUID, du wolltest die Tabelle. |
| „Argumenttyp inkompatibel mit Tabelle." | Variante davon — meist hilft `[@…]`. |
| „Spalte 'X' nicht gefunden" obwohl sie existiert | Scope-Konflikt: PowerFx sucht im falschen Record-Type. `As`-Operator setzen. |

## Anti-Patterns

- ❌ `Patch(Personenzeilen; …)` ohne `[@…]`, wenn ein Regiekopf-Record im Scope sichtbar ist
- ❌ `Filter(Personenzeilen; Regiekopf.'Rapport-ID' = X.'Rapport-ID')` — funktioniert oft nicht, weil PowerFx das doppelte Hop nicht delegieren kann. Besser: `Filter(Personenzeilen; Regiekopf = X)` ODER (besser noch) `X.Personenzeilen`
- ❌ `ForAll(src; Patch(…; { Feld: Feld }))` — `Feld: Feld` ist mehrdeutig (welche Seite ist Source?). Mit `As src`: `Feld: src.Feld`

## Quick-Reference

```powerfx
// Globale Datenquelle erzwingen:
[@TableName]

// Iteration-Variable benennen:
ForAll(Quelle As item;   Patch(…; { x: item.x }))
Filter(Quelle As item;   item.Status = "Aktiv")
LookUp(Quelle As item;   item.Id = varGesucht)

// Master-Detail-Iteration:
ForAll(masterRecord.DetailTabelle As d; …)
```

## Verwandt

- [[50.work/power-platform/powerfx-deutsche-lokalisierung|PowerFx Deutsche Lokalisierung (Semikolon-Syntax)]]
- [[50.work/power-platform/powerfx-filter-search-combobox|Filter + Search + Combobox kombinieren]]
- [[50.work/power-platform/powerfx-hidden-datacard-submitform|Hidden Datacard SubmitForm]]
- [[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regie-Rapport-App MVM]] — Ursprungs-Fall (Kopierfunktion 2026-06-11)
