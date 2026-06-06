---
created: 2026-06-06
type: exam-prep-guide
source: own synthesis from Exercise Sets 1–4 + Solutions + Aguiar VL
tags: [organizational-economics, problem-sets, recipes, klausur-vorbereitung]
status: master
---

# Problem-Set-Recipes — "Wenn die Aufgabe X fragt, mach Y"

> **Ziel dieses Guides:** Du sollst nie wieder ratlos vor einer Modellrechnung sitzen. Hier steht für jede Aufgabe **wo du anfängst, welcher Schritt als nächstes kommt, und warum**. Die mathematische Maschinerie ist immer dieselbe; nur die Variablen-Buchstaben ändern sich.

---

## TL;DR — Aller Aufgaben-Typ in 30 Sekunden

| Set | Plattform-Logik | Kernfrage | Universal-Rezept |
|---|---|---|---|
| **Set 1** | **One-sided, single Platform**, WGNE (Within-Group) | "Wer joined bei welchem Preis?" | Indifferent Consumer finden → FEE imposen → Demand-Funktion plotten |
| **Set 2** | **One-sided, 2 competing Platforms** (Hotelling), WGNE | "Welcher Marktanteil? Tippt der Markt?" | Indifferent Consumer x̂ → 3 FEE-Kandidaten → Profit-Maximization mit FOC |
| **Set 3** | **Two-sided, Monopol-Platform**, CGNE, identische User | "Wen subventionieren?" | 4 Equilibrium-Konfigurationen testen → Trap erkennen → Divide-and-Conquer |
| **Set 4** | **Two-sided, Monopol-Platform**, CGNE, heterogene User | "Optimale Membership Fees?" | Indifferent τ̂ finden → System lösen → FOC → Lerner-Logik |

**Wichtigste Beobachtung:** *Alle vier Sets nutzen dieselbe Grundstruktur* — "Indifferent User finden, Erwartungen schließen (FEE), Plattform-Profit maximieren". Die Unterschiede liegen nur in (a) wie viele Sides es gibt und (b) ob User homogen oder heterogen sind.

---

## Die 3 Grundoperationen, die in JEDEM Set auftauchen

Wenn du diese drei beherrschst, kannst du jede Modellrechnung lösen.

### Operation A — "Indifferent User finden"

> **Wann anwenden:** Immer wenn die Aufgabe sagt "Continuum von Konsumenten", "heterogene User", oder "share who joins".

**Schritt-für-Schritt:**

1. Schreibe die Utility-Funktion U(θ) oder U(x) hin
2. Setze U = Outside Option (meist 0)
3. Löse nach θ̂ (oder x̂) auf
4. Die Anzahl/der Share der Joiner ist:
   - Wenn die Eager-Side bei θ = 1: `n = 1 − θ̂`
   - Wenn die Eager-Side bei θ = 0: `n = θ̂`

**Beispiel (Set 1.2):** `U(θ) = θV + βn^e − p = 0 ⇒ θ̂ = (p − βn^e)/V ⇒ n = 1 − θ̂`

**Eselsbrücke:** "Wer ist genau bei Null-Utility? Alle besser-bewertenden joinen, alle schlechteren bleiben weg."

### Operation B — "FEE: Fulfilled-Expectations Equilibrium imposen"

> **Wann anwenden:** Sobald du `n^e` (expected) in der Utility-Funktion hast.

**Schritt-für-Schritt:**

1. Setze `n^e = n` (Erwartungen sind im Equilibrium erfüllt)
2. Löse die entstandene Gleichung nach `n` oder `p` auf
3. Achte auf 3 Fälle:
   - **n = 0** (no one joins)
   - **n = 1** (all join)
   - **0 < n < 1** (interior, share joins)

**Beispiel (Set 1.2):** Aus `n = 1 − (p − βn^e)/V` und FEE wird `n = (V − p)/(V − β)`.

**Achtung-Falle:** Bei Set 1.3 (β·θ·n^e — Heterogenität *im Network-Term*) entsteht eine **quadratische** Gleichung in n → drei FEE statt drei Fällen.

### Operation C — "Plattform maximiert Profit"

> **Wann anwenden:** Sobald die Plattform Preise setzt (Sets 2, 3, 4).

**Schritt-für-Schritt:**

1. Schreibe `π = (P − c)·n(P)` (oder mehrdimensional `π = P_b·n_b + P_s·n_s`)
2. Ersetze `n(P)` mit der Demand-Funktion aus Operation B
3. FOC: `∂π/∂P = 0` (bei mehreren Preisen: gleichzeitiges System)
4. Löse nach P* auf
5. Setze P* zurück in die Demand-Funktion → n*
6. Berechne π* = P*·n*

