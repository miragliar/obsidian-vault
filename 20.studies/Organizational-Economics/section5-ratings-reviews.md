---
created: 2026-06-06
type: section-deep-dive
source: ME 3 Aguiar VL Section 5
tags: [organizational-economics, section5, ratings, reviews, reputation, trust]
status: master
---

# Section 5 — Ratings and Reviews Systems

> **Big Picture:** Plattformen vermitteln Trxns zwischen *Anonymen*. Ratings & Reviews (R&R) sind das institutionelle Vehikel, um Trust zu erzeugen — sie ersetzen "repeated interaction" als Disziplinierungs-Mechanismus.

---

## Roadmap

1. R&R-Systeme: Produkte vs. Sellers/Buyers
2. Network Effects durch R&R
3. Reputation als Trust-Mechanismus (Game-theoretisch)
4. Empirische Evidenz: Chevalier-Mayzlin, Luca, Resnick
5. Challenges: Selektion, Strategisches Verhalten, Reciprocity

---

## 1. Was sind R&R-Systeme?

**Asymmetric Information** ist ein zentrales Problem auf Plattformen:
- Kaufst du ein Produkt von einem unbekannten Seller? Du weißt nicht, ob es gut ist (Adverse Selection)
- Wird der Seller versenden, wie versprochen? (Moral Hazard)

R&R-Systeme adressieren beide Probleme.

### Zwei Typen

**Product R&R** (Käufer bewerten Produkt):
- Typisch für Online-Retailer (Amazon, Zalando)
- Buyer rated/reviewed das Produkt nach Kauf
- Zukünftige Buyers nutzen das Aggregat

**Seller/Buyer R&R** (Counterparts bewerten einander):
- Typisch für Marketplaces (eBay) und P2P-Plattformen (Airbnb)
- Eine Trxn führt zu *zwei* Reviews (Buyer rated Seller, Seller rated Buyer)
- Reputation wird über Zeit aufgebaut

### Was R&R *nicht* sind

R&R ≠ Quality Control durch Plattform. Plattform überprüft nicht selbst — sondern aggregiert User-Feedback. Das ist crowdsourced quality assessment.

---

## 2. Network Effects in R&R

R&R-Systeme sind selbst eine Quelle von Network Effects:

### Positive WGNE auf Buyer-Seite

> Mehr Buyers ⇒ mehr Reviews ⇒ präzisere Averages ⇒ höherer Wert für ALLE Buyers.

**Mechanik:** Mit n Reviews ist der Sample-Mittelwert mit Standardfehler O(1/√n) — je mehr Reviews, desto besser der Estimate der wahren Qualität.

→ **Attraction Loop** auf Buyer-Seite, wenn R&R-System gut designed ist.

### Positive CGNE Buyer → Seller (durch Adverse Selection)

> Mehr Buyer-Reviews ⇒ Low-Quality-Sellers werden identifiziert ⇒ verlassen Plattform ⇒ Seller-Pool wird besser ⇒ noch mehr Buyer angezogen.

→ **Self-Reinforcing Mechanism.**

### Positive CGNE Buyer → Seller (durch Moral Hazard)

> Sellers wissen, dass Verhalten getrackt ⇒ strengen sich an ⇒ Trxn-Qualität steigt ⇒ Buyers zufriedener.

### Platform-Specific Network Effects

R&R-NE sind plattform-spezifisch:
- Wenn du auf Amazon einen Laptop kaufen willst, willst du Amazon-Reviews — nicht die von Galaxus
- Sellers konditionieren Verhalten auf die Plattform (höhere Sorgfalt bei besseren Review-Systemen)
- Identity matters: derselbe Seller hat unterschiedliche Reputation auf eBay vs. Amazon

→ **R&R verstärkt erfolgreiche Plattformen** auf Kosten kleinerer Rivalen. Lock-in-Effekt.

---

## 3. Reputation als Trust-Mechanismus

### Das Trust-Game (Tadelis 2016)

