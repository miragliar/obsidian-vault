---
created: 2026-06-06
type: section-deep-dive
source: ME 3 Aguiar VL Section 3 + Exercise Set 3
tags: [organizational-economics, section3, launching, divide-and-conquer, seeding]
status: master
---

# Section 3 — Growing a Platform (Launch, Trust, Expansion)

> **Big Picture:** Plattformen scheitern an der Erwartung — niemand joined, weil niemand erwartet, dass jemand joined. Diese Sektion ist das **Strategie-Handbuch**: wie man die Erwartungs-Spirale dreht.

---

## Roadmap

1. The Chicken-and-Egg Problem
2. Divide-and-Conquer Pricing (formales Modell)
3. Seeding-Strategien
4. Trust unter anonymen Usern
5. Plattform-Expansion

---

## 1. The Chicken-and-Egg Problem

### Warum es bei Plattformen schlimmer ist

- **One-sided Platform** (Set 1, 2): Multiple Equilibria existieren, aber innerhalb *einer* Gruppe. User A entscheidet anhand der Erwartung über andere User in derselben Gruppe.
- **Two-sided Platform** (Set 3): Group A formt Erwartungen über *Group B*, deren Erwartungen wiederum von Group A abhängen. → Doppeltes Coordination-Problem.

### Konkret: Das Null-Equilibrium

> "Group A joined nur wenn Group B joined; Group B joined nur wenn Group A joined → niemand joined."

In Set 3 ist das die `(0, 0)`-Konfiguration. Sie ist *immer* ein Equilibrium, sobald die Plattform-Fees positiv genug sind, dass Stand-Alone-Wert allein nicht reicht.

### Beispiel: OpenTable

Vor OpenTable: Diners-Restaurants-Coordination war chaotisch (Anrufe, leere Tische, frustrierte Gäste). Die Plattform-Möglichkeit war klar — aber wer joined zuerst?

- Restaurants: "Warum sollen wir auf OpenTable sein, wenn keine Gäste dort suchen?"
- Gäste: "Warum sollen wir OpenTable benutzen, wenn keine Restaurants gelistet sind?"

→ OpenTable musste aktiv Restaurants ködern (subsidiert, anfangs gratis) bevor Gäste den Wert sehen konnten.

---

## 2. Divide-and-Conquer (formales Modell)

### Setup

Eine Plattform, zwei Sides (b = Buyer, s = Seller), N_b und N_s identische User. CGNE: γ_b (Wirkung auf b) und γ_s (Wirkung auf s).

Utility:
```
u_b = r_b + γ_b·n_s − P_b
u_s = r_s + γ_s·n_b − P_s
```

Outside Options u_b^0, u_s^0. Marginal Costs c_b, c_s.

### 4 Equilibrium-Konfigurationen

Weil alle User auf einer Side identisch sind und gemeinsame Outside Option haben, entscheiden alle gleich. → Nur 4 Configs möglich:

1. `(N_b, N_s)` — alle joinen
2. `(0, 0)` — niemand joined
3. `(N_b, 0)` — nur Buyers joinen
4. `(0, N_s)` — nur Sellers joinen

(Configurations 3 und 4 sind selten Equilibria, weil eine Seite alleine wenig Wert hat.)

### Bedingungen für jedes Equilibrium

`(N_b, N_s)` ist Equilibrium iff:
```
P_b ≤ r_b − u_b^0 + γ_b·N_s     UND     P_s ≤ r_s − u_s^0 + γ_s·N_b
```

`(0, 0)` ist Equilibrium iff:
```
P_b > r_b − u_b^0                UND     P_s > r_s − u_s^0
```

### Die kritische Überlappung

Wenn beide Bedingungs-Paare *gleichzeitig* erfüllt sind:
```
r_b − u_b^0 < P_b ≤ r_b − u_b^0 + γ_b·N_s
r_s − u_s^0 < P_s ≤ r_s − u_s^0 + γ_s·N_b
```

→ **Sowohl** `(N_b, N_s)` **als auch** `(0, 0)` sind Equilibria. Die Plattform sitzt in der "Grauzone" — Outcome hängt rein an User-Erwartungen.

