---
source: claude-import
imported: 2026-06-01
conv_uuids: [c4a6635a-30be-4b75-8836-ccf9420483f1, e4dd2cab-a348-4a94-a9a2-57fd4c6a0174]
tags: [word, docx, xml, python, subscript, automation]
---

# DOCX-Subscripts: `X_Y` batch-weise zu echten Subscripts konvertieren

## Problem

Ein Word-Dokument (z.B. Vorlesungs-Zusammenfassung) enthält ~200 Vorkommen von Underscore-Notationen wie `V_A`, `U_i`, `n_W`, `n_S`, `β_b`. Im Text sind das **literal underscores**. Sie sollen zu echten typografischen Subscripts werden (`V` mit kleinem hochgesetztem `A`), damit das Dokument publikationsreif ist.

Manuelles Klicken durch jede Stelle in Word skaliert nicht. „Suchen/Ersetzen mit Formatierung" in Word funktioniert für **einzelne** Subscript-Zeichen, aber nicht zuverlässig für hunderte Patterns mit unterschiedlichem Run-Kontext.

## Lösung

DOCX ist ein ZIP mit XML drin. Der relevante Teil ist `word/document.xml`. Subscript wird per Run-Property `<w:vertAlign w:val="subscript"/>` ausgezeichnet. Konkrete Strategie:

```
DOCX  →  unzip  →  document.xml  →  Regex/XML-Patch  →  rezip  →  DOCX
```

### Anatomie eines Word-Runs

```xml
<w:r>
  <w:rPr>…Font, Größe, Farbe…</w:rPr>
  <w:t>V_A</w:t>
</w:r>
```

Um `V_A` zu konvertieren, splittet man den Run in **zwei** Runs, übernimmt die `<w:rPr>` und fügt im zweiten Run ein `<w:vertAlign w:val="subscript"/>` ein:

```xml
<w:r>
  <w:rPr>…Original…</w:rPr>
  <w:t>V</w:t>
</w:r>
<w:r>
  <w:rPr>…Original…<w:vertAlign w:val="subscript"/></w:rPr>
  <w:t>A</w:t>
</w:r>
```

### Python-Workflow (Skizze)

```python
import zipfile, shutil, re
from pathlib import Path

src = Path("Section_2.docx")
dst = Path("Section_2_subscripts.docx")
work = Path("/tmp/docx_unpack")

# 1) Entpacken
shutil.rmtree(work, ignore_errors=True)
with zipfile.ZipFile(src) as z:
    z.extractall(work)

xml = (work / "word/document.xml").read_text(encoding="utf-8")

# 2) Pattern: ein Buchstabe + "_" + ein Buchstabe/Ziffer
#    matched innerhalb <w:t>...</w:t>
RUN_RE = re.compile(
    r'(<w:r>\s*<w:rPr>(?P<rpr>.*?)</w:rPr>\s*<w:t[^>]*>)(?P<text>[^<]*?)([A-Za-z])_([A-Za-z0-9])([^<]*?)(</w:t>\s*</w:r>)',
    re.DOTALL,
)

def split(m):
    pre, rpr, before, base, sub, after, post = m.group(1), m.group("rpr"), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)
    new = []
    # leading text + base letter (Normalformat)
    new.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{before}{base}</w:t></w:r>')
    # subscript run
    new.append(f'<w:r><w:rPr>{rpr}<w:vertAlign w:val="subscript"/></w:rPr><w:t xml:space="preserve">{sub}</w:t></w:r>')
    # trailing text
    if after:
        new.append(f'<w:r><w:rPr>{rpr}</w:rPr><w:t xml:space="preserve">{after}</w:t></w:r>')
    return "".join(new)

# Wiederholen bis keine Treffer mehr (mehrere Patterns pro Run)
prev = None
while prev != xml:
    prev = xml
    xml = RUN_RE.sub(split, xml)

(work / "word/document.xml").write_text(xml, encoding="utf-8")

# 3) Repack
if dst.exists(): dst.unlink()
with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
    for f in work.rglob("*"):
        if f.is_file():
            z.write(f, f.relative_to(work))
```

