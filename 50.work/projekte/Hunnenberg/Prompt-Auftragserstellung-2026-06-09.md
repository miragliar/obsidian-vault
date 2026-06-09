---
name: Hunnenberg KI — Prompt Auftragserstellung
slug: prompt-auftragserstellung-hunnenberg
klient: Hunnenberg
klient_link: "[[50.work/26_Firmen/Hunnenberg|Hunnenberg]]"
projekt_link: "[[50.work/projekte/Hunnenberg/Einfassbaender-Hunnenberg|Einfassbänder-Hunnenberg]]"
status: produktiv
version: 2026-06-09
kategorie: prompt
tags: [hunnenberg, prompt, ai-builder, power-automate, json, extraction, einfassbaender]
type: prompt-snapshot
created: 2026-06-09
---

# Hunnenberg KI — Prompt Auftragserstellung

> **Snapshot vom 2026-06-09** — aktueller produktiver Prompt im AI Builder.
> Siehe Projekt-Hub: [[50.work/projekte/Hunnenberg/Einfassbaender-Hunnenberg|Einfassbänder-Hunnenberg]]
> Pattern-Doku: [[40.meta/prompt-strukturierte-extraktion|Strukturierte JSON-Extraktion]]

## Zweck

Aus einem mehrseitigen Auftragsdokument (PDF) + E-Mail mit Lieferinfo werden alle Positionen und Lieferdaten als JSON extrahiert. Eingesetzt in einem Power-Automate-Flow mit AI Builder.

## Aufbau

