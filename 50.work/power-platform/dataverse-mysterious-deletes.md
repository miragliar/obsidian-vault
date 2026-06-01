---
source: claude-import
imported: 2026-06-01
conv_uuids: [c2cb4d7f-5c11-48eb-b7c7-5b5e994ff251]
tags: [dataverse, power-apps, debugging, audit, security, data-loss]
---

# Dataverse — Unerklärte Datenverluste systematisch diagnostizieren

## Problem

Kunde meldet: Datensätze in einer Tabelle sind weg. Die Master-Tabelle hat den Kopf, aber die zugehörigen Detail-Zeilen (`Bestelltabelle`, `Positionen`, etc.) sind verschwunden.

Klassische Konstellation:

- Es gibt **keinen** offensichtlichen Delete-Button in der App
- Es gibt **keinen** Flow, der `Delete` ausführt (du hast nachgesehen)
- Im Trigger-Log eines „on-delete"-Flows sehen Sie reale Delete-Events
- Der Datenverlust passiert wiederholt, scheinbar zufällig

Die Versuchung: Screenshots durch die App jagen. Das skaliert nicht und übersieht garantiert was.

## Lösung

### Schritt 1 — `RunAsSystemUserId` im Delete-Trigger lesen

Wenn du einen „on-delete"-Flow hast, enthält dessen Trigger-Payload:

```json
{
  "body": {
    "SdkMessage": "Delete",
    "RunAsSystemUserId": "b5425aed-ca2e-ed11-9db1-002248829734",
    ...
  }
}
```

Diese GUID zeigt den **Sicherheitskontext**, in dem der Delete lief.

Lookup im Dataverse: `systemuser`-Tabelle nach dieser GUID filtern.

**Drei Szenarien:**

| Wer ist `RunAsSystemUserId`? | Bedeutung | Nächster Schritt |
|---|---|---|
| **SYSTEM** oder Application User | Automatisiert — Cascade Delete, Plugin, Bulk-Delete-Job | Relationships & Cascading prüfen (s.u.) |
| **Echter User** | Hat manuell oder über ein Tool gelöscht | App-Code + Audit-Log + alternative Zugänge prüfen |

### Schritt 2 — Cascade Deletes als #1-Verdächtigen prüfen

**Datenmuster „Kind weg, Parent bleibt"** = klassisch Cascade Delete auf einer **anderen** Lookup-Beziehung als der zum Master.

```
Bestelltabelle.Baustellelookup → Baustelle [Parental/Cascade Delete]
```

→ Sobald jemand eine **Baustelle** löscht, geht **alles** verknüpfte mit (Bestellungen, Positionen, …) — egal wie viele Master-Zeilen davon abhängen.

**Wo prüfen:**

```
Maker Portal → Dataverse → Tabelle (Bestelltabelle) → Relationships
→ jede N:1-Beziehung → "Behavior" / "Type of behavior"
```

Mögliche Werte:

- **Parental / Cascade All** → kaskadiert Delete + Reparent + Assign + Share + Unshare
- **Configurable Cascading** → man kann Delete einzeln steuern (oft `Cascade` oder `Restrict`)
- **Referential, Restrict Delete** → blockiert Delete der Parent-Zeile, wenn Kinder existieren (sicher)
- **Referential** → Lookup wird auf `null` gesetzt, Kind bleibt (sicher)

→ Suche alle Beziehungen mit `Cascade Delete`. **Inkl. Beziehung zum User/Team!** Wenn der `Owner`-Lookup auf Cascade steht und ein User deaktiviert wird, gehen die Owned-Records mit.

### Schritt 3 — App-Source nach `Remove`/`RemoveIf` grepen

Statt dutzende Screens durchzuklicken — App exportieren und Volltext-Suche:

```bash
# .msapp ist ein ZIP
unzip RegieApp.msapp -d /tmp/app_src
cd /tmp/app_src/Src
grep -rn 'Remove(' *.pa.yaml
grep -rn 'RemoveIf(' *.pa.yaml
```

**Was die Power-Apps-Studio-Suche übersieht:**

- Custom Components (interne Properties)
- Komponenten-Library-Templates
- Versteckte Galerie-Item-Properties
- `OnVisible` / `OnHidden` von Screens

