---
created: 2026-06-06
type: intuition-guide
source: ME 3 Aguiar VL + own synthesis
tags: [organizational-economics, intuitionen, mechanismen, klausur-vorbereitung]
status: master
---

# Intuitionen und Mechanismen — die Story hinter den Formeln

> **Warum dieser Guide?** In der Klausur bist du nicht verloren, wenn du eine Formel vergessen hast — sondern wenn du die *Story* vergessen hast. Die Mathematik ist nur die Buchhaltung. Hier steht, was *wirklich* passiert.

---

## Die GROSSE Frage des Kurses

> **Wie unterscheiden sich Plattformen von "normalen" Firmen, und welche Konsequenzen hat das für Strategie, Pricing, und Marktstruktur?**

Drei Antworten in einem Satz:

1. **Plattformen managen Network Effects aktiv** — sie verkaufen nicht ein Produkt, sondern *vermitteln Interaktionen*.
2. **Demand ist interdependent und expectationsbasiert** — die User entscheiden, *abhängig davon, was andere User entscheiden*. → Multiple Equilibria, Tipping, Coordination-Probleme.
3. **Pricing ist asymmetrisch** — Plattformen subventionieren oft eine Seite, um auf der anderen zu verdienen. Der Lerner-Index reicht nicht.

---

## Block 1 — Was ist eine Plattform? (Section 1)

### Die UZH-Definition (auswendig lernen)

> Eine Plattform ist eine **Entität, die ökonomische Agenten zusammenbringt UND Netzwerk­effekte zwischen ihnen aktiv managt**.

**Zwei Bedingungen, beide notwendig:**

1. Network Effects existieren zwischen den Agenten
2. Die Entität managt sie aktiv (Pricing, Rating, Algorithm, Moderation)

**Klassifikations-Beispiele:**

| Entität | Plattform? | Warum? |
|---|---|---|
| Uber | ✅ Ja | Match + Pricing + Rating |
| Wikipedia | ✅ Ja | Aktive Moderation, Reader-Writer-Interaktion |
| Amazon Marketplace | ✅ Ja | Match + Reviews |
| Amazon (Reseller) | ❌ Nein initial, jetzt teils | Pure Reseller hat keine NE-Verwaltung |
| Supermarkt | ❌ Nein | Bringt zusammen, managt keine NE |
| Esperanto | ❌ Nein | NE existieren, aber keine Entity managt sie |
| Netflix | ✅ Eingeschränkt | One-sided platform mit WGNE via Recommendation |

### Network Effects — die 4 Kategorien

|             | Innerhalb Gruppe (WGNE) | Zwischen Gruppen (CGNE) |
|-------------|-------------------------|--------------------------|
| **Positiv** | Telefon, WhatsApp, Wikipedia | Uber (Fahrer ↔ Rider) |
| **Negativ** | Online-Poker (Profis), Stau auf Waze | Werbung (Advertiser → User) |

**Die häufigste Verwechslung:** *Uber-Fahrer auf Uber-Fahrer = WGNE (negativ)*, nicht CGNE! Die Fahrer sind in derselben Gruppe; mehr Fahrer = mehr Konkurrenz = schlechter für jeden Fahrer.

### Direkte vs. Indirekte Network Effects

- **Direkter NE = Within-Group:** Du profitierst direkt davon, dass andere User in *deiner* Gruppe joinen
- **Indirekter NE = Cross-Group-Kombination:** Du profitierst indirekt, weil mehr User in Gruppe A → mehr in Gruppe B → was indirekt dir (in A) hilft

**Beispiel:** Mehr Airbnb-Guests → mehr Hosts → mehr Auswahl für alle Guests (indirekter positiver Effekt auf Guests).

### Die 3 CGNE-Situationen

