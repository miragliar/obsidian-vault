#!/usr/bin/env python3
"""
build_projects.py
-----------------
Erzeugt Projekt-Hubs in 50.work/projekte/ aus mehreren Quellen:
  • Claude-Export-Conversation-Index (Manifest)
  • Teams-Gruppenchat-Daten (teams_digest.json)
  • Mail-Stats (mail_digest.json)
  • Personen-/Firmen-Notizen (für Wikilinks)
"""
import json
from pathlib import Path

VAULT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul")
PROJEKTE = VAULT / "50.work" / "projekte"
PROJEKTE.mkdir(exist_ok=True)
SCRIPTS = VAULT / "50.work" / "m365-graph" / "scripts"

teams = json.loads((SCRIPTS / "teams_digest.json").read_text())

# Index mit msg-counts + dates für Conv-Anker
manifest = json.loads((VAULT / "_imports" / "manifest.json").read_text())
conv_by_uuid = {c["uuid"]: c for c in manifest}


# =========================================================================
# Projekt-Definitionen
# Schlüssel = Slug, Werte siehe build_hub()
# =========================================================================
PROJECTS = [
    # ---------------------------------------------------------------------
    {
        "slug": "Subunternehmerprozess-Koster",
        "name": "Subunternehmer-Dokumentenverwaltung",
        "klient": "Koster AG",
        "klient_slug": "Koster-AG",
        "status": "produktiv / Wartung",
        "zeitraum": "März 2026 — laufend",
        "kategorie": "kunde",
        "beteiligte": ["H. Baumann", "Monika Kuhn"],
        "tags": ["miraglia", "projekt", "koster-ag", "power-apps", "ai-builder"],
        "kurz": (
            "Power-Apps-Lösung zur automatisierten Verwaltung von "
            "Subunternehmer-Dokumenten (Verträge, Deklarationen, Zeugnisse) "
            "mit KI-gestützter Datenextraktion via AI Builder und "
            "Power-Automate-Flows."
        ),
        "kontext": [
            "Subunternehmer schicken Dokumente, die in einem komplexen Workflow "
            "verarbeitet, klassifiziert und archiviert werden müssen.",
            "Status-Maschine pro Dokument (Eingang → Prüfung → Freigabe / Rückfrage / Ablage).",
            "AI Builder Prompt extrahiert Positionsdaten / Deklarations-Felder "
            "aus PDFs, Power Automate orchestriert die Folge-Schritte.",
            "Wöchentliche Erinnerungs-Flows an säumige Subunternehmer.",
        ],
        "convs": [
            "8e6798fb-1d28-4ff3-aeab-a6100e3b7e36",  # 206 msg
            "74779f30-8453-472d-8a55-2b584a4efe41",  # 8 msg
            "0c6f8de5-764e-4c9c-a51b-9a7a1cfd165b",  # 4 msg
            "7d4fb25c-711c-4383-88b4-975610fbce88",  # 6 msg Deklaration ID
            "b476d092-ca47-4dbe-aa91-1c0bc184537e",  # 18 msg Unterstrich Deklaration
            "6beaaba8-4816-4ba3-a754-23305827b3bb",  # 8 msg Wöchentliche Erinnerung
        ],
        "teams_groups": [],  # keine eigene Gruppe gefunden, nur 1:1
        "verwandte_patterns": [
            ("50.work/power-platform/ai-prompt-json-output", "AI Prompt für strukturierte JSON-Extraktion"),
            ("50.work/power-platform/powerfx-filter-search-combobox", "Filter+Search Combobox"),
            ("50.work/power-platform/power-automate-string-expressions", "String-Expressions"),
            ("50.work/power-platform/powerfx-hidden-datacard-submitform", "Hidden Datacard SubmitForm"),
        ],
        "lessons": [
            "Deklarations-IDs mit Unterstrich brauchen besondere Behandlung — Display vs. Internal Name (siehe Pattern Power-Automate-String).",
            "Wöchentliche Reminder als scheduled Flow, mit Filter auf säumige Dokumente.",
            "JSON-Schema fix halten — bei Datentyp-Drift schlägt Parse-JSON-Action fehl (siehe AI-Prompt-Pattern).",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Regieapp-Neubau-MVM",
        "name": "Regie-Rapport-App (Neubau)",
        "klient": "MVM AG",
        "klient_slug": "MVM-AG",
        "status": "Test- / Rollout-Phase",
        "zeitraum": "April 2026 — Mai 2026",
        "kategorie": "kunde",
        "beteiligte": ["Remo Pfister", "M. Schärli"],
        "tags": ["miraglia", "projekt", "mvm-ag", "power-apps", "dataverse", "offline"],
        "kurz": (
            "Neukonzeption und Aufbau einer Power-Apps-Regie-Rapport-App für "
            "die mobile Erfassung von Arbeits-, Material- und Personenzeilen "
            "auf Baustellen. Dataverse-Datenmodell mit Offline-Profile für "
            "Außendienst, Filter+Search-UI, Form-Submit-Logik."
        ),
        "kontext": [
            "Architektur: Master-Tabelle `Regiekopf` + drei N:1-Detail-Tabellen "
            "(Arbeitsbeschriebzeile, Materialzeile, Personenzeile).",
            "Stammdaten-Lookups: Baustelle, Materialkatalog, Mitarbeitertypen.",
            "Mobile-First: Außendienst erfasst auf der Baustelle, oft ohne Netz "
            "→ Offline-Profil als zentrale Anforderung.",
            "UI mit Combobox-Mehrfachauswahl (Baustelle) + Volltextsuche über "
            "Empfänger, Kalenderwoche, PL-Kommentar.",
        ],
        "convs": [
            "47b30ad6-ab3f-4f61-8ed6-727fcf5c16dc",  # Neukonzeption 9
            "46548c10-c314-4be6-ba48-5743f4f4c181",  # Filter+Search 42
            "ad2297d4-f6dc-4183-8400-1a9c47683f30",  # Offlineprofil 46
            "f58e17d1-af25-4580-9184-1daf2616fa59",  # Testphase 2
            "a6b53a21-3ba7-467b-9215-92a390c3cb6e",  # Installation 2
        ],
        "teams_groups": [],
        "verwandte_patterns": [
            ("50.work/power-platform/powerfx-filter-search-combobox", "Filter + Search + Combobox kombinieren"),
            ("50.work/power-platform/powerfx-hidden-datacard-submitform", "Hidden Datacard SubmitForm"),
            ("50.work/power-platform/dataverse-offlineprofile", "Mobile Offline-Profile"),
            ("50.work/power-platform/dataverse-mysterious-deletes", "Cascade-Delete-Diagnose"),
        ],
        "lessons": [
            "Auto-generiertes Offline-Profil → nutzlos. Eigenes Profil in Solution anlegen, sonst Schema-Drift bei jeder Spaltenänderung.",
            "Lookup-Filter ohne `.Id`-Suffix verwenden: `Baustellelookup in ComboBox1.SelectedItems` ist delegierbar und sauberer.",
            "`Search()` außen, `Filter()` innen — UI-Pattern für Combobox + Volltext.",
            "Hidden Datacards mit `Visible = false` schreiben NICHT in Dataverse → stattdessen `Height: 0, Visible: true`.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Telemarketing-App-Nahrin",
        "name": "Telemarketing-App",
        "klient": "Nahrin AG",
        "klient_slug": "Nahrin-AG",
        "status": "produktiv / Wartung",
        "zeitraum": "März 2026 — laufend",
        "kategorie": "kunde",
        "beteiligte": ["Stefanie Ringwald", "Christoph Kübler"],
        "tags": ["miraglia", "projekt", "nahrin", "power-apps"],
        "kurz": (
            "Power-Apps-Lösung für das Nahrin-Telemarketing-Team: "
            "Kundenliste mit Anruf-Logik, Notizen, Nachverfolgung."
        ),
        "kontext": [
            "Hauptkanal: Teams-Gruppe \u201ETelemarketing App - Nahrin\u201C mit 71 Nachrichten.",
            "Stakeholder: Christoph Kübler (Nahrin), Stefanie Ringwald (Nahrin), Giovanni (Miraglia).",
            "Inaktive Kunden tauchten ungewollt in der App auf → Filter-Logik-Bug.",
        ],
        "convs": [
            "0b5ececa-6acc-4005-a347-e1bfffda5fa9",  # Inaktive Kunden 4
        ],
        "teams_groups": ["Telemarketing App - Nahrin"],
        "verwandte_patterns": [
            ("50.work/power-platform/powerfx-filter-search-combobox", "Filter / inaktive-Filter-Logik"),
        ],
        "lessons": [
            "Inaktive Kunden müssen aktiv ausgefiltert werden — `inactive = false` als Default-Filter im Galerie-Items-Property.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Support-Powerplattform-Nahrin",
        "name": "Support Powerplattform",
        "klient": "Nahrin AG",
        "klient_slug": "Nahrin-AG",
        "status": "laufend",
        "zeitraum": "—",
        "kategorie": "kunde",
        "beteiligte": ["Stefanie Ringwald", "Christoph Kübler", "Alessandro Castelli"],
        "tags": ["miraglia", "projekt", "nahrin", "support", "cross-functional"],
        "kurz": (
            "Cross-funktionaler Support-Kanal für die Nahrin-Power-Platform-Landschaft, "
            "mit mehreren externen Partnern."
        ),
        "kontext": [
            "Teams-Gruppe \u201ESupport Nahrin Powerplattform\u201C mit 37 Nachrichten, 8 Personen.",
            "Beteiligte (extern, nicht im 25_People-Folder): Tobias Herzog, Flavio Waser, Oliver Buck, Tobias Lackner.",
            "Funktion: Übergreifender Support — vermutlich Ticket-Triage, Issue-Tracking, kleine Anpassungen.",
        ],
        "convs": [],
        "teams_groups": ["Support Nahrin Powerplattform"],
        "verwandte_patterns": [
            ("50.work/power-platform/_README", "Allgemeine Power-Platform-Pattern-Bibliothek"),
        ],
        "lessons": [
            "Cross-functional Support-Chats → Ticket-/Issue-Log in Vault spiegeln wäre nützlich, derzeit nur Chat-History.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Averecura-Hauswaeckerling",
        "name": "Averecura (Pflegezentrum-Lösung)",
        "klient": "Hauswäckerling",
        "klient_slug": "Hauswaeckerling",
        "status": "laufend",
        "zeitraum": "—",
        "kategorie": "kunde",
        "beteiligte": ["Andreas Funke", "Alessandro Castelli"],
        "tags": ["miraglia", "projekt", "hauswaeckerling", "pflege", "averecura"],
        "kurz": (
            "Lösung für das Betreuungs- und Pflegezentrum Hauswäckerling im "
            "Rahmen der \u201EAverecura\u201C-Initiative. Vermutlich Power-Platform-basiert "
            "für interne Verwaltungs-/Pflege-Prozesse."
        ),
        "kontext": [
            "Teams-Gruppe \u201EAverecura\u201C mit 23 Nachrichten.",
            "Stakeholder: Giovanni Miraglia, Alessandro Castelli (Partner Castelli Solutions), "
            "Andreas Funke (Hauswäckerling).",
            "Hauswäckerling = Betreuungs- und Pflegezentrum (Webseite-Profil).",
        ],
        "convs": [],
        "teams_groups": ["Averecura"],
        "verwandte_patterns": [],
        "lessons": [
            "Inhalt der Lösung noch nicht im Vault dokumentiert — Folge-Aufgabe: Andreas Funke nach Stand fragen, Architektur-Notiz anlegen.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Zeugnis-App-Obrist",
        "name": "Zeugnis-Test-App",
        "klient": "Obrist Interior",
        "klient_slug": "Obrist-Interior",
        "status": "produktiv / Test",
        "zeitraum": "Sept – Okt 2025",
        "kategorie": "kunde",
        "beteiligte": ["Barbara Gilli", "Tobias Lamprecht", "Bianca Tschuppert"],
        "tags": ["miraglia", "projekt", "obrist-interior", "power-apps", "zeugnis"],
        "kurz": (
            "Power-Apps-Lösung bei Obrist Interior für die Verwaltung von "
            "(Mitarbeiter-?)Zeugnissen. Test-Phase mit drei Stakeholderinnen — "
            "Barbara Gilli, Tobias Lamprecht und Bianca Tschuppert."
        ),
        "kontext": [
            "Chat-Samples zeigen: Diskussion um Zeugnis-Links, Sichtbarkeit der Zeugnisse, "
            "Test-Zeugnisse für \u201EAndreas Walser\u201C.",
            "Mögliche Verbindung zu Conv \u201EWöchentliche Erinnerung zu ausstehenden Zeugnissen\u201C "
            "(2026-03-12, 8msg) — andere Klientenbeziehung, evtl. parallele Logik.",
            "Tobias Lamprecht: \u201EWenn ich auf den Link von Barbara klicke, sehe ich kein Zeugnis mehr.\u201C",
            "Bianca Tschuppert: \u201EHallo Raoul, auch ich habe das Test Zeugnis für Andreas Walser erhalten.\u201C",
        ],
        "convs": [],
        "teams_groups": [],
        "verwandte_patterns": [
            ("50.work/power-platform/powerfx-filter-search-combobox", "Filter-Logik für Zeugnis-Liste"),
            ("50.work/power-platform/dataverse-mysterious-deletes", "Sichtbarkeits-/Berechtigungs-Probleme"),
        ],
        "lessons": [
            "Sichtbarkeits-Bug (\u201Esehe kein Zeugnis\u201C) deutet auf Security-Role / Owner-Filter hin — Standard-Diagnose-Pfad: Dataverse-Berechtigung + Filter-Predicates prüfen.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "Einfassbaender-Hunnenberg",
        "name": "Einfassbänder / AI-Prompt-Auftragserstellung",
        "klient": "Hunnenberg",
        "klient_slug": "Hunnenberg",
        "status": "produktiv",
        "zeitraum": "April 2026",
        "kategorie": "kunde",
        "beteiligte": ["TH Hunnenberg"],
        "tags": ["miraglia", "projekt", "hunnenberg", "power-automate", "ai-builder"],
        "kurz": (
            "Power-Automate-Flow + AI-Builder-Prompt für die automatische "
            "Auftragserstellung im Teppich- und Bodenbelag-Großhandel: aus "
            "PDF-Dokumenten + Mail werden Positionen + Lieferinfo extrahiert "
            "und in eine Strukturierte Auftragsdaten-JSON überführt."
        ),
        "kontext": [
            "Klient: Hunnenberg, Düsseldorf — Großhandel für Bodenbeläge und Teppich-Kettelei.",
            "Workflow: Mehrseitiges Dokument + Mail mit Lieferinfo → AI Builder Prompt → "
            "JSON mit Positionen (Artikel-Nr., Beschreibung, Menge, Form, Länge, Breite, "
            "Einfassung, Farbe, Breite, Rückenbeschichtung) + Lieferdatum / Spedition.",
            "Komplexer Fall: Positionen können über zwei Seiten verteilt sein "
            "(Marker \u201EWarenausgangsnr.\u201C als Fortsetzungs-Header).",
            "Domain-Wissen: Einfassbreite = 1cm → Farbe = Konkatenation aus Einfassfarbe-PDF + letzten 2 Ziffern; sonst Nummer ohne Präfix.",
            "Float-Cast benötigt Komma → Punkt Replace (siehe Pattern Power-Automate-String).",
        ],
        "convs": [
            "7c1d0fc3-26a3-414c-b8b2-96f142294501",  # Einfassbänder 14
            "2a3604c1-b39e-4936-b083-33cbf2e5bd33",  # Prompt JSON 42
            "f4c08cc2-6c5a-455f-aec8-ccb495ce7f02",  # Wertsubstitution 2
        ],
        "teams_groups": [],
        "verwandte_patterns": [
            ("50.work/power-platform/ai-prompt-json-output", "AI Builder Prompts — strukturierte JSON-Ausgabe"),
            ("50.work/power-platform/power-automate-string-expressions", "String-Expressions & Locale-Fallen (Komma vs. Punkt)"),
            ("50.work/power-platform/powerfx-filter-search-combobox", "PowerFx Filter"),
        ],
        "lessons": [
            "AI-Prompts: \u201EVorgehensweise intern, nicht ausgeben\u201C → step-by-step-Rechnen reduziert Klammer-Fehler im JSON-Output.",
            "Bei seitenübergreifenden Positionen den Fortsetzungs-Marker explizit im Prompt benennen, sonst entstehen halbe Duplikat-Einträge.",
            "Locale: deutsche Komma-Notation muss vor `float()` zu Punkt-Notation gemapped werden.",
            "Bedingungslogik (z.B. \u201EWenn Einfassbreite = 1cm dann …\u201C) gehört in Power Automate `Condition` + `concat`, NICHT in den LLM-Prompt.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "PowerTeam-intern",
        "name": "PowerTeam (Partner-Kollaboration)",
        "klient": "intern + Partner",
        "klient_slug": None,
        "status": "laufend",
        "zeitraum": "—",
        "kategorie": "intern",
        "beteiligte": ["Giovanni Miraglia", "Michael Kipfer", "Alessandro Castelli"],
        "tags": ["miraglia", "intern", "powerteam", "partner"],
        "kurz": (
            "Kernchannel für die Zusammenarbeit zwischen Miraglia BI, "
            "Kipfer DP und Castelli Solutions. Hauptachse der Power-Platform-Praxis."
        ),
        "kontext": [
            "Teams-Gruppe \u201EPowerTeam\u201C mit 100 Nachrichten.",
            "Drei Teilnehmer: Giovanni Miraglia, Michael Kipfer, Alessandro Castelli.",
            "Funktion: tagesübergreifender Austausch zu Power-Platform-Themen, Kunden-Setups, Lösungs-Ideen.",
        ],
        "convs": [],
        "teams_groups": ["PowerTeam"],
        "verwandte_patterns": [
            ("50.work/power-platform/_README", "Power-Platform-Pattern-Bibliothek (Output dieser Kollaboration)"),
        ],
        "lessons": [
            "Wichtigste Quelle für ad-hoc Best Practices und Eskalationen — periodisches Sichten lohnt sich.",
        ],
    },
    # ---------------------------------------------------------------------
    {
        "slug": "RPA-Monitoring-intern",
        "name": "RPA-Monitoring",
        "klient": "intern",
        "klient_slug": None,
        "status": "produktiv",
        "zeitraum": "—",
        "kategorie": "intern",
        "beteiligte": ["Giovanni Miraglia", "Michael Kipfer"],
        "tags": ["miraglia", "intern", "rpa", "monitoring"],
        "kurz": (
            "Internes Monitoring für die RPA-Infrastruktur (Power Automate Desktop, "
            "Service-Accounts wie `rpa@miraglia-bi.com`)."
        ),
        "kontext": [
            "Teams-Gruppe \u201ERPA-Monitoring\u201C mit 100 Nachrichten.",
            "Zwei Teilnehmer: Giovanni Miraglia, Michael Kipfer.",
            "Service-Account `rpa@miraglia-bi.com` taucht in 95 Mails auf — vermutlich Run-Notifications.",
            "Im Power-Platform-Cluster: Conv \u201EAuto-repair feature in Power Automate Desktop einrichten\u201C (2026-05-13) — gehört vermutlich hierhin.",
        ],
        "convs": [],
        "teams_groups": ["RPA-Monitoring"],
        "verwandte_patterns": [
            ("50.work/power-platform/power-automate-invalidopenapiflow", "Flow-Fehler-Diagnose"),
        ],
        "lessons": [
            "Auto-Repair-Feature in PAD nutzen, um instabile UI-Robotics-Schritte resilienter zu machen.",
        ],
    },
]


# =========================================================================
# Hub-Bauer
# =========================================================================
def slug_person(name):
    return name.replace(" ", "-")


def build_hub(p):
    fpath = PROJEKTE / f"{p['slug']}.md"

    # Frontmatter
    fm = ["---",
          f"name: {p['name']}",
          f"slug: {p['slug']}",
          f"klient: {p['klient']}"]
    if p["klient_slug"]:
        fm.append(f"klient_link: \"[[50.work/26_Firmen/{p['klient_slug']}|{p['klient']}]]\"")
    fm += [
        f"status: {p['status']}",
        f"zeitraum: {p['zeitraum']}",
        f"kategorie: {p['kategorie']}",
        f"tags: [{', '.join(p['tags'])}]",
        "type: projekt-hub",
        "source: claude-import + m365-graph",
        "created: 2026-06-01",
        "---",
        "",
        f"# {p['name']}",
        "",
    ]
    if p["klient_slug"]:
        fm.append(f"**Klient:** [[50.work/26_Firmen/{p['klient_slug']}|{p['klient']}]]  ")
    else:
        fm.append(f"**Kategorie:** {p['kategorie']}  ")
    fm += [
        f"**Status:** {p['status']}  ",
        f"**Zeitraum:** {p['zeitraum']}",
        "",
        "## Worum geht es",
        "",
        p["kurz"],
        "",
        "## Beteiligte",
        "",
    ]
    for pname in p["beteiligte"]:
        fm.append(f"- [[50.work/25_People/{slug_person(pname)}|{pname}]]")
    fm.append("")

    if p["kontext"]:
        fm += ["## Kontext / Architektur", ""]
        for c in p["kontext"]:
            fm.append(f"- {c}")
        fm.append("")

    # Conversations (claude-import)
    if p["convs"]:
        fm += ["## Quell-Conversations (Claude-Export)", "",
               "Aus dem Original-Claude-Export (UUID-basiert rückverfolgbar). "
               "Die destillierten Pattern-Notizen sind unter \u201EVerwandte Patterns\u201C.",
               "",
               "| msgs | Datum | Titel | UUID |",
               "|---:|---|---|---|"]
        rows = []
        for uuid in p["convs"]:
            c = conv_by_uuid.get(uuid)
            if c:
                rows.append((c["msgs"], c["updated_at"][:10], c["name"], uuid))
        rows.sort(key=lambda r: r[0], reverse=True)
        for msgs, date, name, uuid in rows:
            fm.append(f"| {msgs} | {date} | {name} | `{uuid[:8]}…` |")
        fm.append("")

    # Teams-Gruppen
    if p["teams_groups"]:
        fm += ["## Teams-Gruppen-Chats", ""]
        for topic in p["teams_groups"]:
            # Finde Gruppe
            for gc in teams.get("group_chats", []):
                if (gc.get("topic") or "") == topic:
                    members = [m for m in (gc.get("members") or []) if m]
                    fm.append(
                        f"- **{topic}** — {gc.get('msg_count', 0)} Nachrichten "
                        f"(letzter {gc.get('last', '—')})"
                    )
                    if members:
                        fm.append(f"  - Mitglieder: {', '.join(members)}")
                    break
            else:
                fm.append(f"- **{topic}** _(nicht in teams_digest.json gefunden)_")
        fm.append("")

    if p["verwandte_patterns"]:
        fm += ["## Verwandte Pattern-Notizen", ""]
        for link, label in p["verwandte_patterns"]:
            fm.append(f"- [[{link}|{label}]]")
        fm.append("")

    if p["lessons"]:
        fm += ["## Erkenntnisse / Lessons Learned", ""]
        for l in p["lessons"]:
            fm.append(f"- {l}")
        fm.append("")

    fm += ["## Persönliche Notizen",
           "",
           "_Manuelle Notizen, Aufgaben, Ideen, Risiken kommen hier hin._",
           "",
           "## Verwandt",
           "",
           "- [[50.work/projekte/_Index|Projekt-Index]]",
           ]
    if p["klient_slug"]:
        fm.append(f"- [[50.work/26_Firmen/{p['klient_slug']}|Klient: {p['klient']}]]")

    fpath.write_text("\n".join(fm), encoding="utf-8")
    return fpath


def build_index():
    idx = PROJEKTE / "_Index.md"
    lines = [
        "---", "source: claude-import + m365-graph", "imported: 2026-06-01",
        "type: projekte-index", "tags: [projekte, index, miraglia]", "---", "",
        "# Projekt-Index", "",
        f"{len(PROJECTS)} Projekte und Programme aus den Quellen "
        "Claude-Conversations + Teams-Gruppenchats + Mail-Aggregation.",
        "",
    ]
    by_cat = {}
    for p in PROJECTS:
        by_cat.setdefault(p["kategorie"], []).append(p)
    for cat, label in [("kunde", "Kunden-Projekte"),
                       ("intern", "Intern / Partner-Kollaboration")]:
        if cat not in by_cat:
            continue
        lines += [f"## {label}", "",
                  "| Projekt | Klient | Beteiligte | Status |",
                  "|---|---|---|---|"]
        for p in by_cat[cat]:
            klient = (f"[[50.work/26_Firmen/{p['klient_slug']}|{p['klient']}]]"
                      if p["klient_slug"] else p["klient"])
            beteiligte = ", ".join(p["beteiligte"][:3])
            if len(p["beteiligte"]) > 3:
                beteiligte += "…"
            lines.append(
                f"| [[{p['slug']}|{p['name']}]] | {klient} | {beteiligte} | {p['status']} |"
            )
        lines.append("")

    lines += ["---", "",
              "_Generiert via `_imports/build_projects.py` aus Manifest + Teams-Digest._"]
    idx.write_text("\n".join(lines), encoding="utf-8")
    return idx


def main():
    print(f"Build Projekt-Hubs → {PROJEKTE}")
    print("-" * 60)
    for p in PROJECTS:
        path = build_hub(p)
        print(f"  ✓ {path.name:42s}  [{p['kategorie']}] {p['klient']}")
    idx = build_index()
    print(f"\n  ✓ Index: {idx.name}")


if __name__ == "__main__":
    main()
