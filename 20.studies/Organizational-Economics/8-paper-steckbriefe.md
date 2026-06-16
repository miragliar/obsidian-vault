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

| # | Paper | Stichwort | Methode | Effekt (grob) |
|---|---|---|---|---|
| **1** | **Zhang & Zhu (2011)** (Tut. 3) | **Wikipedia** (China-Block) | **DiD** (natural experiment) | **Negativ:** Block → −1.7 Beiträge/User. Social Benefits motivieren Contributions. |
| **2** | **Algan et al.** (Tut. 3) | **Surfing** (CH-Breitband) | **IV** (Breitband-Rollout als Instrument) | **Positiv:** Broadband → mehr Content-Creation & Social Ties. |
| **3** | **Reshef (2023)** (Tut. 4) | **Pie** (Smaller Slices of a Growing Pie) | **DiD** + Event Study + DDD | **Heterogen:** Positiv für High-Quality, negativ für Low-Quality Creators. |
| **4** | **Klein et al. (2025)** (Tut. 9) | **Search** (kleine Suchmaschine) | **RCT** / Field Experiment | **Positiv:** Mehr User-Daten → bessere Result-Quality, v.a. bei Rare Queries (74% Traffic). |
| **5** | **Freimane (2025)** (Tut. 10) | **Dislikes** (YouTube Removal) | **DiD** (Dislike-Removal als Schock) | **Positiv für Frauen:** +8.4% Videos, +15.5% Demand. Bias-Reduktion durch weniger negatives Feedback. |
| **6** | **Seamans & Zhu (2014)** (Tut. 10) | **Craigslist** (Newspapers) | **DiD** (staggered Entry) | **Negativ für Newspapers:** ↓ Classified-Ad-Rates, ↑ Subscription-Preise (Two-Sided-Market-Reaktion). |
| **7** | **Anderson & Magruder (2012)** (Tut. 11) | **Yelp** (Half-Star-Cutoff) | **RDD** (Rating-Rounding) | **Positiv:** +0.5 Sterne → +19 pp (≈49%) Sellout-Frequency. Ratings kausal für Demand. |
| **8** | **Bursztyn et al. (2025)** (Tut. 11) | **TikTok/Instagram** (Collective Trap) | **RCT** (Online, BDM/MPL, pre-registriert) | **Negativ:** User würden zahlen, damit Plattform nicht existiert (Trap). WTA Keep > WTA Remove. |

---

## Universelle Validitäts-Checks pro Methode

Falls du dir bei einem unbekannten Paper unsicher bist, frage:

| Methode | Wichtigste Validitäts-Frage | Sekundäre Robustheit |
|---|---|---|
| **DiD** | Sind die Pre-Trends parallel? (= indirekte Evidenz für Common-Trends-Annahme — der eigentlichen Annahme über *counterfactual post-trends*) | Placebo-Tests, alternative Control-Gruppen, ökonomische Plausibilität der CTA |
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
