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

## Treatment vs. Control — präzise Identifikations-Setups

> **Use:** Wenn die Klausur fragt "Was war das Treatment? Wer war Treatment-/Control-Gruppe?" — diese Tabelle gibt die exakte Antwort.

| # | Paper | **Treatment-Gruppe** | **Kontroll-Gruppe** | **Was war das Treatment (= der Schock / die Intervention)** |
|---|---|---|---|---|
| **1** | **Zhang & Zhu (2011)** — Wikipedia | **Nicht-chinesische** Wikipedia-Contributors mit **hohem Anteil** chinesischer Co-Editoren (= `PercentageBlocked` hoch) | Nicht-chinesische Contributors mit **niedrigem Anteil** chinesischer Co-Editoren (`PercentageBlocked` niedrig) | **Oktober 2005:** Chinesische Regierung **blockierte Wikipedia in China** → chinesische Editors verschwanden plötzlich. Reduktion der Gruppen-Größe als exogener Schock auf die *verbleibenden* Contributors. Continuous Treatment via Interaktion `PercentageBlocked × AfterBlock`. |
| **2** | **Algan et al.** — Surfing (CH-Breitband) | Haushalte / Gemeinden in **CH-Regionen mit (frühem) Breitband-Zugang** | Haushalte / Gemeinden **ohne** Breitband-Zugang (oder mit späterem Rollout) | **Breitband-Internet-Verfügbarkeit** an sich. Endogen → daher **IV**: technisch-geographische Determinanten des Rollouts (z. B. Entfernung zur Hauptverteilung, Topologie) als **Instrument** für tatsächliche Breitband-Nutzung. First Stage prüft Relevanz (F > 10), Second Stage misst Effekt auf Content-Creation + Social Ties. |
| **3** | **Reshef (2023)** — Pie | **DiD:** **Incumbent-Restaurants in Städten mit GrubHub-YTP-Entry** (= Schock im Restaurant-Angebot). **DDD-Zusatz:** **Low-Quality** Incumbents als zweite Dimension | **DiD:** Incumbent-Restaurants in Städten **ohne / vor** dem Entry-Schock (staggered). **DDD-Zusatz:** **High-Quality** Incumbents als Baseline | **2018:** Yelp Transactions Platform (YTP) **Partnership mit GrubHub** → effektiv **massiver Eintritt neuer Restaurants** auf der Plattform. Treatment = "wie stark hat sich das Restaurant-Angebot in dieser Stadt erhöht". Heterogenität via DDD: zusätzlich Quality (High vs. Low) → Triple-Interaktion `Treat × Post × Low`. |
| **4** | **Klein et al. (2025)** — Search | User-Queries, die vom Suchmaschinen-Algorithmus mit **mehr Trainingsdaten / größerem Daten-Pool** bedient werden | Identische Queries, bedient mit **weniger Trainingsdaten / kleinerem Daten-Pool** | **Künstliche Variation der Datenmenge**, die der Algorithmus zum Lernen bekommt (Field Experiment auf einer realen, kleinen Suchmaschine). Random Assignment → saubere ATE-Identifikation. Spezieller Fokus: **Rare Queries** (74 % des Traffics). |
| **5** | **Freimane (2025)** — Dislikes | **Weibliche YouTube-Creators** (sensibler für negatives Feedback, Hypothese) | **Männliche YouTube-Creators** (Baseline) | **November 2021:** YouTube **entfernte den öffentlich sichtbaren Dislike-Count**. Plötzlicher Plattform-Design-Schock. DiD-Vergleich: Veränderung Frauen (vor/nach) **minus** Veränderung Männer (vor/nach). Misst, ob das Entfernen negativer Signale Bias auf der Supply-Seite reduziert. |
| **6** | **Seamans & Zhu (2014)** — Craigslist | **Lokale Zeitungen in Städten, in denen Craigslist** (zu einem bestimmten Zeitpunkt) **eintrat** | Lokale Zeitungen in Städten, **in denen Craigslist noch nicht eingetreten ist** (oder später) | **Craigslist-Markteintritt** in einer Stadt (staggered über Zeit 1995–2009). Verdrängt Classified-Ads-Einnahmen → Two-Sided-Market-Reaktion: Zeitungen senken Ad-Rates (Money-Side bricht weg) und **erhöhen Subscription-Preise** (Subsidy-Side wird belastet). |
| **7** | **Anderson & Magruder (2012)** — Yelp | Restaurants mit "wahrem" Rating **knapp über** dem Half-Star-Cutoff (z. B. 3.75 → angezeigt als **4.0**) | Restaurants mit "wahrem" Rating **knapp unter** dem Cutoff (z. B. 3.74 → angezeigt als **3.5**) | **Yelps Rundungs-Algorithmus**: Average wird auf nächste halbe Sterne gerundet. Restaurants direkt am Cutoff sind in ihrer **tatsächlichen** Qualität **fast identisch** (∆ ≈ 0.01), werden aber **displayed unterschiedlich** (∆ = 0.5 Sterne). Running Variable = exaktes Rating; Treatment-Indikator = `1{Rating ≥ Cutoff}`. Identifikation rein durch **Display-Manipulation**, Qualität konstant. |
| **8** | **Bursztyn et al. (2025)** — Collective Trap | User, denen die Frage gestellt wird: **"Was würdest du zahlen / verlangen, damit TikTok/IG für ALLE User verschwindet?"** (kollektives Szenario) | User, denen die Frage gestellt wird: **"Was würdest du zahlen / verlangen, damit DU SELBST TikTok/IG nicht mehr nutzt?"** (individuelles Szenario) | **Random Assignment** zwischen den beiden Szenarien. Bewertung via **BDM/MPL** (incentive-kompatible Mechanismen zur Offenlegung der wahren Zahlungsbereitschaft). Outcome: **WTA (Willingness-to-Accept) Keep** vs. **WTA Remove**. Resultat: Kollektive Removal-Bewertung > individuelle → User sind in einem **Trap** (würden lieber leben, wenn niemand drauf wäre, aber jeder einzelne joined trotzdem). Pre-registriert. |

### Methoden-Logik der Treatment-/Control-Definition

| Methode | Wie "Treatment" und "Control" entstehen |
|---|---|
| **DiD** (Zhang-Zhu, Reshef, Freimane, Seamans-Zhu) | Treatment-Gruppe = von exogenem Schock betroffen; Control-Gruppe = (noch) nicht betroffen. **Kausale Differenz** = `(ΔY_Treated) − (ΔY_Control)`. |
| **IV** (Algan et al.) | Treatment (Broadband) ist endogen → man konstruiert "as-if-randomly assigned" Variation via Instrument. Treatment-/Control-Logik ist **kontinuierlich**, nicht binär. |
| **DDD** (Reshef Erweiterung) | Zusätzliche Subgruppen-Dimension (High vs. Low Quality) → Triple-Differenz isoliert **Heterogenität** des Effekts. |
| **RDD** (Anderson-Magruder) | Treatment- und Kontroll-Gruppe sind **direkt am Cutoff** quasi-identisch → Sprung am Cutoff ist kausaler Effekt. |
| **RCT** (Klein et al., Bursztyn et al.) | Forscher randomisieren **selbst** in Treatment vs. Control → höchster interner Validitäts-Standard. |

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
