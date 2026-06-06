---
created: 2026-06-06
type: cheatsheet
source: ME 3 Aguiar VL + Exercise Sets 1–4
tags: [organizational-economics, formelsammlung, cheatsheet, klausur]
status: master
---

# Formelsammlung — alle Modelle auf einen Blick

> **Use:** Klausur-Vorbereitung, schnelle Erinnerungsstütze. Jede Formel mit (a) wann sie gilt, (b) was sie ökonomisch bedeutet.

---

## 1. Notation (durchgängig)

| Symbol | Bedeutung |
|---|---|
| `V`, `V_A`, `V_B` | Stand-Alone-Bewertung (=Wert ohne andere User) |
| `β` | Within-Group Network Effect-Intensität (Set 1, 2) |
| `β_b, β_s` | Cross-Group NE: Wirkung auf Buyer/Seller (Set 4) |
| `γ_1, γ_2` | Cross-Group NE: Wirkung auf Side 1/2 (Set 3) |
| `n^e` | Erwartete Network-Größe (vor FEE-Auflösung) |
| `n, n_b, n_s, n_1, n_2` | Realisierte Network-Größe |
| `p` | Plattform-Preis (Membership Fee, ein-seitig) |
| `P_b, P_s` | Membership Fee für Buyer/Seller |
| `a_b, a_s` | Transaction Fee (Set 4.1) |
| `r_b, r_s` | Stand-Alone-Bewertung pro Side |
| `u_b^0, u_s^0` | Outside Option pro Side |
| `c, c_b, c_s` | Marginal-Cost pro User |
| `θ ∈ [0,1]` | Heterogenität-Parameter Continuum-Setup |
| `τ` | Hotelling-Transportkosten (horizontale Differenzierung) |
| `q` | Vertikaler Qualitätsvorteil von Pl. 1 |
| `x̂, θ̂, τ̂` | Indifferent-User-Schwelle |

---

## 2. SET 1 — One-Sided, Single Platform

### 1.1 Two Discrete Consumers

```
U_A = V_A + β·𝟙_{B joins} − p
U_B = V_B + β·𝟙_{A joins} − p
```

**Schwellenwerte für Equilibria (V_A > V_B):**

| Equilibrium | Bedingung |
|---|---|
| `(Buy, Buy)` | `p ≤ V_B + β` |
| `(Don't, Don't)` | `p > V_A` |
| `(Buy, Don't)` | `V_B + β < p < V_A` (existiert nur wenn `β < V_A − V_B`) |
| `(Don't, Buy)` | nie |

**Multiple Equilibria-Region** (starker NE):
```
β > V_A − V_B   ⇒   for V_A < p < V_B + β :  N ∈ {0, 2}
```

### 1.2 Continuum, heterogene Stand-Alone

```
U(θ) = θV + βn^e − p,   θ ~ U[0,1]
```

**Indifferent Consumer:**
```
θ̂ = (p − βn^e)/V
```

**Demand (pre-FEE):**
```
n(p, n^e) = 1 − θ̂ = 1 − (p − βn^e)/V
```

**FEE-Demand (n^e = n):**
```
n(p) = (V − p)/(V − β)        if 0 < n < 1
```

**Eckpunkte:**
- `n = 1` if `p ≤ β`
- `n = 0` if `p ≥ V`

**Inverse Demand:**
```
p(n) = V − (V − β)·n
```

**Demand-Form:**
- `V > β` (weak NE) → downward-sloping, unique
- `V < β` (strong NE) → upward-sloping, multiple FEE

### 1.3 Continuum, heterogene Network-Bewertung

```
U(θ) = V + θβn^e − p,   θ ~ U[0,1]
```

**Indifferent Consumer:**
```
θ̂ = (p − V)/(βn^e)
```

**Inverse Demand (FEE):**
```
p(n) = V + βn(1 − n)
```

→ **Inverse-U-Shape**, Maximum bei `n = 1/2`, `p_max = V + β/4`.

**3 FEE für `V < p < V + β/4`:**
```
n_0 = 0
n_1 = 1/2 − √(1/4 − (p−V)/β)     ← unstable critical mass
n_2 = 1/2 + √(1/4 − (p−V)/β)     ← stable success
```

