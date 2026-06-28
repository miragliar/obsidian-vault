---
name: MVM Power Platform News — Vorbereitung (Sync 28.06. + Vor-Ort)
slug: MVM-News-Vorbereitung-2026-06
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Vorbereitung
zeitraum: Interner Sync 28.06.2026 (abends) · Vor-Ort-News nächste Woche
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, power-platform, meeting-prep, regie, ausmass]
type: meeting-prep
source: m365-graph (Mail Giovanni 28.06) + Dataverse-Journal + Projekt-Hubs
created: 2026-06-28
updated: 2026-06-28
---

# MVM Power Platform News — Vorbereitung

> [!abstract] TL;DR für deinen Part
> Dein Block sind die **Baustellen-/Rapportprozesse (Regie-App)** und die **KI (Digitales Ausmass)**.
> - **Regie-App** = dein Flaggschiff 2026: Komplett-Neubau, **seit 01.06. live**, jetzt Stabilisierung + neue **Aestico→Domus-Rechnung**. → **Live-Demo-Kandidat Nr. 1.**
> - **Ausmass** = Konzept tragen, **Betrieb ist an Giovanni übergeben** (Snapshot 22.06., damit er es vor Ort zeigt). Du lieferst das „Wie funktioniert's" + Ausblick.
> - Heute klären: **Welche Demos**, **Reihenfolge**, **wer zeigt Ausmass vor Ort**.

## 1 · Kontext des Termins

**Mail Giovanni, 28.06. 17:48** — interner Sync zur Vorbereitung der „Power Platform News" bei MVM **nächste Woche vor Ort** bei [[50.work/25_People/Remo-Pfister|Remo Pfister]] & [[50.work/25_People/Sascha Ziswiler|Sascha Ziswiler]].

- **Heute Abend, ca. 30–60 Min, Teams** (ID `363 183 677 615 085`, Passcode `AB9tc6bB`).
- **Dabei:** Giovanni · du · **Mike Kipfer** · **Ale Castelli** (3 Firmen: Miraglia BI / Castelli Solutions / Kipfer Digital-Power).
- **Ablauf:** jede(r) sagt kurz woran er steht → Highlights & Demos festlegen → offene Punkte & Reihenfolge.
- Giovanni hat 3 Dokumente angehängt — relevant für dich ist v. a. das **Kunden-PDF „Stand & Ausblick"** (die Aussensicht, in der dein Part eingebettet ist).

> [!note] Wo dein Part im Kunden-PDF steht
> - **Baustellen- & Rapportprozesse:** „Regie-Rapport-App komplett neu: mobil, offline-fähig, mit automatischer PDF-Erstellung inkl. Baustellenfotos" + „Neue Schnittstelle erzeugt aus den Rapporten automatisch Einzel- und Sammelrechnungen in Domus".
> - **Künstliche Intelligenz:** „Digitales Ausmass: KI liest Ausmasse (Räume, Flächen, Öffnungen) automatisch aus Bauplänen … Pilot erfolgreich getestet."
> - **Ausblick H2/2026:** Ausmass produktiv (Plausibilisierung + Prüf-App) · **Aestico-Schnittstelle live**.

---

## 2 · Regie-App — dein Hauptthema

> **In einem Satz:** Mobile, offline-fähige App, mit der die Baustelle Stunden + Material + Personen rapportiert → automatisch PDF (inkl. Fotos) an den Projektleiter → automatisch Rechnung in Domus (via Aestico).

### Die Story (so erzählst du „woran du stehst")

