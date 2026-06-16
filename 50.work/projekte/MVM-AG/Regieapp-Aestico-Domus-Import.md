---
name: Regie-Rapport-App — Aestico-Schnittstelle / Automatisierte Rechnungserstellung Domus
slug: Regieapp-Aestico-Domus-Import
parent_project: "[[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]]"
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Setup / Roadmap
zeitraum: Juni 2026 — Oktober 2026
zieldatum: 2026-10-31
meilenstein: 2026-09-30
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, regie-app, domus, aestico, automatisierung, rechnung]
type: projekt-sub-hub
created: 2026-06-15
updated: 2026-06-16
last_change: "2026-06-16: Aestico-v2-Format aus Optiwork-Doku extrahiert — JSON-Datei-Schnittstelle (keine API/CSV). Spec als [[aestico-schnittstelle/aestico-v2-spec]] abgelegt. Personen-/Firmen-Notizen Optiwork, Turnkey, Dominik Hüsser, Stefan Zumbühl angelegt."
---

# Regie-Rapport-App → Automatisierte Rechnungserstellung im Domus (Aestico-Schnittstelle)

**Eltern-Projekt:** [[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]]
**Auftrag:** [[50.work/25_People/Remo-Pfister|Remo Pfister]], Mail 2026-06-10 09:21
**Status:** Setup-Phase — Hub-Anlage, Mapping-Recherche
**Zieldatum:** 31.10.2026 (vollautomatisierte Rechnungserstellung)
**Meilenstein:** 30.09.2026 (Status-Update an Remo)

## Lizenzrechtliche Grundlage — Optiwork ↔ MVM AG (signiert, 15.06.2026)

