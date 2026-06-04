---
name: Magazin-App MVM
slug: Magazin-App-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Wartung + laufende Erweiterung
zeitraum: produktiv (Bestand) — Erweiterungen Juni 2026
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, magazin, materialbezug, dataverse, power-automate, brz, filliger]
type: projekt-hub
source: chat-context 2026-06-04 (Remo Pfister, Nicole Scherrer, Filliger/Kanita)
created: 2026-06-04
---

# Magazin-App MVM

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]] · auch [[50.work/26_Firmen/Filliger-Partner|Filliger & Partner AG]] (Kreditoren-Schnittstelle)
**Status:** Wartung + laufende Erweiterung
**Mailbox:** `magazin@mvm-ag.ch`

## Worum geht es

Power-Apps-/Dataverse-Lösung für die Verwaltung von **Materialbezügen, KANBAN-Liste und Rechnungen** der MVM AG. Magaziner erfasst Materialbezüge, App generiert Rechnungen an Kunden, Daten werden in BRZ und an die Buchhaltung bei [[50.work/26_Firmen/Filliger-Partner|Filliger & Partner AG]] übertragen.

## Beteiligte

- [[50.work/25_People/Remo-Pfister|Remo Pfister]] · Mitglied GL, Owner Magazin-Prozess
- [[50.work/25_People/Nicole-Scherrer|Nicole Scherrer]] · Sachbearbeiterin Rechnungswesen MVM — Reviewerin Rechnungs-Flow
- Kanita ([[50.work/26_Firmen/Filliger-Partner|Filliger & Partner AG]]) · Sachbearbeiterin Kreditoren — Materialkosten-Import-Verarbeitung

## Architektur (rekonstruiert)

```
Magaziner (PowerApp)         Dataverse                BRZ / Filliger
─────────────                ─────────                ─────────────
Materialbezug erfassen ────► tbl_Materialbezug ──┬──► KANBAN-Liste (Anzeige)
                                                 │
                                                 └──► Rechnungs-Generator
                                                          │
                                                          ▼
                                                 PDF-Rechnung
                                                          │
                                                          ▼
                                                 Materialkosten-Import-Datei
                                                          │
                                                          ▼
                                                 BRZ / Filliger&Partner (Kreditoren)
```

## Aktuelle Offene Punkte (Stand 2026-06-04)

### Preislogik: EP vs. Verkaufspreis intern
- **Status quo:** Rechnung verwendet **Einstandspreis (EP)** aus Materialkatalog.
- **Plan (Remo, 2026-06-02):** In KANBAN-Liste neue Spalte „Verkaufspreis intern" ergänzen (z.B. EP + Aufschlag).
- **Umbau-Auftrag (Raoul):** Sobald Remo die Spalte angelegt hat → Rechnungs-Logik umstellen auf neue Spalte. Pauschale Aufschlag-% oder Wert pro Artikel zu klären.
- **ToDo:** ⏳ Warten auf Remo, dann Umbau.

### KST-Spalte für Magaziner (Nicole Scherrer, 2026-06-02)
- **Anforderung:** Magaziner soll bei jedem Materialbezug die **Kostenstelle (KST)** mitgeben.
- **Umsetzung:** Dataverse-Spalte `KST` zur Materialbezug-Tabelle hinzufügen + im PowerApps-Form sichtbar machen + Pflichtfeld.
- **ToDo:** ⏳ Spalte + UI-Änderung, dann Test mit Nicole.

### Filter „505 ignorieren" (Nicole Scherrer)
- Position/Konto „505" soll in der Rechnungs-/Materialbezug-Logik nicht mehr berücksichtigt werden (vermutlich Konto-Bewegung die unschön durchschlägt).
- **ToDo:** ⏳ Filter im Flow / im Rechnungs-Generator setzen.

### IBAN-Korrektur (Nicole Scherrer)
- Korrekte IBAN: `CH28 0077 8010 7005 1110`
- **ToDo:** ⏳ Master-Eintrag (Firma/Mandant) korrigieren.

### Materialkosten-Importdatei Bug (Filliger Partner / Kanita, 2026-06-03)
- **Symptom:** „Datei von gestern scheinbar fehlerhaft" — Materialbezüge müssen manuell erfasst werden.
- **Möglichkeiten:**
  - Flow-Trigger nicht angesprungen (Auslöser-Bedingung verfehlt?)
  - Datei generiert aber inhaltlich corrupt (Zeichensatz, Spalten-Layout, leeres Feld)
- **ToDo:** ⏳ Flow-Run-History von 2026-06-02/03 prüfen, Fehler reproduzieren, Fix einspielen. Manuell-Fallback unterstützen bis Fix steht. Kanita ist Fr. abwesend → Rückmeldung Do.

## Verwandte Pattern-Notizen

- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung für File-Save Flows]]
- [[50.work/power-platform/power-automate-string-expressions|Power Automate String-Expressions]] (für IBAN-Validierung)

## Verwandt

- [[_Index|Projekt-Index]]
- [[Regieapp-Neubau-MVM|Regie-Rapport-App]] — verwandt (gleiches Dataverse-Env, gleiche User)
- [[Mahnprozess-MVM|Mahnprozess MVM]] — Rechnungs-Ausgang → Mahnstrecke
- [[50.work/26_Firmen/MVM-AG|MVM AG]]
- [[50.work/26_Firmen/Filliger-Partner|Filliger & Partner AG]] — Kreditoren-Empfänger
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04]] — ToDos 9 + 10