### Divide-and-Conquer-Lösung

**Idee:** Eliminiere `(0, 0)` als Equilibrium.

**Variante A: "Subsidize Buyers, Conquer Sellers":**
```
P_b = r_b − u_b^0   (oder leicht darunter)
P_s = r_s − u_s^0 + γ_s·N_b
```

→ Bei diesem `P_b` joinen Buyers *garantiert* (Utility ≥ Outside Option auch ohne Sellers). Sellers wissen das, joinen auch.

**Variante B: "Subsidize Sellers, Conquer Buyers":**
```
P_s = r_s − u_s^0
P_b = r_b − u_b^0 + γ_b·N_s
```

### Welche Variante ist profitabler?

Profit-Vergleich:
```
π_(b) = N_b·(r_b − u_b^0 − c_b) + N_s·(r_s − u_s^0 + γ_s·N_b − c_s)     (subsidize b)
π_(s) = N_b·(r_b − u_b^0 + γ_b·N_s − c_b) + N_s·(r_s − u_s^0 − c_s)     (subsidize s)
```

Differenz:
```
π_(b) − π_(s) = N_b·N_s·(γ_s − γ_b)
```

**Subsidize-Regel:**
```
π_(b) > π_(s)   ⇔   γ_s > γ_b   (=Seller-Attraction-Power größer)
                ⇔   subsidiere Buyers, monetarisiere Sellers
```

**Verbal-Eselsbrücke:** *"Subsidiere die Magnet-Seite; verdiene an der angezogenen Seite."*

(Vorsicht beim Index — γ_s misst die Wirkung von Side b *auf* s. Wenn γ_s groß: Sellers sind leicht zu attractieren *gegeben* Buyer-Präsenz → daher: Buyer sind die "Magneten", die man subsidieren sollte.)

### Wann werden Preise negativ?

Wenn `r_k < u_k^0` (Outside Option besser als Stand-Alone-Wert der Plattform):
```
P_k* = r_k − u_k^0 < 0
```
→ Plattform **zahlt** User zum Joinen.

**Beispiel: Uber-Fahrer.** Klassische Outside-Option (Job, Taxi-Genossenschaft) hatte hohen Wert → Uber zahlte Garantielöhne in den ersten Monaten. Verluste auf Fahrer-Seite, kompensiert durch Profit auf Rider-Seite.

### Profitabilitätsbedingung

D&C ist nur sinnvoll, wenn am Ende `max{π_(b), π_(s)} > 0`:
```
max{γ_b, γ_s} > (u_b^0 − r_b + c_b)/N_s + (u_s^0 − r_s + c_s)/N_b
```

**Verbal:** D&C lohnt sich, wenn mindestens eine Seite **stark genug** Cross-Group-Effekte erzeugt, um die Subvention zu rechtfertigen.

**Was die Bedingung **erleichtert**:**
- ↑ NE (γ_b, γ_s)
- ↑ Markt-Größe (N_b, N_s)
- ↑ Intrinsischer Wert (r_b, r_s)
- ↓ Outside Options
- ↓ Marginal Costs

### Praktisches Beispiel — Microsoft Xbox

Microsoft musste Game-Entwickler überzeugen, dass es genug Xbox-User geben würde, damit Spiele rentabel sind.

- **Strategie:** Xbox unter Cost verkauft, $4 Milliarden Verlust geschluckt
- **Logik:** "Wir bauen die Userbase auf, Game-Entwickler folgen, dann verdienen wir am Game-Royalty"
- **Result:** Funktionierte — Xbox wurde dominante Plattform

### D&C-Voraussetzungen

D&C funktioniert nur wenn:
1. **Beobachtbar:** Die andere Seite muss die Subvention sehen können (sonst keine Erwartungs-Veränderung)
2. **Deep Pockets:** Anfangsverluste finanzierbar — VC oder Mutterfirma als Backup
3. **Verbindlichkeit:** Subvention muss als dauerhaft (nicht nur Promo) wahrgenommen werden

---

## 3. Seeding-Strategien (Alternative/Komplement zu D&C)