> **Status-Update 2026-06-15:** Remo hat Giovanni eine signierte Zusatzklausel weitergeleitet (Mail *„WG: Gewährung Schnittstelle Aestico"*, 2026-06-15 11:48). Giovannis Auftrag an mich: dokumentieren und ablegen.

**Unterzeichnete Klausel — Ziffer 6 „Besondere Nutzungen der Lizenzpakete":**

> *„Optiwork AG erlaubt MVM AG die Nutzung der Schnittstelle Aestico zum Generieren von Offert- und Rechnungspositionen aus der Eigenentwicklung von MVM AG, solange Aestico die Nutzung erlaubt."*
>
> *„Der digitale Lohnabrechnungsversand ist gemäss Lizenzübersicht Teil des Lizenzpakets Lohn und kann entsprechend ohne Lizenzkostenfolge durch MVM AG genutzt werden."*

![[50.work/projekte/MVM-AG/aestico-schnittstelle/2026-06-15-lizenzklausel-ziffer6-optiwork-mvm.png]]

**Bedeutung für unser Projekt:**

| Was | Folge |
|---|---|
| ✅ Lizenz-Hürde weg | Wir dürfen die Aestico-Schnittstelle aus der Regie-App heraus nutzen, um Offert-/Rechnungspositionen zu erzeugen. „Eigenentwicklung von MVM AG" deckt unsere Power-Platform-Lösung explizit ab. |
| ⚠️ Bedingung | *„solange Aestico die Nutzung erlaubt"* — das Nutzungsrecht hängt von Aestico-Seite ab. Falls Aestico die Schnittstelle technisch oder vertraglich schliesst, fällt unser Mechanismus. Risiko nach Phase 4 mitführen (Vendor-Lock-In). |
| 🎁 Bonus / separater Lead | Lohnabrechnungs-Versand digital → **ohne Zusatzkosten** im Paket *Lohn* enthalten. Nicht Teil dieses Projekts, aber Hinweis an Giovanni / Remo wert (potenziell eigener Mini-Use-Case). |
| 📌 Vertragspartner | **Optiwork AG** ist Lizenzgeberin von Aestico. Sollte als Stakeholder/Eskalationspfad in der Phase-1-Klärung mit auftauchen (siehe Frage 3 unten — wer macht die Schnittstelle technisch auf). |

**Offene Folge-Punkte aus der Klausel:**
- [ ] Vollständige Lizenzvereinbarung Optiwork ↔ MVM beschaffen (nur Ziffer 6 ist sichtbar — Kontext und Geltungsbereich der weiteren Ziffern checken)
- [ ] Klären, ob die „Erlaubnis von Aestico-Seite" formell schon vorliegt oder noch eingeholt werden muss (Optiwork hat zugestimmt; Aestico-Produkt-Eigentümer = Optiwork? → vermutlich ja, aber sauber dokumentieren)
- [ ] Optiwork-Kontakt von Remo erfragen (für technische Doku-/API-Spec-Anfragen)

## Auftrag (wörtlich aus Remos Mail 10.06.2026)

> *„Werte Herren — um in der Projektleitung betreffend Rechnungsstellung mehr Effizienz zu erhalten, sollen künftig die digital erstellten Regierapporte vollautomatisiert — Auslösung durch den Projektleiter — als einzelne oder als Sammel-Rechnung im Domus erstellt werden. Die Grundlagen / Basisdaten für dieses Vorhaben sind meines Erachtens vorhanden. Ab der Domus-Revision 28, ab 16.06.2026, werden wir auch die Aestico-Schnittstelle offen haben. Bringt die Regie-Rapportdaten in das gewünschte Import-Format und lasst den Roboter arbeiten."*
>
> *„Ziel: bis 31.10.2026 vollautomatisierte Rechnungsstellung von Regierapporten. Einzelrechnung pro Regierapport oder Sammelrechnung mehrerer Regierapporte. Manuell angestossen durch den jeweiligen Projektleiter."*
>
> *„Gerne hätte ich per 30.09.2026 ein Meilenstein-Update, wie weit wir sind, und ob das Zieldatum eingehalten werden kann."*

**Adressat:** *„Werte Herren"* — vermutlich Raoul + Giovanni + Mike Kipfer (TBC). Empfänger-Verteiler aus Originalmail nochmal prüfen, bevor Antwort raus geht.

## Zielbild

Ein **PL** klickt in der Regie-App einen Button → fertige Rechnung erscheint im **Domus** zur Freigabe/Versand. Keine manuelle Dateneingabe mehr. Zwei Modi:

1. **Einzelrechnung:** pro Regierapport
2. **Sammelrechnung:** Auswahl mehrerer Regierapporte → eine Rechnung

In beiden Fällen: **manuelle Auslösung durch den PL** (kein Auto-Trigger), Daten gehen über die **Aestico-Schnittstelle** in Domus rein.

## Voraussetzungen / Abhängigkeiten

| Stand | Voraussetzung |
|---|---|
| 🟢 Vorhanden | Regierapporte digital in Dataverse (`Regiekopf` + Detail-Tabellen) |
| 🟢 Vorhanden | Power Automate Stack für Regie-App (PDF, Mail, etc.) |
| 🟢 Ab 16.06.2026 | **Domus-Revision 28** live — Aestico-Schnittstelle damit „offen" |
| 🟢 Geklärt (16.06.) | **Aestico-Import-Format = JSON v2** (`.aest`-Endung, JSON-Schema Draft-07) → [[aestico-schnittstelle/aestico-v2-spec\|Technische Spec im Vault]] |
| 🟡 In Arbeit | Field-Mapping Regiekopf/Detail → Aestico-Schema (Skeleton in Spec, jetzt konkretisieren) |
| 🔴 Offen | **Transport-Mechanismus** `.aest` → Domus-Server (Watch-Folder? SharePoint? T-Laufwerk?) — Klärung mit Turnkey + MVM-IT |
| 🔴 Offen | Konto-/KST-/Mwst-Logik (Schnittstelle zu DomusFiBu/Buchhaltung) |
| 🔴 Offen | Test-Mandant in Domus für Roundtrip-Tests |
| 🟢 Geklärt (15.06.) | **Lizenz Optiwork → MVM:** Nutzung Aestico-Schnittstelle für Offert-/Rechnungspositionen aus Eigenentwicklung erlaubt (Ziffer 6 unterzeichnet) |

## Mein erster Schritt-Plan

### Phase 0 — Setup (heute, 15.06.2026)
- [x] Sub-Hub angelegt (diese Notiz)
- [ ] Verteiler von Remos Originalmail nachschauen (Giovanni mit drin? Mike Kipfer? Sonst noch jemand?)
- [ ] Mit Giovanni Abstimmung: **Wer macht was?** Power BI/DAX vs. Power Platform vs. Domus-FiBu — Aufgabenteilung definieren

### Phase 1 — Spezifikation (KW 25–26, bis Ende Juni)
- [x] Aestico-Doku beschaffen (Optiwork-Doku v2, 2023-12-04) — vorhanden in `Dropbox/Miraglia-BI/MVM/Aestico/aestico_v2_doc/`
- [x] Import-Format geklärt: **JSON v2** (kein CSV, kein XML, keine REST-API) — Spec im Vault: [[aestico-schnittstelle/aestico-v2-spec]]
- [ ] Mit Domus-Anbieter ([[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]] / Turnkey) Kontakt aufnehmen — Schnittstellen-Support, Transport-Mechanismus, Customer-Mapping
- [ ] Mit [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl]] (MVM-IT) klären: Ablage-/Watch-Folder für `.aest`-Files, Service-Account-Berechtigungen
- [ ] **Field-Mapping-Tabelle** vervollständigen: Regiekopf-Spalten → Aestico-Felder (Skeleton in Spec, jetzt konkretisieren)
- [ ] Sonderfälle dokumentieren (KST 500 vs. 505, Hybrid-Mitarbeiter, Räber-Spezial-Logik)
- [ ] Test-`.aest`-Datei aus echtem Regie-Rapport bauen + gegen Schema validieren

