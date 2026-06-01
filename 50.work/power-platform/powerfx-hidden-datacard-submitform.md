---
source: claude-import
imported: 2026-06-01
conv_uuids: [46548c10-c314-4be6-ba48-5743f4f4c181]
tags: [power-fx, power-apps, form, datacard, submitform]
---

# PowerFx — Hidden Datacard speichert nicht beim SubmitForm

## Problem

In einem Edit-Form gibt es Datacards, die der User nicht sehen soll (z.B. ein automatisch gesetztes Status-Feld, ein Default-User, eine berechnete Kategorie). Naheliegender Reflex: `Visible = false`.

Beim `SubmitForm` wird der Wert **nicht** in Dataverse geschrieben. Das Update-Property hat einen Wert, der Submit erfolgt fehlerfrei — aber das Feld im Record bleibt leer oder behält den alten Wert.

Dieser Bug kostet bei Fehlersuche schnell eine halbe Stunde, weil:

- Das `Update`-Property der Datacard sieht korrekt aus
- `SubmitForm` wirft keinen Fehler
- Im Studio funktioniert es im Preview, im publishten App nicht (oder umgekehrt)

## Lösung

**Power Apps ignoriert beim `SubmitForm` das `Update`-Property jeder Datacard, deren `Visible = false` ist.** Das ist dokumentiertes Verhalten, nicht Bug, aber unerwartet.

Statt `Visible = false`: die Card per Größe verstecken.

```powerfx
// Auf der DataCard:
Height: 0
Visible: true   // <-- bleibt true!
```

Alternativ kann das **innere Control** (TextInput, Dropdown) ausgeblendet werden, während die Card selbst sichtbar bleibt:

```powerfx
// Auf dem inneren Control (z.B. DataCardValue1):
Visible: false
// Die Card selbst:
Visible: true
Height: 1   // oder 0, je nach Layout-Verhalten
```

### Pattern: Default-Wert immer schreiben

Häufiger Use Case — Feld soll beim Anlegen immer mit einem Default befüllt werden, ohne dass der User es sieht:

```powerfx
// DataCard.Update:
"Status_Neu"
// DataCard.Visible:
true
// DataCard.Height:
0
```

### Pattern: Dynamischer Default aus anderem Control

```powerfx
// DataCard.Update:
Coalesce(DataCardValue_Status.Selected.Value; "Neu")
// Height: 0, Visible: true
```

### Validierung des Workflows

1. Card im Studio sichtbar machen → Wert testen
2. `Height: 0` setzen
3. SubmitForm im Preview ausführen
4. In Dataverse prüfen (nicht nur in der App-Anzeige!) ob das Feld geschrieben wurde

## Wann nicht

- **Bei wirklich optionalen Feldern** (User soll selbst entscheiden, ob er Wert eingibt): dann ist `Visible = true` und ein leeres Control korrekt — kein Hide-Workaround nötig.
- **Wenn du das Feld nur lesen willst, nie schreiben:** Display-Form (Form-Modus „View") schreibt sowieso nichts — keine Update-Logik nötig.
- **Wenn der Wert via `Patch()` getrennt vom Form gesetzt wird:** Dann ist das Form irrelevant, du schreibst direkt — und die Datacard kann auch ausgeblendet bleiben (`Visible = false`) ohne Datenverlust, weil sie eh nicht beim Submit beteiligt ist.
- **Bei Anti-Pattern „Phantom-Card für Geschäftslogik":** Wenn du eine Card nur einbaust, damit `Update` ein Wert berechnet, ist das brüchig. Berechnung gehört in eine `Set()`-Variable oder direkt ins `Update` der echten Card, nicht in eine Phantom-Card.

## Diagnose-Checkliste, wenn ein SubmitForm „leise versagt"

| Symptom | Ursache | Fix |
|---|---|---|
| Feld bleibt leer trotz Update-Wert | Card hat `Visible = false` | `Height = 0`, `Visible = true` |
| Wert kommt mit `null` an | `Update` referenziert nicht-existentes Control | Control-Namen prüfen |
| Submit wirft `Required-field` Fehler bei verstecktem Feld | DataCard-Property `Required = true` greift trotzdem | `Required = false` setzen wenn Feld optional |
| SubmitForm scheint zu funktionieren, Refresh zeigt alten Wert | Caching / Form muss `ResetForm` + `Refresh(Datasource)` | Nach Submit: `Refresh(Datasource); ResetForm(Form1)` |
| Nur im Mobile fehlt der Wert | Offline-Profil kennt das Feld nicht | siehe [[50.work/power-platform/dataverse-offlineprofile]] |

## Verwandt

- [[50.work/power-platform/powerfx-filter-search-combobox]]
- [[50.work/power-platform/dataverse-offlineprofile]]
- [[50.work/power-platform/_conversation-index]]
