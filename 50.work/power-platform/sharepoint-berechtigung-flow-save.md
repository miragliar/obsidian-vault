---
source: chat-context 2026-06-04
imported: 2026-06-04
type: pattern
tags: [power-platform, power-automate, sharepoint, berechtigung, flow-save, troubleshooting]
related_projects: ["[[50.work/projekte/Regieapp-Neubau-MVM|Regie-Rapport-App MVM]]"]
trigger_case: "Rapport 26-1039 / Christoph Räber (MVM AG, 2026-06-03)"
---

# SharePoint-Berechtigung als Flow-Save-Voraussetzung

Ein Power-Automate-Flow, der ein erzeugtes Dokument (z.B. PDF-Rapport, generierte Rechnung) auf SharePoint ablegt **und danach** via Mail versendet, schlägt **stillschweigend für End-User ohne SharePoint-Schreibrechte** auf den Ziel-Speicherort fehl — selbst wenn der Flow als Service-Account / mit höheren Rechten läuft.

## Problem

Beim Trigger durch einen End-User (z.B. „Rapport beenden" in Power Apps) übernimmt der Flow oft den **Aufruferkontext** für den **SharePoint-Save-Step** (typisch bei `Datei erstellen` in SharePoint, wenn der Connector auf die User-Connection läuft). Wenn der User dort keine Schreibberechtigung hat:

1. Flow rechnet alles korrekt durch (Quellen lesen, PDF generieren etc.).
2. Save-Step schlägt fehl → kein Datei-Pfad vorhanden.
3. Folgender Mail-Send-Step kann das Attachment nicht laden → schlägt ebenfalls fehl oder fällt auf einen Default-Empfänger (manchmal der Auslöser selbst) zurück.
4. **Symptom für den End-User:** Bestätigungs-Toast sagt „Rapport an dich selbst gesendet" — irreführend, weil die echte Ursache der Save-Fail ist.

## Konkret beobachtet (Trigger-Case)

**Rapport Nr. 26-1039 / [[50.work/25_People/Christoph-Räber|Christoph Räber]] (MVM AG, 03.06.2026):**

- Christoph (Hybrid-Mitarbeiter, neu im System) beendete einen Rapport in der PDF-Ansicht.
- Bestätigung: „Rapport an ihn selbst gesendet".
- Tatsächliche Ursache: Keine SharePoint-Berechtigung auf den Speicherort, wohin der Flow das PDF speichern wollte.
- **Fix:** Berechtigung für Christoph nachgetragen → Rapport lief sauber durch (Save → Mail an Kunde).

## Lösung

### Beim User-Onboarding mitführen

In die User-Onboarding-Checkliste für jede Power-App, die Dokumente auf SharePoint generiert, **explizit** aufnehmen:

- [ ] Aufnahme in fachliche Sicherheitsgruppe (z.B. „Power Apps PL")
- [ ] **SharePoint-Schreibrechte auf den Save-Speicherort** des relevanten Flows
- [ ] Mandantenspezifische Berechtigungen (Standort, Baustellen-Liste, etc.)

### Im Flow defensiv prüfen

Wenn machbar: vor dem SharePoint-Save-Step einen **Permission-Check** einbauen (z.B. `Get folder metadata` mit Try/Catch). Bei Fehler:

- Klare Fehlermeldung an den User (statt irreführende Default-Bestätigung)
- Optional: Notification an Admin / Power-Platform-Lead

### Connector-Connection auf Service-Account legen (Trade-off)

Alternativ: SharePoint-Connector im Flow auf eine **Service-Account-Connection** zwingen, statt User-Connection. Vorteil: User-Berechtigung wird umgangen. Nachteil: weniger Audit-Trail wer was geschrieben hat — abwägen, ob sinnvoll.

## Diagnose-Hinweise

Wenn Bug-Reports kommen mit Muster:
- „Hat funktioniert, aber Empfang ist falsch"
- „Mail kam bei mir, nicht beim Kunden"
- Neue User / kürzlich onboarded
- Reproduzierbar bei genau einer Person, aber nicht bei anderen

→ **Erstes Verdachtsfeld: SharePoint-Save-Berechtigung.** Flow-Run-History des betreffenden Triggers anschauen, Save-Step-Output prüfen.

## Wann nicht relevant

- Flows die nur lesen (keine Save-Aktion)
- Flows ohne SharePoint (z.B. nur Dataverse + Mail)
- Flows die strikt unter Service-Account laufen (kein User-Kontext)

## Verwandt

- [[50.work/projekte/Regieapp-Neubau-MVM|Regie-Rapport-App MVM]] — Trigger-Case
- [[50.work/projekte/Magazin-App-MVM|Magazin-App MVM]] — analoges Pattern (Materialkosten-Importdatei, Filliger)
- [[50.work/power-platform/_README|Power Platform Pattern-Bibliothek]]
