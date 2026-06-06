---
source: claude-import + 2026-06-06 notes
imported: 2026-06-01
updated: 2026-06-06
conv_uuids: [c64ee9d8-3770-4fe2-9111-0851866733df, e4dd2cab-a348-4a94-a9a2-57fd4c6a0174, c7dfb788-465f-421f-8e0c-1171cb2ca585, 7168948c-3faa-41d2-abf1-7c6124bd9495]
tags: [organizational-economics, two-sided-markets, hotelling, pricing, divide-and-conquer]
---

# Two-Sided Markets — Pricing, Divide-and-Conquer, Hotelling

> **2026-06-06 Note:** Diese Notiz deckt die *grundlegende* Modell-Logik von Set 2 (Hotelling) und Set 3 (D&C). Für **Schritt-für-Schritt-Rezepte** zu jeder Aufgabe → siehe [[20.studies/Organizational-Economics/problem-set-recipes]]. Für die **ökonomische Intuition** → siehe [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]].

## Problem

Plattform-Pricing-Aufgaben sind die häufigste Modellrechnung in OE-Klausuren. Die Aufgabe ist immer dieselbe Struktur:

1. Nutzen-Funktionen pro Seite aufschreiben
2. Gleichgewichtsbedingungen für die 4 Konfigurationen prüfen ((N_b, N_s), (N_b, 0), (0, N_s), (0, 0))
3. Multiple-Equilibrium-Trap erkennen
4. Divide-and-Conquer anwenden
5. Optimale Fees berechnen + Profitabilitätsbedingung prüfen

Typische Klausur-Falle: das **β mit gekreuzten Indizes** (β_s misst Wirkung von Sellers auf Buyers — Index ist die wirkende Seite).

## Lösung

### Formal Model Setup (Kurs-Standard)

Plattform versucht, Buyers und Sellers anzuziehen. Es gibt N_b Buyers und N_s Sellers (jeweils ≥ 2).

Wenn n_b Buyers und n_s Sellers joinen:

$$
u_b = r_b + \beta_b \cdot n_s - P_b
$$

$$
u_s = r_s + \beta_s \cdot n_b - P_s
$$

| Symbol | Bedeutung |
|---|---|
| r_b, r_s | Stand-Alone-Nutzen (Wert der Plattform ohne andere Seite) |
| β_b, β_s | Cross-Group-Network-Effect-Intensität |
| P_b, P_s | Access-Fee (Plattform-Preis) |
| u_b^0, u_s^0 | Outside Option (auch negativ möglich) |
| c_b, c_s | Grenzkosten der Plattform pro zusätzlichem User |

### Schritt 1 — Vier Equilibrium-Konfigurationen prüfen

Weil alle Buyers (bzw. Sellers) identisch sind und Outside Option konstant ist, **machen alle Buyers dieselbe Entscheidung** (all or none). Vier Kandidaten-Gleichgewichte:

| Konfig | Buyer-Bedingung | Seller-Bedingung |
|---|---|---|
| (N_b, N_s) | P_b ≤ r_b − u_b^0 + β_b · N_s | P_s ≤ r_s − u_s^0 + β_s · N_b |
| (0, 0) | P_b > r_b − u_b^0 | P_s > r_s − u_s^0 |
| (N_b, 0) | P_b ≤ r_b − u_b^0 | P_s > r_s − u_s^0 + β_s · N_b |
| (0, N_s) | P_b > r_b − u_b^0 + β_b · N_s | P_s ≤ r_s − u_s^0 |

**Pattern zum Verinnerlichen:** Der β-Term trägt N (volle Partizipation der anderen Seite) **nur** dann, wenn die andere Seite voll joined. Wenn die andere Seite bei 0 ist, verschwindet der Netzwerkbonus aus der Bedingung.

### Schritt 2 — Multiple-Equilibrium-Trap

Es gibt einen **Preisbereich**, in dem sowohl (N_b, N_s) **als auch** (0, 0) Gleichgewichte sind:

$$
r_b - u_b^0 < P_b \le r_b - u_b^0 + \beta_b N_s
$$
$$
r_s - u_s^0 < P_s \le r_s - u_s^0 + \beta_s N_b
$$

In dieser „Grauzone" hängt das Outcome an **Erwartungen**: Wenn alle erwarten, dass beide Seiten joinen → (N_b, N_s). Wenn alle erwarten, dass niemand kommt → (0, 0). Reines Koordinationsproblem („chicken and egg").

### Schritt 3 — Divide-and-Conquer (das zentrale Pricing-Pattern)

Um (0, 0) als Gleichgewicht **zu eliminieren**, setze mindestens eine Fee so, dass eine Seite **unabhängig** von der anderen joined.

**Variante 1 — Subsidize Buyers, Conquer Sellers:**

- Setze P_b = r_b − u_b^0 → alle Buyers joinen, egal ob Sellers da sind
- Dann erhöhe P_s = r_s − u_s^0 + β_s · N_b → Sellers joinen, weil sie wissen, Buyers sind garantiert

**Variante 2 — Subsidize Sellers (z.B. Uber zahlt Fahrer):**

- Setze P_s = r_s − u_s^0 → alle Sellers joinen
- Dann erhöhe P_b = r_b − u_b^0 + β_b · N_s

