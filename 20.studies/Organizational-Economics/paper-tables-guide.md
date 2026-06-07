---
created: 2026-06-06
type: methods-guide
source: ME 3 Aguiar VL + Course Papers (Zhang-Zhu 2011, Reshef 2023, Luca 2016, Chevalier-Mayzlin 2006, Resnick 2006)
tags: [organizational-economics, papers, tabellen, empirie, ökonometrie, klausur-vorbereitung]
status: master
---

# Wie liest man empirische Ergebnis-Tabellen?

> **Problem:** Du öffnest ein Paper, siehst eine Tabelle mit 6 Spalten und 8 Zeilen voller Zahlen. Welche Zahl ist die "Antwort" auf die Forschungsfrage? Warum schauen 6 Spalten den gleichen Effekt an, aber mit unterschiedlichen Werten? Was bedeuten die Sternchen, die Klammern, die "log", die "IHS"-Hinweise?
>
> **Dieser Guide:** Eine systematische Anleitung mit konkreten Beispielen aus den Kurs-Papers.

---

## Roadmap

1. Anatomie einer Tabelle — der universelle Aufbau
2. Warum so viele Spalten? — Robustheits-Logik
3. Wie findet man den "richtigen" Koeffizienten?
4. Methodenspezifische Tabellen
   - 4.1 OLS / Cross-Section
   - 4.2 DiD (Difference-in-Differences) — Zhang-Zhu, Reshef
   - 4.3 Triple-Diff (DDD) — Reshef Heterogenität
   - 4.4 RDD (Regression Discontinuity) — Luca Yelp
   - 4.5 IV (Instrumental Variables)
   - 4.6 Fixed-Effects-Tabellen
   - 4.7 RCT / Field Experiment — Resnick eBay
5. Prozent vs. Prozentpunkte (häufige Verwirrung)
6. Log vs. Levels — Koeffizienten-Interpretation
7. IHS (Inverse Hyperbolic Sine) — der Reshef-Spezialfall
8. Checkliste: Wie liest du JEDE Tabelle in 5 Schritten?

---

## 1. Anatomie einer Tabelle — der universelle Aufbau

Jede ökonometrische Tabelle hat die gleiche Struktur:

```
┌────────────────────────────────────────────────────┐
│           (1)        (2)        (3)        (4)     │ ← SPALTEN = Spezifikationen (Modelle)
├────────────────────────────────────────────────────┤
│ Variable A  0.131*    0.125*    0.011                │ ← Koeffizient
│            [0.068]   [0.064]   [0.048]              │ ← Standardfehler in Klammern
│                                                    │
│ Variable B  1.717***  1.568***  1.524***            │ ← weiteres Koeffizient
│            [0.448]   [0.425]   [0.336]              │
├────────────────────────────────────────────────────┤
│ Observations 13,376   13,376    13,376              │ ← Statistik-Block am Ende
│ R²           0.11     0.11      0.09                │
│ Specification OLS     OLS       FE                  │ ← Modell-Typ
└────────────────────────────────────────────────────┘
```

### Die Elemente

| Element | Bedeutung |
|---|---|
| **Header-Zeile** (1)(2)(3)... | Jede Spalte = eine separate Regression (= eine Spezifikation) |
| **Zeile mit Variablen-Namen** | Erklärende Variable / Variable of Interest |
| **Wert (z.B. 0.131)** | Geschätzter Koeffizient — wie viel ändert sich Y, wenn X um 1 steigt? |
| **Wert in Klammern \[0.068\]** | Standardfehler — wie präzise ist der Schätzer? |
| **Sterne (\*, \*\*, \*\*\*)** | Signifikanzniveau (10%, 5%, 1%) |
| **Observations** | Anzahl der Beobachtungen (Stichprobengröße) |
| **R²** | Erklärte Varianz (selten zentral für Causal-Identifikation) |
| **Specification** | Welche Methode wurde verwendet? (OLS, FE, IV, ...) |

### Wichtig zum Vergleich: Standardfehler ≠ Standardabweichung

Im Studium hast du oft "SD" für Standardabweichung gesehen. In Regressions-Tabellen sind die Klammer-Werte aber meist **Standardfehler** (SE), nicht SDs:

- **Standardabweichung (SD):** Streuung der Daten in der Stichprobe
- **Standardfehler (SE):** Streuung des Koeffizienten-Schätzers (= "wie wackelig" ist meine Schätzung?)

**Faustregel:** Koeffizient / SE = **t-Statistik**. Wenn |t| > 1.96, ist der Effekt 5%-signifikant.

---

## 2. Warum so viele Spalten? — Die Robustheits-Logik

