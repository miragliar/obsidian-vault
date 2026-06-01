---
source: claude-import
imported: 2026-06-01
conv_uuids: [c64ee9d8-3770-4fe2-9111-0851866733df, e4dd2cab-a348-4a94-a9a2-57fd4c6a0174]
tags: [cheatsheet, unicode, reference]
type: reference
---

# Unicode Sub-/Superscript-Referenz

Reine Tabelle zum Nachschlagen. Erklärung & Trade-offs in [[30.patterns/text-formatting/unicode-subscript-konvertierung]].

## Subscripts (tiefgestellt)

| Klasse | Verfügbar | Fehlt |
|---|---|---|
| Ziffern | `₀ ₁ ₂ ₃ ₄ ₅ ₆ ₇ ₈ ₉` | — |
| Kleinbuchstaben | `ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ` | b, c, d, f, g, q, w, y, z |
| Großbuchstaben | — | **alle** |
| Symbole | `₊ ₋ ₌ ₍ ₎` | — |
| Griechisch | `ᵦ ᵧ ᵨ ᵩ ᵪ` (β γ ρ φ χ) | α, δ, ε, … |

## Superscripts (hochgestellt)

| Klasse | Verfügbar | Fehlt |
|---|---|---|
| Ziffern | `⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹` | — |
| Kleinbuchstaben | `ᵃ ᵇ ᶜ ᵈ ᵉ ᶠ ᵍ ʰ ⁱ ʲ ᵏ ˡ ᵐ ⁿ ᵒ ᵖ ʳ ˢ ᵗ ᵘ ᵛ ʷ ˣ ʸ ᶻ` | q |
| Großbuchstaben | `ᴬ ᴮ ᴰ ᴱ ᴳ ᴴ ᴵ ᴶ ᴷ ᴸ ᴹ ᴺ ᴼ ᴾ ᴿ ᵀ ᵁ ⱽ ᵂ` | C, F, Q, S, X, Y, Z |
| Symbole | `⁺ ⁻ ⁼ ⁽ ⁾` | — |

## Small-Caps-Fallback (kein echtes Subscript, aber „kleiner Großbuchstabe")

`ᴀ ʙ ᴄ ᴅ ᴇ ꜰ ɢ ʜ ɪ ᴊ ᴋ ʟ ᴍ ɴ ᴏ ᴘ ǫ ʀ ꜱ ᴛ ᴜ ᴠ ᴡ ʏ ᴢ`

→ steht auf der Grundlinie. Nur als optische Annäherung im Plaintext-Index, niemals für Maths.

## Beispiele aus realer Vorlesung

| Quelle | Plaintext-Ergebnis | Anmerkung |
|---|---|---|
| `n_1^e` | `n₁ᵉ` | sauber, alles existiert |
| `V_a` | `Vₐ` | sauber |
| `V_A` | `Vₐ` *oder* `V_A` | kein Sub-A → klein schreiben *oder* belassen |
| `n_W^t` | `n_W` mit `ᵗ` daneben, **nicht** stapelbar | für stacked Notation → HTML/LaTeX |
| `β_b·n_s` | `βᵦ·nₛ` | `ᵦ` ist subscript-β, kann mit `_b` kollidieren — Kontext prüfen |
