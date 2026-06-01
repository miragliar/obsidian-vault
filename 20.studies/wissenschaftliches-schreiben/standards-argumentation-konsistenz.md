---
source: claude-import
imported: 2026-06-01
conv_uuids: [453cb575-19dc-43aa-b16c-175af1dff5fd, 8914de4f-a0b1-4a2b-aeaf-ba4fcc5ab733, 31209536-8917-465a-a7e5-5130c0837d5a]
tags: [wiss-schreiben, qualitätsprüfung, konsistenz, kohärenz, standards]
---

# Standards-Check, Argumentationskonsistenz, Volumen

Pattern für die finale Qualitätssicherung wissenschaftlicher Arbeiten.

## Checkliste — wissenschaftliche Standards in einer Seminararbeit

Vor Abgabe systematisch durchgehen:

### Inhalt
- [ ] Forschungsfrage klar, präzise, beantwortbar
- [ ] Methode passt zur Frage (qualitativ vs. quantitativ vs. diskursanalytisch)
- [ ] Quellen sind aktuell, peer-reviewed wo möglich, kanonisch zitiert
- [ ] Hauptthese explizit benannt und durch Argumentation getragen
- [ ] Gegenpositionen referenziert und behandelt
- [ ] Schluss antwortet auf die Eingangsfrage (nicht: anderes Thema)

### Form
- [ ] Inhaltsverzeichnis & Seitenzahlen
- [ ] Zitierstil konsistent durchgezogen (`(Autor, Jahr, S. X)` o.ä.)
- [ ] Literaturverzeichnis vollständig & konsistent formatiert
- [ ] Abbildungs- und Tabellenverzeichnis (wo nötig)
- [ ] Eidesstattliche Erklärung (Schluss)
- [ ] Rechtschreibung & Grammatik geprüft (DUDEN; bei CH: ss statt ß)

### Methodisch
- [ ] Quellenkritik reflektiert (z.B. Zeitschichtung der Quellen)
- [ ] Begriffsdefinitionen klar
- [ ] Operative Begriffe vor Verwendung definiert
- [ ] Eingrenzung des Gegenstands transparent
- [ ] Limitationen ehrlich benannt (nicht formelhaft)

### Sprache
- [ ] Emische vs. etische Sprachebene konsistent
- [ ] Keine umgangssprachlichen Phrasen
- [ ] Konjunktiv I bei indirekter Rede / fremder Aussage
- [ ] Tempus konsistent (meist Präsens für theoretische Aussagen, Präteritum für Ereignisse)

## Pattern: Argumentations-Kohärenz prüfen

Bei jedem Hauptkapitel:

1. **Kernthese in einem Satz formulieren** (ohne in den Text zu schauen)
2. **Stützen identifizieren** — welche Quellen / Argumente tragen?
3. **Gegenpositionen** identifizieren — wo könnte das Argument scheitern?
4. **Übergang zum nächsten Kapitel** — was bringt das mit?

Wenn (1) schwer formulierbar ist: das Kapitel hat **noch keine** klare These — Indikator zum Überarbeiten.

## Pattern: Argumentative Congruence — Vergleich von Texten

Wenn zwei Quellen / Argumentationen verglichen werden:

| Achse | Quelle A | Quelle B | Konvergenz / Divergenz |
|---|---|---|---|
| Forschungsfrage | ... | ... | ... |
| Methode | ... | ... | ... |
| Datengrundlage | ... | ... | ... |
| Schlüsselbefund | ... | ... | ... |
| Mechanismus | ... | ... | ... |
| Limitation | ... | ... | ... |

→ Tabelle füllen, dann **die markantesten Konvergenz/Divergenz-Linien** als Argumentationsachsen herausarbeiten.

## Volumen — Faustregeln

Häufige Frage: was bedeutet das Volumen-Limit?

- **1 Seite Fließtext** ≈ 2'500–3'000 Zeichen (mit Leerzeichen, 12pt, 1.5-Zeilenabstand)
- **17'000 Zeichen** ≈ 6 Seiten Fließtext
- **60'000 Zeichen** ≈ 20–24 Seiten

**Pflicht-Konsistenz:** Die Angabe „Zeichen mit Leerzeichen" oder „ohne Leerzeichen" macht ~15 % Differenz — bei Volumen-knapp lesen, was die Vorgabe ist.

**Volumen-Check in Word:** *Überprüfen → Wörter zählen* zeigt beides.

## Häufige Konsistenz-Fehler

| Fehler | Wie finden |
|---|---|
| Zitationsstil-Drift (`(Burla 2025)` vs. `(Burla, 2025, S. X)`) | Regex-Search `\(\w+\s+\d` in Word |
| Em-Dash schleicht ein (`—`) | Find-Replace mit Vorsicht |
| Daten-Inkonsistenz über Kapitel | Versions-Stand pro Kapitel notieren |
| ß vs. ss (CH-Variante) | Globaler Replace + Spell-Check |
| Konjunktiv vergessen bei indirekter Rede | Manuelles Lesen mit Fokus „sagt/argumentiert/zeigt" |
| Tempus-Wechsel mitten im Satz | Lautes Lesen |
| Abkürzung beim ersten Auftreten nicht definiert | Vor jeder Erstverwendung manuell prüfen |
| „Ich"-Form in argumentativen Sätzen | Optional je nach Stil-Vorgabe — meist passiv oder „in dieser Arbeit" |

## Pattern: Reverse Outline

Beim finalen Lektorat: pro Absatz **eine Marginalie** ans Rand schreiben (1 Zeile) — was tut dieser Absatz?

Dann die Marginalien als „Outline" lesen:

- Sind die Marginalien konsekutiv? (Übergang sauber?)
- Gibt es Sprünge?
- Gibt es Wiederholung?
- Tut jeder Absatz **eine** Sache?

→ Effektivstes Tool für strukturelle Probleme, die im Detail nicht auffallen.

## Verwandt

- [[20.studies/wissenschaftliches-schreiben/wissenschaftliche-formulierung-religion]]
- [[20.studies/wissenschaftliches-schreiben/paper-kritisch-analysieren-fuer-praesentation]]
- [[20.studies/Anneliese-Michel/05-Schreibwerkstatt-Konsistenz-Zitate]] — Schreibroutinen am konkreten Projekt
- [[20.studies/Working-Poor-Gesundheit/03-Kapitel-4-Architektur-und-Synthese]]
- [[20.studies/wissenschaftliches-schreiben/_README]]