Du fragst dich: "Warum schauen 4 Spalten dasselbe an?" — Die Antwort: Sie schauen **nicht** genau dasselbe an, sondern variieren das Setup, um zu zeigen, dass das Ergebnis **robust** ist.

### Die typischen Variationen

**A. Schrittweises Hinzufügen von Kontrollvariablen**

| Col (1) | Col (2) | Col (3) |
|---|---|---|
| Nur Treatment | + Demographics | + Time FE |

→ Wenn der Koeffizient stabil bleibt, ist er **robust gegen Confounder**. Wenn er sich stark ändert, gibt es einen Bias.

**B. Verschiedene Outcome-Variablen**

Wie in Zhang & Zhu Table 4:
- Col 1: Total Contributions
- Col 2: Additions (new content)
- Col 3: Deletions (revisions)

→ Zeigt, ob der Effekt überall wirkt oder nur in bestimmten Aspekten.

**C. Verschiedene Spezifikations-Typen**

Wie in Zhang & Zhu Table 4 (Spalten 4–6 vs. 1–3):
- (1)(2)(3) = OLS
- (4)(5)(6) = Fixed Effects

→ Zeigt, ob das Ergebnis von der Annahme abhängt, wie man Heterogenität kontrolliert.

**D. Verschiedene Sub-Samples**

Wie in Reshef Table 2:
- Col 1: Median-binary Treatment
- Col 2: Sharp binary (exclude middle)
- Col 3: Continuous Treatment

→ Zeigt, dass das Ergebnis nicht an einer bestimmten Sample-Auswahl hängt.

**E. Verschiedene Bandbreiten (bei RDD)**

z.B. Luca Yelp:
- Col 1: ±0.1 Sterne um Cutoff
- Col 2: ±0.25 Sterne
- Col 3: ±0.5 Sterne

→ Zeigt Robustheit gegen Bandbreitenwahl.

### Wann ist Robustheit "schlecht"?

Wenn der Hauptkoeffizient bei verschiedenen Spezifikationen **stark schwankt** (z.B. von 0.5 in Col 1 zu 0.1 in Col 3) oder **das Vorzeichen wechselt**, hat das Paper ein **Identifikations-Problem**. Solche Schwächen kann man in Klausur-Diskussionen aufdecken.

---

## 3. Wie findet man den "richtigen" Koeffizienten?

> **Die Schlüsselfrage:** Was will das Paper *eigentlich* zeigen, und welche Variable misst diesen Effekt?

### Schritt-für-Schritt

**Schritt 1 — Lies die Forschungsfrage.**
- Sie steht im Abstract und in der Einleitung.
- Beispiel Zhang-Zhu: *"Wie wirkt eine Reduktion der Gruppen-Größe auf die Beiträge der verbleibenden Konsumenten?"*

**Schritt 2 — Identifiziere die zentrale Variation.**
- Was wurde künstlich variiert (oder als-if-randomly variiert)?
- Beispiel Zhang-Zhu: Der **Block** von Wikipedia in China (exogenes Schocks, das die Gruppen-Größe für nicht-blockierte Konsumenten reduzierte).

**Schritt 3 — Finde die Variable, die das misst.**
- DiD: meist `Treat × Post` oder ein Interaktions-Term
- DDD: meist `Treat × Post × Group`
- RDD: die Treatment-Indikator-Variable (über/unter dem Cutoff)
- IV: der Koeffizient auf der endogenen Variable in der zweiten Stufe
- OLS: die Policy-Variable von Interesse

**Schritt 4 — Lese den Wert in der Hauptspalte.**
- Die Hauptspalte ist meist Col (1) oder die mit den meisten Kontrollen.

**Schritt 5 — Übersetze in eine Aussage.**
- Was bedeutet `β = −1.717` ökonomisch?
- Hier hilft die Kenntnis von Methode + Funktional-Form (log? IHS? level?).

### Beispiel Zhang-Zhu Table 4

Forschungsfrage: *"Reduziert die Reduktion der Gruppen-Größe die Beiträge der verbleibenden Konsumenten?"*

Schlüsselvariable: `PercentageBlocked × AfterBlock` — die Interaktion misst, wie sehr sich Beiträge ändern, wenn mehr Kollaborateure blockiert wurden, **nach** dem Block.

In Col 1: `β = −1.717***`
→ Antwort: **Ja**, ein Anstieg um 1 in `PercentageBlocked` (was eine 100%-Verschiebung wäre) verringert die Beiträge im Schnitt um 1.717 Beiträge nach dem Block. Hoch signifikant (***).

---

## 4. Methodenspezifische Tabellen

