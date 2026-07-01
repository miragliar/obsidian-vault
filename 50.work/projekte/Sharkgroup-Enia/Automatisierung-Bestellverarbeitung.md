---
name: Sharkgroup / enia — Automatisierung Bestellverarbeitung mit PROFFIX-Integration
slug: sharkgroup-enia-automatisierung-bestellverarbeitung
klient: Sharkgroup AG / enia vertriebs gmbh
tags: [sharkgroup, enia, proffix, ai-builder, power-automate, automatisierung, projekt]
status: anfrage
phase: prä-offerte
created: 2026-06-15
ansprechpartner_kunde:
  - Stephanie Stark — Stv. Leitung Verkauf-Innendienst (enia vertriebs gmbh, DE) — stephanie.stark@sharkgroup.swiss
ansprechpartner_extern:
  - Alessandro Castelli — bestehende PROFFIX-Vorarbeit
quellen:
  - "Mail Stark 2026-06-11: evg_Anfrage zu einem ungefähren Kostenvorschlag - Umsetzung Automatisierung Bestellverarbeitung inkl. Proffix-Integration"
  - "Teams-Meeting 2026-06-01 (Kick-off)"
---

# Sharkgroup / enia — Automatisierung Bestellverarbeitung

> **Status (2026-06-15):** Anfrage von Frau Stark eingegangen. Antwort: Vor-Ort-Tag statt formelle Offerte. Realistisches Ziel: 1 Tag End-to-End-PoC + saubere Aufwandschätzung für Rest.

## Anforderung (aus Mail vom 2026-06-11)

1. **PDF-Bestellungen automatisiert auslesen** (später auch Mail-Bodies)
2. **Lieferanten-Artikelnummern erkennen** (Hoegner `ho-…`, bodecor `bo-…`, Werkhaus `wh-…`) und gegen interne `ArtikelNrLAG` aus Tabelle `LAG_Artikel` mappen
3. **Musterbestellungen** (z. B. `LB-202606-13723`): automatisch ein **„M"** vor die Artikelnummer ergänzen
4. **Import in PROFFIX-Auftragsbearbeitung** via bestehender REST-API — Mandant **enia vertriebs gmbh** ggf. noch einzurichten
5. **Rückmeldung-Mail** mit Original-Infos + generierter Auftragsnummer

### Beispiel-Mapping (aus Mail)

| ArtikelNrLAG | Z_ArtikelNr_Hoegner | Z_bodecor_ArtikelNr | Z_werkhaus_ArtikelNr |
|---|---|---|---|
| 34150 160 | ho-052334-150160 | bo-052002-150160 | wh-042002-150160 |
| 34750 500 | NULL | bo-032503-340500 | NULL |

## Tech-Stack — Vorschlag

### Erkennung / Extraktion: AI Builder Prompt (GPT-4o)

