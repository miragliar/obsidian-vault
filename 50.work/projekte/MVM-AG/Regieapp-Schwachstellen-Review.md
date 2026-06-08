---
name: Regie-Rapport-App Schwachstellen-Review
slug: Regieapp-Schwachstellen-Review
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
parent: "[[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regieapp-Neubau-MVM]]"
status: Review
review_datum: 2026-06-08
review_objekt: RegieRapportProzess_1_0_0_23_managed.zip
type: code-review
tags: [miraglia, mvm-ag, power-apps, dataverse, schwachstellen, audit]
created: 2026-06-08
updated: 2026-06-08
---

# Regie-Rapport-App — Proaktive Schwachstellen-Analyse

**Solution:** RegieRapportProzess 1.0.0.23 (managed)
**Reviewer:** Claudian
**Review-Datum:** 2026-06-08
**Status:** App läuft in Produktion. Ziel des Reviews: Probleme vor Schadensfall identifizieren — anders als im Subunternehmer-Prozess.

> **Reviewer-Hinweis:** Ich habe nur Befunde aufgenommen, die ich konkret im Code/Schema verifizieren konnte. Jede Stelle ist mit Datei + Zeilen-Referenz belegt. Wenn ein Befund "potenziell" ist, ist das ausdrücklich markiert.

---

## Executive Summary

Die App ist insgesamt sauber strukturiert (Master-Detail mit Dataverse, sinnvolles Rollen-Schema, Environment Variables für Sandbox/Prod). Es gibt **eine Klasse von Schwachstellen, die in Summe das größte Risiko darstellen**: stille Inkonsistenz zwischen App-Status und tatsächlich generiertem Output. Konkret:

1. **Fire-and-forget bei den PDF/Excel-Flows** kombiniert mit **vorgezogenem Status-Patch** ⇒ Rapporte gelten als "abgeschlossen", obwohl PDF/Mail nie ankommen.
2. **Foto-Löschen in Produktion verwendet die falsche SharePoint-Liste** ⇒ entweder stille Fehler oder Bilder werden aus Sandbox gelöscht.
3. **O365-Gruppe und Dataverse-Rollen nicht gekoppelt** ⇒ derselbe Fehler-Mechanismus wie beim Subunternehmer-Prozess (Privilege-Drift).

Daneben: einige Validierungslücken (leere Unterschrift, leere Empfänger), hardcoded Personenbezüge (Räber, Chef-Mails), keine Idempotenz bei Doppelklicks.

**Empfehlung:** P1-Punkte (K1, K4, K5, K9) zeitnah angehen — die haben das Potenzial, Schaden zu verursachen, bevor jemand merkt, dass etwas fehlt.

---

## Schweregrade

- **P1 — Schadens-Potenzial (still):** Schaden tritt auf, ohne dass User/Admin es zwingend bemerkt. Höchste Priorität.
- **P2 — Schadens-Potenzial (sichtbar):** Schaden tritt auf, ist aber für Endnutzer sichtbar (Fehlermeldung, leere Liste). Mittel.
- **P3 — Robustheit/Hygiene:** Kein direkter Schaden, aber Wartbarkeit/Skalierung leidet.

---

## P1 — Stille Inkonsistenzen / Datenverlust

### K1 — Foto-Löschen verwendet in Produktion die falsche SharePoint-Liste

**Datei:** `CanvasApps/.../Src/Fotos.pa.yaml`
**Zeilen:** 195, 277–294

Items-Anzeige wechselt korrekt:
```powerfx
Items: =Filter(If(varenv = "Sandbox",'Regie-Bilder','Regie-Bilder_1'),
              Rapport_x002d_ID = currentitem.'Rapport-ID')
```

Aber das Löschen ist **hartcodiert** auf die Sandbox-Liste:
```powerfx
Remove('Regie-Bilder', selectedRecord_SP);
If(IsEmpty(Errors('Regie-Bilder', selectedRecord_SP)), ...
```

**Auswirkung in Prod (`varenv != "Sandbox"`):**
- Der `Remove` läuft gegen `'Regie-Bilder'` (Sandbox). `selectedRecord_SP` zeigt aber auf einen Datensatz aus `'Regie-Bilder_1'` (Prod). Das ist ein **Cross-List-Operation** → in der Regel still scheiternd (oder im schlimmsten Fall: ein Sandbox-Datensatz mit zufällig gleicher ID wird gelöscht).
- Die `IsEmpty(Errors(...))`-Prüfung läuft auch gegen die Sandbox-Liste. Wenn dort nichts passiert, wird `isItemSelected: false` gesetzt — also alles wirkt UI-seitig wie ein Erfolg.

**Fix:** `If(varenv = "Sandbox", 'Regie-Bilder', 'Regie-Bilder_1')` analog zum Items-Pattern. Besser: in eine Sammlung/Variable `colFotosSource` einmalig in App.OnStart auflösen und überall referenzieren.

---

### K4 — PDF/Excel-Flows antworten **vor** der Verarbeitung (fire-and-forget)

**Datei:** `Workflows/02_V2-rrpt-PDFGenerierung-...json` Zeilen 1548–1564 und `03_V2-rrpt-XLSXGenerierung-...json` Zeilen 147–163

Beide Flows haben die "Response"-Action mit **leerem `runAfter: {}`**:
```json
"Auf_eine_Power_App_oder_einen_Flow_reagieren": {
  "type": "Response",
  "kind": "PowerApp",
  "inputs": { ..., "statusCode": 200, "body": {} },
  "runAfter": {}
}
```

Das ist absichtlich "fire-and-forget". Vorteil: User wartet nicht 30s. Nachteil: **Wenn der Flow später scheitert (PDF4Me down, Word-Template fehlt, SharePoint-Berechtigung weg), erfährt der User es nicht**.