### 4.1 OLS / Cross-Section-Tabellen

**Typisches Setup:**
```
Y_i = α + β·X_i + γ·Controls_i + ε_i
```

**Was lesen?**
- Koeffizient `β` auf `X` (die Variable von Interesse)
- Vorzeichen + Signifikanz interpretieren

**Wichtig:** Bei pure-OLS-Tabellen ist die **kausale** Interpretation oft schwierig — Confounding, Reverse Causality, Selection. Solche Tabellen kommen meist als "vorläufige Korrelationen" vor.

**Klausur-relevant:** Wenn ein Paper *nur* OLS rechnet, frage: "Was ist das Identifikations-Problem? Welche Confounder fehlen?"

---

### 4.2 DiD (Difference-in-Differences) — der häufigste Fall

**Typisches Setup:**
```
Y_it = α + β₁·Treat_i + β₂·Post_t + β₃·(Treat_i × Post_t) + ε_it
```

**Was lesen?**
- **`β₃` (die Interaktion Treat × Post)** = der DiD-Schätzer = der Treatment-Effekt
- `β₁` (Treat alone) = der pre-treatment Niveauunterschied zwischen den Gruppen (oft nicht von Interesse)
- `β₂` (Post alone) = der Trend, den auch die Control-Gruppe erlebt (nicht von Interesse)

**Konkretes Beispiel — Zhang-Zhu Table 4:**

| Variable | Col 1 (OLS) | Was bedeutet das? |
|---|---|---|
| AfterBlock | −0.131* | Verbleibende Konsumenten contribuieren ~0.131 weniger nach dem Block (Baseline-Trend) |
| **PercentageBlocked × AfterBlock** | **−1.717\*\*\*** | **← DiD-Effekt!** Pro Prozent mehr blockierte Kollaborateure: 1.717 weniger Beiträge |
| PercentageBlocked | 7.552*** | Baseline-Korrelation (Kontributoren mit blockierten Kollabs hatten *vor* dem Block höhere Beiträge — daher der positive Wert) |

→ Die **Interaktion** ist das, was zählt. Die anderen Koeffizienten sind "Bausteine", die du brauchst, um die Interaktion korrekt zu interpretieren.

### Common-Trends-Annahme (CTA) — präzise

**Die Annahme** (was DiD verlangt):
> In Abwesenheit des Treatments hätten Treatment- und Control-Gruppe **parallele counterfactual post-treatment Trends** gehabt.

→ Das ist eine **counterfactual** Annahme — sie ist per Definition **nicht direkt testbar**, weil wir die hypothetische Welt "Treated ohne Treatment in der Post-Phase" nie sehen.

**Der Test** (was man empirisch prüfen kann):
> **Parallel pre-trends** — vor dem Treatment liefen beide Gruppen parallel.

→ **Notwendige, aber nicht hinreichende** Bedingung. Suggestive Evidenz für die CTA, kein Beweis.

In Tabellen sieht man das oft als:
- **Pre-Trends-Test** (Tabellen-Zeile oder F-Test)
- **Event-Study-Plots** (Lead-Lag-Coefficients vor Treatment alle ~0)
- **Placebo-Tests** (fake Treatment-Datum, kein Effekt erwartet)

**Wenn die Pre-Trends nicht parallel sind → DiD ist verdächtig** (CTA wahrscheinlich verletzt). Aber: auch wenn Pre-Trends parallel sind, **garantiert das nicht** die Post-CTA — zusätzliche ökonomische Argumentation nötig.

### Die zwei Differenzen — woher der Name kommt

Die "Difference-in-Differences" sind:
1. **Über Zeit:** ΔT = Y_T,post − Y_T,pre und ΔC = Y_C,post − Y_C,pre
2. **Zwischen Gruppen:** DiD = ΔT − ΔC

Die kausale Story: Wir vergleichen die **actual** Treated-Trajektorie mit der **counterfactual** Treated-Trajektorie. Der Counterfactual wird gebaut als `Y_T,pre + ΔC` — wir nutzen Control's Trend als Proxy.

### Event-Study-Tabellen

Manche DiD-Papers zeigen statt einer Tabelle einen **Event-Study-Plot**:
```
β_{-3}, β_{-2}, β_{-1}, β_0, β_1, β_2, β_3
   (vor Treatment)        (nach Treatment)
```

- Pre-Treatment-Koeffizienten sollten ~0 sein (Common Trends)
- Post-Treatment-Koeffizienten = der Effekt über Zeit

Reshef Figure 3 ist genau das: Du siehst Punkte vor Week 0 (sollten ~0 sein) und nach Week 0 (sollten den Effekt zeigen).

