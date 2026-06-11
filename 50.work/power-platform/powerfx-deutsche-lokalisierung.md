---
name: PowerFx — Deutsche Lokalisierung (Semikolon-Syntax)
slug: powerfx-deutsche-lokalisierung
type: pattern
kategorie: power-platform
tags: [miraglia, power-apps, powerfx, lokalisierung, syntax, deutsch]
status: aktiv
created: 2026-06-11
quelle: Raoul (Konvention Miraglia-BI)
---

# PowerFx — Deutsche Lokalisierung (Semikolon-Syntax)

> **Harte Regel für alle Miraglia-Bi Power-Apps-Projekte:** Code wird in **deutscher Lokalisierung** geschrieben. Das ändert die Trennzeichen — wer das nicht weiss, baut Snippets, die im Studio Syntax-Fehler werfen.

## Die zwei Regeln

| Zweck | Englisch (en-US) | Deutsch (de-DE/de-CH) |
|---|---|---|
| Parameter-Trenner innerhalb einer Funktion | `,` (Komma) | **`;` (Semikolon)** |
| Statement-Trenner (Chain) zwischen Aktionen | `;` (Semikolon) | **`;;` (Doppelsemikolon)** |
| Dezimal-Trennzeichen in Zahlen | `.` (Punkt) | **`,` (Komma)** — wird vom Studio meist automatisch übersetzt |

**Warum:** Power Apps Studio liest die Browser/Maker-Sprache und passt die Syntax an. Wenn der Maker in deutscher Sprache arbeitet (`de-CH` / `de-DE`), kollidiert das Komma als Parameter-Trenner mit dem deutschen Dezimaltrennzeichen (1,5 als Zahl) → Microsoft löst das, indem Parameter mit `;` getrennt werden und Statement-Chains mit `;;`.

## Beispiele Side-by-Side

### Beispiel 1 — If mit drei Argumenten

```powerfx
// ❌ Englisch (wirft Fehler in deutscher Maker-Umgebung):
If(IsBlank(varVPModus), DisplayMode.Disabled, DisplayMode.Edit)

// ✅ Deutsch:
If(IsBlank(varVPModus); DisplayMode.Disabled; DisplayMode.Edit)
```

### Beispiel 2 — Set + Navigate als Chain

```powerfx
// ❌ Englisch:
Set(varVPModus, "intern"); Set(varStep, 2); Navigate(RechnungsScreen)

// ✅ Deutsch:
Set(varVPModus; "intern");; Set(varStep; 2);; Navigate(RechnungsScreen)
```

### Beispiel 3 — Patch mit Record

```powerfx
// ❌ Englisch:
Patch(Regiekopf, ThisItem, {Status: "PL", PL_Email: User().Email})

// ✅ Deutsch:
Patch(Regiekopf; ThisItem; {Status: "PL"; PL_Email: User().Email})
```

Beachte: **innerhalb eines Records `{…}`** bleibt der Trenner ein **Semikolon** (zwischen Feldern), nicht Doppel-Semikolon — Records sind kein "Statement-Chaining".

### Beispiel 4 — ForAll mit Filter und Patch

```powerfx
// ❌ Englisch:
ForAll(
    Filter(Materialzeile, Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID'),
    Patch(NeueMaterialzeile, Defaults(NeueMaterialzeile), {
        Material: Material,
        Menge: Menge
    })
)

// ✅ Deutsch:
ForAll(
    Filter(Materialzeile; Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID');
    Patch(NeueMaterialzeile; Defaults(NeueMaterialzeile); {
        Material: Material;
        Menge: Menge
    })
)
```

### Beispiel 5 — IfError + komplexe Chain

```powerfx
// ❌ Englisch:
IfError(
    Patch(Regiekopf, ThisItem, {Status: "Archiviert"});
    Notify("Archiviert", Success),
    Notify("Fehler beim Archivieren", Error)
)

// ✅ Deutsch:
IfError(
    Patch(Regiekopf; ThisItem; {Status: "Archiviert"});;
    Notify("Archiviert"; Success);
    Notify("Fehler beim Archivieren"; Error)
)
```

Beachte hier den Unterschied:
- `IfError(TryBranch; CatchBranch)` — das ist **Parameter-Trenner** → `;`
- Innerhalb des TryBranch: `Patch … ;; Notify …` — das ist **Statement-Chain** → `;;`

## Mnemonik / Eselsbrücke

> „**Komma wird Strichpunkt, Strichpunkt wird Doppelstrichpunkt.**"

Oder visuell:
- `,` → `;`
- `;` → `;;`

## Wo Englisch trotzdem erlaubt bleibt

- **Datenquellen-/Tabellen-/Feld-Namen** sind sprachunabhängig — die ändern sich nicht (`Regiekopf`, `cr57f_vpintern`).
- **Funktionsnamen** (`If`, `Patch`, `ForAll`, `Notify`) werden in der deutschen Maker-Umgebung automatisch übersetzt-angezeigt (`Wenn`, `Patch`, `ForAll`, `Benachrichtigen`), aber der gespeicherte Code in `.pa.yaml` enthält weiterhin die Original-Namen. Beim Reinkopieren akzeptiert das Studio beide.

## Konsequenzen für Code-Reviews und Snippets

- **Snippets, die ich (Claudian) liefere**, müssen die deutsche Syntax verwenden — Raoul kann sonst nicht direkt reinkopieren.
- **AI-/Web-Beispiele aus englischen Quellen** müssen vor der Übernahme konvertiert werden.
- **Schwachstellen-Reviews** (wie der bestehende Regie-App-Review) zitieren Code aus `.pa.yaml`-Dateien — dort steht der Code in der Sprache, in der er im Studio geschrieben wurde. Bei Miraglia-BI also bereits **mit `;` und `;;`**.

## Anti-Patterns

- ❌ Snippet aus US-Doku 1:1 kopieren → Syntaxfehler
- ❌ Beim Mischen von `;` und `;;` versehentlich `;;` als Parameter-Trenner schreiben → "Erwartet wurde ein Operator, Bezeichner oder Sammlungsabschluss"
- ❌ In Records `{a:1;; b:2}` schreiben → Records nehmen nur einfaches `;`

## Quick-Reference Cheatsheet

```powerfx
// Funktion mit n Parametern:
Funktion(Param1; Param2; Param3)

// Statement-Chain:
Aktion1;; Aktion2;; Aktion3

// Record:
{Feld1: Wert1; Feld2: Wert2}

// Tabelle (Liste von Records):
Table({a:1; b:2}; {a:3; b:4})

// Lookup mit Bedingung und Default:
LookUp(Tabelle; Bedingung; Spalte)  // Spalte ist Param 3, nicht Statement
```

## Verwandt

- [[50.work/power-platform/powerfx-filter-search-combobox|Filter + Search + Combobox kombinieren]]
- [[50.work/power-platform/powerfx-hidden-datacard-submitform|Hidden Datacard SubmitForm]]
- [[50.work/projekte/MVM-AG/Magazin-App-MVM|Magazin-App MVM]] — nutzt diese Konvention
- [[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regie-Rapport-App]] — nutzt diese Konvention
