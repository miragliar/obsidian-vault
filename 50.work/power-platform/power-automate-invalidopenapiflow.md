---
source: claude-import
imported: 2026-06-01
conv_uuids: [58e514e7-5db8-4622-b227-e627324ab45a]
tags: [power-automate, flow, error, debugging, openapi]
---

# Power Automate — `InvalidOpenApiFlow` beim Speichern diagnostizieren

## Problem

Beim **Speichern** eines Flows wirft Power Automate:

```
Flow client error returned with status code "BadRequest"
and details "InvalidOpenApiFlow".
```

Im UI sind **keine** roten Markierungen sichtbar. Der Flow „funktioniert" beim manuellen Test, aber lässt sich nicht persistieren. Häufiger Auslöser: man hat eine Variable umbenannt/gelöscht, einen Trigger angepasst oder Schritte kopiert.

Die UI-Validierung von Power Automate ist nicht JSON-vollständig — sie zeigt nur Auswahl-Felder, lässt aber Schema-Verstöße auf JSON-Ebene durchschlüpfen, die der Backend-OpenAPI-Validator dann ablehnt.

## Lösung

**Diagnose-Reihenfolge** (von schnell-zu-langsam):

### 1. Häufige Auslöser durchgehen

| Ursache | Fix |
|---|---|
| **Leerzeichen oder Sonderzeichen** in Variablen-/Aktionsnamen | Umbenennen: nur `A-Za-z0-9_` |
| **Doppelte Action-Namen** (entstehen beim Kopieren) | Betroffene Schritte umbenennen — interner Name muss eindeutig sein |
| **Leere Condition/Apply-to-each-Branches** | Jeden Branch mit mind. 1 Aktion füllen oder ganz löschen |
| **Trigger-Eingabefeld ohne `name`** | Manual-Trigger-Inputs prüfen, jedes Feld benennen |
| **Verwaiste Referenzen** nach Variable-Löschen | Codeansicht öffnen, Volltextsuche nach altem Namen |
| **Ungültiges JSON-Schema** in Parse-JSON-Aktion | Schema im Editor validieren (Pretty-Print → Online-JSON-Linter) |
| **Custom Connector mit kaputter OpenAPI-Definition** | Connector neu publishen oder Aktion entfernen |
| **Import aus anderer Umgebung** mit gebrochenen Referenzen | Connections neu binden, Environment-Variables prüfen |

### 2. Codeansicht öffnen

```
Flow oben rechts → "..." → "Codeansicht anzeigen"
```

Worauf konkret schauen (mit `Ctrl+F`):

- `"name": ""` → leerer Parameter-Name
- `"type": null` oder fehlender `type` in einem Input → Schema-Lücke
- Doppelte `operationId`
- `$ref`-Referenzen auf nicht-existierende Aktionen
- Sonderzeichen in `description` (`"`, `<`, `>` unescaped)
- Alte Variable-Namen, die übersehen wurden

**Konkretes Beispiel aus der Praxis:** Eine Variable mit Leerzeichen im Namen (`"name": "Ablagestruktur Ordner"`) wird vom Frontend toleriert, vom OpenAPI-Validator beim Save aber als ungültig abgelehnt. → ohne Leerzeichen umbenennen, alle Referenzen anpassen, **dann** speichern.

### 3. Flow als Solution exportieren und JSON inspizieren

Wenn die Codeansicht nicht weiterhilft:

```
Solution → Export Solution → Unmanaged
```

→ ZIP enthält `workflows/{flowname}.json` — vollständiges Schema. In einem JSON-Editor mit Schema-Validierung öffnen.

### 4. Nuclear Option: leeren Flow + Aktionen einzeln zurückkopieren

Manchmal ist der Flow strukturell so kaputt, dass Debugging länger dauert als Neubau:

1. Neuen leeren Flow anlegen (gleicher Trigger)
2. Aktionen **einzeln** rüberkopieren (per Copy/Paste-from-Clipboard)
3. Nach jeder Aktion speichern → so identifiziert man die kaputte Aktion

## Wann nicht

- **Wenn der Fehler beim Ausführen kommt** (nicht beim Speichern): Das ist kein `InvalidOpenApiFlow`, sondern ein Runtime-Fehler. Schau in den Run-History-Logs auf die fehlgeschlagene Aktion.
- **Wenn das UI rote Markierungen zeigt:** Nicht auf JSON-Ebene suchen — UI-Fix reicht, schneller.
- **Bei Custom Connector-Problemen:** Der Fehler liegt im Connector-Swagger, nicht im Flow. Connector-Definition validieren (im Maker-Portal unter „Custom Connectors" → „Test/Definition").
- **Bei `BadGateway` oder `InternalServerError`:** Das ist Microsoft-seitig — kurz warten, neu versuchen, ggf. Status-Page checken.

## Präventiv: Save-Disziplin

- Nach **jeder** Variablen-Umbenennung sofort speichern → wenn's bricht, weißt du wo
- Niemals 3 Variablen am Stück löschen und „dann mal speichern"
- Aktionen, die du copy-paste-st, sofort umbenennen (sonst Name-Duplikate)
- Bei größeren Refactorings: vorher Solution-Export als Backup

## Verwandt

- [[50.work/power-platform/power-automate-string-expressions]] — die häufigste Folgefrage nach „Flow läuft, aber Werte falsch"
- [[50.work/power-platform/dataverse-mysterious-deletes]] — wenn ein „kaputter" Flow versehentlich Daten löscht
- [[50.work/power-platform/_conversation-index]]
