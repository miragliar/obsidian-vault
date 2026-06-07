---
created: 2026-06-07
type: paper-overview
source: ME 3 Aguiar Tutorial Papers (8 Stück)
tags: [organizational-economics, papers, methoden, robustheit, klausur-vorbereitung]
status: master
---

# Die 8 Paper-Steckbriefe — Methoden, Effekt-Tabellen und Robustheits-Checks

> **Use:** Schnelle Übersicht für jedes Paper, das in den Tutorials behandelt wurde. Wenn die Klausur fragt "Welche Methode? Wo der Effekt? Was wäre Robustheits-Konzern?" → diese Tabelle.

---

## Übersicht

| # | Paper | Methode | Effekt-Tabelle & Spalte | Robustheit & Validität (Check) |
|---|---|---|---|---|
| **1** | **Zhang & Zhu (2011)** — Chinese Wikipedia (Tut. 3) | DiD (natural experiment: Block of Wikipedia in China) | **Table 4, Col 1:** Koeffizient `PercentageBlocked × AfterBlock = −1.717***`. Cols 4–6 = robustness mit Fixed Effects | **Parallel pre-trends** vor dem Block prüfen (2003/2004 als Placebo-Periode). Robustness: politische Artikel ausschließen, IT-Kategorien ausschließen, banned Users ausschließen, Proxy-Server-Nutzer ausschließen. |
| **2** | **Algan et al.** — Swiss Surfing / Social Ties (Tut. 3) | IV / natural experiment (Schweizer Breitband-Rollout als Instrument) | Haupttabelle: 2SLS Second Stage. Koeffizient auf endogene Variable (Broadband-Adoption → Content-Creation/Social Ties) | **First-Stage F-Stat > 10** prüfen (Relevanz des Instruments). **Exklusions-Restriktion** ökonomisch argumentieren (Breitband nur über Internet-Nutzung, nicht direkt auf Outcomes). Reduced-Form-Check (Z auf Y direkt). |
| **3** | **Reshef (2023)** — Smaller Slices of a Growing Pie (Tut. 4) | DiD + Event Study + DDD (Heterogenität) | **Table 2, Cols 1–3** für Average Effect (`Treat × Post`). **Table 3** für Heterogenität: `Treat × Post` für High-Quality + `β₁+β₂`-Zeile für Low-Quality | **Event Study (Figure 3)** zeigt parallele Pre-Trends. Robustness: verschiedene Treatment-Definitionen (Median/Sharp/Continuous), verschiedene Quality-Definitionen, IPW-Matching, de Chaisemartin/D'Haultfœuille-Korrektur für heterogene Treatment-Effekte (Two-Way-FE-Bias). |
| **4** | **Klein, Kurmangaliyeva, Prüfer & Prüfer (2025)** — User-Generated Data & Search Quality (Tut. 9) | RCT / Field Experiment (kleine Suchmaschine mit exogen variierter Datenmenge) | Haupttabelle mit Treatment-Indikator: Effekt von "mehr Daten" auf Result-Quality (typischerweise Col 1 oder die Spec mit allen Controls) | **Randomization Balance** prüfen (sind treated/control auf Observables ähnlich?). **Compliance**: lieferte das Treatment wirklich mehr Daten? Heterogenität: Effekt vor allem bei Rare Queries (74% der Traffic) — separate Specs für rare vs. common queries. |
| **5** | **Marita Freimane (2025)** — Gender Bias, Feedback & Productivity (Tut. 10) | DiD (YouTube Dislike-Removal als exogener Schock) | Haupt-DiD-Tabelle: `Female × Post`. Resultate: +8.4% Videos, +15.5% Demand bei Frauen | **Parallel Pre-Trends** für Male/Female Productivity vor Dislike-Removal. **Placebo Test**: Effekt kommt vom Drop in Dislikes, nicht von der Entfernung aus Public View. **Spillover-Check**: keine Effekte auf Comments → Mechanismus ist spezifisch Dislikes. |
| **6** | **Seamans & Zhu (2014)** — Craigslist on Newspapers (Tut. 10) | DiD mit staggered Craigslist-Entry (zeitlich/geografisch gestaffelt) | Mehrere Outcome-Tabellen (Classified-Ad-Rates, Subscription-Prices, Display-Ad-Rates, Differenzierung). Schlüssel-Koeffizient: `CraigslistEntry × Post` in jeder Tabelle | **Parallel Pre-Trends** vor Craigslist-Entry. **Endogenes Entry-Timing**: prüfen ob Craigslist gezielt in schwächere Newspaper-Märkte einging (Bias-Quelle). Alternative Control-Gruppen (geografisch ähnliche Märkte ohne Entry). |
| **7** | **Anderson & Magruder (2012)** — Yelp RDD (Tut. 11) | RDD (Half-Star-Rounding-Cutoff bei Yelp-Ratings) | RDD-Tabellen mit Treatment-Indikator "above cutoff". Effekt: +19 pp (49%) Sellout-Frequency. Spalten = verschiedene Bandbreiten um Cutoff | **McCrary-Test** (keine Manipulation der Running Variable — Restaurants heap nicht künstlich über dem Cutoff). **Covariate Continuity** (keine Diskontinuität in Beobachtbaren am Cutoff). Robustness: verschiedene Bandbreiten + Polynomial-Ordnungen + Donut-Hole-Spec. |
| **8** | **Bursztyn, Handel, Jiménez-Durán & Roth (2025)** — Social Media Collective Traps (Tut. 11) | Online RCT / pre-registriert (BDM/MPL-Mechanism in 3 Steps) | Tabellen mit WTA-Schätzern: Vergleich `Valuation Keeping Network` vs. `Removing Network` vs. `Nonexistence`. Effekt = Differenz zwischen den drei Steps | **Incentive Compatibility** des BDM-Mechanism (Anreiz, ehrlich zu antworten). **Randomization Balance** zwischen Gruppen. **Pre-Registration** limitiert Researcher-Degrees-of-Freedom (HARKing). Robustness: Konsistenz über TikTok vs. Instagram, verschiedene Sub-Samples. |

---

## Universelle Validitäts-Checks pro Methode

Falls du dir bei einem unbekannten Paper unsicher bist, frage:

| Methode | Wichtigste Validitäts-Frage | Sekundäre Robustheit |
|---|---|---|
| **DiD** | Sind die Pre-Trends parallel? | Placebo-Tests, alternative Control-Gruppen |
| **DDD** | Wie bei DiD + ist die "Differential"-Annahme glaubwürdig? | Verschiedene Subgroup-Definitionen |
| **RDD** | Keine Manipulation am Cutoff (McCrary)? | Verschiedene Bandbreiten + Polynomial-Ordnungen |
| **IV** | First-Stage F > 10? Exklusion plausibel? | Reduced-Form-Check, Overidentification-Tests |
| **RCT** | Randomization Balance? Compliance? | Pre-Registration, ITT vs. LATE |
| **FE** | Reicht Zeitkonstanz oder gibt es time-varying Confounder? | Verschiedene FE-Sets (Unit / Time / Unit×Time) |

---

## Verwandt

- [[20.studies/Organizational-Economics/paper-tables-guide]] — Wie liest man die Tabellen im Detail
- [[20.studies/Organizational-Economics/identifikationsstrategien]] — Methoden-Cheatsheet (IV, DiD, FE, RCT)
- [[20.studies/Organizational-Economics/section5-ratings-reviews]] — Section 5 VL-Papers (Luca, Chevalier-Mayzlin, Resnick)
- [[20.studies/Organizational-Economics/Hub]]
