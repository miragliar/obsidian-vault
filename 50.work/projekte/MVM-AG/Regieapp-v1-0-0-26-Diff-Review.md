---
name: Regie-Rapport-App v1.0.0.26 — Diff-Review zur v1.0.0.23
slug: Regieapp-v1-0-0-26-Diff-Review
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
parent: "[[50.work/projekte/MVM-AG/Regieapp-Schwachstellen-Review|Regieapp-Schwachstellen-Review v1.0.0.23]]"
status: Review
review_datum: 2026-06-11
review_objekt: RegieRapportProzess_1_0_0_26.zip (Solution Manifest)
zip_source: "/Users/raouleliasmiraglia/Desktop/ZIP-Solutions/Zip Beispiel 1.zip"
tags: [miraglia, mvm-ag, power-apps, dataverse, schwachstellen, audit, version-diff]
created: 2026-06-11
updated: 2026-06-11
---

# Regie-Rapport-App v1.0.0.26 — Diff-Review

**Solution:** RegieRapportProzess 1.0.0.26 (Managed)
**Vorgänger-Review:** [[Regieapp-Schwachstellen-Review|v1.0.0.23 Schwachstellen-Review vom 2026-06-08]]
**Reviewer:** Claudian
**Review-Datum:** 2026-06-11
**Scope:** Vergleich Workflows + Customizations + Env-Vars; Canvas-App (`.msapp`) nicht ausgepackt.

> **Reviewer-Hinweis:** Drei Versionen sind seit dem letzten Review vergangen (23 → 26). Diese Notiz fokussiert auf **was sich verändert hat** — gefixt, neu eingeführt, immer noch offen.

---

## Executive Summary

**3 Versionen weiter — was hat sich getan:**

| Kategorie | Anzahl | Beispiele |
|---|---:|---|
| Gefixt seit v23 | **0** verifiziert | (keine P1-Befunde aus altem Review behoben) |
| Verbessert seit v23 | **1** | `01-rrpt-NotifyPL` hat jetzt Sandbox-Routing (`If(Umgebung != Sandbox, MailPL = body, MailPL = raoul@miraglia-bi.com)`) |
| Neue P1-Befunde | **2** | Skelett-Flow `03-rrpt-ExcelGenerierung` ausgeliefert; hartkodierte Sandbox-App-URL im NotifyPL-Mail-Body |
| Neue P2-Befunde | **2** | Anti-Pattern bei Env-Var-Defaults; Filename-Newline-Bug |
| Aus altem Review noch offen | **K4, K5, K9, K24 (teilweise)** | siehe unten |

**Wichtigste Bewertung:** Die App ist **nicht in einem besseren Sicherheitszustand** als bei v1.0.0.23 — eher in einem leicht schlechteren, weil mit dem Skelett-Flow zusätzliche Angriffsoberfläche reingekommen ist.

---

## Was wurde verbessert (Solution v23 → v26)

### ✅ `01-rrpt-NotifyPL` hat Sandbox-Routing bekommen

**Datei:** `Workflows/01-rrpt-NotifyPL-...json` Zeilen 71–119
```json
"Bedingung": {
  "type": "If",
  "expression": {"and": [{"not": {"equals": [
    "@parameters('Umgebung (rrpt_Umgebung)')", "Sandbox"]}}]},
  "actions": {"Variable_festlegen": {
    "value": "@outputs('Zeile_nach_ID_abrufen')?['body/rrpt_zustandigerplemail']"
  }},
  "else": {"actions": {"Variable_festlegen_1": {
    "value": "raoul@miraglia-bi.com"
  }}}
}
```
**Status K24 aus altem Review:** **Teilweise gefixt.** Sandbox-Routing existiert. Aber:
- Sandbox-Adresse ist hartkodiert (`raoul@miraglia-bi.com`) statt aus Env-Var
- Wenn `Zeile_nach_ID_abrufen` fehlschlägt (ungültige GUID): in Prod-Path `body=null` → `MailPL=""` → Mail-Connector wirft Fehler → ABER: App bekommt durch K24-Pattern weiterhin `Notify(..., Success)`