1. **Attraction Spiral** (beide positiv): Marktplätze (eBay), Matching (Tinder) → schnelle Plattform-Wachstum möglich
2. **Attraction/Repulsion Pendulum** (eine Richtung positiv, andere negativ): Media (User ⇄ Advertiser) — schwer zu balancieren
3. **Attraction Spillover** (eine Richtung positiv, andere null): Pros & Amateure auf Foren — Pros profitieren nicht von Amateuren

### Plattform-Typologie nach Wertschöpfung

| Wie wird Wert geschaffen? | Wie wird er extrahiert? |
|---|---|
| Cross-Group NE | Charge users (Uber, Airbnb) ODER bundle bads (YouTube ads) |
| Within-Group NE | Charge users (Spotify Premium, Netflix) ODER ads (Facebook) |
| Stand-Alone | Pure ads (New York Times, klassische Zeitung) — keine echte Plattform |

---

## Block 2 — Demand für Network Goods (Section 2 Part 1)

### Das Kernrätsel

> Wenn der Wert für mich davon abhängt, wer noch joined — und der Wert für den anderen davon abhängt, ob ich joine — *wie weiß ich, ob ich joinen soll?*

Antwort: Du **bildest Erwartungen** über andere. Wenn diese Erwartungen sich gegenseitig stützen, hast du ein **Fulfilled Expectations Equilibrium (FEE)**.

### Was FEE wirklich heißt

`n^e = n` ist keine reine Notation. Es bedeutet: "Was alle erwarten, wird auch eintreten."

Drei mögliche FEE können koexistieren:
- **n = 0:** Niemand erwartet, dass jemand joined → niemand joined → Erwartung erfüllt
- **n = 1:** Alle erwarten, dass alle joinen → alle joinen → Erwartung erfüllt
- **n = n***: Manche joinen (kritische Masse), Erwartung erfüllt

Das **null-Equilibrium** ist die zentrale Falle: Selbst wenn alle besser dran wären, wenn sie joinen — wenn niemand das *glaubt*, joined niemand.

### Selbst­erfüllende Prophezeiung — das Schlüsselkonzept

> "Wenn alle erwarten, dass Plattform X erfolgreich wird, wird sie erfolgreich. Wenn alle das Gegenteil erwarten, scheitert sie."

**Beispiel:** Der Million Dollar Homepage (2005) — Alex Tew schaffte es, durch frühe Käufe von Familie/Freunden + Pressemitteilung die Erwartung zu setzen, dass die Seite "etabliert" sei. Das wurde self-fulfilling und brachte $1 Mio. ein. *Hätte er die initialen Käufer nicht generiert, wäre die Seite leer geblieben.*

### Critical Mass

In Strong-NE-Settings gibt es drei FEE: 0, kritische Masse n_S, und n_L. Die kritische Masse ist:

- **Unstable:** Genau darüber explodiert das Netzwerk; genau darunter kollabiert es
- **Schwelle für Erfolg:** Wenn die Plattform es schafft, n_S zu erreichen, wird sie zu n_L wachsen

**Praktische Implikation:** Frühe Strategien (Seeding, Marketing, Faking) sind nicht "Werbung", sondern **Critical-Mass-Erzeugung**.

### Warum upward-sloping Demand kein Witz ist (Set 1.2, Strong NE)

Bei `V < β` ist die FEE-Demand `n(p)` *steigend* in `p`. Klingt absurd — höhere Preise sollten doch Demand reduzieren?

**Auflösung:** Bei höherem `p` ist nur derjenige Konsument bereit zu kaufen, der eine starke Network-Vorliebe (θ groß) hat. *Wenn der erwartet, dass viele andere joinen*, kauft er trotz hohem Preis. Die Demand-Kurve trackt nicht "wie viel kaufst du bei p?", sondern "wie viel wird unter rationaler Erwartung gekauft?".

---

## Block 3 — Plattform-Wettbewerb (Section 2 Part 2)

### Inkompatible vs. Kompatible Networks

