---
created: 2026-06-06
type: section-deep-dive
source: ME 3 Aguiar VL Section 2 (Parts 1, 2, 3)
tags: [organizational-economics, section2, demand, hotelling, compatibility, defensibility, data-network-effects]
status: master
---

# Section 2 — Features of Platforms and Markets with Platforms

> **Big Picture:** Wie unterscheidet sich Demand für Network Goods von Standard-Demand? Wie konkurrieren Plattformen? Was schützt eine etablierte Plattform vor Disruption? Diese Section enthält die ZENTRALE Modell-Mathematik des Kurses (Sets 1, 2 basieren auf ihr) plus die strategische Defensibility-Theorie.

---

## Roadmap

1. Demand for Single Network Good (one-sided, Set 1)
   - Simple Model (2 Konsumenten)
   - General Model (Continuum)
   - Heterogenität, Multiple FEE, Critical Mass
2. Demand & Pricing of Incompatible Network Goods (Set 2)
   - WhatsApp-vs-Signal-Tipping
   - Hotelling mit Network Effects
   - Equilibrium-Pricing
3. Compatibility Decisions
4. Defensibility: Beyond Network Effects
5. Data Network Effects

---

## 1. Demand for Single Network Good

### Warum ist Demand für Network Goods anders?

Bei "normalen" Gütern: Ich kaufe Bananen, ohne mich um andere zu kümmern. Meine Entscheidung ist **isoliert**.

Bei Network Goods: Mein Wert hängt davon ab, wer noch joined. Ich kann meine Entscheidung **nicht isoliert** treffen — ich muss Erwartungen bilden.

**Konsequenzen:**
1. Demand ist **schwer vorhersagbar** für gegebenen Preis
2. Demand hängt von **Erwartungen** ab
3. Kleine Preisänderungen können **Tipping** auslösen (alle oder keiner)

### Simple Model: 1 Good, 2 Consumers

**Ohne Network Effects:**
```
U_i = V_i − p   für i = A, B
```

Demand:
- `p > V_A`: niemand kauft (N = 0)
- `V_A ≥ p > V_B`: nur A kauft (N = 1)
- `V_B ≥ p`: beide kaufen (N = 2)

→ Standard Law of Demand, eindeutige Quantity pro Price.

**Mit Network Effects (β):**
```
U_i = V_i + β·𝟙_{j buys} − p
```

→ Decisions interdependent. Game-theoretisches Setup nötig.

### Das Spiel (2x2 Normal Form)

|         | B buys     | B doesn't  |
|---------|------------|------------|
| **A buys**  | (V_A+β−p, V_B+β−p) | (V_A−p, 0) |
| **A doesn't** | (0, V_B+β−p) | (0, 0) |

### 4 Outcomes — wann ist welcher Nash Equilibrium?

(Annahme: V_A > V_B)

