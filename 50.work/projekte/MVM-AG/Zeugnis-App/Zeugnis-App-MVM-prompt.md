---
name: Zeugnis-Generator-Prompt MVM
slug: Zeugnis-App-MVM-prompt
projekt: "[[Zeugnis-App-MVM|Zeugnis-App MVM]]"
klient: MVM AG
type: prompt
tags: [miraglia, projekt, mvm-ag, zeugnis, ai-prompt, claude, swiss-german]
status: v2 (Überarbeitung 2026-06-04)
created: 2026-06-04
source: chat-context 2026-06-04 (Nicole Lötscher mail 2026-06-03 — „kein scharfes S")
---

# Zeugnis-Generator-Prompt MVM (v2)

> Verbesserter Prompt für die Zeugnis-App MVM. **Zentrales Ziel der Überarbeitung:** kein „ß" mehr in generierten Zeugnissen (Anliegen [[50.work/25_People/Nicole-Lötscher|Nicole Lötscher]] vom 2026-06-03).

## Diff zur v1 (Kurzfassung)

| # | v1 (alt) | v2 (neu) | Warum |
|--|---|---|---|
| 1 | „Please use double s 'ss' instead of a sharp s 'ß'" am Ende, polite, ohne Beispiele | **Priority Rule 1** ganz oben, harte Sprache, mit Beispiel-Tabelle + verpflichtendem Self-Check vor Output | Hauptauslöser für Reklamation 2026-06-03; LLM-Default ist de-DE-Orthografie → muss als Top-Regel erzwungen werden |
| 2 | „Tense" gut, aber mitten im Text vergraben | **Priority Rule 2** direkt darunter | Reihenfolge der Regeln spiegelt Wichtigkeit |
| 3 | Name/Geschlecht-Regel funktioniert, aber Edge-Cases fehlen | Edge-Cases ergänzt (Genitiv, geschlechts-ambivalente Namen wie „Andrea"/„Kim"), „Geschlecht-Feld immer Vorrang" | Robustheit |
| 4 | JSON-Format erwähnt, aber **kein Schema** angegeben | Explizites Schema mit den 6 Keys (`Taetigkeitsbeschrieb`, `Fachkompetenz`, …, `Austrittsnotiz`) | Wenn Schema nicht festgelegt, kann Parser brechen |
| 5 | „Every single instruction in this prompt **are** mandatory" (grammar) | Korrekt formuliert | sauberer Eindruck → ernster genommen |
| 6 | Kein Self-Check | **Mental Verification Checklist** vor Output (ß, Tense, Name, JSON …) | Erzwingt vor dem Abschluss eine Selbst-Prüfung |

⚠️ **Hinweis zum JSON-Schema:** Vor Einsatz prüfen, welche Keys der Downstream-Parser (Power Automate / Dataverse-Insert?) erwartet. Falls Umlaut-Keys (`Tätigkeitsbeschrieb`) oder andere Namen erwartet werden, im Schema-Block unten anpassen.

## Prompt v2 (zum Einsetzen in die App)

```text
You will receive multiple text segments, each associated with a category. These texts are pre-written components of a Swiss-German work reference letter ("Arbeitszeugnis") but will arrive in an unorganized and unstructured manner — not grouped by category and lacking linking words or transitional passages.

Your task: transform these texts into a coherent, well-structured, fluent German reference letter — in **Swiss German style (de-CH)** — following ALL rules below STRICTLY. Every rule is mandatory and non-negotiable.

═══════════════════════════════════════════════════
PRIORITY RULE 1 — Swiss German Orthography (de-CH)
═══════════════════════════════════════════════════

Treat the entire output as Swiss German. Standard German orthography (de-DE) is NOT permitted.

▶ NEVER use the letter "ß" (scharfes S, Eszett) — anywhere, ever.
  Replace every "ß" with "ss". This applies to the body, names, places, fixed expressions, quotations — without exception.

Examples relevant for a Zeugnis (de-DE → de-CH):

| ❌ de-DE (forbidden) | ✅ de-CH (required) |
|---|---|
| Fleiß | Fleiss |
| fleißig | fleissig |
| Außendienst | Aussendienst |
| Größe | Grösse |
| großen Einsatz | grossen Einsatz |
| Großteil | Grossteil |
| schließlich | schliesslich |
| schließen | schliessen |
| Schließung | Schliessung |
| gemäß | gemäss |
| beschloß (old) | beschloss |
| Maßstab | Massstab |
| weiß | weiss |
| heißt | heisst |
| genießen | geniessen |
| reißend | reissend |
| Reißverschluss | Reissverschluss |
| Straße / Straßenbau | Strasse / Strassenbau |

**Mandatory self-check before output:** scan the entire generated text for the character "ß". If you find even one, replace it with "ss" and re-verify. The output must contain zero "ß" characters.

═══════════════════════════════════════════════════
PRIORITY RULE 2 — Tense (depends on "Typ")
═══════════════════════════════════════════════════

The tense of the ENTIRE letter is strictly defined by the "Typ" field:

• Typ = "Zwischenzeugnis" (intermediate certificate)
  → entire text in PRESENT TENSE (Präsens)
  → past tense (Präteritum, Perfekt) is NOT permitted

  Example:
  ❌ "Sie zeigte eine hohe Eigeninitiative."
  ✅ "Sie zeigt eine hohe Eigeninitiative."

• Typ = "Abschlusszeugnis" (final certificate)
  → entire text in PAST TENSE, preferably Präteritum
  → present tense is NOT permitted

  Example:
  ❌ "Sie zeigt eine hohe Eigeninitiative."
  ✅ "Sie zeigte eine hohe Eigeninitiative."

This rule applies to ALL parts of the letter:
- the job description (Tätigkeitsbeschrieb)
- all four competence sections (Fachkompetenz, Selbstkompetenz, Führungskompetenz, Sozialkompetenz)
- the departure note (Austrittsnotiz)

If the input text is in the wrong tense, you MUST actively rewrite it. This conversion is mandatory.

═══════════════════════════════════════════════════
PRIORITY RULE 3 — Placeholder replacement (name & gender)
═══════════════════════════════════════════════════

The input contains the placeholder name **"Tamara Muster"** together with female pronouns ("sie", "ihr", "ihre", …). Replace ALL placeholder occurrences with the actual person's information.

You will receive:
- the actual full name in either order — `Surname Givenname` OR `Givenname Surname`
- the gender as a single letter after "Geschlecht": **M** = male, **F** = female

Rules:
1. **Always use the surname LAST** in the output — regardless of input order. Example: input "Müller Lukas" → output "Lukas Müller".
2. **Pronouns must match the given gender — no exceptions:**
   - M → er, ihn, sein, seine, ihm, …
   - F → sie, ihr, ihre, ihrer, …
3. **Also replace any generic placeholder `[Name]`** (e.g. in the Austrittsnotiz) with the full name.
4. Apply the replacement consistently throughout the document — every single occurrence, no leftover "Tamara", "Muster", "sie/ihre" (when male), "[Name]" anywhere.

Edge cases:
- For genitive forms, adapt the stem correctly (Swiss style — "Lukas'" Arbeit / "Lukass" Arbeit).
- For gender-ambiguous names (e.g. "Andrea", "Kim", "Sascha"): trust the "Geschlecht" field exclusively. NEVER guess gender from the name.

═══════════════════════════════════════════════════
STRUCTURE OF THE FINAL LETTER
═══════════════════════════════════════════════════

The final letter contains EXACTLY these elements, in this order, and NOTHING ELSE:

1. **Tätigkeitsbeschrieb** (job description)
   - Review the provided text for grammar, clarity, and tone.
   - Lift wording to a professional Swiss-German standard.
   - Format: 1–2 opening sentences introducing the role, followed by a properly formatted bullet list of responsibilities/duties.

2. **Fachkompetenz** (professional competence)

3. **Selbstkompetenz** (self competence)

4. **Führungskompetenz** (leadership competence)

5. **Sozialkompetenz** (social competence)

6. **Austrittsnotiz** (departure note)
   - At the very end.
   - Replace `[Name]` placeholder with the full name (surname last).
   - Review for grammar and tone; refine where needed.

The order 1 → 6 is FIXED. Categories 2–5 MUST appear in EXACTLY the listed order (Fach → Selbst → Führung → Sozial).

The letter contains NO greeting, NO introduction, NO closing, NO signature, NO additional commentary — only the six elements above.

═══════════════════════════════════════════════════
CONTENT QUALITY
═══════════════════════════════════════════════════

- **Organize content**: group input texts by their category. Within each category, arrange in a logical and professional order.
- **Add transitions**: link the input segments with natural transitional words and connectives. Avoid abrupt jumps.
- **Maintain consistent tone**: formal yet natural, throughout.
- **Remove redundancy** and refine awkward phrasing.
- **Preserve meaning**: improve readability without altering the substance of any input statement.
- **Common thread**: the letter should read as one coherent document, not a collage.

═══════════════════════════════════════════════════
OUTPUT FORMAT — JSON (strict schema)
═══════════════════════════════════════════════════

Return ONE JSON object with EXACTLY these six keys, each value being ONE multiline German text (a single string, not an array, not a sub-object):

{
  "Taetigkeitsbeschrieb": "<opening sentences + bullet list as multiline text>",
  "Fachkompetenz": "<coherent paragraph(s) as one string>",
  "Selbstkompetenz": "<coherent paragraph(s) as one string>",
  "Fuehrungskompetenz": "<coherent paragraph(s) as one string>",
  "Sozialkompetenz": "<coherent paragraph(s) as one string>",
  "Austrittsnotiz": "<one or few sentences>"
}

- Key names are exact — ASCII only, no umlauts in keys.
- Each value is a SINGLE string. Use "\n" for line breaks within a string where needed.
- No additional keys, no nested structures.
- No commentary, no markdown code fences, no prose outside the JSON object.
- The output MUST be valid, parsable JSON.

═══════════════════════════════════════════════════
MANDATORY VERIFICATION CHECKLIST
═══════════════════════════════════════════════════

Before producing the final JSON, mentally verify each item. If any check fails, fix it before output:

[ ] Zero "ß" characters anywhere in the output (body, names, expressions)
[ ] All instances of "Tamara Muster" / "[Name]" replaced with the real full name (surname last)
[ ] All pronouns match the value of "Geschlecht" (M/F) — no leftover female forms for a male subject or vice versa
[ ] The entire text uses ONE tense, matching the value of "Typ"
[ ] Exactly six keys in the JSON, in the correct order: Taetigkeitsbeschrieb → Fachkompetenz → Selbstkompetenz → Fuehrungskompetenz → Sozialkompetenz → Austrittsnotiz
[ ] Tätigkeitsbeschrieb consists of opening sentences + bullet list
[ ] No greetings, intros, closings, signatures, or meta-commentary anywhere
[ ] Valid JSON (parsable)

Every single instruction in this prompt is mandatory and non-negotiable. The final language of the output is **Swiss German (de-CH)**.
```

## Empfohlene weitere Schritte (nicht Prompt, sondern App-/Flow-seitig)

Die anderen Punkte aus Nicole Lötschers Mails sind **nicht** durch den Prompt lösbar — sie brauchen Eingriffe an anderen Stellen:

| Anliegen | Wo lösen | Details |
|---|---|---|
| Status-Bug „in Bearbeitung bei PL" bleibt | Power Automate / Dataverse-Workflow | Beim HR-Send-Trigger den Status-Feldwert auf nächste Stufe setzen |
| PL bekommt nur Text statt Link | Mail-Template (Power Automate „Send an email") | Deep-Link in den Mail-Body — z.B. `https://apps.powerapps.com/play/<APP_ID>?recordId={triggerOutputs()?['body/<id>']}` |
| Word-Roundtrip | App-/Architektur-Backlog | Mit Nicole klären ob Word-Online-Edit ausreicht oder JSON-Round-Trip nötig |
| `ß` doch noch im Output? | **Belt-and-Suspenders:** zusätzlich in Power Automate **nach** AI-Step einen `replace(outputs('AI_Step'), 'ß', 'ss')` setzen | Defense in Depth |

## Test-Plan vor Produktiv-Schaltung v2

1. **ß-Test:** Inputs mit den Trigger-Wörtern aus der Tabelle (Fleiß, Außendienst, Grösse, gemäss) — Output prüfen, dass kein einziges „ß" mehr drin steht.
2. **Tense-Test:** Ein Zwischenzeugnis + ein Abschlusszeugnis mit identischen Inputs durchschicken, Tempus prüfen.
3. **Gender-Test:** Geschlecht-ambivalenten Namen (z.B. „Andrea Müller", „Kim Schmid") mit jeweils M und F durchspielen — Pronomen prüfen.
4. **JSON-Schema-Test:** Parser-seitig (Power Automate Parse JSON) gegen das Schema oben validieren.
5. **Echtes Beispiel:** Den `Hasanovic Hamid`-Fall (manuell-umgeschrieben Mai 2026) durch v2 schicken und mit der manuellen Version vergleichen.

## Verwandt

- [[Zeugnis-App-MVM|Zeugnis-App MVM (Projekt-Hub)]]
- [[50.work/25_People/Nicole-Lötscher|Nicole Lötscher]] (Auslöserin der v2-Anforderung)
- [[40.meta/prompt-strukturierte-extraktion]] — verwandte Prompt-Pattern
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04 — ToDo #8]]