**Inkompatibel** (WhatsApp vs. Signal):
- NE sind **plattform-spezifisch**
- Outside Option = anderes Netzwerk → wird **endogen** (sinkt für Plattform A, wenn Plattform B wächst)
- → Attraction Loops verstärken sich → **Tendenz zum Tipping**

**Kompatibel** (Email-Anbieter):
- NE sind **global**
- Konkurrenz nur über Stand-Alone-Eigenschaften
- → Plattformen können **koexistieren**

### Hotelling — was es wirklich modelliert

Die Linie [0, 1] ist nicht "geografische Distanz". Sie ist die **Heterogenität der Präferenzen**: Manche User wollen viel Privacy (Position 1, prefer Signal), andere viel Convenience (Position 0, prefer WhatsApp).

Die Disutility `τ·x` ist die "Schmerz-Funktion" — wie viel verlierst du, wenn die Plattform nicht zu deinem idealen Punkt passt.

- **Größeres τ:** Plattformen sind **stärker differenziert** → Konsumenten kleben an "ihrer" Plattform → weniger Tipping
- **Größeres β:** Network Effects **dominieren** Differenzierung → Konsumenten wechseln zu größerer Plattform → mehr Tipping

### Die Tipping-Bedingung

```
Tippt der Markt? ⇔ β > τ AND q groß genug (z.B. q > 3(τ−β))
```

**Verbal:**
> Wenn Network Effects stark genug sind, dass sie die Differenzierungs-Friktionen überwinden, UND eine Plattform einen Qualitätsvorteil hat — dann gewinnt diese Plattform alles.

### Network Effects als endogene vertikale Differenzierung

Diese Einsicht ist Klausur-relevant:

`q` ist exogen-vertikal (Plattform 1 ist objektiv besser). `β·n_1` ist **endogen-vertikal** (Plattform 1 wird vertikal besser, weil sie mehr User attraktiert, weil sie mehr User attraktiert, ...).

→ Beim Pricing-Wettbewerb mit NE: **Mehr User zu gewinnen wird wertvoller als nur den Marginalprofit zu kassieren** → schärferer Preiswettbewerb → niedrigere Preise.

### Tipping ohne Tipping — wann koexistieren Plattformen?

| Faktor | Effekt |
|---|---|
| Stärkere NE (β) | + Concentration (mehr Tipping) |
| Skaleneffekte | + Concentration |
| Differenzierung (τ) | − Concentration |
| Multi-Homing | − Concentration |
| Congestion | − Concentration |

**Multi-Homing** ist real: Du nutzt sowohl Spotify als auch Apple Music. Dann sind NE nicht mehr exklusiv → Wettbewerb in market statt for market.

### Compatibility-Trade-off (Set 2.2 Teil 5)

Ein neuer Entrant (q > 0) muss entscheiden: kompatibel mit Legacy oder nicht?

**Zwei Effekte:**

1. **Willingness-to-pay Effekt** (immer positiv): Bei Compatibility ist die *common* Netzwerk-Größe größer → User zahlen mehr.
2. **Level-Playing-Field Effekt** (negativ wenn `q > τ−β`): Bei Compatibility verliert Entrant seinen NE-Vorteil → schadet ihm, wenn er sonst mehr User hätte.

**Ergebnis:** Entrant präferiert Compatibility *außer* wenn sein Qualitätsvorteil sehr groß ist (`q > q̂ = √(τ(τ−β))`).

**Praktisches Beispiel:** Tesla bei Charging — anfangs proprietär (sehr großer Qualitäts-/Network-Vorteil), jetzt teilweise kompatibel (CCS), weil der Markt reift.

---

## Block 4 — Two-Sided Plattformen launchen (Section 3)

### Das Chicken-and-Egg-Problem

> Group A joined nur wenn Group B joined. Group B joined nur wenn Group A joined. → Beide joinen nicht. → Null-Equilibrium.

