---
created: 2026-06-18
type: exam-feedback
source: Claudian-Korrektur der zwei Probeprüfungen (Sample-Final-Exam + Sample-Final-Exam-2)
tags: [organizational-economics, klausur-19-juni, fehler-muster, lernfokus]
status: master
---

# Probeprüfungs-Korrektur — 2026-06-18

> Zwei Sample-Klausuren, beide Teil A + Teil B bewertet (Teil C handschriftlich, ausgelassen). Teil B nachsichtig, fokussiert auf Intuition statt jedes Schlüsselwort.

## Gesamtbild

| Komponente | Punkte | Anteil |
|---|---|---|
| Exam 1 — Teil A (MC) | 16 / 30 | 53 % |
| Exam 1 — Teil B (Paper) | 17.5 / 30 | 58 % |
| Exam 2 — Teil A (MC) | 16 / 28 | 57 % |
| Exam 2 — Teil B (Paper) | 21 / 30 | 70 % |
| **Total ohne Teil C** | **70.5 / 118** | **≈ 60 %** |

**Lese-Linie.** Teil B ist klar besser als Teil A; in Klausur 2 (Intuitions-MC, weniger Tabellen-Folien-Items) hast du in beiden Teilen mehr Score gemacht. Die Schwächen in Teil A sind **inhaltlich klar geclustert** — nicht zufällig — und in nur ~3 Stunden gezielt fixbar.

---

## Teil A — Welche Fragen waren falsch

### Exam 1 (15 MC × 2 Pkt)

| Q | Section | Dein | Richtig | Fehler |
|---|---|---|---|---|
| Q1 | S1 | B,C | B,C | ✅ |
| **Q2** | S1 | B,C | C,D | (B) fälschlich markiert + (D) fehlt |
| Q3 | S1 | A,B,C | A,B,C | ✅ |
| Q4 | S2 | A,B | A,B | ✅ |
| **Q5** | S2 | C,D | A,C,D | (A) fehlt — "NE = endogene vertikale Differenzierung" |
| **Q6** | S2 | A,C,D | A,B,C | (D) zu Unrecht; (B) fehlt — Data-NE-Bedingung |
| Q7 | S3 | A,B,C | A,B,C | ✅ |
| Q8 | S3 | A,C,D | A,C,D | ✅ |
| **Q9** | S3 | B,D | A,B | (D) markiert obwohl D RICHTIG ist (Frage: "welche sind FALSCH?") + (A) fehlt |
| **Q10** | S4 | B,C | A,C | (B) fälschlich markiert + (A) fehlt |
| **Q11** | S4 | B,D | B,C | (D) fälschlich markiert + (C) fehlt |
| **Q12** | S4 | A,B | A,B,D | (D) fehlt — Pre-Trxn-Comms treibt Leakage |
| Q13 | S5 | A,C | A,C | ✅ |
| Q14 | S5 | A,B,D | A,B,D | ✅ |
| Q15 | S5 | B,D | B,D | ✅ |

→ 8 von 15 richtig.

### Exam 2 (7 MC × 4 Pkt)

| Q | Section | Dein | Richtig | Fehler |
|---|---|---|---|---|
| **Q1** | S1 | B | B,D | (D) fehlt — "User können nicht zu Ad-hoc-Alternative" ist auch valid |
| Q2 | S2 | A,B | A,B | ✅ |
| **Q3** | S2 | A,C,D | A,D | (C) fälschlich markiert — billiges Multi-Homing **senkt** Defensibility |
| Q4 | S3 | A,B,C | A,B,C | ✅ |
| **Q5** | S4 | A,C,D | A,B,D | (B) fehlt + (C) fälschlich markiert — beides Lerner/Non-Neutralität |
| Q6 | S4 | A,B,D | A,B,D | ✅ |
| Q7 | S5 | A,B,C | A,B,C | ✅ |

→ 4 von 7 richtig.

---

## Fehler-Muster — gebündelt auf 5 Cluster

Wenn du nur **fünf Sachen** vor der Klausur fixierst, sind es diese.

### Cluster A ⭐⭐⭐  CGNE im Pricing — Lerner-Adjustment + Non-Neutralität

**Betroffen:** Exam 1 Q11 (D, C) und Exam 2 Q5 (B, C). Zwei Wiederholungen → wichtigste Stelle.

**Die zwei Aussagen, die du beide drauf haben musst:**

