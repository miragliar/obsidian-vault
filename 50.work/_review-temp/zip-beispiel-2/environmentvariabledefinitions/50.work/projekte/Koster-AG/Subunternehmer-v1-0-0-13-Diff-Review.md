---
name: Subunternehmer-Solution v1.0.0.13 — Code-Review
slug: Subunternehmer-v1-0-0-13-Diff-Review
klient: Koster AG
klient_link: "[[50.work/26_Firmen/Koster-AG|Koster AG]]"
parent: "[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess-Koster (Projekt-Hub)]]"
status: Review
review_datum: 2026-06-11
review_objekt: Subunternehmer v1.0.0.13 (Managed)
zip_source: "/Users/raouleliasmiraglia/Desktop/ZIP-Solutions/ZIP Beispiel 2.zip"
tags: [miraglia, koster-ag, power-apps, power-automate, dataverse, schwachstellen, audit, version-diff]
created: 2026-06-11
updated: 2026-06-11
---

# Subunternehmer-Solution v1.0.0.13 — Code-Review

**Solution:** `Subunternehmer` 1.0.0.13 (Managed)
**Publisher:** `Koster` (Prefix `ks`)
**Bestehender Projekt-Hub:** [[Subunternehmerprozess-Koster|Subunternehmer-Dokumentenverwaltung]]
**Reviewer:** Claudian
**Review-Datum:** 2026-06-11
**Scope:** Solution-Manifest, alle 11 Workflows (Grep-Scan + Tieflesungen), 7 Env-Vars, Roles-Definitionen. Canvas-App-`.msapp` nicht ausgepackt.

> **Reviewer-Hinweis:** Dies ist eine Live-Analyse zum Showcase-Video. Befunde sind mit Datei + Zeilen-Referenzen belegt. Wo ich nicht tief verifiziert habe (z.B. Schema-Details), ist das markiert.

---

## Executive Summary

| Kategorie | Anzahl | Highlight |
|---|---:|---|
| **P1 — Schadens-Potenzial** | 3 | **15 Stellen** mit hartkodiertem `/K20`-Jahres-Pfad → **bricht in ~6,5 Monaten** |
| **P2 — Robustheit / Drift** | 3 | Env-Var-Anti-Pattern; Library-Doppel-Variable Drift; Cross-Publisher-Entity |
| **P3 — Code-Hygiene** | 2 | Toter `Compose: "x"`-Block; nie gelesene Variable |
| **Schon im Vorgänger-Review dokumentiert** | 2 | Cluster A1/A2 Binary Damage (Pattern-Notiz vorhanden); Hash-Speicherung |

**Wichtigste Bewertung:** Solution ist funktional sauber gegliedert (11 spezialisierte Flows), aber **die in der Pattern-Notiz `lessons-learned-koster` dokumentierten latenten Risiken sind nicht entschärft**. Vor allem der Jahreswechsel-Bug ist mit 6,5 Monaten Vorlauf akut.

---

## P1 — Akute Schwachstellen

### 🔴 P1-1 — Jahreswechsel-Bug (`/K20`) an **15 Stellen** akut

**Schadens-Datum:** ~ 2027-01-01 (in **~6,5 Monaten** ab heute, 2026-06-11)

**Verteilung:**

| Datei | Anzahl | Kontext |
|---|---:|---|
| `01-SUB-AuftragerstellenundDokumenteversenden.json` | **12** | Z. 294, 476, 657, 844, 1026, 1212 (File-Path), Z. 1353, 1399, 1445, 1491, 1537, 1583 (SP-Pfad) |
| `02-SUB-EingehendeE-Mailverarbeiten.json` | **2** | Z. 331, 605 (Move-Destination) |
| `04-SUB-UnzugewiesenenachAppEintragverarbeiten.json` | **1** | Z. 230 (Move-Destination) |