**Mehr User-Gruppen = schlimmer.** Bei one-sided platforms gibt es WGNE; bei two-sided gibt es CGNE *plus* gegenseitige Erwartungen — ein doppeltes Coordination-Problem.

### Divide-and-Conquer (D&C) — das zentrale Pricing-Pattern

**Idee:** Eliminiere `(0, 0)` als Equilibrium, indem du EINE Seite so attraktiv machst, dass sie *garantiert* joined — auch ohne die andere.

**Mechanik:**
1. **Divide:** Setze für Side k einen so niedrigen Preis (`P_k = r_k − u_k^0`), dass User auf Side k *unabhängig* von der anderen Seite joinen
2. **Conquer:** Da Side k garantiert da ist, kann Side −k höhere Preise akzeptieren: `P_{−k} = r_{−k} − u_{−k}^0 + γ_{−k}·N_k`

### Welche Seite subsidieren? — die häufige Klausur-Falle

**Regel:** Subsidiere die Seite, die der anderen *nicht* viel bringt; monetarisiere die Seite, ohne die die andere nicht kommt.

**Formal:** `π_(b) > π_(s) ⇔ γ_s > γ_b` — der Index `γ_s` steht für "Effekt von Side _b_ **auf** Side _s_" (oder: wie sehr Side s von Side b angezogen wird).

**Verkehrt-vertretbare Eselsbrücke:** Schau, wer wen "stärker liebt":
- γ_s groß ⇒ Sellers lieben Buyers stark → Buyers sind die Magnet-Seite → **subsidiere Buyers**
- Sellers werden auch ohne Subvention kommen, weil sie ohnehin von Buyers angezogen sind → **monetarisiere Sellers**

### Negative Preise — wann ist das optimal?

`P_k* = r_k − u_k^0 < 0` wenn `r_k < u_k^0` (Outside Option besser als intrinsischer Wert).

**Uber-Beispiel:** Fahrer haben hohe Outside Option (klassischer Job, Taxi-Genossenschaft, eigenes Auto privat nutzen). Uber muss Garantielöhne zahlen → effektiv negativer Preis. Die Verluste auf Fahrer-Seite werden mit Rider-Profiten überkompensiert.

### Seeding-Strategien (Alternative/Komplement zu D&C)

Real-Welt-Strategien für den Plattform-Launch:

| Strategie | Idee | Beispiel |
|---|---|---|
| **Marquee** | Ziele *bekannte* User, die viele andere anziehen | Joe Rogan auf Spotify; Obama auf Twitter |
| **Within-Group NE** | Ziel Gruppe mit positivem WGNE — wächst von alleine | Videospiele (Spieler-Spieler-Interaktion) |
| **Stand-Alone Value** | Biete Wert auch ohne andere User | VCR (Recording-Funktion); PlayStation (DVD-Player) |
| **Niche Market** | Konzentriere auf eng definierte Gruppe | Yelp startete mit SF-Foodies; Facebook mit Harvard |
| **Fleeing Existing Platform** | Nutze negative NE auf etablierter Plattform | Bluesky vs. X; Etsy-Alternativen |
| **Piggyback** | Nutze bestehende Plattform als Bootstrapping | PayPal auf eBay; Airbnb auf Craigslist |
| **Boost Expectations** | Marketing/PR/Fake Profiles um Erwartungen zu schüren | Reddit (Fake-Accounts initial); GrubHub (ungenehmigte Listings) |
| **Start as Pipeline** | Erst eigene Produkte → später öffnen | Amazon → Marketplace; Konsolen → Third-party Games |

---

## Block 5 — Pricing auf etablierten Plattformen (Section 4)

### Zwei Preis-Instrumente

| Typ | Was reguliert es? | Wann nutzen? |
|---|---|---|
| **Membership Fee** | Access — wer ist auf der Plattform? | Wenn viele kleine Transaktionen oder Trxn-Tracking schwer |
| **Transaction Fee** | Activity — was passiert auf der Plattform? | Wenn Trxns gut beobachtbar und wertvoll |

