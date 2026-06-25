---
name: Regie-Rapport-App — Bug "keine Daten" auf dem Handy (Personen-Korrektur)
slug: Regieapp-Bug-Personen-Mobile-keineDaten
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
parent: "[[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regieapp-Neubau-MVM]]"
status: Ursache identifiziert
melder: Remo Pfister
meldung_datum: 2026-06-25
betroffener_rapport: "26-1124"
umgebung: Prozesse Produktion (7b1a7c1a-efba-e4b4-8666-97c3fe33ab4a)
solution: Regie Rapport Prozess
app: Regie Rapport App (publiziert 2026-06-17)
type: bug-analysis
tags: [miraglia, mvm-ag, power-apps, canvas, mobile-offline, modern-controls, root-cause]
created: 2026-06-25
updated: 2026-06-25
---

# Regie-App — "Leider kommen keine Daten" auf dem Handy

**Melder:** Remo Pfister (Mail "Neue Regie-App", 2026-06-25)
**Analyse:** Claudian — read-only Diagnose in *Prozesse Produktion* (Login `powerplatform@mvm-ag.ch`)
**Konfidenz:** **Sehr hoch** für die Ursache (sauberer Negativ-/Positiv-Vergleich im Code, s. u.). Der genaue Auslöse-Moment "beim Querstellen" ist mit hoher Konfidenz erklärt, sollte aber am Gerät einmal gegengeprüft werden.

> **Reviewer-Hinweis:** Jeder Befund ist mit Datei + Zeile (entpackte Live-`.msapp`) bzw. mit einer Dataverse-Abfrage belegt. Microsoft-Doku-Belege sind unten unter *Quellen* verlinkt.

---

## 1. Symptom (wie gemeldet)

Mitarbeiter erstellt Rapport **26-1124**. In der Ansicht **„PDF-PL-schicken"** fällt auf, dass die Personenstunden nicht stimmen (einmal 2 h, einmal 3 h erfasst). Korrektur über den Button → auf dem **Handy** erscheint eine Ansicht → **Handy ins Querformat gedreht** → **„Leider kommen keine Daten!"**. Auf dem **Desktop (über Teams)** liess sich derselbe Rapport öffnen und korrigieren.

Kernmuster: **Desktop/Teams = funktioniert, Handy = keine Daten.** Speziell der **Korrektur-/Personen-Screen**, nicht die PDF-Vorschau.

---

## 2. Ursache (Executive Summary)

Die **Personen-Korrekturliste** (und Material-/Abschluss-Liste) ist mit dem **modernen „Table"-Steuerelement** (`Table@1.0.278`, intern *PowerAppsOneGrid*) bzw. dem **`ModernDataGrid@1.3.0`** gebaut. **Beide sind Microsoft *Preview*-Controls** ("pre-release, subject to change", nicht für Produktion). Im **Power-Apps-Mobile-Player** (der die App **offline** ausführt) rendern diese Preview-Grids die Dataverse-Zeilen **nicht zuverlässig** → leere Liste = „keine Daten".

Auf dem **Desktop/Teams** läuft dieselbe App im **Online-Web-Runtime** (Teams- und Browser-Apps können laut MS gar nicht offline laufen) → das Grid wird server-seitig befüllt → Daten erscheinen, Korrektur klappt.

**Beweis, dass es am Control liegt und nicht an Daten/Filter:** Die **PDF-PL-schicken-Ansicht zeigt exakt dieselben Personenzeilen mit demselben Filter**, aber über eine **klassische `Gallery`** — und die **funktioniert auf dem Handy**. Gleiche Daten, gleicher Filter, gleicher `currentitem`; einziger Unterschied = **Control-Typ**.

| Screen | List-Control | Datei:Zeile | Handy |
|---|---|---|---|
| **PDF Editierung** ("PDF-PL-schicken") | klassische **`Gallery@2.15.0`** | `PDF Editierung.pa.yaml:23` | **funktioniert** ✅ |
| **Personen** (Korrektur) | **`Table@1.0.278`** (Preview/OneGrid) | `Personen.pa.yaml:201` | **keine Daten** ❌ |
| **Material** (Korrektur) | **`Table@1.0.278`** (Preview/OneGrid) | `Material.pa.yaml:277` | gleiches Risiko ❌ |
| **Fotos** | **`Table@1.0.278`** (Preview/OneGrid) | `Fotos.pa.yaml:195` | gleiches Risiko ❌ |
| **Abschluss** | **`ModernDataGrid@1.3.0`** (Preview) | `Abschluss-Screen.pa.yaml:84,186` | gleiches Risiko ❌ |

