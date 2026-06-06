---
created: 2026-06-06
type: section-deep-dive
source: ME 3 Aguiar VL Section 4 + Exercise Set 4
tags: [organizational-economics, section4, pricing, lerner, disintermediation]
status: master
---

# Section 4 — Platform Pricing & Disintermediation

> **Big Picture:** Pricing auf etablierten Plattformen ist *fundamentally* anders als Standard-Monopol-Pricing. Wegen Cross-Group-Effekten ist die Price-Structure non-neutral, oft asymmetrisch, manchmal mit negativen Preisen. Außerdem: Wie bekämpft man Disintermediation (= User, die die Plattform umgehen)?

---

## Roadmap

1. Pricing-Instrumente: Membership vs. Transaction
2. Same-Side Differential Pricing (Freemium, Prominence)
3. Two-Sided Transaction Pricing (Set 4.1)
4. Two-Sided Membership Pricing (Set 4.2–4.4)
5. Lerner-Index für Plattformen
6. Disintermediation und Counter-Strategien

---

## 1. Die zwei Preis-Instrumente

### Membership/Subscription Fees

> Regulieren **Access** zur Plattform. User zahlen wiederkehrend, unabhängig von Nutzung.

**Wann sinnvoll?**
- Wenn der typische User viele Transaktionen macht (Trxn-Tracking aufwändig)
- Wenn Trxns schwer zu monitoren sind
- Wenn die Plattform Lock-In wünscht

**Beispiele:**
- Netflix-Subscription (monatlich)
- eBay-Listing-Fees
- LinkedIn-Premium

**Hauptchallenges:**
- Plattform muss genug Stand-Alone-Wert bieten, damit man die monatliche Fee rechtfertigt
- Verschärft das Chicken-and-Egg-Problem (User muss vorausbezahlen, bevor er weiß, ob andere da sein werden)

### Usage/Transaction Fees

> Regulieren **Activity** auf der Plattform. User zahlen pro Transaktion (fix oder als Anteil).

**Wann sinnvoll?**
- Wenn Trxns leicht beobachtbar/monitorbar sind
- Wenn Trxns relativ unfrequent aber hochwertig sind
- Wenn man Wert proportional zur Aktivität abschöpfen will

**Beispiele:**
- Airbnb (Host gibt Share an Plattform ab)
- Uber-Provision pro Ride
- App Store (30% Commission)

**Hauptchallenges:**
- Disintermediation-Anreiz (Trxn-Fee = Anreiz, Plattform zu umgehen)
- Erfordert gute Trxn-Verifikation

### Oft kombiniert

eBay charges Sellers sowohl Listing Fees (Membership-like) als auch Final Value Fees (Transaction-like). So entstehen mehrere Pricing-Hebel.

---

## 2. Same-Side Differential Pricing

Plattformen bieten *innerhalb derselben Gruppe* Preis-Menüs, um Selbst-Selektion zu fördern.

### Selling Prominence

Sellers können extra zahlen, um in Suchergebnissen oben zu erscheinen.

**Beispiele:**
- eBay: bezahlte Listing-Verbesserungen
- Ricardo.ch: bezahlte Prominenz
- Babysitter-Plattformen: prominent Listing

**Logik:** Sellers mit höherem erwartetem Trxn-Value zahlen mehr für Sichtbarkeit — gut für Plattform-Profit *und* User-Matching.

### Freemium-Strategie

Free-Basis-Version + Premium-Bezahl-Version (z.B. Spotify Free vs. Premium).

**Logik:**
- Free attrahiert **Critical Mass** (lower barrier)
- Positive WGNE: Free-User generieren indirekt Wert (Network-Größe, Daten, Word-of-Mouth)
- Premium konvertiert die wertvollsten Free-User

**Challenge:** Richtige Balance zwischen Free-Features (genug Wert, um zu attractionen) und Premium-Features (genug Differenzierung, um zu konvertieren).

---

## 3. Two-Sided Transaction Pricing (Set 4.1)

### Setup

Monopoly-Plattform. N_b Buyers, N_s Sellers. Transaction Fees `a_b, a_s` pro Trxn.

```
u_b = (V_b − a_b)·n_s     (jeder Buyer macht Trxn mit jedem Seller)
u_s^i = (V_s^i − a_s)·n_b  (Seller i, mit i-spezifischer Bewertung)
π = (a_b + a_s)·n_b·n_s
```

### Der "Short-Sighted" Approach (Fehler)

Setze `a_b` so hoch, dass alle Buyer noch joinen (extract full surplus): `a_b* = V_b = 6`.

Dann setze `a_s` optimal *für die Seller-Seite*:
```
| a_s | n_s | π_s |
| 3   | 1   | 18  |
| 2   | 2   | 24  ← max für die Seite
| 1   | 3   | 18  |
```

→ `(a_b, a_s) = (6, 2)`, Profit = 96. **Aber nicht optimal!**

### Der Right Approach — Cross-Group beachten!

Wenn du `a_s` reduzierst:
- ↓ Profit pro Seller-Trxn
- ↑ n_s (mehr Sellers joinen)
- ↑ Buyer-Side-Profit: `π_b = a_b·n_b·n_s` wächst mit n_s
- → Mehr Transaktionen insgesamt

