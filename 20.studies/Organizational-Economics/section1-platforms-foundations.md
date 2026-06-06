---
created: 2026-06-06
type: section-deep-dive
source: ME 3 Aguiar VL Section 1 (Parts 1, 2, 3)
tags: [organizational-economics, section1, plattform-definition, network-effects, typologie]
status: master
---

# Section 1 — Plattformen: Definitionen und Kernkonzepte

> **Big Picture:** Plattformen sind kein Marketing-Buzzword, sondern eine **spezifische Organisationsform** mit eigenständiger ökonomischer Logik. Diese Section legt die Definitionen fest, die für ALLES Folgende essenziell sind: Was ist eine Plattform? Welche Network Effects gibt es? Wie klassifiziere ich sie?

---

## Roadmap

1. Definition und Wert von Plattformen
2. Offline vs. Online — warum digitale Plattformen explodieren
3. Network Effects — Definitionen und Beispiele (das Herzstück)
4. Typologie der Plattformen

---

## 1. Definition und Wert von Plattformen

### Die UZH-Definition (auswendig!)

> Eine **Plattform** ist eine Entität, die ökonomische Agenten zusammenbringt **UND** Netzwerkeffekte zwischen ihnen **aktiv managt**, wodurch sie Wert für alle Teilnehmer schafft.

**ZWEI Bedingungen, beide notwendig:**

1. **Network Effects existieren** zwischen den Agenten
2. Die Entität **managt diese Effekte aktiv** (Pricing, Rating, Algorithm, Moderation, etc.)

### Warum brauchen User eine Plattform?

Klassische Frage: Wenn Agent A und Agent B beide von ihrer Interaktion profitieren — warum suchen sie sich nicht selbst?

**Antwort: Transaktionskosten.** Sich gegenseitig zu finden, zu verifizieren, zu bezahlen ist teuer. Plattformen reduzieren diese Kosten.

**Beispiel — Ride-Sharing:**

| Vor BlaBlaCar (Hitchhiking) | Mit BlaBlaCar |
|---|---|
| Hohe Such-/Matching-Kosten (am Strassenrand stehen) | Match via App |
| Trust-Problem (Wer ist der Fahrer?) | Profile, Reviews, Verifikation |
| Selten erfolgreiche Trxns | Hohe Trxn-Frequenz |

**→ Plattform-Wert = Transaktionskosten-Reduktion + Network-Effekt-Management.**

### Illustration: Was passiert ohne Plattform?

**Austin, Texas, Mai 2016:** Uber und Lyft zogen sich nach einer Regulierung zurück. User versuchten, sich via **Facebook-Gruppen** zu reorganisieren:
- Riders posteten Location + Destination
- Drivers connecteten via Hashtags
- Bezahlung via PayPal/Venmo

→ Funktionierte teilweise, war aber **massiv ineffizienter**: keine Sicherheits-Checks, ungeregelte Bezahlung, keine Dispatch-Logik.

**Lehre:** Eine Plattform addiert systematischen Wert (Trust, Matching, Coordination), den Ad-hoc-Lösungen nicht replizieren können.

### Plattform-Definition — was sie NICHT ist

| Entität | Plattform? | Warum nicht? |
|---|---|---|
| **Supermarkt** | ❌ Nein | Bringt zusammen, aber **managt keine NE** |
| **Esperanto** | ❌ Nein | Hat NE (mehr Sprecher = nützlicher), aber **keine Entity managt** sie aktiv |
| **Pure Reseller (Amazon 1995)** | ❌ Nein | Kein Marktplatz — Amazon kauft & verkauft direkt |

| Entität | Plattform? | Warum? |
|---|---|---|
| **Uber** | ✅ Ja | Match + Pricing + Rating (Algorithm-Management) |
| **Wikipedia** | ✅ Ja | Aktive Moderation, Reader-Writer-Interaktion |
| **Amazon Marketplace (seit 2001)** | ✅ Ja | Match + Reviews + Recommendation |
| **Netflix** | ✅ Eingeschränkt | One-sided platform mit WGNE via Recommendation |

---

## 2. Offline vs. Online — Warum die Explosion digitaler Plattformen?

### Plattformen sind NICHT neu

**Klassische Plattformen:**
- Shopping Mall (1950er+)
- Ad-finanzierte Zeitungen (19. Jh.)
- Nightclubs
- Flea Markets

### Historisches Beispiel — Frankreich, 12. Jh.