Setup:
- Buyer bietet sich an, ein Produkt für 15 CHF zu kaufen
- Seller hat Cost = 5 CHF, Buyer bewertet Produkt mit 25 CHF
- Wenn Trade stattfindet & ehrlich: Buyer Surplus = 10, Seller Surplus = 10
- Wenn Seller "abused" (nimmt Geld, liefert nicht): Buyer Surplus = -15, Seller Surplus = 15

**Game-Baum:**
```
Nature: Seller honest (p) or opportunistic (1-p)
↓
Buyer: Trust or Not Trust
↓
[if Trust + honest seller] → (10, 10)
[if Trust + opportunistic seller] → Seller chooses Honor or Abuse
   → Honor: (10, 10)
   → Abuse: (-15, 15)
[if Not Trust] → (0, 0)
```

### Einmaliges Spiel

Opportunistischer Seller missbraucht *immer* (15 > 10).

Buyer rechnet damit. Buyer's erwarteter Surplus:
```
E[surplus] = p·(10) + (1-p)·(-15) = 25p - 15
Trust ⇔ E ≥ 0 ⇔ p ≥ 0.6
```

→ Wenn weniger als 60% Sellers ehrlich sind, kein Trade.

### Wiederholtes Spiel

Wenn das Spiel mehrfach gespielt wird, kann opportunistischer Seller heute "ehrlich" handeln, um morgen wieder vertraut zu werden.

**Logik:** Verlust heute = -5 (10 statt 15). Gewinn morgen = 10 (statt 0). Wenn future-discount nicht zu hoch ⇒ "honor" optimal.

**Take-Away:** Repeated interaction → Trust möglich, auch bei opportunistischen Sellers.

### R&R als Substitute für Repeated Interaction

Plattform-Märkte sind oft *one-shot zwischen* spezifischen Buyer-Seller-Paaren. Aber R&R macht das Seller-Verhalten **sichtbar für ALLE zukünftigen Buyers**.

→ Der Seller hat Anreiz, sich zu disziplinieren, weil *sein heutiges Verhalten morgen für alle Buyers sichtbar ist*.

**Formal:** Es gibt keine repeated interaction mit demselben Buyer, aber repeated interaction mit dem **Markt**. Reputation = Repository der vergangenen Aktionen.

### Trust-Beispiele auf Plattformen

- **Ricardo.ch:** Profilbild + Vergangenheit + Reviews aus 12 Monaten + "405 positive, 0 negative" angezeigt
- **Airbnb:** Konfirmierte Identität (Email, Telefon, ID), Verifizierte Listings, 2-sided Reviews

### Adverse Selection und Moral Hazard auf Airbnb

R&R löst beide Probleme:
- **Adverse Selection:** Schlechte Wohnungen werden durch Reviews entlarvt → schlechte Hosts verlassen oder werden gemieden
- **Moral Hazard:** Hosts wissen, dass Verhalten gerated wird → strengen sich an

Aber auch *umgekehrt*: Hosts haben Adverse-Selection-/Moral-Hazard-Probleme mit Guests (Wohnung beschädigen). → **2-Sided Rating** (Airbnb).

---

## 4. Empirische Evidenz

### Chevalier & Mayzlin (2006): Reviews → Buchverkäufe

**Frage:** Beeinflussen Online-Reviews wirklich Sales? Oder ist die Korrelation nur Reflektion von echter Qualität?

**Identifikations-Strategie:** Vergleich derselben Bücher auf Amazon vs. Barnes & Noble.
- Wenn eine negative Review *nur* auf B&N gepostet wird (nicht Amazon), und B&N-Sales relativ sinken → Effekt ist kausal (Quality ist konstant)

**Result:** Verbesserung der Reviews auf einer Plattform → Erhöhung der relativen Sales dort. → **Reviews haben kausalen Einfluss.**

### Luca (2016): Yelp-Ratings → Restaurant-Revenues

**Identifikations-Trick:** Yelp **rundet** Ratings auf halbe Sterne.
- Restaurant mit 3.24 Stars → angezeigt als "3.0 Stars"
- Restaurant mit 3.25 Stars → angezeigt als "3.5 Stars"

