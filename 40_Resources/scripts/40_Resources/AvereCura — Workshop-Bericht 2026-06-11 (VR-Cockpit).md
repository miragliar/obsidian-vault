---
type: report
status: final
created: 2026-06-11
client: "[[20_Clients/AvereCura.md|AvereCura]]"
zweck: "Workshop-Bericht VR-Cockpit, Vor-Ort 11.06.2026 — inkl. Measure-/Definitions-Doku"
tags: [report, workshop, powerbi, averecura]
---
# Workshop-Bericht — AvereCura VR-Cockpit, 11.06.2026

*Vor-Ort, Tramstrasse 55, Uetikon am See · Miraglia BI (Giovanni Miraglia) mit AvereCura (Finanzen/ICT/Verwaltung) · Engagement via Upgreat AG.*

## 1. Ausgangslage & Ziel
Aufbau eines **Cockpits für den Verwaltungsrat (VR)** auf Basis des Heim-ERP **Lobos**. Zielkennzahlen (VR): Hauptertrag, Personalaufwand, EBT/Erfolg, Belegung, Cashflow/Liquidität, Investitionen, Fluktuation, Kosten pro Bewohner/Tag, Pflege-/Betreuungsaufwand, RAI-Stufen-Entwicklung. Bis dato deckte das Cockpit nur **Pflege/Bewohner/Leistungsfaktura** ab; Ziel des Workshops war die **Finanz-Domäne (FIBU)** und die **VR-taugliche Architektur**.

## 2. Architektur-Entscheid (verbindlich)
- **Ein semantisches Datenmodell pro juristischer Entität / Haus** (Wäckerling, Rivabella, Impuls Wetzikon, …) — jedes Haus = die „Wahrheit" für seine Zahlen.
- **Später ein Composite-Modell für den VR**, das ausgewählte Kennzahlen über alle Häuser **zusammenführt/summiert**.
- **Additive** Kennzahlen (Hauptertrag, Personalaufwand, ER, Pflegetage, Bettage) dürfen summiert werden; **nicht-additive** (Quoten/%, Kosten pro Bewohner/Tag, Belegungsgrad) werden im VR-Modell **aus summierten Zählern/Nennern neu gerechnet**, nie addiert.
- **Mandanten-Parametrisierung** umgesetzt: PBIX nutzt Power-Query-Parameter `DataflowID`/`WorkspaceID`. **Neues Haus = Modell kopieren → `DataflowID` umstellen → Refresh → Hausfarben-Theme.** Pattern: [[PowerQuery__Dataflow_Mandanten_Parameter]].

## 3. Was heute umgesetzt wurde
1. **FIBU vollständig ins Cockpit „Haus Wäckerling" integriert** — `hauptbuchjournal` (Faktentabelle) + `hauptbuchkonto`/Kontoplan (Dimension) inkl. **NRL-Hierarchie** (= exakte Struktur der Erfolgsrechnung/Saldenliste mit konzerninterner Einfaltung).
2. **Finanz-Measures definiert & gegen Saldenliste validiert** (rappengenau, **2024 UND 2025**): `Hauptertrag`, `Erfolgsrechnung (ER)`, `Personalaufwand`, `Bilanz`, `Saldo FIBU` (Details → Abschnitt 4).
3. **Saubere Periodenabgrenzung**: eigenes `Periodendatum` (Buchungsdatum auf die offizielle Buchungsperiode geklemmt) → Monats-/Jahreswerte = Saldenliste, auch bei Abgrenzungs-/Abschlussbuchungen. Eine gemeinsame Zeitachse für Faktura UND FIBU.
4. **Erste VR-Visualisierung „Hauptertrag-Entwicklung"** (3 Kennzahlen-Kacheln + Säulen lfd. Jahr vs. Linie Vorjahr nach Monat) inkl. Time-Intelligence-Measures (Vorjahr / Δ / Δ % / YTD).
5. **Corporate Design**: Hausfarben-Palette für **alle Häuser** erhalten (Marketing) → **13 Power-BI-Theme-Dateien** generiert; holdingweit einheitliche **semantische Bewertungsfarben** (positiv/Warnung/kritisch). Ablage: `…/UpGreat/averecura/files/`.
6. **Zweites Cockpit „Residenza Rivabella" aufgebaut & validiert** (via Parameter-Pattern) — inkl. Tessiner Spezialfälle (Spitex, Mieterträge, kantonale Restfinanzierung als Pauschale).
7. **Neuer Dataflow „Lobos Impuls Wetzikon" erstellt & erfolgreich aktualisiert** (Refresh 14:09).