1. **Lerner mit CGNE → niedrigere Preise, nicht höhere.** Die Formel ist
   `P_s = c_s − β_b · n_b + N_s(u_s)/N_s'(u_s)`.
   Das `−β_b · n_b` ist eine **negative effektive Marginal-Cost**: jeder zusätzliche Seller bringt der Plattform indirekt mehr Buyer-Profit, also ist der Plattform-Anreiz, ihn zu attractionen, höher als bei einem Standard-Monopol → Preis niedriger.
   In Exam 1 Q11 D / Exam 2 Q5 B war jeweils die richtige Aussage: "Plattform-Lerner gibt **LOWER** markup als Standard-Monopol mit gleicher Elastizität" — Markup nach unten gedrückt durch Cross-Group-Subvention.

2. **Price Structure ist non-neutral: Aufteilung matters, nicht nur Summe.** In einer two-sided Plattform bestimmt nicht nur `(a_b + a_s)`, sondern die Splittung das Gleichgewicht. Grund: die Demand auf jeder Seite hängt direkt von der Größe der **anderen** Seite ab. Daher wirkt eine Verschiebung der Last von b nach s nicht wie eine Tirole-style Steuer-Inzidenz-Verschiebung, sondern verändert das Equilibrium fundamental.
   In Exam 2 Q5 C hast du fälschlich gesagt "Summe matters, Split egal" — das ist genau der klassische Fehler.

**Mnemonik.** *Cross-Group ist eine negative Marginal-Cost. Negative MC ⇒ niedrigerer Preis. Negative MC ist seiten-spezifisch ⇒ Split ist non-neutral.*

