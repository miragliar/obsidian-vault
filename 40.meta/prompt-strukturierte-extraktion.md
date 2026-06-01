---
source: claude-import
imported: 2026-06-01
conv_uuids: [c1f21b4d-9f2e-4104-a708-cb44ee69e60e, eaee47ae-5ef8-4539-8ab2-2ab2bebd9162]
tags: [claude, prompt, json, extraction, dokumenten-analyse, power-platform]
---

# Prompt-Pattern: Strukturierte JSON-Extraktion aus Geschäfts-Dokumenten

Pattern für die wiederkehrende Aufgabe: aus einem mehrseitigen Geschäfts-Dokument (Auftrag, Rechnung, Lieferschein) **strukturierte Felder** zuverlässig in JSON extrahieren — inkl. Fallstricke wie seitenübergreifender Positionen und Datums-Berechnungen.

## Anatomie eines belastbaren Extraktions-Prompts

```
1. Eingaben klar benennen (Dokument + E-Mail-Text + ...)
2. Aufgaben durchnummeriert
3. Pro Aufgabe: Ausgabeformat (JSON-Schema)
4. Edge-Cases als "Wichtige Hinweise" explizit
5. Fehlende Werte: was tun? (null vs. "—" vs. weglassen)
6. "Nur das JSON ausgeben, keine Erklärungen"
```

## Beispiel — Mehrteiliges Auftragsdokument

Verdichteter Prompt aus realem Power-Automate-AI-Builder-Einsatz:

```
Du erhältst zwei Eingaben:
1. Ein mehrseitiges Dokument zur Auftragserstellung
2. Einen E-Mail-Text mit Lieferinformationen

---

Aufgabe 1 – Positionen aus dem Dokument extrahieren

Lies alle Positionen vollständig aus und gib sie als JSON-Array zurück.

Felder pro Position:
  position, artikel_nr, beschreibung, menge, form,
  laenge_m, breite_m, art_einfassung, farbe_einfassung,
  einfassungsbreite_cm, rueckenbeschichtung

Wichtige Hinweise:
- Mehrseitig: lies alle Seiten vollständig.
- Eine Position kann über zwei Seiten verteilt sein.
  Erkennung: Tabellenartige Auflistung unter "Warenausgangsnr."
  wird auf der nächsten Seite fortgesetzt, ohne dass eine
  neue Position beginnt → zu EINER Position zusammenführen.
- Fehlende oder nicht erkennbare Werte: null.

---

Aufgabe 2 – Lieferinformationen extrahieren

Aus dem E-Mail-Text und der ersten Seite des Dokuments:

{
  "auftragsnr": "<von Seite 1 des Dokuments>",
  "spedition": "<aus E-Mail>",
  "kalenderwoche": <int>,
  "lieferdatum": "<Freitag dieser KW als YYYY-MM-DD>",
  "fertigstellung": "<Freitag der KW davor als YYYY-MM-DD>"
}

---

Ausgabe:
Nur ein einziges JSON-Objekt mit zwei Top-Level-Keys:
  "positionen": [...],
  "lieferinfo": { ... }

Keine Erklärungen davor oder danach.
```

## Pattern-Bausteine im Detail

### 1. Seitenübergreifende Logik

Tabellen mit Fortsetzungs-Header ("Warenausgangsnr.") sind die häufigste Fehlerquelle. Im Prompt **explizit** sagen, woran man die Fortsetzung erkennt — sonst werden zwei halbe Positionen als zwei eigenständige interpretiert.

### 2. Datums-Konvertierungen mit Wochenlogik

Die KI rechnet KW → Datum überraschend zuverlässig, aber:
- ISO-Wochenzählung explizit machen
- Jahr festlegen (sonst rät die KI evtl. 2024 vs. 2025)
- Beispiel im Prompt liefern: „KW 23 → Freitag 06.06.2025"

### 3. Fehlende Werte — eine einheitliche Konvention

Die drei häufigen Optionen:

| Konvention | Wann |
|---|---|
| `null` | für JSON-Konsumenten (z.B. Power Automate Parse JSON) — pflicht, weil sonst Schema bricht |
| `"—"` | für menschenlesbare Outputs |
| Feld weglassen | nur, wenn nachgelagerter Code das toleriert (riskant) |

Empfohlen: **`null` mit explizitem Hinweis im Prompt.**

### 4. „Nur JSON ausgeben"

Standardsatz am Ende:

> Gib nur das JSON aus. Keine Erklärungen, keine Code-Blöcke, kein Markdown.

Manche Modelle wrappen trotzdem in ```json ... ``` — defensive parsing-Logik einbauen.

### 5. Schema-Validierung als Sicherheitsnetz

Im Anschluss-Schritt (Power Automate Parse JSON oder Python): das Schema validieren, bei Drift loggen. Siehe [[50.work/power-platform/ai-prompt-json-output]] für Komma/Punkt-Parsing-Fallen.

## Wann nicht

- **Bei vollständig OCR-fähigen Dokumenten** mit Tabellen: Tools wie Adobe Extract, Azure Form Recognizer, Power Automate AI Builder (mit eigenem Modell trainiert) liefern strukturierte JSON-Ausgabe direkt — kein Prompt-Engineering nötig.
- **Bei stets gleichbleibenden Templates:** Trainiere ein AI-Builder-Document-Extraction-Modell auf 5–10 Beispielen → deterministische Felder, kein Prompt-Drift.
- **Wenn die Felder berechnet (nicht extrahiert) werden:** das ist Power-Automate-Logik, nicht LLM-Aufgabe (siehe [[50.work/power-platform/ai-prompt-json-output]]).
- **Bei sehr großen Dokumenten** (>50 Seiten): Vision-Token-Limit + Halluzinationsrisiko. Vorab segmentieren.

## Pattern: Code-Extraktion aus Text

Variante des gleichen Prompts:

> Extrahiere alle [Codes / IDs / Versicherungsnummern / Artikelnummern] aus dem folgenden Text. Gib sie als JSON-Array zurück, ohne Kontext, ohne Duplikate.

Verwendet z.B. in der Conv „Code extraction from text" zur Stapelverarbeitung.

## Verwandt

- [[40.meta/dokumentenanalyse-vorlesung-zusammenfassen]] — verwandtes Pattern für Lerninhalte
- [[40.meta/claude-projekte-und-custom-ai]]
- [[50.work/power-platform/ai-prompt-json-output]] — JSON-Output in Power Automate (Komma-vs-Punkt)
- [[40.meta/_conversation-index]]
