---
name: Power Apps — Navigate() bricht OnSelect-Cleanup + Mobile-Touch-Falle bei Inline-Edit
slug: powerapps-navigate-bricht-onselect-cleanup
type: pattern
kategorie: power-platform
tags: [miraglia, power-apps, powerfx, navigate, onselect, mobile, touch, state-leak, edit-modus]
status: aktiv
created: 2026-06-11
quelle: MVM-AG Regieapp Kopierfunktion Mobile-Bug (2026-06-11)
verwandt: [powerfx-deutsche-lokalisierung, powerfx-disambiguation-und-as-operator]
---

# Power Apps — Navigate() bricht OnSelect-Cleanup + Mobile-Touch-Falle bei Inline-Edit

> **Worum geht's:** Du baust eine Galerie mit Inline-Edit-Modus (`Set(varEdit, ThisItem.'Id')` als Schalter) und einem Button, der nach erfolgreichem Patch via `Navigate()` weiterspringt. Auf Desktop läuft alles, auf Mobile springt zufällig ein Item in den Edit-Modus, oder der Edit-Modus persistiert über Screen-Wechsel. **Zwei Bug-Klassen treffen zusammen** — beide musst du adressieren.

## Bug 1: `Navigate()` ist ein terminaler Befehl

`Navigate()` (und ähnlich `Back()`, `Launch()` mit Target Self) **bricht den restlichen Code im selben Handler ab**. Was nach `Navigate` steht, wird im Success-Pfad NIE ausgeführt.

```powerfx
=IfError(
    // Success
    ... Patches ...
    Notify("Erfolg");
    Navigate(ZielScreen);        // ← Code stoppt hier
    Set(varCleanup, Blank()),    //   wird NIE erreicht
    
    // Catch
    Notify("Fehler")
);
Refresh(Datenquelle);            // wird im Success NIE erreicht
Set(varCleanup, Blank())         // wird im Success NIE erreicht
```

**Symptom:** State-Variablen (wie `varEdit`, `visibleedit`, `varSubmitting`, `varSelected`) bleiben nach dem Navigate „dirty". Sobald der User zum Quell-Screen zurückkommt, ist die UI in einem komischen Zustand.

**Fix:**
1. Cleanup-Variablen **VOR** dem `Navigate` setzen, nicht danach
2. Plus: **globaler Reset im `OnVisible`** des Quell-Screens als Sicherheitsnetz

## Bug 2: Mobile-Touch-Propagation triggert benachbarte Buttons

Auf Mobile-Touch hat ein Tap eine effektive Zone von ~±10 Pixel um den Centroid. Wenn zwei klickbare Controls vertikal nah beieinander sitzen (z.B. zwei kleine Icon-Buttons mit `Height: 25–27`), kann ein einziger Tap **beide Controls treffen** — Power Apps Mobile feuert dann beide `OnSelect`-Events sequentiell. Auf Desktop kommt das nicht vor, weil Maus-Klicks pixel-genau sind.

Klassisches Anti-Pattern:
- Edit-Button mit `OnSelect: =Set(varEdit, ThisItem.'Id')` bei `Y=0, Height=27`
- Copy-Button mit `OnSelect: =Patch(…); Navigate(…)` bei `Y=31, Height=36`
- Auf Mobile-Tap: beide feuern → Edit-Modus springt UND Copy läuft

## Die kombinierte Falle (genau dieser Fall, MVM-Regieapp 06.2026)

1. User tippt auf Mobile auf den **Copy-Button** (Y=111 z.B.)
2. Touch-Zone berührt den Edit-Button mit (Edit feuert zuerst):
   - `varDuplicating` ist noch `false` → Schutz-If greift nicht
   - `Set(visibleedit, ThisItem.'Rapport-ID')` → Edit-Modus an
3. Copy-Button feuert danach:
   - `Set(varDuplicating, true)` → Lock setzen
   - Patches laufen
   - `Set(visibleedit, Blank())` steht NACH `Navigate(Personen)` → wird **nicht erreicht**
   - `Navigate(Personen)` → Screen-Wechsel
4. User wechselt später zurück zum Galerie-Screen
5. `visibleedit` ist immer noch auf der alten Rapport-ID → Item rendert im Edit-Modus

→ User glaubt, Copy hätte Edit ausgelöst. Diagnose-Spur: keine Notify, keine Fehlermeldung, einfach „die UI ist falsch".

## Drei-Layer-Lösung

