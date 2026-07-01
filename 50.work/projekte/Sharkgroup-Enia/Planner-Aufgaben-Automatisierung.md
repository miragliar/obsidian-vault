---
name: Sharkgroup / enia — Mail-zu-Aufgabe-Automatisierung mit Microsoft Planner & Power Automate
slug: sharkgroup-enia-planner-aufgaben-automatisierung
klient: Sharkgroup AG / enia vertriebs gmbh
tags: [sharkgroup, enia, planner, power-automate, automatisierung, projekt, mail-triage]
status: anfrage
phase: prä-termin
created: 2026-07-01
termin: 2026-07-14
ansprechpartner_kunde:
  - Stephanie Stark — Stv. Leitung Verkauf-Innendienst — stephanie.stark@sharkgroup.swiss
  - Rahel Bachmann — Rückfragen telefonisch +41 43 497 86 84 — rahel.bachmann@sharkgroup.swiss
quellen:
  - "Mail Stark 2026-06-30: Anfrage TO DO's Microsoft Planner / Power Automate"
---

# Sharkgroup / enia — Mail-zu-Aufgabe mit Planner & Power Automate

> **Status (2026-07-01):** Zweites Thema für den Vor-Ort-Termin am **14.07.2026**, zusätzlich zur [[50.work/projekte/Sharkgroup-Enia/Automatisierung-Bestellverarbeitung|Bestellverarbeitung]]. Frau Stark hat den Ansatz vorab geschildert, damit wir den Termin nicht sprengen. Antwort-Entwurf an sie liegt in Outlook.

## Worum es geht

Sharkgroup will die **Mail-Triage im Innendienst** entlasten: Eingehende Mails an ein Sammelpostfach (z. B. `info@sharkgroup.swiss`) sollen **automatisch als Aufgabe (Task) im Microsoft Planner** landen — kein manuelles Erfassen und Zuweisen mehr. Outlook dient nur noch als **Eingangskanal**, die eigentliche Bearbeitung passiert komplett im Planner-Board.

**Gewünschte Board-Struktur (Status):**

| Status | Bedeutung |
|---|---|
| **Eingang** | Alle neuen Mails, noch nicht zugewiesen |
| **Zuweisen / Klärung** | Unklare Zuständigkeit, interne Rückfrage |
| **In Bearbeitung** | Task zugewiesen und aktiv in Arbeit |
| **Warten auf Kunde / Lieferant** | Antwort steht aus |
| **Erledigt** | Abgeschlossen und dokumentiert |

Voraussetzung ist erfüllt: Der Power-BI-Admin hat **bereits Zugriff auf das Postfach**.

## Wie das technisch funktioniert (in einfachen Worten)

Planner ist als **fertiger Connector direkt in Power Automate integriert** — es braucht keine Programmierung, sondern das Zusammenstecken vorhandener Bausteine. Der Ablauf ist Standard:

```
Neue Mail im Sammelpostfach (info@sharkgroup.swiss)
        │  Trigger: "Wenn eine neue E-Mail eintrifft" (Office 365 Outlook)
        ▼
Power Automate
        │  ggf. Filter (nur bestimmte Absender / kein Spam / keine Antworten)
        ▼
Planner-Aktion "Aufgabe erstellen"
   → Titel  = Betreff der Mail
   → Bucket = "Eingang"
   → Details/Beschreibung = Absender, Datum, Kurztext + Link zur Original-Mail
        │
        ▼
Task erscheint im Board unter "Eingang" → Innendienst arbeitet weiter
```

Die fünf Status setzen wir im Planner als **Buckets** (die Spalten des Boards) um. Ein neuer Task landet automatisch in „Eingang"; das Weiterschieben (Zuweisen → In Bearbeitung → …) macht der Innendienst per Drag & Drop von Hand — genau so, wie es gewünscht ist.

## Worauf wir bei der Umsetzung achten (die „Eigenheiten" des Connectors)

> Kurz für den Termin: Der Ansatz ist gut machbar. Es gibt beim Planner-Connector ein paar bekannte Stolpersteine, die aber alle lösbar sind — **keine Blocker**, nur „gut zu wissen".

- **Vieles läuft über technische IDs, nicht über Namen.** Plan, Bucket und die zuzuweisende Person werden im Flow über eine ID (GUID) angesprochen, nicht über ihren Klartext-Namen. In der Praxis wählt man sie im Flow einmal aus einer Liste aus — man muss die IDs also nicht selbst kennen, aber im Hintergrund sind es IDs. Deshalb kann das Umbenennen einer Person / eines Buckets im Flow etwas „ruppig" wirken.
- **Feldbezeichnungen des Connectors können sich ändern.** Microsoft hat Felder in der Vergangenheit umbenannt; das ist erfahrungsgemäss kosmetisch und beim Aufsetzen schnell erledigt.
- **Beschreibung/Notizen kommen über einen zweiten Schritt** („Aufgabendetails aktualisieren") — die eigentliche Aufgabe wird zuerst angelegt, die Details danach angehängt.
- **Anhänge:** Planner speichert keine Dateien direkt in der Aufgabe, sondern verlinkt sie (über die SharePoint-/Gruppen-Ablage). Original-Mail bzw. PDF verlinken wir also, statt sie „hineinzukopieren".
- **Doppelte Tasks vermeiden:** Antworten im selben Mail-Thread oder Automatik-Mails sollten keinen zweiten Task erzeugen → sauberer Trigger-Filter.
- **Betriebssicheres Konto:** Der Flow und der Plan sollten idealerweise einem **funktionalen/geteilten Konto** gehören, nicht einer Einzelperson — sonst bricht die Automation, wenn jemand das Unternehmen verlässt.

## Wie wir es planen umzusetzen

1. **Plan & Board vorbereiten** — einen Planner-Plan anlegen, die fünf Buckets als Status setzen.
2. **Sammelpostfach klären** — welches Postfach genau (`info@…`?), Zugriff/Berechtigung bestätigen (Power-BI-Admin hat bereits Zugriff).
3. **Flow bauen** — Trigger „neue Mail" → Filter → „Aufgabe erstellen" in Bucket „Eingang" → Details anhängen (Absender, Link zur Mail).
4. **Zuweisungs-Logik besprechen** — soll die Zuweisung von Hand erfolgen (einfach, empfohlen für Start) oder teils automatisch nach Absender/Stichwort?
5. **Testlauf** mit echten Mails, dann Feinschliff (Filter, Duplikate, Beschreibungstext).

## Offene Punkte / für den Termin klären

- [ ] Genaues Sammelpostfach + Berechtigungen bestätigen
- [ ] Wer soll Tasks zuweisen — manuell oder teilautomatisch (Regeln nach Absender/Betreff)?
- [ ] Sollen Antworten/Weiterleitungen im Thread einen neuen Task erzeugen oder nicht?
- [ ] Besitzer-Konto für Flow & Plan (funktionales Konto empfohlen)
- [ ] Umgang mit Anhängen (Verlinkung vs. reiner Verweis auf die Mail)
- [ ] Reihenfolge am 14.07.: erst Bestellverarbeitung, dieses Thema als „nice to have" hintenan

## Verwandt

- [[50.work/projekte/Sharkgroup-Enia/Automatisierung-Bestellverarbeitung|Sharkgroup / enia — Automatisierung Bestellverarbeitung (Hauptthema Termin 14.07.)]]
