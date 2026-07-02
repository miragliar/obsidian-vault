---
datum: 2026-07-01
kunde: Koster AG
projekt: Subunternehmer – Eingehende E-Mail verarbeiten
typ: arbeitsbeschrieb
tags: [koster, arbeitsbeschrieb, subunternehmer]
---

# Arbeitsbeschrieb – Koster AG, 2026-07-01

## Thema
Automatische Verarbeitung eingehender Subunternehmer-Dokumente (E-Mail → Ablage/Zuordnung).

## Ausgangslage
Mehrere Dokumente wurden nicht korrekt verarbeitet. Ursache: Fehlte der Firmenname im Dokument, konnte der Subunternehmer nicht zugeordnet werden und die Verarbeitung brach ab.

## Durchgeführte Arbeiten
- Fehlerursache analysiert und den betroffenen Fall von heute im System bestätigt.
- Neue, zuverlässigere Erkennung des Subunternehmers eingebaut: Statt nur über den Firmennamen wird die Zuordnung jetzt zusätzlich über die **Absender-E-Mail und deren Domain** gemacht.
- Aufbau des Ablaufs verschlankt und aufgeräumt, damit er wieder stabil gespeichert und veröffentlicht werden kann.
- Änderungen live getestet: Der richtige Subunternehmer wird nun korrekt erkannt.

## Ergebnis
- Erkennung des Subunternehmers funktioniert und ist deutlich robuster.
- Verbleibender Randfall (Subunternehmer ohne offenen Auftrag) wird bewusst als Fehler gemeldet – so gewünscht.

## Nächster Schritt
- Vollständiger Testdurchlauf mit einem Subunternehmer, der einen offenen Auftrag hat.