Diese Restaurants sind *substantiv* fast identisch (Qualitäts-Difference 0.01), aber *angezeigt* unterschiedlich (Differenz 0.5 Stars).

→ Effekt der **Display** kann gemessen werden, ohne dass echte Qualität konfundiert.

**Results:**
- 1-Star-Increase → 5–9% Revenue-Increase
- **Nur für independente Restaurants**, nicht für Chains (Konsumenten kennen McDonald's bereits)
- **Reviews von "Elite"-Usern** haben fast doppelt so viel Effekt

**Interpretation:** Reviews matter, wo asymmetric information real ist (independent restaurants); Reviews matter weniger, wo Info schon verbreitet ist (chains).

### Resnick et al. (2006): Reputation → Willingness-to-Pay

**Experiment auf eBay:**
- Verkaufte identische Postcards entweder unter einem Account mit guter Reputation oder einem Newcomer-Account
- Random assignment zwischen den Accounts

**Result:** High-Rep-Seller bekam **8% mehr Preis** für dasselbe Produkt.

→ Reputation ist ökonomisch wertvoll. User zahlen Premium für Vertrauen, auch bei homogenem Produkt.

---

## 5. Challenges von R&R

### Selection Bias in Reviews

Wer reviewt? **Nicht alle.** Tendentiell:
- Extrem zufriedene oder unzufriedene User
- "Elite"-User (Yelp)
- Spezifische Demographien

→ Reviews sind keine repräsentative Stichprobe → Average kann verzerrt sein.

### Strategisches Verhalten

**Fake Reviews:**
- Sellers kaufen positive Reviews
- Konkurrenten schreiben negative Reviews

**Erpressung:**
- "Gib mir Discount, sonst gibt's 1-Stern" — besonders bei Restaurants und Hotels

**Plattform-Counter:**
- Algorithmus erkennt Fake-Patterns
- Verified-Purchase-Badges
- Elite-Reviewer-Programme

### Reciprocity (Airbnb-Problem)

In 2-sided Rating-Systemen (Airbnb) sehen sich Host und Guest gegenseitig.
- Wenn ich dich kritisiere, wirst du mich kritisieren
- → Inflation: alle bekommen 4.8-4.9 Stars
- → Information-Wert schrumpft

**Airbnb-Lösung:** Blind-Reviews (Reviews werden simultan released, nachdem beide Seiten gerated haben).

### Truthfulness Incentives

R&R-Systeme funktionieren nur, wenn Reviews **wahrhaftig** sind. Plattformen müssen:
- Anreize geben, ehrlich zu sein (z.B. Reputation der Reviewer selbst)
- Falsche Reviews bestrafen
- Aggregations-Algorithmen robust gegen Manipulation gestalten

### Informativeness vs. Volume

Eine 5-Stern-Bewertung mit 2 Reviews ist anders als mit 200.

**Display-Design-Wahl:**
- Average + Total Number (z.B. "4.5 stars, 1,234 reviews")
- Confidence Intervals (selten)
- Sortierung nach Helpfulness

Volume = Vertrauen ins Aggregat. Aggregierende Plattformen müssen das visualisieren.

---

## Klausur-Relevante Punkte

1. **Erkläre adverse selection vs. moral hazard** und wie R&R beide adressiert
2. **Diskutiere die WGNE/CGNE durch R&R** — selbstverstärkender Mechanismus
3. **Trust-Game-Logik:** Warum funktioniert Reputation auch im One-Shot-Setting?
4. **Empirische Studien:** Chevalier-Mayzlin, Luca, Resnick — was haben sie *identifiziert* und wie?
5. **3+ Challenges** und Counter-Strategien

## Verwandt

- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Block 6
- [[20.studies/Organizational-Economics/identifikationsstrategien]] — Methoden, die Luca etc. nutzen
- [[20.studies/Organizational-Economics/section4-pricing-disintermediation]]
- [[20.studies/Organizational-Economics/Hub]]