**Tipp:** Sie können kombiniert werden (eBay = Listing-Fee + Final-Value-Fee).

### Why is the Price Structure Not Neutral?

In standard-Markt: Steuer auf Verkäufer oder Käufer? → ökonomisch egal, nur Inzidenz verschiebt sich.

In Two-Sided-Markt: **NICHT egal.** Die Aufteilung `(a_b, a_s)` bestimmt, wer joined → wie viele Transaktionen → Total Profit.

**Mechanik (Set 4.1):**

Senke `a_s` → mehr Sellers joinen → mehr Transaktionen → MEHR profit auf Buyer-Seite (auch wenn weniger pro Seller).

Optimum balanciert die zwei Effekte. *Kann* zu negativen Fees auf einer Seite führen.

### Asymmetric Pricing — der eigentliche Take-Away

> Price tends to be lower on the side where:
> - User Sensitivity to price is **higher** (elastische Demand)
> - Cross-Group Network Effect *generated* by that side is **larger** (große Attraktion-Power)

**Beispiele in der Realität:**

| Plattform | Subsidy Side | Money Side |
|---|---|---|
| Nightclub | Frauen (frei/discount) | Männer |
| Kreditkarten | Konsumenten (cashback) | Händler |
| Magazine | Leser (under cost) | Werbung |
| Yellow Pages | Konsumenten (free) | Businesses |
| Shopping Mall | Shopper (free parking) | Stores (rent) |

### Lerner-Index für Plattformen

Standard-Monopol:
```
(p − c)/p = 1/η     (höhere Elastizität → niedrigerer Markup)
```

Two-Sided:
```
(P_s − (c_s − β_b·n_b))/P_s = 1/η_s(P_s | n_b)
```

→ Der "effektive Marginal-Cost" ist `c_s − β_b·n_b`. Weil der Buyer-Side-Effekt eine "negative Kost" ist (Sellers attraktieren Buyers, was Plattform Geld bringt), markdown der Preis nach unten.

**Verbal:** Die Plattform behandelt User wie ein "kostbare Externalität" — sie zahlt (oder nimmt weniger), um sie zu haben.

### Disintermediation (Plattform-Leakage)

> User treffen sich auf Plattform, transaktieren aber direkt off-platform um Trxn-Fee zu sparen.

**Was triebt Leakage?**

1. **Wert der Transaktion** hoch (Jobs > Reinigung)
2. **Repeat-Beziehung** möglich (Babysitter > Uber-Fahrer)
3. **Trxn ist gut definierbar** ohne weitere Kommunikation
4. **Trxn ist in-person** (Trust-Aufbau)
5. **Plattform fügt wenig Value über Match hinaus** (Booking.com vs. Airbnb)

**Was kann Plattform tun?**

- **Karotte:** Versicherung (Airbnb), Dispute-Resolution, Coaching-Tools, Discounts für On-Platform-Trxns
- **Stock:** User-Banning bei Off-Platform-Versuchen (eBay, Airbnb)
- **Pricing-Modell ändern:** Lead-Fees (Thumbtack), Subscription (Tinder)
- **Pipeline werden:** Selber Service anbieten (Hello Alfred, Batmaid)

---

## Block 6 — Ratings & Reviews Systems (Section 5)

### Wozu brauchen Plattformen R&R?

Plattformen erlauben Transaktionen zwischen *anonymen Agenten*. Klassischer ökonomischer Mechanismus für Trust (repeated interaction) funktioniert nicht.

→ **Reputation** als institutioneller Ersatz: Vergangenes Verhalten wird sichtbar, daher heute incentive, gut zu handeln (auch wenn dieser Kunde nie wiederkommt).

### Adverse Selection vs. Moral Hazard

