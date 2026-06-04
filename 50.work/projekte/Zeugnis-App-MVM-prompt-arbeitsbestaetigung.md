---
name: Arbeitsbestätigung-Prompt MVM
slug: Zeugnis-App-MVM-prompt-arbeitsbestaetigung
projekt: "[[50.work/projekte/Zeugnis-App-MVM|Zeugnis-App MVM]]"
klient: MVM AG
type: prompt
tags: [miraglia, projekt, mvm-ag, zeugnis, arbeitsbestaetigung, ai-prompt, swiss-german]
status: v2 (Überarbeitung 2026-06-04)
created: 2026-06-04
source: chat-context 2026-06-04 (Anschluss-Review nach Zeugnis-Prompt v2)
---
Ihre Eingabeaufforderung wurde nach unseren Systemrichtlinien gefiltert. [Weitere Informationen](https://go.microsoft.com/fwlink/?linkid=2268317)  
Sie können die Inhaltsmoderationsebene des Prompts in den Prompteinstellungen konfigurieren. [Weitere Informationen](https://go.microsoft.com/fwlink/?linkid=2344811)
# Arbeitsbestätigung-Prompt MVM (v2)

> Zweiter Prompt im Zeugnis-Tool — wird angesteuert wenn der `Typ = "Arbeitsbestätigung"` ist (nicht volles Zeugnis, sondern Bestätigung bei Austritt **innerhalb der Probezeit**).
>
> Geschwister-Prompt: [[50.work/projekte/Zeugnis-App-MVM-prompt|Zeugnis-Prompt v2]]

## Diff zur v1 (Kurzfassung)

| # | v1 (alt) | v2 (neu) | Warum |
|--|---|---|---|
| 1 | „Use 'ss' instead of 'ß'." nebenbei in Salutation-Block | **Priority Rule 1** ganz oben mit Beispiel-Tabelle + Self-Check | Gleiches Reklamations-Anliegen Nicole Lötscher (03.06.) |
| 2 | Umlaut-Inkonsistenz im Body (`bestaetigen`, `wuenschen`, `fuer` neben `Tätigkeitsbeschrieb`, `berufliche`) | **Konsistent echte Umlaute** im Body (ä/ö/ü), ASCII-Keys nur im JSON | Sieht professionell aus, korrektes Deutsch |
| 3 | Rating 1-4: nur „slightly reduce" / „neutral" — vage | **Explizite Templates Rating 1-5** mit Schlüssel-Adjektiven und Schlusssatz | Reproduzierbarkeit, Bulletproof-Wording (du hast es selbst im Prompt-Ende vorgeschlagen) |
| 4 | Adjektiv-Endungs-Platzhalter `freundliche{r}` und `kooperative{n}` ambig | **Explizite Templates pro Geschlecht** (Mask/Fem komplett ausgeschrieben) | Eindeutig, keine Modell-Rate-Schritte |
| 5 | Austritts-Satz: „fuer {sein\|ihr} berufliche" — grammatikalisch falsch (müsste „seine/ihre" sein) | **Korrekt:** „für seine berufliche..." (M) / „für ihre berufliche..." (F) | Femininum „Zukunft" braucht Possessivpronomen mit -e |
| 6 | Kein Self-Check | **Mandatory Verification Checklist** | Selbst-Prüfung vor Output |

## Prompt v2 (zum Einsetzen in die App)

```text
You will receive structured input for generating a Swiss-German **Arbeitsbestätigung** (employment confirmation) — typically issued when an employee leaves within the probation period and therefore does not receive a full Zeugnis.

Input fields:
- **Typ** (Type) — must match (case-insensitive): "Arbeitsbestätigung" / "Arbeitsbestaetigung" / "Employment confirmation"
- **Vorname** (first name)
- **Nachname** (last name)
- **Geschlecht** (gender) — single letter: M = male, F = female
- **Rating** — integer 1–5 (1 = poor, 5 = excellent personal/behavioral assessment)
- **Tätigkeitsbeschrieb** — description of the person's tasks and responsibilities (immediately after the rating)

Produce a JSON object with exactly three sections. Follow ALL rules below STRICTLY. Every rule is mandatory and non-negotiable.

═══════════════════════════════════════════════════
PRIORITY RULE 1 — Swiss German Orthography (de-CH)
═══════════════════════════════════════════════════

Treat the entire output as Swiss German. Standard German orthography (de-DE) is NOT permitted.

▶ NEVER use the letter "ß" (scharfes S, Eszett) — anywhere, ever.
  Replace every "ß" with "ss". This applies to body, names, fixed expressions, quotations — without exception.

Examples relevant for an Arbeitsbestätigung (de-DE → de-CH):

| ❌ de-DE (forbidden) | ✅ de-CH (required) |
|---|---|
| verläßt (old) / verläßlich | verlässt / verlässlich |
| Außendienst | Aussendienst |
| Außenwirkung | Aussenwirkung |
| Größe | Grösse |
| gemäß | gemäss |
| beschloß (old) | beschloss |
| Maßstab | Massstab |
| stets selbständig & zuverlässig | stets selbständig und zuverlässig (no ß) |
| Fleiß | Fleiss |
| schließlich | schliesslich |
| schließen | schliessen |
| weiß | weiss |

▶ DO use proper umlauts (ä, ö, ü) in the BODY text — write `bestätigen`, `wünschen`, `für`, `persönlich`, `verlässt`, `Tätigkeit`, NOT `bestaetigen` / `wuenschen` / `fuer` / `persoenlich` / `verlaesst` / `Taetigkeit`. UTF-8 is fully supported.

▶ JSON KEYS remain ASCII-only (no umlauts in keys): `Taetigkeitsbeschrieb`, `Persoenlicher_Absatz`, `Austrittsabsatz`.

**Mandatory self-check before output:** scan the entire generated text for the character "ß". If you find even one, replace it with "ss" and re-verify. The output must contain zero "ß" characters.

═══════════════════════════════════════════════════
PRIORITY RULE 2 — Gender → Salutation, Pronouns, Role noun
═══════════════════════════════════════════════════

Use the value of **Geschlecht**:

| Field | Geschlecht = M | Geschlecht = F |
|---|---|---|
| Anrede | Herr | Frau |
| Personalpronomen Nom. | er | sie |
| Personalpronomen Akk. | ihn | sie |
| Personalpronomen Dat. | ihm | ihr |
| Possessiv (Mask./Neut.) | sein | ihr |
| Possessiv (Fem.) | seine | ihre |
| Rollen-Nomen | Mitarbeiter | Mitarbeiterin |
| Adjektiv-Endung Akk. nach „als" | freundlichen, kooperativen, zuverlässigen, pflichtbewussten (-en) | freundliche, kooperative, zuverlässige, pflichtbewusste (-e) |

**Name order:** Always **Vorname Nachname** in the output, regardless of input order.

**Gender-ambiguous names** (e.g. „Andrea", „Kim", „Sascha"): trust the Geschlecht field exclusively. Never guess from the name.

═══════════════════════════════════════════════════
STRUCTURE — Three sections, in this fixed order
═══════════════════════════════════════════════════

══ PART 1 — Tätigkeitsbeschrieb ══

Review the provided Tätigkeitsbeschrieb for grammar, clarity, and tone.
Rewrite it in polished, formal, concise Swiss-German.
Return it as ONE clean paragraph (no bullet points, no headings).

══ PART 2 — Persönlicher Absatz (depends on Rating) ══

Select the template for the given Rating and gender. Use the templates as a base — adapt minimally to fit name and grammatical agreement, but preserve the tone and the key adjective(s).

▼ Rating 5 (excellent — enthusiastisch):

  M: "In persönlicher Hinsicht bestätigen wir gerne, dass wir Herrn {Vorname} {Nachname} als sehr freundlichen und kooperativen Mitarbeiter kennengelernt haben. Sein Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war stets vorbildlich."
  F: "In persönlicher Hinsicht bestätigen wir gerne, dass wir Frau {Vorname} {Nachname} als sehr freundliche und kooperative Mitarbeiterin kennengelernt haben. Ihr Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war stets vorbildlich."

▼ Rating 4 (good — positiv, ohne „sehr"):

  M: "In persönlicher Hinsicht bestätigen wir, dass wir Herrn {Vorname} {Nachname} als freundlichen und kooperativen Mitarbeiter kennengelernt haben. Sein Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war einwandfrei."
  F: "In persönlicher Hinsicht bestätigen wir, dass wir Frau {Vorname} {Nachname} als freundliche und kooperative Mitarbeiterin kennengelernt haben. Ihr Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war einwandfrei."

▼ Rating 3 (neutral — sachlich):

  M: "In persönlicher Hinsicht haben wir Herrn {Vorname} {Nachname} als zuverlässigen Mitarbeiter kennengelernt. Sein Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war korrekt."
  F: "In persönlicher Hinsicht haben wir Frau {Vorname} {Nachname} als zuverlässige Mitarbeiterin kennengelernt. Ihr Verhalten gegenüber Vorgesetzten, Mitarbeitenden und Kunden war korrekt."

▼ Rating 2 (mildly reserved — knapp):

  M: "In persönlicher Hinsicht haben wir Herrn {Vorname} {Nachname} als pflichtbewussten Mitarbeiter kennengelernt."
  F: "In persönlicher Hinsicht haben wir Frau {Vorname} {Nachname} als pflichtbewusste Mitarbeiterin kennengelernt."

▼ Rating 1 (minimal endorsement — rein faktisch, keine Charaktereigenschaft):

  M: "Herr {Vorname} {Nachname} war innerhalb der Probezeit in unserem Unternehmen tätig."
  F: "Frau {Vorname} {Nachname} war innerhalb der Probezeit in unserem Unternehmen tätig."

Replace `{Vorname}` and `{Nachname}` with the input values. No other modifications to the templates above.

══ PART 3 — Austrittsabsatz (fixed, gender-adjusted) ══

  M: "Herr {Nachname} verlässt unser Unternehmen innerhalb der Probezeit. Wir wünschen ihm für seine berufliche sowie private Zukunft alles Gute und viel Erfolg."
  F: "Frau {Nachname} verlässt unser Unternehmen innerhalb der Probezeit. Wir wünschen ihr für ihre berufliche sowie private Zukunft alles Gute und viel Erfolg."

Replace `{Nachname}` with the input value.

═══════════════════════════════════════════════════
OUTPUT FORMAT — JSON (strict schema)
═══════════════════════════════════════════════════

Return ONE JSON object with EXACTLY these three keys, each value being a single string (multiline if needed):

{
  "Taetigkeitsbeschrieb": "<one clean paragraph, no bullets>",
  "Persoenlicher_Absatz": "<one paragraph, from Rating template>",
  "Austrittsabsatz": "<one paragraph, fixed template>"
}

- Key names are exact: ASCII-only, no umlauts (`Taetigkeitsbeschrieb`, `Persoenlicher_Absatz`, `Austrittsabsatz`).
- Each value is a SINGLE string. Use `\n` for line breaks within a string if needed.
- No additional keys, no nested structures.
- No commentary, no markdown code fences, no prose outside the JSON object.
- The output MUST be valid, parsable JSON.
- No greetings, no introductions, no closing salutations — only the three sections.

═══════════════════════════════════════════════════
MANDATORY VERIFICATION CHECKLIST
═══════════════════════════════════════════════════

Before producing the final JSON, mentally verify each item. If any check fails, fix it before output:

[ ] Zero "ß" characters anywhere in the output
[ ] Umlauts (ä, ö, ü) used correctly in body — no "ae/oe/ue" substitutes
[ ] JSON keys are ASCII-only (Taetigkeitsbeschrieb / Persoenlicher_Absatz / Austrittsabsatz)
[ ] Anrede (Herr/Frau) matches Geschlecht (M/F)
[ ] All pronouns (er/sie, ihm/ihr, sein/ihr, seine/ihre) match Geschlecht consistently
[ ] Rollen-Nomen (Mitarbeiter/Mitarbeiterin) matches Geschlecht
[ ] Adjektiv-Endungen passend zum Geschlecht (-en für Mask., -e für Fem. nach „als")
[ ] Vorname Nachname order (surname last) — never reversed
[ ] Rating-Template wurde korrekt gewählt (1–5)
[ ] Tätigkeitsbeschrieb ist ein sauberer Absatz, keine Bullets
[ ] Austrittsabsatz ist exakt der Fix-Satz (gender-adjusted), unverändert ansonsten
[ ] Three and only three keys in the JSON
[ ] No greetings, intros, closings, signatures, or meta-commentary anywhere
[ ] Valid, parsable JSON

Every single instruction in this prompt is mandatory and non-negotiable. The final language of the output is **Swiss German (de-CH)**.
```

## Test-Plan (analog Zeugnis-Prompt)

1. **ß-Test:** Tätigkeitsbeschrieb mit Trigger-Wörtern füttern („Fleiss/Fleiß", „Aussendienst/Außendienst", „gemäss/gemäß", „verlässt/verläßt") — Output prüfen, dass kein „ß" mehr drin steht.
2. **Umlaut-Test:** Input mit Umlauten (z.B. „Maler-Tätigkeit übernommen") — Output muss echte Umlaute haben, keine „ae/oe/ue"-Ersatzformen im Body.
3. **Rating-Matrix:** 5 × 2 (M/F) = 10 Generierungen mit identischem Namen — die persönlichen Absätze müssen sich klar voneinander unterscheiden und zum Rating-Wording passen.
4. **Gender-Test:** Geschlecht-ambivalenter Name („Andrea Müller", „Kim Schmid") jeweils mit M und F — Anrede + Pronomen + Adjektiv-Endungen kontrollieren.
5. **JSON-Schema-Test:** Power-Automate-Parse-JSON gegen das Schema validieren (3 Keys, ASCII).

## Belt-and-Suspenders (Power-Automate-Stufe)

Wie auch beim Zeugnis-Prompt: zusätzlich **nach** dem AI-Step einen `replace(outputs('AI'), 'ß', 'ss')` als Defense-in-Depth einbauen. Falls das Modell die Regel mal verfehlt, fängt das Flow-Replace es ab — egal welcher der beiden Prompts gefeuert hat.

## Verwandt

- [[50.work/projekte/Zeugnis-App-MVM|Zeugnis-App MVM (Projekt-Hub)]]
- [[50.work/projekte/Zeugnis-App-MVM-prompt|Zeugnis-Prompt v2 (Geschwister)]]
- [[50.work/25_People/Nicole-Lötscher|Nicole Lötscher]] — Auslöserin der ß→ss-Anforderung
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04 — ToDo #8]]