Daher der ZIP-Export — er hat **alles**.

### Schritt 4 — Klassischer Logik-Bug: Komma vs. Semikolon im `If`

**Häufiger Bug, der wie ein Cascade aussieht:**

```powerfx
// In App mit Semikolon als Statement-Separator:
If(ThisItem.Status = "Eröffnet";
    Remove(Masters; ThisItem);                          // Statement-Separator!
    RemoveIf(Bestelltabellen; Bestellid = Value(...))   // Statement-Separator!
)
```

In einer Sprache mit `;` als Statement-Trenner und `,` als Argument-Trenner interpretiert Power Fx das als:

- `If(Bedingung; ThenExpr; ElseExpr)` — also drei Argumente
- Bei `Status = "Eröffnet"` → `Remove(Masters, ThisItem)` läuft (Then-Branch)
- Bei `Status ≠ "Eröffnet"` → `RemoveIf(Bestelltabellen, ...)` läuft (Else-Branch) ← **dort werden die Bestellungen gelöscht**

→ User klickt einen Button auf einer Zeile mit Status ≠ Eröffnet → Bestellungen weg.

**Fix:** Kommata zwischen den Statements, dann werden beide ausgeführt (oder, je nach Intent, eine echte `If`-Logik bauen).

### Schritt 5 — Audit-Log einschalten (wenn nicht schon)

```
Power Platform Admin Center → Environment → Settings → Audit and logs
→ Auditing aktivieren
→ Pro Tabelle: "Audit individual record changes" aktivieren
```

Audit zeigt:

- **Wer** hat **was** **wann** gelöscht
- Aus welchem Gerät / welcher IP
- Mit welcher Client-App (Power Apps Mobile, Maker-Portal, Excel-online, etc.)

→ Beantwortet die offenen Restfälle, wenn App-Code und Cascade nichts zeigen.

### Andere Quellen für Deletes außerhalb der App

| Quelle | Wie erkennen |
|---|---|
| Bulk Delete Job | Admin Center → Bulk Delete Jobs |
| „Daten in Excel bearbeiten" (Edit data in Excel) | RunAs = User, Modify-Activity-ID im Audit |
| Direkter Zugriff im Maker-Portal | RunAs = User, Source = Web-UI |
| Power Automate Run aus anderer Solution | Trigger-Logs ALLER Flows in der Env |
| Plugin (custom code) | Plugin Trace Log aktivieren |

## Wann nicht

- **Bei Audit-Log-Verfügbarkeit:** Wenn Audit aktiv ist und du den User/Zeitstempel hast — direkt nachfragen oder im Code an die genaue Stelle springen. Diese ganze systematische Suche ist nur nötig, wenn Audit fehlt oder unzureichend ist.
- **Bei einer kleinen App** (<5 Screens): Die manuelle Code-Inspektion via Studio-Suche kann schneller sein als ZIP-Export.
- **Bei reinen Online-Daten ohne Mobile:** Offline-Sync-Race-Conditions sind keine Option — überspringe diese Hypothese.
- **Bei einem klaren Reproduktionsfall:** Wenn der User den Klick reproduzieren kann → Power Apps Monitor live mitlaufen lassen → der zeigt jeden Patch/Remove in Echtzeit. Viel schneller als Code-Forensik.

## Präventiv

- **Cascade Delete nur, wenn wirklich nötig** — Defaultweg: `Referential, Restrict Delete`
- **`Owner`-Lookup-Cascading** nie auf `Cascade All` (sonst killt Userdeaktivierung Daten)
- **Audit immer an, von Anfang an** — kostet kaum Speicher, rettet Stunden
- **App-Reviews vor Release:** grep nach `Remove`/`RemoveIf` mit Reviewer-Augen
- **Soft-Delete-Pattern** statt Hard-Delete: ein `Status = 'Archiviert'`-Flag und Filter überall einbauen

## Verwandt

- [[50.work/power-platform/powerfx-filter-search-combobox]]
- [[50.work/power-platform/dataverse-offlineprofile]]
- [[50.work/power-platform/power-automate-invalidopenapiflow]]
- [[50.work/power-platform/_conversation-index]]