### Layer 1: Cleanup AM ANFANG des kritischen Buttons

Übersteuere alles, was ein anderer Touch-getriggerter Handler vorher gesetzt haben könnte:

```powerfx
=Set(visibleedit, Blank());          // ← allererste Zeile, übersteuert Edit-Trigger
If(varDuplicating, ... Exit());
Set(varDuplicating, true);
...
```

### Layer 2: Cleanup VOR dem Navigate

Im Success-Pfad, eine Zeile vor dem terminalen Befehl:

```powerfx
IfError(
    ...
    Set(varDuplicating, false);
    Set(visibleedit, Blank());                  // ← VOR Navigate
    Navigate(ZielScreen, ScreenTransition.Fade),
    ...
)
```

### Layer 3 (entscheidend): Globaler Reset im `OnVisible`

Auf dem Galerie-Screen, Eigenschaft `OnVisible`:

```powerfx
=Set(visibleedit, Blank())
```

Egal von wo der User zurückkommt — beim Eintritt in den Screen ist der State garantiert sauber. Das ist der eigentliche Game-Changer: alle anderen Patches sind defensive Mitigationen, dieser ist der **architektonische Fix**.

## Generalisierte Regel

> **Jede State-Variable, die UI-Zustände innerhalb eines Screens steuert** (`varEdit`, `varSelected`, `varMode`, `varSubmitting`, …), muss im `OnVisible` des betreffenden Screens **explizit auf den Default zurückgesetzt** werden.

Sonst lecken State-Reste über Screen-Wechsel — und das passiert garantiert, sobald irgendwo `Navigate()` in einem `OnSelect` nach einem `Set` steht.

## Anti-Patterns

- ❌ `OnSelect = …; Navigate(X); Set(cleanup, Blank())` — Set nach Navigate ist tot
- ❌ State-Variable nur in Save/Cancel-Buttons zurücksetzen — Screen-Wechsel umgeht die
- ❌ Sich auf `If(varLock, …)`-Guards verlassen, wenn die Reihenfolge der OnSelect-Aufrufe auf Mobile unklar ist
- ❌ Zwei kleine Icon-Buttons vertikal mit nur wenigen Pixeln Abstand stapeln (Touch-Zone-Overlap)

## Pro-Patterns

- ✅ `OnVisible = Set(varEdit, Blank())` auf jedem Screen mit Inline-Edit-Modus
- ✅ Cleanup VOR Navigate, nicht danach
- ✅ Cleanup AM ANFANG eines neuen Aktion-Buttons (übersteuert evtl. von Touch-Propagation gesetzten State)
- ✅ Buttons mit mind. 16px Abstand vertikal — oder horizontal trennen
- ✅ `Notify(...)`-Tracer in OnSelect-Handler einbauen während Mobile-Debug, um Trigger-Reihenfolge zu sehen

## Diagnose-Pattern wenn der Bug auftritt

Notify-Trace temporär einbauen:

```powerfx
// Verdächtiger Edit-Button OnSelect:
=Notify("Edit-Button: " & ThisItem.'Id' & " | varLock=" & varDuplicating);
If(varDuplicating, false, Set(visibleedit, ThisItem.'Id'))

// Verdächtiger Aktions-Button OnSelect:
=Notify("Aktions-Button: " & ThisItem.'Id');
...
```

Auf Mobile testen. Reihenfolge der Toasts zeigt dir:
- Welche Handler überhaupt feuern (manchmal nur einer, manchmal beide)
- In welcher Reihenfolge
- Mit welchen Variable-Werten

## Verwandt

- [[50.work/power-platform/powerfx-deutsche-lokalisierung|PowerFx Deutsche Lokalisierung]]
- [[50.work/power-platform/powerfx-disambiguation-und-as-operator|PowerFx Disambiguation und As-Operator]]
- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung als Flow-Save-Voraussetzung]] — ähnliches stille-Inkonsistenz-Pattern (Save schlägt fehl, App sagt Erfolg)
- [[50.work/projekte/MVM-AG/Regieapp-Neubau-MVM|Regie-Rapport-App MVM]] — Ursprungs-Fall (Mobile-Bug Kopierfunktion 2026-06-11)
- [[50.work/projekte/MVM-AG/Regieapp-Schwachstellen-Review|Regie-App Schwachstellen-Review]] — K33 (varSubmitting nicht zurückgesetzt nach Navigate) ist die gleiche Bug-Klasse