| Equilibrium | Bedingung |
|---|---|
| **(Buy, Buy)** | beide profitieren bei Joinen, wenn andere joinen: `p < V_B + β` |
| **(Don't, Don't)** | beide besser, wenn keiner joined: `p > V_A` |
| **(Buy, Don't)** | A buyt allein lieber als nichts; B will nicht beitragen: `V_B + β < p < V_A` ⇔ `β < V_A − V_B` |
| **(Don't, Buy)** | nie (V_A > V_B → A würde immer mit B mitmachen) |

### Zwei Fälle

**Fall 1: Schwache NE (β < V_A − V_B)**

```
Wenn p < V_B + β     → N = 2 (beide)
Wenn V_B + β < p < V_A → N = 1 (nur A)
Wenn p > V_A         → N = 0
```

→ Demand ist **monoton** in p. Gibt **eindeutige** Quantity pro Price.

**Fall 2: Starke NE (β > V_A − V_B)**

```
Wenn p < V_B + β    → (Buy, Buy) ist Equilibrium → N = 2
Wenn p > V_A        → (Don't, Don't) ist Equilibrium → N = 0
ABER: für V_A < p < V_B + β sind BEIDE Equilibria!
```

→ **Multiple Equilibria** für mittlere Preise. N = 0 oder N = 2 — abhängig von Erwartungen.

### Self-fulfilling Prophecies

In der Multiple-Equilibria-Region:
- **Optimistische Beliefs** → beide erwarten "der andere joined" → beide joinen → bestätigt
- **Pessimistische Beliefs** → keiner joined → bestätigt

**Konsequenzen:**
1. **Unpredictability:** Plattform kann den Outcome nicht garantieren
2. **Potential Inefficiency:** Bei pessimistischen Beliefs landet man bei (0,0), obwohl beide bei (2,2) besser dran wären

### General Model — Continuum von Konsumenten

**Setup:**
- Mass 1 of consumers, real numbers `θ ∈ [0, 1]`
- Konsument θ entscheidet, ob er joined; seine Decision **affektiert die Network-Größe nicht spürbar** (Atomis-Annahme)
- Konsumenten entscheiden **simultan** und müssen Erwartungen über andere bilden

### Utility Function

```
U(θ) = V + f(n^e) − p
```

Mit `f(n^e) = β · n^e` (linearer Network-Benefit).

| Symbol | Bedeutung |
|---|---|
| `V` | Stand-Alone Benefit (kein NE-Dependence) |
| `f(n^e)` | Network Benefit, `f(0) = 0, f' > 0` |
| `p` | Preis für Plattform-Zugang |
| `n^e` | erwartete Network-Größe |

### Fulfilled-Expectations Equilibrium (FEE)

Wir focusieren auf Equilibria, wo **die gemeinsame Erwartung der Konsumenten korrekt ist**: `n^e = n`.

Das ist äquivalent zu: für gegebenes `p`, spielen Konsumenten ein **anonymes Game**, dessen Nash-Equilibrium wir lösen.

### Heterogenitäts-Varianten

**Variante 1 — Heterogeneous Stand-Alone:**
```
U(θ) = θV + βn^e − p
```
- Höhere θ → höherer Stand-Alone-Wert
- Smartphones, "tech aficionados" als early Adopters (sie wertschätzen die Technologie an sich)
- → Set 1.2

**Variante 2 — Heterogeneous Network Benefit:**
```
U(θ) = V + θβn^e − p
```
- Höhere θ → höhere Bewertung der Network-Größe
- Blackberry, "business people" als early Adopters (sie wollen viele Kontakte, nicht das Tech)
- → Set 1.3

### Variante 1 — Detail (Set 1.2)

**Indifferent Consumer:**
```
θ̂V + βn^e − p = 0
⇒ θ̂ = (p − βn^e)/V
```

Consumer mit `θ ≥ θ̂` joinen → `n = 1 − θ̂`.

**Demand-Eckfälle:**
- `n = 1` (alle): `θ̂ ≤ 0` ⇔ `n^e ≥ p/β`
- `n = 0`: `θ̂ ≥ 1` ⇔ `n^e ≤ (p − V)/β`

**FEE-Demand:**
```
n(p) = (V − p)/(V − β)
```

(oder inverse: `p(n) = V − (V − β)·n`)

### Zwei Fälle bei Variante 1

**Fall A: V > β (schwache NE)**

`n` ist **decreasing** in `p` → Standard Law of Demand → **eindeutige** Demand.

```
p
|
V|*
 |  *
 |    *
β|------ *
 |        |
 0--------1-->n
```

**Fall B: V < β (starke NE)**

`n` ist **increasing** in `p` → "perverse" Demand → **multiple FEE**.

```
p
|
β|        *
 |      *
 |    *
V|  *
 |
 0------1-->n
```

**Intuition Fall B:** Bei höherem `p` joined nur der Konsument mit starker Network-Bewertung (θ groß). Wenn er erwartet, dass viele joinen, kauft er trotzdem.

### Fall B — Drei FEE

Für gegebenes p können **drei** FEE koexistieren:
- `n = 0` (keiner joined)
- `n = n_S = (V−p)/(V−β)` (kritische Masse, unstabil)
- `n = 1` (alle joinen)

### Stabilität — Dynamic Adjustment

**Idee:** Welche Equilibria sind robust gegen kleine Erwartungs-Perturbationen?

- Wenn `WTP > p` für Konsumenten am Rand → `n` wächst
- Wenn `WTP < p` → `n` schrumpft

**Resultate:**
- `n = 0` → **STABLE** (kleines Aufpoppen wird gedämpft)
- `n_S` → **UNSTABLE** ("critical mass")
- `n = 1` → **STABLE**

### Critical Mass — die zentrale Lektion

Wenn die Plattform die Userzahl über `n_S` (Critical Mass) bringt, **snowballt** sie automatisch zu `n = 1` (Erfolg). Bleibt sie darunter, fällt sie auf `n = 0` (Tod).

→ **Erfolgreiche Plattformen erreichen die Critical Mass.**

### Variante 2 — Detail (Set 1.3)

**Indifferent Consumer:**
```
V + θ̂βn^e − p = 0
⇒ θ̂ = (p − V)/(βn^e)
```

**Inverse FEE-Demand:**
```
p(n) = V + βn(1 − n)
```

→ **Inverse-U-Form**, Maximum bei `n = 1/2`, `p_max = V + β/4`.

### Drei FEE bei Set 1.3

Für `V < p < V + β/4`:
- `n_0 = 0` (STABLE)
- `n_1 = 1/2 − √(1/4 − (p−V)/β)` (UNSTABLE)
- `n_2 = 1/2 + √(1/4 − (p−V)/β)` (STABLE)

### Die zwei Forces

In Set 1.3 gibt es eine sichtbare Spannung:
- **Law of Demand:** höhere `n` braucht niedrigere `p` (Standard)
- **Network Effect:** höhere `n` erlaubt höhere `p` (Plattform wird wertvoller)

Für `n < 1/2`: Network-Effect dominiert (inverse Beziehung)
Für `n > 1/2`: Law of Demand dominiert (Standard)

### Case in Point — The Million Dollar Homepage

**Story:** 2005 setzte Alex Tew eine Webpage mit 1 Mio. Pixel auf, $1 pro Pixel an Werber.

**Logik:** **Indirekte Network Effects** — mehr Werber → mehr neugierige Visitors → mehr Werber wollen drauf.

**Critical-Mass-Engineering:**
- Familie + Freunde kauften erste Pixel
- Press-Release ging zum BBC und Tech-Sites
- Innerhalb eines Monats: $250k
- Snowball → $990k in 4 Monaten, 25k Visitors/Stunde

**Lehre:** Right Expectations können selbst-erfüllend sein. Hätte Tew die Critical Mass nicht generiert, wäre die Seite leer geblieben.

---

## 2. Demand & Pricing of Incompatible Network Goods

### Outside Option wird endogen

Bei einer einzelnen Plattform: Outside Option = "nichts kaufen" (exogen, konstant = 0).

Bei mehreren Plattformen mit Inkompatibilität: Outside Option = "die andere Plattform" → **endogen** (hängt davon ab, wer dort joined).

**Konsequenz:** Attraction Loops werden noch stärker. Wenn Plattform A wächst, sinkt der Wert des Bleibens bei B → mehr User wechseln zu A → ...

### Compatible vs. Incompatible Networks

| Incompatible | Compatible |
|---|---|
| NE sind **plattform-spezifisch** | NE sind **global** |
| Outside Option **endogen** | Outside Option **konstant** |
| Attraction Loops verstärken sich | Plattformen können koexistieren |
| **Nur eine Plattform überlebt** typischerweise | Competition **in** the market |
| Competition **for** the market | |

### Demand für 2 Inkompatible Network Goods — Modell

**Setup:** 2 Plattformen (W = WhatsApp, S = Signal). User arrivieren sequentiell.
- "Signal fans" haben Stand-Alone-Bewertung 50 für S, 0 für W
- "WhatsApp fans" haben 0 für S, 50 für W
- In jeder Periode: 1 neuer User (W-fan oder S-fan, 50/50)
- Alle User wertschätzen jeden anderen User mit 1
- User sind **myopisch** (basieren Entscheidung auf aktueller Network-Größe, nicht zukünftige)

**Utility-Matrix:**

|         | Signal | WhatsApp |
|---------|--------|----------|
| **Signal fans** | 50 + n_S^t | 0 + n_W^t |
| **WhatsApp fans** | 0 + n_S^t | 50 + n_W^t |

### Tipping-Bedingung

Ein **Signal-fan** wechselt zu WhatsApp wenn:
```
0 + n_W^t ≥ 50 + n_S^t   ⇔   n_W^t − n_S^t ≥ 50
```

Sobald WhatsApp **50 mehr User** hat, wechseln auch Signal-Fans → **Markt tippt zu WhatsApp**.

Symmetrisch: Markt tippt zu Signal wenn `n_W^t − n_S^t ≤ −50`.

### Simulations-Beispiel

Stochastische Simulationen zeigen: Der Markt-Pfad ist **zufällig**, aber sobald die 50er-Schwelle erreicht ist, ist der Outcome **deterministisch**.

→ Reale Welt: Frühe Pluralität kann sich zu Monopol entwickeln, ohne dass ein Anbieter "besser" ist.

### Pricing of Incompatible Network Goods

Bisher haben wir Preise als gegeben angenommen. Jetzt: **Plattformen wählen Preise strategisch**.

**Differenzierung kann Tipping verhindern:** Wenn Konsumenten starke Präferenzen für eine Plattform haben, kann eine kleinere Plattform durch Differenzierung überleben.

→ **Hotelling-Modell**.

### Product Differentiation: Horizontal vs. Vertical

**Horizontal:** Bei gleichem Preis stimmen Konsumenten **nicht überein**, welches Produkt besser ist.
- "Manche mögen Light-Roast, andere Dark-Roast Coffee"
- WhatsApp vs. Signal: Manche wollen Convenience, andere Privacy

**Vertical:** Bei gleichem Preis ziehen **alle** Konsumenten ein Produkt vor.
- "BMW ist objektiv besser als Dacia"
- Alle bevorzugen High-Quality Coffee Beans über Low-Quality (bei gleichem Preis)

### Hotelling Model — Setup

**Konsumenten:** Uniformly distributed auf `[0, 1]` (Hotelling-Linie).
- Position `x` = idealer Mix von Stand-Alone-Eigenschaften
- Plattform 1 ist bei 0, Plattform 2 bei 1

**Disutility:** Konsument bei `x` zahlt Disutility `τ·x` für Plattform 1 (oder `τ·(1−x)` für Plattform 2).
- `τ` = "Transport Cost" = Maß für **Differenzierungs-Stärke**
- Höheres τ = stärker differenziert = User kleben an "ihrer" Plattform

### Hotelling mit Network Effects

```
U(x) = V + q − τx + βn_1^e − p_1     (joining Pl. 1)
U(x) = V − τ(1−x) + βn_2^e − p_2     (joining Pl. 2)
U(x) = 0                              (joining nobody)
```

- `V`: Stand-Alone-Wert (groß genug, dass alle eine Plattform joinen)
- `q`: Vertikaler Qualitäts-Vorteil von Pl. 1 (`q > 0`)
- `τ`: Horizontale Differenzierung
- `β`: Network-Effect-Intensität

### Indifferent Consumer x̂

Setze U_1 = U_2:
```
V + q − τx̂ + βn_1^e − p_1 = V − τ(1−x̂) + βn_2^e − p_2

⇒ x̂ = 1/2 + [β(n_1^e − n_2^e) + q + p_2 − p_1] / (2τ)
```

→ Konsumenten mit `x < x̂` joinen Pl. 1, mit `x > x̂` joinen Pl. 2.

### Network Effects als endogene vertikale Differenzierung

Beachte: `∂n_i/∂n_i^e = β/(2τ) > 0`. Plattform mit mehr erwarteten Usern bekommt höheren Marktanteil.

**Interpretation:** Network-Benefits sind **endogene Qualitäts-Differenz** (zusätzlich zu `q`).
- Plattform, die als groß erwartet wird, **wird** groß (self-fulfilling)
- Stärkere NE (β groß) → größere Bedeutung dieser endogenen Qualität → mehr Tipping-Risiko

### Pricing Decisions — 2-Stage Game

**Stage 1:** Plattformen wählen Preise `p_1, p_2`.
**Stage 2:** Konsumenten entscheiden (mit FEE: `n_i^e = n_i`).

→ Solve durch **Backward Induction**.

### 3 Possible Fulfilled-Expectations-Equilibria

| Configuration | FEE-Bedingung |
|---|---|
| All join Pl. 1 | `p_1 − p_2 ≤ q + β − τ` |
| All join Pl. 2 | `p_1 − p_2 ≥ q − (β − τ)` |
| Interior (beide koexistieren) | beide oben verletzt |

### Wann gibt es Multiple Equilibria?

- **Wenn β > τ (starke NE):** Die Bedingungen überlappen → multiple equilibria → Markt kann tippen
- **Wenn β < τ (schwache NE):** Unique Interior Equilibrium → Plattformen koexistieren

### Interior Demand mit FEE

```
n_1 = 1/2 + (q + p_2 − p_1) / [2(τ − β)]
n_2 = 1 − n_1
```

**Sign of slope** (`dn_1/dp_1`):
- `(τ − β) > 0` (weak NE): Standard, `dn_1/dp_1 < 0`
- `(τ − β) < 0` (strong NE): Pervers, `dn_1/dp_1 > 0`

### Weak NE: Optimal Pricing

Profit-Maximierung mit `π_i = (p_i − c) · n_i`:

**FOC liefert Reaction Functions:**
```
p_1(p_2) = (τ − β + p_2 + q + c) / 2
p_2(p_1) = (τ − β + p_1 − q + c) / 2
```

**Equilibrium:**
```
p_1* = c + τ − β + q/3
p_2* = c + τ − β − q/3

n_1* = 1/2 + q/[6(τ − β)]
n_2* = 1/2 − q/[6(τ − β)]
```

### Komparative Statik

**β ↑ (NE stärker):**
- `p_i* ↓` — schärferer Wettbewerb (jeder User ist wertvoller, weil er andere anzieht)
- `n_1* ↑` (Pl. 1 gewinnt durch Quality-Advantage)
- Profit von Pl. 1: **ambiguous** (Preis ↓, Menge ↑)
- Profit von Pl. 2: **unambiguously ↓**

**No-Tipping-Bedingung:** `q < 3(τ − β)` — sonst kann Pl. 1 den ganzen Markt nehmen.

### Strong NE — Multiple Equilibria

Bei `β > τ` wird das Pricing-Problem komplex (mehrere Equilibria sind möglich, je nach Erwartungen).

**Tendenz:** **Tipping** wahrscheinlicher. Der Markt collapsed zu Single-Winner.

### Networks & Market Structure — Summary

| Force | Effekt auf Konzentration |
|---|---|
| Network Effects | **+ (mehr Konzentration)** |
| Economies of Scale | + |
| Differentiation (τ) | **− (weniger Konzentration)** |
| Multi-Homing | − |
| Congestion | − |

### Konkurrenz IN vs. FOR the Market

- **Competition for the market** (Tipping): Eine Plattform gewinnt alles. Stark NE + niedrige Differenzierung.
- **Competition in the market** (Koexistenz): Mehrere Plattformen halten Marktanteile. Differenzierung dominiert.

### Multi-Homing

User können auf mehreren Plattformen gleichzeitig sein (Spotify + Apple Music, iOS + Android-Game-Dev).

**Effekt:** NE sind nicht mehr exklusiv → Konkurrenz in market statt for market.

### Congestion

Wenn eine Plattform sehr groß wird, kann Suche/Matching teurer werden (z.B. zu viele Listings → schwerer zu finden).

→ User könnten zu kleineren, fokussierten Alternativen ziehen.

### Economies of Scale

Hohe Fixkosten + niedrige Grenzkosten → größere Plattform hat Kostenvorteil → Tendenz zu Konzentration.

**Beispiele:** Visa/MasterCard (hohe Aufbau-Kosten, fast 0 Kosten pro Trxn).

---

## 3. Network Goods: Compatibility Decisions

### Setup

**Markt mit etabliertem Incumbent + neuem Entrant.**
- Entrant hat Quality-Advantage `q > 0` (Stand-Alone)
- Entrant entscheidet: kompatibel mit Incumbent oder nicht?
- User entscheiden dann, ob sie zum Entrant wechseln

**Frage:** Wann gewinnt Entrant *mehr* durch Compatibility (sharing the network) vs. eigene Netzwerk-Bildung?

### Die zwei Effekte von Compatibility

**1. Willingness-to-Pay-Effekt (immer positiv):**
Bei Compatibility ist die *gemeinsame* Netzwerk-Größe größer → User zahlen mehr → Entrant kann höhere Fee verlangen.

**2. Level-Playing-Field-Effekt (kann negativ sein):**
Bei Incompatibility hat Entrant einen "Cold Start"-Nachteil (kleines Netzwerk). Compatibility eliminiert diesen Nachteil — aber **auch** den NE-Größenvorteil, wenn Entrant *sonst* mehr User hätte.

### Compatibility-Entscheidungs-Regel

| Entrant's q | Optimale Entscheidung |
|---|---|
| **q klein** | Compatibility — vermeidet Cold-Start-Nachteil |
| **q groß** | Incompatibility — behält NE-Größenvorteil bei |
| **q = 0** (identische Qualität) | Compatibility — kein Grund, sich abzuschotten |

### Formal: Compatibility-Threshold

(Aus Set 2.2:)
```
Entrant prefers Compatibility  ⇔  q < q̂ = √(τ(τ−β))
```

**Wenn `τ − β < q < q̂`:**
- "Level-Playing-Field"-Effekt ist negativ
- ABER "WTP-Effekt" ist positiv und überwiegt
- → Compatibility immer noch besser

### Praktische Beispiele

**Tesla Charging:**
- Anfangs proprietär (sehr großer q-Advantage) → Inkompatibilität rational
- Jetzt teils CCS-kompatibel (Markt reift, q-Advantage sinkt) → Compatibility wird attraktiver

**Apple vs. Android:**
- Apple bleibt inkompatibel (großer q-Advantage durch Ecosystem-Tight-Integration)
- Android offen (Google's Strategie war ursprünglich, alle anzuziehen)

---

## 4. Defensibility: Beyond Network Effects

### Network Effects ≠ Automatische Defensibility

**Zentrale Frage:** Wenn Plattform groß wird — wie hart ist es für Rivalen, sie zu disrupten?

**Naive Antwort:** "Network Effects schützen automatisch." → **Falsch.**

**Aguiar-Lehre:** Defensibility hängt von 4 Faktoren ab:
1. **Strength and Scope of Network Effects**
2. **Multi-Homing**
3. **Coordination Costs**
4. **Trust and Disintermediation**

### Case Study — Smartphone OS

**2007:** Nokia Symbian dominiert (>60% Marktanteil, 10k+ Apps).
**2007:** Apple iPhone launcht; Google Android launcht später.
**2015:** Android + iOS = >95% Marktanteil. **Symbian ist tot.**

**Warum scheiterte Symbian?**

Symbian hatte Scale, aber **deep ecosystem frictions:**
- Verschiedene Handset-Hersteller hatten unterschiedliche Interfaces
- Mobile Carriers schränkten ein, was Apps tun konnten
- Apps mussten für jedes Handset separat angepasst werden

→ **Schwierig für Developer**, Apps zu erstellen, die für alle Symbian-User funktionieren.

**Wie haben iOS und Android gewonnen?**
- **iOS:** Kontrollierte Hardware + Software-Standards komplett (no fragmentation)
- **Android:** Bildete **Open Handset Alliance** (gleicher OS für alle Hardware) — eliminierte Symbians Frictions

**Lehre:** Network Effects (mehr User → mehr Apps → mehr User) funktionieren nur, wenn die Plattform die NE **richtig managed**. Pure Scale ohne Management ist verwundbar.

### Windows Phone — warum scheiterte es?

**2010:** Microsoft launcht Windows Phone 7 (3 Jahre nach iOS/Android).
- **Great Stand-Alone Value** (Reviewers loben das UI)
- Microsoft hatte Loyalitätsbasis durch Windows + Xbox

**Trotzdem scheiterte:**
- Critical Mass war zu spät erreicht
- Developer hatten bereits iOS + Android priorisiert
- Microsoft zahlte sogar Developer pro App ($100k), reichte nicht
- 2016: nur Android + iOS übrig

**Steve Ballmer 2007:** "There's no chance that the iPhone is going to get any significant market share." → Klassisches Beispiel für **Smart Incumbents misreading Platform Threats**.

**Lehre:** **Critical Mass und Timing** matter. Eine technisch überlegene Plattform kann scheitern, wenn der Markt schon "gekippt" ist.

### Defensibility-Faktor 1: Strength of Network Effects

**Strong NE:** Wert eines extra Users bleibt hoch, auch bei großem Netzwerk.
- **YouTube:** Mehr Creator → mehr Content-Vielfalt → mehr User → mehr Content
- → Schwer zu replizieren

**Weak NE:** Wert eines extra Users **sinkt schnell**.
- **Videogame-Konsolen:** Wenige Hit-Games matter; weitere Games sind kaum wertvoll
- → Konsolen-Marktanteile fluktuieren stark

### Defensibility-Faktor 1b: Scope — Global vs. Local NE

**Global NE:** User profitieren von Teilnahme **über viele Orte hinweg**.
- **Airbnb:** Gast aus Frankreich profitiert von Hosts in allen Ländern → scaliert über Geografien
- → **Strong defensibility:** Launch in neuem Land bringt sofort die ganze installed base ins Spiel

**Local NE:** User kümmern sich nur um lokale Userbase.
- **TaskRabbit:** Freelancer in Zurich nutzen nur Zurich-Tasks
- → **Limited defensibility:** Plattform muss in jeder neuen Stadt von 0 anfangen

**Ambivalente Fälle:**
- **Uber:** Hauptsächlich lokal, aber mit Cross-City-Spillover (Reisende)
- **Etsy:** Local kann global werden, wenn Versand günstig (kleine Items)
- **Marketplaces für digitale Produkte/Services** (Upwork, Fiverr): **inherent global** (kein Versand nötig)

### Defensibility-Faktor 2: Multi-Homing

> **Multi-Homing** = User können simultan auf mehreren Plattformen aktiv sein.

**Wenn Multi-Homing leicht:** NE bieten wenig Defensibility.
- Uber vs. Lyft: Driver können auf beiden warten → Preiskampf
- iOS- vs. Android-Devs: Apps für beide → keine Plattform-Exklusivität

**Multi-Homing reduzieren durch:**
- **Höhere Joining-Costs** (monetär: Konsolen — kannst nicht beide kaufen; non-monetär: Streaming-Dienste — Subscription pro Dienst)
- **Personalisierte Empfehlungen** (lock-in durch User-Daten)
- **Learning-Costs** (gelernte Workflows in einer Plattform schwer transferierbar)

### Defensibility-Faktor 3: Coordination Costs

> Wie leicht ist es für User, sich auf der Nutzung *einer* Plattform zu coordinieren?

**Wenn Koordination leicht:** NE bieten wenig Defensibility.
- User können einfach zur Konkurrenz wechseln, wenn alle gleichzeitig

**Hohe Koordinationskosten machen NE defensibler:**

**Exogene Faktoren:**
- **Teure Hardware** (Videogame-Konsolen — wenig Switching, weil Hardware-investment)
- **eBay vs. anderer Marketplace** — User können nicht koordinieren, alle gleichzeitig zu wechseln (Stand-Alone-Wert hängt an existierender Userbase)

**Endogene Faktoren (Platform-Design):**
- **Spotify Personalized Recommendations** — Lern-Effekt steigt mit Nutzung, schaltet bei Switch auf 0 zurück
- **Zoom Virtual Backgrounds, Custom Settings** — User-Customization als Switching-Cost

### Coordination — Beispiel Zoom (Pandemie)

**Zoom wuchs extrem schnell** während Covid-19 dank starker NE.

Aber: **Defensibility war niedrig**. User konnten leicht zu Google Meet, Teams wechseln.
- Zoom konnte wenig Value extrahieren (Subscription nur für Pro-Features)
- **Business-User** hatten höhere Switching Costs (Workflow-Integration, Feature-Familiarity)

### Defensibility-Faktor 4: Trust and Disintermediation

(Vorgriff auf Section 4.)
- Wenn User die Plattform **vertrauen müssen**, ist die Plattform schwerer zu disrupten
- Wenn Trxns **off-platform** möglich sind (Disintermediation), ist die Plattform vulnerable

---

## 5. Data Network Effects

### Big Data — Drei V's

Online-Plattformen generieren **Big Data**:
- **Volume:** Viele Observations
- **Variety:** Verschiedene Quellen & Typen
- **Velocity:** Häufig aktualisiert

Wert kommt aus: **Generation → Storage → Preparation → Analysis → Usage idea** (ongoing process).

### Data-Enabled Learning

**Mechanismus:**
```
Mehr User → mehr Daten → bessere Algorithmen/Empfehlungen
       → wertvolleres Service → mehr User → ...
```

→ **Self-reinforcing cycle** = **Data-Enabled Learning** = potential **Data Network Effects**.

### Wann ist Data-Enabled Learning = Network Effects?

**Recall NE-Definition:** Decision von User A affektiert Wohlergehen von User B (alle anderen Sachen gleich).

**Test:** Hilft Datum von User A irgendetwas für User B?

**Ja → Data Network Effects:**
- **Waze:** Mehr User → präzisere Verkehrsinfo → besser für alle
- **Google Search:** Mehr Queries → relevantere Ergebnisse für alle

**Nein → Keine Network Effects, nur Cost Efficiency:**
- **Logistics:** Mehr Daten → bessere Logistics → niedrigere Kosten → User profitieren *indirekt* (via Preis). Aber das ist **Economy of Scale**, nicht NE.
- **Content-based Filtering (Pandora):** Lernt nur über *einen* User. Daten von User A helfen User B nicht.

### Collaborative vs. Content-Based Filtering

**Collaborative Filtering (Netflix-Style):**
- "User wie du haben auch X geguckt"
- Daten von einem User helfen Empfehlungen für andere
- → **Data Network Effects**

**Content-Based Filtering (Pandora-Style):**
- "Du hast Rock-Songs geliked, hier ist mehr Rock"
- Lernt nur über den einzelnen User
- → **Keine Data Network Effects**

### Wann führt Data zu Competitive Advantage?

**3 Bedingungen müssen erfüllt sein:**

#### 1. Data von einem User hilft anderen
→ Generiert Network Effects (siehe oben).

**Pandora vs. Spotify:**
- Pandora's Recommendations machen den Service nicht besser für andere
- Spotify hat Sharing/Discovery-Features → **direkter NE**
- → Spotify hat stärkere Defensibility durch Daten

#### 2. Value of Data ist hoch und langlebig

**Hoch:** Daten-Wert sollte hoch relativ zum Stand-Alone-Wert sein.
- **TikTok:** Algorithmus ist Hauptwert
- **Smart TVs:** Daten-Wert niedrig im Vergleich zu Screen-Quality → trotz Datensammlung wenig Defensibility durch Daten

**Langlebig:**
- Marginal Value of Data bleibt hoch auch bei großer Userbase
  - **Google Search:** Edge Cases (rare Queries) immer noch wertvoll
- Relevanz der Daten **veraltet nicht schnell**
  - **Google:** Past Search-Daten heute noch relevant
- Daten können bessere Algorithmen trainieren
  - **Plantix (plant disease detection):** Alte Daten trainieren bessere Image-Recognition

#### 3. Data ist proprietär und schwer zu imitieren

**Schwierig, alternative Datenquellen zu acquirieren:**
- Speech-Recognition kann YouTube-Captions als Training-Daten nutzen (publicly available) → wenig Daten-Defensibility
- Unique Customer Data ist nicht leicht zu replizieren

**Schwierig, Improvements zu copyen:**
- Software-Features sind beobachtbar → leicht kopierbar
- z.B. Zoom-Background-Blur → Teams adoptiert es schnell

### Take-Aways für Daten-Defensibility

Data alleine ist **nicht automatisch** ein Schutz. Nur wenn:
1. Daten **Network Effects** generieren (collaborative > content-based)
2. Daten **lange relevant** sind
3. Daten **proprietär** sind und Improvements **schwer imitierbar**

---

## Take-Aways für die Klausur

### Modell-Mathematik beherrschen

1. ✅ **Indifferent Consumer** für Set 1.2, 1.3, 2.1 schreiben können
2. ✅ **FEE-Demand** ableiten (Substitution `n^e = n`)
3. ✅ **Multiple Equilibria identifizieren** und Stabilität analysieren
4. ✅ **Hotelling Pricing** durchrechnen (FOC, Reaction Functions)

### Konzepte verstehen

1. ✅ **Warum kann Demand upward-sloping sein?** (strong NE + Heterogenität)
2. ✅ **Self-fulfilling Prophecies** erklären können (Multi-Equilibria)
3. ✅ **Critical Mass** definieren und Stabilitäts-Argument
4. ✅ **Tipping** und seine Bedingungen (β > τ)
5. ✅ **Compatibility-Trade-off** (WTP-Effekt vs. Level-Playing-Field-Effekt)

### Defensibility & Data NE diskutieren

1. ✅ **Symbian-Fall:** Warum scheiterte Network-Größe als Schutz?
2. ✅ **Windows Phone-Fall:** Was passiert, wenn man zu spät kommt?
3. ✅ **Multi-Homing reduzieren** — Strategien
4. ✅ **Local vs. Global NE** — Beispiele und Implikationen
5. ✅ **Data NE vs. Economies of Scale** — Unterschied erklären
6. ✅ **3 Bedingungen für Data-Defensibility**

### Häufige Klausur-Fallen

| Falsche Antwort | Korrekt |
|---|---|
| "Demand decreases in p, immer" | Bei strong NE + Heterogenität kann sie **increasing** sein |
| "Multi-Homing ist immer Hindernis für Plattform" | NEIN — Plattformen können es **reduzieren** durch Design |
| "Big Data = Network Effects" | NEIN — nur wenn Data von User A → wertvoller für User B |
| "Compatibility immer schlecht für Entrant" | NEIN — wenn q klein, dann besser kompatibel |
| "Local NE bedeutet nur lokale Präsenz" | NEIN — TaskRabbit ist global präsent, aber NE sind lokal |
| "Network Effects = unschlagbare Defensibility" | NEIN — Symbian + Windows Phone als Gegenbeispiele |

---

## Verwandt

- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Block 2 + 3
- [[20.studies/Organizational-Economics/section1-platforms-foundations]] — VL Section 1 (Definitionen, NE-Taxonomie)
- [[20.studies/Organizational-Economics/problem-set-recipes#SET 1 — One-Sided Platform mit WGNE|Problem Set 1 Rezept]]
- [[20.studies/Organizational-Economics/problem-set-recipes#SET 2 — Hotelling mit Network Effects (One-Sided, 2 Competing)|Problem Set 2 Rezept]]
- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]] — Hotelling + D&C-Detail
- [[20.studies/Organizational-Economics/formelsammlung-cheatsheet]] — alle Formeln
- [[20.studies/Organizational-Economics/Hub]]