Konkrete Fehler-Quellen im PDF-Flow ohne `Configure run after`:
- `Microsoft_Word-Vorlage_auffüllen_-_Emmen` (Drive-ID `b!v9qW6riscUaRL3WR_QCEhJuDGfXR11NCgGtVrzVDJSS5vmLXnL62So-d0F3k5qlG` hartcodiert)
- `Word-Dokument_in_PDF_konvertieren`
- `HTML_in_PDF_konvertieren` und `Merge_V1` (PDF4me — externer Dienstleister)
- `Datei_oder_Bild_herunterladen` (Unterschrift)

**Auswirkung:** kein Output, kein Mail an PL, kein Alert. Rapport ist nach K5 trotzdem auf Status "PDF".

**Fix:**
1. Globalen `Try/Catch/Finally`-Scope (Power Automate "Scope" mit `runAfter: Failed/Skipped/TimedOut`) um die Hauptlogik.
2. Im Catch-Scope: Notification an `MailPL` oder Admin: "Generierung Rapport X fehlgeschlagen — Status zurück auf PL".
3. Im Catch-Scope: Status zurück auf "PL" patchen, damit der Rapport in der Home-Galerie wieder auftaucht.

---

### K5 — Status wird auf "PDF" gesetzt, bevor der Flow tatsächlich erfolgreich war

**Datei:** `Src/PDF Editierung.pa.yaml` Zeilen 348–360

```powerfx
'02_V2-rrpt-PDFGenerierung'.Run(
    currentitem.Regiekopf,
    currentitem.Baustellelookup.Baustelle,
    LookUp(Arbeitsbeschriebzeilen, Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID').Arbeitsbeschriebzeilen
);
Notify("Rapport " & currentitem.'MVM-Rapportnummer' & " wird ... versendet", Success);
Patch(Regiekopf, currentitem, {'Status (rrpt_status)': 'Status (Regiekopf)'.PDF})
```

Da der Flow per K4 sofort zurückkommt, ist die `.Run()`-Zeile praktisch sofort fertig. Der nächste Patch setzt Status auf "PDF" — **immer**, auch wenn der Flow später scheitert.

**Folge (zusammen mit K4):**
- Home-Galerie filtert PL/PDF nach `'Zuständiger PL Email' = varcurrentuser` — Rapport bleibt sichtbar, aber als PDF "fertig"
- Beim Archivieren rutscht er weg, weil kein Mensch nach PDF-Status sucht
- Niemand weiß: PDF wurde nie generiert/verschickt

**Fix:** Status-Patch in den Flow verlagern (am Ende, im Success-Path). App nur "Wird gerade generiert" anzeigen, kein Status-Wechsel im Client.

---

### K9 — O365-Gruppe und Dataverse-Sicherheitsrolle nicht gekoppelt (gleiches Pattern wie Subunternehmer-Prozess)

**App-Seite:** `Src/App.pa.yaml` Zeile 59–62 + 124–133
```powerfx
ClearCollect(colsecurity,
    'Office365-Gruppen'.ListGroupMembers("2effe64a-6339-4c83-bfef-663590883137").value
);
If(varcurrentuser in colsecurity.mail Or ...,
    Set(varwer, "PL"), Set(varwer, "MA"))
```

**Dataverse-Seite:** `customizations.xml` (Rolle `RRPT_MA`):
- `prvReadrrpt_Regiekopf` Level=**Basic**
- `prvReadrrpt_Personenzeilen` Level=**Basic**
- `prvReadrrpt_Materialzeile` Level=**Basic**

**Rolle `RRPT_PL`:** alle relevanten Privileges auf **Global**.

**Problem:** Es gibt keinen automatischen Mechanismus, der die Mitgliedschaft in der O365-Gruppe `Power Apps PL` mit der Zuweisung der Dataverse-Rolle `RRPT_PL` synchronisiert.

**Szenario A (neuer PL):**
- User wird in O365-Gruppe aufgenommen, aber RRPT_PL nicht gegeben
- App: `varMAtyp = "PL"` ⇒ Home-Filter `'Status' = PL And 'Zuständiger PL Email' = varcurrentuser`
- Dataverse: User hat nur RRPT_MA (Basic Read) ⇒ sieht nur eigene Records
- Records sind aber im Eigentum der MA, die sie erstellt haben
- ⇒ **Galerie ist leer. PL denkt, die App funktioniert nicht.**

**Szenario B (PL verlässt Gruppe):**
- User wird aus O365 entfernt, aber RRPT_PL bleibt
- App behandelt ihn als MA
- Er sieht aber dank Dataverse weiterhin alles
- ⇒ Datenschutz-Issue: ehemaliger PL kann immer noch Rapporte und Kostendaten lesen

**Fix:**
- Entweder: PL-Erkennung NUR über Dataverse-Rolle (`User().Roles in `RRPT_PL``) — aber Power Fx hat das nicht direkt
- Oder: Onboarding-Checkliste/Automatisierung, die O365-Gruppe + Dataverse-Rolle gleichzeitig setzt
- Pragmatisch: bei App-Start eine Lookup-Tabelle `rrpt_pl_assignments` mit allen aktiven PL prüfen — ein Ort der Wahrheit, ein Trigger der die O365-Gruppe und die Dataverse-Rolle setzt

> Genau das war beim Subunternehmer-Prozess der Fehler-Mechanismus: zwei Wahrheits-Quellen, eine wird gepflegt, die andere nicht.

---

### K6 — PDF wird ohne Unterschrift generiert, wenn Unterschriftsfeld leer ist

