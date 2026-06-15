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
updated: 2026-06-15
last_change: "2026-06-15: Lizenz Optiwork↔MVM Ziffer 6 dokumentiert (Mail Remo→Giovanni→Raoul 15.06.)"
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
| 🟡 Ab 16.06.2026 | **Domus-Revision 28** geht live — Aestico-Schnittstelle wird damit „offen" |
| 🔴 Offen | Aestico-Import-Format-Spezifikation (Aestico-Doku, Domus-Rev.-28-Doku) |
| 🔴 Offen | Field-Mapping Regiekopf/Detail → Aestico-Schema |
| 🔴 Offen | Konto-/KST-/Mwst-Logik (Schnittstelle zu DomusFiBu/Buchhaltung) |
| 🔴 Offen | Test-Mandant in Domus für Roundtrip-Tests |
| 🟢 Geklärt (15.06.) | **Lizenz Optiwork → MVM:** Nutzung Aestico-Schnittstelle für Offert-/Rechnungspositionen aus Eigenentwicklung erlaubt (Ziffer 6 unterzeichnet) |

## Mein erster Schritt-Plan

### Phase 0 — Setup (heute, 15.06.2026)
- [x] Sub-Hub angelegt (diese Notiz)
- [ ] Verteiler von Remos Originalmail nachschauen (Giovanni mit drin? Mike Kipfer? Sonst noch jemand?)
- [ ] Mit Giovanni Abstimmung: **Wer macht was?** Power BI/DAX vs. Power Platform vs. Domus-FiBu — Aufgabenteilung definieren

### Phase 1 — Spezifikation (KW 25–26, bis Ende Juni)
- [ ] Aestico-Doku beschaffen (Domus-Rev. 28 — am 16.06. verfügbar)
- [ ] Import-Format-Beispiel von Aestico besorgen (CSV? XML? JSON?)
- [ ] Mit Domus-Anbieter (vermutlich über S. Zumbühl / MVM-IT) Kontaktdetails für Schnittstellen-Support klären
- [ ] **Field-Mapping-Tabelle** erstellen: Regiekopf-Spalten → Aestico-Felder
- [ ] Sonderfälle dokumentieren (KST 500 vs. 505, Hybrid-Mitarbeiter, Räber-Spezial-Logik)

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

## Beteiligte (vermutlich)

- [[50.work/25_People/Remo-Pfister|Remo Pfister]] — Auftraggeber, GL
- **Giovanni Miraglia** — Power BI / Domus-Datenmodell-Spezialist (siehe Giovannis Vault, READ-ONLY)
- **Mike Kipfer** — vermutlich Domus-/ERP-Seite, Castelli-Solutions-Strang
- **Stefan Zumbühl** (MVM-IT) — Domus-Server-Migration
- **Dominik Hüsser** (Turnkey) — Domus-Anbieter-Seite
- **Alessandro Castelli** (Castelli-Solutions) — Power-Platform-Architekt
- [[50.work/25_People/M.-Schärli|Manuel Schärli]] — PL-Pilot Vorschlag

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

- 🔴 **Aestico-Doku spät verfügbar** → Phase 1 könnte sich verzögern → Phase 4 in Q4 eng. Mitigation: bis 16.06. abend gehst du den Phase-0-Check mit Giovanni durch; bei Doku-Verzug → früh eskalieren.
- 🟡 **Buchhaltungs-Logik komplexer als angenommen** (z. B. Mwst-Sätze, Skonti, Sondertarife). Mitigation: in Phase 2 mit konkretem Test-Rapport früh validieren.
- 🟡 **Roundtrip-Test braucht Domus-Test-Mandant**, der erst nach Rev.-28-Live verfügbar wird. Mitigation: Reihenfolge so planen, dass Test-Mandant ab ~Anfang Juli läuft.
- 🟡 **Giovanni-Aufgabenteilung unklar** — wenn Giovanni die Domus-/Aestico-Seite übernimmt, muss ich das früh wissen, damit ich nicht doppelt baue.

## Persönliche Notizen

_Manuelle Notizen, Aestico-Spec-Snippets, Mapping-Drafts, Test-Ergebnisse hier ergänzen._

## Verwandt

- [[Regieapp-Neubau-MVM|Regie-Rapport-App (Haupt-Hub)]]
- [[Regieapp-Offline-Funktionalität|Regie-App Offline-Funktionalität (Sub-Hub)]]
- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]
- [[50.work/25_People/Remo-Pfister|Remo Pfister]]
- [[60.daily/2026-06-15|Daily 2026-06-15]] — ToDo 7