**Beispiel (Set 4.3):** `π = P_b · n_b(P_b, P_s) + P_s · n_s(P_b, P_s)` → 2 FOCs → 2 Gleichungen → P_b*, P_s*.

---

## SET 1 — One-Sided Platform mit WGNE

### Big Picture für Set 1

> **Die Platform ist alleine, alle User sind in derselben Gruppe** (z.B. WhatsApp, Dropbox). Network-Effekt = "je mehr User, desto besser für mich" (oder das Gegenteil).

**Was sich von Set zu Set unterscheidet:**

| Aufgabe | Heterogenität | Utility | Schwierigkeit |
|---|---|---|---|
| 1.1 | Keine (2 User, A & B) | `U_A = V_A + β·1_{B joins} − p` | Game-theoretisches Setup |
| 1.2 | Im **Stand-Alone** (θV) | `U(θ) = θV + βn^e − p` | Standard-Modell |
| 1.3 | Im **Network** (θβn^e) | `U(θ) = V + θβn^e − p` | Quadratische Gleichung, 3 FEEs |

### REZEPT: Aufgabe 1.1 (Discrete, 2 Consumers)

**Wenn die Aufgabe sagt:** "2 Konsumenten Anna & Bruno, mit Bewertungen V_A, V_B, joinen je nach Beobachtung des anderen…"

**Schritt 1 — Utility-Funktionen schreiben:**
```
U_A = V_A + β − p  (wenn B joined)
U_A = V_A − p      (wenn B nicht joined)
```
Analog für B.

**Schritt 2 — Normal-Form-Matrix:**

|             | B joined                | B joined nicht |
|-------------|-------------------------|----------------|
| A joined    | (V_A+β−p, V_B+β−p)      | (V_A−p, 0)     |
| A joined nicht | (0, V_B+β−p)         | (0, 0)         |

**Schritt 3 — 4 Equilibria checken:**

Für jede Zelle: Hat Anna Anreiz, von dieser Strategie abzuweichen? Hat Bruno? Wenn niemand abweicht → Nash.