Der **Filter ist in allen Fällen identisch**:
`=Filter(Personenzeilen; Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID')`

---

## 3. Warum „erst beim Querstellen"?

Der Personen-Screen ist ein **Master-Detail-Layout**, das per Bildschirmgrösse umschaltet (`Personen.pa.yaml`):

- **Hochformat (Handy, `Personen.Size = ScreenSize.Small`):** Es ist nur **eine** Spalte sichtbar. Standardmässig die **Liste** (Sidebar mit dem Table-Control, `Visible`-Logik Zeile 160), das Detail-Formular ist ausgeblendet (Zeile 504).
- **Querformat (Handy wird breiter → `Size` wechselt von `Small` auf `Medium`/`Large`):** Jetzt werden **Liste + Detail-Formular gleichzeitig** eingeblendet. Das **Table-Control wird im zweispaltigen Layout neu dimensioniert/gerendert** — und genau dabei zeigt das Preview-OneGrid-Control die Zeilen nicht mehr an.

Zusätzlich verschärfend (`App.pa.yaml:27-37`): die Variable **`varsmartphone` wird nur **einmalig** in `App.OnStart`** aus `App.Width < 600` gesetzt — also ein **statischer Schnappschuss vom App-Start**. Sie aktualisiert sich beim Drehen **nicht**, während `Personen.Size` **reaktiv** umschaltet. Die App mischt damit eine eingefrorene und eine reaktive Layout-Quelle → inkonsistentes Verhalten nach dem Drehen.

> Kurz: Das Drehen löst den Layout-Wechsel aus, der das (ohnehin auf dem Handy unzuverlässige) Preview-Grid in einen Zustand bringt, in dem es leer bleibt.

---

## 4. Beleg-Kette im Detail

**a) App läuft auf dem Handy offline.** Die App hat ein gebundenes Offline-Profil ("Regie Rapport App Profile", geändert 2026-06-17, gleicher Tag wie Publish). Beleg zusätzlich: der **App Checker** der `.msapp` emittiert eine Regel der Kategorie *offline* (`app-NotOfflineEnabledTable`) — diese Regelklasse entsteht nur bei **offline-aktivierten** Apps.

**b) Desktop = Online, Handy = Offline (MS-Doku).**
- "Canvas apps in **Teams** … doesn't work [offline]" und "Canvas apps running in **web browsers** can't run offline" → Desktop/Teams = Online-Runtime → Grid wird befüllt.
- Offline-Runtime gibt es nur im nativen Power-Apps-Mobile-Player (iOS/Android/Windows) → hier greift die Schwäche der Preview-Controls.

**c) Modern Table & Data Grid sind Preview.** MS Learn: „**Table modern control in Power Apps (preview)** — [This article is pre-release document and is subject to change.]" und „**Data Grid modern control … (preview)**". Preview-Features sind laut MS „**not meant for production use and may have restricted functionality**".

**d) Es ist nicht der Beziehungs-Filter.** `Regiekopf.'Rapport-ID' = …` ist eine **Ein-Ebenen-Lookup-Navigation**; die ist laut MS-Doku **offline erlaubt** (Beispiel `Filter(Account; 'ContactID'.'Zipcode' = "11056")`). App Checker flaggt diese Filter auch nicht als Offline-Problem. → Filter ist nicht die Ursache der leeren Liste.

**e) Flows sind nicht beteiligt.** Aktive Custom-Flows in der Umgebung: `02_V2 - rrpt - PDF Generierung`, `01 - rrpt - Notify PL`, `Unbenannter Flow`. Entwürfe: `03_V2 - XLSX`, `04 - Rechnung BRZ`. Rest = Standard-Dataverse-System-Flows. **Kein Flow rendert die Personenliste**, und laut MS „**Power Automate flows aren't supported in offline mode**". `plugintracelog` ist **leer** → keine serverseitigen Plugin-/Flow-Fehler. ⇒ Der Fehler ist rein **client-seitiges Rendering**.

**f) Datenlage Rapport 26-1124 (Dataverse, read-only).**
- Regiekopf `23cd0e58-3e0b-4c10-bcc6-83bac7bc0563`, Besitzer **Isacco Rizzo**, Status **PL**, KW 26/2026, erstellt 2026-06-24, geändert 2026-06-25 07:23 (= die Desktop-Korrektur).
- **Nur 1 Personenzeile** vorhanden: `cr19a_stundentotal = 2.0` (Mittwoch 2 h), erstellt 2026-06-24 09:36, nie geändert.
- **Die zweite Zeile (3 h) existiert in Dataverse nicht.**
- Besitzer = Rizzo selbst → das Offline-Profil (`regiekopf = ownedByMe`) blockiert ihn **nicht**; seine eigenen Rapporte synchronisieren aufs Gerät. Die fehlende 3-h-Zeile passt dazu, dass er sie **auf dem Handy nicht erfassen/korrigieren konnte** (Korrektur-Screen leer) und auf den Desktop ausweichen musste.

