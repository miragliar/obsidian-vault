---
name: Claudian-Showcase — Live-Demo-Drehbuch
slug: demo-claudian-showcase
type: demo-script
purpose: Video-Drehbuch für Kunden-News — Wie Claudian in Obsidian Solutions analysiert, verbessert und Wissen sichert
tags: [demo, video, claudian, miraglia-bi, showcase, anonymisiert]
status: ready
created: 2026-06-11
updated: 2026-06-11
zielgruppe: Bestands- und Neukunden (Miraglia-BI News)
tonalität: Mittelweg — Code sichtbar, aber jede Schwachstelle mit 1-Satz-Business-Impact
roter_faden: "Wie schnell wurde Code-Review mit Claudian einfacher"
laufzeit_ziel: 4–6 Minuten
---

# Claudian-Showcase — Drehbuch

> **Ziel des Videos:** Kunden zeigen, wie wir bei Miraglia-BI mit Claude (Claudian) im Obsidian-Vault arbeiten, um produktive Power-Platform-Solutions in Minuten statt Stunden zu analysieren — mit konkretem Code-Beweis und gesichertem Wissen für künftige Projekte.
>
> **Roter Faden:** *„Vor zwei Jahren war ein Code-Review einer Power-Apps-Solution ein halber Tag Arbeit. Heute lade ich die Solution in den Vault, frage Claudian — und habe Befunde mit Zeilen-Referenzen, bevor mein Kaffee kalt wird."*
>
> **Was Kunden NICHT sehen:** Firmennamen, echte Flow-Namen, echte Personen, echte Tabellen-Schemata. Alle Bezeichner über das Mapping unten anonymisiert.

---

## 🎬 Anonymisierungs-Mapping (verbindlich für den Dreh)