| Equilibrium | Bedingung | Wann erfüllt? |
|---|---|---|
| (Buy, Buy) | beide besser-off beim Joinen | `p < V_B + β` (V_B < V_A) |
| (Don't, Don't) | beide besser-off beim Wegbleiben | `p > V_A` |
| (Buy, Don't) | A buyt allein lieber als gar nicht | `V_B + β < p < V_A` ⇔ `β < V_A − V_B` |
| (Don't, Buy) | NIE (weil V_A > V_B) | – |

**Schritt 4 — Demand zeichnen:**

- Wenn `β < V_A − V_B` ("schwacher Network Effect"): drei Regionen (N=2, N=1, N=0), **eindeutige** Demand
- Wenn `β > V_A − V_B` ("starker Network Effect"): zwei Equilibria überlappen → **Multiple Equilibria** für `V_A < p < V_B + β`

**Schritt 5 — Interpretation:**

- Starker Network Effect = Markt unvorhersehbar, hängt an Erwartungen
- Pessimistische Erwartungen ⇒ ineffizient (alle joinen-wollen, aber niemand traut sich)

**Klassische Klausur-Fragen:**
- "How many users join if optimistic/pessimistic beliefs?" → Self-fulfilling prophecy
- "What changes when β erhöht?" → Trap-Region entsteht

### REZEPT: Aufgabe 1.2 (Heterogeneous Stand-Alone)

**Wenn die Aufgabe sagt:** "Continuum, U(θ) = θV + βn^e − p, θ ∼ U[0,1]"

**Schritt 1 — Indifferent Consumer** (Operation A):
```
θ̂V + βn^e − p = 0
⇒ θ̂ = (p − βn^e)/V
```
Consumer mit `θ ≥ θ̂` joinen → `n = 1 − θ̂ = 1 − (p − βn^e)/V`.

**Schritt 2 — Eckfälle prüfen:**
- `n = 1` (alle joinen) wenn `θ̂ ≤ 0` ⇔ `n^e ≥ p/β`
- `n = 0` (niemand joined) wenn `θ̂ ≥ 1` ⇔ `n^e ≤ (p−V)/β`

**Schritt 3 — FEE imposen** (Operation B):
Setze `n^e = n` und löse:
```
n = (V − p)/(V − β)
```
Bzw. invers: `p(n) = V − (V − β)·n`

**Schritt 4 — Fallunterscheidung V vs. β:**

| Fall | Demand-Verhalten | Equilibria |
|---|---|---|
| **V > β** (weak NE) | `n` decreasing in `p` (standard) | Eindeutig |
| **V < β** (strong NE) | `n` increasing in `p` (!!) | Multiple (3) |

**Plot:**
- V > β: Standard, downward-sloping (Knick bei n=1)
- V < β: Upward-sloping (Knick bei n=1) — das ist der "weird" Fall

**Schritt 5 — Stabilität (bei V < β):**
- `n = 0` ist STABLE (kleines Aufpoppen wird gedämpft)
- `n_S = (V − p)/(V − β)` ist UNSTABLE — "kritische Masse"
- `n = 1` ist STABLE

**Intuition:** Im starken-NE-Fall ist der hochbewerter Konsument (θ=1) so begeistert von Network Effects, dass er auch bei hohem Preis joined, *wenn* alle andere mitmachen.

### REZEPT: Aufgabe 1.3 (Heterogeneous Network Benefit)

**Wenn die Aufgabe sagt:** "U(θ) = V + θβn^e − p"  
(Heterogenität sitzt im **Network-Term**, nicht im Stand-Alone)

**Schritt 1 — Indifferent Consumer:**
```
V + θ̂βn^e − p = 0
⇒ θ̂ = (p − V)/(βn^e)
```
**Wichtig:** Jetzt joinen Consumer mit `θ ≥ θ̂` → `n = 1 − θ̂`

**Schritt 2 — Invertierte Demand vor FEE:**
```
p(n, n^e) = V + βn^e − βn·n^e
```

**Schritt 3 — FEE imposen** (`n^e = n`):
```
p(n) = V + βn(1 − n)
```
→ **Quadratische Gleichung in n!** Das gibt einen inverse-U-shape.

**Schritt 4 — Wendepunkt analysieren:**

- Maximum bei `n = 1/2`, dort `p = V + β/4`
- Für `n < 1/2`: Network-Effekt dominiert (höhere n ⇒ höhere p) — "Snowball-Region"
- Für `n > 1/2`: Law of Demand dominiert (höhere n ⇒ niedrigere p)

**Schritt 5 — Drei FEE für gegebenen p:**

| Preis | Anzahl Equilibria |
|---|---|
| `p ≥ V + β/4` | 1 (nur n=0) |
| `p ≤ V` | 1 (nur n=1) |
| `V < p < V + β/4` | **3** (n=0, n₁, n₂) |

Wobei `n₁ = 1/2 − √(1/4 − (p−V)/β)` (small) und `n₂ = 1/2 + √(1/4 − (p−V)/β)` (large).

**Schritt 6 — Stabilität:**

- `n = 0` → STABLE (Pessimismus-Falle)
- `n₁` → UNSTABLE (critical mass)
- `n₂` → STABLE (success!)

**Intuition:** Wer joined zuerst? Die mit hohem θ (= hohe Network-Bewertung). Aber die brauchen viele andere, um zu joinen. → Coordination Trap.

**Praktische Beispiele:** Blackberry (geschäftliche Power-Nutzer); Telefon (early adopters = Vielnutzer).

---

## SET 2 — Hotelling mit Network Effects (One-Sided, 2 Competing)

### Big Picture für Set 2

> **Zwei Plattformen konkurrieren**, Konsumenten gleichmäßig auf [0, 1] verteilt, **horizontale Differenzierung** (τ) + **vertikale Qualität** (q) + Network Effects (β). Zentrale Frage: Tippt der Markt oder koexistieren beide?

**Was sich zwischen 2.1 und 2.2 unterscheidet:**

| Aufgabe | Setting | Schwierigkeit |
|---|---|---|
| 2.1 | Symmetric Hotelling, gemeinsames β | Standard 2-Stage-Game |
| 2.2 | Asymmetric β_1, β_2 (entrant vs. legacy) + Compatibility | Komplex, mehrere Cases |

### REZEPT: Aufgabe 2.1 (Symmetric Hotelling mit NE)

**Setting:**
```
U(x) = V + q − τx + βn₁^e − p₁   (joining Plattform 1)
U(x) = V − τ(1−x) + βn₂^e − p₂   (joining Plattform 2)
```

**Schritt 1 — Indifferenter Konsument x̂:**

Setze die zwei Utilities gleich:
```
V + q − τx̂ + βn₁^e − p₁ = V − τ(1−x̂) + βn₂^e − p₂
⇒ x̂ = 1/2 + (p₁ − p₂ − q)/(2(β − τ))     ← !! Note den Nenner !!
```

(Vorsicht beim Vorzeichen — Aufgabe schreibt manchmal mit (β−τ), andere mit (τ−β).)

**Schritt 2 — 3 mögliche FEE:**

Mit `n₁ = x̂` und `n₂ = 1 − x̂` und FEE `n_i^e = n_i`:

| Configuration | Bedingung (mit FEE) |
|---|---|
| All join Pl. 1: `x̂ = 1` | `p₁ − p₂ ≤ q + β − τ` |
| All join Pl. 2: `x̂ = 0` | `p₁ − p₂ ≥ q − (β − τ)` |
| Interior `x̂ ∈ (0,1)` | Beide obige Bedingungen verletzt |

**Schritt 3 — Wann gibt es **multiple equilibria**?**

- Wenn `β > τ` (strong NE): Die Bedingungen für "all 1" und "all 2" überlappen → multiple equilibria → Markt kann tippen
- Wenn `β < τ` (weak NE, weil Differentiation dominiert): eindeutiges Interior-Equilibrium → beide Plattformen koexistieren

**Schritt 4 — Pricing-FOC (nur für β < τ-Fall):**

Aus dem interior Demand:
```
n₁ = 1/2 + (q + p₂ − p₁)/(2(τ − β))
```
Profit: `π_i = p_i · n_i` (Annahme c=0)

FOCs liefern Reaction Functions:
```
p₁(p₂) = (τ − β + p₂ + q)/2
p₂(p₁) = (τ − β + p₁ − q)/2
```

System lösen:
```
p₁* = τ − β + q/3
p₂* = τ − β − q/3
```

**Schritt 5 — Equilibrium-Quantitäten:**
```
n₁* = 1/2 + q/(6(τ − β))
n₂* = 1/2 − q/(6(τ − β))
```

**Schritt 6 — Komparative Statik (β ↑):**

- `p_i*` ↓ (mehr Network = mehr Anreiz, User zu gewinnen → schärferer Preiswettbewerb)
- `n₁*` ↑, `n₂*` ↓ (höhere Qualität wirkt stärker, wenn NE stark)
- Profit von Plattform 1: ambiguous (Preis runter aber Menge hoch)
- Profit von Plattform 2: unambiguously ↓

**Intuition:** Network Effects sind **endogene vertikale Differenzierung**. Sie verstärken den Quality-Advantage von Plattform 1 und machen Wettbewerb intensiver — bis hin zu Tipping (wenn `q ≥ 3(τ − β)`).

### REZEPT: Aufgabe 2.2 (Entrant vs. Legacy + Compatibility)

**Setting:** Plattform 2 ist Legacy (free, p_2 = 0). Plattform 1 ist Entrant mit q-Advantage, eigene β_1 (möglicherweise ≠ β_2).

**Schritt 1 — Indifferent Consumer x̂ (mit asymmetrischen β):**
```
x̂ = 1/2 + (q + β₁n₁^e − β₂n₂^e − p₁) / (2τ)
```

**Wichtige Ableitung:** `∂n_i/∂n_i^e = β_i / (2τ)` — direkt sichtbar, dass größeres β_i Tipping wahrscheinlicher macht.

**Schritt 2 — Interior FEE mit Algebra-Heavy Lösung:**

Setze FEE, sammle n₁-Terme auf einer Seite:
```
n₁ = (τ + q − β₂ − p₁) / (2τ − β₁ − β₂)
```

**Schritt 3 — Sign-of-Slope:**

Das Vorzeichen von `dn₁/dp₁` hängt vom Vorzeichen von `2τ − β₁ − β₂` ab:

- Wenn `(β₁+β₂)/2 < τ` ("average NE weak"): Standard, `dn₁/dp₁ < 0`
- Wenn `(β₁+β₂)/2 > τ` ("average NE strong"): Pervers, `dn₁/dp₁ > 0`

**Schritt 4 — Profit-Maximierung (Fall: weak NE):**

```
max_{p₁} (τ + q − β₂ − p₁)/(2τ − β₁ − β₂) · p₁
```

Erste Ableitung = 0:
```
p₁* = (q + τ − β₂)/2
n₁* = (q + τ − β₂)/[2·(2τ − β₁ − β₂)]
π₁* = (q + τ − β₂)² / [4·(2τ − β₁ − β₂)]
```

**Schritt 5 — Komparative Statik in β₂:**

Das ist die schwierige Frage: "Was passiert wenn der Legacy stärkere Network Effects hat?"

- **Price Effect:** `∂p₁*/∂β₂ < 0` (Entrant muss Preis senken)
- **Quantity Effect:** `∂n₁/∂β₂ < 0` für gegebenen p₁ (mehr User wechseln zu Legacy)
- **Net Effect auf n₁*:** ambiguous → wird positiv wenn `β₁ > τ − q` (Entrant hat selbst starkes NE)
- **Net Effect auf π₁*:** kann positiv sein wenn `β₁ > (3τ − q − β₂)/2`

**Intuition:** Wenn Legacy stärker wird, könnte Entrant *theoretisch* profitieren — denn die Attraction-Loop, die Legacy stärkt, fließt auch zum Entrant durch den Preiswettbewerb. Klingt paradox, aber stimmt formal.

**Schritt 6 — Compatibility-Entscheidung (Teil 5):**

Wenn beide Plattformen kompatibel sind, sehen User die Network-Effekte **als gemeinsam** an (`n_1^e = n_2^e = 1` weil alle joinen).

Indifferent consumer wird einfacher:
```
x̂ = (τ + q − p₁)/(2τ)
```

Optimaler Fee:
```
p₁^c* = (τ + q)/2
n₁^c* = (τ + q)/(4τ)
π₁^c* = (τ + q)²/(8τ)
```

**Compatibility-Vergleich:**

- Plattform 1 bevorzugt Compatibility wenn `q < q̂ ≡ √(τ(τ−β))`
- Bei sehr großem q (q > q̂): Entrant ist so stark, dass es lieber seine Network-Größe als Vorteil behält
- Bei kleinem q: Compatibility ist hilfreich (vermeidet "Cold Start"-Nachteil)

**Die zwei Effekte:**

1. **Willingness-to-Pay Effect:** Compatibility = höherer Preis (User mögen die "common" große Netzwerk-Optik) → **immer positiv für Entrant**
2. **Level-Playing-Field Effect:** Compatibility eliminiert den Network-Größen-Vorteil → **negativ für Entrant**, wenn `q > τ − β` (Entrant hätte sonst mehr User)

Für `τ − β < q < q̂`: WTP-Effekt überwiegt, Compatibility immer noch besser.

---

## SET 3 — Two-Sided Monopol, IDENTISCHE User (Divide-and-Conquer)

### Big Picture für Set 3

> **EINE Plattform, ZWEI Sides** (z.B. Uber: Fahrer & Rider). Alle User auf einer Side sind **identisch** → entweder alle joinen oder keiner. Cross-Group Network Effects (CGNE: γ₁, γ₂). Das Chicken-and-Egg-Problem ist hier zentral.

### REZEPT: Aufgabe 3.1 (Divide-and-Conquer Drill)

**Setting:**
```
U₁ = r₁ + γ₁·n₂ − P₁
U₂ = r₂ + γ₂·n₁ − P₂
```
Outside Options `u_1^0, u_2^0`. Costs `c_1, c_2` pro User.

**Schritt 1 — 4 Equilibrium-Konfigurationen testen:**

Weil alle User auf einer Side identisch sind und gemeinsame Outside Option haben, gibt es nur 4 möglichen Configs: `(N₁, N₂), (0, 0), (N₁, 0), (0, N₂)`.

Für jedes Config: "Ist es ein Equilibrium?" = "Hat irgendein User Anreiz, abzuweichen, gegeben die anderen?"

| Config | Bedingung Side 1 | Bedingung Side 2 |
|---|---|---|
| `(N₁, N₂)` | `P₁ ≤ r₁ − u₁⁰ + γ₁N₂` | `P₂ ≤ r₂ − u₂⁰ + γ₂N₁` |
| `(0, 0)` | `P₁ > r₁ − u₁⁰` | `P₂ > r₂ − u₂⁰` |
| `(N₁, 0)` | `P₁ ≤ r₁ − u₁⁰` | `P₂ > r₂ − u₂⁰ + γ₂N₁` |
| `(0, N₂)` | `P₁ > r₁ − u₁⁰ + γ₁N₂` | `P₂ ≤ r₂ − u₂⁰` |

**Pattern zum Verinnerlichen:** Der γ·N-Term steht da, wenn die andere Seite voll joined; verschwindet, wenn 0.

**Schritt 2 — Multiple-Equilibrium-Trap finden:**

Wenn die Plattform Fees in dieser Grauzone setzt:
```
r₁ − u₁⁰ < P₁ ≤ r₁ − u₁⁰ + γ₁N₂
r₂ − u₂⁰ < P₂ ≤ r₂ − u₂⁰ + γ₂N₁
```
... sind **sowohl** `(N₁,N₂)` **als auch** `(0,0)` Equilibria → Coordination Problem!

**Schritt 3 — Divide-and-Conquer (D&C):**

Ziel: `(0,0)` als Equilibrium *eliminieren*.

**Variante A — "Buyer subsidieren" (subsidiere Side 1):**
- Setze `P₁ = r₁ − u₁⁰` (oder leicht darunter) → Side 1 joined unabhängig
- Erhöhe `P₂ = r₂ − u₂⁰ + γ₂·N₁` → Side 2 joined, weil sie Side 1 garantiert vorfindet

**Variante B — "Sellers subsidieren":**
- `P₂ = r₂ − u₂⁰`, dann `P₁ = r₁ − u₁⁰ + γ₁·N₂`

**Schritt 4 — Welche Seite subventionieren?**

```
π_(b) > π_(s)  ⇔  γ_2 > γ_1
```

**Verbal:** Subventioniere die Seite mit **niedriger** Attraction Power. Monetarisiere die mit **hoher** Attraction Power.

**Achtung — Indexverwirrung (häufige Klausurfalle):**
- `γ₁` misst Wirkung von Side 2 **auf** Side 1 (also wie sehr Side 1 von Side 2 angezogen wird)
- Wenn γ₂ groß: Side 2 wird stark von Side 1 angezogen → **subventioniere Side 1**, monetarisiere Side 2

Merksatz: *"Subventioniere die Seite, ohne die die andere nicht kommt; verdiene an der Seite, die nicht weg kann."*

**Schritt 5 — Negative Fees können optimal sein:**

Wenn `r_k < u_k^0` (Outside Option besser als intrinsischer Plattform-Wert) → subsidierte Side hat `P_k* < 0` → Plattform **zahlt** User zum Joinen (Uber-Logik).

**Schritt 6 — Profit-Check:**

```
π_(b) = N_b(r_b − u_b⁰ − c_b) + N_s(r_s − u_s⁰ + γ_s·N_b − c_s)   (Buyer subsidiert)
π_(s) = N_b(r_b − u_b⁰ + γ_b·N_s − c_b) + N_s(r_s − u_s⁰ − c_s)    (Seller subsidiert)
```

Profitabilitätsbedingung:
```
max{γ_b, γ_s} > (u_b⁰ − r_b + c_b)/N_s + (u_s⁰ − r_s + c_s)/N_b
```

**Was macht D&C profitabel?**
- ↑ γ_b, γ_s (Network Effects)
- ↑ N_b, N_s (große Märkte)
- ↑ r_b, r_s (intrinsischer Wert)
- ↓ u_b⁰, u_s⁰ (schlechte Outside Options)
- ↓ c_b, c_s (niedrige Costs)

### Numerisches Beispiel (Aufgabe 3.1 e–i):

Mit N₁=N₂=100, γ₁=3, γ₂=6, r₁=10, r₂=5, u₁⁰=20, u₂⁰=0:

- γ₂ > γ₁ → subventioniere **Side 1**
- `P₁* = r₁ − u₁⁰ = 10 − 20 = −10` (negativer Preis!)
- `P₂* = r₂ − u₂⁰ + γ₂·N₁ = 5 + 6·100 = 605`
- `π* = 100·(−10 − 4) + 100·(605 − 1) = −1400 + 60400 = 59000`

---

## SET 4 — Two-Sided Monopol, HETEROGENE User (Membership Pricing)

### Big Picture für Set 4

> Plattform setzt Membership-Fees P_b, P_s. User auf jeder Seite haben unterschiedliche **Opportunitätskosten τ** (oder unterschiedliche Stand-Alone-Bewertungen r). Continuum-Setup → keine Multiple-Equilibria-Trap, sondern smooth Demand Functions.

### REZEPT: Aufgabe 4.1 (Transaction Fees, numerisch)

**Setting:** Diskret 3 oder 6 User auf jeder Seite, Transaction Fees `a_b, a_s`.

**Schritt 1 — Buyer-Side maximieren:**

Buyer-Surplus: `u_b = (V_b − a_b)·n_s`

Da alle Buyer dieselbe Bewertung haben (homogen), kann Plattform den vollen Surplus auf Buyer-Seite extrahieren: `a_b* = V_b`.

**Schritt 2 — Seller-Side iterieren (Tabelle!):**

Seller i hat Surplus `u_s^i = (V_s^i − a_s)·n_b`. Seller joined nur wenn `V_s^i ≥ a_s`.

→ Mache eine **Tabelle** über mögliche a_s-Werte (von max bis min) und schaue, wie viele Seller joinen (n_s) und was Profit ist.

**Schritt 3 — Den Trick erkennen — Cross-Group Network Effects!**

Wenn du a_s reduzierst:
- ↓ Profit auf Seller-Seite (geringerer a_s pro Transaktion)
- ↑ n_s (mehr Seller joinen)
- ↑ Buyer-Profit, weil `π_b = a_b · n_b · n_s` und n_s steigt → **mehr Transaktionen!**

**Schritt 4 — Iterativ optimieren:**

| a_s | n_s | π_s | π_b (mit a_b·n_b·n_s) | π_total |
|---|---|---|---|---|
| 3 | 1 | 18 | 36 | 54 |
| 2 | 2 | 24 | 72 | 96 |
| 1 | 3 | 18 | 108 | 126 |
| 0 | 4 | 0 | 144 | 144 |
| **−1** | **5** | **−30** | **180** | **150** ← max |
| −2 | 6 | −72 | 216 | 144 |

**→** Manchmal ist es optimal, die Seller zu **subventionieren** (a_s < 0), weil die zusätzlichen Transaktionen auf Buyer-Seite mehr einbringen.

**Take-Away:** *Price Structure is not neutral* — die *Summe* `a_b + a_s` allein bestimmt nicht den Profit, sondern die *Aufteilung*.

### REZEPT: Aufgabe 4.2 (General Membership Fees, Heterogene τ)

**Setting:**
```
u_b = r_b + β_b·n_s − P_b − τ_b,   τ_b ~ U[0,1]
u_s = r_s + β_s·n_b − P_s − τ_s,   τ_s ~ U[0,1]
```

**Schritt 1 — Indifferent Buyer τ̂_b:**
```
r_b + β_b·n_s − P_b − τ̂_b = 0
⇒ τ̂_b = r_b + β_b·n_s − P_b
```
→ Alle Buyer mit `τ_b < τ̂_b` joinen → `n_b = τ̂_b = r_b + β_b·n_s − P_b`

Analog: `n_s = r_s + β_s·n_b − P_s`

**Schritt 2 — System lösen (Substitution):**

Setze n_s aus zweiter Gleichung in erste:
```
n_b = r_b + β_b(r_s + β_s·n_b − P_s) − P_b
n_b(1 − β_b·β_s) = (r_b − P_b) + β_b(r_s − P_s)
n_b = [(r_b − P_b) + β_b(r_s − P_s)] / (1 − β_b·β_s)
```
Analog: `n_s = [(r_s − P_s) + β_s(r_b − P_b)] / (1 − β_b·β_s)`

**Schritt 3 — Intuition vor Profit-Maximierung:**

Beachte: `∂n_b/∂P_s < 0` — wenn Plattform Seller-Preis erhöht, sinken nicht nur n_s sondern auch n_b (weil Buyer Seller wollen!) — **Cross-Group-Externalität**.

**Schritt 4 — Profit-Maximierung:**
```
π = P_b·n_b + P_s·n_s
```

2 FOCs gleichzeitig. Nach viel Algebra:
```
P_b* = [r_b(2 − β_b·β_s − β_s²) + (β_b − β_s)·r_s] / [4 − (β_b + β_s)²]
P_s* = [r_s(2 − β_b·β_s − β_b²) + (β_s − β_b)·r_b] / [4 − (β_b + β_s)²]
```

(In der Klausur muss man das vermutlich nicht auswendig — aber den Weg dorthin schon.)

**Schritt 5 — Wann zahlt Buyer weniger?**
```
P_b* < P_s*  ⇔  (1 − β_s)·r_b < (1 − β_b)·r_s
```

Zwei Spezialfälle:

- **Gleiche Stand-Alone (r_b = r_s):** `P_b* < P_s* ⇔ β_s > β_b` → "Seite mit größerer Attraction Power zahlt mehr"
- **Gleiche β (β_b = β_s):** `P_b* < P_s* ⇔ r_b < r_s` → "Seite mit niedrigerer intrinsischer Bewertung zahlt weniger"

### REZEPT: Aufgabe 4.3 (Spezifische Zahlen)

**Wenn β_b = 4/5, β_s = 1/5, r_b = r_s = 1/2:**

**Schritt 1 — Konkrete Demands:**
```
n_B = 1/2 + (4/5)·n_S − P_B
n_S = 1/2 + (1/5)·n_B − P_S
```

**Schritt 2 — System lösen:**
```
n_B = (5/21)·(9/2 − 5P_B − 4P_S)
n_S = (5/21)·(3 − P_B − 5P_S)
```

**Schritt 3 — Profit & FOCs:**
```
P_B* = 2/5,   P_S* = 1/10
n_B* = 1/2,   n_S* = 1/2
π*   = 1/4
```

**Interpretation:** Seller zahlt weniger (1/10 < 2/5), weil Seller-Attraction-Power (β_b = 4/5) **größer** ist als Buyer-Attraction-Power (β_s = 1/5). Sellers ziehen Buyers stärker an → Plattform investiert (subventioniert) in Seller, um Buyer zu attractionen.

### REZEPT: Aufgabe 4.4 (Stand-Alone Heterogenität statt τ)

**Hier:** Heterogenität sitzt in `r_b, r_s ~ U[0,1]`, nicht in τ.

**Schritt 1 — Indifferent **r-Wert**:**
```
r̂_B + (1/4)·n_S − P_B = 0
⇒ r̂_B = P_B − (1/4)·n_S
```
Konsumenten mit `r_B > r̂_B` joinen (im Gegensatz zu Set 4.2, wo τ̂_b die *Obergrenze* war):
```
n_B = 1 − r̂_B = 1 − P_B + (1/4)·n_S
```

**→ Genau dasselbe Rezept wie 4.2**, nur das Vorzeichen ist umgekehrt.

**Final-Antworten:**
```
P_S* = 3/5,   P_B* = 2/5
n_S* = 4/5,   n_B* = 4/5
π*   = 4/5
```

**Side mit lower Fee:** **Buyer** zahlt weniger, weil Buyer-Side größere Attraction Power exert (β = 1/2 > 1/4).

---

## KOMPAKT — Welche Operation für welche Aufgabe?

| Aufgabe enthält... | Mache zuerst... |
|---|---|
| "two consumers Anna & Bruno" | Normal-form 2×2 Matrix, alle 4 Cells als mögliche Equilibria checken |
| "Continuum θ uniformly distributed, U(θ) = θV + ..." | Setze U(θ̂) = 0, löse nach θ̂, `n = 1 − θ̂` |
| "Continuum mit Heterogenität im β-Term: U(θ) = V + θβn^e" | Setze U(θ̂) = 0, dann quadratische FEE-Gleichung |
| "Two platforms with Hotelling, U=V−τx+βn^e..." | Indifferent x̂ aus U₁=U₂, dann 3 FEE-Kandidaten |
| "Two-sided platform, N_b identische Buyers, N_s identische Sellers" | 4 Equilibrium-Configurationen testen → D&C |
| "Two-sided, τ_b ~ U[0,1], heterogene Opp.Kosten" | Indifferent τ̂_b, System lösen (Substitution), FOCs |

---

## Universal-Checkliste vor jeder Modellrechnung

1. ✅ **Lies das Setup zweimal.** Welche Variablen sind exogen, welche endogen?
2. ✅ **Zeichne das Schema:** Wie viele Sides? Homogen oder heterogen? Network Effect within oder cross?
3. ✅ **Schreibe die Utility-Funktion(en) hin** (Sub 1)
4. ✅ **Finde Indifferent User** (θ̂ oder x̂ oder τ̂) → Demand-Funktion in n^e
5. ✅ **Impose FEE** `n^e = n` → reine Demand-Funktion in p
6. ✅ **Falls Plattform:** Schreibe Profit `π = (p−c)·n` oder mehrdimensional
7. ✅ **FOC** `∂π/∂p = 0` lösen
8. ✅ **Einsetzen** zurück → p*, n*, π*
9. ✅ **Plot oder Tabelle** um Multiple Equilibria zu erkennen
10. ✅ **Komparative Statik:** Was passiert, wenn β ↑, τ ↑, q ↑?

---

## Häufige Klausurfehler (Liste)

| Fehler | Korrekt |
|---|---|
| Vergessen, FEE zu imposen | Bei Demand-Modellen IMMER `n^e = n` setzen |
| β und τ in Hotelling verwechseln | β = Network-Effekt (vertikal-endogen); τ = Differenzierung (horizontal) |
| Subventions-Regel-Indizes vertauschen | `π_(b) > π_(s) ⇔ γ_s > γ_b` (Index der **wirkenden** Seite) |
| Stabilität ignorieren | Bei multiple FEEs immer die *unstable critical mass* benennen |
| "Compatibility immer besser" | NEIN — kommt auf `q` vs. `q̂ = √(τ(τ−β))` an |
| "Demand IMMER decreasing in p" | NEIN — bei strong NE kann demand upward-sloping sein |
| Tipping ignorieren | Wenn `β > τ`, kann Markt tippen — explizit erwähnen |

---

## Verwandt

- [[20.studies/Organizational-Economics/plattformen-network-effects]] — Theorie der WGNE/CGNE
- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]] — Detail zu D&C
- [[20.studies/Organizational-Economics/formelsammlung-cheatsheet]] — alle Formeln auf einen Blick
- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — die ökonomische Story
- [[20.studies/Organizational-Economics/Hub]]
