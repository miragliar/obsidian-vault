---
name: Optiwork AG
slug: Optiwork-AG
domain: optiwork.ch
typ: lieferant
branche: ERP / Branchen-Software Bauhandwerk (Domus, Aestico)
web: https://www.optiwork.ch
tags: [miraglia, lieferant, optiwork, domus, aestico, mvm-ag]
status: aktiv
created: 2026-06-16
source: aestico-doku + chat-context 2026-06-16
---

# Optiwork AG

**ERP / Branchen-Software Bauhandwerk — Hersteller von Domus und Aestico**

## Profil

<!-- firmenprofil -->
**Web:** https://www.optiwork.ch
**Was sie tun:** Optiwork AG ist Anbieter von Branchen-Software für das Bauhandwerk in der Schweiz. Zwei zentrale Produkte:
- **Domus** — ERP-System (Auftrag, Faktura, Lohn, Kreditoren etc.), bei MVM AG produktiv
- **Aestico** — mobile App / Schnittstelle für Offert- und Rechnungspositionen (Tablet-Erfassung auf der Baustelle, JSON-Export ins ERP)
<!-- /firmenprofil -->

## Bezug zu MVM-AG-Projekten

| Was | Status (Stand 16.06.2026) |
|---|---|
| Domus-Lizenz MVM AG | aktiv (Standard-Branchen-ERP MVM) |
| Aestico-Schnittstelle MVM AG | Nutzung lizenzrechtlich **erlaubt** ab 15.06.2026 (Ziffer 6 der Lizenzvereinbarung Optiwork ↔ MVM, siehe Projekt-Notiz) |
| Domus-Revision 28 | live ab 16.06.2026 — öffnet Aestico-Schnittstelle für externe Eigenentwicklung |

## Produkt: Aestico

- **Format:** JSON-Datei (`.aest`-Endung), JSON-Schema Draft-07, Version 2 (Stand 2023-12-04)
- **Doku:** `/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/MVM/Aestico/aestico_v2_doc/`
- **Technische Spec im Vault:** [[50.work/projekte/MVM-AG/aestico-schnittstelle/aestico-v2-spec|Aestico v2 — JSON-Spec]]
- **Richtung:** Aestico exportiert Quote → empfangendes System (Domus) importiert
- **Transport zum ERP:** in Aestico-Doku **nicht** spezifiziert — siehe offene Punkte in der Projekt-Notiz

## Lizenz-Bedingungen Aestico (Auszug Ziffer 6, signiert 15.06.2026)

> *„Optiwork AG erlaubt MVM AG die Nutzung der Schnittstelle Aestico zum Generieren von Offert- und Rechnungspositionen aus der Eigenentwicklung von MVM AG, solange Aestico die Nutzung erlaubt."*

- ✅ Eigenentwicklung MVM (= Regie-App auf Power Platform) darf Aestico-Schnittstelle nutzen
- ⚠️ Bedingung: *„solange Aestico die Nutzung erlaubt"* — Vendor-Lock-In-Risiko, in Risiken-Sektion mitführen

## Personen / Kontakt

- Bislang **keine direkt benannte Optiwork-Kontaktperson** dokumentiert.
- Eskalations-/Doku-Pfad bei Aestico-Spec-Fragen vermutlich über **[[Turnkey|Turnkey AG]]** (Domus-Anbieter-Seite, [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]]) → Optiwork.
- **TODO:** Direkten Optiwork-Kontakt von [[50.work/25_People/Remo-Pfister|Remo Pfister]] erfragen, sobald für Phase-1-Klärung (Aestico-Doku, Transport-Mechanismus) gebraucht.

## Persönliche Notizen

_Manuelle Notizen zur Firma (Account-Manager, Lizenz-Erneuerungen, Support-Stand, …) kommen hier hin._

## Projekte (Berührungspunkte)

- [[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import|Regie-Rapport-App → Aestico-Schnittstelle / Domus-Import]] — Hauptprojekt, in dem Aestico konsumiert wird

## Verwandt

- [[50.work/26_Firmen/_Index|Firmen-Index]]
- [[50.work/26_Firmen/Turnkey|Turnkey AG]] — Domus-Anbieter
- [[50.work/26_Firmen/MVM-AG|MVM AG]] — Lizenznehmer
- [[50.work/projekte/MVM-AG/aestico-schnittstelle/aestico-v2-spec|Aestico v2 — JSON-Spec]]