---

### 4.3 Triple-Diff (DDD) — Heterogenitäts-Analyse

Wenn das Paper fragt: "Ist der Treatment-Effekt für Gruppe A anders als für Gruppe B?" → DDD.

**Typisches Setup:**
```
Y_it = α + β₁·Treat + β₂·Post + β₃·Group + 
       β₄·(Treat × Post) + β₅·(Treat × Group) + β₆·(Post × Group) +
       β₇·(Treat × Post × Group) + ε
```

**Was lesen?**
- **`β₄` = Treatment-Effekt für die Baseline-Gruppe** (z.B. High-Quality)
- **`β₇` = Differenz im Treatment-Effekt zwischen Gruppen** (Heterogenität)
- **`β₄ + β₇` = Treatment-Effekt für die andere Gruppe** (z.B. Low-Quality)

**Konkretes Beispiel — Reshef Table 3:**

| Variable | Col 1 (Weekly orders) | Bedeutung |
|---|---|---|
| **Treat × Post** | **0.036\*\*\*** | DiD-Effekt für **High-quality** Restaurants (Baseline-Gruppe): +3.6% mehr Bestellungen |
| **Treat × Post × Low** | **−0.062\*\*\*** | **Differenz** zwischen Low- und High-Quality: Low-Quality hat 6.2% niedrigeren Effekt |
| **β₁ + β₂** | **−0.026** | **Effekt für Low-quality** (Summe): 3.6% − 6.2% = −2.6% (Low-Quality verliert) |
| p-value | 0.001 | Test, ob β₁+β₂ signifikant von 0 verschieden |

**Take-Away:** Bei DDD-Tabellen MUSST du die Koeffizienten **addieren**, um den Effekt für die Nicht-Baseline-Gruppe zu kriegen. Das wird oft als separate Zeile (`β₁ + β₂`) berichtet.

---

### 4.4 RDD (Regression Discontinuity Design)

**Typisches Setup:**
```
Y_i = α + τ·D_i + f(X_i) + ε_i
```
- `X_i` = Running Variable (z.B. Yelp-Rating)
- `D_i = 1{X_i ≥ cutoff}` (Indikator, ob über dem Cutoff)
- `f(X_i)` = polynomiale Funktion (kontrolliert für glatte Veränderung)

**Was lesen?**
- **`τ` (der Treatment-Indikator-Koeffizient)** = der Diskontinuitäts-Effekt am Cutoff

**Konkretes Beispiel — Luca (2016) Yelp:**

Yelp rundet Ratings. Restaurant mit 3.24 Sternen → angezeigt als "3.0"; 3.25 Sterne → "3.5". Diese zwei Restaurants sind ökonomisch fast identisch, werden aber unterschiedlich angezeigt.

Tabellen-Struktur (vereinfacht):

| Variable | Col 1 (Bandwidth 0.1) | Col 2 (BW 0.25) | Col 3 (BW 0.5) |
|---|---|---|---|
| **Above Cutoff (D)** | **0.054\*\*\*** | **0.061\*\*\*** | **0.058\*\*\*** |
| | (0.012) | (0.011) | (0.010) |
| Rating (Running Variable) | 0.012 | 0.015* | 0.020** |
| Observations | 1,200 | 3,400 | 8,700 |

→ Der **Diskontinuitäts-Effekt** ist ~5-6%. Das ist robust über verschiedene Bandbreiten.

### RDD-spezifische Robustheits-Tests

- **Bandbreiten-Variation** (verschiedene Spalten)
- **Donut-Hole**: Beobachtungen direkt am Cutoff weglassen
- **McCrary-Test**: Gibt es Manipulation der Running Variable?

---

### 4.5 IV (Instrumental Variables) — 2 Tabellen

IV-Papers zeigen typischerweise **zwei Tabellen** (oder zwei Panels):

**First Stage:**
```
X_endogen = α + π·Z_instrument + Controls + ε
```
→ Zeigt, ob das Instrument relevant ist (F-Statistik > 10)

**Second Stage:**
```
Y = α + β·X̂_predicted + Controls + ε
```
→ `β` ist der kausale Schätzer

**Was lesen?**

| Tabelle | Hauptkoeffizient | Was prüfen? |
|---|---|---|
| First Stage | `π` (Instrument auf endogene Variable) | F-Stat > 10? Ist der Effekt signifikant und plausibel? |
| Second Stage | `β` (predicted endogene auf Y) | Vorzeichen, Signifikanz, plausible Größe |

**Achtung Distraktoren:**
- Wenn nur die Second Stage gezeigt wird (ohne First Stage), ist das **schlechte Praxis**
- Wenn die First-Stage-F < 10, ist das Instrument **schwach** und IV-Schätzer ist verzerrt