Der Graf von Champagne organisierte regelmäßige **Trade Fairs**, bei denen Händler aus ganz Europa garantiert aufeinandertrafen. Er:

- **Coordination:** Garantierte Anwesenheit (löste das Henne-Ei-Problem)
- **Trust:** Bereitstellte sichere Streitbeilegung
- **Level Playing Field:** Gleiche Regeln für alle Händler

Im Gegenzug nahm er **einen kleinen Anteil jeder Transaktion** — und wurde reich.

**Parallel zu heute:** Ersetze "Champagne-Graf" durch "Jeff Bezos" und "Trade Fair" durch "Amazon Marketplace". *Plattform-Logik ist uralt; die Technologie skaliert sie.*

### Warum jetzt so viele *digitale* Plattformen?

Digitalisierung bewirkt zwei Dinge:

1. **Reduziert Transaktionskosten dramatisch:**
   - Suche, Matching, Trust, Reputation, Payment — alles billiger
2. **Erlaubt aktives NE-Management bei Skalierung:**
   - Recommender-Systeme
   - Rating-Aggregation
   - Real-time Pricing
   - Datensammlung & Analyse

→ Beide Plattform-Bedingungen werden viel leichter erfüllt → digitale Plattformen entstehen massenhaft.

### Die Größe digitaler Plattformen

| Jahr | Top-10-Firmen weltweit (Markt-Cap) |
|---|---|
| 2008 | Petrobras, ExxonMobil, GE, China Mobile, ICBC, ... (Old Economy) |
| 2018 | **Apple, Google, Microsoft, Amazon, Facebook, Tencent**, Berkshire Hathaway, **Alibaba**, J&J, JPM |

→ 7 von 10 sind Plattform-Firmen.

### Mit weniger Angestellten — anderes Geschäftsmodell

| Klassisch | Plattform | Differenz |
|---|---|---|
| BMW (1916, 116k MA, $53B) | Uber (2009, 7k MA, $60B) | ähnlich Marktwert, **17× weniger MA** |
| Marriott (1927, 200k MA) | Airbnb (2008, 5k MA) | massiv schlanker |
| Disney (1923, 185k MA) | Facebook (2004, 12.7k MA) | 14× schlanker |

→ Plattformen **vermitteln Wertschöpfung**, statt sie zu **produzieren**. Daher weniger Angestellte für vergleichbare Marktkapitalisierung.

---

## 3. Network Effects — Definitionen und Beispiele

### Die Grunddefinition

> Ein **Netzwerkeffekt** ist ein **externer Effekt (Externalität)**, generiert vom "Originator" (= dem zusätzlichen User), der einen anderen Agenten ("Receiver") affektiert.

**Wichtig:** Network Effects sind **Externalitäten** — der Originator internalisiert sie nicht im Preis. Plattformen können diese Externalitäten **internalisieren** (durch Pricing, Subventionierung, Rating, etc.).

### Die 2 Hauptkategorien

#### 1. Within-Group Network Effects (WGNE)

> Wie affektiert die Entscheidung eines Agenten, der Plattform beizutreten, das Wohlergehen anderer Agenten **in seiner eigenen Gruppe**?

#### 2. Cross-Group Network Effects (CGNE)

> Wie affektiert die Entscheidung eines Agenten das Wohlergehen anderer Agenten **in einer anderen Gruppe**?

In beiden Fällen wichtig: **positiv** oder **negativ**?

### Die 4 Kategorien (Klausur-Pflicht-Wissen)

|             | innerhalb Gruppe (WGNE) | zwischen Gruppen (CGNE) |
|-------------|--------------------------|--------------------------|
| **positiv** | Telefonnetz, WhatsApp, Wikipedia | Uber (Fahrer ↔ Rider), eBay |
| **negativ** | Online-Poker (Profis), Waze-Stau | Werbung (Advertiser → User) |

---

### Within-Group Network Effects (WGNE) — Direkter Effekt

**Positiv-Beispiele:**
- **Telefon:** Je mehr User, desto mehr potentielle Gesprächspartner
- **WhatsApp / Zoom / Teams:** Communication-Tools — Wert nimmt mit Größe zu
- **Fashion:** Trends — was viele tragen, wird modisch

**Negativ-Beispiele:**
- **Stau auf Waze:** Wenn alle die "Stau-Umfahrung" nehmen, entsteht da Stau
- **Online-Poker mit Profis:** Mehr starke Spieler = schlechtere Gewinnchancen für Amateure
- **Twitter mit zu vielen Schreibern:** Cacophony statt Conversation

