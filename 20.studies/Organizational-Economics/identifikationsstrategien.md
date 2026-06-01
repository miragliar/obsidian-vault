---
source: claude-import
imported: 2026-06-01
conv_uuids: [80055c55-a7ed-4ffc-9ff6-38d082cde5ef, 9f3dbee1-87dc-42a4-8400-508bf9c435c0, 4ee2e85a-9880-4859-9bf2-a2317e9fcf84, 30e94011-16a7-4834-9509-cca4e360ec69, 26525bd0-1946-4180-b76d-662aa1d04f88]
tags: [organizational-economics, kausalinferenz, iv, did, fixed-effects, omitted-variable-bias]
---

# Identifikationsstrategien — IV, DiD, FE, RCT (Methoden-Cheatsheet)

## Problem

In OE-Klausuren (Aguiar, UZH) wird Methodenkenntnis präzise abgefragt — meist in MC-Form mit fiesen Distraktoren über die **Annahmen** der jeweiligen Strategie. Zusätzlich: Paper-Analysen (Seamans & Zhu, andere) verlangen, das Identifikationsdesign aus einer Regressionstabelle herauszulesen.

Häufige Verwechslungen:

- IV-Relevanz vs. IV-Exklusion vs. IV-Exogenität
- DiD common-trends-Annahme vs. Parallelität der Niveaus
- Fixed Effects vs. Random Effects
- Selection Bias vs. Omitted Variable Bias vs. Reverse Causality

## Lösung

### Übersicht: vier Strategien, vier Annahmen, vier Failure Modes

| Strategie | Kernidee | Schlüssel-Annahme | Failure Mode |
|---|---|---|---|
| **RCT** | Random Treatment-Zuweisung | Randomisierung sauber | Non-Compliance, Attrition |
| **IV** | Exogene Variation in X durch Instrument Z | Relevanz + Exklusion + Exogenität von Z | Schwacher Instrument, verletzte Exklusion |
| **DiD** | Vor-Nach × Treatment-Control | Common Trends (parallele Trends) | Differential Trends, Anticipation |
| **FE** | Within-Unit-Variation | Constant Unobserved Heterogeneity | Time-varying Confounders |

### RCT — Randomized Controlled Trial

**Logik:** Random Treatment-Zuweisung → Treatment- und Control-Gruppe sind ex ante identisch (in Erwartung) → Differenz im Outcome ist kausal.

**Bedingungen für saubere Identifikation:**

1. **Balance** auf beobachtbaren UND unbeobachtbaren Variablen (durch Randomisierung)
2. **Compliance** — Treated-Gruppe akzeptiert wirklich das Treatment, Control nicht
3. **No Spillover** — Treatment einer Unit beeinflusst Control-Units nicht
4. **No Attrition Bias** — Drop-outs nicht systematisch

**Failure Modes:**

- Non-Compliance → ITT (Intention-to-Treat) statt ATE
- Attrition Bias → Robustness-Checks (Lee Bounds)
- Spillover → Cluster-Randomization (Schulen, Dörfer)

### IV — Instrumental Variables

**Logik:** Endogene Variable X ist korreliert mit Error u (Omitted Variable, Reverse Causality). Finde ein Instrument Z, das X beeinflusst, aber nicht direkt das Outcome.

**Drei Bedingungen — alle drei müssen halten:**

1. **Relevanz** — cov(Z, X) ≠ 0 (testbar: First-Stage F-Stat > 10)
2. **Exklusion (Exclusion Restriction)** — Z beeinflusst Y **nur** durch X (nicht testbar, ökonomisch argumentieren)
3. **Exogenität** — cov(Z, u) = 0 (Z ist als-if random gegeben Kontrollen)

**Schwache Instrumente** (low F-Stat) → IV-Schätzer kann mehr Bias haben als OLS. Faustregel F < 10 = schwach.

**Verbreitete Distraktoren:**

- „IV löst Omitted Variable Bias automatisch" — nur wenn alle 3 Annahmen halten
- „Mehr Instrumente = besser" — nur wenn Exklusion für **alle** hält (Overidentification-Tests)
- „Z muss exogen mit Y sein" — Z muss exogen mit **u** sein, kann mit X korreliert sein

### DiD — Difference-in-Differences

**Logik:** Vergleiche Veränderung der Treatment-Gruppe (vorher → nachher) mit Veränderung der Control-Gruppe. Differenz = kausaler Effekt.

**Spezifikation:**

$$
Y_{it} = \alpha + \beta \cdot \text{Treat}_i + \gamma \cdot \text{Post}_t + \delta \cdot (\text{Treat}_i \times \text{Post}_t) + \epsilon_{it}
$$

→ δ ist der Treatment-Effekt.

**Common-Trends-Annahme:** In Abwesenheit des Treatments hätten Treatment- und Control-Gruppe **parallele** Trends. Nicht die *Niveaus*, sondern die *Trends*.

**Tests/Robustness:**

- Pre-Treatment-Trends visualisieren (Event Study, Leads + Lags)
- Placebo-Tests (fake Treatment-Datum)
- Synthetic Control als Alternative

**Verbreitete Distraktoren:**

