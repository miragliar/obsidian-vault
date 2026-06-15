---
name: Regie-Rapport-App (Neubau)
slug: Regieapp-Neubau-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Live / Wartung
zeitraum: April 2026 — Juni 2026 Live-Schaltung
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, power-apps, dataverse, offline, sharepoint]
type: projekt-hub
source: claude-import + m365-graph + chat-context 2026-06-04
created: 2026-06-01
updated: 2026-06-15
sub_hubs:
  - "[[Regieapp-Offline-Funktionalität|Offline-Funktionalität]]"
  - "[[Regieapp-Aestico-Domus-Import|Aestico-Schnittstelle / Domus-Rechnungsautomatisierung]]"
---

# Regie-Rapport-App (Neubau)

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]]  
**Status:** Live / Wartung (produktiv aufgeschaltet 01.06.2026)
**Zeitraum:** April 2026 — Juni 2026 Live-Schaltung

## Worum geht es

Neukonzeption und Aufbau einer Power-Apps-Regie-Rapport-App für die mobile Erfassung von Arbeits-, Material- und Personenzeilen auf Baustellen. Dataverse-Datenmodell mit Offline-Profile für Außendienst, Filter+Search-UI, Form-Submit-Logik.

## Sub-Hubs / Teilprojekte

| Hub | Status | Was |
|---|---|---|
| [[Regieapp-Offline-Funktionalität|Offline-Funktionalität]] | In Arbeit | Mobile Offline-Profile, Cross-Tenant (Zug), Fotos offline, Cascade-Delete-Atomarität, Sync-Fehler-Handling |
| [[Regieapp-Aestico-Domus-Import|Aestico-Schnittstelle / Domus-Rechnungsautomatisierung]] | Setup | Regie-Rapport → Domus-Rechnung via Aestico, Auftrag Remo 10.06., Ziel 31.10.2026 |
| [[Regieapp-Schwachstellen-Review|Schwachstellen-Review]] | Lebendes Doku | K1–K35 Code-Review, Severity-Sortierung |
| [[Regieapp-v1-0-0-26-Diff-Review|v1.0.0.26 Diff-Review]] | Snapshot | Diff-Doku zum letzten Solution-Upgrade |

## Beteiligte

### Geschäftsleitung / Ansprechpartner
- [[50.work/25_People/Remo-Pfister|Remo Pfister]] — Power-Platform-Lead, Mitglied GL
- [[50.work/25_People/M.-Schärli|Manuel Schärli]] — Test-/Live-Feedback Gipserei

### PL-Gruppe „Power Apps PL" (Entra-Gruppe `2effe64a-6339-4c83-bfef-663590883137`)
- [[50.work/25_People/Richy-Schön|Richy Schön]] — rein 06.2026
- [[50.work/25_People/Jan-Schwitter|Jan Schwitter]] — rein 06.2026
- [[50.work/25_People/Reto-Limacher|Reto Limacher]] — raus 06.2026 (bleibt aber Offertwesen Lead)

### Standort Meggen
- [[50.work/25_People/Stefanie-Furrer|Stefanie Furrer]] — PL Meggen
- [[50.work/25_People/Antonio-De-Finis|Antonio De Finis]] — Maler Meggen, seit 01.05.2026

### Hybrid-Mitarbeiter
- [[50.work/25_People/Christoph-Räber|Christoph Räber]] — Kundendienst Fassade

## Kontext / Architektur

- Architektur: Master-Tabelle `Regiekopf` + drei N:1-Detail-Tabellen (Arbeitsbeschriebzeile, Materialzeile, Personenzeile).
- Stammdaten-Lookups: Baustelle, Materialkatalog, Mitarbeitertypen.
- Mobile-First: Außendienst erfasst auf der Baustelle, oft ohne Netz → Offline-Profil als zentrale Anforderung.
- UI mit Combobox-Mehrfachauswahl (Baustelle) + Volltextsuche über Empfänger, Kalenderwoche, PL-Kommentar.

## Quell-Conversations (Claude-Export)

Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). Die destillierten Pattern-Notizen sind unter „Verwandte Patterns“.

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 46 | 2026-05-20 | Offlineprofil Fehler beim Speichern und Öffnen | `ad2297d4…` |
| 42 | 2026-04-09 | Filter mit Combobox und Textsuche erweitern | `46548c10…` |
| 9 | 2026-04-08 | Neukonzeption einer Regie-Rapport-App für Power Platform | `47b30ad6…` |
| 2 | 2026-04-16 | Regieapp-Testphase und Zugriffsverwaltung | `f58e17d1…` |
| 2 | 2026-05-03 | Neue Regie-App und Power Apps Installation | `a6b53a21…` |