### Stand Power-BI-Umgebung (Live-Inventar 11.06., read-only)
**4 Dataflows** (Workspace „Datenmanagement"):

| Dataflow | Dataflow-ID | Refresh |
|---|---|---|
| Lobos Haus Wäckerling | `6b2d48f4-1dc6-48c0-b818-b91309dd824b` | 14:11 |
| Lobos Brunisberg | `38aa617f-a194-49fc-94bc-64bb15fd9a3e` | 09:19 |
| Lobos Haus Rivabella | `aa1e2b34-1aea-40a9-b01f-093fff989497` | 12:51 |
| **Lobos Impuls Wetzikon** | **`58c1a5ab-cba8-43da-9523-eb52ba9fe6c8`** | 14:09 |

**Cockpits (Semantikmodelle):** „Cockpit Haus Wäckerling" (FIBU-erweitert) · „Cockpit Residenza Rivabella" (neu). **Impuls Wetzikon: Modell noch zu bauen** (→ Hausaufgabe, Abschnitt 6).

> ℹ️ Korrektur Dataflow-ID: Die im Workshop genannte ID `aa1e2b34-…` gehört zu **Rivabella**; der **Impuls-Wetzikon-Dataflow** ist **`58c1a5ab-…`** (gegen Tenant verifiziert).

## 4. Kurz-Dokumentation: Measures & Definitionen

### A) Finanzkennzahlen (FIBU) — holdingweit identisch, Saldenlisten-validiert (2024 & 2025)
| Measure | Definition | Validierung Haus Wäckerling |
|---|---|---|
| **Saldo FIBU** | Kontosaldo aus dem Hauptbuch-Journal (Haben − Soll; + = Ertrag). Basis aller Finanz-Measures. | — |
| **Hauptertrag** | Betriebshauptertrag = NRL-Gruppe 60 (inkl. konzerninterner Erträge; **ohne** Betriebsneben-/Finanzertrag, **ohne** Spitex). Additiv. | 2025: **19'680'607.03** · 2024: 17'499'162.27 |
| **Erfolgsrechnung (ER)** | Periodenergebnis = Erträge − Aufwände (NRL-Gruppen ≥ 30 ohne Abschlussgruppe 89; + = Gewinn). Additiv. | 2025: **+2'561'269.88** (Gewinn) |
| **Personalaufwand** | NRL-Klasse Personalaufwand (inkl. konzernintern, Vorzeichen positiv). Additiv. | 2025: **12'784'385.38** · 2024: 12'048'190.86 |
| **Bilanz** | Stichtagssaldo Bilanzkonten (Aktiven +) + Jahresergebnis (Gruppe 89). Additiv bei gleichem Stichtag. | Aktiven 2025: **18'133'652.14** |
| **Hauptertrag VJ / Δ VJ / Δ VJ % / YTD** | Time-Intelligence (Vorjahresvergleich, Differenz, %, Jahreskumuliert). | — |

### B) Leistungs- & Belegungskennzahlen (aus der Heimfakturierung) — pro Haus prüfen
| Measure | Definition | Hinweis |
|---|---|---|
| **Umsatz** | Summe Fakturapositionen (+ Vorjahr/Differenz) | Leistungs-/Pensionserträge aus der Faktura |
| **Pflegetage** | Summe Pflegetage aus den RAI-Leistungspositionen | ⚠ **Leistungsnummernkreise je Haus verschieden** (Wäckerling 2700er; Rivabella 9000er) → bei jedem neuen Haus prüfen |
| **Krankenkassenbeitrag / Restfinanzierung Gemeinde** | KK- bzw. Gemeinde-/Kantonsanteil | mandantenspezifisch; bei Rivabella rappengenau gegen FIBU validiert |
| **Anzahl mögliche Bettage / Bettenbelegungsgrad** | Effektive ÷ mögliche Bettage | ⚠ Headline-Nenner noch zu klären (Abschnitt 5) |

### C) Rivabella-spezifisch (Tessiner Rechnungslegung)
- **Spitex Ertrag** (NRL-Gruppe 61) — separat ausgewiesen, **nicht** im Hauptertrag (im Tessin nicht in den Betriebshauptertrag klassiert).
- **Personalkostenquote** = Personalaufwand ÷ (Hauptertrag + Spitex Ertrag), da das Spitex-Personal untrennbar im Personalaufwand enthalten ist. **2024: 68.4 % · 2025: 72.7 %** (Wäckerling 66.7 % / 63.0 %). Im VR-Composite je Haus mit eigenem Nenner → aus summierten Zählern/Nennern rechnen.

**Konvention:** Alle Zeitvergleiche laufen über die zentrale `Zeitachse`; Finanz-Measures über das `Periodendatum`.

## 5. Offene Punkte
1. **Pflegetage-Definition Rivabella** (Leistungsnummern 9000–9009) — formale Bestätigung durch [[Radovanovic Jadranko|Jadranko Radovanovic]] offen.
2. **Bettenbelegungsgrad**: Headline ~74 % ≠ Monatswerte 89–96 % (Wäckerling) bzw. 48.6 % bei 77 Betten (Rivabella, da Residenza-Mieter keine RAI-Tage erzeugen) → **Nenner „mögliche Bettage" klären**, bevor es dem VR gezeigt wird.
3. **Datumsbasis Faktura**: Beziehung läuft aktuell über `lfk_valutadatum` (Rechnung) statt `lfp_datumvon` (Leistung) → Miraglia prüft/hängt um.
4. **RAI/RUG-Hilfstabelle** = manuell gepflegtes SharePoint-Excel → für VR-Reporting mittelfristig in eine governte Quelle überführen.
5. **Farbkollision** Corporate Design ↔ semantische Bewertungsfarben (AVER/ROGA) → mit Marketing klären.
6. **Nächste Domänen** (Folgeausbau): BEBU/Kostenstellen (→ Kosten pro Bewohner/Tag), Lohn/HR (→ Personalaufwand-Detail, Fluktuation inkl./exkl. Pensionierungen — braucht Austrittsgrund), Cashflow/Investitionen (Datenquelle klären).

## 6. Hausaufgabe [[Radovanovic Jadranko|Jadranko Radovanovic]] — Semantikmodell „Impuls Wetzikon"
**Ziel:** das Cockpit-/Semantikmodell für **Impuls Wetzikon** selbst aufbauen — als Vorlage **Residenza Rivabella** oder **Haus Wäckerling** verwenden.

**Vorgehen (Parameter-Pattern):**
1. Vorlage-PBIX kopieren (Rivabella oder Wäckerling).
2. Power-Query-Parameter **`DataflowID`** auf den Impuls-Wetzikon-Dataflow setzen: **`58c1a5ab-cba8-43da-9523-eb52ba9fe6c8`** (Dataflow „Lobos Impuls Wetzikon", Workspace „Datenmanagement"). `WorkspaceID` bleibt.
3. **Refresh** → Daten validieren (gegen Saldenliste Impuls Wetzikon, sofern vorhanden).
4. **Leistungs-Measures prüfen/anpassen** (`Pflegetage`, `Krankenkassenbeitrag`, `Restfinanzierung Gemeinde`) — die Leistungsnummernkreise/Gruppennamen sind je Lobos-Mandant verschieden; die **FIBU-Measures sind dagegen NRL-stabil** und portieren 1:1.
5. **Hausfarben-Theme** Impuls Wetzikon (IMPW) laden + Modell publishen.

> Jadranko arbeitet ebenfalls mit Claude AI + Power BI → die Projekt-Anweisung [[40_Resources/Claude-Desktop Projekt-Anweisung — AvereCura Haus Wäckerling (Power BI).md]] kann als Grundlage dienen.

## 7. Verweise
- Kunden-Hub: [[20_Clients/AvereCura.md|AvereCura]]
- Projekt-Anweisung Claude Desktop: [[40_Resources/Claude-Desktop Projekt-Anweisung — AvereCura Haus Wäckerling (Power BI).md]]
- Mandanten-Parameter-Pattern: [[PowerQuery__Dataflow_Mandanten_Parameter]]
- Mandantenspezifische Leistungs-Measures: [[ERP__Lobos_Leistungsmeasures_Mandantenspezifisch]]