→ Recap-Kurs: [[20.studies/Organizational-Economics/section4-pricing-disintermediation#5. Lerner-Index für Plattformen]]

---

### Cluster B ⭐⭐  Defensibility-Faktoren — was härtet vs. was öffnet

**Betroffen:** Exam 2 Q3 (C falsch). Die Hälfte der Defensibility-Liste ist invertiert: was man häufig automatisch als "gut für Plattform" liest, ist tatsächlich Risiko.

**Die 4 Aguiar-Faktoren mit RICHTUNG:**

| Faktor | Defensibility ↑ | Defensibility ↓ |
|---|---|---|
| **Strength & Scope of NE** | Stark + global | Schwach + lokal |
| **Multi-Homing** | Teuer (man kann nicht beide nutzen) | **Billig** (User kann beide gleichzeitig) |
| **Coordination Costs** | Hoch (Lern-/Switching-Kosten) | Niedrig (alle können einfach gemeinsam wechseln) |
| **Trust & Value-Add** | Plattform liefert proprietären On-Platform-Service | User können off-platform problemlos transactieren |

In Exam 2 Q3 hattest du C markiert: "Multi-Homing ist billig → härtet Defensibility". Genau das Gegenteil: billiges Multi-Homing ist die **klassische** Defensibility-Schwäche (Uber vs. Lyft, Spotify vs. Apple Music).

**Mnemonik.** *Lokales NE, billiges Multi-Homing, niedrige Coord-Costs, schwacher Value-Add — vier Lecks im Schiff.*

→ Recap-Kurs: [[20.studies/Organizational-Economics/section2-demand-competition#4. Defensibility: Beyond Network Effects]]

---

### Cluster C ⭐⭐  Indirect NE, Data NE — Definitions-Subtilitäten

**Betroffen:** Exam 1 Q2 (B falsch), Exam 1 Q6 (B fehlt, D falsch).

**Subtilität 1: Indirect NE existieren auch in einseitigen Plattformen.**
In Exam 1 Q2 (B) hast du gesagt "Indirect NE only in 2-sided" — falsch. Eine einseitige Plattform mit Data NE (Waze, Google Search) hat indirekte NE: dein Datum macht den Algorithmus besser → besseres Service für alle anderen User. Eine einzige Gruppe, aber indirekt verkettet über Daten.

**Subtilität 2: Die DREI Aguiar-Bedingungen für Data-Defensibility.**
In Exam 1 Q6 hast du fälschlich (D) "muss collaborative filtering sein" als notwendig markiert. Das ist eine typische Implementation, aber nicht zwingend.

Die drei NOTWENDIGEN Bedingungen sind:

1. **Cross-User Spillover** (Datum von User A verbessert Service für User B). *Ohne das: nur eine supply-side scale economy, kein NE.*
2. **Persistent / non-depreciating Value** (Daten bleiben über Zeit relevant, und Margin-Value sinkt nicht schnell auf 0).
3. **Proprietär + hard to imitate** (Daten + Improvements können nicht trivial kopiert werden).

Collaborative filtering ist eine TYPISCHE Implementation von (1), aber nicht die einzige.

**Mnemonik.** *Spillover + Persistenz + Proprietät. Drei Bedingungen, keine vier, kein collaborative-filtering-Zwang.*

→ Recap-Kurs: [[20.studies/Organizational-Economics/section2-demand-competition#5. Data Network Effects]]

---

### Cluster D ⭐⭐  Disintermediation + Membership vs. Transaction Fees

**Betroffen:** Exam 1 Q9 (D), Q10 (B), Q12 (D). Drei verschiedene Items im selben Cluster.

**Sub-Pattern 1: Pre-Transaction Communication treibt Leakage.**
In Exam 1 Q12 hast du D nicht markiert. Aber pre-trade-Kommunikation (Custom-Freelance-Briefs, Wedding-Planning, Home-Repair) **erzwingt Kontakt-Daten-Austausch** → Kontakt direkt vorhanden → off-platform-Trade trivial.
**Disintermediation-Treiber-Liste:** (1) hoher Trxn-Wert, (2) repeated Trade mit derselben Person, (3) **viel Pre-Trxn-Communication nötig**, (4) in-person Treff, (5) wenig Plattform-Value-Add.

**Sub-Pattern 2: Many small Trxns ⇒ Membership, nicht Transaction.**
In Exam 1 Q10 hattest du (B) "Many small Trxns" als pro-Transaction-Argument markiert. Genau umgekehrt: bei vielen kleinen Trxns ist der per-Trxn-Tracking-Aufwand groß → MEMBERSHIP ist effizienter. Transaction-Fees sind sinnvoll wenn Trxns **leicht observierbar UND unfrequent aber wertvoll** sind (Airbnb-Übernachtung, Uber-Ride als Beispiele).

**Sub-Pattern 3: Negative Prices sind in D&C die OPTIMALE Antwort, nicht ein Fehler.**
In Exam 1 Q9 hattest du (D) als FALSCH markiert — aber D ist WAHR: bei `r_k < u_k⁰` ist der optimale Subsidy-Preis tatsächlich NEGATIV (Plattform zahlt den User für's Joinen — Uber-Driver-Garantie-Beispiel).
**Wichtig:** die Frage hieß "Welche sind FALSCH?" — Fragetyp hat dich vermutlich verwirrt. Bei FALSCH-Fragen: zwei Filter durchlaufen.

→ Recap-Kurs: [[20.studies/Organizational-Economics/section4-pricing-disintermediation]]

---

### Cluster E ⭐  Hotelling + NE = endogene vertikale Differenzierung

**Betroffen:** Exam 1 Q5 (A fehlt).

**Die zentrale Set-2-Aussage:** Network Effects wirken in einem Hotelling-Setting **wie eine endogene Qualitäts-Boost** für die Plattform mit der größeren erwarteten Userbase. Daher tilten stärkere `β` die Markt-Anteile weiter zur größeren Plattform — wie eine reine Quality-Wedge `q`. Formal: `∂n_1/∂n_1^e = β/(2τ)` — größeres β = mehr "self-fulfilling tilt".

**Konsequenz.** No-Tipping-Bedingung ist `q < 3(τ − β)`. Stärkeres β verschiebt die Tipping-Region **nach unten** (kleineres q reicht zum Tipping).

→ Recap-Kurs: [[20.studies/Organizational-Economics/section2-demand-competition#2. Demand & Pricing of Incompatible Network Goods]]

---

## Teil B — Wo das Verständnis schon sitzt und wo nicht

### Was gut sitzt

- **Identifikations-Strategie sauber benennen** (Exam 2 B1 Sub 1 hervorragend, Exam 1 B1 Sub 1 solide). RDD, DiD, Treatment/Control klar.
- **Cross-side propagation in Newspaper-Beispiel** (Exam 2 B1 Sub 2): "Money side verliert → Subsidy side wird belastet" — exakt die Aguiar-Mechanik.
- **YouTube-Dislike-Mechanismus über Herding** (Exam 2 B2 Sub 3): das Wort "Manipulation" war strikt-genommen das gefragte Schlüsselwort, aber dein "Herding"-Argument ist ökonomisch korrekt und reicht im closed-book Setting.
- **High-vs.-Low-Quality-Polarisierung bei Reshef** (Exam 1 B2 Sub 3): die zwei Forces (Business-Stealing vs. indirect NE via new users) hast du.

### Wo es noch klemmt

**T1 — DDD vs. Staggered DiD nicht trennscharf** (Exam 1 B2 Sub 1).
Du hast "Triple D = staggered over time" geschrieben. Sind zwei verschiedene Designs:

- **DDD** = drei DIMENSIONEN (z.B. City × Time × Quality). Drei Differenzen werden gebildet.
- **Staggered DiD** = ZEITLICHE Versetzung des Treatments (Einheiten werden zu unterschiedlichen Zeitpunkten treated).

Reshef ist beides — die Staffelung gibt Identifikation, die Triple-Dimension trennt heterogen.

**T2 — Statistische Signifikanz bei DDD-Sums übersehen** (Exam 1 B2 Sub 2).
Du hast für Low-Quality "−2.6 %, not statistically significant" gesagt. Aber Tabelle 3 zeigt `β₁ + β₂ = −0.026` mit **p-value 0.001** — also signifikant bei 1 %. Bei DDD-Tabellen schaue immer die `β₁ + β₂` Zeile und ihre p-value mit an, nicht nur die rohen Koeffizienten.

**T3 — Asymmetrische Information richtig herum drehen** (Exam 1 B1 Sub 3).
Du hast geschrieben: *"More ratings → better informativeness for diners → probability of being sold out shrinks with less reviews."* Genau umgekehrt:
- WENIGER Reviews (100–500) = WENIGER unabhängige Info → Yelp-Rating ist marginal **wertvoller** → größerer RD-Effekt.
- MEHR Reviews (>500) = schon viel bekannt → Yelp-Signal **marginal weniger informativ** → kleinerer Effekt (Spalte 3: −0.005, ≈ 0).

Die Logik ist: **R&R-Systeme sind dort am wertvollsten, wo asymmetrische Information am größten ist.** Das ist auch die Story bei Luca's Chains vs. Independents.

**T4 — Cross-Side-Propagation = Price Structure Non-Neutralität, nicht D&C** (Exam 2 B1 Sub 3).
Du hast "Divide and Conquer" geschrieben. D&C ist eine LAUNCH-Strategie (Section 3) für das Henne-Ei-Problem. Was Seamans-Zhu zeigen, ist:
- Eine Plattform mit mehreren Sides hat eine optimale **Aufteilung der Fees** über die Sides.
- Wenn auf einer Seite ein Schock kommt (Craigslist drückt Classified Rates), reoptimiert die Plattform die Aufteilung — sie erhöht den Preis auf der subscriber-Seite, weil die optimale Split sich verschoben hat.
- Das ist die empirische Manifestation der **Price Structure Non-Neutralität** (Section 4).

D&C wäre, *wenn die Plattform initial alle Newspapers gewonnen hätte*. Hier geht es um optimal pricing **nach** einem Wettbewerbs-Schock.

---

## Empfehlung für die Klausur am 19. Juni

**Heute Abend (90 Min reicht):**

1. Section 4 nochmal durchgehen, **fokussiert auf Lerner-Adjustment + Non-Neutralität**. [[20.studies/Organizational-Economics/section4-pricing-disintermediation]]
2. Defensibility-Liste mündlich aufsagen, mit RICHTUNG (was härtet, was öffnet). [[20.studies/Organizational-Economics/aufzaehlungen-cheatsheet|Aufzählungen-Cheatsheet]] Frage 2.
3. Data-NE-Bedingungen aus dem Kopf rezitieren (Spillover, Persistenz, Proprietät). [[20.studies/Organizational-Economics/aufzaehlungen-cheatsheet|Aufzählungen-Cheatsheet]] Frage 7.

**Donnerstag Morgen:**

4. 5-Minuten-Drill: "Membership oder Transaction Fee?" — durchgehen mit Beispielen.
5. "Welche Sektion ist welche Frage zuständig?" — wenn du "Cross-Side-Propagation" siehst, sag automatisch "Section 4 / Price Structure Non-Neutrality"; wenn "Henne-Ei", sag "Section 3 / D&C".

**Bei Multi-Select-Fragen in der Klausur:**

- Bei "FALSCH"-Frageformat **zweimal** lesen. Du hast in Q9 D als FALSCH markiert, obwohl D wahr ist — die Frage hat dich verleitet.
- Bei jeder Option **separat** entscheiden, mit der Logik "ist diese Aussage als geschriebene Aussage wahr?" — nicht "passt diese Aussage halbwegs zur Frage?".

---

## Verwandt

- [[20.studies/Organizational-Economics/Sample-Final-Exam-Claudian]] — Klausur 1
- [[20.studies/Organizational-Economics/Sample-Final-Exam-2-Claudian]] — Klausur 2
- [[20.studies/Organizational-Economics/aufzaehlungen-cheatsheet]] — Recall-Karte
- [[20.studies/Organizational-Economics/section2-demand-competition]] — Defensibility + Data NE
- [[20.studies/Organizational-Economics/section4-pricing-disintermediation]] — Lerner + Disintermediation
- [[20.studies/Organizational-Economics/paper-tables-guide]] — Tabellen lesen (für DDD-Summen-p-values)
- [[20.studies/Organizational-Economics/Hub]]