**Beispiel** (Flow 01 Z. 1353):
```javascript
"item/ks_versendet_sp_pfad":
  "@{split(outputs('Create_file_PDF_-_Brief')?['body/Path'],'/K20')[0]}/@{variables('Prefix')}"
```
Sobald der Pfad `K27` enthält (ab 1. Jan 2027), liefert `split(..., '/K20')[0]` den **gesamten ursprünglichen Pfad** zurück — also die Logik produziert dann „pfad/zur/datei.pdf/K27/file.pdf" statt nur den Folder-Prefix.

**Auswirkung:**
- Subunternehmer-Pfade werden nicht mehr korrekt extrahiert
- Move-Operations versuchen in einen ungültigen `destinationFolderPath` zu schreiben
- `Add_a_new_row` befüllt `ks_versendet_sp_pfad` mit fragmentiertem Wert → Folge-Flows mit Pfad-Logik brechen

**Fix-Strategie (aus Vorgänger-Review wiederverwenden):**
- Subunternehmer-Folder-Lookup statt String-Split
- Oder: dynamische Jahres-Erkennung — `split(..., '/K' + substring(string(year(utcNow())), 2, 2))[0]`
- Empfohlen: 1-Helper-Flow ggf. via Child-Flow, der den Subunternehmer-Folder-Pfad zentral liefert

**Aufwand:** ~ 2–4 Std (Helper-Flow + 15 Stellen-Refactor)

---

### 🔴 P1-2 — Environment Variable Defaults zeigen explizit auf Sandbox

**Datei:** `environmentvariabledefinitions/*/environmentvariablevalues.json`

