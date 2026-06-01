---
source: claude-import
imported: 2026-06-01
conv_uuids: [9393073f-20c9-4404-96af-884e23cd5501, 7081be43-39bf-4846-adae-eaf9f77a11ee]
tags: [paper-analyse, peer-review, ewa, präsentation, methodenkritik]
---

# Peer-reviewed Paper kritisch analysieren — für Präsentation / Assessment

Pattern für die wiederkehrende Aufgabe: **eine empirische wirtschaftswissenschaftliche Studie auswählen + journalistische Coverage kritisch einordnen** (z.B. EWA-Assessment, Tutoriats-Bewerbung).

## Auswahl-Kriterien (in Reihenfolge)

1. **Peer-reviewed** — Working Paper / NBER / SSRN reichen oft *nicht*. JEBO, JPE, Journal of Public Economics, ECONtribute, AEJ-Applied: ja.
2. **Max. 20 Seiten** — sonst nicht in 10-Minuten-Präsentation verdichtbar
3. **Klare empirische Identifikation** (RCT, DiD, IV, FE, Feldexperiment) — macht die methodische Kritik substanziell, siehe [[20.studies/Organizational-Economics/identifikationsstrategien]]
4. **Aktuelle journalistische Coverage** (z.B. letzte 3 Monate) als Aufhänger
5. **Domäne**: passend zum Studienschwerpunkt (VWL Minor → Arbeit, Bildung, Verhaltensökonomie)

## Recherche-Workflow

```
1. Journal-Webseiten (JEBO, JPE, AEJ-Applied) → Recent Issues, Online-First
   ↓ filter: empirisch, <20 Seiten
2. Pro Kandidat: Google News + Pressetexte im Fenster Δt suchen
   ↓ wenn Lücke: Pressemitteilung des Instituts (z.B. ECONtribute) → Konsumer-Portale
3. 2–3 Kandidaten parallel evaluieren, dann *einen* wählen
```

**Erfahrung:** Working Papers haben oft mehr Coverage, weil sie früher öffentlich gepusht werden. Aber Assessment fordert peer-reviewed → frühzeitig auf JEBO/JPE-Status prüfen.

## Strukturelle Lücken — was schiefgehen kann

| Problem | Fix |
|---|---|
| Coverage nur in Web-Portalen (kein „newspaper of record") | Web-Portal nutzen, im Kommentar transparent machen („Web-Portal, nicht klassische Tageszeitung") |
| Coverage außerhalb des Zeitfensters | Lockerung des Fensters dokumentieren oder anderen Aufhänger wählen |
| Working Paper als Top-Treffer | Auf peer-reviewed Variante prüfen (oft im Folgejahr erschienen) |
| Studie zu komplex (>30 Seiten, mehrere Methoden) | Wählt 1 Abbildung als „Anker", erklärt nur diesen Strang |

## Analyse-Raster für die Präsentation (10 min)

| Teil | Inhalt | Zeit |
|---|---|---|
| (a) **Worum geht's** | Forschungsfrage + Aufhänger-Artikel | 1 min |
| (b) **Treue der Berichterstattung** | Was sagt der Artikel? Was sagt das Paper? Diskrepanzen explizit | 2 min |
| (c) **Wissenschaftliche Standards** | Methode, Identifikation, Sample, Power, Robustness | 3 min |
| (d) **Verbesserungspotenzial** | Was würde *dich* unzufrieden lassen? Konkrete Vorschläge | 2 min |
| Schluss | Take-away, Q&A | 2 min |

## Diskrepanz-Patterns (Berichterstattung ↔ Paper)

| Im Artikel | Im Paper |
|---|---|
| „Studie beweist X" | Paper findet Assoziation, keine Kausalität (oder kausalen Effekt unter Annahme Y) |
| „Z % der Befragten" | Sub-Sample, gewichtete Daten, andere Bezugsgröße |
| Effekt für „alle" | Heterogenität: Effekt nur in Subgruppe stark |
| Keine Confidence Intervals | Paper zeigt CI = (0.01, 0.45), Punktwert wird als bare Zahl gemeldet |
| „erstmals gezeigt" | Replikation, Erweiterung, oder Re-Analyse |

→ Diskrepanzen sind die **substantiellsten Punkte** der Präsentation.

## Methodische Standards prüfen (Checkliste)

- [ ] Identifikationsstrategie sauber benannt? (siehe [[20.studies/Organizational-Economics/identifikationsstrategien]])
- [ ] Sample beschrieben (n, Selektion, Drop-outs)?
- [ ] Statistische Power diskutiert?
- [ ] Robustness Checks vorhanden?
- [ ] Wahrscheinlichste Verletzungen der Schlüssel-Annahme thematisiert?
- [ ] Verallgemeinerbarkeit (External Validity) reflektiert?
- [ ] Limitationen aufgelistet — und ernst gemeint, nicht nur formelhaft?

## Verbesserungs-Vorschläge formulieren

Vermeide generische Sätze („mehr Daten wären gut"). Konkret pro Aspekt:

| Aspekt | Generisch (schlecht) | Konkret (gut) |
|---|---|---|
| Sample | „Größere Stichprobe" | „Replikation in BU-Sektor, da hier nur Privatschulen, Generalisierbarkeit unklar" |
| Methode | „Andere Methode probieren" | „IV-Schätzung mit Z=[konkret] könnte Selektion in Treatment adressieren" |
| Outcome | „Mehr Variablen messen" | „Langfristige Outcomes (5 Jahre) ergänzen, kurzfristige Effekte können dissipieren" |
| Mechanismus | „Mechanismen klären" | „Heterogenitätsanalyse nach Eingangsmotivation würde testen, ob Effekt durch X oder Y getrieben ist" |

## Verwandt

- [[20.studies/Organizational-Economics/identifikationsstrategien]]
- [[20.studies/wissenschaftliches-schreiben/wissenschaftliche-formulierung-religion]]
- [[20.studies/wissenschaftliches-schreiben/_README]]