- **Aufgabe 1**: Positionen extrahieren (inkl. Seitenumbruch-Logik via „Warenausgangsnr.")
- **Normalisierung**: `form`, `art_einfassung` auf erlaubte Werte mappen
- **Sonderlogik**: `farbe_einfassung` mit K-/P-Präfix-Regeln (P-Farben + Einfassbreite 1 cm → Substitution 43→38, 52→48)
- **Abgeleitete Flags**: `filterbez`, `geschorene_Teppiche`, `Black_Thermo`, `Schweissnaht`, `Riviera`, `Rutschhemmung`
- **Beschreibung**: Single-Line-String mit Pipe-Trennern ` | ` zwischen den Bestandteilen (Bezeichnung, Stk-Angabe, Einfassbreite, Farbe, ggf. Schweißen). KEINE echten Newlines im AI-Output — würde sonst „Create CSV table" sprengen.
- **Pipeline-Nachbearbeitung**: Pipe ` | ` ist NUR Transport-Format. In Power Automate wird der Pipe nach dem CSV-Build per `replace()` zu echtem CRLF konvertiert, damit Sage den Memo-Text mehrzeilig rendert. → Details im Abschnitt [Pipeline / Nachbearbeitung](#pipeline--nachbearbeitung-pipe--newline).
- **Aufgabe 2**: `auftragsnr` (mit Mengen-Summe), `kalenderwoche`, `lieferdatum` (Freitag KW), `fertigstellung` (Freitag Vorwoche), `spedition` (Mapping Verhoek=13, DPD=7, MSG=12, sonst=15)

## Prompt — Originaltext

```
Du erhältst zwei Eingaben:
1. Ein mehrseitiges **Dokument** zur Auftragserstellung  Dokumenteingabe 
2. Einen **E-Mail-Text** mit Lieferinformationen EMailText 


**Aufgabe 1 – Positionen aus dem Dokument extrahieren**

Lies alle Positionen vollständig aus und gib sie als JSON-Array zurück.

Felder pro Position:
```
position, artikel_nr, beschreibung, menge, form, laenge_m, breite_m, art_einfassung, farbe_einfassung, einfassungsbreite_cm, rueckenbeschichtung
```

**Wichtige Hinweise:**
- Das Dokument kann mehrere Seiten enthalten – lies alle Seiten vollständig.
- Eine Position kann über einen Seitenumbruch hinweg verteilt sein (maximal 2 Seiten). Erkennungszeichen: Am Anfang einer Seite erscheinen unter „Warenausgangsnr." Felder wie Farbe der Einfassung, Einfassungsbreite in cm oder Rückenbeschichtung ohne vorangehende neue Positionsnummer (also kein 1., 2., 3. etc. davor). Diese Felder gehören zur letzten Position der Vorseite — füge sie zu dieser zusammen. Eine neue Position beginnt ausschliesslich dann, wenn eine neue Nummer (1., 2., 3. …) gefolgt von einer Art.-Nr. erscheint.
- Fehlende oder nicht erkennbare Werte setzt du auf `null`.

**Normalisierung der Werte – Form und Einfassung**

Die Werte für `form` und `art_einfassung` müssen exakt auf folgende gültige Werte gemappt werden, unabhängig von Gross-/Kleinschreibung oder abweichender Schreibweise im Dokument:

**`form` – erlaubte Werte:**
| Im Dokument (Beispiele) | Wert im JSON |
|---|---|
| Rechteckig, rechteckig, RECHTECKIG | `rechteckig` |
| Rund, rund, RUND | `rund` |
| Sonderform, SF, sonderform | `SF` |
| Muster, muster | `Muster` |

**`art_einfassung` – erlaubte Werte:**
| Im Dokument (Beispiele) | Wert im JSON |
|---|---|
| Einfassung, einfassung, Einfassband, Natural Border, Zweifarbiges Baumwollband, Einfassband Baumwolle, Einfassband Protect, Natural Border Riviera, Einfassband Raulederoptik, Einfassband Leder | `Einfassung` |
| Kettelung, kettelung, Gekettelt | `Kettelung` |
| Einfassung Fransen, fransen, Fransen | `Fransen` |
| fert.Tepp, Fert. Tepp, fertigtepp, Konfektioniert, kanten umschlagen, Kantenschnitt | `fert.Tepp` |

Wenn ein Wert nicht eindeutig zugeordnet werden kann, setze ihn auf `null` und füge ein zusätzliches Feld `"mapping_hinweis"` mit dem Originalwert aus dem Dokument ein.

Ergänzungen:

**farbe_einfassung**
Führe folgende Schritte zwingend in dieser Reihenfolge aus:
Schritt 1 – Präfix prüfen:
Schau ob die Farbe mit "K "  beginnt oder mit "P "  beginnt.
Schritt 2a – Farbe beginnt mit "K ":
Übernimm die Farbe exakt so wie sie ist (inkl. "K " ). Fertig. farbe_einfassung hat in diesem Fall den gesamten Wert inkl. K.
Schritt 2b – Farbe beginnt mit "P " :
Entferne zuerst das "P " am Anfang. Du hast jetzt nur noch die Zahl (z. B. 4302).
Schritt 3 – Nur wenn "P " , Einfassbreite prüfen:

Einfassbreite = 1 cm → Ersetze die ersten zwei Ziffern durch 38 wenn die ersten beiden Ziffern 43 sind (z. B. 4302 → 3802, 4306 → 3806, 4312 → 3812). Ersetze die ersten beiden Ziffern durch 48 wenn die ersten beiden Ziffern 52 sind (z. B. 5298→ 4898, 5234→ 4834, 5200→ 4800). Fertig. farbe_einfassung hat in diesem Fall nur die Zahl drin.


---

**filterbez**

| Im Dokument (Beispiele) | Wert im JSON |
|'Zweifarbiges Baumwollband'|'Tallin'|
|'Einfassband Baumwolle'|'BW'|
|'Einfassband Protect'|'Objecta'|
|'Natural Border'|'natural border'|
|'Natural Border Riviera'|'natural border'|
|'Einfassband Raulederoptik'|'Rauleder'|
|'Einfassband Leder'|'Leder'|
|'Einfassung Fransen'|'Fransen'|
|'Konfektioniert, kanten umschlagen'|'fertige Teppiche'|
|'Kantenschnitt'|'fertige Teppiche'|
|'Gekettelt'|null|
|'Corfu'|'Corfu'|
|'Malta'|'Malta'|
|'Menorca'|'Menorca'|
|'Capri'|'Capri'|
|'Rodi'|'Rodi'|
|'Milo'|'Milo'|

**geschorene_Teppiche**
"Ja": Wenn die Artikelbeschreibung einer der folgenden Werte enthält: 
Glory, ID Glossy, Grace, Helix, Highs x Sighs, Loft, Maxime, Move, Poodle, Pure Silk, Pure Wool, Rolex, Silky Seal, Smoozy, Blogg, Eddy, Flash, Frizzle, Glamour, Marc Ten, Mondiale, Mood, Moody, Peak, Shiny, Shift, Sheen, Slim, Splash, Tosh
"Nein": in allen anderen Fällen.

**Black_Thermo**
"Ja": Wenn die Rückenbeschichtung einer der folgenden Werte enthält: 
Black Thermo, black thermo, Black thermo, black Thermo
"Nein": in allen anderen Fällen.

**Schweissnaht**
"Ja": Wenn die Form einer der folgenden Werte enthält: 
Schweissnaht, Schweißnaht
"Nein": in allen anderen Fällen.

**Riviera**
"Ja": Wenn die Art der Einfassung einer der folgenden Werte enthält: 
Riviera, riviera
"Nein": in allen anderen Fällen.

**Rutschhemmung**
"Ja": Wenn `breite_m` grösser als 4 (m) ist UND die Rückenbeschichtung einer der folgenden Werte enthält: 
Rutschhemmung, rutschhemmung
"Nein": in allen anderen Fällen.


---

**beschreibung**

Aufbau in dieser Reihenfolge:

1. Erste Zeile der Beschreibung aus dem PDF
2. `[Menge] Stk. á [Länge] x [Breite] m`
3. Nur wenn Einfassbreite vorhanden: `Einfassbreite: [X] cm`
4. Farbe: `farbe_einfassung` aus obiger Logik, jedoch mit `P ` wieder vorangestellt (bei K-Farben bleibt es wie es ist)
5. Nur wenn PDF-Beschreibung „Schweissen", „Schweissnaht" o. Ä. enthält: `Schweißen` anhängen

**Wichtig — Trennung der Punkte 1–5:** Die einzelnen Bestandteile MÜSSEN im finalen `beschreibung`-String durch ` | ` (Leerzeichen-Pipe-Leerzeichen) getrennt sein. Der Wert ist ein einzeiliger String. KEINE echten Zeilenumbrüche, KEIN `\n`, KEIN `<br>`, KEIN ` - `, KEIN ` / `.

Grund: Der String wird in eine CSV-Spalte geschrieben (Power Automate „Create CSV table") und in Sage importiert. Echte Newlines würden die CSV-Zeilenstruktur zerstören; Sage stellt das Pipe-Zeichen als sichtbaren Trenner im Memo-Feld dar.

**Beispiel ohne Schweissen — logische Struktur (so denkst du den Inhalt):**
```
FLOW x GLOW 760
2 Stk. á 2,50 x 3,20 m
Einfassbreite: 1 cm
P 3802
```

**Beispiel ohne Schweissen — tatsächlicher `beschreibung`-Wert im JSON:**
```
"beschreibung": "FLOW x GLOW 760 | 2 Stk. á 2,50 x 3,20 m | Einfassbreite: 1 cm | P 3802"
```

**Beispiel mit Schweissen — logische Struktur:**
```
SILKY SEAL 1224 MALACHIT
1 Stk. á 8,20 x 5,50 m
K 9032
Schweißen
```

**Beispiel mit Schweissen — tatsächlicher `beschreibung`-Wert im JSON:**
```
"beschreibung": "SILKY SEAL 1224 MALACHIT | 1 Stk. á 8,20 x 5,50 m | K 9032 | Schweißen"
```

---

**Aufgabe 2 – Auftragsnr. und Lieferinformationen extrahieren**

- **`auftragsnr`**: Die Auftragsnummer steht auf der ersten Seite des Dokuments, immer direkt nach dem Wort **„Auftragsnr."**. Falls die Auftragsnummer das Wort „ORD" enthält, entferne dieses. Formatiere den Wert im JSON als: `"P-[Auftragsnr.] - [Summe aller Mengen] Stk."` (Beispiel: `"P-12345 - 8 Stk."`, wobei 8 die Summe aller `menge`-Werte aller Positionen ist).
- **`kalenderwoche`**: Die KW-Angabe aus dem E-Mail (z.B. `"KW 11 2025"`)
- **`lieferdatum`**: Der **Freitag** der genannten Kalenderwoche (ISO 8601, z.B. `"2025-03-14"`)
- **`fertigstellung`**: Der **Freitag der Vorwoche** (eine KW früher)
- **`spedition`**:  Wenn "Verhoek" (od. ähnlich) dann 13, wenn "DPD" dann 7, wenn MSG dann 12. Sonst 15

---

**Ausgabe – ausschliesslich als JSON, ohne Erläuterungen:**
```json
{
  "lieferinfo": {
    "auftragsnr": "P-12345 - 8 Stk.",
    "kalenderwoche": "KW 11 2025",
    "lieferdatum": "2025-03-14",
    "fertigstellung": "2025-03-07",
    "spedition": "13"
  },
  "positionen": [
    {
      "position": 1,
      "artikel_nr": "...",
      "beschreibung": "FLOW x GLOW 760 | 2 Stk. á 2,50 x 3,20 m | Einfassbreite: 1 cm | P 3802",
      "menge": 2,
      "form": "rechteckig",
      "laenge_m": 1.5,
      "breite_m": 0.8,
      "art_einfassung": "Kettelung",
      "farbe_einfassung": "...",
       "filterbez": "Objecta",
      "einfassungsbreite_cm": 3,
      "rueckenbeschichtung": "...",
      "geschorene_Teppiche": "Nein",
      "Black_Thermo": "Nein",
      "Schweissnaht": "Nein",
      "Riviera": "Nein",
      "Rutschhemmung": "Nein",
    }
  ]
}
```

Antworte ausschliesslich mit einem JSON-Objekt. Kein Text davor, kein Text danach, keine Markdown-Formatierung, keine Backticks. Das JSON muss zwingend "positionen" enthalten. Gibt es kein positionen ist die Antwort falsch.
```

## Pipeline / Nachbearbeitung: Pipe → Newline

**Ziel:** Im Sage-Memo-Feld soll der `beschreibung`-Text mehrzeilig dargestellt werden (echte CRLF zwischen Zeilen). Der Pipe ` | ` im AI-Output ist nur Transport-Format und wird in Power Automate nach dem CSV-Build durch echtes `\r\n` ersetzt.

### Reihenfolge der Power-Automate-Steps

```
1. Trigger (Mail mit Anhang)
2. AI Builder — Prompt ausführen
3. Parse JSON — Schema mit `positionen[]` + `lieferinfo`
4. Apply to each positionen   ← (oder Select)
   └── (weitere Verarbeitung)
5. Create CSV table             ← Pipe ` | ` ist hier noch im beschreibung-Feld
6. Compose — "CSV mit Newlines" ← HIER der replace()
7. Create file (.csv)           ← Output von Step 6 als Dateiinhalt
8. Sage-Import (manuell oder automatisiert)
```

### Expression für Step 6 (Compose)

```
replace(body('Create_CSV_table'), ' | ', decodeUriComponent('%0D%0A'))
```

- `body('Create_CSV_table')` → das fertige CSV als String
- ` | ` (Leerzeichen-Pipe-Leerzeichen) → der Trenner aus dem AI-Output
- `decodeUriComponent('%0D%0A')` → echtes CRLF (Windows-Newline, von Sage erwartet)
- Falls Sage Unix-Newlines erwartet: `decodeUriComponent('%0A')` (nur LF)

### Caveats

1. **Pipe darf nirgendwo sonst in der CSV vorkommen.** Der `replace()` ist global auf dem ganzen CSV-String. In Teppich-Artikelbeschreibungen kommt ` | ` praktisch nie natürlich vor → safe. Falls doch (z. B. in `artikel_nr`), Trenner-Token ändern auf etwas garantiert Eindeutiges wie `<<NL>>` und im Prompt entsprechend anpassen.

2. **CSV-Quoting in `Create CSV table`:** Die Standard-Action quotet Felder nicht automatisch, wenn sie Newlines enthalten. Nach Step 6 stehen also echte `\r\n` im CSV ohne `"..."` drumherum. Sage muss CSV-Felder mit eingebetteten Newlines lesen können (in den meisten Versionen via Import-Mapping konfigurierbar). Falls Sage abbricht:
   - Variante A: Spalte `beschreibung` im Sage-Import-Mapping explizit als „Memo" / „Multi-Line" markieren
   - Variante B: CSV-Build refactoren — `Create CSV table` ersetzen durch eigenen Select + Compose mit manuellem `"…"`-Quoting

3. **Reihenfolge wichtig:** `replace()` MUSS nach `Create CSV table` passieren. Wenn man den Pipe schon vorher zu Newlines macht (im Select pro Position), zerschießt `Create CSV table` die Struktur.

### Test-Vorgehen

1. AI-Builder-Output prüfen: enthält `beschreibung` ` | ` (mit Spaces), keine `\n`?
2. CSV nach Step 5 anschauen: alle Zeilen auf je 1 Zeile, Pipe noch drin?
3. CSV nach Step 6 anschauen: Pipe ersetzt durch CRLF (in Notepad++ mit „Show All Characters" sichtbar)?
4. In Sage importieren, Memo-Feld einer Position öffnen → mehrzeilig?

## Changelog

- **2026-06-09 (Update 4)** — Pipe ` | ` ist nur Transport-Format. Neuer Abschnitt „Pipeline / Nachbearbeitung" mit Power-Automate-Replace-Expression (`replace(body('Create_CSV_table'), ' | ', decodeUriComponent('%0D%0A'))`) und Caveats — am Ende soll Sage echte CRLF im Memo sehen.
- **2026-06-09 (Update 3)** — `beschreibung` umgestellt von `\n`-Newlines auf Pipe-Trenner ` | ` (Single-Line-String). Grund: CSV-Pipeline („Create CSV table" → Sage) verträgt keine echten Newlines in Feldern; Pipe ist robuster und in Sage als visueller Trenner sichtbar. Update 2 (Newlines) damit revidiert.
- **2026-06-09 (Update 2)** — ~~`beschreibung` MUSS echte Zeilenumbrüche (`\n`) enthalten.~~ **Revidiert in Update 3** (siehe oben).
- **2026-06-09 (Update 1)** — Neues Flag `Rutschhemmung`: `"Ja"` wenn `breite_m > 4` UND `rueckenbeschichtung` enthält `Rutschhemmung`/`rutschhemmung`, sonst `"Nein"`.
- **2026-06-09** — Initial snapshot. Neu vs. früheren Versionen: `filterbez`, `geschorene_Teppiche`, `Black_Thermo`, `Schweissnaht`, `Riviera`, expliziter `beschreibung`-Aufbau mit 5 Zeilen.

## Verwandt

- [[50.work/projekte/Hunnenberg/Einfassbaender-Hunnenberg|Projekt-Hub Einfassbänder]]
- [[50.work/26_Firmen/Hunnenberg|Klient: Hunnenberg]]
- [[40.meta/prompt-strukturierte-extraktion|Pattern: Strukturierte JSON-Extraktion]]
- [[50.work/power-platform/ai-prompt-json-output|AI Builder Prompts — JSON-Output]]
