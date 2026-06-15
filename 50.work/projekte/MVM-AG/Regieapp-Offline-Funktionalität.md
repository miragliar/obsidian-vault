---
name: Regie-Rapport-App — Offline-Funktionalität
slug: Regieapp-Offline-Funktionalität
parent_project: "[[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]]"
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: In Arbeit
zeitraum: Mai 2026 — laufend
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, power-apps, dataverse, offline, mobile, cross-tenant]
type: projekt-sub-hub
created: 2026-06-15
updated: 2026-06-15
---

# Regie-Rapport-App — Offline-Funktionalität

**Eltern-Projekt:** [[Regieapp-Neubau-MVM|Regie-Rapport-App (Neubau)]]
**Status:** In Arbeit (Quick-Fix „App via Teams" akzeptiert, echter Fix offen)
**Letztes Symptom:** Foto-Hochladen scheitert bei Giuseppe Garofano (Zug-Tenant) via nativem Power-Apps-Client (Remo, 11.06.2026)

## Worum es geht

Die Regie-Rapport-App muss im Aussendienst funktionieren — auf der Baustelle, oft ohne Netz. Dataverse-Offline-Profile sind die zentrale Voraussetzung. Aktueller Stand: **eingeschränkt stabil**; Quick-Fix für die Anwender ist „die App via Teams-Client öffnen", weil Teams-eingebettete Power Apps weniger Offline-Anforderungen haben.

## Aktueller Stand (15.06.2026)

| Bereich | Stand | Quelle |
|---|---|---|
| Dataverse-Offline-Profil (manuell, in Solution) | ✅ Architektur definiert | [[50.work/power-platform/dataverse-offlineprofile|Pattern-Notiz]] |
| Tabellen-Filter (Stammdaten = „Alle", Detail = „Verknüpfte") | ✅ definiert | s.o. |
| Schema-Republish nach Spalten-Änderungen | 🟡 manueller Prozess, fehleranfällig | s.o. |
| Cross-Tenant-Szenario Zug (`mvm-ag-zug.ch`) | 🔴 ungetestet, evtl. ursächlich für Garofano-Symptom | Remo 11.06. |
| Foto-Upload offline (SharePoint-Listen) | 🔴 nicht offline-fähig (K35) | [[Regieapp-Schwachstellen-Review#K35]] |
| Cascade-Delete im Client | 🟡 nicht atomar (K34) — kann Sync-Drift verursachen | [[Regieapp-Schwachstellen-Review#K34]] |
| Home-Galerie Sync-Fehler-Handling | 🔴 kryptische Default-Fehlermeldung | [[Regieapp-Neubau-MVM#Rizzo Isacco]] |

## Bekannte Symptome — Case-by-Case

### Case 1 — Giuseppe Garofano (Zug-Tenant), 11.06.2026
- **User:** Giuseppe Garofano, Maler, MVM AG Zug
- **Domain:** `mvmgga@mvm-ag-zug.ch` — **anderer Tenant** als Haupt-MVM (`mvm-ag.ch`)
- **Symptom:** Foto-Hochladen scheitert in der nativen Power-Apps-App. Via Teams-eingebettet funktioniert es.
- **Status:** **Quick-Fix kommuniziert** („App via Teams"), Remo hat das mit *„Sehr gut, danke für die Info"* akzeptiert.
- **Annahme zur Root Cause** (zu verifizieren): Kombination aus K35 (SharePoint-Liste für Bilder ist nicht offline-fähig) + Cross-Tenant-Auth (Power-Apps-Client cached Token pro Tenant; Wechsel oder Refresh kann fehlschlagen).
- **Bemerkung:** Garofano sieht eine Fehlermeldung („dieses Bild" — Remo bezieht sich auf einen Screenshot im Original-Mail). Screenshot ggf. nachfordern, falls Diagnose nötig.

### Case 2 — Rizzo Isacco, 10.06.2026
- **Symptom 1:** Banner „Fehler beim Abrufen von Daten aus dem Netzwerk" auf Home-Galerie.
- **Symptom 2:** Beim Löschen: *„You cannot delete this record because it doesn't exist in the offline mode"* (Code `-2147093944`).
- **Diagnose:** Offline-Sync-Drift. Cache enthält den zu löschenden Record nicht (Sync nicht durchgelaufen oder Record erst nach letztem Sync entstanden).
- **Fix-Hierarchie:**
  1. **Sofort (non-code):** App schliessen → bei stabilem Netz neu öffnen → 30s Sync abwarten → erneut versuchen.
  2. **Hotfix (1–2h, code):** `IfError`-Wrap um den Home-Delete-Block (`Home.pa.yaml` Z. 423–450) mit user-friendly Notification.
  3. **Echter Fix:** K34 — Dataverse-Beziehungen auf `CascadeDelete = Cascade` umstellen, dann atomarer Single-`Remove(Regiekopf, ThisItem)`.
- **Screenshots:** `regie-app-screenshots/2026-06-10_rizzo_netzwerk-fehler-home.png` und `…_remove-offline-fehler.png`

## Architektur — Solls (aus Pattern-Notiz destilliert)

> Voll dokumentiert in [[50.work/power-platform/dataverse-offlineprofile|Mobile Offline-Profile]].

### Manuelles Profil in Solution
Auto-generiertes Offline-Profil = nutzlos (kein ALM, kein Schema-Update). Eigenes Profil in der Solution anlegen: `rrpt_RegieRapport_OfflineProfile`.

### Filter-Regeln pro Tabelle

| Tabelle | Filter | Begründung |
|---|---|---|
| `Regiekopf` | Benutzerzeilen | User-owned Transaktionsdaten |
| `Baustelle` | Alle Zeilen | Stammdaten, Lookup-Target |
| `Materialkatalog` | Alle Zeilen | Stammdaten |
| `Mitarbeitertypen` | Alle Zeilen | Stammdaten |
| `Arbeitsbeschriebzeile` | Nur verknüpfte (über Regiekopf) | Detail einer Master-Row |
| `Materialzeile` | Nur verknüpfte (über Regiekopf) | Detail |
| `Personenzeile` | Nur verknüpfte (über Regiekopf) | Detail |
| `Übersetzungstabelle` | Alle Zeilen | klein, kein Lookup |
| `Zeitachse` | Alle Zeilen | klein, kein Lookup |

**Pflicht nach jeder Tabellen-Auswahl:** Beziehung explizit aktivieren (`+` auf der Regiekopf-Beziehung in der Detail-Tabelle). Sonst lädt nichts.

### Schema-Update-Prozess (manuell, fehleranfällig)
1. Profil im Maker-Portal öffnen
2. Spalten der betroffenen Tabelle prüfen / neue Lookups auch das **Lookup-Feld selbst** aufnehmen
3. Profil **republishen**
4. Auf dem Gerät: App schliessen → Cache leeren → resync
5. Komplette Resync abwarten (kann auf Mobile Minuten dauern)

## Bekannte Gaps / Verbesserungs-Backlog

### Gap A — Fotos nicht offline-fähig (K35, P3)
- **Status quo:** Fotos laufen über SharePoint-Listen (`Regie-Bilder` / `Regie-Bilder_1`). Power-Apps-Offline-Profile unterstützen primär Dataverse — SharePoint-Listen sind eingeschränkt.
- **Folge:** MA auf Baustelle ohne Netz kann zwar Personen/Material erfassen, **aber keine Bilder**. Das ist der vermutete Garofano-Pfad.
- **Fix:** Bilder in Dataverse-File-Field migrieren. Tabelle `rrpt_foto` ist bereits in der Solution deployed, aber leer/ungenutzt (siehe B1 im Schwachstellen-Review).
- **Aufwand:** mittel (Schema-Migration, Sync-Setup, App-Refactor `Fotos.pa.yaml`).

### Gap B — Cascade-Delete im Client (K34, P1)
- **Status quo:** Beim Löschen eines Rapports werden Details (Arbeitsbeschriebzeilen, Materialzeile, Personenzeile) im Client per `RemoveIf` einzeln gelöscht. Nicht atomar — wenn nach dem Master-Delete das Netz abbricht, hängen die Detail-Rows als Waisen herum.
- **Fix:** Dataverse-Beziehungen auf `CascadeDelete = Cascade` setzen, dann ein einzelnes `Remove(Regiekopf, ThisItem)` reicht. Server-seitige Atomarität.
- **Bonus:** Löst auch den Rizzo-Isacco-Sync-Drift-Symptom.

### Gap C — Error-Handling Home-Galerie (P1)
- **Status quo:** Kryptische Default-Meldung bei Offline-Sync-Fehlern (Rizzo-Case).
- **Fix:** `IfError`-Wrap mit `Notify("Bitte App komplett schliessen und mit stabilem Netz neu starten."; NotificationType.Error)`.
- **Aufwand:** 1–2h. Sofort umsetzbar.

### Gap D — Cross-Tenant-Auth (Garofano-Case)
- **Status quo:** ungeprüft. Sample-Hypothese: Power-Apps-Mobile-Client cached MSAL-Token pro Tenant. Wechsel zwischen Haupt- und Zug-Tenant kann Token-Refresh-Fehler triggern.
- **Test-Vorgehen:**
  1. Garofano-Gerät reproduzieren (oder Test-Account im Zug-Tenant)
  2. Auf nativem Power-Apps-Client: kompletter Logout + Re-Login + Sync
  3. Foto-Upload-Pfad isoliert testen vs. Teams-eingebettet
  4. Logs aus Power-Apps-Diagnose-Modus ziehen (Shake-to-Diagnostics auf iOS/Android)

### Gap E — Schema-Republish-Drift
- **Status quo:** Bei jeder Tabellen-/Spalten-Änderung muss das Profil manuell republished + auf jedem Gerät resynced werden. Vergisst man's, fliegen Fehler à la `table X has no column named Y`.
- **Mitigation:** Solution-Build-Checkliste, Release-Notes pro Profil-Update an alle User.
- **Echter Fix:** Profil-Update in den CI-Build aufnehmen (so etwas wie `pac solution import` mit Mobile-Offline-Step) — ALM-Thema.

## Test-Matrix (zu pflegen)

| Tenant | Gerät | Client | Foto-Upload | Sync-Fehler-Recovery | Cascade-Delete |
|---|---|---|---|---|---|
| Haupt (`mvm-ag.ch`) | iOS | Power Apps native | ? | ? | ? |
| Haupt | iOS | Teams-eingebettet | ✅ (per Remo) | ? | ? |
| Haupt | Android | Power Apps native | ? | ? | ? |
| Haupt | Desktop | Browser | n/a (offline n/a) | n/a | ? |
| **Zug** (`mvm-ag-zug.ch`) | ? | Power Apps native | 🔴 (Garofano 11.06.) | ? | ? |
| Zug | ? | Teams-eingebettet | ✅ (Quick-Fix akzeptiert) | ? | ? |

## Quell-Conversations (Claude-Export)

| msgs | Datum | Titel | UUID |
|---:|---|---|---|
| 46 | 2026-05-20 | Offlineprofil Fehler beim Speichern und Öffnen | `ad2297d4-f6dc-4183-8400-1a9c47683f30` |
| 8 | 2026-05-13 | Tabelle Environment Variable Value offline schalten | (siehe `_conversation-index`) |

## Verwandte Pattern-Notizen

- [[50.work/power-platform/dataverse-offlineprofile|Mobile Offline-Profile — Konfiguration & Schema-Mismatches]] — die zentrale Anleitung
- [[50.work/power-platform/dataverse-mysterious-deletes|Cascade-Delete-Diagnose]] — zu Gap B / K34
- [[50.work/power-platform/powerapps-navigate-bricht-onselect-cleanup|Navigate() bricht OnSelect-Cleanup]] — relevant für Sync-State-Resets im OnVisible
- [[50.work/power-platform/sharepoint-berechtigung-flow-save|SharePoint-Berechtigung Flow-Save]] — zu Gap A (SharePoint-Bilder)

## Roadmap (Vorschlag, anpassen)

| Prio | Aufgabe | Aufwand | Status |
|---|---|---|---|
| P1 | Gap C — `IfError`-Wrap auf Home-Delete-Block | 1–2h | offen |
| P1 | Gap B — `CascadeDelete = Cascade` Dataverse-Beziehungen | 2–3h | offen |
| P1 | Gap D — Cross-Tenant-Test Zug (Garofano-Path reproduzieren) | 0.5d | offen |
| P2 | Gap A — Fotos in `rrpt_foto` migrieren (DV-File-Field) | 1–2d | offen |
| P2 | Gap E — Profil-Republish-Checkliste + Release-Notes-Template | 0.5d | offen |
| P3 | Gap E (Stretch) — Profil-Update in CI integrieren | mehrtägig | Backlog |

## Persönliche Notizen

_Manuelle Notizen, neue Symptome, Hypothesen, Test-Ergebnisse hier ergänzen._

## Verwandt

- [[Regieapp-Neubau-MVM|Regie-Rapport-App (Haupt-Hub)]]
- [[Regieapp-Schwachstellen-Review|Regieapp Schwachstellen-Review]] (K33–K35)
- [[Regieapp-Aestico-Domus-Import|Regie-App → Aestico-Domus-Import (Sub-Hub)]]
- [[50.work/26_Firmen/MVM-AG|Klient: MVM AG]]
- [[50.work/25_People/Remo-Pfister|Remo Pfister]]
- [[60.daily/2026-06-15|Daily 2026-06-15]] — ToDo 8