### Edge Cases, die man beim ersten Durchlauf vergisst

| Edge Case | Folge | Fix |
|---|---|---|
| `_` liegt **zwischen** zwei `<w:t>`-Elementen (Word splittet Runs nach Wortgrenzen) | Pattern matcht nicht | Vor dem Patch: benachbarte Runs mit identischem `<w:rPr>` mergen |
| Run enthält `<w:drawing>` oder `<w:lastRenderedPageBreak/>` zwischen `<w:rPr>` und `<w:t>` | Pattern matcht nicht (Strict-Regex) | Permissiveres Pattern: `<w:rPr>...</w:rPr>(?:(?!<w:t).)*<w:t>` |
| Run hat **keine** `<w:rPr>` | Pattern matcht nicht | Zweiter Pattern mit optionalem `<w:rPr>` oder Default-rPr einfügen |
| Underscore steht in echtem Code/URL (`https://x_y/`) | Falscher Positive | Pattern auf Buchstaben-um-Buchstabe einschränken: `([A-Za-z])_([A-Za-z0-9])(?![A-Za-z0-9_])` |
| Mehrere Subscripts im selben Run (`V_A V_B U_i`) | Erster wird gepatcht, Rest nicht | `while prev != xml: …` Schleife (s.o.) |
| `xml:space="preserve"` fehlt | führende/trailing Spaces verschwinden | Immer mit Attribut setzen |

### Validierung

1. Mit Word/LibreOffice öffnen → optisch prüfen
2. `unzip -p out.docx word/document.xml | grep -c 'vertAlign w:val="subscript"'` → Zähler sollte = erwartete Treffer
3. `unzip -p out.docx word/document.xml | grep -oE '[A-Za-z]_[A-Za-z]' | sort -u` → Soll-leer (alle konvertiert)

## Wann nicht

- **`python-docx` reicht:** für einfache Fälle (neuer Inhalt schreiben, ein Wort fett machen) → kein Regex-Patchen nötig. Diese Strategie ist **nur** für Mass-Patches an bestehenden Runs mit erhaltener Formatierung sinnvoll.
- **LaTeX-Workflow:** wenn das Dokument ohnehin in LaTeX kompiliert wird → einfach `$X_Y$` schreiben, kein DOCX-Patching nötig.
- **Wenn Notation primär gelesen, nicht gedruckt wird** (Notiz-App, Mail): Unicode-Subscripts reichen → [[30.patterns/text-formatting/unicode-subscript-konvertierung]].
- **Wenn Quellfile in Google Docs liegt:** Apps Script statt Python; Run-Modell ist anders.
- **Bei wenigen Vorkommen** (<20): manuelles Markieren in Word ist schneller als Skript-Engineering + Edge-Case-Jagd.

## Alternativen

- **Pandoc-Round-Trip:** DOCX → Markdown → Subscripts via `~X~`-Syntax → DOCX zurück. Sauberer, aber verliert oft komplexe Formatierung (Spalten, Boxen, Stile).
- **VBA-Makro in Word:** `Selection.Find` mit `Replacement.Font.Subscript = True`. Funktioniert für simple Patterns, scheitert oft an Run-Boundaries genauso wie naives Suchen/Ersetzen.
- **`docx2python` zum Lesen + `python-docx` zum Schreiben einer neuen Datei:** kompletter Rewrite, verliert ebenfalls Style-Details.

## Verwandt

- [[30.patterns/text-formatting/unicode-subscript-konvertierung]] — die Plaintext-Variante
- [[30.patterns/text-formatting/unicode-sub-sup-referenz]]
- [[20.studies/Organizational-Economics/Hub]] — Quelle (Section-2-Zusammenfassung der OE-Vorlesung)