| Problem | Was es heißt | Wie R&R hilft |
|---|---|---|
| **Adverse Selection** | Unsicherheit über *Qualität* (hidden info) | Reviews → Low-Quality-Sellers werden gemieden/verlassen Plattform |
| **Moral Hazard** | Unsicherheit über *Anstrengung* (hidden action) | Reviews → Sellers haben Anreiz, sich anzustrengen |

### Network Effects in R&R-Systemen

R&R ist selbst eine Quelle von Network Effects:

- **WGNE auf Buyer-Seite:** Mehr Buyers → mehr Reviews → präzisere Average-Bewertungen → wertvoller für andere Buyers
- **CGNE Buyer → Seller:** Mehr Reviews → Low-Quality-Sellers gehen → bessere Auswahl für Buyers (Adverse Selection ↓)
- **CGNE Buyer → Seller (Behavior):** Sellers wissen, dass Verhalten getrackt → besseres Verhalten (Moral Hazard ↓)

→ R&R verstärkt Plattform-Power und macht erfolgreiche Plattformen noch erfolgreicher.

### Wann wirken Reviews kausal?

**Chevalier & Mayzlin (2006):** Vergleich von Book-Sales auf Amazon vs. Barnes&Noble. Wenn eine Plattform eine negative Review erhält und die andere nicht, sinken Sales relativ. → **Reviews haben kausalen Einfluss.**

**Luca (2016):** Yelp-Ratings auf Restaurant-Revenues. Trick: Yelp rundet Ratings → 3.24 wird "3", 3.25 wird "3.5". Zwei sehr ähnliche Restaurants werden ganz anders angezeigt.
- Result: 1-Stern-Increase → 5–9% Revenue-Increase
- ABER: nur für **independente** Restaurants, nicht für Chains (McDonald's ist McDonald's egal welche Sterne)
- ELITE-Reviewers haben fast doppelt so viel Effekt

### Probleme von R&R

1. **Selection Bias:** Wer reviewt? Oft extreme Erfahrungen (sehr positiv ODER sehr negativ).
2. **Strategic Behavior:** Sellers können Fake-Reviews kaufen; Buyers können erpressen ("4-Stern = 1-Stern Drohung").
3. **Reciprocity:** 2-sided Ratings führen oft zu inflationären Ratings (Airbnb).
4. **Informativeness:** Rating allein vs. Volume — ein 5-Stern-Restaurant mit 2 Reviews ist anders zu interpretieren als mit 200.

### Reputation als Disziplin-Mechanismus

Klassisches Modell (Tadelis 2016):