### Phase 2 — Prototype (Juli)
- [ ] Test-Regie-Rapport → Aestico-Import-File generieren (manueller End-to-End)
- [ ] Domus-Import testen (Testmandant)
- [ ] Roundtrip: Regierapport → Aestico → Domus → Rechnung sichtbar
- [ ] Auto-Generierung über Power Automate (vermutlich erweitert auf bestehenden PDF-Flow)

### Phase 3 — Produktivierung (August / September)
- [ ] PL-Trigger-UI in Regie-App (Button auf Home oder Archiv)
- [ ] Sammelrechnung-Logik: Multi-Select in der Galerie → Aggregation → ein Import-File
- [ ] Fehler-Handling (Aestico schlägt Import zurück → User-Notification)
- [ ] Pilotierung mit 1–2 PL (vorschlag: Manuel Schärli, Schumacher Martin)

### Phase 4 — Rollout (Oktober)
- [ ] Schulung aller PL
- [ ] Doku im Vault: PL-Anleitung, Trouble-Shooting
- [ ] Go-Live bis **31.10.2026**
- [ ] Meilenstein-Update an Remo **per 30.09.2026** (Phase 2/3-Stand + Prognose Zieldatum)

## Offene Fragen — Klärung mit Remo / Giovanni / Mike

1. **Wer rechnet was ab?** Aestico generiert ja die Buchungszeile, aber:
   - Aufschlag/Marge/MwSt — wer rechnet das vor dem Import? Power Automate oder Aestico/Domus?
   - VP-Spalten-Logik aus der Magazin-App: gilt analog für Regierapport-Rechnungen?
2. **Welche Aestico-Version** ist mit Domus-Rev. 28 kompatibel? Aestico hat selbst Versionen.
3. **Wer macht die Aestico-Schnittstelle auf?** Domus-Anbieter im Rahmen Rev. 28, oder MVM-IT, oder S. Zumbühl?
4. **Identifier-Mapping:**
   - Welche Aestico-/Domus-Kundennummer hängt an welchem MVM-Empfänger?
   - Baustelle in Regie-App → Auftrag/Projekt in Domus — gibt es eine ID-Verknüpfung?
5. **Buchhaltungs-Logik bei Sammelrechnung:** Wie werden Regiekopf-übergreifende Positionen aggregiert? (z. B. Material aus mehreren Rapporten zur gleichen Baustelle)
6. **Domus-Rev.-28 — am 16.06. wirklich live?** Stefan Zumbühl hat Migration für 16.06. angekündigt — siehe Threads Alessandro/Stefan Anfang Juni.

## Beteiligte

- [[50.work/25_People/Remo-Pfister|Remo Pfister]] — Auftraggeber, GL MVM
- [[50.work/25_People/Giovanni-Miraglia|Giovanni Miraglia]] — Power BI / Domus-Datenmodell-Spezialist (siehe Giovannis Vault, READ-ONLY)
- [[50.work/25_People/Michael-Kipfer|Michael Kipfer]] — Kipfer DP, Power-Platform-Partner
- [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl]] — MVM-IT, Domus-Server / Infrastruktur
- [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser]] — Turnkey AG, Domus-Anbieter-Seite
- [[50.work/25_People/Alessandro-Castelli|Alessandro Castelli]] — Castelli Solutions, Power-Platform-Architekt
- [[50.work/25_People/M.-Schärli|Manuel Schärli]] — PL-Pilot Vorschlag

## Beteiligte Firmen / Lieferanten