**Datei:** `Workflows/02_V2-rrpt-PDFGenerierung-...json` Zeile 437–474

```json
"Datei_oder_Bild_herunterladen": {
  "type": "OpenApiConnection",
  "inputs": { ..., "fileImageFieldName": "cr19a_unterschrift" }
}
```
Wenn das Feld leer ist, gibt der Connector entweder einen Fehler (ganzer Flow bricht, siehe K4) oder leeren Content zurück. Die `Compose`-Action danach setzt `image/png` mit leerem `$content` — Word-Template rendert ein leeres Bild.

**App-Seite:** Im Abschluss-Screen (Zeilen 278–293) ist die Validierung kosmetisch:
```powerfx
TextInput6 (Unterschreiber):
  Fill: =If(IsBlank(Self.Text), RGBA(255, 184, 174, 1), Color.Transparent)
```
Nur rote Hintergrundfarbe — kein `Disabled` am Submit-Button, keine harte Validierung.

`PenInput1` (Unterschrift selbst) hat überhaupt keine Sichtkontrolle.

**Fix:** Submit-Button mit:
```powerfx
DisplayMode: =If(
    IsBlank(TextInput6.Text) Or IsBlank(PenInput1.Image),
    DisplayMode.Disabled,
    DisplayMode.Edit
)
```

---

### K15 — PL-Eigene Rapporte überspringen den Abschluss-Workflow

**Datei:** `Src/Home.pa.yaml` Zeile 657–675

Beim Anlegen eines neuen Regiekopfs:
```powerfx
'Status (rrpt_status)': If(
    varMAtyp = "PL",
    'Status (Regiekopf)'.PL,           // direkt auf PL
    'Status (Regiekopf)'.Entwurf
)
```

Wenn ein PL selbst einen Rapport erstellt, startet er direkt im Status "PL" — **damit kommt er nie auf den Abschluss-Screen**, wo Unterschrift und Unterschreiber eingegeben werden. PDF wird dann ohne Unterschrift gerendert (siehe K6).

**Fix:** Auch PL-Eigene Rapporte müssen den Abschluss-Workflow durchlaufen, ODER der PDF-Flow muss vor Rendering prüfen, ob Unterschrift vorhanden ist, und gegebenenfalls einen anderen Template-Pfad nehmen ("PL-intern, ohne Unterschrift").

---

### K22 — `Visible=false`-DataCard mit `Update: =currentitem` ist ein Trojaner

**Datei:** `Src/Personen.pa.yaml` Zeilen 1094–1108 (Regiekopf_DataCard1), gleiches Pattern in Material/Arbeitsbeschrieb

```yaml
- Regiekopf_DataCard1:
    Properties:
      Update: =currentitem
      Visible: =false
```

Das versteckte Feld pusht `currentitem` bei jedem SubmitForm in den Fremdschlüssel `rrpt_Regiekopf`. Solange `currentitem` korrekt gesetzt ist, funktioniert das. **Aber:**

- Wenn der User durch direkten Navigate (z.B. von Archiv-Screen mit `Set(currentitem, ThisItem)`, dann zurück, dann andere Aktion) `currentitem` "vergessen" wird, kann der nächste Submit eine Personenzeile mit dem **letzten currentitem** speichern — also unter dem falschen Rapport.
- Wenn `currentitem` Blank wird (z.B. nach Cancel auf Abschluss-Screen, Zeile 317: `Set(currentitem, Blank())`), wird `Update: =currentitem` → Blank ⇒ Orphan-Datensatz ohne Fremdschlüssel.

**Verifiziert:** Im `Abschluss-Screen` (Zeile 317) wird `currentitem` tatsächlich auf Blank() gesetzt. Wenn der User danach direkt einen anderen Rapport öffnet ohne über Home zu navigieren (theoretisch über bestimmte Pfade möglich), kann es zu Mismatches kommen.

**Fix:** Hidden-DataCard mit Fail-Safe: `Update: =If(IsBlank(currentitem), ThisItem.Regiekopf, currentitem)` oder Submit hard-blocken wenn `IsBlank(currentitem)`.

---

### K24 — NotifyPL: ungültige ID führt zu E-Mail an leere Adresse

**Datei:** `Workflows/01-rrpt-NotifyPL-...json`

Flow:
1. `Zeile_nach_ID_abrufen` (GetItem)
2. `Variable_festlegen MailPL = @outputs('Zeile_nach_ID_abrufen')?['body/rrpt_zustandigerplemail']`
3. `E-Mail_senden_(V2) To: @variables('MailPL')`

Wenn `triggerBody().text` keine gültige GUID ist oder GetItem nichts findet, ist `body` `null`, `MailPL` ist leer, E-Mail wird an leere Adresse gesendet → Connector wirft Fehler → Flow auf "Failed".

**Aber:** Im `Abschluss-Screen` (Zeile 334–346) ruft die App den Flow und zeigt **immer** `Notify("Wird an PL gesendet", Success)`. Der User glaubt, alles ist gut.

**Fix:** `If(IsBlank(MailPL), Terminate Failed mit Notification an Admin)`. App-seitig: nicht fire-and-forget, sondern Response prüfen.

---

### K31 — Auto-Empfänger-Logik kann leeren Empfänger schreiben

**Datei:** `Src/Home.pa.yaml` Zeilen 577–625

```powerfx
varempfängercheck_1: Filter(Regiekopf, Baustellenbezeichnung = ... And Kalenderwoche = ...);
colempfängerfinal: Filter(colempfänger_kunde, Not(Value in varempfängercheck_2));
varempfänger: First(colempfängerfinal).Value
```