---

### 4.6 Fixed-Effects (FE) Tabellen

FE absorbieren zeitkonstante (oder unit-konstante) Heterogenität:

```
Y_it = α_i + γ_t + β·X_it + ε_it
```
- `α_i` = Unit-Fixed-Effect (z.B. Firmen-FE)
- `γ_t` = Time-Fixed-Effect (z.B. Jahr-FE)

**Was lesen?**
- `β` auf `X_it` — der "within-Firmen, within-Jahr"-Effekt

**Achtung:** FE eliminieren **nur zeitkonstante** Confounders. Time-varying Confounders bleiben ein Problem.

**Konkretes Beispiel — Zhang-Zhu Spalten 4–6:**

Im OLS (Cols 1–3): `PercentageBlocked` erscheint als signifikanter Baseline-Effekt.
Im FE (Cols 4–6): `PercentageBlocked` ist **dropped** (weil zeitkonstant pro Kontributor → von FE absorbiert).
Die Interaktion `PercentageBlocked × AfterBlock` bleibt aber identifiziert.

→ FE absorbiert die Niveau-Unterschiede zwischen Kontributoren; nur die zeitliche Variation ist relevant.

### Wann FE erkennt man am Tabellen-Boden:

```
Specification: FE
Firm FE: Yes
Year FE: Yes
```

→ Wenn "FE: Yes" steht, sind diese Effekte rausgerechnet.

---

### 4.7 RCT / Field Experiment — Resnick (2006) eBay

Bei sauberen Experimenten ist die Tabelle viel einfacher:

```
Y_i = α + β·Treatment_i + ε_i
```

**Was lesen?**
- `β` auf `Treatment` = der ATE (Average Treatment Effect)

**Beispiel — Resnick et al. (2006) eBay-Postcards:**

| Variable | Col 1 |
|---|---|
| **High-Reputation-Seller (Treatment)** | **+8%\*\*\*** |
| | (1.2) |

→ Postkarten von High-Reputation-Sellern erzielten 8% höhere Preise (für dasselbe Produkt). Saubere Identifikation, weil Random Assignment.

**Robustheits-Spalten bei RCTs:** meistens
- Mit/ohne Kontrollvariablen (Balance-Test-Style)
- Verschiedene Outcomes (Preis, Verkaufswahrscheinlichkeit, etc.)
- Sub-Samples (z.B. Produkt-Kategorien)

---

## 5. Prozent vs. Prozentpunkte — der häufigste Verwirrungs-Fall

### Definitionen

**Prozent (%):** Relativer Wert. "5% Anstieg von 20 = 21" (= 20 × 1.05)

**Prozentpunkt (pp):** Absoluter Wert auf einer Prozent-Skala. "5pp Anstieg von 20% = 25%"

**Faustregel:** Wenn der Bezugswert selbst eine Rate/Anteil ist, sprichst du in **Prozentpunkten**, sonst in **Prozent**.

### Beispiele

| Outcome Y | Was bedeutet "5% Effekt"? | Was bedeutet "5pp Effekt"? |
|---|---|---|
| Umsatz (CHF) | +5% (von 100 → 105) | Keine Bedeutung — Umsatz ist kein Prozent |
| Verkaufs-Wahrscheinlichkeit | Unklar — kommt drauf an | Wahrscheinlichkeit steigt absolut um 5%-Punkte (z.B. 30% → 35%) |
| Arbeitslosenrate | +5% von der Rate (z.B. 10% → 10.5%) | +5pp (10% → 15%) |
| Marktanteil | +5% (z.B. 20% → 21%) | +5pp (20% → 25%) |

### Wie erkennst du das in einer Tabelle?

**1. Schau, was Y ist:**
- Wenn `Y = Marktanteil` (also eine Zahl zwischen 0 und 1 oder 0 und 100): Koeffizient ist in **Prozentpunkten** (wenn Y in 0–100 Skala) oder als Anteilsdifferenz (wenn 0–1)
- Wenn `Y = log(Umsatz)`: Koeffizient ist in **Prozent** (Logarithmus-Trick, siehe nächste Sektion)
- Wenn `Y = Umsatz` (in $): Koeffizient ist in **absoluten $-Beträgen**

**2. Schau in die Tabellen-Notes:**
- Manche Paper schreiben explizit "coefficients should be interpreted as percent changes"
- Reshef sagt z.B.: "The dependent variables are the inverse hyperbolic sine transformation and should be interpreted as percent changes on a scale from 0 to 1"