---

## 3. SET 2 — One-Sided Competition (Hotelling + NE)

### 2.1 Symmetric Hotelling mit NE

```
U(x) = V + q − τx + βn_1^e − p_1      (joining Pl. 1)
U(x) = V − τ(1−x) + βn_2^e − p_2     (joining Pl. 2)
```

**Indifferent Consumer:**
```
x̂ = 1/2 + (p_1 − p_2 − q)/[2(β − τ)]
```

(oder äquivalent mit (τ−β) im Nenner — Vorzeichen drehen!)

**Drei mögliche FEE:**

| Configuration | FEE-Bedingung |
|---|---|
| All join Pl. 1 | `p_1 − p_2 ≤ q + β − τ` |
| All join Pl. 2 | `p_1 − p_2 ≥ q − (β − τ)` |
| Interior | beide oben verletzt |

**Interior Demand mit FEE:**
```
n_1 = 1/2 + (q + p_2 − p_1)/[2(τ − β)]
n_2 = 1 − n_1
```

**FOC-Reaction-Functions:**
```
p_1(p_2) = (τ − β + p_2 + q)/2
p_2(p_1) = (τ − β + p_1 − q)/2
```

**Equilibrium:**
```
p_1* = c + τ − β + q/3
p_2* = c + τ − β − q/3
n_1* = 1/2 + q/[6(τ − β)]
n_2* = 1/2 − q/[6(τ − β)]
```

(Mit Marginal-Cost c = 0 entfällt der c-Term.)

**No-Tipping-Bedingung:**
```
q < 3(τ − β)
```

### 2.2 Hotelling mit asymmetric NE (Entrant vs. Legacy)

```
U(x) = V + q − τx + β_1·n_1^e − p_1   (joining new platform 1)
U(x) = V − τ(1−x) + β_2·n_2^e         (staying on legacy, p_2 = 0)
```

**Indifferent Consumer:**
```
x̂ = 1/2 + (q + β_1·n_1^e − β_2·n_2^e − p_1)/(2τ)
```

**Sensitivität:**
```
∂n_i/∂n_i^e = β_i/(2τ)
```
→ Tipping wahrscheinlicher wenn `β_i/(2τ)` groß.

**FEE-Bedingungen:**

| Configuration | FEE-Bedingung |
|---|---|
| All join new (n_1 = 1) | `p_1 ≤ q + β_1 − τ` |
| All stay legacy (n_2 = 1) | `p_1 ≥ q − β_2 + τ` |
| Interior | beide verletzt |

**Interior FEE-Demand:**
```
n_1 = (τ + q − β_2 − p_1)/(2τ − β_1 − β_2)
n_2 = (τ − q − β_1 + p_1)/(2τ − β_1 − β_2)
```

**Sign-Slope:** `dn_1/dp_1 < 0` iff `(β_1+β_2)/2 < τ` (weak NE im Durchschnitt).

**Optimal Fee (Weak-NE-Fall):**
```
p_1* = (q + τ − β_2)/2
n_1* = (q + τ − β_2)/[2(2τ − β_1 − β_2)]
π_1* = (q + τ − β_2)²/[4(2τ − β_1 − β_2)]
```

### 2.2 (Teil 5) Compatibility

Bei Compatibility (`β_1 = β_2 = β`, beide Networks "shared"):
```
x̂ = (τ + q − p_1)/(2τ)
p_1^c* = (τ + q)/2
n_1^c* = (τ + q)/(4τ)
π_1^c* = (τ + q)²/(8τ)
```

**Profit Compare:**
```
π_1^c* > π_1*  ⇔  q < q̂ ≡ √(τ(τ − β))
```

---

## 4. SET 3 — Two-Sided Monopol, Identische User

### Setup
```
U_1 = r_1 + γ_1·n_2 − P_1
U_2 = r_2 + γ_2·n_1 − P_2
```

### 4 Equilibrium-Configurationen