### Attraction Loop — der Mechanismus positiver WGNE

> Höheres Aktivitätsniveau der Gruppe → attraktiver für jeden Einzelnen → mehr User → höheres Aktivitätsniveau → ...

Typisch für Communications-Systems.

**Zwei Channels für Attraction Loops:**

1. **Direkter Benefit von Interaktion** (Telefonnetz, Facebook)
2. **Qualität abhängig von Useranzahl** (Google Search — bessere Ergebnisse mit mehr Search-Daten; Waze — präzisere Verkehrsinfo)

### Bei zu großem Netzwerk: Network Effects kippen ins Negative

**Waze-Beispiel:** Anfangs leitet Waze um Staus herum. Aber wenn **alle** User dieselbe Umleitung nehmen, verlagert sich der Stau dorthin. Plus: **Non-Users** (Anwohner) leiden unter dem Verkehr.

→ **Manchmal können Policy-Interventionen nötig sein** (z.B. LA Residents-Beschwerden über Waze-Re-Routing in steile Straßen).

### Coordination und Winner-takes-all

Attraction Loops + Singleton-Plattformen führen zu **"Winner-takes-all"-Outcomes**:

1. Markt endet in **asymmetrischer Struktur** — selbst wenn die Plattformen ex-ante symmetrisch waren
2. Coordination auf einer Plattform kann User auf eine *suboptimale* Plattform zwingen (z.B. WhatsApp statt Signal trotz Datenschutz-Bedenken)

### Negative Schocks können WGNE zerstören

**Beispiel — Chatroulette:** Web-Plattform, die User zufällig für Webcam-Gespräche paart.
- **Anfangs:** Positiver Attraction Loop
- **Nach "hairy naked guy problem":** Negative Erfahrungen verdrängten User → Loop kippt

**Lehre:** Plattformen müssen User-Verhalten **regulieren** (Moderation), um positive WGNE zu schützen.

---

### Cross-Group Network Effects (CGNE)

**Positiv-Beispiele:**
- **Trading-Plattformen** (eBay, Amazon Marketplace): Mehr Buyer → mehr Anreiz für Seller, und umgekehrt
- **Matching-Plattformen** (Tinder, LinkedIn-Recruiting): Mehr eine Seite → mehr Match-Möglichkeiten für andere Seite

**Negativ-Beispiele:**
- **Ad-finanzierte Content-Plattformen** (YouTube, Free-TV): Mehr Werbung → weniger User-Nutzen (Annoyance)

**Asymmetrische CGNE:** Manchmal sind sie **in einer Richtung positiv, in der anderen negativ:**
- User → Advertiser: positiv (mehr User = attraktiver für Werber)
- Advertiser → User: negativ (mehr Werbung = annoyance)

### 3 typische CGNE-Situationen

#### 1. Attraction Spiral (beide positiv)

Jede Gruppe exert positive NE auf die andere → mutual attraction → schnelles Plattform-Wachstum.

**Eigenschaften:**
- Generiert **positive indirekte Network Effects** innerhalb jeder Gruppe (durch die Cross-Effekt-Verkettung)
- **Beispiel:** eBay — mehr Buyer → mehr Seller → mehr Auswahl für Buyer → noch mehr Buyer

#### 2. Attraction/Repulsion Pendulum

Eine Richtung positiv, andere negativ:

- **Content users ↔ Advertisers:**
  - User → Advertiser: positiv (mehr Reichweite)
  - Advertiser → User: negativ (Werbung als Annoyance)
- **User ↔ Hackers (Web-Browser):**
  - User → Hacker: positiv (mehr Ziele)
  - Hacker → User: negativ (Sicherheitsbedrohung)

**Mechanik:** Wenn Group A wächst → Group B wächst (positiv) → Group A schrumpft (negativ) → Group B schrumpft → Group A wächst wieder ... Pendel.

→ **Generiert negative indirekte Network Effects** für jede Gruppe.

#### 3. Attraction Spillover (eine Richtung positiv, andere null)

Group A attractiv für Group B, aber Group B nicht für Group A.

**Beispiele:**
- **Pros vs. Amateure auf Foren:** Amateure profitieren von Pros (lernen), Pros profitieren nicht von Amateuren
- **Early Adopters vs. Late Users (System Goods):** Early sammeln Daten/Erfahrung, die später-Adopters profitieren; aber Later-Adopters bringen nichts mehr für Early