## Verwandte Pattern-Notizen

- [[50.work/power-platform/powerfx-deutsche-lokalisierung|PowerFx — Deutsche Lokalisierung (`;` / `;;`)]]
- [[50.work/power-platform/powerfx-disambiguation-und-as-operator|PowerFx — Disambiguation `[@…]` + `As`-Operator]] 🆕 aus Kopierfunktion 2026-06-11
- [[50.work/power-platform/powerapps-navigate-bricht-onselect-cleanup|Navigate() bricht OnSelect-Cleanup + Mobile-Touch-Falle]] 🆕 aus Mobile-Bug 2026-06-11
- [[50.work/power-platform/powerfx-filter-search-combobox|Filter + Search + Combobox kombinieren]]
- [[50.work/power-platform/powerfx-hidden-datacard-submitform|Hidden Datacard SubmitForm]]
- [[50.work/power-platform/dataverse-offlineprofile|Mobile Offline-Profile]]
- [[50.work/power-platform/dataverse-mysterious-deletes|Cascade-Delete-Diagnose]]
- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Flow-Save-Voraussetzung]]

## Erkenntnisse / Lessons Learned

- Auto-generiertes Offline-Profil → nutzlos. Eigenes Profil in Solution anlegen, sonst Schema-Drift bei jeder Spaltenänderung.
- Lookup-Filter ohne `.Id`-Suffix verwenden: `Baustellelookup in ComboBox1.SelectedItems` ist delegierbar und sauberer.
- `Search()` außen, `Filter()` innen — UI-Pattern für Combobox + Volltext.
- Hidden Datacards mit `Visible = false` schreiben NICHT in Dataverse → stattdessen `Height: 0, Visible: true`.
- 🆕 **SharePoint-Berechtigung auf Speicherort = Pflicht-Voraussetzung** für jeden User der Rapporte erfasst. Wenn der Flow das PDF dort nicht ablegen kann, schlägt Save+Send fehl — und es entsteht eine irreführende „an ihn selbst gesendet"-Bestätigung. → Pattern: [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Flow-Save-Voraussetzung]]
- 🆕 **User-Onboarding-Checkliste:** (a) Aufnahme in Entra-Gruppe „Power Apps PL", (b) SharePoint-Speicherort-Berechtigung, (c) Bei Mitarbeitern eines Standorts: Baustellen-Freischaltung am Mandanten (Meggen / Emmen / Cham).
- 🆕 **Hybrid-Mitarbeiter** (selbständige Annahme + Rechnungsstellung an Kunden — z.B. Christoph Räber): brauchen identisches PDF/Mail-Setup wie PL.

## Onboarding-Log (User-Liste Stand Juni 2026)

| Datum | Aktion | User | Quelle |
|---|---|---|---|
| 06.2026 | + Richy Schön → PL-Gruppe | [[50.work/25_People/Richy-Schön\|Richy Schön]] | Remo 2026-06-01 |
| 06.2026 | + Jan Schwitter → PL-Gruppe | [[50.work/25_People/Jan-Schwitter\|Jan Schwitter]] | Remo 2026-06-01 |
| 06.2026 | – Reto Limacher → raus PL-Gruppe | [[50.work/25_People/Reto-Limacher\|Reto Limacher]] | Remo 2026-06-01 |
| 06.2026 | + Antonio De Finis → User, Baustellen Meggen pending | [[50.work/25_People/Antonio-De-Finis\|Antonio De Finis]] | Remo 2026-05-29 |
| 06.2026 | + Christoph Räber → SharePoint-Permission Fix | [[50.work/25_People/Christoph-Räber\|Christoph Räber]] | Remo 2026-06-03 |

## Bekannte Bugs / Resolutions