**3. Schau ins Y-Variable-Label im Header der Tabelle:**
- "Weekly orders (log)" → Koeffizient = % Veränderung
- "Weekly orders" → Koeffizient = absolute Anzahl
- "Probability of joining" → Koeffizient = pp Veränderung in Wahrscheinlichkeit

### Beispiel Reshef Table 2

Notes sagen: *"The dependent variables are the per business inverse hyperbolic sine transformation of weekly number of orders ... and should be interpreted as percent changes on a scale from 0 to 1."*

Col 1: `Treat × Post = 0.007`
→ Effekt = **0.7%** (auf 0–1-Skala bedeutet 0.007 = 0.7%)

Der Text sagt: *"a 4.5 percent increase in revenue"* — was zu `β = 0.044` in Col 2 passt (Panel B).

**Wichtig:** Reshef interpretiert seine Koeffizienten **direkt als Prozent**, nicht als Prozentpunkte. Das ist nicht falsch, aber präzise gesagt: Es sind **% Veränderungen relativ zur Baseline**.

---

## 6. Log vs. Levels — Koeffizienten-Interpretation

### Das Grundprinzip

| Y-Form | X-Form | Interpretation von β |
|---|---|---|
| Level (Y) | Level (X) | β = Anstieg in Y pro Einheit-Anstieg in X |
| **Log(Y)** | Level (X) | **β·100 ≈ % Veränderung in Y pro Einheit-Anstieg in X** |
| Level (Y) | Log(X) | β/100 = Anstieg in Y pro 1% Anstieg in X |
| Log(Y) | Log(X) | β = **Elastizität** (% Anstieg in Y pro % Anstieg in X) |

### Warum log? — Drei Gründe

1. **Skalierungs-Effekte:** Wenn Y stark variiert (z.B. Umsätze von $100 bis $1Mio), wirkt log-Transformation symmetrisierend
2. **Multiplikative Effekte:** Wenn der "wahre" Effekt multiplikativ ist (z.B. +10%, nicht +$10), passt log
3. **Heteroskedastizität reduzieren:** Manchmal werden Standardfehler stabiler

### Approximation vs. Exact

Für **kleine** β (sagen wir |β| < 0.1):
- `β = 0.05` → ~5% Effekt (Approximation reicht)

Für **größere** β:
- Exakt: `(e^β − 1) × 100%`
- `β = 0.5` → e^0.5 − 1 = 0.649 = **64.9%** (nicht 50%!)
- `β = −0.3` → e^(−0.3) − 1 = −0.259 = **−25.9%** (nicht −30%)

### Praktisch in Klausur

Wenn `Y = log(Y_orig)`:
- Koeffizient 0.05 → ~5% (close to β, no need to exponentiate for small β)
- Koeffizient 0.5 → **NICHT 50%, sondern 65%** (exponentiate für große β!)

### Beispiel Zhang-Zhu (Online Appendix)

In ihrem Robustness-Check fanden sie: "We repeat the regression analysis, this time using **the logarithm** of each contributor's weekly contribution of new articles as the dependent variable."

→ In dieser Spec sind Koeffizienten **% Veränderungen**, nicht absolute Beiträge. Wichtig zu wissen, wenn du Tabellen in Appendices liest.

### Wie erkennst du log in Tabellen?

**Im Header oder Footer der Tabelle:**
- "Dependent variable: Log(Sales)"
- "Y is in logs"
- "ln(weekly_orders)"

**Im Methoden-Text:**
- "We regress the natural logarithm of Y on..."
- "We use a log-linear specification"

---

## 7. IHS (Inverse Hyperbolic Sine) — der Reshef-Spezialfall

Reshef nutzt nicht log, sondern **Inverse Hyperbolic Sine (IHS)** Transformation:

```
arcsinh(Y) = ln(Y + √(Y² + 1))
```

**Warum nicht einfach log?**
- log(0) ist undefiniert → Problem bei Y = 0 Beobachtungen
- IHS funktioniert auch bei Y = 0
- IHS-Koeffizienten verhalten sich für große Y wie log-Koeffizienten (≈ % Effekte)

**In Reshef:** *"should be interpreted as percent changes on a scale from 0 to 1"*

→ `β = 0.042` heißt **+4.2% Veränderung**.

**Klausur-relevant:** Wenn du "arcsinh" oder "IHS" siehst, interpretier den Koeffizienten **ähnlich wie log**: ~% Veränderung.

---

## 8. Universelle Checkliste — wie liest du JEDE Tabelle in 5 Schritten?

### Schritt 1: Lies den Titel + Notes der Tabelle