**Edge Case:** Wenn alle 20 vordefinierten "Kunde-Rapport 1..20" bereits für diese Baustelle+KW belegt sind:
- `colempfängerfinal` ist leer
- `First(colempfängerfinal).Value` ist **Blank()**
- Patch erstellt Regiekopf mit `Empfänger: Blank()` (kein Schutz)

**Zweiter Edge Case:** Wenn DropDown "Freitext" gewählt, aber `TextInput3.Text` leer:
- `varempfänger: TextInput3.Text` = Blank()
- Patch akzeptiert Blank.

**Fix:** Vor dem Patch:
```powerfx
If(IsBlank(varempfänger),
    Notify("Empfänger fehlt", Error); Exit,
    Patch(...)
)
```
Oder: Submit-Button erst aktivieren, wenn Empfänger nicht blank ist.

---

### K33 — Patch auf "Weiter" ohne Pflichtfeld-Validierung

**Datei:** `Src/Home.pa.yaml` Zeile 569–687 (EmpfängerFreitext-Button)

Der "Weiter"-Button erstellt einen neuen Regiekopf, **ohne zu prüfen ob**:
- `Baustellenauswahl.Selected` gesetzt ist
- `TextInput2.Text` (KW) ein gültiges Format hat
- `TextInput2_1.Text` (bei Kleinauftrag) gefüllt ist

Konsequenz: User klickt "Weiter" mit leeren Feldern → leerer Regiekopf in der DB, kein Fehler sichtbar (varempfänger evtl. Blank → siehe K31).

**Fix:** Button-Disabled-Condition oder harte If-Prüfung in OnSelect.

---

### K34 — Cascade-Delete im Client (keine Atomarität)

**Datei:** `Src/Home.pa.yaml` Zeilen 430–447

```powerfx
RemoveIf(Materialzeile, Regiekopf.'Rapport-ID' = ThisItem.'Rapport-ID');
RemoveIf(Personenzeilen, Regiekopf.'Rapport-ID' = ThisItem.'Rapport-ID');
RemoveIf(Arbeitsbeschriebzeilen, Regiekopf.'Rapport-ID' = ThisItem.'Rapport-ID');
Remove(Regiekopf, ThisItem)
```

Vier separate Calls. Wenn das Netz zwischendurch wegbricht (User auf Baustelle!), bleiben Orphans. Die Dataverse-Beziehungen sind in der customizations.xml als `ReferentialRestrict` / Standard, **nicht** als Cascade konfiguriert (Standard für 1:N-Lookups).

**Fix:** In Dataverse das `CascadeDelete = Cascade` auf der `rrpt_Regiekopf → rrpt_Personenzeilen/Materialzeile/Arbeitsbeschriebzeilen`-Beziehung setzen. Dann reicht im Client `Remove(Regiekopf, ThisItem)`.

---

## P2 — Sichtbare Schwachstellen / UX-Risiken

### K2 — Doppelter Klick auf "Weiter" → doppelte Regiekopf-Datensätze

**Datei:** `Src/Home.pa.yaml` Zeile 569 (EmpfängerFreitext-Button)

`OnSelect` macht Lookups, dann Patch, dann `Set(visiblenew, false); Navigate(Personen)`. Solange der Patch läuft, ist der Button noch klickbar. Ein hektischer User (mobile, schlechtes Netz) kann zweimal tippen.

**Fix:** `DisplayMode: =If(IsBlank(currentitem) Or visiblenew, DisplayMode.Edit, DisplayMode.Disabled)`, oder einen Lock-Boolean (`Set(varSubmitting, true)`) am Anfang setzen, am Ende zurück.

Gleiches Pattern in `Abschluss-Screen` Submit, `PDF Editierung` "Ablegen und Senden".

---

### K3 — Räber-Spezialfall hartcodiert mit personalisierter E-Mail/Name

**Datei:** `Src/App.pa.yaml` Zeilen 134–140 + `Src/Home.pa.yaml` Zeilen 626–653

```powerfx
ClearCollect(colräber, [126304, 225104]);
...
If(LookUp(Baustelle, ...).Baustellennummer in colräber,
    Set(varprojektleiter, "mvmcr@mvm-ag.ch"),
    Set(varprojektleiter, Baustellenauswahl.Selected.'Zuständiger PL Email'));
If(... in colräber,
    Set(varprojektleitername, "Christoph Räber"),
    Set(varprojektleitername, LookUp(colsecurity, varprojektleiter = mail Or ...).displayName));
```

**Probleme:**
1. Wenn Räber die Firma verlässt → App-Release nötig
2. Wenn neue Räber-Baustellen dazukommen → Baustellennummer in den Code aufnehmen → App-Release
3. `LookUp(colsecurity, ...).displayName` kann Blank() sein, wenn der zuständige PL nicht in der "Power Apps PL"-Gruppe ist (z.B. neu, noch nicht aufgenommen) → Name ist Blank → PDF und E-Mail haben leere PL-Namen

**Fix:** Statt der hartcodierten Liste eine Boolean-Spalte `cr19a_haupterantwortlich_pl` an `rrpt_Baustelle` ergänzen, die für die zwei Baustellen ein anderer PL-Override sein kann (oder direkt das `'Zuständiger PL Email'`-Feld der Baustelle pflegen).

---

### K16 — Chef-E-Mails hartcodiert (`colchef`)

**Datei:** `Src/App.pa.yaml` Zeilen 50–57
```powerfx
ClearCollect(colchef, [
    "powerplatform@mvm-ag.ch",
    "r.pfister@mvm-ag.ch",
    "mvmrp@mvm-ag.ch"
]);
```

Personalwechsel ⇒ App-Release.