---

## P1 — Bestätigt offen aus altem Review

### 🔴 K4 (Fire-and-forget) — UNVERÄNDERT

**Dateien:** 
- `Workflows/02_V2-rrpt-PDFGenerierung-...json` Zeilen 1548–1564
- `Workflows/03_V2-rrpt-XLSXGenerierung-...json` Zeilen 147–163

```json
"Auf_eine_Power_App_oder_einen_Flow_reagieren": {
  "type": "Response",
  "statusCode": 200,
  "body": {},
  "runAfter": {}
}
```

Beide Flows antworten weiterhin **sofort**, ohne auf Erfolg zu warten. Catch-Scope nach wie vor nicht implementiert. **Drei Versionen unverändert.**

### 🔴 K5 (Status-Patch vor Flow-Erfolg) — UNVERÄNDERT

Canvas-App-Source (`.msapp`) nicht ausgepackt in dieser Session, aber Annahme nach Workflow-Analyse: K4 + K5 hängen zusammen. Wenn K4 unverändert ist, ist K5 mit hoher Wahrscheinlichkeit auch unverändert.

> **TODO:** `.msapp` auspacken (`msapp` ist ZIP) und `Src/PDF Editierung.pa.yaml` Zeile ~348 verifizieren.

### 🔴 K9 (Identitäts-Drift O365 ↔ Dataverse) — UNVERÄNDERT

**Datei:** `customizations.xml` Zeilen 17581 (RRPT_MA) + 18142 (RRPT_PL)

Identische Privilegien-Levels wie in v1.0.0.23:
- **RRPT_MA:** `prvRead/Write rrpt_Regiekopf` etc. auf `Basic` (Z. 17990, 18121)
- **RRPT_PL:** `prvRead/Write rrpt_Regiekopf` etc. auf `Global` (Z. 18551, 18682)
- Kein Sync-Mechanismus mit O365-Gruppe in der Solution erkennbar

---

## P1 — NEU in v1.0.0.26

### 🆕 N1 — Skelett-Flow `03-rrpt-ExcelGenerierung` (V1) in der Managed Solution

**Datei:** `Workflows/03-rrpt-ExcelGenerierung-F5BA74CC-975A-F111-BEC7-002248A05689.json` (komplette Datei, 42 Zeilen)

```json
"actions": {
  "Verfassen": {
    "runAfter": {},
    "type": "Compose",
    "inputs": "x"
  }
}
```

Trigger: `PowerAppV2` ohne Inputs.
Action: ein einziger `Compose` mit String `"x"`.

**Vermutung:** Das ist ein V1-Vorläufer der `03_V2-rrpt-XLSXGenerierung`. Wurde irgendwann angelegt, nie befüllt, beim Solution-Export aber als RootComponent mit aufgenommen (`<RootComponent type="29" id="{f5ba74cc-...}"/>` in `solution.xml` Zeile 96).

**Auswirkung:**
- Wird der Flow von irgendwo aufgerufen → 200 OK, kein Effekt
- Erhöht die Solution-Größe + Verwaltungs-Komplexität
- Bei einer zukünftigen Refaktor-Welle leicht zu übersehen

**Fix:** 
- Entweder Flow ausimplementieren (wenn er einen Zweck hatte) oder
- Aus Solution entfernen: `<RootComponent type="29" id="{f5ba74cc-975a-f111-bec7-002248a05689}"/>` aus `solution.xml` löschen + Workflow-Datei nicht mehr exportieren

### 🆕 N2 — Sandbox-App-URL hartkodiert im NotifyPL-Mail-Body

