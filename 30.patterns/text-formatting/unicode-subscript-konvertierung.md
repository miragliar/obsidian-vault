---
source: claude-import
imported: 2026-06-01
conv_uuids: [c64ee9d8-3770-4fe2-9111-0851866733df, e4dd2cab-a348-4a94-a9a2-57fd4c6a0174]
tags: [text, unicode, subscript, superscript, plaintext]
related: [[30.patterns/text-formatting/unicode-sub-sup-referenz]]
---

# Unicode-Subscript-Konvertierung (Plaintext)

## Problem

Formeln aus Vorlesungs-/Skript-Texten enthalten Notationen wie `n_W`, `V_A`, `n^t`, `n_1^e`. In Plaintext (Markdown, E-Mail, Notiz-App ohne Rich-Text) sollen sie als „kleine, tiefgestellte/hochgestellte" Zeichen erscheinen — ohne HTML, ohne Word.

Naive Annahme: Unicode liefert für alle Buchstaben/Ziffern echte Sub-/Superscripts. **Das stimmt nicht.** Es gibt nur eine Teilmenge — und genau diese Lücke ist die häufigste Frustquelle.

## Lösung

**Tatsächlich verfügbare Unicode-Subscripts (vollständig):**

- **Ziffern:** `₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉`
- **Kleinbuchstaben:** `ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ`
  → fehlen: **b, c, d, f, g, q, w, y, z**
- **Großbuchstaben:** **keine**.
- **Symbole:** `₊ ₋ ₌ ₍ ₎`
- **Griechisch:** `ᵦ` (beta), `ᵧ` (gamma), `ᵨ` (rho), `ᵩ` (phi), `ᵪ` (chi)

**Superscripts (vollständig):**

- **Ziffern:** `⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹`
- **Kleinbuchstaben:** `ᵃ ᵇ ᶜ ᵈ ᵉ ᶠ ᵍ ʰ ⁱ ʲ ᵏ ˡ ᵐ ⁿ ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ` (fast vollständig, fehlen q)
- **Symbole:** `⁺ ⁻ ⁼ ⁽ ⁾`

**Strategien für fehlende Glyphen (priorisiert):**

1. **Im Quelltext klein schreiben** (`V_a` statt `V_A`) → echte Unicode-Subscripts → optisch konsistent. Pragmatisch & sauber, akzeptiert Verlust der Groß-/Kleinschreibung im Index.
2. **Small-Caps-Unicode als Fallback für Großbuchstaben:** `ᴀ ʙ ᴄ ᴅ ᴇ ꜰ ɢ ʜ ɪ ᴊ ᴋ ʟ ᴍ ɴ ᴏ ᴘ ǫ ʀ ꜱ ᴛ ᴜ ᴠ ᴡ ʏ ᴢ`. Sieht aus wie kleine Großbuchstaben, ist **kein** echtes Subscript (steht auf der Grundlinie). Nur als visuelle Annäherung.
3. **`_X` einfach so stehen lassen.** Bei z.B. `n_W` hässlich, aber semantisch eindeutig.
4. **HTML mit `<sub>` / `<sup>`** — der einzige Weg für echte tiefgestellte Großbuchstaben, funktioniert aber nur, wo HTML interpretiert wird (Webnotizen, GitHub Markdown, Obsidian-Renderer ja, Plaintext-Editor nein).
5. **Doppel-Glyphe als Notnagel** vermeiden: `ᵥᵥ` als Pseudo-w sieht nach „vv" aus, nicht nach „w" — verwirrt Leser.

**Mini-Algorithmus zum manuellen Konvertieren von `X_Y` und `X^Y`:**

1. `Y` mit der obigen Tabelle prüfen.
2. Existiert echtes Subscript/Superscript → ersetzen.
3. Existiert nicht & Y ist Großbuchstabe → Lower-case prüfen → ggf. mit Hinweis im Text klein schreiben, oder Small-Caps-Fallback.
4. Stacked sub+sup auf gleichem Symbol (`n_W^t`) → in Plaintext **nicht stapelbar**. Entweder einen weglassen oder HTML.

## Wann nicht

- **Wenn die Notation publikationsrelevant ist** (Seminararbeit, wiss. Paper): nicht Unicode-basteln, sondern echte Sub-/Superscripts in Word/LaTeX (s. [[30.patterns/text-formatting/docx-subscripts-batch-konvertieren]]).
- **Wenn das Zieldokument HTML rendert** (Obsidian, Notion, GitHub-MD): `X<sub>Y</sub>` ist semantisch sauberer und löst das Lücken-Problem komplett.
- **Wenn Mathe-Tiefe verlangt ist:** Lieber LaTeX-Inline (`$n_W^t$`) statt Unicode-Approximation — Obsidian rendert das, kopierbar in alle wiss. Workflows.
- **Wenn Großbuchstaben semantisch zwingend sind** (z.B. `V_A` vs. `V_a` haben unterschiedliche Bedeutung im Modell): Klein-Schreiben ist ein Bug, nicht ein Feature. → HTML/LaTeX.

## Verwandte Trade-offs

- **„Sieht klein aus" ≠ „ist Subscript":** Small-Caps stehen auf der Grundlinie. Echte Subscripts liegen tiefer. In Fließtext fällt es auf, in einer Notiz nicht.
- **Copy-Paste-Robustheit:** Unicode-Subscripts überleben fast überall (Slack, Mail, Web). LaTeX nicht. HTML nur in Rendering-Targets.
- **Suchbarkeit:** `n₁` ist nicht dasselbe Token wie `n1` oder `n_1` — Volltextsuche bricht. Bei suchintensivem Material lieber `n_1` lassen oder zusätzlich indexieren.
- **Accessibility/Screenreader:** Unicode-Subscripts werden oft als „kleine Eins" oder gar nicht vorgelesen. HTML `<sub>` ist semantisch markiert.

## Verwandt

- [[30.patterns/text-formatting/unicode-sub-sup-referenz]] — die Tabelle als reine Cheat-Sheet
- [[30.patterns/text-formatting/docx-subscripts-batch-konvertieren]] — Word-DOCX direkt patchen
- [[20.studies/Organizational-Economics/Hub]] — Quelle vieler `V_A`/`n_W^t`-Formeln
