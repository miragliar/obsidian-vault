---
source: claude-import
imported: 2026-06-01
conv_uuids: [2a3604c1-b39e-4936-b083-33cbf2e5bd33, de41dbbc-78f9-4ab9-9ad6-635335121aea]
tags: [power-automate, string, expression, substring, float, locale]
---

# Power Automate — String-Expressions & Locale-Fallen

## Problem

Power Automate Workflow-Expressions sind nicht intuitiv: keine IDE-Autocomplete für die Innereien, schlechte Fehlermeldungen, Klammern-Hölle. Wiederkehrende Aufgaben — letzte n Zeichen extrahieren, Substring **nach** einem Marker, Komma vs. Punkt bei Zahlen, Pfad ohne Präfix — kosten jedes Mal Suche.

Häufige Stolpersteine:

- Falsch verschachtelte Klammern in `substring(length(sub(...)))`
- `float()` schlägt fehl, weil der String `"22,8"` statt `"22.8"` enthält
- `replace()` löscht versehentlich mehr als gewollt
- `indexOf` liefert `-1` wenn der Marker fehlt — und das wird unbemerkt als Substring-Start verwendet

## Lösung

### Letzte n Zeichen eines Strings

```
substring(<text>, sub(length(<text>), <n>), <n>)
```

Beispiel — letzte 2 Zeichen aus `farbe_einfassung` einer For-each-Item:

```
substring(
  items('For_each_-_Position')?['farbe_einfassung'],
  sub(length(items('For_each_-_Position')?['farbe_einfassung']), 2),
  2
)
```

**Klammer-Falle:** Es muss `sub(length(x), 2)` heißen — die `2` ist Argument **von `sub`**, nicht von `length`. Häufiger Fehler: `sub(length(x)), 2)` — eine `)` zu früh.

### Substring **nach** einem Marker (z.B. nach `"P "`)

```
substring(<text>, add(indexOf(<text>, 'P '), 2))
```

`indexOf` liefert die Position, `add(..., 2)` springt 2 Zeichen weiter (überspringt das `"P "` selbst), `substring` ohne drittes Argument nimmt alles **bis zum Ende**.

**Edge Case:** Wenn `'P '` nicht im Text vorkommt, gibt `indexOf` **-1** zurück, und `add(-1, 2) = 1` → der Substring startet bei Position 1, was unsinnig ist und keinen Fehler wirft (silent bug). **Defensive Variante:**

```
if(
  greaterOrEquals(indexOf(<text>, 'P '), 0),
  substring(<text>, add(indexOf(<text>, 'P '), 2)),
  <text>   // Fallback: ganzer Text
)
```

### Float-Parsing mit Komma statt Punkt

Wenn ein AI-Builder-Output `"Resultat": "22,8"` liefert (deutsche Locale), schlägt `float()` fehl. Fix:

```
mul(
  1.01,
  float(replace(<value>, ',', '.'))
)
```

Generell: vor jedem `float()`/`decimal()` ein `replace(x, ',', '.')` einbauen, **wenn** der String aus deutsch-lokalisierten Quellen kommt (AI Builder Prompts mit deutschem Format-Wunsch, Excel-Zellen mit Komma-Separator, deutsche User-Inputs).

**Achtung:** Niemals `replace` blind anwenden, wenn das Komma echte Bedeutung hat (z.B. Listen-Separator). Erst sicher sein, dass der String nur **eine** Zahl ist.

### Multiplikation, Division etc.

```
mul(5, 3)           // Multiplikation
div(10, 2)          // Division (Float-Result)
add(1, 2)
sub(10, 3)
mod(10, 3)          // Modulo
```

Mit Variablen:

```
mul(variables('Zahl1'), variables('Zahl2'))
```

### Pfad ohne Präfix extrahieren

Aus `'Freigegebene Dokumente/Projekt/Datei.pdf'` nur `'Projekt/Datei.pdf'` extrahieren:

```
substring(
  outputs('Neuer_Ordner_...')?['body/{FullPath}'],
  add(indexOf(outputs('Neuer_Ordner_...')?['body/{FullPath}'], 'Freigegebene Dokumente/'), 23)
)
```

(23 = `length('Freigegebene Dokumente/')` — exakt zählen, kein „ungefähr".)

Sauberer mit `split`:

```
join(skip(split(outputs(...)?['body/{FullPath}'], '/'), 1), '/')
```

→ splitten, ersten Pfad-Teil wegwerfen, Rest wieder zusammenfügen. Robuster wenn der Präfix variiert.

### Häufig benötigte Funktionen (Cheat-Sheet)

| Aufgabe | Expression |
|---|---|
| Länge | `length(x)` |
| Erste n Zeichen | `substring(x, 0, n)` |
| Letzte n Zeichen | `substring(x, sub(length(x), n), n)` |
| Position eines Substrings | `indexOf(x, 'marker')` (−1 wenn nicht) |
| Substring ab Position | `substring(x, pos)` |
| String enthält? | `contains(x, 'sub')` (Boolean) |
| Beginnt mit? | `startsWith(x, 'prefix')` |
| Trimmen | `trim(x)` |
| Klein/Groß | `toLower(x)` / `toUpper(x)` |
| Splitten | `split(x, ',')` → Array |
| Joinen | `join(array, ',')` |
| Ersetzen | `replace(x, 'old', 'new')` |
| Konkatenation | `concat(a, b, c)` oder String-Format mit `formatNumber()` |

### Defensive Patterns

- **`coalesce(x, '')`** wrappen, wenn Quelle `null` sein kann
- **Length-Check vor Substring**: `if(greater(length(x), n), substring(x, n), '')`
- **Pre-trim**: AI-Builder-Outputs und Mail-Bodies haben oft leading/trailing whitespace
- **Test mit Leer-String**: viele String-Funktionen verhalten sich bei `""` schweigend falsch

## Wann nicht

- **Bei komplexen Transformationen:** Lieber JSON parsen + `select`-Action mit Mapping, statt 5-fach verschachtelte `substring`/`indexOf`. Übersichtlicher, debuggbarer.
- **Bei wiederholten Operationen:** Wenn dieselbe String-Logik in 3+ Aktionen vorkommt — in eine Variable extrahieren oder in einen Child-Flow auslagern.
- **Wenn die Logik in PowerFx (App-Side) gehört:** String-Manipulation auf der App-Seite ist meist lesbarer (`Text()`, `Left()`, `Right()`, `Mid()` mit normaler Syntax). Nur dort verschieben, was wirklich Server-seitig laufen muss.
- **Bei Mathe statt String:** Wenn der Use Case eigentlich numerisch ist (z.B. „Verspätung berechnen") — nicht String-substring, sondern direkt rechnen.

## Verwandt

- [[50.work/power-platform/ai-prompt-json-output]] — die Quelle vieler Komma-vs-Punkt-Probleme
- [[50.work/power-platform/power-automate-invalidopenapiflow]]
- [[50.work/power-platform/_conversation-index]]
