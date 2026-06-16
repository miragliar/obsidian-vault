---
name: Arbeitsbeschrieb — Aestico-Schnittstelle
slug: arbeitsbeschrieb
parent_project: "[[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import|Regieapp-Aestico-Domus-Import]]"
klient: MVM AG
typ: arbeitsbeschrieb
status: draft
stand: 2026-06-16
tags: [miraglia, mvm-ag, aestico, regie-app, arbeitsbeschrieb]
created: 2026-06-16
---

# Arbeitsbeschrieb — Aestico-Schnittstelle (Regie-Rapport → Domus)

**Stand:** 16.06.2026

## Ziel

Regie-Rapporte aus der Regie-App per Knopfdruck als Rechnung im **Domus** erzeugen — als Einzelrechnung pro Rapport oder als Sammelrechnung mehrerer Rapporte. Schluss mit manueller Übertragung der Rapportdaten ins Domus.

## Was Aestico macht

Aestico ist die offizielle Schnittstelle des Domus-Herstellers ([[50.work/26_Firmen/Optiwork-AG|Optiwork AG]]). Sie nimmt eine Datei mit Rechnungspositionen entgegen und legt im Domus den entsprechenden Beleg an.

## Was bereits gebaut ist

- Die Regie-App erzeugt aus den eingegebenen Rapport-Daten automatisch eine Datei im Aestico-Format.
- Funktioniert sowohl für eine einzelne Rechnung als auch für eine Sammelrechnung über mehrere Rapporte.
- Die Datei enthält pro Rapport einen eigenen Block mit allen Stunden- und Materialpositionen, am Schluss die MwSt.
- Die Datei ist gegen die offiziellen Vorgaben von Optiwork geprüft und schema-konform.

## Was noch zu klären ist

1. **Übergabeweg zu Domus** — wie kommt die fertige Datei zum Domus-Server? Klärung mit [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]] ([[50.work/26_Firmen/Turnkey|Turnkey AG]]) und [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl]] ([[50.work/26_Firmen/MVM-AG|MVM-IT]]).
2. **Kunden-Mapping** — die Datei enthält bisher nur den Absender (MVM AG). Der Empfänger pro Baustelle muss aus den Domus-Stammdaten gezogen werden.
3. **Test-Mandant** — bei Turnkey eine Test-Umgebung im Domus anfordern, um einen ersten kompletten Durchlauf zu fahren.
4. **MwSt-Behandlung** — abklären, ob Domus die MwSt selbst rechnet oder den Wert aus der Datei übernimmt.

## Zeitplan

- Punkte 1–4 klären: Ende Juni / Anfang Juli
- Erster Testlauf im Domus-Mandant: Juli
- Pilotierung mit 1–2 Projektleitern: August / September
- Statusmeldung an [[50.work/25_People/Remo-Pfister|Remo Pfister]]: 30.09.2026
- Go-Live: 31.10.2026

## Beteiligte

| Rolle | Person / Firma |
|---|---|
| Auftraggeber | [[50.work/25_People/Remo-Pfister|Remo Pfister]] ([[50.work/26_Firmen/MVM-AG|MVM AG]], GL) |
| Schnittstellen-Hersteller | [[50.work/26_Firmen/Optiwork-AG|Optiwork AG]] (Aestico + Domus) |
| Domus-Anbieter | [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]] ([[50.work/26_Firmen/Turnkey|Turnkey AG]]) |
| MVM-IT / Infrastruktur | [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl]] |
| Power-Platform-Partner | [[50.work/25_People/Alessandro-Castelli|Alessandro Castelli]] ([[50.work/26_Firmen/Castelli-Solutions|Castelli Solutions]]) |
| Umsetzung | [[50.work/25_People/Giovanni-Miraglia|Giovanni Miraglia]] + Raoul ([[50.work/26_Firmen/Miraglia-Business-Intelligence|Miraglia BI]]) |

## Verwandt

- [[Regieapp-Aestico-Domus-Import|Projekt-Hub Regieapp-Aestico-Domus-Import]]
- [[aestico-v2-spec|Aestico v2 — technische Spec]]
- [[flow-04-aestico-json-anleitung|Flow-04 — Schritt-für-Schritt-Umsetzung]]
