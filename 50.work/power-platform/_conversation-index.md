---
source: claude-import
imported: 2026-06-01
type: conversation-index
tags: [index, power-platform, miraglia]
---

# Power-Platform — Conversation-Index

Alle 63 Conversations aus dem Claude-Export, die als Power-Platform-Cluster identifiziert wurden, sortiert nach Umfang.

**Lege-Regel:** Wenn dir eine konkrete Fragestellung wieder begegnet, suche zuerst in den Pattern-Notizen im [[_README]]. Dieser Index ist die Rückfall-Quelle, wenn ein Detail aus einer bestimmten Conversation gebraucht wird.

Die wichtigsten Conversations sind als destillierte Patterns ausgekoppelt. Die übrigen sind hier mit Kurzbeschreibung katalogisiert.

| msgs | Datum | Titel | Pattern / Notiz |
|---:|---|---|---|
| 206 | 2026-04-08 | Subunternehmer-Dokumentenverwaltung mit KI und Power Apps | Großprojekt: Subunternehmer-Dokumentenverwaltung mit KI + Power Apps (206msg) — referenziert von vielen Patterns |
| 74 | 2026-04-24 | Code-Formel für Anwesenheit anpassen | Excel-LET-Formel für Anwesenheit/Verspätungen (Excel, nicht PowerFx) |
| 46 | 2026-05-20 | Offlineprofil Fehler beim Speichern und Öffnen | -> [[dataverse-offlineprofile]] |
| 42 | 2026-04-09 | Filter mit Combobox und Textsuche erweitern | -> [[powerfx-filter-search-combobox]], [[powerfx-hidden-datacard-submitform]] |
| 42 | 2026-04-23 | Prompt zur Formelberechnung mit JSON-Ausgabe | -> [[ai-prompt-json-output]], [[power-automate-string-expressions]] |
| 38 | 2026-05-28 | Unerklärte Datenverluste in Dataverse-Bestelltabelle | -> [[dataverse-mysterious-deletes]] |
| 36 | 2026-04-15 | Power automate InvalidOpenApiFlow error | -> [[power-automate-invalidopenapiflow]] |
| 26 | 2026-04-29 | Prozessoptimierung und Feedback zur App-Testphase | Strategisches Feedback-Loop für App-Tests |
| 21 | 2026-05-07 | Contributor-Rechte für Billing plan konfigurieren | -> [[azure-service-principal-billing-rollen]] |
| 18 | 2026-04-03 | Unterschiede zwischen screenshot auflistungen | Screenshot-Vergleich für Bug-Reproduktion |
| 18 | 2026-03-25 | PowerFx Code Fehleranalyse | PowerFx Syntax-Error-Triage |
| 18 | 2026-04-29 | Unterstrich in Deklarations_ID verschwindet | Power Automate Display vs. Internal Name (Underscore-Erhaltung) |
| 18 | 2026-04-23 | SharePoint file path not found error | SP-Datei-Pfad: Slash- und Encoding-Issues |
| 18 | 2026-05-28 | Table-Wert von Power Apps zu Power Automate übergeben | Komplexe Tabellen-Struktur via JSON-Parse zwischen App + Flow |
| 16 | 2026-05-28 | API response headers analysis | HTTP-Headers in Power Automate parsen (Listing-Performance API) |
| 14 | 2026-03-25 | Filter expression syntax error | Filter-Syntax: häufige Tippfehler & Lookup-Probleme |
| 14 | 2026-04-30 | Filter für Einfassbänder und Teppichkanten | PowerFx-Filter mit komplexen Choice-Mehrfachauswahlen |
| 12 | 2026-03-26 | Chat GPT Entwicklungsstrategie bewerten | Meta: AI-Tooling-Strategie für Entwicklung |
| 10 | 2026-04-07 | Exclude "Divers" from dropdown choices | Filter-Pattern: Distinct - {Wert} im Dropdown |
| 10 | 2026-04-02 | Custom prompt funktioniert nicht mehr | AI-Builder-Custom-Prompt: Schema-Drift nach Update |
| 10 | 2026-03-19 | Bildbezeichnungen extrahieren | Bild-Filename-Extraction für Dokumentation |
| 10 | 2026-05-07 | Leere Werte im Lookup-Feld der Power App | Lookup-Feld zeigt leer wegen Sync/Schema-Issue |
| 9 | 2026-04-08 | Neukonzeption einer Regie-Rapport-App für Power Platform | Architektur-Refactor der Rapport-App |
| 8 | 2026-04-10 | Power Automate Bild zu Base64 konvertieren | Image -> Base64 für AI-Builder-Input |
| 8 | 2026-03-19 | Subunternehmerprozess automatisiert und vereinfacht | End-to-End-Email an CFO über Subunternehmer-Automatisierung |
| 8 | 2026-03-12 | Wöchentliche Erinnerung zu ausstehenden Zeugnissen | Scheduled Flow für Reminder-Emails |
| 8 | 2026-05-13 | Tabelle Environment Variable Value offline schalten | Environment-Variable global deaktivieren statt löschen |
| 8 | 2026-05-08 | Word Claude Add-in für Mac installieren | Word-Add-in (Mac) Installation und Aktivierung |
| 8 | 2026-04-22 | Power Automate Umschlagtaste codieren | URL-Encode für Umschlag-/Sonderzeichen in Pfaden |
| 6 | 2026-03-26 | Deklaration ID Leerfeld-Prüfung funktioniert nicht | IsBlank/Coalesce für ID-Felder in PowerFx |
| 6 | 2026-03-18 | Pfad aus Ordnervariable extrahieren | -> [[power-automate-string-expressions]] (Pfad-Extraktion) |
| 6 | 2026-05-07 | Listing performance API request configuration | Performance-API-Tuning via HTTP-Request-Config |
| 6 | 2026-05-06 | SharePoint folder not found error | SP-Folder-Path-Encoding (Sonderzeichen, Leerzeichen) |
| 4 | 2026-04-02 | Subunternehmerprozess und Dokumentenstatus | Status-Machine für Dokumenten-Lifecycle |
| 4 | 2026-04-02 | PDF-Dokument aufteilen Syntax | PDF-Split via PAD/Connector |
| 4 | 2026-03-19 | Power Apps formulas guide | PowerFx-Formel-Übersicht für Einsteiger |
| 4 | 2026-03-19 | Getting current environment in Power Automate | Environment-Detection via Workflow-Properties |
| 4 | 2026-03-12 | Gallery nach Kompetenzkategorien sortieren | Sort + Group in Gallery via PowerFx |
| 4 | 2026-03-12 | Inaktive Kunden erscheinen in Telemarketing-App | Filter-Bug: 'inactive=true' korrekt anwenden |
| 4 | 2026-05-07 | Array-Variable korrekt anhängen | append to array variable - typische Gotchas |
| 4 | 2026-05-06 | DAX-Abfrage für Leistungsvorerfassung | DAX measure für Pre-Capture Leistungs-Daten |
| 4 | 2026-04-23 | Dateipfad-Fehler behoben | SharePoint-Pfad mit Unicode-Sonderzeichen |
| 4 | 2026-05-27 | GitHub Copilot free display and M365 license linking | M365-Lizenzkopplung mit GitHub Copilot Free-Display-Anzeige |
| 2 | 2026-04-16 | Regieapp-Testphase und Zugriffsverwaltung | Rollen-/Rechte-Setup während Pilot-Phase |
| 2 | 2026-04-10 | Feld-Extraktion aus Zeitachse in Power Automate | Timeline-Entity-Feld via Dataverse-Connector |
| 2 | 2026-04-10 | Power Apps Lizenzierung auf App- oder Umgebungsebene | Per-App vs. Per-Environment Premium-Lizenzen |
| 2 | 2026-04-07 | Anhänge mit Buchstaben statt Nummern beschriften | Letter-Index statt Nummer für Attachments |
| 2 | 2026-04-07 | Dokumente Typ Divers: OK oder unvollständig | Choice-Wert 'Divers' validieren vs. Required-Fields |
| 2 | 2026-04-02 | Email an Developer-Tenant-Partner verbessern | Mail-Tonalität an MS-Tenant-Support |
| 2 | 2026-04-02 | Power Automate fields reappearing after removal | Geisterfelder im Flow-JSON nach Variable-Lösch |
| 2 | 2026-03-19 | Flow 2 Datei-Erstellungsproblem | Create-File-Action: Pfad-Konflikte beheben |
| 2 | 2026-03-18 | E-Mail zu Ordnerpfaden in Flow-Automatisierung vereinfachen | Mail-Body-Pfad-Refactoring |
| 2 | 2026-03-12 | Power Automate Run Logs in Dataverse | Custom-Audit-Logging in Dataverse-Tabelle |
| 2 | 2026-03-12 | Datum-Validierung für Archivierungslogik | Date-Compare für Archive-Filter |
| 2 | 2026-05-13 | Auto-repair feature in Power Automate Desktop einrichten | PAD-Robotik: Auto-repair für UI-Elemente |
| 2 | 2026-05-11 | Flow-Version aktualisiert | Versionierung & Republish nach Schema-Änderung |
| 2 | 2026-05-07 | Excel-Dateipfad in Power Automate korrigieren | Pfad-Bug bei Excel-Connector lösen |
| 2 | 2026-05-07 | FTP-Export Header-Problem lösen | FTP-Export: Header-Mapping in Power Automate |
| 2 | 2026-05-03 | Neue Regie-App und Power Apps Installation | Initial-Setup einer neuen Regie-Rapport-App |
| 2 | 2026-04-29 | Tage zwischen Juli und September berechnen | Datums-Arithmetik in PowerFx (DateDiff / DateAdd) |
| 2 | 2026-04-29 | Power App Gallery Breite Problem | Gallery-Width-Bug in Custom Components |
| 2 | 2026-04-23 | Logik für E-Mail-Filter anpassen | Outlook-Filter via Body-Inhalt in Flow |
| 2 | 2026-04-22 | Formelberechnung mit Wertsubstitution | Variable-Substitution in Berechnungs-Prompt |

---

## Rückverfolgung

- Jede Pattern-Notiz führt die `conv_uuids` der Quell-Konversationen im Frontmatter.
- Rohe Konversations-Daten liegen **nicht** im Vault (Entscheidung „nur destillierte Patterns").
- Quelle: Claude Export, `~/Downloads/data-748e…/conversations.json`.
- Eine einzelne Conv lässt sich per UUID extrahieren:
  ```bash
  jq -r '.[] | select(.uuid=="<UUID>") | .chat_messages[] | "[\(.sender)] \(.text)"' conversations.json
  ```