---
name: Mahnprozess MVM
slug: Mahnprozess-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Live
zeitraum: produktiv ab Juni 2026
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, mahnprozess, brz, teams, hybrid-mitarbeiter]
type: projekt-hub
source: chat-context 2026-06-04 (Remo Pfister mail 2026-06-03)
created: 2026-06-04
---

# Mahnprozess MVM

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]]
**Status:** Live (aktiv ab Juni 2026)

## Worum geht es

Workflow zur Steuerung von **Mahnungs-Entscheidungen** für MVM-Rechnungen, insbesondere für **Hybrid-Mitarbeiter** (Mitarbeiter die selbständig Aufträge annehmen und Rechnungen an Kunden ausstellen — siehe [[50.work/25_People/Christoph-Räber|Christoph Räber]]).

## Workflow

```
BRZ                                Mail-Benachrichtigung           Teams
───                                ────────────────────           ─────
Mahnungs-Entscheidung ────────►   Email an Mitarbeiter ────────► Teams-Registerkarte
notwendig                          (über ihre Mailadresse)         (PL/Mitarbeiter
                                                                    berechtigt)
                                                                          │
                                                                          ▼
                                                                 Mitarbeiter
                                                                 entscheidet
                                                                 (mahnen / nicht)
```

## Beteiligte (Hybrid-Mitarbeiter im Prozess, Stand 06.2026)

- [[50.work/25_People/Christoph-Räber|Christoph Räber]] · Kundendienst Fassade
- [[50.work/25_People/Richy-Schön|Richy Schön]] · PL
- [[50.work/25_People/Jan-Schwitter|Jan Schwitter]] · PL

## Architektur-Entscheidungen

### Teams-Registerkarte als zentrale UI
- Mahnungs-Entscheidungen werden in einer **Teams-Registerkarte** dargestellt — nicht als Standalone-Power-App.
- Vorteil: Berechtigung über Teams-Mitgliedschaft, native Notification, mobile-fähig.
- Self-Service-Pattern: **Remo kann die Mitgliederliste der Teams-Registerkarte selbständig pflegen** — kein Miraglia-Eingriff nötig für neue Hybrid-Mitarbeiter.

### Trigger: BRZ-Mail an Mitarbeiter
- Quelle der Mahnungs-Entscheidung ist BRZ (DOMUS).
- BRZ schickt Mail an die Mitarbeiter-Adresse → Mitarbeiter sieht die Mahnstrecke in Teams.

## Self-Service-Spielregeln (für Remo)

Für zukünftige Mitarbeiter, die in den Mahnprozess aufgenommen werden sollen:

1. Mitarbeiter zur **Teams-Registerkarte** hinzufügen (mehr braucht es typischerweise nicht).
2. Sicherstellen, dass die BRZ-Mailadresse korrekt hinterlegt ist.
3. Bei Sonderfällen (z.B. neue Hybrid-Rolle) → Rückfrage Raoul.

## Verwandte Pattern-Notizen

- (potenziell) [[50.work/power-platform/_README|Power Platform Patterns]]

## Verwandt

- [[_Index|Projekt-Index]]
- [[Magazin-App-MVM|Magazin-App MVM]] — Rechnungs-Ausgang
- [[Regieapp-Neubau-MVM|Regie-Rapport-App]] — auch für Hybrid-Mitarbeiter (Christoph Räber)
- [[50.work/26_Firmen/MVM-AG|MVM AG]]
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04]] — ToDo #2 (erledigt)