Trust-Game: Buyer entscheidet erst, dem Seller zu vertrauen (Trust/Don't); Seller entscheidet dann, ehrlich zu sein (Honor/Abuse).

**Einmalig gespielt:** Opportunistischer Seller missbraucht immer. Buyer rechnet damit, vertraut nicht → Trade collapses.

**Wiederholt gespielt:** Opportunistischer Seller könnte heute "ehrlich" sein, um morgen wieder Vertrauen zu bekommen → Kooperation möglich.

**R&R-Pflöcke das auch im anonymen Markt:** Wenn dein heutiges Verhalten morgen für *alle* sichtbar ist, hast du Anreiz zu kooperieren — selbst wenn du diesen Buyer nie wiedersiehst.

### Empirische Effekte von Reputation

**Resnick et al. (2006) — eBay-Experiment:**
- Postkarten verkauft entweder unter etabliertem Account (hohe Reputation) oder Newcomer-Account
- High-Rep-Seller bekam 8% mehr Preis
- → Reputation ist ökonomisch wertvoll (auch für sonst homogenes Produkt)

---

## Querbeziehungen — die roten Fäden des Kurses

### Roter Faden 1: Erwartungen sind alles

- Section 1: Network Effects → User-Entscheidungen interdependent
- Section 2: Fulfilled-Expectations-Equilibrium → Multiple Equilibria
- Section 3: Chicken-and-Egg → Coordination-Problem
- Section 4: Strategic Pricing → Erwartungen steuern
- Section 5: R&R → Erwartungen über Counterparts

### Roter Faden 2: Pricing internalisiert Externalitäten

- Standard-Markt: Preis = Marginal-Cost-Plus
- Plattform: Preis berücksichtigt **die NE, die dieser User auf andere wirft**
- → Asymmetric Pricing, manchmal negative Preise

### Roter Faden 3: Die zwei Forces — Concentration vs. Dispersion

| Concentration-Forces (Tipping) | Dispersion-Forces (Coexistence) |
|---|---|
| Network Effects (β) | Differenzierung (τ) |
| Economies of Scale | Multi-Homing |
| Switching Costs | Congestion |
| R&R-Lock-in | Compatibility |

### Roter Faden 4: Trust als Plattform-Asset

- Without Trust: Hohe Transaktionskosten, Adverse Selection, Moral Hazard
- Plattform-Trust-Tools: R&R, Insurance, Dispute Resolution, Algorithm-Curation
- Trust-Quelle: Repeated Interaction (klassisch) oder Reputation (Plattform-spezifisch)

---

## Zusammenfassende Mind-Map

```
ORGANIZATIONAL ECONOMICS — PLATFORM ECONOMICS
│
├── Section 1: Definition & Network Effects
│   ├── Plattform = NE existieren + aktiv managed
│   ├── 4 Kategorien: ±WGNE, ±CGNE
│   └── Typologie: Wertschöpfung × Wertextraktion
│
├── Section 2: Demand & Competition
│   ├── Demand für 1 Network Good
│   │   ├── Discrete (2 Konsumenten) → Game Theory
│   │   ├── Continuum + θ-Heterogenität → Indifferent User
│   │   └── Strong vs. Weak NE → Multiple FEE oder einzigartig
│   ├── Hotelling mit NE
│   │   ├── τ vs. β: Differenzierung vs. NE-Dominanz
│   │   ├── Tipping bei β > τ
│   │   └── Equilibrium-Preise sinken mit β
│   └── Compatibility-Entscheidung
│       ├── WTP-Effekt (immer positiv)
│       ├── Level-Playing-Field-Effekt (negativ für stark-q Entrant)
│       └── Threshold q̂ = √(τ(τ−β))
│
├── Section 3: Launching Platforms
│   ├── Chicken-and-Egg-Problem
│   ├── Divide-and-Conquer
│   │   ├── 4 Equilibrium-Configs prüfen
│   │   ├── Trap-Region eliminieren
│   │   └── Subsidieren ↔ Monetarisieren
│   └── Seeding-Strategien
│       ├── Marquee, Niche, Piggyback, etc.
│       └── Expectations boostern
│
├── Section 4: Pricing & Disintermediation
│   ├── Membership vs. Transaction Fees
│   ├── Asymmetric Pricing
│   │   ├── Price Structure Not Neutral
│   │   ├── Lerner-Index mit NE-Adjustierung
│   │   └── Subsidy Side ≠ Money Side
│   └── Disintermediation
│       ├── 5 Drivers
│       └── Karotte & Stock
│
└── Section 5: Ratings & Reviews
    ├── R&R löst Adverse Selection + Moral Hazard
    ├── R&R = WGNE-Quelle + Network-Verstärker
    ├── Empirie: Chevalier-Mayzlin, Luca
    └── Reputation = Disziplin im anonymen Markt
```

---

## Verwandt

- [[20.studies/Organizational-Economics/problem-set-recipes]] — Konkrete Schritt-für-Schritt-Anleitungen
- [[20.studies/Organizational-Economics/formelsammlung-cheatsheet]] — Alle Formeln
- [[20.studies/Organizational-Economics/plattformen-network-effects]] — Mehr Detail zu Network Effect Typen
- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]] — Mehr Detail zu D&C
- [[20.studies/Organizational-Economics/Hub]]