Tabelliere alle Optionen mit `a_b = 6` fix:
```
| a_s | n_s | π_s | π_b | π_total |
| 3   | 1   | 18  | 36  | 54      |
| 2   | 2   | 24  | 72  | 96      |
| 1   | 3   | 18  | 108 | 126     |
| 0   | 4   | 0   | 144 | 144     |
| -1  | 5   | -30 | 180 | 150 ←   |
| -2  | 6   | -72 | 216 | 144     |
```

→ Optimal: `(a_b, a_s) = (6, -1)`. **Sellers werden subventioniert!**

### Take-Away: Price Structure Not Neutral

In Standard-Markt: Steuer auf Buyer oder Seller → ökonomisch egal (nur Inzidenz verschiebt sich).

In Two-Sided-Markt: **Niemals** egal. Die *Aufteilung* `(a_b, a_s)` bestimmt das Equilibrium, nicht nur die Summe `a_b + a_s`.

---

## 4. Two-Sided Membership Pricing (Set 4.2)

### Setup

```
u_b = r_b + β_b·n_s − P_b − τ_b,   τ_b ~ U[0,1]
u_s = r_s + β_s·n_b − P_s − τ_s,   τ_s ~ U[0,1]
β_b·β_s < 1  (NE nicht zu stark)
```

### Schritt-für-Schritt

**1. Indifferent Users:**
```
τ̂_b = r_b + β_b·n_s − P_b   →   n_b = τ̂_b
τ̂_s = r_s + β_s·n_b − P_s   →   n_s = τ̂_s
```

**2. System (Substitution):**
```
n_b = [(r_b − P_b) + β_b(r_s − P_s)] / (1 − β_b·β_s)
n_s = [(r_s − P_s) + β_s(r_b − P_b)] / (1 − β_b·β_s)
```

**Comparative Statics:**
- `∂n_b/∂P_b < 0` (eigene Demand)
- `∂n_b/∂P_s < 0` (Cross-Demand — höherer Sellers-Preis vertreibt Sellers → reduziert auch Buyer-Demand)

**3. Profit-Maximierung:**
```
π = P_b·n_b + P_s·n_s
```
2 FOCs gleichzeitig → optimale Fees (siehe [[formelsammlung-cheatsheet]]).

### Wer zahlt weniger?

```
P_b* < P_s*   ⇔   (1 − β_s)·r_b < (1 − β_b)·r_s
```

**Spezialfall 1: r_b = r_s** (gleiche intrinsische Wertigkeit):
```
P_b* < P_s*   ⇔   β_s > β_b
```
→ Side mit größerer Attraction Power (β_s = Wirkung von Side _b_ auf Side _s_) zahlt MEHR.

Verbal: "Wenn Sellers Buyers stark wertschätzen, kann die Plattform sie melken."

**Spezialfall 2: β_b = β_s** (gleiche Network-Intensität):
```
P_b* < P_s*   ⇔   r_b < r_s
```
→ Side mit niedrigerem Stand-Alone-Wert zahlt weniger.

---

## 5. Lerner-Index für Plattformen

### Klassischer Lerner für Monopol

Für ein Single-Product-Monopol:
```
(p − c)/p = 1/η
```
- Hohe Elastizität (η groß) → niedriger Markup
- Markup = "wie viel über Marginal-Cost"

### Plattform-Lerner mit NE

Für two-sided Membership-Pricing:
```
P_s = c_s − β_b·n_b + N_s(u_s)/N_s'(u_s)
P_b = c_b − β_s·n_s + N_b(u_b)/N_b'(u_b)
```

Drei Terme:
1. `c_k` = direkte Cost-Comp
2. `−β_(−k)·n_(−k)` = **Network-Effekt-Adjustment** (Subtraktion — als ob effektive Cost niedriger wäre)
3. `N_k/N_k'` = Inverse-Elastizität-Adjustment

### Verbal-Erklärung

Wenn ich einen Seller attraktiere (höheres n_s), bekomme ich nicht nur P_s, sondern auch erhöhte Buyer-Demand → erhöhter Buyer-Profit. **Diese Cross-Group-Externalität reduziert den effektiven Marginal-Cost** der Seller-Akquise.

→ Plattform "behandelt" das Cross-Group-Network-Benefit als negative Cost → niedrigere Preise als ein Standard-Monopolist setzen würde.

### Take-Away

> **Price tends to be lower on the side where:**
> - User sensitivity to price is **higher** (elastische Demand, η groß)
> - The cross-group network effect *generated* by that side is **larger** (β groß)

**Reale Beispiele:**

| Plattform | Money Side | Subsidy Side |
|---|---|---|
| Nightclub | Männer | Frauen (frei) |
| Shopping Mall | Stores (rent) | Shopper (frei + Parking) |
| Kreditkarte | Händler | Konsumenten (cashback) |
| Magazine | Werber | Leser (under cost) |
| Yellow Pages | Businesses | Konsumenten (frei) |