- [[50.work/26_Firmen/MVM-AG|MVM AG]] — Endkunde
- [[50.work/26_Firmen/Optiwork-AG|Optiwork AG]] — Hersteller Domus + Aestico (Lizenzgeber)
- [[50.work/26_Firmen/Turnkey|Turnkey AG]] — Domus-Anbieter / Implementierung
- [[50.work/26_Firmen/Castelli-Solutions|Castelli Solutions]] — Power-Platform-Partner
- [[50.work/26_Firmen/Kipfer-DP|Kipfer DP]] — Power-Platform-Partner

## Verwandte Mails (Mail-Kontext rund um Domus-Rev. 28)

| Datum | Von | Betreff | Relevanz |
|---|---|---|---|
| 2026-06-10 09:21 | Remo Pfister | **Regie-Rapport → Automatisierte Rechnungserstellung im Domus** | **Hauptauftrag** |
| 2026-06-15 10:24 | Remo Pfister → Giovanni → Raoul | **WG: Gewährung Schnittstelle Aestico** (signierte Ziffer 6: Optiwork erlaubt MVM Aestico-Nutzung) | **Lizenz-Freigabe** — siehe Abschnitt „Lizenzrechtliche Grundlage" oben |
| 2026-06-12 12:13 | Alessandro Castelli | AW: Domus Migration am Dienstag — Zeitplan und Vorgehen | Domus-Migration 16.06.2026 |
| 2026-06-12 10:22 | S. Zumbühl (MVM) | AW: Domus Migration am Dienstag — Zeitplan und Vorgehen | Detail-Zeitplan Migration |
| 2026-06-12 14:07 | Alessandro Castelli | Domus: Testumgebung nach dem Go-Live am Dienstag | Test-Mandant-Verfügbarkeit |
| 2026-06-12 14:20 | Dominik Hüsser (Turnkey) | AW: Domus: Testumgebung nach dem Go-Live am Dienstag | Turnkey-Verfügbarkeit Test |
| 2026-06-12 10:58 | Alessandro Castelli | WG: MVM - CSV Laufwerk | T-Laufwerk-Sync, Migrationsdetail |

## Risiken

- 🟢 ~~**Aestico-Doku spät verfügbar**~~ — **erledigt 16.06.2026**: Doku ist vorhanden, Format ist JSON v2 (siehe [[aestico-schnittstelle/aestico-v2-spec]]).
- 🟡 **Buchhaltungs-Logik komplexer als angenommen** (z. B. Mwst-Sätze, Skonti, Sondertarife). Mitigation: in Phase 2 mit konkretem Test-Rapport früh validieren.
- 🟡 **Roundtrip-Test braucht Domus-Test-Mandant**, der erst nach Rev.-28-Live verfügbar wird. Mitigation: Reihenfolge so planen, dass Test-Mandant ab ~Anfang Juli läuft.
- 🟡 **Giovanni-Aufgabenteilung unklar** — wenn Giovanni die Domus-/Aestico-Seite übernimmt, muss ich das früh wissen, damit ich nicht doppelt baue.

## Persönliche Notizen

_Manuelle Notizen, Aestico-Spec-Snippets, Mapping-Drafts, Test-Ergebnisse hier ergänzen._

## Verwandt

### Spec / Technik
- [[aestico-schnittstelle/aestico-v2-spec|Aestico v2 — JSON-Schnittstellen-Spec]] (16.06.2026 angelegt)

### Hubs
- [[Regieapp-Neubau-MVM|Regie-Rapport-App (Haupt-Hub)]]
- [[Regieapp-Offline-Funktionalität|Regie-App Offline-Funktionalität (Sub-Hub)]]

### Firmen
- [[50.work/26_Firmen/MVM-AG|MVM AG (Klient)]]
- [[50.work/26_Firmen/Optiwork-AG|Optiwork AG (Hersteller Domus + Aestico)]]
- [[50.work/26_Firmen/Turnkey|Turnkey AG (Domus-Anbieter)]]

### Personen
- [[50.work/25_People/Remo-Pfister|Remo Pfister (Auftraggeber)]]
- [[50.work/25_People/Dominik-Hüsser|Dominik Hüsser (Turnkey)]]
- [[50.work/25_People/Stefan-Zumbühl|Stefan Zumbühl (MVM-IT)]]
- [[50.work/25_People/Alessandro-Castelli|Alessandro Castelli (Castelli Solutions)]]
- [[50.work/25_People/Giovanni-Miraglia|Giovanni Miraglia]]

### Daily
- [[60.daily/2026-06-15|Daily 2026-06-15]] — ToDo 7
- [[60.daily/2026-06-16|Daily 2026-06-16]] — Aestico-Doku-Auswertung