**Fix:** Dataverse-Lookup-Tabelle `rrpt_appbenutzer_rolle` mit Spalte `rolle = "Chef" | "PL" | "MA"` und Email.

---

### K12 — `'Erstellt Von Name'` als String-Snapshot

**Datei:** `Src/Home.pa.yaml` Zeile 678
```powerfx
'Erstellt Von Name': varusername  // = User().FullName
```

Snapshot. Bei Namensänderung (Heirat, etc.) bleibt der alte Name. Außerdem: `createdby` (Standard-Dataverse-Lookup) ist sowieso schon befüllt — Doppel-Daten.

**Fix:** Felder entfernen. In Flow/Report `_createdby_value` Lookup-Daten verwenden.

---

### K17 — Archivieren ohne Bestätigung

**Datei:** `Src/Home.pa.yaml` Zeilen 299–311

Ein Klick auf das Geschichts-Icon (sieht aus wie ein History/Archivieren-Knopf), und der Rapport ist sofort weg:
```powerfx
OnSelect: =Patch(Regiekopf, ThisItem, {'Status (rrpt_status)': 'Status (Regiekopf)'.Archiviert})
```

In Material/Personen/Fotos gibt es einen `DeleteConfirmDialogContainer`. Hier nicht.

**Fix:** Confirmation-Dialog oder mindestens `Notify("Archiviert", Success)` mit `Undo`-Aktion.

---

### K20 — Delete-Button im Home ohne Bestätigung

**Datei:** `Src/Home.pa.yaml` Zeilen 423–450 (ButtonCanvas3_4)

Selbe Geschichte: roter Delete-Button löscht Regiekopf inkl. aller Lines mit einem Klick. Während andere Screens Confirmations haben.

**Fix:** Confirmation analog Personen-Screen einbauen.

---

### K14 — Translator-API ohne Error Handling, Original-Text wird beim Edit überschrieben

**Datei:** `Src/Arbeitsbeschrieb.pa.yaml` Zeilen 188–230

```powerfx
If(MicrosoftTranslatorV2.Detect(TextInput4.Text).Code <> "de",
   Set(übersetzt, MicrosoftTranslatorV2.Translate("de", TextInput4.Text));
   Patch(Übersetzungstabelle, Defaults(...), {Originaltext: TextInput4.Text, Übersetzung: übersetzt, ...}),
   Set(übersetzt, TextInput4.Text)
);
If(IsBlank(arbeitsbeschriebvar),
   Patch(Arbeitsbeschriebzeilen, Defaults(...), {'Original Text': übersetzt, Regiekopf: currentitem}),
   Patch(Arbeitsbeschriebzeilen, arbeitsbeschriebvar,
         {'Original Text': übersetzt, 'Übersetzter Text': übersetzt})  // ← Bug
)
```

**Bug:** Beim **zweiten** Speichern (Edit) wird:
- `'Original Text'` auf die Übersetzung gesetzt
- `'Übersetzter Text'` auf dieselbe Übersetzung

Damit ist der wirklich-original eingegebene Text nach dem ersten Edit **verloren**. Bei mehrfachem Edit verschiebt sich der Sinn potenziell.

**Zusätzlich:** `Detect()` ohne Try/Catch — bei API-Ausfall stürzt der Save ab.

**Fix:**
- Edit-Pfad: `'Original Text': TextInput4.Text` (nicht `übersetzt`)
- Try/Catch um Translator-Calls, oder vorher prüfen ob TextInput4.Text > 5 Zeichen

---

### K7 — Keine Validierung im Abschluss-Screen vor Submit

**Datei:** `Src/Abschluss-Screen.pa.yaml` Zeilen 319–346

Der Submit-Button hat keine Pflichtfeld-Prüfung. User kann:
- Unterschreiber-Feld leer lassen
- PenInput leer lassen
- Keine Personenzeilen erfasst haben

⇒ alles wird trotzdem als "PL" eingereicht und Mail wird verschickt.

**Fix:** Disabled-Logic kombinieren mit K6 (Unterschrift) und zusätzlich:
```powerfx
DisplayMode: =If(
    IsBlank(TextInput6.Text) Or
    IsBlank(PenInput1.Image) Or
    CountRows(Filter(Personenzeilen, Regiekopf.'Rapport-ID' = currentitem.'Rapport-ID')) = 0,
    DisplayMode.Disabled, DisplayMode.Edit
)
```

---

### K10 — XLSX-Flow liest das Template hartcodiert aus der Sandbox-Site

**Datei:** `Workflows/03_V2-rrpt-XLSXGenerierung-...json` Zeile 862
```json
"Datei_kopieren": {
  "inputs": {
    "parameters": {
      "dataset": "https://mvmag.sharepoint.com/sites/MVMProzesseSandbox",
      "parameters/sourceFileId": "%252fFreigegebene%2bDokumente%252f01_Vorlagen%252fRapport-Zusammenfassung.xlsx",
      ...
    }
  }
}
```

Der PDF-Flow nutzt die Environment Variable `rrpt_SharepointSite` — der XLSX-Flow **nicht**. Wenn die Sandbox-Site umbenannt/abgeschaltet wird, bricht die Excel-Generierung in Prod.

**Fix:** Die `dataset` durch `@parameters('Sharepoint Site (rrpt_SharepointSite)')` ersetzen. Templates müssen in beiden Sites liegen (oder via Env Var direkt umgeschaltet werden).

---

### K18 — Excel-Flow: 1-Minuten-Hardcoded-Verzögerung

**Datei:** `03_V2-rrpt-XLSXGenerierung-...json` Zeilen 952–959
```json
"Verzögerung": {
  "type": "Wait",
  "inputs": { "interval": { "count": 1, "unit": "Minute" } }
}
```