Erkennst du das Pattern? **Die Seite mit höherer Attraction Power zahlt mehr; die Seite, die schwer zu attractionen ist, wird subventioniert.**

---

## 6. Platform Disintermediation (Leakage)

### Definition

> Plattform-Disintermediation (oder Leakage) passiert, wenn Agenten sich auf der Plattform treffen, aber die Transaktion **off-platform** durchführen — um die Trxn-Fee zu sparen.

### Beispiele

- **Glints/ZipRecruiter:** Employer findet Kandidat → Hires direkt off-platform (umgeht Vermittlungs-Fee)
- **Babysitter-Plattformen:** Familie und Babysitter bauen Vertrauen → spätere Buchungen direkt
- **Booking.com:** User findet Hotel → ruft Hotel direkt an (manchmal billiger)

### Was treibt Leakage?

**1. Wert der Transaktion**
Hochwertige Trxns → hohe absolute Fees → starker Anreiz zu umgehen.
*Job-Matching > einmaliges Reinigung*

**2. Was sucht der User?**
- **Diskovery vieler Counterparts** (z.B. Uber: jedes Mal ein neuer Fahrer) → Plattform unverzichtbar → wenig Leakage
- **Repeated Trxn mit derselben Person** (z.B. Babysitter, Handwerker) → Trust kann aufgebaut werden → hohes Leakage-Risiko

**3. Kommunikation vor Trxn nötig?**
- **Wenig Komm. nötig** (Uber-Ride, eBay-Standard-Produkte) → Trxn auf Plattform leicht
- **Viel Komm. nötig** (Home-Repair, Dating) → User tauschen Kontaktdaten → Leakage einfach

**4. In-person oder online?**
- **In-person Trxn** → Trust-Aufbau, Zahlungs-Koordination off-platform leicht (TaskRabbit)
- **Online Trxn** → Plattform kann monitoren (Fiverr)

**5. Kann Plattform Value-Add bieten?**
- **Booking.com vs. Airbnb:** Hotels sind etablierte Institutionen → wenig Trust-Problem → wenig Plattform-Value-Add → leicht zu disintermediaten
- **Airbnb:** Hosts sind Privatpersonen → Insurance + Reviews adden Wert → schwerer zu disintermediaten

### Counter-Strategien

**1. Pricing-Modell anpassen**
Trxn-Fees abschaffen, andere Modelle nutzen:
- **Lead-Fees** (Thumbtack): Service-Provider zahlt für jeden Lead (Anfrage), nicht für die Trxn
- **Membership** (Tinder, ZipRecruiter): Subscription statt pro Match
- **Listing-Fees** (eBay): Pay-to-be-Listed

**2. Pipeline-Modell**
Plattform übernimmt die Trxn selbst — wird zum Service-Anbieter.
- **Hello Alfred:** Hat eigene "Alfreds" (Mitarbeiter), nicht freie Worker
- **Batmaid:** Hat angestellte Reinigungskräfte

→ Trade-off: Mehr Kontrolle, aber höhere Fix-Costs und weniger Skalierung.

**3. Karotten — Value für On-Platform bieten**

Reduziere Friktionen und biete Bonus-Services, die nur on-Platform verfügbar sind:
- **Insurance** (Airbnb: Host-Guarantee bei Schäden)
- **Dispute Resolution** (eBay-Buyer-Protection)
- **Coaching/Tracking** (Coachup, Stylebait)
- **Discounts oder bessere Sichtbarkeit** für On-Platform-Verhalten

**4. Stöcke — Off-Platform bestrafen**

Drohungen und Restrictions:
- **Banning** bei Off-Platform-Versuchen (Airbnb, eBay)
- **Kontaktdaten verbergen** (kein Telefonnummer-Austausch im Chat)
- **Email/Phone-Filter** (Airbnb scannt Messages für Off-Platform-Hinweise)

**Caveat:** Sticks führen oft zu User-Resentment und lösen das Problem nicht völlig — User finden Wege drumherum (z.B. Fotos von Telefonnummern statt Text).

---

## Klausur-Relevante Punkte

1. **Unterscheide** Membership vs. Transaction Fees und nenne je 2 Beispiele
2. **Erkläre warum Price Structure non-neutral ist** — mit Set 4.1-Beispiel (Tabelle)
3. **Wende den Lerner-Index mit NE-Adjustment an** — verbal erklären, warum P niedriger als bei Standard-Monopol
4. **Diskutiere die "Wer zahlt weniger?"-Bedingung** und gib reale Beispiele
5. **Beschreibe Disintermediation und 3+ Counter-Strategien**

## Verwandt

- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Block 5
- [[20.studies/Organizational-Economics/problem-set-recipes#SET 4 — Two-Sided Monopol, HETEROGENE User (Membership Pricing)|Problem Set 4 Rezept]]
- [[20.studies/Organizational-Economics/formelsammlung-cheatsheet#5. SET 4 — Two-Sided Monopol, Heterogene User|Formeln Set 4]]
- [[20.studies/Organizational-Economics/section3-launching-platforms]]
- [[20.studies/Organizational-Economics/section5-ratings-reviews]]
- [[20.studies/Organizational-Economics/Hub]]
