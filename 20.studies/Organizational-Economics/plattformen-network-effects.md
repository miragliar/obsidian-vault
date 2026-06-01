---
source: claude-import
imported: 2026-06-01
conv_uuids: [c7dfb788-465f-421f-8e0c-1171cb2ca585, 5edcadf0-0073-4648-a71a-9fd9c4731e63, 891355ab-3275-4bd1-b405-7ee27b9421f1, f41a7525-fa79-44ba-907b-ad70a35eee53, 2315ac93-4909-43db-9819-cc5628fc7a4b]
tags: [organizational-economics, plattformen, network-effects, theorie]
---

# Plattformen & Network Effects — Definitionen und Typologie

## Problem

In Klausuraufgaben zu Organizational Economics werden Konzepte wie *Plattform*, *Netzwerk­effekt*, *Within-Group* vs. *Cross-Group*, *positiv* vs. *negativ* präzise abgefragt. Distraktoren zielen genau auf typische Verwechslungen:

- Plattform vs. einfacher Marktplatz
- Same-Side vs. Cross-Side Effects
- Positive WGNE vs. positive CGNE
- Network Effect vs. Economy of Scale

## Lösung

### Plattform — Definition (UZH-Standard)

> Eine **Plattform** ist eine Entität, die ökonomische Agenten zusammenbringt **und** Netzwerk­effekte zwischen ihnen **aktiv** managt.

Zwei Bedingungen, **beide** müssen erfüllt sein:

1. Network Effects existieren zwischen den Agenten
2. Die Entität managt diese Effekte aktiv (Algorithmen, Pricing, Rating, Moderation)

**Beispiele klassifizieren:**

| Entität | Plattform? | Begründung |
|---|---|---|
| Uber | ja | Matched Fahrer/Fahrgäste, manages Pricing, Rating |
| Wikipedia | ja | Aktive Moderation, Reader-Writer-Interaktion |
| Amazon Marketplace | ja | Match + Reviews + Pricing-Empfehlung |
| Klassischer Supermarkt | nein | Bringt zusammen, aber managt keine Netzwerk­effekte |
| Telefonnetz (Infrastruktur) | grenzwertig | WGNE existieren, aktives Management gering |

### Network Effect — Allgemeine Definition

> Ein **Netzwerk­effekt** ist eine **Externalität** (externer Effekt), generiert vom „Originator", die einen anderen Agenten („Receiver") affektiert.

Wichtig: Externalität → der Effekt ist nicht im Preis internalisiert. Der Plattform-Job ist u.a., diese Externalitäten zu internalisieren (durch Pricing, Subventionierung, Rating).

### Vier Kategorien (Klausur-Pflicht)

| | innerhalb Gruppe | zwischen Gruppen |
|---|---|---|
| **positiv** | **Positive WGNE** | **Positive CGNE** |
| **negativ** | **Negative WGNE** | **Negative CGNE** |

**Within-Group Network Effect (WGNE):** Originator und Receiver gehören zur **gleichen** Gruppe.

- Positive WGNE: Telefonnetz — mehr Nutzer → höherer Wert für andere Nutzer (Metcalfe-artig)
- Negative WGNE: Online-Poker mit heterogenen Spielerstärken — mehr Profis → schlechtere Erfahrung für Amateure; Stau auf Waze; Twitter mit zu vielen Schreibern vs. wenigen Lesern

**Cross-Group Network Effect (CGNE):** Originator und Receiver gehören zu **verschiedenen** Gruppen.

- Positive CGNE: Uber — mehr Fahrer → kürzere Wartezeit für Fahrgäste (und umgekehrt); Yelp/Grubhub für Restaurants ↔ Esser
- Negative CGNE: Werbung in Apps — mehr Werbung → geringerer User-Nutzen (User ↔ Advertiser, gegenseitige Sicht)

### Typische Distraktoren in MC

| Falscher Reflex | Korrekt |
|---|---|
| „Uber-Fahrer auf Uber-Fahrer = CGNE, weil Mehr-Fahrer = weniger Job für mich" | Das ist **negative WGNE** — Originator und Receiver beide aus der Fahrer-Gruppe |
| „Network Effect = Economy of Scale" | Nein. Economy of Scale = sinkende Stückkosten produktionsseitig. Network Effect = steigender Nutzen nachfrageseitig. |
| „Positive CGNE = beide Richtungen positiv" | Nicht zwingend. Kann asymmetrisch sein (z.B. Advertising: User → Advertiser positiv, Advertiser → User negativ) |
| „Switching Costs = Network Effect" | Nein. Switching Costs sind Friktion bei Wechsel; Network Effects sind Nutzen-Funktionen von Größe. Oft koexistent, aber konzeptuell verschieden. |

### Network-Effect-Stärke (β-Parameter)

Im Plattform-Modell ist β der Intensitätsparameter:

- u_b = r_b + β_b · n_s − P_b (Buyer-Utility, Plattform mit 2 Seiten)
- β_b groß → Buyer wertet die Sellers stark → Cross-Side-Effekt stark
- → Implikation für Pricing: subventioniere die Seite, deren β niedrig ist; monetarisiere die Seite, deren β hoch ist

(Vollständige Pricing-Logik in [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]].)

### Attraction Loops & Tipping

Wenn positive CGNE stark genug sind, kann der Markt **tippen** — eine Plattform gewinnt alles, die andere stirbt. Beispiel WhatsApp vs. Signal: Wenn der Stand-Alone-Nutzen von Signal höher ist, aber WhatsApp 50× mehr User hat, wechseln Nutzer trotzdem zu WhatsApp, sobald der Netzwerk­effekt-Bonus die Stand-Alone-Differenz überwiegt.

**Tipping-Bedingung (vereinfacht):** Marktteil-Differenz × β > Stand-Alone-Nutzen-Differenz.

### „Then and Now" — historische Parallelen

Der Kurs (Aguiar) zieht gerne Parallelen — Henri (12. Jh.) als Markt-Maker in Frankreich vs. Bezos als digitaler Markt-Maker. Plattformen sind kein neues Phänomen, das Internet skaliert die Effekte.

## Wann nicht

- **Bei reinen Substanz-Fragen ohne ökonomischen Mechanismus:** Wenn es um deskriptive Plattformanalyse geht (Marktforschung, Strategie-Beratung), ist die WGNE/CGNE-Taxonomie Overkill — qualitative Stakeholder-Analyse reicht.
- **Bei Tools/Infrastruktur, die nicht aktiv managen:** Ein DNS-Server, ein BitTorrent-Tracker — formal vielleicht „Plattform"-artig, aber das Kurs-Konzept passt nur teilweise. In Klausur diese Edge Cases nicht überstrapazieren.
- **Bei one-sided Märkten:** Klassische Märkte ohne Cross-Group-Struktur — kein Bedarf für CGNE-Analyse.

## Verwandt

- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]] — Pricing-Mechanik, Hotelling
- [[20.studies/Organizational-Economics/identifikationsstrategien]] — empirische Methoden zu CGNE-Effekten
- [[30.patterns/text-formatting/unicode-subscript-konvertierung]] — Notation `n_b`, `β_b` lesbar machen
- [[20.studies/Organizational-Economics/_conversation-index]]
