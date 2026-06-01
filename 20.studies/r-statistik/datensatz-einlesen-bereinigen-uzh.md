---
source: claude-import
imported: 2026-06-01
conv_uuids: [224f41f2-2479-488c-bbef-78dc6cb5e4f1, 54cad496-0587-4531-a0db-e3d4faec07d7, d3c6f9d4-afcd-4172-8b77-e7801b68b15d, 2711fbd1-054c-49cb-9b1e-5f23e2a4b828, 31440c08-ee97-4094-9e21-64bf097be94a]
tags: [r, datenbereinigung, factor, tidyverse, uzh, ebpi]
---

# R — Datensatz einlesen & bereinigen (UZH-Stil EBPI)

## Problem

Im Kurs „Get Ready: Introduction to Data Analysis for Empirical Research" (UZH EBPI) folgen Hausaufgaben einem wiederkehrenden Setup:

1. Excel/CSV einlesen
2. Codebook abgleichen (Variablen-Bedeutung, Missing-Codes wie `77`, `99`)
3. Variablen zu `factor` / `ordered factor` umwandeln
4. Inkonsistente Schreibweisen normalisieren (`"black female"` vs. `"Black female"`)
5. Fehler in einzelnen Zellen korrigieren (z.B. Row 991)
6. Variablen droppen, die nicht gebraucht werden
7. Subset für die eigentliche Analyse (z.B. nur Trial 1, nur Control)

Schiefgeht regelmäßig:

- Vergessene Faktor-Konvertierung → `summary()` zeigt Mean für eine ID-Variable
- Missing-Codes nicht zu `NA` → Statistik wird verfälscht
- `ordered factor` falsche Level-Reihenfolge → Plots/Modelle ordnen alphabetisch
- Levels nach Filter bleiben → leere Balken in `barplot(table(...))`

## Lösung

### Einlesen — Excel & CSV

```r
library(readxl)
library(readr)

# Excel mit spezifischem Sheet
dat <- read_excel("data_Tiktok_wage.xlsx", sheet = "Estudio Tecnologías Digitales_V")

# CSV (klassisch)
dat <- read.csv("full_data.csv", stringsAsFactors = FALSE)

# CSV (tidyverse, oft robuster bei Encoding/Locale)
dat <- read_csv("full_data.csv", locale = locale(encoding = "UTF-8"))
```

**Empfehlung:** `stringsAsFactors = FALSE` bei `read.csv` (default seit R 4.0, aber explizit besser). Du **willst** kontrollieren, welche Spalte zum Faktor wird.

### Erste Inspektion

```r
str(dat)         # Datentypen + erste Werte
summary(dat)     # Min/Max/Mean/NAs für numeric, Frequencies für factor
head(dat, 10)
dim(dat)         # Zeilen × Spalten
colSums(is.na(dat))    # NAs pro Spalte
```

### Variablen zu Faktor / Ordered Factor

```r
# Binär/Nominal
dat$gender <- factor(dat$gender, levels = c("male", "female"))

# Ordered factor mit definierter Reihenfolge
dat$timetiktok <- factor(dat$timetiktok,
  levels = c("No consumption", "<30 min", "30–60 min", "1–2 h",
             "2–3 h", "3–4 h", ">4 h"),
  ordered = TRUE
)

# Mit numerischen Codes + Labels (codebook-driven)
dat$court <- factor(dat$court,
  levels = c(1, 2, 3, 4),
  labels = c("Commission", "Committee", "Chamber", "Grand Chamber")
)
```

### Vektorisiert mehrere Spalten in Faktor verwandeln

Im Kurs explizit ohne `for`-Loop gefragt — Trick mit `mutate` + `across`:

```r
library(dplyr)

ct_vars <- grep("^ct_", names(dat), value = TRUE)

dat <- dat |>
  mutate(across(all_of(ct_vars), 
                ~ factor(.x,
                    levels = c("Never", "Rarely", "Sometimes", "Often", "Always"),
                    ordered = TRUE)))
```

Base-R-Variante:

```r
dat[ct_vars] <- lapply(dat[ct_vars], factor,
                       levels = c("Never","Rarely","Sometimes","Often","Always"),
                       ordered = TRUE)
```

### Missing-Codes zu echten NA

```r
# Einzelne Spalte
dat$age[dat$age == 77 | dat$age == 99] <- NA

# Mehrere Spalten gleichzeitig
miss_codes <- c(77, 99)
cols <- c("age", "gender", "court")
dat[cols] <- lapply(dat[cols], function(x) ifelse(x %in% miss_codes, NA, x))

# Tidyverse
dat <- dat |> mutate(across(all_of(cols), ~na_if(.x, 77)),
                     across(all_of(cols), ~na_if(.x, 99)))
```

### String-Inkonsistenzen normalisieren

```r
# Tippfehler: "black female" vs "Black female" gleichmachen
dat$patient_demo <- tolower(trimws(dat$patient_demo))

# Punktuelle Korrektur (z.B. Row 991 hat `gender = "femlae"`)
dat$gender[dat$gender == "femlae"] <- "female"
dat[991, c("abserror", "gender", "race")] <- list(0.42, "female", "Black")
```

### Variablen droppen

```r
# Mehrere Variablen mit Selektion
dat <- dat[, !(names(dat) %in% c("var1", "var2"))]

# Letzten n Spalten weg (häufig im Kurs)
dat <- dat[, 1:(ncol(dat) - 4)]

# Tidyverse
dat <- dat |> select(-var1, -var2, -starts_with("ignore_"))
```

### Subset für Analyse

```r
# Nur TikTok-Konsumenten
dat.tiktok <- dat[dat$timetiktok != "No consumption", ]
# WICHTIG: Levels die jetzt 0 Beobachtungen haben aufräumen
dat.tiktok$timetiktok <- droplevels(dat.tiktok$timetiktok)

# Tidyverse
dat.tiktok <- dat |>
  filter(timetiktok != "No consumption") |>
  mutate(timetiktok = droplevels(timetiktok))
```

**`droplevels()` ist Pflicht nach jedem Subset**, sonst tauchen leere Levels in `table()`, `barplot()`, `tableone` etc. weiter auf.

### Sparse-Wert-Check (vor Statistik)

```r
length(unique(dat$agency))       # wieviele unterschiedliche Werte?
table(dat$agency, useNA = "ifany")   # Häufigkeit + NA-Counts
```

Faustregel: < 5 unterschiedliche Werte → besser als Faktor behandeln, nicht als kontinuierlich.

### Normalitätsprüfung — Kurs-Standard

```r
hist(dat$emotresi)
qqnorm(dat$emotresi); qqline(dat$emotresi)
shapiro.test(dat$emotresi)   # statistischer Test (n < 5000)
```

Wenn nicht normal → bei Statistik `nonnormal = "varname"` an `print(tableone)`, oder Wilcoxon statt t-Test (s. [[20.studies/r-statistik/tableone-summary-tabellen]]).

## Wann nicht

- **Bei kleinem Datensatz (<50 Zeilen) ohne Codebook:** Lieber von Hand inspizieren statt automatisierte Faktor-Pipelines.
- **Wenn Codebook unklar ist:** Erst Codebook abklären (auch Default-Annahmen wie „77 = missing" sind kursspezifisch). Sonst wandelst du valide Daten zu NA.
- **Wenn das Dataset bereits sauber ist** (öffentliche bereinigte Datasets wie `iris`, `mtcars`, `palmerpenguins`): Cleaning-Pipeline ist Overhead.
- **Bei reinen Time-Series-Daten:** Andere Tools (`xts`, `tsibble`) — die Faktor-Logik hier ist Cross-Sectional-orientiert.

## Verwandt

- [[20.studies/r-statistik/plots-base-r-ggplot2]]
- [[20.studies/r-statistik/tableone-summary-tabellen]]
- [[20.studies/r-statistik/_conversation-index]]
- [[20.studies/Organizational-Economics/Hub]]