D&C ist eine **statische** Pricing-Strategie. In Realität wachsen Plattformen **dynamisch** — du fängst klein an, baust Critical Mass auf.

### Marquee-Strategie

> Ziel die **Marquee Users** — bekannte Personen/Firmen, die per se große CGNE erzeugen.

**Beispiele:**
- **Spotify ↔ Joe Rogan:** Spotify zahlte $100M+ für Exklusiv-Deal mit Rogan, weil Rogan-Fans für Spotify subscribed
- **Videospiele-Konsolen ↔ FIFA, COD:** Wenn die Top-Spiele auf der Konsole sind, kommen die User
- **Twitter ↔ Obama, Promis:** Marquee-User legitimieren die Plattform

**Caveat:** Marquee-User sind teuer, weil auch konkurrierende Plattformen sie wollen.

### Within-Group-NE ausnutzen

Wenn eine User-Gruppe **positive WGNE** hat (z.B. Spieler spielen lieber mit anderen Spielern), wächst diese Gruppe von selbst, sobald die Plattform sie attrahiert.

→ **Beginne bei der Gruppe mit positiven WGNE**, lass sie snowballen, dann attraktiere die zweite Gruppe.

### Stand-Alone Value bieten

Manche User joinen nicht wegen Network-Effekten, sondern weil das Produkt für sich alleine schon nützlich ist.

**Beispiele:**
- **VCR (1980er):** Recording-Funktion war Wert an sich, *unabhängig* von Cassetten-Auswahl. Erst nachdem Recorder verbreitet waren, kamen kommerzielle Tapes.
- **PlayStation 2:** War billigster DVD-Player am Markt → Leute kauften ihn als DVD-Player, dann gingen sie zu Games über
- **Airbnb anfangs:** Vermieter hatten "echte" Räume und Hosts wollten Side-Income — Plattform diente als Bonus, nicht Hauptfunktion

### Niche-Markt-Fokus

Statt für die ganze Welt zu launchen, fokussiere auf eine enge Gruppe wo Critical Mass leicht zu erreichen ist.

**Beispiele:**
- **Yelp:** Started mit ethnischem Essen in San Francisco — dedizierte "Foodies" als Early Adopter
- **Facebook:** Started in Harvard only — Ivy-League dann erst alle Universities
- **Tinder:** Started in US-College-Campuses

→ Critical-Mass-Engineering. Wachstum kommt durch geografische/demographische Expansion.

### Attract Users Fleeing Existing Platform

Wenn eine etablierte Plattform **negative Network Effects** hat (Congestion, toxische Inhalte), kann eine neue Plattform User abziehen.