---

## 5. Lösung

### P1 — Behebt den gemeldeten Fehler: Preview-Grids durch Gallery ersetzen

Die **Korrektur-/Listen-Controls** auf **Personen**, **Material**, **Fotos** und **Abschluss** von den Preview-Controls (`Table@1.0.278` / `ModernDataGrid@1.3.0`) auf die **klassische `Gallery`** umstellen — exakt das Control, das auf demselben Datenstand in `PDF Editierung` (`GalleryPersonen`/`GalleryMaterial`) auf dem Handy nachweislich funktioniert.

- `Items` bleibt unverändert:
  `=Filter(Personenzeilen; Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID')`
- Auswahl-Verdrahtung: statt `Table3.Selected` / `Table3.SelectedItems` künftig `Gallery.Selected` verwenden (Detail-Formular `Form2.Item` entsprechend an die Gallery-Selektion hängen).
- **Sortierung explizit setzen** (Offline-Best-Practice), z. B.:
  `=Sort(Filter(Personenzeilen; Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID'); rrpt_datum)`

> PowerFx in **deutscher** Maker-Syntax (Semikolon als Parametertrenner) — direkt kopierbar.

### P2 — `varsmartphone` reaktiv machen

`App.OnStart:27-37` setzt `varsmartphone` einmalig (statischer Schnappschuss). Layout-Eigenschaften stattdessen **reaktiv** auf die Screen-Grösse beziehen, konsistent mit der bereits genutzten `…Size = ScreenSize.Small`-Logik, z. B.:
`Layout: =If(Self.Size = ScreenSize.Small; "Icon only"; "Icon before")`
(bzw. den jeweiligen Screen-`Size`-Wert verwenden), und die statische Variable nicht mehr für Layout-Entscheide heranziehen.

### P3 — Hygiene (vom App Checker der Live-App gemeldet)

- **`Environment Variable Values`** ist nicht offline-aktiviert (`app-NotOfflineEnabledTable`). `varenv` hat zwar einen sicheren Default ("Produktion"), trotzdem Tabelle offline aktivieren **oder** Abhängigkeit entfernen.
- **`Grenzwert für Datenzeilen` > 500** (`app-DataSourceDefaultMaxRowsLimit`, Performance) → auf ≤ 500 senken und Filter delegierbar halten.
- `app-CrossScreenEventDependencies` (7×) rund um `currentitem` — beim Umbau der Selektion gleich mitbereinigen.

---

## 6. Verifikation / nächste Schritte

1. **Reproduktion am Gerät** (1 Min.): Rapport mit ≥ 1 Personenzeile auf einem Handy im **Power-Apps-Mobile-Player** öffnen, Personen-Korrektur aufrufen, **quer drehen** → erwartet: Liste leer. Danach Fix einspielen → erwartet: Gallery zeigt Zeilen in beiden Lagen.
2. **Fix in Studio** umsetzen (Gallery statt Preview-Grid), App **republishen**, User App schliessen/neu starten.
3. **26-1124 fachlich**: die fehlende **3-h-Zeile** mit Rizzo abklären und sauber nacherfassen (aktuell nur 2 h Mittwoch gespeichert).

---

## Quellen (Microsoft Learn)

- Mobile offline limitations for canvas apps — Teams/Browser nicht offline, Relationship-Filter 1 Ebene, Flows offline nicht unterstützt: <https://learn.microsoft.com/power-apps/mobile/limitations-canvas-apps>
- Table modern control (preview): <https://learn.microsoft.com/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-table>
- Data Grid modern control (preview): <https://learn.microsoft.com/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-data-grid>
- Develop offline-capable canvas apps (nativer Player offline, Browser nicht): <https://learn.microsoft.com/power-apps/maker/canvas-apps/offline-apps>
- Set up mobile offline / Best Practices (Sortierung, Gallery): <https://learn.microsoft.com/power-apps/mobile/canvas-mobile-offline-setup>

## Verwandt

- [[50.work/projekte/MVM-AG/Regieapp-Schwachstellen-Review|Regieapp-Schwachstellen-Review]]
- [[50.work/projekte/MVM-AG/Regieapp-Offline-Funktionalität|Regieapp-Offline-Funktionalität]]
- [[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regieapp-Neubau-MVM]]
- [[50.work/power-platform/powerfx-deutsche-lokalisierung|PowerFx deutsche Lokalisierung]]