### Rapport Nr. 26-1039 — „an ihn selbst gesendet" (gelöst 06.2026)
- **Symptom:** Christoph Räber finalisierte Rapport am Laptop in PDF-Ansicht (Button „Beendet" rechts unten). Bestätigungsmeldung: „Rapport an ihn selbst gesendet".
- **Root Cause:** Christoph hatte zu dem Zeitpunkt **keine SharePoint-Berechtigung** auf den Ziel-Speicherort. Flow rechnete korrekt, PDF wurde generiert — Save-Step schlug fehl → daraus folgend kein Mail-Versand möglich → Bestätigung war falsch.
- **Fix:** Berechtigung nachgetragen. Rapport lief sauber durch.
- → Pattern dokumentiert: [[50.work/power-platform/sharepoint-berechtigung-flow-save]]

### PDF-Generation Manuel Schärli (05.2026, Stabilisierung)
- Symptom: „Heute Morgen hat es wieder nicht funktioniert" + keine Produktnamen (nur Menge/Einheit/Preis).
- Fix: Solution nochmals neu eingespielt, in eine konsistente Version gebracht.
- Stand 06.2026: stabil, abschließende Bestätigung von Manu ausstehend.

### Rizzo Isacco — Offline-Sync-Fehler (10.06.2026)
- **Symptom 1:** Banner „Fehler beim Abrufen von Daten aus dem Netzwerk" auf Home-Galerie.
  ![[regie-app-screenshots/2026-06-10_rizzo_netzwerk-fehler-home.png]]
- **Symptom 2:** Beim Löschen: „Netzwerkfehler bei Verwendung der Remove-Funktion: Fehler bei Regiekopf: code -2147093944 — You cannot delete this record because it doesn't exist in the offline mode".
  ![[regie-app-screenshots/2026-06-10_rizzo_remove-offline-fehler.png]]
- **Diagnose:** Offline-Sync-Drift. Power Apps Offline-Profil hat den zu löschenden Record nicht im Cache (Sync nicht durchgelaufen oder Record erst nach letztem Sync entstanden). Passt zu den im Review identifizierten K34 (Cascade-Delete im Client, nicht atomar) + K35 (Foto-Listen nicht offline-fähig).
- **Sofort-Massnahme (non-code):** App komplett schliessen → bei stabilem Netz neu öffnen → 30s Sync abwarten → Operation wiederholen. Remo direkt an Rizzo weiterleiten.
- **Hotfix (1–2h, code):** `IfError`-Wrap um Home-Delete-Block (`Home.pa.yaml` Zeilen 423–450) mit user-friendly Notification statt der kryptischen Default-Meldung.
- **Echter Fix (mittel):** K34 umsetzen — Dataverse-Beziehungen auf `CascadeDelete = Cascade` umstellen → atomarer Single-`Remove(Regiekopf, ThisItem)`.
- **Langfristig:** K35 — Fotos in Dataverse (`rrpt_foto` ist im Schema, ungenutzt) statt SharePoint.

## Offene Anforderungen / Backlog

### Kopierfunktion für Regie-Rapporte (Remo, 10.06.2026)
- **Use-Case:** Rapport 1:1 duplizieren, danach in der neuen Instanz anpassen (z.B. Folge-Auftrag, ähnliches Setup).
- **Priorität (Raoul, 11.06.2026):** Variante A zuerst (vor Wochentage-Plus / Variante B).
- **Konzept:** Icon-Button auf Home-Galerie-Item → Confirmation → Patch neuer Regiekopf (Status=Entwurf) → ForAll über Detail-Tabellen (Arbeitsbeschriebzeilen, Personenzeilen, Materialzeile).
- **Status:** Implementiert + lauffähig nach Disambiguation-Fix (siehe unten).

#### Was wird NICHT kopiert
- Status (immer Entwurf, vermeidet K15-Falle)
- Rapport-ID (neue Auto-Increment-Sequenz, Dataverse generiert)
- Unterschrift / Unterschreiber (rechtlich problematisch, werden im Abschluss-Screen neu erfasst)
- Fotos (SharePoint-Liste, datums-/situationsspezifisch)
- `Personentotal` / `Stunden Total` (Formel-Spalten — Dataverse berechnet automatisch)
- System-Felder (`createdon`, `createdby`, `modifiedon`, `modifiedby`)

#### Risiken-Mitigation
- K2 (Doppelklick) → `varDuplicating`-Lock am Anfang
- K15 (PL-Status direkt) → Hardcode auf `'Status (Regiekopf)'.Entwurf`
- Offline → `IfError`-Wrap mit user-friendly Notify

#### 🪲 Compiler-Falle: GUID/Table-Fehler bei ForAll auf Detail-Tabellen

Erster Code-Versuch warf "Ungültiger Argumenttyp (GUID). Stattdessen wird ein Table-Wert erwartet" auf den `ForAll(Filter(Detailtabelle; …))`-Blöcken.

**Ursache:** Schatten-Konflikt zwischen Datenquelle und 1:N-Navigation-Property. Vollständig dokumentiert in [[50.work/power-platform/powerfx-disambiguation-und-as-operator|PowerFx Disambiguation `[@…]` und `As`-Operator]].

**Fix:**
1. Datenquellen-Referenzen mit `[@TableName]` (z.B. `Patch([@Personenzeilen]; …)`)
2. Iteration-Variable mit `As src` benennen (`ForAll(varSource As src; …)`)
3. Master-side Navigation-Property statt Reverse-Lookup-Filter (`Master.Details` statt `Filter(Details; Master = X)`)

#### Schema-Mapping pro Detail-Tabelle (Stand 2026-06-11)

| Tabelle | Felder die kopiert werden | Bemerkung |
|---|---|---|
| `Regiekopf` (Master) | Baustellenbezeichnung, Baustellelookup, Kalenderwoche (=heute), Empfänger, 'Zuständiger PL Email', 'Zuständiger PL Name', 'Status (rrpt_status)' = Entwurf, Datum = Today(), Rapportnummer = Year(Today()), 'Erstellt Von Name' | Status hardcoded auf Entwurf |
| `Arbeitsbeschriebzeilen` | Regiekopf, 'Original Text', 'Übersetzter Text' | Falls weitere Spalten existieren — ergänzen |
| `Personenzeilen` | Regiekopf, Mitarbeiter, Mitarbeitertypen, Regieansatz, Mo, Di, Mi, Do, Fr, Sa, So | Personentotal + Stunden Total: NICHT (Formel-Spalten) |
| `Materialzeile` | Regiekopf, 'Material Name', Materialkatalog, Einheitspreis, Einheit, Menge, Bemerkung | Einheitspreis als Snapshot (Magaziner kann angepasst haben) |

#### Finaler funktionsfähiger Code

OnSelect von `btnDuplicate` (im Home-Galerie-Item):
```powerfx
If(varDuplicating;
    Notify("Duplikation läuft bereits …"; NotificationType.Warning);;
    Exit()
);;
Set(varDuplicating; true);;
Set(varConfirmDuplicateSource; ThisItem);;
Set(varShowDuplicateConfirm; true)
```

OnSelect von `btnConfirmDuplicateYes` (im Confirm-Dialog):
```powerfx
IfError(
    Set(varNewKopf;
        Patch([@Regiekopf]; Defaults([@Regiekopf]); {
            Baustellenbezeichnung: varConfirmDuplicateSource.Baustellenbezeichnung;
            Baustellelookup: varConfirmDuplicateSource.Baustellelookup;
            Kalenderwoche: Text(WeekNum(Today()));
            Empfänger: varConfirmDuplicateSource.Empfänger;
            'Zuständiger PL Email': varConfirmDuplicateSource.'Zuständiger PL Email';
            'Zuständiger PL Name': varConfirmDuplicateSource.'Zuständiger PL Name';
            'Status (rrpt_status)': 'Status (Regiekopf)'.Entwurf;
            Datum: Today();
            Rapportnummer: Year(Today());
            'Erstellt Von Name': varusername
        })
    );;
    ForAll(
        varConfirmDuplicateSource.Arbeitsbeschriebzeilen As src;
        Patch([@Arbeitsbeschriebzeilen]; Defaults([@Arbeitsbeschriebzeilen]); {
            Regiekopf: varNewKopf;
            'Original Text': src.'Original Text';
            'Übersetzter Text': src.'Übersetzter Text'
        })
    );;
    ForAll(
        varConfirmDuplicateSource.Personenzeilen As src;
        Patch([@Personenzeilen]; Defaults([@Personenzeilen]); {
            Regiekopf: varNewKopf;
            Mitarbeiter: src.Mitarbeiter;
            Mitarbeitertypen: src.Mitarbeitertypen;
            Regieansatz: src.Regieansatz;
            Mo: src.Mo;
            Di: src.Di;
            Mi: src.Mi;
            Do: src.Do;
            Fr: src.Fr;
            Sa: src.Sa;
            So: src.So
        })
    );;
    ForAll(
        varConfirmDuplicateSource.Materialzeile As src;
        Patch([@Materialzeile]; Defaults([@Materialzeile]); {
            Regiekopf: varNewKopf;
            'Material Name': src.'Material Name';
            Materialkatalog: src.Materialkatalog;
            Einheitspreis: src.Einheitspreis;
            Einheit: src.Einheit;
            Menge: src.Menge;
            Bemerkung: src.Bemerkung
        })
    );;
    Notify("Rapport dupliziert: " & varNewKopf.'MVM-Rapportnummer' &
           " · Fotos und Unterschrift wurden nicht mitkopiert.";
           NotificationType.Success);;
    Set(currentitem; varNewKopf);;
    Set(varShowDuplicateConfirm; false);;
    Set(varDuplicating; false);;
    Navigate(Personen; ScreenTransition.Fade);
    Notify("Duplizieren fehlgeschlagen — bitte mit Internet verbinden und erneut versuchen.";
           NotificationType.Error);;
    Set(varDuplicating; false);;
    Set(varShowDuplicateConfirm; false)
)
```

OnSelect von `btnConfirmDuplicateNo`:
```powerfx
Set(varShowDuplicateConfirm; false);;
Set(varDuplicating; false)
```

#### Lessons Learned (für nächste Master-Detail-Patches)
- **Immer `[@TableName]` verwenden**, wenn Datenquelle gleichzeitig als Navigation-Property eines im Scope sichtbaren Records existiert
- **`As src` setzen**, sobald der ForAll-Body Felder referenziert, die sowohl auf Source als auch auf Ziel-Tabelle existieren könnten
- **Navigation-Property bevorzugen** (`Master.Details`) vor reverse Lookup-Filter
- Diese drei Patterns kombiniert ergeben den robusten Code

#### 🐛 Mobile-Bug Inline-Edit-Modus (gefixt 11.06.2026)

Beim Erstes Mobile-Test sprang die Galerie bei Tap auf Copy-Button in den Edit-Modus (statt nur zu duplizieren). Auf Desktop kein Problem.

**Zwei Bug-Klassen trafen zusammen:**
1. **Mobile Touch-Propagation:** Edit-Button und Copy-Button waren in benachbarten Touch-Zonen → ein Tap feuerte beide OnSelect-Handler sequentiell. Auf Desktop pixel-genau, auf Mobile ±10px.
2. **`Navigate()` als terminaler Befehl:** Im Success-Pfad des Duplizier-Buttons stand `Set(visibleedit, Blank())` NACH `Navigate(Personen)` → wurde nie erreicht, `visibleedit` blieb auf der Source-Rapport-ID gesetzt → beim Re-Entry rendert das Item im Edit-Modus.

**Drei-Layer-Fix:**
1. **`Set(visibleedit, Blank())` als ALLERERSTE Zeile** im Copy-Button OnSelect (übersteuert von Touch-Propagation gesetzten Edit-Trigger)
2. **`Set(visibleedit, Blank())` VOR `Navigate(Personen)`** im Success-Branch des IfError (statt nach dem Navigate, wo es nicht erreicht wird)
3. **`Set(visibleedit, Blank())` in `Home.OnVisible`** als globaler Reset bei jedem Re-Entry (architektonischer Fix — alle anderen sind defensive Mitigationen)

Pattern-Notiz: [[50.work/power-platform/powerapps-navigate-bricht-onselect-cleanup|Navigate() bricht OnSelect-Cleanup + Mobile-Touch-Falle]].

> **Generalisierte Regel:** Jede State-Variable, die UI-Zustände in einem Screen steuert, muss im `OnVisible` des Screens zurückgesetzt werden. Sonst lecken State-Reste über Screen-Wechsel sobald irgendwo `Navigate()` nach einem `Set` steht. Gilt auch für K33 (`varSubmitting`) aus dem Schwachstellen-Review — gleiche Bug-Klasse.

> **Code in deutscher PowerFx-Syntax** (`;` / `;;`). Siehe [[50.work/power-platform/powerfx-deutsche-lokalisierung]].
> **Disambiguation-Pattern** im Detail: [[50.work/power-platform/powerfx-disambiguation-und-as-operator]].

### Wochentage + Datums-Plus bei Personen (Remo, 10.06.2026) — Variante B
- **Use-Case (Remo):** „EINE Arbeit, EINEN Regierapport" — Auftrag zieht sich über mehrere Datumsschienen.
- **Status:** Backlog. Erst nach Variante A umsetzen, ggf. nochmals mit Remo abstimmen.
- **Aufwand:** 3–4h (Schema-Erweiterung `rrpt_personenzeile` + UI Personen-Screen).

### Anzeige Alt-Rapporte in neuer App (Remo, 10.06.2026)
- **Frage von Remo:** Werden Rapporte aus der ALTEN App in der NEUEN angezeigt?
- **Antwort:** Nein. Neues Datenmodell (Dataverse `rrpt_Regiekopf`), Alt-Daten nicht migriert.
- **Empfehlung an Remo:** Alt-Rapporte bleiben in der alten App als Read-Only-Archiv. Keine Migration, kein gemischter Schema-Mix.

> **Wichtig für alle Code-Snippets in diesem Projekt:** **deutsche PowerFx-Syntax** (`;` Parameter-Trenner, `;;` Statement-Chain). Siehe [[50.work/power-platform/powerfx-deutsche-lokalisierung]].

## Persönliche Notizen

_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._

## Verwandt

- [[_Index|Projekt-Index]]
- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]