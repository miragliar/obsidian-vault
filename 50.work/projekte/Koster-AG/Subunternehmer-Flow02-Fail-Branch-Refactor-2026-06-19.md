---
source: chat-context 2026-06-19
imported: 2026-06-19
type: projekt-doku
klient: Koster AG
klient_link: "[[50.work/26_Firmen/Koster-AG|Koster AG]]"
projekt_hub: "[[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster]]"
flow: "02 - SUB - Eingehende E-Mail verarbeiten"
solution_diff: "v1.0.0.14 → v1.0.0.15"
tags: [koster-ag, subunternehmer, power-automate, refactor, fail-handling, ai-builder]
---

# Subunternehmer Flow 02 — Fail-Branch-Refactor (v14 → v15)

Konkrete Diff-Dokumentation für den Refactor der Fail-Pfade im Flow `02 - SUB - Eingehende E-Mail verarbeiten`.

**Ursache:** 3 Mails am 2026-06-18 mit Subject „KI hat dieses Dokument bei Koster AG nicht verarbeiten können" — kein App-Eintrag dazu. Triage führte zur Erkenntnis, dass die Fail-Logik undifferenziert und teilweise tot war.

**Generalisiertes Pattern:** [[50.work/power-platform/power-automate-fail-branch-strategie]].

## Optionset `ks_eingangsqueue.ks_eq_status` (Stand v15)

| Code | Label | Semantik | App-Sichtbarkeit |
|---|---|---|---|
| 124080000 | Neu | Frisch erstellt, noch nicht verarbeitet | – |
| 124080001 | Verarbeitet | Erfolgreich zur Deklaration gemappt | – |
| 124080002 | **Fehlgeschlagen** | **Technischer Pipeline-Fehler** (Parse_JSON / PDF_Split) — **Audit-only, MA arbeitet aus Mail** | **keine View** (toter Bucket, bewusst) |
| 124080003 | **Manuell** | KI hat etwas erkannt, kein eindeutiger Match — **Mensch entscheidet in der App** | App-Manuell-Queue |

**Wichtig — semantische Trennung:**
- „Fehlgeschlagen" (124080002) wird **nirgendwo gelesen** (kein Flow, keine View). Bewusst genutzt als Audit-Spur, damit man später in Dataverse nachschauen kann, dass es einen Pipeline-Fail gab. Der eigentliche Triage-Workflow läuft **über die Mail**.
- „Manuell" (124080003) erscheint in der App-Manuell-Queue. Der MA arbeitet dort.

## Struktur der Fail-Pfade (Stand v15)

```
For_each (über Mail-Attachments)
└── Condition: PNG-Filter
    └── Scope_-_Dokument_verarbeiten
        ├── Scope_KI
        │   ├── Run_a_prompt        (AI Builder Custom Prompt)
        │   └── Parse_JSON          (runAfter Run_a_prompt: Succeeded)
        │
        ├── Condition_Split          (runAfter Scope_KI: Succeeded)
        │   if length(result) > 1:
        │     PDF_-_Split_Document_2 (PDF4me)
        │   else: leer
        │
        ├── Apply_to_each            (runAfter Condition_Split: Succeeded)
        │   └── Scope (Inner)        — pro erkanntes Sub-Dokument
        │       └── [diverse Branches: Deklaration-ID-Match, Sub-Name-Match, …]
        │           ├── happy → Status 124080001 "Verarbeitet"
        │           └── nicht-eindeutig → Status 124080003 "Manuell"
        │
        ├── Update_a_row_-_Verarbeiten_fehlgeschlagen_-_aber_noch_manuell
        │       runAfter: Scope (Inner): Failed
        │       → Status 124080003 "Manuell"
        │       → Fehlertext "KI hat Structured Output nicht mitgeliefert"
        │       (KEIN Mail mehr — war früher "Fehlgeschlagen" + Mail)
        │
        ├── Send_an_email_-_Parse_JSON_fail
        │       runAfter: Scope_KI: Failed
        │       Subject: "KI-Parse fehlgeschlagen bei Koster — kein strukturierter Output"
        │       → danach: Add_a_new_row_-_Parse_fail → Status 124080002
        │
        └── Send_an_email_-_PDF_Split_Fail
                runAfter: Condition_Split: Failed
                Subject: "PDF-Split fehlgeschlagen bei Koster — Multi-Doc muss händisch gesplittet werden"
                Body enthält: length(result), Seite_von_bis_concat
                → danach: Add_a_new_row_-_Split_fail → Status 124080002
```

## Diff v14 → v15

### 1. `Bereich`-Scope aufgelöst, durch `Scope_KI` ersetzt

**v14:**
- Ein Sammel-`Bereich`-Scope wrappte `Parse_JSON` + `Condition_Split` (+ `PDF_Split` darin)
- Sammel-Mail bei `Bereich: Failed` — undifferenziert für Parse-Fail und Split-Fail

**v15:**
- `Scope_KI` umfasst nur `Run_a_prompt` + `Parse_JSON` (zwei semantisch zusammengehörige Actions)
- `Condition_Split` steht freistehend daneben, kein Wrapper
- Zwei separate Mail-Branches:
  - `Scope_KI: Failed` → eigener Mail mit eigenem Subject + Body
  - `Condition_Split: Failed` → eigener Mail, kann Triage-Helfer (`length`, `Seite_von_bis_concat`) aus dem **erfolgreichen** `Parse_JSON` mitgeben