- Titel: "Table 4 — DiD Estimations of the Impact of the Block on Contributors" — sagt dir: DiD-Methode, Treatment = Block
- Notes (am Ende der Tabelle): Klärt Einheiten, Standardfehler, Spezifikations-Annotation

### Schritt 2: Identifiziere die abhängige Variable (Y)

- Im Tabellen-Header
- Manchmal pro Spalte unterschiedlich (Reshef Panel A vs. Panel B)
- **Frage:** Ist Y in **Levels**, **logs**, oder eine **Rate**?

### Schritt 3: Finde die Hauptvariable von Interesse (X)

- Nicht alle Variablen sind gleich wichtig!
- Die wichtige Variable ist die, die die **kausale Frage** beantwortet
- Bei DiD: die Interaktion
- Bei RDD: der Treatment-Indikator
- Bei IV: die endogene Variable in 2nd Stage

### Schritt 4: Lese den Koeffizienten + Standardfehler

- Vorzeichen (+/−)
- Größe (klein/groß relativ zur baseline mean von Y)
- Signifikanz (Sterne, oder t = β/SE > 1.96?)

### Schritt 5: Übersetze in ökonomische Aussage

- Y ist log → "X führt zu β·100% Veränderung in Y"
- Y ist level → "X führt zu β absoluten Einheiten Veränderung in Y"
- Y ist Rate → "X führt zu β Prozentpunkten Veränderung in der Rate"

### Schritt 6 (bonus): Robustheits-Check

- Variieren die Koeffizienten zwischen den Spalten stark?
  - Stabil → robust (gut)
  - Stark schwankend → bedenklich
- Wenn Vorzeichen wechselt → Identifikations-Problem!

---

## 9. Cheat-Sheet: Common Patterns in Kurs-Papers

| Paper | Methode | "Right" Coefficient | Y-Form | Interpretation |
|---|---|---|---|---|
| **Zhang & Zhu (2011)** | DiD | `PercentageBlocked × AfterBlock` | Level (number of contributions) | Absolute Anzahl Beiträge pro Einheit PercentageBlocked |
| **Reshef (2023) Table 2** | DiD | `Treat × Post` | IHS-transformed | % Veränderung (≈ log) |
| **Reshef (2023) Table 3** | DDD | `Treat × Post` (Baseline-Gruppe) + `Treat × Post × Low` (Differenz) | IHS-transformed | % Veränderung, getrennt nach High/Low Quality |
| **Luca (2016) Yelp** | RDD | Treatment-Indikator (above cutoff) | log(revenue) | ~5-9% Revenue-Increase pro Stern |
| **Chevalier-Mayzlin (2006)** | DiD across platforms | Interaktion (Reviews × Platform) | log(sales) | % Veränderung in Sales |
| **Resnick et al. (2006)** | Field Experiment | Treatment-Indikator (high-rep account) | Price | Absolute $-Differenz oder % Premium |

---

## 10. Typische Klausurfehler beim Tabellen-Lesen

| Fehler | Korrekt |
|---|---|
| "Der R² ist niedrig → das Paper ist schwach" | NEIN — R² ist für Vorhersage, nicht Kausalität. Kausal-Schätzer können auch bei niedrigem R² gut sein. |
| "Alle 6 Spalten zeigen dasselbe → redundant" | NEIN — sie zeigen Robustheit. Wenn alle 6 ähnlich, ist das ein Pluspunkt. |
| "Koeffizient auf `Post` ist der Effekt" | NEIN — bei DiD ist die **Interaktion** Treat × Post der Effekt. |
| "β = 0.5 in log-Spezifikation bedeutet 50%" | NEIN — bei großen β: e^0.5 − 1 = 65%. Approximation bricht bei großen Werten. |
| "Standardfehler in Klammern = Standardabweichung" | NEIN — SE ist die Wackelhaftigkeit des Schätzers, SD die Daten-Streuung. |
| "Wenn ich Prozent und Prozentpunkte verwechsle, ist das egal" | NEIN — 5pp Anstieg von 20% Marktanteil = 25% Marktanteil = 25%-relative-Zunahme. Verwechslung führt zu völlig anderen Aussagen. |
| "Bei DDD den Koeffizienten der Triple-Interaktion direkt als Effekt nehmen" | NEIN — die Triple-Interaktion misst die **Differenz**, nicht den Effekt selbst. Du musst Koeffizienten oft **addieren** (β₁ + β₂). |
| "Bei IV ist nur die Second Stage relevant" | NEIN — First-Stage F > 10 ist essenziell. Schwaches Instrument → schlechter Schätzer. |

---

## 11. Worked Example — Reshef Table 3 in voller Tiefe