- „DiD verlangt gleiche Niveaus vor Treatment" — Nein, nur parallele Trends
- „Wenn Trends im Plot parallel aussehen, ist es OK" — visuell ≠ statistisch (CIs!)
- „DiD funktioniert immer wenn Pre-Post-Daten da sind" — Anticipation, Spillover, differential trends können brechen

**Seamans & Zhu (Klausur-relevantes Paper):** Klassisches 2×2-DiD, oft mit log-spezifizierten Outcomes → Koeffizient β interpretieren als „treatment führt zu (e^β − 1) × 100 % Veränderung", grob ≈ β·100 % für kleine β.

### Fixed Effects

**Logik:** Demean nach Unit (oder Time) → eliminiert alle **zeitkonstanten** (oder unit-konstanten) Unobservables.

**Spezifikation:**

$$
Y_{it} = \alpha_i + \gamma_t + \beta \cdot X_{it} + \epsilon_{it}
$$

α_i = Unit-FE (z.B. Firma), γ_t = Time-FE (z.B. Jahr).

**Was FE kontrolliert:**

- ✓ Zeitkonstante unbeobachtete Heterogenität (Management-Qualität, Standort, Industrie)
- ✗ Zeitvariierende Confounder (Konjunktur, neue Konkurrenz)
- ✗ Reverse Causality

**Verbreitete Distraktoren:**

- „FE löst Endogenität" — nur eine Form (zeit­konstant unbeobachtet)
- „Random Effects = FE" — Nein. RE nimmt cov(α_i, X_it) = 0 an (oft verletzt), FE nicht.

### Omitted Variable Bias (OVB)

**Logik:** Wenn eine relevante Variable W aus dem Modell weggelassen wird, und cov(X, W) ≠ 0, dann hat der OLS-Schätzer für β einen Bias.

**Bias-Richtung (Faustformel):**

$$
\text{Bias}(\hat\beta) = \gamma \cdot \text{cov}(X, W) / \text{var}(X)
$$

wobei γ = Effekt von W auf Y im wahren Modell.

| sign(γ) | sign(cov(X, W)) | Bias |
|---|---|---|
| + | + | positiv (β überschätzt) |
| + | − | negativ (β unterschätzt) |
| − | + | negativ |
| − | − | positiv |

**Verbreitete Klausur-Fragen:**

- „Welche Richtung hat der Bias?" — beide signs multiplizieren
- „Würde Randomisierung helfen?" — Ja, weil cov(X, W) → 0 bei Randomisierung von X
- „Hilft mehr Daten?" — Nein, mehr Daten reduziert Varianz, nicht Bias

### Randomisierung und OVB — die Verbindung

Randomisierung (RCT) löst OVB, weil sie cov(X, W) = 0 erzwingt — für **jede** W, auch die unbeobachtbaren. Das ist die einzigartige Stärke des RCT.

Quasi-experimentelle Methoden (IV, DiD, FE) versuchen, **as-if-random** Variation zu finden. Aber sie schließen OVB nur für bestimmte Klassen von Confoundern aus:

- IV: nur Confounder, die nicht mit Z korrelieren
- DiD: nur Confounder, die nicht differential trend haben
- FE: nur zeitkonstante Confounder

### Selection Bias

**Logik:** Stichprobe ist nicht zufällig aus Population — Selektion in die Stichprobe ist mit Y korreliert.

**Beispiele:**

- College-Wage-Premium: nur Beschäftigte beobachtet, Wage hängt aber auch von Selection in Beschäftigung ab
- Treatment-Effect: nur Compliers im IV-Setup → LATE (Local Average Treatment Effect), nicht ATE

**Korrektur:** Heckman-Selection-Modell, Inverse Probability Weighting, sample-Reweighting.

### Selection Bias ≠ OVB ≠ Reverse Causality

Drei separate Identifikationsprobleme, oft verwechselt:

| Problem | Mechanismus | Beispiel |
|---|---|---|
| **OVB** | Confounder fehlt | Education ↔ Income, IQ fehlt |
| **Selection Bias** | Sample nicht zufällig | nur Beschäftigte beobachtet |
| **Reverse Causality** | Y → X statt X → Y | Polizei ↔ Kriminalität |

## Wann nicht

- **Bei deskriptiven Analysen:** Wenn keine Kausalaussage gewollt ist, brauchst du keine Identifikationsstrategie. Korrelation kommunizieren.
- **Bei sehr kleinen Samples:** IV/DiD-Power ist schwach. Lieber RCT-Design oder qualitative Methoden.
- **Bei reinen Vorhersage-Aufgaben:** ML/Prediction braucht keine Kausalität (Korrelation reicht für Forecasting). Verwechslung Causation vs. Correlation hier kein Problem.
- **Bei perfekter Randomisierung:** Wenn ein RCT verfügbar ist, brauchst du keine Quasi-Experimente. Das ist der Goldstandard.

## Verwandt

- [[20.studies/Organizational-Economics/plattformen-network-effects]] — Theoretische Mechanismen, die empirisch identifiziert werden
- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]]
- [[20.studies/r-statistik/tableone-summary-tabellen]] — Baseline-Balance-Tabellen in RCTs
- [[20.studies/Organizational-Economics/_conversation-index]]
