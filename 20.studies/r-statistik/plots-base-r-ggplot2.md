---
source: claude-import
imported: 2026-06-01
conv_uuids: [224f41f2-2479-488c-bbef-78dc6cb5e4f1, d3c6f9d4-afcd-4172-8b77-e7801b68b15d, 54cad496-0587-4531-a0db-e3d4faec07d7, 7d1587b3-b3f0-4c8f-9dc1-edea08c0b0cd, 13e09a9a-47b8-431b-96bc-3b9932e7c9ea]
tags: [r, ggplot2, base-r, plots, visualization]
---

# R — Plots mit base R und ggplot2 (Kurs-Standard)

## Problem

Im UZH-Kurs werden Plots oft **doppelt verlangt**: einmal mit base R, einmal mit ggplot2 — zur Demonstration beider Welten. Häufige Fallstricke:

- `base R`-Argumente sind kurz und kryptisch (`las`, `pch`, `cex`)
- `ggplot`-Syntax ist verbose, dafür konsistent
- Color-Codings müssen pro Library anders gemacht werden
- Achsenrotation, Labels, Titel, Legenden: andere Namen pro Library
- 3D-Information (Gruppe) via Farbe einbringen ist die Standard-Aufgabe

## Lösung

### Quick-Reference: dasselbe Plot in beiden Welten

#### Histogramm

```r
# base
hist(dat$age, main = "Age distribution", xlab = "Age", col = "steelblue")

# ggplot2
library(ggplot2)
ggplot(dat, aes(x = age)) +
  geom_histogram(fill = "steelblue", bins = 30) +
  labs(title = "Age distribution", x = "Age")
```

#### Boxplot (1D nach Gruppe)

```r
# base
boxplot(age ~ gender, data = dat, col = c("#7fbf7b", "#af8dc3"),
        main = "Age by gender", ylab = "Age", las = 1)

# ggplot2
ggplot(dat, aes(x = gender, y = age, fill = gender)) +
  geom_boxplot() +
  scale_fill_manual(values = c("#7fbf7b", "#af8dc3")) +
  labs(title = "Age by gender", y = "Age") +
  theme_minimal()
```

#### Scatter mit Farb-Coding (3. Dimension)

```r
# base
plot(dat$age, dat$emotresi,
     las = 1, pch = 19,
     xlab = "Age", ylab = "Emotional Resilience",
     main = "Emotional Resilience vs Age",
     col = dat$gender)
legend("topright", legend = levels(dat$gender),
       col = 1:length(levels(dat$gender)), pch = 19)

# ggplot2
ggplot(dat, aes(x = age, y = emotresi, color = gender)) +
  geom_point(size = 2) +
  labs(title = "Emotional Resilience vs Age",
       x = "Age", y = "Emotional Resilience") +
  theme_minimal()
```

#### Stacked Barplot mit Facetten

```r
# ggplot2 (in base R deutlich umständlicher)
ggplot(dat, aes(x = year, fill = judgment)) +
  geom_bar() +
  facet_wrap(~ religion_group) +
  scale_fill_manual(values = c("Violation" = "#d7191c",
                               "No violation" = "#abd9e9")) +
  labs(x = "Year", y = "Number of cases", fill = "Outcome") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
```

#### Beeswarm (Punkte verteilt in Box) — Base R Highlight

```r
library(beeswarm)
boxplot(yeardec ~ court, data = dat,
        col = "lightgrey", outline = FALSE)
beeswarm(yeardec ~ court, data = dat,
         pch = 16, col = c("#1b9e77","#d95f02","#7570b3","#e7298a"),
         add = TRUE, cex = 0.7)
```

ggplot-Äquivalent:

```r
library(ggbeeswarm)
ggplot(dat, aes(x = court, y = yeardec, color = court)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.3) +
  geom_beeswarm(cex = 0.7) +
  theme_minimal()
```

### Base-R-Argumente Cheat-Sheet

| Argument | Bedeutung |
|---|---|
| `main` | Titel |
| `xlab`, `ylab` | Achsenbeschriftungen |
| `las = 1` | Y-Achsen-Nummern horizontal (lesbarer) |
| `pch = 19` | Solide Punkte (statt Standard-Kreis) |
| `cex = 1.2` | Punkt-/Text-Größe |
| `col = vector` | Farbe — kann Faktor sein (auto-mapping) |
| `lwd` | Linienbreite |
| `lty` | Linientyp (1=solid, 2=dashed) |
| `legend()` | Separate Funktion, nach `plot()` |
| `abline(v=…, h=…)` | Vertikale/horizontale Referenzlinien |

### ggplot2-Customization-Patterns

#### Color-Brewer-Paletten

```r
library(RColorBrewer)
scale_fill_brewer(palette = "Set2")   # qualitative
scale_color_brewer(palette = "RdBu")  # diverging
scale_fill_viridis_d()                 # für color-blind-safe
```

Oder direkt: https://colorbrewer2.org → Hex-Codes:

```r
scale_fill_manual(values = c("#7fbf7b", "#af8dc3", "#f7f7f7"))
```

#### Achsenrotation, Theme, Legende

```r
+ theme_minimal()
+ theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "bottom")
+ coord_flip()      # X- und Y-Achse tauschen
+ scale_y_continuous(labels = scales::percent)   # %-Achse
```

#### Werte auf 0 Dezimalstellen runden in Achsen-Labels

```r
+ scale_y_continuous(labels = function(x) sprintf("%.0f", x))
# oder
+ scale_y_continuous(labels = scales::label_number(accuracy = 1))
```

### Plot speichern

```r
# Base R
png("plot1.png", width = 800, height = 600, res = 100)
plot(...)
dev.off()

# ggplot
ggsave("plot2.png", plot = my_ggplot, width = 8, height = 6, dpi = 300)
ggsave("plot2.pdf", plot = my_ggplot, width = 8, height = 6)   # für LaTeX
```

### „Kein for-loop" — vektorisiert plotten

Kurs-Constraint, aber leicht erfüllt: ggplot's `facet_wrap()` macht die for-Loop-Aufgabe in einer Zeile.

```r
ggplot(dat, aes(x = age)) +
  geom_histogram() +
  facet_wrap(~ gender)
```

Statt: drei separate Plots im Loop.

## Wann nicht

- **Bei interaktiven Dashboards:** `ggplot` ist statisch. Für interaktive Plots: `plotly::ggplotly()`-Wrapper oder `shiny`.
- **Bei sehr großen Datasets (>100k Punkte):** Beide Welten werden langsam. Lösungen: `geom_hex()` statt `geom_point()`, oder Subsampling.
- **Bei 3D-Plots:** Beide ungeeignet. `plotly`, `rgl` oder besser: 3D-Information als Farbe + Facette in 2D, das ist lesbarer.
- **Bei Publication-Quality (Paper):** ggplot ist Standard, aber `cowplot` / `patchwork` für Multi-Panel, plus `ggsave(dpi=300)` für Print-Qualität.

## Verwandt

- [[20.studies/r-statistik/datensatz-einlesen-bereinigen-uzh]]
- [[20.studies/r-statistik/tableone-summary-tabellen]]
- [[20.studies/r-statistik/_conversation-index]]