Warten 1 Minute, damit Excel Online die `AddRowV2`-Calls committed hat, bevor die Datei runtergeladen wird. Bei wenig Daten = unnötige Wartezeit. Bei vielen Rapporten (Chef erstellt z.B. Quartals-Übersicht über 200 Rapporte) reicht 1 Minute potenziell nicht ⇒ Excel-Mail enthält teilweise leere Tabelle.

**Fix:** Statt `Wait` → "Get worksheet" oder "List rows" als Pseudo-Sync. Oder Polling-Loop "until rows in Excel == rows expected".

---

### K23 — `Combobox2.OnChange` (PDF Editierung) ohne Error Handling

**Datei:** `Src/PDF Editierung.pa.yaml` Zeilen 49–58

```powerfx
OnChange: |
    =Patch(Personenzeilen, ThisItem,
        {Regieansatz: LookUp(Mitarbeitertypen, Bezeichnung = Self.Selected.Bezeichnung).Regieansatz,
         Mitarbeiter: Self.Selected.Bezeichnung,
         Mitarbeitertypen: Self.Selected});
```

Wenn der Patch fehlschlägt (Berechtigung, Validation), wird der User nicht benachrichtigt. Die Combobox zeigt aber den neuen Wert. ⇒ stille Diskrepanz zwischen UI und DB.

**Fix:** `IfError`-Wrap mit `Notify("Speichern fehlgeschlagen", Error)`.

---

### K25 — `currentitem.Regiekopf` als Parameter — unklare Semantik

**Datei:** `Src/Abschluss-Screen.pa.yaml` Zeile 336 und `PDF Editierung.pa.yaml` Zeile 350

```powerfx
'01-rrpt-NotifyPL'.Run(currentitem.Regiekopf)
'02_V2-rrpt-PDFGenerierung'.Run(currentitem.Regiekopf, ...)
```

`currentitem` IS ein Regiekopf-Record. `currentitem.Regiekopf` ist ein bisschen kryptisch — vermutlich ein "primary key"-Alias (Power Apps Standard für Lookup auf sich selbst), der die GUID liefert. Falls Schema sich ändert oder Power Apps das Verhalten umstellt, kann das brechen.

**Fix:** Explizit `currentitem.'Rapport-ID'` (wenn das der Schlüssel ist, den der Flow erwartet) oder die GUID direkt: `GUID(currentitem.'Regiekopf')` mit klarem Code-Kommentar.

> Der Flow erwartet `triggerBody()['text']` als Record-ID für `GetItem`. `GetItem` braucht die GUID (`rrpt_regiekopfid`). Aktuell scheint die Übergabe zu funktionieren — aber das ist **implicit** und sollte explicit gemacht werden.

---

### K28 — `PenInput.Image` direkt in Patch — potenziell sehr groß

**Datei:** `Src/Abschluss-Screen.pa.yaml` Zeile 332

```powerfx
{Unterschrift: PenInput1.Image}
```

`PenInput.Image` ist eine PNG-Base64-URI. Bei langer Sitzung oder hohem Pixelinhalt kann das mehrere MB groß sein. Dataverse Image-Feld `cr19a_unterschrift` hat `MaxLength=9437328` (~9MB) — generös, aber nicht unbegrenzt.

Bei mehrfachem Unterschreiben (User zeichnet → unzufrieden → erneut) wird das aktuelle Bild beim Patch hochgeladen. Bei wirklich langsamen Netzverbindungen (Baustelle) blockiert das den Submit.

**Fix:** Vorher `Resize(PenInput1.Image, 600, 200, ImageType.Png)` oder via Picture-Komprimierung verkleinern. Limit dokumentieren.

---

### K27 — Kein Lock auf Regiekopf während PDF-Generierung läuft

**Datei:** `Src/PDF Editierung.pa.yaml`

Wenn PL "Ablegen und Senden" drückt, läuft der Flow async (siehe K4). Währenddessen kann derselbe oder anderer PL/Chef die Lines weiterbearbeiten — der Flow rendert dann mit aktuellem oder veraltetem Stand, je nachdem wann er die `ListRecords` ausführt.

**Fix:** Status sofort auf "PDF in Generierung" patchen (eigener Status oder ein `cr19a_genlock = true` Feld). UI zeigt dann "in Bearbeitung — Edit gesperrt". Flow setzt am Ende den Lock zurück.

---

## P3 — Robustheit / Best Practice / Skalierung

### K8 — ForAll mit Patch über `GalleryX.AllItems`

**Dateien:** `Src/PDF Editierung.pa.yaml` Zeilen 455–510 (Personenzeilen) und 545–566 (Materialzeile)

AppChecker meldet `app-ForAllWithMutation` (2x) und `app-CountRowsGalleryAllItems` (2x). `ForAll(... GalleryX.AllItems ...)` arbeitet client-seitig — bei >2000 Records nicht delegiert. Aktuell unproblematisch (Reports klein), aber Skalierungs-Falle.

**Fix:** Auf Galerie-Ebene direkt Patch-on-Change (sobald User editiert) statt globaler Save-Button. Oder direkt mit Form-Pattern (wie Personen-Screen) statt PDF-Editierung-Variante mit eigener Edit-Logik.

---

### K11 — Auto-Increment ohne Jahres-Reset

**Schema:** `cr19a_autoincrementrapportnummer` mit `<AutoNumberFormat>{SEQNUM:4}</AutoNumberFormat>` + Formel `Right(Text(rrpt_rapportnummer,"0000"),2) & "-" & Text(cr19a_autoincrementrapportnummer)`