**Vierte Situation** (gegenseitig negativ): trivial uninteressant — Plattform würde sich gar nicht erst bilden.

---

### Direkte vs. Indirekte Network Effects

**Direkt = Within-Group:**
- Users in Group A interagieren *direkt* miteinander
- Mehr User in Group A → direkter Nutzen für Group A

**Indirekt = Cross-Group-Kombination:**
- Users in Group A nutzen mehr User in Group A *indirekt*, weil:
  - Mehr User in A → mehr User in B (CGNE)
  - Mehr User in B → mehr Nutzen für A (CGNE umgekehrt)
- → Indirekter positiver Effekt von A-User auf A-User

**Beispiel Airbnb:**
- Ein extra Guest → mehr Hosts → besseres Angebot für alle Guests (indirekter positiver Effekt)

### Indirect Network Effects in System Goods

**System Goods** = Hardware + Software-Komplemente (z.B. Konsole + Games, DVD-Player + DVDs, Smartphone + Apps).

- Direkter NE: **keiner** (Konsole-User interagieren nicht miteinander)
- Indirekter NE: **stark** (mehr Konsole-User → mehr Games-Entwicklung → wertvoller für Konsole-User)

### Empirische Evidenz — Yelp + GrubHub

**Reshef (2020) — Yelp Transactions Platform (YTP):**

2018: YTP started Partnership mit GrubHub → effektiv mehr Restaurants auf der Plattform.

**Frage:** Wie affektierte das die Revenues der bereits existierenden Restaurants?
- **Direct effect (negativ):** Mehr Konkurrenz unter Restaurants
- **Indirect effect (positiv):** Mehr Restaurants → mehr Plattform-Nutzung → mehr Demand für alle

**Result:** Indirekter Effekt **dominierte** — Entry neuer Restaurants **half** den Incumbents.

→ Empirie zeigt: Indirekte CGNE können stark genug sein, um den direkten Konkurrenz-Effekt zu überwiegen.

### Network-Effect-Categorization kann tricky sein

Online Poker — auf den ersten Blick:
- 1 User-Gruppe (Spieler), positiver WGNE (mehr Spieler = kürzere Wartezeiten)

Bei genauerem Hinsehen:
- Spieler sind **heterogen** (low-skilled, high-skilled)
- **Low-skilled** zusätzlicher Spieler: Generiert **positive** WGNE/CGNE (kürzere Wartezeit + bessere Gewinnchancen)
- **High-skilled** zusätzlicher Spieler: Generiert **negative** WGNE/CGNE (geringere Gewinnchancen für alle)

→ Plattform muss **Ability-Differenzen managen** (Stake-Niveaus, Skill-Matching), um nicht von High-Skilled überlaufen zu werden.

### Twitter — wie viele Sides?

Schwierig zu klassifizieren:
- Mit Advertisern: Two-sided (User & Advertiser)
- Ohne Advertiser: One- oder Two-sided?
- Sind Reader und Writer dieselbe Gruppe oder verschieden?

→ Plattform-Klassifikation ist **kontextabhängig** und nicht immer eindeutig.

---

## 4. Typologie der Plattformen

### Warum eine Typologie?

Verschiedene Plattformen funktionieren nach unterschiedlichen Strategien. Eine Typologie hilft:
- **Underlying Forces** zu identifizieren
- **Performance** zu verstehen
- **Strategie** zu entwickeln

### Die Aguiar-Typologie: 2 Dimensionen

**Dimension 1 — Wertschöpfung (Value Creation):**

Wo entsteht der ökonomische Wert?

| Variante | Mechanismus | Beispiel |
|---|---|---|
| Cross-Group NE | Attraction Spiral | Uber, Airbnb |
| Within-Group NE | Attraction Loop | WhatsApp, Spotify |
| Stand-Alone | Nicht-Plattform | Klassische Zeitung (NYT) |

**Dimension 2 — Wertextraktion (Value Capture):**

Wie wird der Wert monetarisiert?

| Variante | Mechanismus | Beispiel |
|---|---|---|
| Charge users enjoying positive NE | Subscription, Membership | Netflix, Spotify Premium |
| Offer bundle including "bad" | Ads, Data | Facebook, YouTube |

### Die Typologie-Tabelle

