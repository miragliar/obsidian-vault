---
source: claude-import
imported: 2026-06-01
conv_uuids: [9f3dbee1-87dc-42a4-8400-508bf9c435c0]
tags: [lernstrategie, pruefung, notebooklm, interleaving, spaced-repetition]
---

# Lernstrategie — OE-Prüfung 19. Juni (Master M&E, UZH)

## Problem

Eine 90-Minuten-Klausur (UZH M&E, „ME 3: Organizational Economics", Prof. Aguiar) mischt drei Aufgabentypen über alle Themen:

- **Multiple-Choice** (Methodik **und** Inhalt)
- **Freitext** (2–4 Sätze, ökonomisch präzise)
- **Modellrechnung** (Hotelling, Plattform-Pricing, komparative Statik)

Material: **5 VL-Zusammenfassungen + 4 Problemsets + 8 Paper-Steckbriefe**. Lernziel: Top-Note (5.5+). Zeitbudget bei Vollzeit-Studium + 60%-Arbeit ≈ 95–100 Stunden über 23 Tage.

Typische Falle: linear durchackern → trügerische Fluency, kein aktiver Abruf, MC-Distraktoren schlagen zu.

## Lösung

### Grundprinzip: 3-Modi-Lernen pro Thema

Weil alle Aufgabentypen alle Themen treffen können, gibt es **keinen Stoff zum Wegpriorisieren**. Jedes Thema muss in drei Abrufmodi sitzen:

| Modus | Was üben | Tool |
|---|---|---|
| **MC-fähig** | Detail-Fakten, Definitionen, Annahmen, Vorzeichen | Karteikarten + NotebookLM-Cross-Topic-MC |
| **Freitext-fähig** | Mechanismen in 2–4 Sätzen erklären | Synthese-Seite pro Thema schreiben |
| **Rechen-fähig** | Modelle, Herleitungen, komparative Statik | Problemsets halbiert + neu rechnen |

Pro Themenblock entstehen **drei Artefakte** — Synthese, Karteikarten-Set, gelöstes Problemset.

### Drei-Phasen-Plan (23 Tage)

**Phase 1 — Aufbau (Tag 1–10, ~42 h)**
- Pro Tag 1 thematischer Block: VL-Zusammenfassung lesen + zugehörige Paper-Steckbriefe + halbes Problemset
- Synthese-Seite anlegen (eigene Worte, Schlüsselformeln, eine Visualisierung)
- Karteikarten-Set füttern (Anki o.ä.)
- NotebookLM nur als **Wiederholungsstütze** — nicht als Erst-Encoding! Sonst entsteht trügerische Fluency.

**Phase 2 — Konsolidierung (Tag 11–17, ~28 h)**
- Querverbindungen zwischen Themen (Interleaving) erzwingen
- Cross-Topic-MC-Quiz aus NotebookLM
- Verbleibende Problemset-Hälften
- 8 Paper-Steckbriefe als geschlossene Wiederholungsrunde
- Methoden-Cheatsheet (IV, DiD, FE, RCT) konsolidieren

**Phase 3 — Simulation (Tag 18–22, ~14 h)**
- Tag 18: Schwachthemen identifizieren + gezielt nachholen
- Tag 19: Mock-Klausur unter Zeitdruck (90 min), dann auswerten
- Tag 20: Schwachstellen aus Mock fixen
- Tag 21: Finale Quiz-Runde, Karteikarten leeren
- Tag 22 (Vortag): Light review, Schlaf priorisieren

### Trainings-/Arbeits-Constraints integrieren

Wenn fixe Slots blockiert sind (z.B. Training Di/Mi/Fr abends, Arbeit Mo/Do):

- **Trainings-Abende:** keine Problemsets (zu kognitiv anspruchsvoll, kein Fokus). Stattdessen: Karteikarten 20 min, NotebookLM-Audio unterwegs.
- **Tote Zeit (Pendeln, Spülen, Sport-Aufwärmen):** Audio-Overviews zu einer **anderen** VL als der aktuell aktiven (= Spaced Repetition für ältere Inhalte).
- **Lerntage (gewählt: Di 2.6, Mi 3.6, Mi 10.6, Fr 12.6, Do 18.6 + WE):** Volle Problemset-Sessions, Synthese-Schreiben, Mock-Tests.

### NotebookLM-Setup (einmalig)

- **Ein Notebook mit allen 5 VL-Zusammenfassungen zusammen** → Basis für Cross-Topic-MC
- **Pro VL ein Audio-Overview** für unterwegs
- **Ein Audio-Overview vom Methoden-Cheatsheet** (IV/DiD/FE/RCT)
- Optional: 1–2 NotebookLM-Videos zu komplexen VL-Themen

### NotebookLM-Prompt-Bibliothek

**Pro-VL-Quiz (Detailabruf):**

> Erstelle ein Quiz mit 12 Fragen ausschließlich zu [VL-Titel / Quelle X]. Mische die Formate: 6 Multiple-Choice mit je 4 Antwortoptionen (nur eine korrekt), 3 Wahr/Falsch, 3 offene Kurzfragen. Bei MC: falsche Optionen plausibel und nah an der richtigen Antwort (typische Verwechslungen). Lösungen mit kurzer Begründung **am Ende**, nicht direkt nach jeder Frage.

**Cross-Topic-MC (der wichtigste — fiese Distraktoren):**

> Erstelle 15 Multiple-Choice-Fragen, die quer über alle Quellen gehen und Konzepte aus verschiedenen Vorlesungen kombinieren. Jede Frage hat 4 Optionen, genau eine korrekt. Distraktoren bilden typische Fehlvorstellungen ab: vertausche ähnliche Konzepte (same-side vs. cross-side Netzwerkeffekte, Selektion vs. Treatment-Effekt, verletzte vs. erfüllte Identifikationsannahme). Frageform „Welche der folgenden Aussagen ist korrekt/falsch?", nicht „Was ist X?". Lösungen mit Begründung am Ende.

**Paper-Quiz (8 Steckbriefe):**

> Frage mich systematisch zu jedem der hochgeladenen Paper ab. Pro Paper 4 Fragen: (1) Forschungsfrage in einem Satz, (2) Identifikationsstrategie + Annahme, (3) Hauptergebnis mit Vorzeichen + grobem Effektgrößen-Sinn, (4) ökonomischer Mechanismus. Lösung erst nach jeder Antwort.

**Freitext-Drill:**

> Stelle mir eine Frage, die in 2–4 Sätzen ökonomisch präzise zu beantworten ist. Nach meiner Antwort: bewerte sie streng (Was fehlt? Wo unscharf? Wo wäre der Begriff X präziser?). Verwende Klausur-Niveau.

### Lerntechniken — was wirkt

| Technik | Warum | Wie einsetzen |
|---|---|---|
| **Spaced Repetition** | Verteiltes Wiederholen → langfristiges Behalten | Karteikarten täglich, NotebookLM-Audio für ältere VL |
| **Interleaving** | Verschiedene Themen mischen → robusterer Abruf | NotebookLM-Cross-Topic-MC, Wechsel von VL zu Paper zu Problemset im Tagesplan |
| **Multimodales Encoding** | Mehrere Sinneskanäle → stärkere Verankerung | Text lesen → Audio hören → Quiz machen → handschriftlich Synthese |
| **Active Recall** | Reproduktion > Wiedererkennung | Karteikarten **ohne** Vorschau, Problemsets **frisch** rechnen |
| **Mock-Klausur unter Zeitdruck** | Simuliert Echtbedingungen | Phase 3 mit 90-Min-Timer |

### Anti-Patterns

- **NotebookLM zuerst, dann VL lesen** → Du erkennst Inhalte wieder, kannst sie nicht reproduzieren.
- **Problemsets nur lesen, nicht rechnen** → MC-Inhalte gehen vielleicht, Modellrechnung scheitert.
- **„Ich lese jede VL nochmal von vorne"** → maximales Volumen, minimaler Lerntransfer. Stattdessen: aktiver Abruf.
- **Mock-Klausur erst am Vortag** → keine Zeit mehr für Schwachstellen-Fix.

## Wann nicht

- **Bei Open-Book-Klausuren:** Detailfaktenwissen weniger wichtig, Konzepte + Strategie zentral. Andere Gewichtung.
- **Bei reinem MC-Format:** Karteikarten + Cross-Topic-MC reichen, Synthese-Seiten weniger nötig.
- **Bei Klausuren mit klarer Themen-Priorisierung** (z.B. Dozent kündigt Schwerpunkte an): Lineare 3-Phasen-Logik kann durch Schwerpunktblock ersetzt werden.
- **Bei <2 Wochen Vorbereitungszeit:** Phase 3 (Simulation) muss um Phase 1 reduziert werden — gewählt wird Top-3-Themen statt aller 5.

## Verwandt

- [[20.studies/Organizational-Economics/plattformen-network-effects]]
- [[20.studies/Organizational-Economics/two-sided-markets-divide-and-conquer]]
- [[20.studies/Organizational-Economics/identifikationsstrategien]]
- [[20.studies/Organizational-Economics/_conversation-index]]