| Original (NICHT zeigen) | Demo-Bezeichnung (zeigen) |
|---|---|
| Solution 1 (Subunternehmer-Doku, Klient „K…AG") | **„Vendor Document Pipeline"** |
| Solution 2 (Außendienst-Rapportierung, Klient „M…AG") | **„Field Service Reporting App"** |
| `02_V2-rrpt-PDFGenerierung` | `flow-document-generation` |
| `03_V2-rrpt-XLSXGenerierung` | `flow-report-export` |
| `01-rrpt-NotifyPL` | `flow-notify-supervisor` |
| `Regie-Bilder` / `Regie-Bilder_1` | `PhotoList_Sandbox` / `PhotoList_Prod` |
| `rrpt_Regiekopf` (+ Lines) | `proj_workorder_header` (+ `_personnel` / `_material` / `_description`) |
| `ks_eq_...` / `ks_deklarationens` | `vendor_eq_...` / `vendor_declarations` |
| Personen (Räber, Pfister, Baumann …) | „Senior PM A", „Director B", „Stakeholder C" |
| `mvmcr@…`, `mvmrp@…`, `personal@mvm-ag.ch` | „internal-pm@example.com", „internal-ops@example.com" |
| `K20…` / `K27…` (Jahres-Ordner) | `Y26…` / `Y27…` |

**Im Bildschirm-Recording auch unkenntlich machen:** Fenster-Titel („Miraglia-BI / Obsidian Raoul"), Sidebar mit Original-Ordnernamen, alle `klient:`-Frontmatter-Felder.

---

## 🎬 Szene 1 — Intro (30 Sek)

**Bildschirm:** Vault-Seitenleiste mit den zwei (anonymisierten) Solutions.

**Raoul on-camera oder Voice-over:**
> *„Wenn ich früher eine fremde Power-Apps-Solution prüfen sollte — sagen wir, ein Übergabe-Review nach einem Entwickler-Wechsel — war das ein halber Tag. PA-YAML lesen, Flow-JSON manuell durchgehen, mit der Customizations.xml abgleichen. Heute mache ich das so:"*

**Raoul-Prompt im Chat (sichtbar tippen):**
> *„Claudian, ich habe dir zwei Power-Platform-Solutions in den Vault gezogen. Lies sie und gib mir die zentralen Stärken und Schwächen mit konkretem Code-Beweis."*

**Claudians Antwort (Vorlage):**
> *„Beide Solutions laufen produktiv. Das, was du jetzt siehst, ist kein „Claude rät" — das sind Befunde mit Datei- und Zeilen-Referenzen. Ich starte mit Solution A."*

---

## 🎬 Szene 2 — „Vendor Document Pipeline" (75 Sek)

**Was die Solution tut (1 Satz):**
> KI-Builder klassifiziert eingehende PDF-Anhänge → Power Automate orchestriert Status-Übergänge (Eingang → Prüfung → Freigabe / Rückfrage / Ablage) → Dataverse + SharePoint archivieren.

### ✅ Stärken

- **Pattern-Katalog:** 7 destillierte Notizen, jede mit konkretem Trigger-Case
- **Deterministische Status-Maschine** — keine versteckten Übergänge
- **Wöchentliche Reminder** als gescheduleter Flow — kein Polling, kein Drift

> 💼 **Was das geschäftlich heißt:** Wenn ein neuer Entwickler übernimmt, ist die Lernkurve flach. Jeder Bug-Fix hinterlässt wiederverwendbares Wissen.

### ⚠️ Top-Schwachstelle (zeigen, 1 Befund mit Code)

**Binary Damage durch Power Automate Variablen**
```
Symptom: EF BF BD (UTF-8 Replacement Character) in PDF-Streams
        + "Bad FCHECK in flate stream"
```
Power Automate behandelt Binärdaten in Variablen als UTF-8-Strings — und beschädigt sie still.
**Fix:** Variablen für File Content **komplett entfernen**, Connector-Output direkt in `Create_file` referenzieren.

> 💼 **Was das geschäftlich heißt:** Hochgeladene PDFs wirkten korrekt — bis jemand sie aufmachen wollte. **Stille Datenkorruption über Wochen**, bis ein Kunde reklamiert.

### 🤔 Eine Rückfrage von Claudian (im Video zeigen)

> *„Es gibt einen latenten Bug, der heute nicht zuschlägt: ein Pfad enthält die Jahreszahl `Y26` hartcodiert. **Bricht in 2027.** Soll ich das jetzt fixen oder als TODO mit Datum 2026-11-01 in deinen Vault setzen?"*

> 💡 **Pointe für die Kunden:** Claudian findet nicht nur akute Bugs — er findet **Bugs, die in 7 Monaten passieren werden**. Das ist der Unterschied zwischen reaktiver Wartung und vorausschauendem Engineering.

---

## 🎬 Szene 3 — „Field Service Reporting App" (90 Sek)

**Was die Solution tut (1 Satz):**
> Canvas-App für Außendienst-MA — Stunden, Material, Fotos, Unterschriften auf der Baustelle erfassen → Auto-PDF → Mailversand an Projektleitung.

### ✅ Stärken

- Master-Detail-Architektur mit Dataverse, sauber strukturiert
- Sandbox-Routing: E-Mails landen konsequent auf Test-Adresse
- Audit auf Schlüsselfeldern aktiviert

> 💼 **Was das geschäftlich heißt:** Wer Compliance-Anforderungen hat (Bau, Engineering, Healthcare) bekommt eine Nachvollziehbarkeit out-of-the-box.

### 🔴 Top-Schwachstelle 1 — „Foto-Delete in der falschen Datenbank"

```powerfx
// Items werden korrekt umgeschaltet:
Items: =Filter(If(varenv = "Sandbox",
                  'PhotoList_Sandbox',
                  'PhotoList_Prod'), ...)

// Aber Remove ist hartcoded auf Sandbox:
Remove('PhotoList_Sandbox', selectedRecord_SP)
```

> 💼 **Was das geschäftlich heißt:** In Produktion löscht die App das falsche Bild — oder gar nichts. Der User sieht „Erfolg", der Datensatz bleibt. Über Monate verschmutzt die Datenbank, niemand merkt es.

**Fix:** 5 Minuten — den `If()`-Block analog zum Items-Pattern einbauen.

### 🔴 Top-Schwachstelle 2 — „Fire-and-forget Flow" (Architektur-Kern)

```json
"flow-document-generation": {
  "runAfter": {}     // ← Flow antwortet sofort, ohne auf Erfolg zu warten
}
```
Plus:
```powerfx
'flow-document-generation'.Run(...);
Patch(proj_workorder_header, currentitem, {Status: "PDF"})  // ← immer
```

> 💼 **Was das geschäftlich heißt:** Wenn der Flow später scheitert (externer Konverter down, Template-Berechtigung weg), bekommt der Endkunde nie sein PDF. App zeigt grün — niemand merkt etwas, bis ein Kunde anruft.

**Fix-Pattern (kurz):**
```
Scope "Hauptlogik"
└── Flow-Inhalt
Scope "Catch" (runAfter: Failed)
├── Status zurück auf "PL"
└── Mail an Admin
Scope "Success" (runAfter: Succeeded)
└── Status auf "PDF" (erst hier!)
```

### 🔴 Top-Schwachstelle 3 — „Identitäts-Drift"

Rolle wird aus O365-Gruppe abgeleitet, Datenzugriff über Dataverse-Rolle gesteuert — **kein Sync zwischen beiden**.

> 💼 **Was das geschäftlich heißt:** Neuer Mitarbeiter sieht eine leere App und glaubt, sie ist kaputt. Ex-Mitarbeiter sieht Monate später noch Kostendaten — **Datenschutz-Issue**.

---

## 🎬 Szene 4 — Cross-Solution-Insight (60 Sek, der „Money Shot")

**Bildschirm:** Beide Solutions nebeneinander, Claudians Antwort dazwischen.

**Claudian sagt (Vorlage):**
> *„Beide Solutions haben den **gleichen Architektur-Fehler** an verschiedenen Stellen: Eine Identität wird an zwei Orten gepflegt — und es gibt keinen Sync-Mechanismus.*
>
> *Das ist kein Bug. Das ist eine **Pattern-Falle**. Ich schreibe das jetzt in deinen Vault als Pattern-Notiz `identity-source-drift`. Beim nächsten Power-Apps-Review erkenne ich das in den ersten 5 Minuten — egal welcher Kunde, egal welche Solution."*

> 💼 **Was das geschäftlich heißt — und das ist die Pointe für die Kunden:**
> Claudian wird nicht müde. Vergisst nicht. Jede Stunde Review baut auf jeder vorherigen auf. **Das Asset wächst mit jeder Session.**

---

## 🎬 Szene 5 — Wissens-Sicherung + Schluss (45 Sek)

Was jetzt im Vault passiert (als Liste einblenden):

1. ✅ Pattern-Notiz `identity-source-drift.md` angelegt — beide Solutions als Trigger-Cases verlinkt
2. ✅ K1-Fix (Foto-Delete) als Code-Snippet bereit — kann sofort ausgerollt werden
3. ✅ Catch-Scope-Template in `30.patterns/` für künftige Flows
4. ✅ „Latente Risiken Q4 2026"-TODO mit Datum gesetzt

**Claudians Schluss-Statement (Vorlage):**
> *„Zwei Solutions, eine Stunde Review, drei P1-Befunde mit Code-Beweis, ein wiederverwendbares Architektur-Pattern — alles im Vault gesichert. Beim nächsten Mal bin ich schneller. Das ist der Unterschied zwischen einem Tool, das antwortet, und einem System, das mit dir lernt."*

**Optional als On-Screen-Text:**
> **Vorher:** halber Tag Code-Review pro Solution.
> **Heute:** Solution rein, Befunde raus, Pattern gespeichert.

---

## 🎬 Regie-Hinweise

### Pre-Flight-Checkliste
- [ ] Fenster-Titel auf neutralen Text (Obsidian-Setting)
- [ ] Sidebar collapsen oder Demo-Ordner mit anonymisierten Namen anlegen
- [ ] Anonymisierungs-Mapping auf 2. Monitor offen
- [ ] Test-Take pro Szene — Claudian variiert leicht zwischen Takes
- [ ] 1080p / 16:9 Recording

### Timing (5 Min gesamt)
- Szene 1 Intro: 30 Sek
- Szene 2 Solution A: 75 Sek
- Szene 3 Solution B: 90 Sek
- Szene 4 Cross-Pattern: 60 Sek
- Szene 5 Wissens-Sicherung + Schluss: 45 Sek

### Optionale Bonus-Szene — ZIP-Workflow
> Wenn du in einem zweiten Durchgang zeigen willst, **wie eine ZIP-Solution ankommt**, kann das so aussehen:
>
> 1. Raoul zieht `.zip` in den Vault
> 2. Frage an Claudian: *„Solution unzippen und Top-5-Risiken in 60 Sekunden"*
> 3. Claudian extrahiert, scannt `Workflows/*.json` + `Src/*.pa.yaml` + `customizations.xml`, liefert priorisierte Liste mit Zeilen-Referenzen
>
> **Pointe:** „Das, was Sie gerade gesehen haben — ich hatte die Solution noch nie zuvor gesehen."

---

## Verwandt

- [[40.meta/claude-projekte-und-custom-ai|Claude Projects & Custom AI — Setup und Teilen]]
- [[40.meta/Claude-Workflows|Claude-Workflows]]
- Original-Solutions (NICHT im Video zeigen):
  - [[50.work/projekte/Koster-AG/Subunternehmerprozess-Koster|Solution A — Original]]
  - [[50.work/projekte/MVM-AG/Regieapp-Schwachstellen-Review|Solution B — Original]]
