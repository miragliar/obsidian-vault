---
source: claude-import
imported: 2026-06-01
conv_uuids: [161195de-f870-4938-aa6f-d7c163be9b80, 54cad496-0587-4531-a0db-e3d4faec07d7]
tags: [r, tableone, summary-statistics, descriptive-statistics, clinical]
---

# R — Patient-Characteristic-Tabellen mit `tableone`

## Problem

In klinischen / quantitativen Hausaufgaben soll eine „Table 1" reproduziert werden — Patient Characteristics nach Treatment-Gruppe. Manuell mit `mean()`, `sd()`, `prop.table()` ist mühsam und fehleranfällig. Häufige Stolpersteine:

- Mean ± SD für stetige, n (%) für kategoriale Variablen — Mix erfordert manuelles Branching
- Stratifizierung nach Behandlungsgruppe (= Spalten in der Tabelle)
- Schiefverteilte Variablen sollen mit Median [IQR] statt Mean SD
- Komplexe Strata wie `patient_demo × round` (4 oder 6 Spalten)
- Output für Paper: nur Prozentsätze, kein Count

## Lösung

Standard: `tableone::CreateTableOne()`.

### Setup

```r
library(tableone)

# Listen definieren
vars      <- c("age", "sex", "migraine", "chronicity")
cat_vars  <- c("sex", "migraine", "chronicity")     # kategorial
```

Faustregel:

| Variable-Typ | Statistik | tableone-Parameter |
|---|---|---|
| stetig, normalverteilt | Mean ± SD | default |
| stetig, schief | Median [IQR] | `nonnormal = "varname"` |
| kategorial | n (%) | `factorVars = c(...)` |

### Einfache Tabelle (nur Gesamtspalte)

```r
tab1 <- CreateTableOne(vars = vars, factorVars = cat_vars, data = dat)
print(tab1, showAllLevels = TRUE)
```

`showAllLevels = TRUE` → zeigt **alle** Levels einer Faktor-Variable, nicht nur die Referenzkategorie.

### Stratifiziert nach Behandlungsgruppe

```r
tab1 <- CreateTableOne(vars = vars, factorVars = cat_vars,
                       strata = "group", data = dat)
print(tab1, showAllLevels = TRUE)
```

→ Spalten = Levels von `group` + Signifikanz-p-Wert (Chi² für kategorial, t-Test für stetig).

### Schiefverteilte Variable → Median [IQR]

```r
tab1.print <- print(tab1, nonnormal = "chronicity", showAllLevels = TRUE)
```

Für mehrere: `nonnormal = c("chronicity", "duration_pain")`.

### Mehrdimensionale Strata (z.B. `demographic × round`)

Wenn die Spalten der Ziel-Tabelle eine Kreuzung zweier Variablen sind:

```r
# Kombinierte Strata-Variable
dat$demo_round <- interaction(dat$patient_demo, dat$round, sep = " — ")

# Reihenfolge der Spalten festlegen
dat$demo_round <- factor(dat$demo_round, levels = c(
  "black female — Initial",
  "white male — Initial",
  "black female — Second",
  "white male — Second",
  "black female — Final",
  "white male — Final"
))

# Subset im data-Argument
tab5 <- CreateTableOne(
  vars   = "treat_rec",
  strata = "demo_round",
  data   = dat[dat$experimental_cond == "Control" & dat$trial_id == 1, ]
)

print(tab5, showAllLevels = TRUE)
```

### Output ohne Counts, nur Prozente

```r
print(tab1, showAllLevels = TRUE,
      noSpaces = TRUE,
      printToggle = FALSE,
      format = "p"          # nur Percentages, kein "n (%)"
)
```

`format`-Optionen: `"fp"` (Frequencies + Percentages, default), `"f"` (nur Counts), `"p"` (nur %), `"pf"` (% + Counts).

### Tabelle in Datei exportieren (z.B. für Word/CSV)

```r
tab_matrix <- print(tab1, quote = FALSE, noSpaces = TRUE, printToggle = FALSE)
write.csv(tab_matrix, "table1.csv")
```

Oder direkt mit `knitr::kable()` ins R Markdown:

```r
knitr::kable(tab_matrix, format = "pipe")
```

→ funktioniert in Quarto, R Markdown, und auch in Obsidian-Markdown.

### Datentypen-Check (Bonus-Aufgabe im Kurs)

```r
class(tab1)        # "TableOne" (S3-Objekt)
class(tab1.print)  # "matrix" (character matrix)
?print.TableOne    # Hilfe zur Print-Methode (mit allen Argumenten)
```

### Häufige Fehler

| Symptom | Ursache | Fix |
|---|---|---|
| Mean wird für kategoriale Variable berechnet | Variable nicht in `factorVars` | Variable hinzufügen |
| Strata-Spalten in falscher Reihenfolge | Faktor-Levels alphabetisch | `factor(x, levels = c(...))` explizit |
| Spalten fehlen nach Subset | `droplevels()` nicht angewendet | `dat$strata <- droplevels(dat$strata)` |
| `chronicity` als Faktor, aber Median gewünscht | `factorVars` enthält die Variable | Aus `factorVars` raus, nur in `nonnormal` aufnehmen |
| p-Wert macht keinen Sinn | tableone berechnet Default-Tests, die evtl. unpassend sind | `print(tab1, test = FALSE)` zum Ausschalten oder `exact = "varname"` für Fisher's Exact |

## Wann nicht

- **Bei sehr individuellen Tabellen-Layouts** (z.B. publication-ready mit verschachtelten Headers): `gtsummary` ist mächtiger und Quarto-ready. `tableone` ist Quick-and-Dirty-Tool für Kurs/Exploration.
- **Bei nur einer Variable:** `summary()` reicht.
- **Wenn das Ziel ein LaTeX-Table für ein Paper ist:** `xtable` oder `stargazer` direkt zum LaTeX-Compile, nicht erst durch tableone.
- **Bei Regressionsergebnissen** (nicht Patient-Characteristics): `broom::tidy(model)` + `gtsummary::tbl_regression()` — andere Welt.

## Verwandt

- [[20.studies/r-statistik/datensatz-einlesen-bereinigen-uzh]]
- [[20.studies/r-statistik/plots-base-r-ggplot2]]
- [[20.studies/r-statistik/_conversation-index]]
