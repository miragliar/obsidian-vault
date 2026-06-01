---
source: claude-import
imported: 2026-06-01
type: template
tags: [miraglia, vorlage, personen]
---

# Personen-Notiz — Vorlage für `25_People/`

Standardstruktur für Notizen in `25_People/<Name>.md`. Wird von `mail_digest.py` über die `email:`-Zeile im Frontmatter erkannt. Die KI-generierte Zusammenfassung wird zwischen den `<!-- mail-summary -->`-Markern eingefügt — alles außerhalb der Marker bleibt beim Refresh unangetastet.

## Vorlage (kopieren & ausfüllen)

```markdown
---
name: <Vorname Nachname>
email: <vorname.nachname@firma.ch>
firma: <Firmenname>
rolle: <z.B. CIO, Projektleiterin Sales>
typ: kunde | kollege | partner | sonstiges
projekte: [<Projekt1>, <Projekt2>]
tags: [miraglia, <typ>, <firma-tag>]
status: aktiv | inaktiv | abgeschlossen
created: <YYYY-MM-DD>
---

# <Vorname Nachname>

**<Firma> — <Rolle>**

## Kontext

<Wie kam der Kontakt zustande? Welches Projekt? Was sind die Erwartungen?>

## Aktuelles Projekt / Status

<Worüber tauschen wir uns gerade aus? Was läuft, was steht offen?>

## Persönliche Notizen

<Manuelle Beobachtungen: Kommunikationsstil, Vorlieben, gemeinsame Themen, geplante Treffen, etc.>

## Mail- & Chat-Verlauf (automatisch generiert)

<!-- mail-summary -->
*Hier fügt Claudian die Zusammenfassung aus mail_digest.json + teams_digest.json ein. Bei jedem Refresh wird dieser Block neu generiert.*
<!-- /mail-summary -->

## Verwandt

- [[<verwandtes Projekt / Hub>]]
```

## Beispiel: ausgefüllte Notiz

```markdown
---
name: Heike Beispiel
email: heike@kunde-ag.ch
firma: Kunde AG
rolle: Projektleiterin Sales
typ: kunde
projekte: [Subunternehmer-Doks, Telemarketing-App]
tags: [miraglia, kunde, kunde-ag]
status: aktiv
created: 2026-03-12
---

# Heike Beispiel

**Kunde AG — Projektleiterin Sales**

## Kontext

Hauptkontakt Kunde AG, koordiniert Power-Apps-Anpassungen und Test-Feedback. Sehr strukturiert, mag knappe Status-Updates mit Action-Item-Listen.

## Aktuelles Projekt / Status

Subunternehmer-Doks-App in Test-Phase. Letzte offene Punkte:
- Status-Machine für Dokumenten-Lifecycle (siehe [[../power-platform/dataverse-mysterious-deletes]])
- Mobile Offline-Profil noch nicht in Solution

## Persönliche Notizen

- Bevorzugt Teams-Calls Mi 14:00
- Bei Mail: Antwort erwartet binnen 24h
- Geht nicht direkt zu Giovanni — alles über Raoul

## Mail- & Chat-Verlauf (automatisch generiert)

<!-- mail-summary -->
**Stand: 2026-06-01**

- **Interaktionen letzte 30 Tage:** 14 Mails (8↓ / 6↑), 22 Teams-Nachrichten (1:1)
- **Top-Themen:**
  1. Offlineprofil-Sync-Fehler nach Schema-Update
  2. Code-Review Anwesenheits-Formel
  3. Test-Phase-Feedback Round 3
- **Offene Punkte:** Antwort zu Excel-Pfad-Korrektur erwartet
- **Letzter Kontakt:** 2026-05-30 (Teams)
<!-- /mail-summary -->

## Verwandt

- [[../power-platform/dataverse-offlineprofile]]
- [[../power-platform/powerfx-filter-search-combobox]]
```

## Konventionen

| Feld | Regel |
|---|---|
| `email:` | Pflicht (sonst keine Verknüpfung); lowercase |
| `firma:` | optional, aber sehr nützlich für Gruppierung |
| `typ:` | strukturiert die Personen-Hubs |
| `tags:` | mindestens `miraglia`, dann `<typ>`, dann Firma |
| Dateiname | `<Vorname-Nachname>.md` (Bindestrich statt Leerzeichen) |
| Marker | `<!-- mail-summary -->` und `<!-- /mail-summary -->` exakt so schreiben |

## Erweiterung: Personen-Hub-Index

Wenn `25_People/` größer wird, lohnt sich ein `25_People/_Index.md`:

```markdown
---
type: people-index
---

# Personen-Index

## Kunden
- [[Heike-Beispiel]] (Kunde AG)
- ...

## Kollegen
- [[Giovanni-Miraglia]] (Miraglia BI)
- ...

## Partner
- ...
```

## Verwandt

- [[setup-und-workflow]] — Anreicherungs-Workflow
- [[01-chef-mail-juni-2026]] — Original-Auftrag
- [[40.meta/claude-projekte-und-custom-ai]] — wie KI die Zusammenfassung erstellt
