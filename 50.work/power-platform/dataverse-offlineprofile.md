---
source: claude-import
imported: 2026-06-01
conv_uuids: [ad2297d4-f6dc-4183-8400-1a9c47683f30]
tags: [dataverse, power-apps, mobile, offline, profile, solution, alm]
---

# Dataverse Mobile Offline-Profile — Konfiguration & Schema-Mismatches

## Problem

Power Apps Mobile App soll offline funktionieren (Außendienst, Baustelle, schlechtes Netz). Beim Speichern oder Öffnen erscheint:

```
table rrpt_regiekopf has no column named cr19a_baustellelookup!id
```

oder die Galerie zeigt keine Daten, obwohl „Bereit" angezeigt wird und alle Tabellen synchronisiert sind.

Ursachen (typischerweise mehrere gleichzeitig):

- **Schema-Mismatch:** lokale SQLite kennt eine kürzlich hinzugefügte Spalte nicht
- **Lookups nicht inkludiert:** Lookup-Felder werden **nicht automatisch** ins Profil aufgenommen, auch wenn die Ziel-Tabelle drin ist
- **Auto-generiertes Offline-Profil:** lebt außerhalb der Solution, kein ALM, keine Versionierung
- **Falsche Daten-Filter:** „Nur eigene Records" statt „Alle Records" bei Stammdaten

## Lösung

### Architektur-Grundsatz: Manuelles Offline-Profil in Solution

**Auto-Profile nicht verwenden.** Sie

1. liegen außerhalb der Solution → kein Deployment
2. updaten sich nicht bei Schema-Änderungen
3. lassen sich **nachträglich nicht** in eine Solution aufnehmen

**Vorgehen:**

```
Solution → New → Mobile → Mobile offline profile
Name: rrpt_RegieRapport_OfflineProfile
```

→ Alle relevanten Tabellen hinzufügen, **inkl. aller Stammdaten-Tabellen**, die per Lookup referenziert werden.

### Filter-Regeln pro Tabelle (das Schlüsselkonzept)

Beim Hinzufügen einer Tabelle muss man wählen: **welche Zeilen sollen aufs Gerät?**

| Option | Bedeutung | Wann verwenden |
|---|---|---|
| **Organisationszeilen / Benutzerzeilen** | Owner = aktueller User | User-owned Transaktionsdaten (nur „meine Records") |
| **Team-Zeilen / Unternehmenseinheit** | Owner = Team / BU | Team-basierte Sicherheit |
| **Alle Zeilen** | Komplette Tabelle | Stammdaten (kleine, alle User brauchen sie) |
| **Nur verknüpfte Zeilen** ⭐ | Über Beziehung zu anderer Offline-Tabelle | Transaktions-Detail-Tabellen (`Positionen` zu einem `Master`) |
| **Benutzerdefiniert (FetchXML)** | Beliebige Filter | Komplexe Szenarien („nur letzte 30 Tage") |

### Konkretes Datenmodell-Beispiel (Rapport-App)

```
Regiekopf (Master, user-owned)
├── → Baustelle (Lookup, Stammdaten)
├── ← Arbeitsbeschriebzeile (N:1 zu Regiekopf)
├── ← Materialzeile (N:1 zu Regiekopf)
│      └── → Materialkatalog (Lookup, Stammdaten)
└── ← Personenzeile (N:1 zu Regiekopf)
       └── → Mitarbeitertypen (Lookup, Stammdaten)
```

**Empfohlene Filter:**

| Tabelle | Filter | Begründung |
|---|---|---|
| `Regiekopf` | Benutzerzeilen (oder Team) | Transaktionsdaten |
| `Baustelle` | Alle Zeilen | Stammdaten, Lookup-Target |
| `Materialkatalog` | Alle Zeilen | Stammdaten |
| `Mitarbeitertypen` | Alle Zeilen | Stammdaten |
| `Arbeitsbeschriebzeile` | Nur verknüpfte Zeilen (über Regiekopf) | Detail einer Master-Row |
| `Materialzeile` | Nur verknüpfte Zeilen (über Regiekopf) | Detail |
| `Personenzeile` | Nur verknüpfte Zeilen (über Regiekopf) | Detail |
| `Übersetzungstabelle` | Alle Zeilen | Lookupfrei, klein |
| `Zeitachse` | Alle Zeilen | Lookupfrei, klein |

**Pflicht-Schritt nach Tabellen-Auswahl:** für jede „Nur verknüpfte Zeilen"-Wahl die **Beziehung explizit aktivieren** (`+` auf der Regiekopf-Beziehung). Sonst wird nichts geladen.

### Schema-Updates publishen

Nach Änderungen an der Tabelle (neue Spalte/Lookup): das Profil hat das **nicht automatisch**. Workflow:

1. Profil im Maker-Portal öffnen
2. Spalten der betroffenen Tabelle prüfen und ergänzen (Lookups: auch das Lookup-Feld selbst!)
3. Profil **republishen**
4. Auf dem Gerät: App schließen → „Mobile offline-Synchronisierung" → ggf. **Cache leeren** (iOS: App-Daten löschen + neu installieren ist der zuverlässigste Weg, „Sync erneuern" in der App reicht oft nicht)
5. Komplett re-synchronisieren

### Schema-Mismatch-Diagnose

Fehlertext `table X has no column named Y` → Y ist in Dataverse vorhanden, aber **nicht im Profil** oder **lokal noch nicht resynced**.

| Schritt | Was prüfen |
|---|---|
| 1 | Im Profil: ist `Y` als Spalte der Tabelle inkludiert? |
| 2 | Ist `Y` ein Lookup? Dann zusätzlich: Ziel-Tabelle im Profil & explizit referenziert |
| 3 | Profil republished nach Hinzufügen? |
| 4 | Gerät komplett resynced (App-Daten cleared)? |
| 5 | App-Formel: nutzt sie `Y.Id` oder `Y` direkt? Manche Sync-Bugs treffen nur `.Id`-Zugriffe |

## Wann nicht

- **App braucht nicht offline zu funktionieren:** Keine Offline-Profile anlegen — sie sind Maintenance-Overhead.
- **Kleine App, alle Daten auf alle Geräte:** Bei <1000 Rows Gesamtvolumen pragmatisch „Alle Zeilen" für alle Tabellen — keine Filter-Komplexität nötig.
- **Bei reinen Web-Apps:** Offline-Profile gelten nur für Mobile App (`iOS/Android Power Apps`). Browser-Apps ignorieren sie.
- **Bei strenger Datentrennung pro Team:** Power Apps Mobile Offline respektiert Security Roles auf Server-Seite **vor** dem Profil-Filter. „Alle Zeilen" liefert trotzdem nur, was die Rolle erlaubt.

## Performance-Faustregeln

- Pro Tabelle: lieber **wenige Spalten** ins Profil als alle. Spalten-Liste explizit setzen statt `*`.
- **Anhänge, Notizen, große Bilder** nur inkludieren, wenn essenziell — sonst explodiert das lokale DB-Volumen.
- **Initial Sync** kann auf Mobilgeräten Minuten dauern. User darauf vorbereiten.
- Lookups in der App lieber per **Owner-Lookup** als per Tiefen-Hierarchie referenzieren — flacher = bessere Sync-Performance.

## Verwandt

- [[50.work/power-platform/powerfx-hidden-datacard-submitform]] — viele Submit-Bugs treten nur offline auf
- [[50.work/power-platform/dataverse-mysterious-deletes]]
- [[50.work/power-platform/_conversation-index]]