| Phase | Was (grob) |
|---|---|
| **Ausgangslage** (Jan '26) | Alte Regie-App lief, aber chronische Probleme (Archiv/Anzeige, kaputte PDF-Vorlage, zusammenrutschende Rapporte) → Entscheid **Komplett-Neubau** |
| **Bau** (Apr '26) | Neues Dataverse-Datenmodell (Regiekopf + 3 Detailtabellen), neue App, PDF-Automatisierung mit Foto-Merge |
| **Go-Live** (01.06.) | Produktiv aufgeschaltet — neue Sicherheitsgruppen, Berechtigungen, erste User live |
| **Seit Go-Live** | Offline-Modus aufs Handy, Kopierfunktion für Rapporte, Excel-Rapportübersicht an PL, viele Stabilisierungen |
| **Neu & Ausblick** (16.06.) | **Aestico-Schnittstelle**: aus Rapporten automatisch **Einzel- UND Sammelrechnung** (Optiwork-Format → Domus) |

### ✅ Was gut lief (Talking Points)

- Kompletter **Neubau erfolgreich live** seit 1. Juni — sauberer Schnitt weg von der Altlast.
- **Offline-fähig & mobil** — Erfassung auf der Baustelle ohne Empfang.
- **Automatisches PDF inkl. Baustellenfotos** an den PL.
- **Aestico/Domus-Rechnung** (Einzel + Sammel), schema-konform gegen die offiziellen Optiwork-Vorgaben geprüft → der grosse Automatisierungsgewinn.

### ⚠️ Was schiefging / Lessons Learned (ehrlich, gut fürs Sync)

- **Kernproblem der Altapp:** Dataverse-*Delegierung* bei zu grossem Archiv → Rapporte „verschwanden". Im Neubau über aufgeteilte Collections gelöst.
- **~15 leere „Geister-Rapporte"**, weil Pflichtfelder nicht erzwungen waren → mit Feldvalidierung / gesperrtem „Weiter"-Button gefixt.
- **Mobile-spezifische Bugs:** zuletzt (27.06.) „keine Daten" nur am Handy — Ursache ein noch als *Preview* markiertes Microsoft-Tabellen-Control, **kein** Datenfehler. → falls die Demo am Handy zickt: bekannt, nicht unsere Datenlogik.
- **SharePoint-Berechtigung = Pflicht-Voraussetzung** pro User (sonst schlägt Save+Send fehl + irreführende „an sich selbst gesendet"-Meldung).
- Weitere Altstolpersteine alle im Neubau adressiert (geleertes BST-Lookup nach Refresh, Punkte in Ordnernamen, Touch-Propagation am Handy).

> Tiefe Details (nicht für die Demo nötig): [[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]] · [[Regieapp-Schwachstellen-Review|Schwachstellen-Review (K1–K35)]] · [[Regieapp-Offline-Funktionalität|Offline-Funktionalität]] · [[Regieapp-Aestico-Domus-Import|Aestico → Domus]] · [[Regieapp-Bug-Personen-Mobile-keineDaten|Mobile-Bug „keine Daten"]]

### → Demo-Empfehlung

Regie-App = dein stärkster **Live-Demo-Kandidat** (sehr greifbar für Remo/Sascha): **Rapport am Handy erfassen → PDF mit Foto → Aestico-Rechnung**. Nah am Tagesgeschäft, visuell, zeigt den ganzen Bogen Erfassung → Rechnung.

---

## 3 · Digitales Ausmass (KI) — Konzept tragen, Betrieb ist übergeben

> [!important] Übergabe-Status
> **An Giovanni übergeben am 22.06.** — lauffähiger Prototyp-Snapshot in der geteilten Dropbox (`MVM/Ausmass/KI-Ausmass-Solution/`) inkl. Guide `START-HIER_Giovanni.md`, **genau damit er den Stand vor Ort zeigen kann**. → Vor Ort demot voraussichtlich **Giovanni**; du lieferst Konzept + Ausblick. (Davor: Code-Übergabe an Mike Kipfer am 27.05.)

### Wie genau die Ausmasse ausgelesen werden (parat haben)

1. **Input:** MVM erhält Offertanfragen als **SIA-konforme Devisierung** (`SIA451.01S` / `.crbx` = strukturierte NPK-Positionsliste) **plus Architekten-Pläne** (PDF). Man legt einen **ganzen Projektordner** ab → Prozess startet.
2. **Schlüssel-Einsicht:** Der ganze Workflow ist **strukturiert — kein OCR auf der Devis-Seite**. Input (SIA) und Output (Messerli-ESO) sind strukturierte Daten; die KI muss „nur" **die Mengen dazwischen** ermitteln.
3. **Kein „from scratch":** In der Anfrage stehen bereits **Vorschlags-Mengen** (grobe Architekten-Schätzung). Die KI **plausibilisiert + ergänzt + verfeinert** — sie misst nicht bei null.
4. **Pläne enthalten strukturierte Raumdaten:** pro Raum Nr., Bezeichnung, **BF** (Bodenfläche), **RH** (Raumhöhe), **B/W/D**-Material-Tags. → Viele Standardpositionen per **Text-Extraktion** (billig/schnell, PyMuPDF). **Vision-KI (Claude)** nur für das Harte: Wandflächen/Umfänge, Stürze, Türen-/Fenster-Zählung.
5. **Pipeline:** Python extrahiert grob → JSON → **Claude liest JSON + Pläne**, schreibt Korrekturen (umbenennen/entfernen/Flächen/Türen/Fenster) + Warnungen → Python wendet an + baut **ein finales Excel** mit Korrektur-Log.
6. **Output:** strukturiertes Excel (Goldstandard-Format), Ziel → `.eso` für Messerli BAUAD. **Mehrsprachig DE/IT/FR**, an 3 realen Projekten validiert (Bleicherstrasse, Baila, La Mobiliare Tessin).

### Status & Ziel

- **Phase 1 (Read & Round-Trip) abgeschlossen**, Drop-Folder-Workflow läuft. Pilot erfolgreich getestet.
- **Kickoff mit [[50.work/25_People/Reto-Limacher|Reto Limacher]]** (Offertwesen-Lead) am 15.06.
- **Ziel (Sascha, 28.05.):** bis 31.12.2026 produktiv im Offertwesen.
- **Ausblick im Kunden-PDF:** produktiv mit **Mengen-Plausibilisierung + Prüf-App** für die Freigabe, dann Pilotbetrieb.

> Voll-Konzept inkl. Phasenplan & Risiken: [[KI-Ausmass-MVM|KI-Ausmass MVM (Devis-Copilot)]]

---

## 4 · Deine weiteren laufenden Prozesse (kurz, falls Thema)

- **Magazin-/Material-Prozess:** Bestell-App mit Magaziner-Genehmigung → PDF + **QR-Rechnung**; neu Verkaufspreis-Logik (intern/extern), Direktbezug-Freigabe. Läuft, kleinere Fixes zuletzt. → [[Magazin-App-MVM|Magazin-App]]
- **Mahnprozess:** komplett auf **Cloud** umgebaut (pdf4me), Abgleich gedruckte Rechnungen ↔ Domus-Mahnlauf, Hybrid-MA eingebunden. → [[Mahnprozess-MVM|Mahnprozess]]
- **HR-Zeugnistool:** KI-generierte Arbeitszeugnisse, korrekte Zeitform, Schweizer Orthografie (ss); Model-Driven-Editieransicht. → [[Zeugnis-App-MVM|Zeugnis-App]]
- **Kreditoren-/Rechnungsfreigabe** (KI-Beleg in Teams → Domus) und **Offert-Doublettencheck** (KI) — laufen, eher Nebenschauplätze für diesen Termin.

---

## 5 · Fürs Sync entscheiden / mitbringen

- [ ] **Regie:** welche 2–3 Features live zeigen? (Vorschlag: Mobil-Rapport → Foto-PDF → Aestico-Rechnung)
- [ ] **Ausmass:** **wer demot vor Ort** (Giovanni hat den Snapshot) — und bist du nächste Woche selbst dabei oder in den Ferien?
- [ ] **Reihenfolge** deines Blocks: Regie (live, stark) → Ausmass (Konzept + Ausblick Prüf-App)
- [ ] **Offene Punkte** einbringen: **Aestico-Go-Live** als „live next", Geister-Rapport-Fix erledigt, Mobile-Preview-Control-Thema (Microsoft-seitig)

---

## Verwandt

- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]
- [[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]] · [[Regieapp-Aestico-Domus-Import|Aestico → Domus]] · [[Regieapp-Schwachstellen-Review|Schwachstellen-Review]]
- [[KI-Ausmass-MVM|KI-Ausmass MVM (Devis-Copilot)]]
- [[Magazin-App-MVM|Magazin-App]] · [[Mahnprozess-MVM|Mahnprozess]] · [[Zeugnis-App-MVM|Zeugnis-App]]