**Datei:** `Workflows/01-rrpt-NotifyPL-...json` Zeile 163
```
<a href="https://apps.powerapps.com/play/e/7b1a7c1a-efba-e4b4-8666-97c3fe33ab4a/a/ef423c5c-24af-445c-8a48-f5bddda953fe?tenantId=3becd9bb-f602-4c6b-8e86-f1e42db365ea&...">Regie-App</a>
```

GUID `7b1a7c1a-…` = Sandbox-Environment, App-GUID `ef423c5c-…` = Sandbox-App.

**Auswirkung in Prod:**
- Sandbox-Routing oberhalb sorgt dafür, dass die Empfänger-Adresse korrekt ist
- ABER die App-URL im Mail-Body ist immer der Sandbox-Link
- PL in Prod klickt → landet in Sandbox-App → entweder „no access" oder Test-Daten

**Fix:** 
- Neue Env-Var `rrpt_AppUrl` einführen (Sandbox- und Prod-Wert)
- Im Mail-Body `@parameters('AppUrl (rrpt_AppUrl)')` referenzieren statt hartkodierte URL

---

## P2 — NEU in v1.0.0.26

### 🆕 N3 — Anti-Pattern: Prod-Werte im Description-Feld der Environment Variables

**Datei:** `environmentvariabledefinitions/rrpt_SharepointLibrary/environmentvariabledefinition.xml`
```xml
<defaultvalue>b!v9qW6riscUaRL3WR_QCEhJuDGfXR11NCgGtVrzVDJSS5vmLXnL62So-d0F3k5qlG</defaultvalue>
<description>Prod: b!3shW9UYukEK-kboW7jY1h7PamA7hN_dHsWU78mTK_UsBRJokZ1dVQ7ShTlhJ-TOD</description>
```

Gleiches Pattern für `rrpt_SharepointRegieListe` (Sandbox-ID als Default, Prod-ID als Beschreibung) und `rrpt_SharepointSite` (Sandbox-URL als Default, keine Prod-Description).

**Auswirkung:** 
- Bei Solution-Import in Prod: Mensch muss Description lesen, Wert raushollen und manuell überschreiben
- Vergessenes Überschreiben → Prod-Flows greifen auf Sandbox-Listen / -Site

**Fix-Optionen:**
1. **„Connection-Reference-Strategie":** Solution-Wrapper mit Prod-Werten pre-set, der beim Import drüber gelegt wird (sauberste Lösung).
2. **„Validation-Flow":** Ein Init-Flow im Targets-Environment, der beim ersten Aufruf checkt, ob `varEnv == "Sandbox"` aber `rrpt_SharepointSite != "...Sandbox..."` (oder umgekehrt) → Admin-Alert.

### 🆕 N4 — Filename-Newline-Bug im PDF-Flow

**Datei:** `Workflows/02_V2-rrpt-PDFGenerierung-...json` Zeile 294
```
"value": "@{outputs('Baustelle_holen')?['body/cr19a_baustellennummer']}-@{outputs('Regiekopf_holen')?['body/cr19a_mvmrapportnummer']}-@{replace(outputs('Regiekopf_holen')?['body/cr19a_baustellenbezeichnung'], '/', '_')\n\n}.pdf"
```
Da steht ein `\n\n` **innerhalb der Expression**, vor der schließenden Klammer.

**Auswirkung:** 
- Aktuell funktioniert es vermutlich (Word-Connector strippt Whitespace)
- Bei Connector-Version-Upgrade potenziell Filename mit Zeilenumbrüchen oder Parser-Error
- **Code-Review-Smell** — Copy-Paste-Artefakt unentdeckt

**Fix:** `\n\n` entfernen.

---

## Inkonsistenz im Drive-ID-Handling (Bonus-Befund)

**Datei:** `Workflows/02_V2-rrpt-PDFGenerierung-...json`

