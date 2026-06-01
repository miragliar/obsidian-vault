---
source: claude-import
imported: 2026-06-01
conv_uuids: [2a3604c1-b39e-4936-b083-33cbf2e5bd33]
tags: [ai-builder, prompt-engineering, power-automate, json]
---

# AI Builder Prompts — Strukturierte JSON-Ausgabe & deterministische Berechnungen

## Problem

In Power Automate wird der „Prompt"-Action (AI Builder / Azure OpenAI) eingesetzt, um:

- Werte aus Text zu extrahieren
- Eine Formel mit dynamischen Werten auszuwerten
- Ein Klassifikations-Ergebnis als JSON zurückzuliefern

Typische Probleme in der Praxis:

1. **Resultat „knapp daneben"** bei Rechen-Prompts (LLMs rechnen ungenau)
2. **JSON wird mit Erklärtext umrahmt** (`"Hier ist das Ergebnis: {...}"`) → Parse JSON crasht
3. **Lokalisierung**: deutsche Dezimal-Notation `1,5` vs. englische `1.5`
4. **Reihenfolge der Werte im Output** schwankt
5. **Modell liefert mal `string`, mal `number`** im selben Feld

## Lösung

### Pattern 1 — JSON-only, kein Erklärtext

Klare Marker im Prompt:

```
**Ausgabe – nur dieses JSON, keine Erklärungen:**
```json
{
  "Werte": "<Werte durch Semikolon getrennt>",
  "Resultat": "<berechnetes Ergebnis>"
}
```
```

Plus explizit am Ende: `Gib nur das JSON aus, ohne weitere Zeichen davor oder danach.`

### Pattern 2 — Step-by-step **intern**, dann Output

Der wichtigste Trick gegen Rechenfehler:

```
**Vorgehensweise (intern, nicht ausgeben):**
1. Ersetze alle Variablen in der Formel durch ihre Zahlenwerte
2. Löse Klammern von innen nach außen auf
3. Führe alle Rechenoperationen Schritt für Schritt aus
4. Prüfe das Ergebnis durch nochmaliges Nachrechnen

**Ausgabe – nur das JSON:**
{ ... }
```

→ Das Modell „denkt" intern in Schritten (reduziert Flüchtigkeitsfehler bei verschachtelten Klammern), gibt aber nur die finale Antwort aus. Funktioniert mit allen Claude/GPT-Modellen.

### Pattern 3 — Locale explizit festlegen

```
**Regeln:**
- Dezimalzahlen mit Komma statt Punkt (z. B. `1,5` statt `1.5`)
- "Werte" listet die Variablen in der Reihenfolge ihres **ersten Auftretens in der Formel**
- Jede Variable erscheint im "Werte"-Feld nur **einmal**, auch wenn sie in der Formel mehrfach vorkommt
```

Wenn du im Flow später `float()` brauchst → siehe [[50.work/power-platform/power-automate-string-expressions]] für Komma→Punkt-Replace vor dem Cast.

### Pattern 4 — Konkretes Beispiel im Prompt

LLMs sind one-shot-Lerner. Ein vollständiges Beispiel im Prompt **mit derselben Output-Struktur** killt 80 % der Format-Drifts:

```
**Beispiel:**
Eingabe:
[Menge]: 2
[Länge]: 2.5
[Breite]: 3.2
Formel: [Menge] * (2 * ([Länge] + [Breite]))

Ausgabe:
{
  "Werte": "2;2,5;3,2",
  "Resultat": "22,8"
}
```

### Pattern 5 — Reihenfolge & Dedup deterministisch

Wenn das JSON eine geordnete Liste enthalten muss:

> `"Werte"` listet die Variablen in der Reihenfolge ihres **ersten Auftretens in der Formel**.
> Jede Variable erscheint nur **einmal**, auch wenn sie in der Formel mehrfach vorkommt.

Diese Sätze sind essentiell — ohne sie sortiert das Modell alphabetisch oder nach Eingabe-Reihenfolge.

### Vollständiges Beispiel-Prompt

```
Du erhältst eine Texteingabe mit benannten Werten und einer Formel.
Setze die Werte ein und berechne das Resultat.

**Vorgehensweise (intern, nicht ausgeben):**
1. Ersetze alle Variablen durch ihre Zahlenwerte
2. Löse Klammern von innen nach außen auf
3. Rechne Schritt für Schritt
4. Prüfe nochmal nach

**Ausgabe – nur dieses JSON, keine Erklärungen:**
```json
{
  "Werte": "<Werte durch Semikolon getrennt>",
  "Resultat": "<berechnetes Ergebnis>"
}
```

**Regeln:**
- Dezimalzahlen mit Komma statt Punkt (z. B. 1,5)
- "Werte" in Reihenfolge ihres ersten Auftretens in der Formel
- Jede Variable nur einmal in "Werte"

**Beispiel:**
Eingabe:
[Menge]: 2
[Länge]: 2.5
[Breite]: 3.2
Formel: [Menge] * (2 * ([Länge] + [Breite]))

Ausgabe:
{
  "Werte": "2;2,5;3,2",
  "Resultat": "22,8"
}
```

### Im Flow konsumieren

Nach der „Prompt"-Action:

```
// Compose:
outputs('Prompt')?['predictionOutput/structuredOutput/Resultat']

// Float-Cast mit Komma-Fix:
float(replace(outputs('Prompt')?['predictionOutput/structuredOutput/Resultat'], ',', '.'))
```

## Wann nicht

- **Wenn die Logik deterministisch ist:** Bedingungs- + Stringverkettungs-Aufgaben wie „wenn Einfassbreite = 1 cm → Farbe X mergen, sonst Y" — **das ist kein Prompt-Job**, das ist eine Power Automate `Condition` + `concat`/`substring`. LLMs für deterministische Logik einsetzen ist langsam, teuer und fehleranfällig.
- **Bei großen Berechnungen oder vielen Operationen:** Nicht das LLM rechnen lassen — Werte extrahieren lassen, Berechnung im Flow mit `mul`/`add` selber machen. Garantiert exakt.
- **Bei strukturierter Datenextraktion:** Wenn das Eingabeformat fest ist (z.B. immer „Name: X, Email: Y") → `split` + `indexOf` ist robuster und kostenlos.
- **Bei Klassifikation mit endlicher Menge** und Trainingsdaten verfügbar: AI Builder „Classification" Model trainieren ist besser als generischer Prompt — höhere Genauigkeit, sauberes Output-Format ohne Prompt-Engineering.
- **Wenn du Schema-Garantien brauchst:** Lieber Structured Output (JSON Schema-mode) der API verwenden statt Prompt-basierter JSON-Generierung — funktioniert in Azure OpenAI mit `response_format`.

## Verwandt

- [[50.work/power-platform/power-automate-string-expressions]]
- [[50.work/power-platform/power-automate-invalidopenapiflow]]
- [[40.meta/Claude-Workflows]] — generelle Prompt-Patterns
- [[50.work/power-platform/_conversation-index]]