| Config | Bedingung Side 1 | Bedingung Side 2 |
|---|---|---|
| `(N_1, N_2)` | `P_1 ≤ r_1 − u_1^0 + γ_1·N_2` | `P_2 ≤ r_2 − u_2^0 + γ_2·N_1` |
| `(0, 0)` | `P_1 > r_1 − u_1^0` | `P_2 > r_2 − u_2^0` |
| `(N_1, 0)` | `P_1 ≤ r_1 − u_1^0` | `P_2 > r_2 − u_2^0 + γ_2·N_1` |
| `(0, N_2)` | `P_1 > r_1 − u_1^0 + γ_1·N_2` | `P_2 ≤ r_2 − u_2^0` |

### Multiple-Equilibria-Trap-Region

```
r_1 − u_1^0 < P_1 ≤ r_1 − u_1^0 + γ_1·N_2
r_2 − u_2^0 < P_2 ≤ r_2 − u_2^0 + γ_2·N_1
```
→ beide `(N_1, N_2)` und `(0, 0)` sind Equilibria.

### Divide-and-Conquer

**Variante A — Subsidize Side 1:**
```
P_1* = r_1 − u_1^0
P_2* = r_2 − u_2^0 + γ_2·N_1
```

**Variante B — Subsidize Side 2:**
```
P_2* = r_2 − u_2^0
P_1* = r_1 − u_1^0 + γ_1·N_2
```

### Welche Seite subsidieren?

```
π_(b) > π_(s)   ⇔   γ_s > γ_b   (Index = wirkende Seite)
```

Verbal: Subsidiere die Seite mit **niedrigerer Attraction Power**.

### Profit pro D&C-Variante

```
π_(b) = N_b·(r_b − u_b^0 − c_b) + N_s·(r_s − u_s^0 + γ_s·N_b − c_s)
π_(s) = N_b·(r_b − u_b^0 + γ_b·N_s − c_b) + N_s·(r_s − u_s^0 − c_s)
```

### Profitabilitätsbedingung

```
max{π_(b), π_(s)} > 0
⇔ max{γ_b, γ_s} > (u_b^0 − r_b + c_b)/N_s + (u_s^0 − r_s + c_s)/N_b
```

---

## 5. SET 4 — Two-Sided Monopol, Heterogene User

### 4.1 Transaction Fees (Numerisch)

```
u_b = (V_b − a_b)·n_s
u_s^i = (V_s^i − a_s)·n_b
π = (a_b + a_s)·n_b·n_s
```

→ Lösen via **Tabelle**: Iteriere über mögliche (a_b, a_s), berechne (n_b, n_s, π).

**Key Insight:** Subsidieren einer Seite (a_s < 0) kann optimal sein, weil mehr n_s ⇒ mehr Transaktionen ⇒ mehr Profit auf Buyer-Seite.

### 4.2 Membership Fees, allgemein

**Setup:**
```
u_b = r_b + β_b·n_s − P_b − τ_b,   τ_b ~ U[0,1]
u_s = r_s + β_s·n_b − P_s − τ_s,   τ_s ~ U[0,1]
```
Assumption: `β_b·β_s < 1`.

**Indifferent Users:**
```
τ̂_b = r_b + β_b·n_s − P_b
τ̂_s = r_s + β_s·n_b − P_s
```

**Demand (n_b = τ̂_b, n_s = τ̂_s):**
```
n_b = [(r_b − P_b) + β_b(r_s − P_s)] / (1 − β_b·β_s)
n_s = [(r_s − P_s) + β_s(r_b − P_b)] / (1 − β_b·β_s)
```

**FOC:**
```
∂π/∂P_b = 0:   (r_b − 2P_b) + β_b·r_s − P_s(β_b + β_s) = 0
∂π/∂P_s = 0:   (r_s − 2P_s) + β_s·r_b − P_b(β_b + β_s) = 0
```

**Optimal Fees:**
```
P_b* = [r_b·(2 − β_b·β_s − β_s²) + (β_b − β_s)·r_s] / [4 − (β_b + β_s)²]
P_s* = [r_s·(2 − β_b·β_s − β_b²) + (β_s − β_b)·r_b] / [4 − (β_b + β_s)²]
```

**Optimal Quantities:**
```
n_b* = [2r_b + (β_b + β_s)·r_s] / [4 − (β_b + β_s)²]
n_s* = [2r_s + (β_b + β_s)·r_b] / [4 − (β_b + β_s)²]
```