Probleme:
1. Nach 9999 Rapporten wird die Zahl 5-stellig: `26-10000`. Funktioniert (Format ist Text), wirkt aber unsauber.
2. Bei Jahreswechsel resettet die Sequenz nicht: `26-9000` (Dezember) → `27-9001` (Januar). Konsistent, aber ein neuer Mitarbeiter wundert sich vielleicht: "Wieso starten 2027er Rapporte bei 9001?"

**Fix (optional):** Sequence per Jahr in Code lösen — `cr19a_jahressequenz = CountIf(Regiekopf, Year('Datum') = Year(Today())) + 1`. Aber Vorsicht: das ist nicht atomar.

---

### K19 — `ClearCollect(materialvar, Filter(Materialkatalog, Or(KST = 61, KST = 62) And Regieapp = "x"))`

**Datei:** `Src/App.pa.yaml` Zeilen 63–72

AppChecker: 7x `app-CollectingReadOnlyTable`. ClearCollect auf read-only Dataverse-Tabelle ist OK für Cache, aber:
1. `Regieapp = "x"` als Boolean-Flag (`"x"` als String) ist ein Anti-Pattern → besser eine Boolean-Spalte `cr19a_regieapp_aktiv`.
2. Cache wird nur bei App-Start aktualisiert. Admin fügt während User-Session ein neues Material hinzu → User sieht es erst nach Neustart.

**Fix:** `Refresh(Materialkatalog)` zusätzlich auf einen "Neu"-Button. Long-term: Boolean-Spalte statt "x".

---

### K30 — Smartphone-Erkennung nur bei OnStart

**Datei:** `Src/App.pa.yaml` Zeilen 23–33

```powerfx
If(App.Width < 600, Set(varsmartphone, true), Set(varsmartphone, false))
```

Bei OnStart einmalig. Bei Display-Drehung oder Wechsel auf Tablet wird nicht neu evaluiert.

**Fix:** Statt Variable direkt `App.Width < 600` in den Sichtbarkeits-Properties verwenden, oder einen Timer/OnAppResume.

---

### K35 — `app-NotOfflineEnabledTable`

AppChecker meldet, dass eine Datenquelle nicht offline-fähig ist. Vermutlich die SharePoint-Listen `Regie-Bilder`/`Regie-Bilder_1`. Power Apps Offline-Profile unterstützen primär Dataverse — SharePoint Lists sind eingeschränkt.

**Folge:** Fotos können offline NICHT erfasst werden. Der MA auf der Baustelle ohne Netz kann zwar Personenzeilen/Material erfassen, aber keine Bilder.

**Fix (langfristig):** Bilder in Dataverse-File-Field (`rrpt_foto`-Tabelle ist bereits in der Solution deployed, aber leer/ungenutzt — siehe B1). Migration: SharePoint → Dataverse, Offline-Sync für Bilder einrichten.

---

### K32 — Toter Code: ForAll mit Distinct ohne Side-Effect

**Datei:** `Src/Home.pa.yaml` Zeilen 586–592
```powerfx
ForAll(Distinct(varempfängercheck_1, Empfänger),
    {Result: ThisRecord.Value}
);
```
Erzeugt eine Tabelle, weist sie keiner Variable zu. Tote Logik. AppChecker zählt das wahrscheinlich als `app-UnusedVariables`.

**Fix:** Block entfernen.

---

### B1 — Ungenutzte Dataverse-Tabelle `rrpt_foto`

Tabelle ist Teil der Solution (`solution.xml` Zeile 83: `<RootComponent type="1" schemaName="rrpt_foto" />`), wird aber in keinem Canvas-Source verwendet (Grep findet sie nicht in `Src/`). App nutzt SharePoint-Listen für Bilder.

Vermutlich Überbleibsel aus Migration / geplanter Refaktor. Entweder:
- Tabelle aus Solution entfernen
- Oder Bilder in Dataverse migrieren (löst K35)

---

### B2 — Hartcodierte Empfänger-Labels (40 Stück)

`Src/App.pa.yaml` Zeilen 73–122 — 20 × "Bauleitung-Rapport N" + 20 × "Kunde-Rapport N". Sollte in Lookup-Tabelle, oder konfigurierbar (für Erweiterung über 20 hinaus).

---

### B3 — Auskommentierte Code-Snippets im Source

Mehrere Stellen mit `// alte Logik` (z.B. Home.pa.yaml Zeilen 152, 208–213, 498). Verwirrt zukünftige Wartung. Aufräumen.

---

### B4 — 125x `acc-AccessibleLabelNeeded`

Barrierefreiheit. Für interne App low priority — aber wenn die App jemals an externe Auditoren geht oder bei Microsoft Power Platform Center of Excellence verglichen wird, ist das ein roter Flag.

---

### B5 — `App.OnStart` ist lang (8 ClearCollects + Lookups)

Startup-Performance, vor allem auf langsamer mobiler Verbindung. Pattern wechseln zu: minimaler OnStart, ClearCollects lazy beim ersten Screen-OnVisible.

---

## Zusammenfassung in einer Tabelle