### 2. Stelle A (Apply_to_each Inner-Scope Failed): Mail entfernt, Status auf „Manuell"

**v14:**
- Bei Inner-Scope Failed → Mail + `Update_a_row` mit Status **124080002 „Fehlgeschlagen"**
- Eintrag landete im toten Bucket, wurde nicht in der App-Manuell-Queue sichtbar
- Trotzdem Mail → doppelter Reiz, MA musste manuell in Tabelle umstellen auf „Manuell"

**v15:**
- Mail entfernt
- `Update_a_row_-_Verarbeiten_fehlgeschlagen_-_aber_noch_manuell` setzt Status **124080003 „Manuell"**
- Eintrag erscheint direkt in der App-Manuell-Queue, MA bearbeitet dort

### 3. Neue Add_a_new_rows für Audit-Spur

**v14:** Bei `Bereich Failed` wurde **kein** Eintrag in `ks_eingangsqueues` angelegt — keine Audit-Spur.

**v15:**
- `Add_a_new_row_-_Parse_fail` runAfter `Send_an_email_-_Parse_JSON_fail: Succeeded`
- `Add_a_new_row_-_Split_fail` runAfter `Send_an_email_-_PDF_Split_Fail: Succeeded`
- Beide setzen Status **124080002 „Fehlgeschlagen"** mit Fehlertext + Original-Mailid
- Bewusst nicht „Manuell" — die Bearbeitung läuft über die Mail, der DV-Eintrag ist reine Audit-Spur

## Bewusste Design-Entscheidungen

### Wieso bei Stelle A „Manuell" + keine Mail, aber bei Pipeline-Fails (Parse/Split) Mail + „Fehlgeschlagen"?

**Stelle A:** Inner-Scope-Fail im Apply_to_each. Das passiert pro **erkanntes Sub-Dokument** — die KI hat es erkannt, der Eintrag existiert bereits (vom `Add_a_new_row_1` als erste Action im Inner-Scope mit Status „Neu"), der MA kann in der App das Dokument sehen und entscheiden. Mail wäre redundant.

**Pipeline-Fails (Parse_JSON / PDF_Split):** Kein erkanntes Sub-Dokument, weil die Pipeline vor dem Apply_to_each abbricht. Es gibt nichts in der App zu sehen außer einem Pseudo-Eintrag. Die Mail mit dem Original-Attachment ist die einzig sinnvolle Reaktion — der MA arbeitet aus dem Postfach heraus (lokales Splitting in Acrobat, ggf. Re-Upload an `deklaration-test@kosterag.ch`).

### Wieso Mail vor Audit-Eintrag (nicht parallel)?

Bewusst: **Mail ist Priorität #1, MUSS kommen.** Wenn die Mail (transient) failt, ist der Audit-Eintrag auch sekundär — Power Automate's Owner-Notification fängt den Flow-Fail auf.

### Wieso überhaupt Audit-Eintrag, wenn er nirgendwo gelesen wird?

Spurensicherung. Wenn später jemand fragt „warum kam diese KI-Mail am 18.06. nicht durch?" — der Eintrag in `ks_eingangsqueues` zeigt: `ks_eq_mailid` + `ks_eq_fehlertext` + Timestamp. Plus: Wenn das in Zukunft häufiger passiert, kann eine Auswertung „wie oft failt die Pipeline?" über diese Einträge gefahren werden ohne ins Flow-Run-History zu müssen.

## Was vor Prod-Deploy zwingend zu prüfen ist

**Static Results für `PDF_-_Split_Document_2` deaktivieren.** Beim v15-Build war für den Test des Split-Fail-Pfads ein `staticResult` mit „Failed" gemockt. In Prod führt das dazu, dass jeder Multi-Doc-Split garantiert failt:

```json
"staticResults": {
  "PDF_-_Split_Document_20": { "status": "Failed", ... }
}
"PDF_-_Split_Document_2": {
  "runtimeConfiguration": {
    "staticResult": {
      "staticResultOptions": "Enabled",   // ← MUSS "Disabled" sein
      "name": "PDF_-_Split_Document_20"
    }
  }
}
```

Stand 2026-06-19: deaktiviert (von Raoul bestätigt).

Sanity-Check vor jedem Export:
```bash
grep -rn "staticResultOptions" Workflows/
```
Sollte leer sein oder nur `"Disabled"` enthalten.

## Verwandt

- [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Subunternehmerprozess Koster — Projekt-Hub]]
- [[50.work/power-platform/power-automate-fail-branch-strategie|Pattern: Power Automate Fail-Branch-Strategie]]
- [[50.work/power-platform/ai-builder-doppel-branch-vermeiden|AI Builder — Doppel-Branch vermeiden]]
- [[50.work/power-platform/mail-attachment-pipeline-fallen|Mail-Attachment-Pipeline — Bug-Cluster aus diesem Flow]]
- [[50.work/26_Firmen/Koster-AG|Klient: Koster AG]]