**Optimal Profit:**
```
π* = [r_b² + r_s² + r_b·r_s·(β_b + β_s)] / [4 − (β_b + β_s)²]
```

**Buyer-Pays-Less-Condition:**
```
P_b* < P_s*   ⇔   (1 − β_s)·r_b < (1 − β_b)·r_s
```

Spezialfälle:
- `r_b = r_s` → `β_s > β_b` (Side mit stärkerer Attraction zahlt mehr)
- `β_b = β_s` → `r_b < r_s` (Side mit niedrigerem Stand-Alone zahlt weniger)

### 4.3 Konkrete Zahlen (β_b=4/5, β_s=1/5, r_b=r_s=1/2)

```
P_S* = 1/10,   P_B* = 2/5
n_B* = n_S* = 1/2
π*   = 1/4
```

### 4.4 Heterogene Stand-Alone (statt τ)

**Setup:**
```
u_b = r_b + β_b·n_s − P_b,   r_b ~ U[0,1]
u_s = r_s + β_s·n_b − P_s,   r_s ~ U[0,1]
```

**Indifferent Users (jetzt joinen die mit `r > r̂`):**
```
r̂_b = P_b − β_b·n_s
n_b = 1 − r̂_b = 1 − P_b + β_b·n_s
```

Analog für s.

### 4.4 Konkrete Zahlen (β_b=1/4, β_s=1/2)

```
P_S* = 3/5,   P_B* = 2/5
n_B* = n_S* = 4/5
π*   = 4/5
```

---

## 6. Pricing Allgemein — Lerner-Index für Plattformen

### Standard-Monopol
```
(p − c)/p = 1/η   (Inverse Elastizität)
```

### Two-Sided-Plattform
```
P_s = c_s − β_b·n_b + N_s(u_s)/N_s'(u_s)
P_b = c_b − β_s·n_s + N_b(u_b)/N_b'(u_b)
```

→ Preise **adjustiert nach unten** durch Network-Effekt-Externalität auf der anderen Seite, **nach oben** durch eigene Sensitivität.

**Verbal:** Markup ist niedriger auf der Seite, wo (a) die Elastizität hoch ist (b) der Cross-Group-Effekt auf die andere Seite groß ist.

---

## 7. Konzeptuelle Faustregeln

| Frage | Faustregel |
|---|---|
| Wann tippt der Markt? | Wenn `β > τ` (NE > Differenzierung) UND `q > 3(τ − β)` |
| Welche Seite subsidieren? | Die mit niedriger Attraction-Power oder hoher Preissensitivität |
| Wann ist Compatibility besser für Entrant? | Wenn `q < q̂ = √(τ(τ − β))` |
| Wann existiert Multiple FEE? | Bei Continuum-Setup wenn `V < β` oder `(β_1+β_2)/2 > τ` |
| Wann ist D&C profitabel? | Wenn `max{γ_b, γ_s}` groß genug (siehe Profit-Bedingung) |
| Wann disintermediation? | Hohe Trxn-Fee, repeated trxns, in-person, leicht zu kommunizieren |

---

## 8. Komparative Statik — Quick Reference

### Stärkeres β (NE-Intensität ↑) bewirkt...

| In Setup | Effekt |
|---|---|
| Set 1 (one-sided) | Trap-Region wächst, Multiple Eq. wahrscheinlicher |
| Set 2 (Hotelling) | Prices ↓ (mehr Wettbewerb), n₁ ↑ (NE = endogene Qualität), Markt eher tippen |
| Set 3 (2-sided D&C) | D&C profitabler |
| Set 4 (Membership) | Optimaler P niedriger auf Side mit hoher Attraction |

### Größerer τ (Differenzierung ↑)

- Schwächt NE relativ → weniger Tipping
- Höhere Marktpreise (Hotelling)

### Größerer q (Qualitätsvorteil Pl. 1)

- Plattform 1 gewinnt mehr Marktanteil
- Plattform 1 preferiert tendenziell Incompatibility
- Mehr Tipping-Risiko zugunsten Pl. 1

---

## Verwandt

- [[20.studies/Organizational-Economics/problem-set-recipes]] — Wie man die Formeln anwendet
- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Die ökonomische Story
- [[20.studies/Organizational-Economics/Hub]]