- **Pattern aus [[50.work/projekte/Hunnenberg/Prompt-Auftragserstellung-2026-06-09|Hunnenberg]]** — produktiv bewährt
- Variable Layouts pro Lieferant → kein klassisches Document-Processing-Modell, sondern Custom Prompt mit erzwungenem JSON-Output
- Viele kleine Spezialfälle (Präfix-Logik `ho-/bo-/wh-`, Musterbestellungs-„M") lassen sich präzise sprachlich beschreiben
- Microsoft-Empfehlung 2026 für genau dieses Szenario: [AI Builder Prompts](https://learn.microsoft.com/en-us/power-platform/release-plan/2024wave2/ai-builder/extract-information-documents-gpt)

### Mapping: Lookup statt Prompt

- `LAG_Artikel`-Tabelle **nicht in den Prompt** packen (Token-Explosion, Wartbarkeit)
- LLM extrahiert nur: `{ lieferant, externe_artikelnr, menge, musterbestellung_ja_nein }`
- Power Automate macht den Lookup gegen PROFFIX-API oder direkt SQL
- Fallback bei unbekannter ArtNr → Klärungs-Mail an Sachbearbeitung statt fehlerhaftem Auftrag

### Import: PROFFIX REST API

- Doku & Endpoints siehe [[50.work/proffix/proffix-rest-api|PROFFIX Px5 REST API — Übersicht]]
- Workflow: Login → Adresse lookup → Auftrag anlegen → Positionen anhängen → Logout
- Mandant enia vertriebs gmbh: **Klärungsbedarf** — separate Lizenz nötig?
- Vorarbeit Alessandro Castelli abklären

## Architektur-Skizze

```
Mail (PDF-Anhang von Lieferant)
        │
        ▼
Power Automate Trigger
        │
        ▼
AI Prompt (GPT-4o)
  → JSON: { kopf:{…}, positionen:[{lieferant, externe_artnr, menge, muster?}] }
        │
        ▼
Apply to each Position:
  ├─ Lookup interne ArtikelNrLAG (PROFFIX oder Mapping-DB)
  ├─ Wenn muster=true: ArtikelNrLAG = "M" + ArtikelNrLAG
  └─ Wenn nicht gefunden → Sammeln für Klärungsmail
        │
        ▼
PROFFIX REST API
  ├─ POST PRO/Login  (Mandant enia)
  ├─ POST AUF/Auftrag (Kopf)
  ├─ POST AUF/Auftragsposition (n×)
  └─ DELETE PRO/Login
        │
        ▼
Bestätigungsmail an Innendienst:
  - Original-Mail-Infos
  - Anhang (Original-PDF)
  - generierte PROFFIX-Auftragsnummer
  - ggf. Klärungspunkte
```

## Aufwandseinschätzung — qualitativ

| Komponente | Best Case | Worst Case | Risiko-Faktor |
|---|---|---|---|
| AI-Prompt für PDF-Extraktion | 2–3 h | 1–2 Tage | Layout-Varianz zwischen Lieferanten, Edge-Cases |
| Mapping-Lookup-Logik | 1 h | 4 h | wie schnell ist DB-Zugang? |
| PROFFIX-Auftrag-POST (inkl. Mandant-Setup) | wenige h | mehrere Tage | Mandant-Einrichtung enia, Custom-Connector, Test-DB |
| Bestätigungsmail | 1 h | 2 h | trivial |
| End-to-End-Test mit echten Bestellungen | 2 h | 1 Tag | abhängig von Test-Daten-Verfügbarkeit |
| **Mail-Body-Variante (Phase 2)** | später | später | erst nach PDF-Stabilität |

> **Gesamteindruck:** Im besten Fall ein produktiver Tag vor Ort. Realistisch eher 1 Tag PoC + 2–4 Tage Härtung. PROFFIX-Mandanten-Anbindung ist die grösste Unbekannte.

## Standorte Sharkgroup

| Standort | Adresse | Funktion |
|---|---|---|
| Uster (registriert) | Wermatswilerstrasse 8, 8610 Uster | Hauptsitz / Verwaltung |
| Oberhasli (neues HQ) | Rietwiesenstrasse 17, 8156 Oberhasli | Bodenkompetenzzentrum (Logistik, Showroom, Schulungen) |

> Welcher Standort für den Vor-Ort-Termin — vor Mailversand mit Frau Stark klären (vermutlich Uster oder Oberhasli, **nicht** Pratteln).

## Nächste Schritte

- [ ] Mail an Frau Stark mit Vor-Ort-Vorschlag (keine Fix-Offerte)
- [ ] Abstimmung mit Alessandro Castelli (PROFFIX-Vorarbeit, Mandant enia)
- [ ] Terminvorschläge ein-/zweiwöchig
- [ ] Vor Termin: Test-Bestellungen aus Anhang in lokaler Sandbox durchspielen
- [ ] Custom Connector für PROFFIX aufsetzen (falls noch nicht vorhanden)

## Verwandt

- [[50.work/projekte/Sharkgroup-Enia/Planner-Aufgaben-Automatisierung|Sharkgroup / enia — Mail-zu-Aufgabe mit Planner (2. Thema Termin 14.07.)]]
- [[50.work/proffix/proffix-rest-api|PROFFIX Px5 REST API — Übersicht & Integrationsleitfaden]]
- [[50.work/projekte/Hunnenberg/Prompt-Auftragserstellung-2026-06-09|Hunnenberg — analoges Pattern]]
- [[50.work/25_People/Alessandro-Castelli|Alessandro Castelli]]
- [[50.work/26_Firmen/Castelli-Solutions|Castelli Solutions]]
- [[40.meta/prompt-strukturierte-extraktion|Pattern: Strukturierte JSON-Extraktion]]