| ID | Schweregrad | Bereich | Kurzbeschreibung |
|---|---|---|---|
| K1 | P1 | Fotos.pa.yaml | Foto-Delete hardcoded auf Sandbox-Liste |
| K4 | P1 | Workflows | PDF/Excel-Flow antwortet vor Ausführung, kein Catch |
| K5 | P1 | PDF Editierung.pa.yaml | Status "PDF" wird vor Flow-Erfolg gesetzt |
| K6 | P1 | Abschluss + PDF-Flow | PDF wird ohne Unterschrift gerendert |
| K9 | P1 | Architektur | O365-Gruppe und Dataverse-Rolle nicht gekoppelt (gleicher Mechanismus wie Subunternehmer) |
| K15 | P1 | Home.pa.yaml | PL-Rapporte überspringen Abschluss → keine Unterschrift |
| K22 | P1 | Personen/Material/Arbeitsbeschrieb | Hidden DataCard mit `Update: =currentitem` ist fragil |
| K24 | P1 | NotifyPL-Flow | Ungültige ID → Mail an leere Adresse, App zeigt Erfolg |
| K31 | P1 | Home.pa.yaml | Auto-Empfänger kann Blank schreiben |
| K33 | P1 | Home.pa.yaml | "Weiter" ohne Pflichtfeld-Validierung |
| K34 | P1 | Home.pa.yaml | Cascade-Delete im Client (nicht atomar) |
| K2 | P2 | Home.pa.yaml | Doppelklick → doppelte Rapporte |
| K3 | P2 | Home.pa.yaml | Räber-Spezialfall hardcoded |
| K7 | P2 | Abschluss-Screen.pa.yaml | Submit ohne Pflichtfeld-Prüfung |
| K10 | P2 | XLSX-Flow | Hartcodierte Sandbox-Site für Template |
| K12 | P2 | Home.pa.yaml | `'Erstellt Von Name'` als String-Snapshot |
| K14 | P2 | Arbeitsbeschrieb.pa.yaml | Translator-API ohne Catch, Original-Text wird überschrieben |
| K16 | P2 | App.pa.yaml | Chef-Mails hardcoded |
| K17 | P2 | Home.pa.yaml | Archivieren ohne Bestätigung |
| K18 | P2 | XLSX-Flow | 1-Min-Wait hardcoded |
| K20 | P2 | Home.pa.yaml | Delete ohne Bestätigung |
| K23 | P2 | PDF Editierung.pa.yaml | Patch in OnChange ohne IfError |
| K25 | P2 | Abschluss + PDF Editierung | `currentitem.Regiekopf` als impliziter Schlüssel |
| K27 | P2 | Architektur | Kein Lock während PDF-Generierung |
| K28 | P2 | Abschluss-Screen.pa.yaml | PenInput.Image ungekürzt patchen |
| K8 | P3 | PDF Editierung.pa.yaml | ForAll+Patch über AllItems (Skalierung) |
| K11 | P3 | Schema | Auto-Increment ohne Jahres-Reset |
| K19 | P3 | App.pa.yaml | Materialkatalog-Cache, `"x"` als Boolean |
| K30 | P3 | App.pa.yaml | varsmartphone nur bei OnStart evaluiert |
| K32 | P3 | Home.pa.yaml | Toter ForAll-Code |
| K35 | P3 | Architektur | Fotos nicht offline-fähig (SharePoint-Liste) |
| B1 | P3 | Schema | `rrpt_foto` deployed aber ungenutzt |
| B2 | P3 | App.pa.yaml | 40 Empfänger-Labels hardcoded |
| B3 | P3 | Code-Hygiene | Auskommentierte Code-Snippets |
| B4 | P3 | Barrierefreiheit | 125x AccessibleLabelNeeded |
| B5 | P3 | App.pa.yaml | OnStart zu lang |

---

## Empfohlene Reihenfolge

1. **Sofort (P1, hat unmittelbare Auswirkung):**
   - K1 (Foto-Delete) — 5 Minuten Fix
   - K15 (PL-Status direkt auf "PL") — kleiner Logik-Fix
   - K6, K7 (Validierung Unterschrift/Submit) — Schutz vor leeren Rapporten
   - K33 (Weiter ohne Pflichtfelder) — analog
   - K31 (Auto-Empfänger Blank) — analog

2. **Architektur-Refactor (P1, größerer Eingriff):**
   - K4 + K5 (Async-Flow mit Status-Patch im Catch) — die zentrale stille Inkonsistenz
   - K9 (O365 + Dataverse Sync) — das ist der "Subunternehmer-Patternfehler"
   - K34 (Cascade-Delete in DV-Beziehung)

3. **P2 nach Priorität:**
   - K3, K16 (hardcoded Personen-Bezüge)
   - K2 (Doppelklick-Schutz)
   - K14 (Translator-Bug Original-Text)
   - Bestätigungs-Dialoge K17, K20
   - K10 (XLSX Sandbox-URL → Env Var)

4. **P3 als Hygiene-Sprint:**
   - K8, K11, K22 (Hidden-DataCard)-Pattern systematisch lösen
   - B1 (rrpt_foto entfernen oder Bilder migrieren — löst auch K35)

---

## Was ich **nicht** gefunden habe (sind ausdrücklich keine Probleme)

Um klar zu sein, hier ist, was ich **geprüft** und **OK befunden** habe:

- **Dataverse-Rollen** für RRPT_PL (Global) und RRPT_MA (Basic) sind sinnvoll skoped — solange die Sync-Lücke (K9) gelöst wird.
- **Environment Variables** für Sandbox/Prod existieren und werden im PDF-Flow korrekt verwendet (nur XLSX hat K10).
- **Formel-Spalten** (`cr19a_mvmrapportnummer`, `cr19a_stundentotal`, `rrpt_personentotal`, `rrpt_materialtotal`) sind korrekt definiert und entlasten die App von Berechnungslogik.
- **Audit** ist auf den meisten Schlüssel-Feldern aktiviert (`IsAuditEnabled>1`).
- **Sandbox-Routing** in Flows (E-Mail an `raoul@miraglia-bi.com`) ist konsistent eingebaut — Sandbox wird nicht versehentlich an echte User schreiben.
- **`cr19a_unterschrift`** ist als Image-Feld (max ~9MB) korrekt typisiert.