| Env-Var | Wert | Prod-Hinweis im Code? |
|---|---|---|
| `ks_Environment` | `"Sandbox"` | Nur als Beschreibung („Sandbox or Production") |
| `ks_Posteingang` | `"deklaration-test@kosterag.ch"` | Im Description-Feld: „... oder deklaration@kosterag.ch" |
| `ks_SP_SiteURL` | `"https://kosterag.sharepoint.com/sites/Subunternehmer_Sandbox"` | **keiner** |
| `ks_SP_Library_Text` | `"b!9-WDOBk4-kmzneZIA-6tXoedMeUrAy1BrO62..."` | Im Description: „Prod: b!sT0FUceMjUybEBiNzlM8Sj..." |
| `ks_SP_Library` | `"59a1d5db-13fe-4eec-93f9-f131bfa2bdf6"` | **keiner** |
| `ks_SP_Kundenpfad` | `"02_Kunden"` | Generisch — vermutlich OK |

**Auswirkung:** Bei Solution-Import in einer Prod-Umgebung muss ein Mensch jeden einzelnen Wert manuell überschreiben. **Kein Validierungs-Check.** Vergisst jemand auch nur eine Variable → Prod-Flows operieren auf Sandbox-Datenbestand.

**Gleiches Anti-Pattern** wie in [[Regieapp-v1-0-0-26-Diff-Review#🆕 N3 — Anti-Pattern Prod-Werte im Description-Feld der Environment Variables|RegieRapport v1.0.0.26 Befund N3]].

> 💡 **Pattern-Konvergenz**: Das ist nicht „Schuld" eines Entwicklers — die Power-Platform-Doku adressiert das Sandbox/Prod-Defaulting nicht klar. Hier bietet sich eine projekt-übergreifende Pattern-Notiz an.

**Fix-Optionen:**
1. **Solution-Layer mit Prod-Werten** (Wrapper-Solution, die beim Import drüber gelegt wird)
2. **Init-Flow im Target Environment** der bei erstem Aufruf inkonsistente Werte zu einem Admin-Alert auflöst
3. **Pre-Import-Skript**, das die JSON-Files vor dem Import anpasst

---

### 🔴 P1-3 — Drift-Risiko zwischen `ks_SP_Library` und `ks_SP_Library_Text`

Zwei Environment Variables, **die dieselbe SharePoint-Library in unterschiedlichen Formaten halten**:

- `ks_SP_Library` (Type 100000004 / SharePoint-Drive-Reference) → GUID `59a1d5db-13fe-4eec-93f9-f131bfa2bdf6`
- `ks_SP_Library_Text` (Type 100000000 / String) → Drive-Hash `b!9-WDOBk4-kmzneZIA-6tXoedMeUrAy1BrO62...`

**Auswirkung:** Beide müssen **manuell synchron** gehalten werden. Bei Library-Wechsel:
- Admin überschreibt `ks_SP_Library` (offensichtlich), vergisst `ks_SP_Library_Text`
- Flows die `_Text` nutzen (Word-Template-Lookup) zeigen auf alte Library
- Flows die `_Library` nutzen (Move-Operations) zeigen auf neue Library
- **Stille Doppelablage** an zwei Orten, kein Indikator im Outlook-Verhalten

**Fix:** Im idealen Fall: Drive-Hash via `outputs('Get_drive_metadata')?['driveId']` zur Laufzeit holen. Pragmatisch: Beide Variables in einer Doku-Notiz koppeln + Check-Skript bauen.

---

## P2 — Robustheit / Strukturelle Schwachstellen

### 🟡 P2-1 — Cross-Publisher-Drift bei Entity `crb4b_subunternehmer`

**Datei:** `solution.xml` Zeile 81
```xml
<RootComponent type="1" schemaName="crb4b_subunternehmer" />
<RootComponent type="1" schemaName="ks_auftrage" />
<RootComponent type="1" schemaName="ks_deklarationen" />
<RootComponent type="1" schemaName="ks_eingangsqueue" />
```

Vier von fünf Entities haben den Custom-Publisher-Prefix `ks_`. Eine (`crb4b_subunternehmer`) trägt den Default-CDS-Prefix `crb4b_`. Die Entity wurde **vor** dem Aufsetzen des Custom-Publishers angelegt — keiner hat sie nachträglich migriert.

**Auswirkung:** 
- Kein akuter Bug, aber Identifier-Inkonsistenz im Schema
- Bei Tenant-Migration oder Solution-Split: höhere Komplexität (zwei Publisher zu pflegen)
- Neue Entwickler verstehen die Inkonsistenz nicht — Sicht-Verschmutzung

**Fix:** Entity-Rename ist in Dataverse aufwändig (alle Lookups, Plug-Ins, Plugin-Steps müssen mit). Wenn nicht jetzt: dokumentieren als „Tech-Debt akzeptiert".

### 🟡 P2-2 — `ks_Environment`-Variable ist nur dekorativ

Die Variable `ks_Environment = "Sandbox"` ist gesetzt, aber **kein Flow scheint sie zu lesen** (Grep nach `parameters('Environment')` in den Workflows liefert keine Treffer in den 11 JSON-Dateien).

> **Achtung:** Diese Aussage gilt nur für die Workflow-JSONs. Die Canvas-App (`.msapp`, nicht ausgepackt) könnte sie referenzieren.

**Auswirkung:** Wenn die Workflows die Variable nicht nutzen, ist das Sandbox-Routing-Pattern aus der RegieRapport-Solution (`If(Umgebung != Sandbox, ...)`) hier nicht etabliert. **Subunternehmer-Mails in Prod könnten an echte Subunternehmer gehen, auch beim Test-Run** — Imagebeschädigung-Risiko.

**Empfehlung:** In den großen Flows (01, 02, 06) checken, ob es Sandbox-Routing für ausgehende Mails gibt. Falls nicht: dringend einbauen analog zum NotifyPL-Pattern.

### 🟡 P2-3 — Nur **eine** Sicherheitsrolle definiert

**Datei:** `customizations.xml` Zeile 7640
```xml
<Role id="{9fa83c22-1f33-f111-88b5-7c1e52742293}" name="Subunternehmer-Prozess">
```

Einzige Custom-Rolle für die ganze Solution. Im Gegensatz zur RegieRapport-Solution mit `RRPT_MA` und `RRPT_PL` gibt es hier kein User-vs-Admin-Profil.

**Auswirkung:**
- Jeder Solution-User hat dieselben Privilegien
- Kein Read-Only-User-Profil möglich (z.B. für Buchhaltung, die nur die Status sehen will)
- Berechtigungs-Eskalation in einem Schritt (an/aus)

**Fix:** Falls fachlich gewollt: zweite Rolle `Subunternehmer-Reader` mit Read-only-Privilegien. Sonst dokumentieren als „bewusst flach".

---

## P3 — Code-Hygiene

### 🟦 P3-1 — Toter `Compose: "x"`-Block in SUB-DateiLadenFlow

**Datei:** `SUB-DateiLadenFlow.json` Z. 60–68
```json
"Compose": {
  "type": "Compose",
  "inputs": "x",
  "runAfter": {}
},
"Get_file_content_using_path": {
  "runAfter": {"Compose": ["Succeeded"]}
}
```

`Compose` produziert `"x"` und ist Vorgänger für `Get_file_content_using_path`. **Debug-Überbleibsel**, das aber jeden Aufruf ein paar Millisekunden Latenz produziert und die Lesbarkeit verschlechtert.

**Wichtig:** **Gleiches Pattern** wie das Skeleton `03-rrpt-ExcelGenerierung` in der RegieRapport-v1.0.0.26-Solution. Zwei verschiedene Kunden, gleicher Code-Smell — sieht nach einem persönlichen Debug-Pattern aus.

**Fix:** `Compose` löschen + `Get_file_content_using_path.runAfter` auf `{}` setzen.

### 🟦 P3-2 — Variable `File Content` initialisiert, nicht gelesen

**Datei:** `02-SUB-EingehendeE-Mailverarbeiten.json` Z. 1034–1051
```json
"Initialize_variable_1": {
  "variables": [{"name": "File Content", "type": "string"}]
}
```

Grep nach `variables('File Content')` und `setVariable.*File Content` im selben Flow → keine Treffer (außer Init selbst).

**Auswirkung:** Tote Variable, Code-Smell. Aber: könnte ein historisches Pattern sein, das später entfernt wurde, ohne den Init-Block zu putzen.

**Fix:** Init-Block entfernen.

---

## Aus dem Vorgänger-Review nicht erneut verifiziert

Im bestehenden Projekt-Hub [[Subunternehmerprozess-Koster]] sind Cluster A1, A2, B1, B2, C1, D dokumentiert. **Diese habe ich in dieser Session nicht erneut verifiziert.** Insbesondere:

- **Cluster A1 (`@{}` Curly Braces zerstört Binary):** Im `SUB-DateiLadenFlow` Z. 107 sehe ich `"base64": "@{base64(body('Get_file_content_using_path'))}"` — das ist `@{}` mit Curly Braces. Diese Response geht aber an Power Apps, nicht in eine Power-Automate-Variable — daher vermutlich OK. **Sollte aber verifiziert werden.**
- **Cluster A2 (Variable Binary Damage):** Variable `File Content` ist tot (P3-2), aber ihre Existenz allein zeigt, dass das Pattern noch im Code-Vokabular ist.
- **Cluster B1, B2, C1, D:** Würden eine detaillierte Tieflesung der Flows 01 (90 KB) und 02 (59 KB) erfordern.

---

## Zusammenfassung in einer Tabelle

| ID | Schweregrad | Datei | Kurzbeschreibung |
|---|---|---|---|
| P1-1 | P1 (akut Q1 2027) | 3 Flows, 15 Stellen | Hartkodiertes `/K20`-Pfad-Element bricht beim Jahreswechsel |
| P1-2 | P1 | 6/7 Env-Vars | Sandbox-Defaults, Prod-Werte nur als Beschreibung |
| P1-3 | P1 | `ks_SP_Library` + `_Text` | Doppel-Variable für selbe Library, manuelle Sync |
| P2-1 | P2 | `solution.xml` | Cross-Publisher-Drift `crb4b_subunternehmer` |
| P2-2 | P2 | 11 Workflows | `ks_Environment` Variable existiert, wird in Flows nicht gelesen → kein Sandbox-Routing? |
| P2-3 | P2 | `customizations.xml` | Nur 1 Sicherheitsrolle, kein User-vs-Reader-Split |
| P3-1 | P3 | `SUB-DateiLadenFlow.json` | Toter `Compose: "x"`-Block |
| P3-2 | P3 | `02-SUB-...EingehendeE-Mail.json` | Tote Variable `File Content` |

---

## Empfohlene Reihenfolge

1. **Sofort (P1-1, akut Q1 2027):**
   - Helper-Flow für Subunternehmer-Folder-Lookup designen (~30 Min)
   - 15 Stellen refactoren (~ 1.5–3 Std je nach Tiefe)
   - Test gegen 2027-Pfad (manuell oder Mock)

2. **Architektur-Refactor (P1-2 + P1-3 + P2-2):**
   - Diskussion mit Stakeholder: Pre-Set-Solution vs. Init-Flow vs. Pre-Import-Skript
   - Falls Init-Flow: Sandbox-Routing in Flow 01 & 02 mit einbauen

3. **P2 nach Priorität:**
   - P2-2 Sandbox-Routing-Check in Flows 01, 02, 06 (verifizieren ob es wirklich fehlt)
   - P2-3 Reader-Rolle nur wenn fachlich relevant

4. **P3 als Hygiene-Sprint:**
   - 15 Min Aufräumen P3-1 + P3-2 + 6 `\n\n`-Newlines in den Expressions

---

## Cross-Solution-Pattern (für die Pattern-Notiz)

**Befunde, die in beiden v1-Solutions identisch auftauchen** (KosterAG Subunternehmer + MVM RegieRapport):

| Pattern | Koster v1.0.0.13 | MVM v1.0.0.26 |
|---|---|---|
| Env-Var-Defaults zeigen auf Sandbox, Prod im Description-Feld | P1-2 (6/7 Variables) | N3 (3/4 Variables) |
| Skeleton-Flow `Compose: "x"` in Managed-Solution | P3-1 (`SUB-DateiLadenFlow`) | N1 (`03-rrpt-ExcelGenerierung`) |
| Hartkodierte Jahres-Pfade in String-Split-Logik | P1-1 (15 Stellen `/K20`) | nicht gefunden |
| Newline-Artefakte mitten in Expression-Parametern | mehrere `\n\n` in Flow 01 | N4 (`\n\n` in Filename) |

> **Vorschlag:** Drei projekt-übergreifende Pattern-Notizen anlegen:
> - `power-platform/env-var-prod-default-anti-pattern.md`
> - `power-platform/skeleton-flow-debug-artifact.md`
> - `power-platform/hardcoded-year-paths.md`
>
> Diese erkenne ich beim nächsten Kunden sofort.

---

## Verwandt

- [[Subunternehmerprozess-Koster|Projekt-Hub: Subunternehmer-Dokumentenverwaltung]]
- [[Regieapp-v1-0-0-26-Diff-Review|MVM RegieRapport v1.0.0.26 — Counterpart-Review]] (das andere Demo-ZIP)
- [[40.meta/demo-claudian-showcase|Drehbuch Claudian-Showcase]]
- ZIP-Quelle: `/Users/raouleliasmiraglia/Desktop/ZIP-Solutions/ZIP Beispiel 2.zip`
- Entpackt unter: `50.work/_review-temp/zip-beispiel-2/` (temporär, kann nach Verifikation gelöscht werden)
