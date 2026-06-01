---
source: claude-import
imported: 2026-06-01
conv_uuids: [a2cce3c8-c4cc-4e91-bdd0-5c60ba033abb, b2616010-3e32-4ebc-9bcc-bbed5c7d744c, a2b43ae4-94f5-41d0-a234-72a064efd928, 0cf3d431-ac67-4c46-8eb4-90ad7e9d094e]
tags: [video, science-to-public, voice-over, talking-head, seminararbeit]
---

# Science-to-Public Video — Strategie & Editing-Basics

Notizen aus dem Video-Projekt fürs Seminar „Besessenheitsdiskurse" (Anneliese-Michel-Kontext).

## Konzept: Voice-Over ↔ Talking Head wechseln

**Voice-Over (VO):** Stimme im Off, Bild zeigt Symbol-/Illustrationsmaterial oder B-Roll.
**Talking Head (TH):** Sprecher:in direkt im Bild, oft im Studio-/Greenscreen-Setup.

Wechsel-Strategie (für Science-to-Public-Format):

| Zweck | Modus |
|---|---|
| Persönliche Authentizität, „Ich-bin-da" | Talking Head |
| Dichte Information / Argumentation | Voice-Over mit visuellem Material |
| Spannungs-/Pausen-Effekt | TH-Cut nach VO |
| Quellen-Verweise / Zitate | VO mit eingeblendetem Text |
| Emotionaler Höhepunkt | TH, langsamer Cut |

→ Faustregel: 60–70 % VO, 30–40 % TH; im 5-Minuten-Video etwa 3–5 TH-Inserts à 10–20 Sek.

## Symbolverwendung — Konkretheit ist Sieg

Beispiel aus eigener Iteration: „Gefängnistür" → „Gerichtshammer" als Symbol für Aschaffenburger Prozess.

| Schwach (abstrakt) | Stark (konkret) |
|---|---|
| Gefängnistür | Gerichtshammer |
| „die Kirche" | Tür/Gewölbe einer Würzburger Kirche |
| „die Medien" | Tonband (echtes Material aus dem Fall) |
| „die Wissenschaft" | EEG-Streifen aus medizinischer Akte |

Konkrete Symbole sind **suchbar** in Stock-Bibliotheken, **wiedererkennbar** beim Publikum, **historisch genauer** als generische Bilder.

## Sprechtext-Disposition

- Erst Sprechtext schreiben, dann Bilder zuordnen — nicht umgekehrt
- Pro Satz/Halbsatz: **ein** visuelles Element
- Dauer einer Voice-Over-Phrase: 3–5 Sek (= 8–14 Wörter)
- Bei Talking Head: 10–20 Sek Block, danach Schnitt für Atemzug

Disposition-Format:

```
[VO] „Anneliese Michel starb am 1. Juli 1976."  | Schwarzes Standbild
[TH] „Was passierte in den Jahren davor?"          | Sprecher direkt
[VO] „Diagnose Temporallappenepilepsie..."        | EEG-Animation
```

## DaVinci Resolve — Basis-Skills

Häufig stolpernde Anfänger-Anforderungen:

| Aufgabe | Tool / Vorgehen |
|---|---|
| Übergang (Crossfade, Cut) | `Effects Library → Video Transitions` zwischen zwei Clips |
| Bild über Bild (PiP) | Zweite Video-Spur, `Transform → Scale + Position` |
| Split-Screen | Beide Clips auf separate Spuren, beide `Transform → Position` auf ±X-Achse |
| Slow-Zoom (Ken Burns) | Keyframes auf `Transform → Scale` (Anfang 1.0, Ende 1.15) |
| Untertitel | `Effects Library → Titles → Subtitle` oder `Edit Index → Subtitle` |
| Voice-Over aufnehmen | Mikrofon-Spur, `Inspector → Audio` für Pegel |
| Color-Grading | `Color`-Tab, `Lift/Gamma/Gain`-Wheels |
| Final Export | `Deliver`-Tab, Preset H.264 1080p für Web |

## Filmage Editor — Slow-Zoom („Ken Burns")

Filmage nennt die Funktion **Keyframe** (selbe Logik wie DaVinci):

1. Bild auf Timeline ziehen, Dauer einstellen (z.B. 5 Sek)
2. Bild anklicken → Keyframe-Panel öffnen
3. Bei `t=0`: `Scale = 1.0`, `Position = (0, 0)`
4. Bei `t=5`: `Scale = 1.15`, `Position = (0, 0)` (oder leicht versetzt für Pan)
5. Vorschau prüfen, evtl. mit `Easing` glätten

→ Klassischer „Ken Burns Effekt" — langsame Kamerafahrt auf einem Standbild, wirkt cineastisch.

## Pattern: Feedback-Mail mit Video-Link

Wenn du jemandem (Dozent:in, Kolleg:in) einen Video-Entwurf zur Begutachtung schickst:

```
Vielen Dank für das ausführliche Feedback. Ich komme gerne auf dein
Angebot zurück und schicke dir eine erste Version meines Videos:
[Link Dropbox / Cloud].

Über Verbesserungsvorschläge wäre ich sehr dankbar.

Mein Ziel war es — wie du auch der angehängten Disposition entnehmen
kannst — zwischen Voice-Over und Talking Head zu wechseln.
Im Sprechtext habe ich mittlerweile 2–3 Anpassungen vorgenommen
(z.B. ersetzt der Gerichtshammer die Gefängnistür). Das Video weicht
also leicht vom Sprechtext ab, inhaltlich hat sich aber kaum etwas
geändert. Der Fokus darf ganz auf Layout und Gesamtwirkung liegen.
```

**Sprachliche Schärfungen:**
- „mal ... mal" → weglassen (umgangssprachlich, doppelt)
- „potenzielle Verbesserungsvorschläge" → „Verbesserungsvorschläge" (potenziell = redundant)
- Em-Dashes → Halbgeviertstrich oder Komma
- Konjunktiv-Wendung statt Imperativ („wäre ich sehr dankbar")

## Wann nicht

- **Bei sehr kurzen Videos (<2 min):** Wechsel VO/TH wirkt hektisch. Bei einem Format entscheiden.
- **Bei Vorträgen / Live-Aufzeichnungen:** Talking Head ohne Schnittwechsel reicht — produktionsökonomisch sinnvoll.
- **Bei reinen Animations-Erklärvideos:** Voice-Over only; TH wäre Ablenkung.
- **Bei Slack-Loom-Updates für Kolleg:innen:** Authentizität > Editing. Roh-TH ohne Cuts ist angemessen.

## Verwandt

- [[20.studies/Anneliese-Michel/03-Filmanalyse-Requiem-2006]] — Inhaltlicher Kontext (was zeigt Schmid, was ergänzt eigenes Video)
- [[20.studies/video-media/_README]]