Lass uns konkret durch eine DDD-Tabelle aus Reshef gehen. Hier ist sie vereinfacht:

```
Panel A. Weekly number of orders
                        (1)         (2)         (3)        (4)         (5)         (6)
Treat × Post         0.036       0.050       0.042      0.065      1.106       1.432
                    (0.007)     (0.010)     (0.009)    (0.012)    (0.202)     (0.269)
Treat × Post × Low  -0.062      -0.098      -0.084     -0.119     -1.654      -2.342
                    (0.010)     (0.013)     (0.012)    (0.015)    (0.286)     (0.377)
β₁ + β₂             -0.026      -0.048      -0.042     -0.054     -0.548      -0.910
p-value              0.001       0.000       0.000      0.000      0.015       0.000

Observations    4,409,516  2,173,244   2,623,347 1,321,619 4,409,516  2,173,244
Treatment def.    Median     25< >75    Median    25< >75   Change     Change
Quality def.      Median     25< >75    25< >75   25< >75   Median     25< >75
```

### Schritt 1: Was misst die Tabelle?

Title + Notes: *Heterogeneous Effects on Incumbent Firms*. Die Y-Variablen sind **IHS-transformed** ("interpreted as percent changes on a scale from 0 to 1"). 

→ **Y ist in % Veränderungen.**

### Schritt 2: Was ist die zentrale Variable?

Reshef hat **zwei** Treatment-Effekte (für High vs. Low Quality):
- `Treat × Post` = Effekt für **High-Quality** (die Baseline-Gruppe)
- `Treat × Post × Low` = **Differenz** zum Low-Quality-Effekt
- `β₁ + β₂` = Effekt für **Low-Quality** (Addition)

### Schritt 3: Was bedeuten die Spalten?

- (1) (3) (5) verwenden **Median**-Quality-Definition
- (2) (4) (6) verwenden **25/75**-Perzentil-Definition (sharper)
- (1)(2) = Median-Treatment, (3)(4) = Sharp-Binary-Treatment, (5)(6) = Continuous Treatment

→ 6 verschiedene Spezifikations-Kombinationen, alle als Robustheits-Checks.

### Schritt 4: Lese die Hauptspalte (Col 1)

- `Treat × Post = 0.036***` → **High-Quality bekommt +3.6%** mehr Bestellungen
- `Treat × Post × Low = −0.062***` → Differenz für Low-Quality ist **−6.2%** (relativ zu High)
- `β₁ + β₂ = −0.026` → **Low-Quality bekommt −2.6%** weniger Bestellungen
- p-value = 0.001 für die Summe → signifikant verschieden von 0

### Schritt 5: Ökonomische Aussage

> "Entry of new restaurants ins Plattform-Markt führt zu einer Polarisierung: **High-Quality-Inkumbenten gewinnen 3.6% mehr Bestellungen**, während **Low-Quality-Inkumbenten 2.6% verlieren**. Der Differenz-Effekt ist hoch signifikant. Das ist konsistent mit der Theorie, dass Konsumenten bei mehr Auswahl zu hochwertigen Optionen wandern."

### Schritt 6: Robustheits-Check

Schau die Koeffizienten quer über die Spalten:
- High-Quality-Effekt: 3.6% bis 6.5% (alle positiv, alle signifikant) ✓
- Low-Quality-Effekt: konsistent negativ (−2.6% bis −5.4% in den binären Specs; viel größer in den continuous Specs, aber Vorsicht — andere Skalierung)

→ **Robust.** Die Story ist stabil über Spezifikationen.

---

## 12. Wann lohnt es sich, Tabellen genauer zu lesen?

**Schau dir genau an:**
- Die **Haupttabelle** (Table 2 oder so) — die zentrale Aussage
- **Heterogenitäts-Tabellen** (DDD) — wenn das Paper Subgroup-Effekte diskutiert
- **Robustheits-Tabellen** im Appendix — wenn der Effekt "wackelig" wirkt

**Skip:**
- Reine Deskriptiv-Tabellen (Demographics, Summary Stats)
- Tabellen, die nur Power oder Pre-Trends zeigen (außer du diskutierst Methodik)
- Robustness-Check-Spalten, die das gleiche zeigen wie die Haupt-Spalte

---

## Verwandt

- [[20.studies/Organizational-Economics/identifikationsstrategien]] — die Methoden im Detail (IV, DiD, FE, RCT)
- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — ökonomische Stories der Papers
- [[20.studies/Organizational-Economics/section5-ratings-reviews]] — empirische Papers in Section 5 (Luca, Chevalier-Mayzlin, Resnick)
- [[20.studies/Organizational-Economics/Hub]]