```
Z. 748:  "drive": "b!v9qW6riscUaRL3WR_QCEhJuDGfXR11NCgGtVrzVDJSS5vmLXnL62So-d0F3k5qlG"
         ← Microsoft_Word-Vorlage_auffüllen — HARTKODIERT

Z. 815:  "drive": "@parameters('Sharepoint Library (rrpt_SharepointLibrary)')"
         ← Word-Dokument_in_PDF_konvertieren — ENV-VAR
```

Gleicher Drive, aber einmal hartkodiert (mit dem Sandbox-Wert), einmal über die Env-Var.

**Fix:** Z. 748 ebenfalls auf `@parameters('Sharepoint Library (rrpt_SharepointLibrary)')` umstellen.

---

## Zusammenfassung in einer Tabelle

| ID | Quelle | Schweregrad | Status v23 → v26 | Schadensszenario |
|---|---|---|---|---|
| K4 | Workflows | P1 | unverändert offen | Fire-and-forget → silent failure |
| K5 | Canvas-App | P1 | unverändert (Annahme) | Status-Patch ohne Flow-Erfolg |
| K9 | customizations.xml | P1 | unverändert offen | Identitäts-Drift, Datenschutz |
| K24 | Flows | P1 → P2 | **teilweise gefixt** | Sandbox-Routing eingebaut, aber Folgeprobleme |
| **N1** | `03-rrpt-Excel-V1` | P1 | **neu** | Toter Flow im Prod-Package |
| **N2** | NotifyPL Mail-Body | P1 | **neu** | Sandbox-App-Link in Prod-Mails |
| **N3** | Env-Var-Defaults | P2 | **neu** | Prod-Werte als Freitext-Description |
| **N4** | PDF-Flow Filename | P2 | **neu** | `\n\n` mitten in Expression |
| Bonus | Drive-ID-Inkonsistenz | P2 | **neu** | Hartkodierung + Env-Var mixed |

---

## Empfohlene Reihenfolge für v1.0.0.27

1. **N1** Skelett-Flow entfernen (1 Min Solution-XML-Edit)
2. **N4** `\n\n` aus Filename entfernen (5 Min)
3. **K24 Restbug** — `varempfänger` in NotifyPL muss bei `IsBlank` `Terminate Failed`, App muss Response prüfen (15 Min)
4. **N2** Neue Env-Var `rrpt_AppUrl` einführen, Mail-Body anpassen (30 Min)
5. **Bonus** Hartkodierte Drive-ID in PDF-Flow auf Env-Var umstellen (5 Min)
6. **N3** Prod-Wert-Pre-Set für Env-Vars architektonisch entscheiden (Diskussion mit Stakeholder)
7. **K4 + K5** Catch-Scope-Pattern aus Vorgänger-Review umsetzen (2–4 Std)
8. **K9** Identitäts-Drift — separater Workshop mit IT-Admin nötig (eigener Sprint)

---

## Was ich NICHT geprüft habe

- Canvas-App-Source: `.msapp` ist als ZIP-Container gepackt — ich habe sie in dieser Session nicht ausgepackt. Annahmen über Client-Seite (K1, K5, K6, K22 etc. aus dem alten Review) sind unverifiziert.
- Formulas (`Formulas/*.yaml`) sind nur 1-Zeiler, formal verifiziert
- Connection References (Konfiguration im Target Environment) — Solution-extern

> **Wenn du willst, packe ich in der nächsten Session die `.msapp` aus und verifiziere die Client-Seite-Befunde aus dem alten Review.**

---

## Verwandt

- [[Regieapp-Schwachstellen-Review|v1.0.0.23 Schwachstellen-Review]] — Original-Review
- [[Regieapp-Neubau-MVM|Projekt-Hub Regie-Rapport-App]]
- ZIP-Quelle: `/Users/raouleliasmiraglia/Desktop/ZIP-Solutions/Zip Beispiel 1.zip`
- Entpackt unter: `50.work/_review-temp/zip-beispiel-1/` (temporär, kann nach Verifikation gelöscht werden)