**Beispiele:**
- **Etsy → Alternativen:** Etsy wurde "Amazon-ifiziert" mit Bulk-Vendors → handgemachte Verkäufer (Etsy's USP) wanderten zu Alternativen
- **X (Twitter) → Bluesky:** Musk's Übernahme + toxischer Content → viele User wechselten zu Bluesky (besonders nach US-Wahlen 2024)

### Piggyback-Strategie

> Statt eigene Netzwerk aufzubauen, **nutze ein bestehendes**.

**Beispiele:**
- **PayPal auf eBay:** PayPal nutzte Bots, um auf eBay zu kaufen/verkaufen und PayPal als Zahlungsmittel zu erzwingen → wurde Standard
- **Airbnb auf Craigslist:** Airbnb-Hosts konnten Listing automatisch zu Craigslist crossposten — nutzten Craigslist-Traffic, bis sie selber genug User hatten

**Risiko:** Wenn die Host-Plattform die Praxis stoppt (Craigslist hat es eventuell verboten), bist du ohne Backup.

### Boost Expectations

Erwartungen direkt manipulieren — durch Marketing, PR, oder unethische Tricks.

**Beispiele:**
- **Reddit:** Co-Founder posteten fake Profile mit fake Content in der Frühphase → echte User dachten, da sei schon Aktivität → jointen
- **GrubHub:** Listete 150.000 Restaurants ungefragt — Plattform sah voll und etabliert aus, auch wenn die Restaurants nichts wussten
- **Dating-Apps:** Manche kaufen Profile aus Datenbroker-Quellen und präsentieren sie als organische User

**Risiko:** Vertrauen kann beschädigt werden, wenn der Trick auffliegt.

### Start as Pipeline

Erst klassisches Reseller-Modell, dann zur Plattform öffnen.

**Beispiele:**
- **Amazon:** Started als Book-Reseller → 2001 Amazon Marketplace eröffnet für Third-Party-Sellers
- **Videogame-Konsolen:** Konsolen-Hersteller produzierten anfangs ihre eigenen Games → später öffneten sie für externe Entwickler

→ Pipeline gibt dir eine etablierte User-Basis; Plattform-Öffnung kommt später.

### Diese Strategien sind nicht exklusiv!

Beispiel **Encore** (Plattform für Event-Musiker-Booking):
1. Startete als "LinkedIn for Musicians" (Networking-Tool für Musiker) → attraktierte Supply Side via Within-Group-NE
2. Öffnete für Konsumenten, **boostete Expectations** durch "vorgespiegelte" Verfügbarkeit
3. Tappte in Facebook-Groups für Musiker, um Anfragen schnell zu matchen → **Piggyback**

---

## 4. Trust und Building Reputation

(Brücke zu Section 5 — wird dort ausführlicher.)

### Das Trust-Problem

Plattformen vermitteln zwischen Anonymen. Klassische Trust-Mechanismen (repeated interaction, persönliche Kenntnis) fehlen.

### Reputations-Lösung

Plattformen ersetzen "repeated interaction zwischen demselben Buyer und Seller" durch "repeated interaction des Sellers mit DEM MARKT". Selbst wenn ich dich nie wiedersehe, sieht der nächste Buyer deine Reviews.

→ **Reputation** disziplinarisiert auch im One-Shot-Setting.

### Plattform-Design-Wahl

Eine Plattform muss entscheiden:
- 1-sided oder 2-sided Reviews? (Airbnb ist 2-sided)
- Wer kann reviewen? (Verified vs. anonymous)
- Wie aggregiert? (Rohe Sterne vs. gewichtet, mit Elite-Status etc.)
- Wie sichtbar? (Detail vs. Average)

---

## 5. Plattform-Expansion

Nach erfolgreichem Launch erweitern Plattformen oft, indem sie:

1. **Geografisch expandieren** (Uber: SF → ganzer USA → weltweit)
2. **Neue Sides hinzufügen** (Amazon Marketplace zu Reseller-Amazon)
3. **Eigene Produkte anbieten** (Amazon Basics, Spotify-Eigenproduktion)
4. **Adjacent Markets erschließen** (Facebook → Instagram → WhatsApp)

### Konflikt: Plattform vs. eigene Sellers

Wenn Amazon eigene Produkte verkauft, konkurriert sie mit den Sellers auf ihrer Plattform. Das hat:

- **Vorteile** für Plattform: höhere Margen, bessere Datennutzung
- **Nachteile:** Sellers vertrauen weniger → Disintermediation, EU-Antitrust

---

## Klausur-Relevante Punkte

1. **Definiere chicken-and-egg-problem** und warum es bei 2-sided platforms schlimmer ist als bei 1-sided
2. **Beschreibe die 4 Equilibrium-Configs** in Set 3 und identifiziere die Trap-Region
3. **Wende die D&C-Subsidy-Regel an:** Welche Seite subventionieren? (γ-Vergleich!)
4. **Erkläre, wann Preise negativ werden** und gib praktisches Beispiel (Uber)
5. **Nenne mindestens 4 Seeding-Strategien** und bringe Beispiele

## Verwandt

- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Block 4
- [[20.studies/Organizational-Economics/problem-set-recipes#SET 3 — Two-Sided Monopol, IDENTISCHE User (Divide-and-Conquer)|Problem Set 3 Rezept]]
- [[20.studies/Organizational-Economics/formelsammlung-cheatsheet#4. SET 3 — Two-Sided Monopol, Identische User|Formeln Set 3]]
- [[20.studies/Organizational-Economics/section4-pricing-disintermediation]]
- [[20.studies/Organizational-Economics/Hub]]