| Value Capture ↓ \ Value Creation → | WGNE | CGNE | Stand-Alone |
|---|---|---|---|
| **Charge users** | Netflix, **LinkedIn 2002**, **Amazon (Pure)** | **LinkedIn 2005**, Airbnb, Uber | **Not a platform** |
| **Monetize via others** | **WhatsApp** (Datenverkauf), **Amazon Marketplace** | **YouTube** | **NYT** (klassische Zeitung) |

### Beispiel — LinkedIn-Evolution

- **LinkedIn 2002 (WGNE-focused, Charge users):** Subscription-Model für Profis
- **LinkedIn 2005 (CGNE added):** Recruiter-Side hinzugefügt → Employers zahlen für Zugang zu Talent-Pool

### Beispiel — WhatsApp-Evolution

- **2010-2018 (WGNE, charge users):** $1/Jahr Subscription
- **2018+ (move to two-sided):** Free für User, "WhatsApp Business" added für Companies → Companies zahlen für Customer Engagement

### Andere Typologien

**Plattform-Objektive:**
- For-profit (Airbnb, Uber)
- Non-profit (Wikipedia)
- Hybrid (Plattformen die ohne Monetization-Strategie starten und später monetarisieren)

**Plattform-Instrumente:**
- **Transaction Platforms:** Trxn passiert *auf* der Plattform (eBay)
- **Non-Transaction Platforms:** Plattform vermittelt nur (Twitter — keine direkten Trxns)

**Plattform-Audiences (B/C-Kombinationen):**
- **B2B:** Alibaba
- **B2C:** Zalando, Airbnb (Host-side)
- **C2C:** Couchsurfing, BlaBlaCar (Peer-to-peer)

**Plattform-Functions:**
- **Hardware/Software Systems:** PlayStation, Android, Windows (App-Developer ↔ End-User)
- **Matchmakers:** Tinder, Monster, Sittercity (pure Interaction)
- **Exchanges:** eBay, Booking, Deliveroo (Match + Trxn)
- **Peer-to-Peer Marketplaces:** Airbnb, Uber
- **Media & Entertainment:** Spotify, YouTube
- **Payment Systems:** Visa, PayPal, MasterCard

---

## Take-Aways für die Klausur

### Definitionen sicher haben

1. ✅ **Plattform-Definition** — 2 Bedingungen
2. ✅ **Network Effect-Definition** — Externalität
3. ✅ **WGNE vs. CGNE** — Originator/Receiver-Logik
4. ✅ **Direkt vs. Indirekt** — von wem die Quelle stammt

### Klassifikation üben

Gegeben eine Plattform (Spotify, Tinder, ...), kann ich:
- Sie als Plattform identifizieren (oder nicht)?
- Die Network Effects benennen (welche Kategorie, ±positiv)?
- Sie in der 2D-Typologie verorten?

### Typische Klausur-Fragen (basierend auf Aguiar-Stil)

1. **"Welche der folgenden Aussagen ist korrekt?"** — meist über NE-Kategorien
2. **"Klassifizieren Sie Plattform X"** — Wertschöpfung × Wertextraktion
3. **"Was passiert, wenn Plattform Y das User-Verhalten nicht moderiert?"** — Chatroulette-Style-Argument
4. **"Welche Network Effects sind auf Plattform Z am Werk?"** — alle 4 Kategorien identifizieren

### Häufige Klausur-Fallen

| Falsche Antwort | Korrekt |
|---|---|
| "Uber-Fahrer auf Uber-Fahrer ist CGNE" | **WGNE** (negativ) — sie sind in derselben Gruppe |
| "Netflix ist keine Plattform" | **Doch** — managed WGNE via Recommendation System |
| "Network Effect = Economy of Scale" | NEIN — NE ist demand-side, EoS supply-side |
| "Esperanto ist eine Plattform" | NEIN — NE existieren, aber keine aktive Management-Entity |
| "Bei zu wenigen Sides keine Plattform" | NEIN — One-sided platforms existieren (WhatsApp) |

---

## Verwandt

- [[20.studies/Organizational-Economics/intuitionen-und-mechanismen]] — Block 1
- [[20.studies/Organizational-Economics/plattformen-network-effects]] — Erweiterte WGNE/CGNE-Details
- [[20.studies/Organizational-Economics/section2-demand-competition]] — VL Section 2 (Demand, Hotelling, Defensibility)
- [[20.studies/Organizational-Economics/problem-set-recipes]] — Konkrete Klausur-Aufgaben
- [[20.studies/Organizational-Economics/Hub]]