### Welche Seite subventionieren?

**Zentrale Entscheidungsregel:**

> Subsidize the side with the **WEAKER attraction power**; monetize the side with the **STRONGER attraction power**.

Formal: π_(b) > π_(s) ⇔ β_s > β_b.

**Achtung — die Indizes sehen verdreht aus, das ist die häufigste Klausur-Falle:**

- β_s misst, wie stark **Buyers Sellers anziehen** (Seller wertet jeden Buyer mit β_s).
- Wenn β_s groß: Sellers sind leicht von Buyers angezogen → Plattform sollte **zuerst Buyers sichern** (subventionieren) und **dann Sellers monetarisieren**.
- Die Seite mit der größeren *Attraction Power* (die also leichter andere anzieht) wird monetarisiert; die Seite, die diese Anziehung *ausübt*, wird subventioniert.

**Merksatz:** Verdiene Geld bei der Seite, die der anderen Seite egal nicht ist; subventioniere die Seite, ohne die die andere nicht kommt.

### Wenn Subsidien zu Verlusten werden

Wenn r_k < u_k^0 (Outside Option > intrinsischer Plattform-Nutzen) → optimale Subsidy-Fee P_k = r_k − u_k^0 **< 0**: Plattform **zahlt** Nutzer fürs Joinen.

Das ist die Uber-Logik: Fahrer wurden anfangs mit garantierten Stundenlöhnen geködert → Plattform machte auf Fahrer-Seite Verlust, verdiente das auf Fahrgast-Seite zurück.

**Profitabilitätsbedingung:**

$$
\max\{\pi_{(b)}, \pi_{(s)}\} > 0 \iff \max\{\beta_b, \beta_s\} > \frac{u_b^0 - r_b + c_b}{N_s} + \frac{u_s^0 - r_s + c_s}{N_b}
$$

Divide-and-Conquer ist profitabler bei:

- Stärkeren Cross-Group-Effects (β_b, β_s, N_b, N_s ↑)
- Größeren intrinsischen Vorteilen (r_b, r_s ↑)
- Kleineren Outside Options (u_b^0, u_s^0 ↓)
- Niedrigeren Grenzkosten (c_b, c_s ↓)

### Numerische Worked-Example-Routine (Problemset-Standard)

1. Werte in die 4 Equilibrium-Bedingungen einsetzen → Trap-Region identifizieren
2. β-N-Vergleich → welche Seite hat größere Attraction Power
3. Subsidized Side: P_k* = r_k − u_k^0 (ggf. negativ)
4. Monetized Side: P_(−k)* = r_(−k) − u_(−k)^0 + β_(−k) · N_k
5. Equilibrium-Utilities + Profit berechnen
6. Profitabilitätsbedingung verifizieren

### Hotelling mit Network Effects (verwandte Aufgabe)

Wenn Konsumenten heterogen über `x ∈ [0, 1]` verteilt sind, Plattform 1 hat Vorteil q, Differenzierung τ:

- U(x) = V + q − τx + β · n_1^e − p_1 (bei Joinen Plattform 1)
- U(x) = V − τ(1 − x) + β · n_2^e − p_2 (bei Joinen Plattform 2)

Indifferenter Konsument: x̂ = 1/2 + (β(n_1^e − n_2^e) + q + p_2 − p_1) / (2τ).

Mit n_1 = x̂, n_2 = 1 − x̂ → Gleichgewicht lösen via Fixpunkt (Rational Expectations: n_i^e = n_i).

Quality-Difference ist **endogen** (entsteht durch Konsumentenentscheidung). Mit großem β → Markt tippt → eine Plattform kassiert alles.

### Tipping-Beispiel (WhatsApp/Signal)

Signal-Fan joined WhatsApp wenn:

$$
0 + n_W^t \ge 50 + n_S^t \iff n_W^t - n_S^t \ge 50
$$

Sobald WhatsApp ≥ 50 mehr User hat, kippt der Markt zu seinen Gunsten — der Netzwerk-Vorteil schlägt den Stand-Alone-Nachteil (50 Punkte).

## Wann nicht

- **Bei one-sided Märkten:** Klassische Mikro reicht — kein Bedarf für Cross-Side-Pricing.
- **Bei Plattformen mit drei oder mehr Seiten** (z.B. Search + Advertiser + Publisher): Das 2-Sided-Framework muss erweitert werden, einfache D&C-Regel reicht nicht.
- **Bei stark heterogenen Konsumenten:** Mean-Field-Annahme (alle Sellers identisch) bricht — du brauchst Verteilungen.
- **Wenn Plattform Marktmacht nicht endogen vertreidigen kann:** Bei free entry der Plattformen sind D&C-Profite kompetitiv weg-erodiert — andere Marktstruktur.

## Verwandt

- [[20.studies/Organizational-Economics/plattformen-network-effects]] — Theoretische Grundlagen
- [[20.studies/Organizational-Economics/identifikationsstrategien]] — Empirisch CGNE messen
- [[30.patterns/text-formatting/unicode-subscript-konvertierung]] — wenn du `n_W^t` lesbar machen willst
- [[20.studies/Organizational-Economics/_conversation-index]]
