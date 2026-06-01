#!/usr/bin/env python3
"""
build_firmen_notes.py
---------------------
Erstellt für jede der 9 bekannten Firmen eine Notiz in 26_Firmen/.

Datenquellen:
  - company_profiles.json (Webseite/Zefix-Steckbrief)
  - teams_digest.json     (Gruppen-Chats pro Firma)
  - mail_digest.json      (Mail-Counts pro Person → Aggregate pro Firma)
  - 25_People/<Name>.md   (für die Verknüpfung Personen ↔ Firma)

Idempotent: existierende Firmen-Notizen werden überschrieben (sind reine
Generator-Output-Files, keine manuellen Inhalte erwartet).
"""
import json
import re
from pathlib import Path
from collections import defaultdict

VAULT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul")
SCRIPTS = VAULT / "50.work" / "m365-graph" / "scripts"
PEOPLE = VAULT / "50.work" / "25_People"
FIRMEN = VAULT / "50.work" / "26_Firmen"
FIRMEN.mkdir(exist_ok=True)

profiles = json.loads((SCRIPTS / "company_profiles.json").read_text())
teams = json.loads((SCRIPTS / "teams_digest.json").read_text())
mail = json.loads((SCRIPTS / "mail_digest.json").read_text())

# Mail-Count pro Email
mail_count = {item["email"].lower(): item["total"] for item in mail.get("frequent_without_note", [])}
for p in mail.get("people", []):
    mail_count[p["email"].lower()] = p.get("total", 0)

# Teams nach Email (merge wegen Guest+intern)
teams_by_email = defaultdict(lambda: {"interactions": 0, "msgs_from": 0,
                                       "my_replies_1to1": 0, "in_1to1": 0,
                                       "in_group": 0, "last": "", "name": ""})
for p in teams.get("people", []):
    e = (p.get("email") or "").lower()
    if not e:
        continue
    t = teams_by_email[e]
    t["interactions"] += p.get("interactions", 0)
    t["msgs_from"] += p.get("msgs_from", 0)
    t["my_replies_1to1"] += p.get("my_replies_1to1", 0)
    t["in_1to1"] += p.get("in_1to1", 0)
    t["in_group"] += p.get("in_group", 0)
    if p.get("last", "") > t["last"]:
        t["last"] = p["last"]
    if not t["name"]:
        t["name"] = p.get("name", "")

# Firmen-Konfiguration: Slug + Personen + Branche + Typ
FIRMS = {
    "Miraglia Business-Intelligence": {
        "slug": "Miraglia-Business-Intelligence",
        "domain": "miraglia-bi.com",
        "people": [("Giovanni Miraglia", "giovanni@miraglia-bi.com", "Chef / Gründer")],
        "typ": "intern",
        "branche": "Business Intelligence / Power Platform Consulting",
        "tags": ["miraglia", "intern", "miraglia-bi"],
    },
    "Kipfer DP": {
        "slug": "Kipfer-DP",
        "domain": "kipfer-dp.com",
        "people": [("Michael Kipfer", "michael@kipfer-dp.com", "Power Platform Partner")],
        "typ": "partner",
        "branche": "Power Platform / Digital Power",
        "tags": ["miraglia", "partner", "kipfer-dp"],
    },
    "Castelli Solutions": {
        "slug": "Castelli-Solutions",
        "domain": "castelli-solutions.ch",
        "people": [("Alessandro Castelli", "alessandro@castelli-solutions.ch", "Power Platform Partner")],
        "typ": "partner",
        "branche": "Power BI / Power Apps / Power Automate",
        "tags": ["miraglia", "partner", "castelli-solutions"],
    },
    "MVM AG": {
        "slug": "MVM-AG",
        "domain": "mvm-ag.ch",
        "people": [
            ("Remo Pfister", "r.pfister@mvm-ag.ch", "Power Platform Ansprechperson"),
            ("M. Schärli", "m.schaerli@mvm-ag.ch", "Mail-Kontakt"),
        ],
        "typ": "kunde",
        "branche": "Maler- und Gipserarbeiten / Bau",
        "tags": ["miraglia", "kunde", "mvm-ag"],
    },
    "Nahrin AG": {
        "slug": "Nahrin-AG",
        "domain": "nahrin.ch",
        "people": [
            ("Stefanie Ringwald", "stefanie.ringwald@nahrin.ch", "Power Platform Ansprechperson"),
            ("Christoph Kübler", "christoph.kuebler@nahrin.ch", "Projekt-Kontakt"),
        ],
        "typ": "kunde",
        "branche": "Lebensmittel / Bouillon / Nahrungsergänzung",
        "tags": ["miraglia", "kunde", "nahrin"],
    },
    "Obrist Interior": {
        "slug": "Obrist-Interior",
        "domain": "obrist-interior.ch",
        "people": [
            ("Barbara Gilli", "b.gilli@obrist-interior.ch", "Projekt-Kontakt"),
            ("Tobias Lamprecht", "t.lamprecht@obrist-interior.ch", "Projekt-Kontakt (Zeugnis-App)"),
            ("Bianca Tschuppert", "b.tschuppert@obrist-interior.ch", "Projekt-Kontakt (Zeugnis-App)"),
        ],
        "typ": "kunde",
        "branche": "Interior Design / Hochwertige Innenausstattung",
        "tags": ["miraglia", "kunde", "obrist-interior"],
    },
    "Bordoni Solutions": {
        "slug": "Bordoni-Solutions",
        "domain": "bordoni-solutions.com",
        "people": [("Mark Bordoni", "mark@bordoni-solutions.com", "Solutions Partner")],
        "typ": "partner",
        "branche": "Solutions / Consulting",
        "tags": ["miraglia", "partner", "bordoni-solutions"],
    },
    "Cloud Champion": {
        "slug": "Cloud-Champion",
        "domain": "cloudchampion.ch",
        "people": [("Daniel CloudChampion", "daniel@cloudchampion.ch", "Cloud / M365 Partner")],
        "typ": "partner",
        "branche": "Cloud / Microsoft 365",
        "tags": ["miraglia", "partner", "cloud-champion"],
    },
    "Koster AG": {
        "slug": "Koster-AG",
        "domain": "kosterag.ch",
        "people": [
            ("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt"),
            ("Monika Kuhn", "m.kuhn@kosterag.ch", "Projekt-Kontakt (App-Wartung)"),
            ("Franc Lechthaler", "f.lechthaler@kosterag.ch", "Direkter Kontakt (älter — 2023)"),
        ],
        "typ": "kunde",
        "branche": "Haustechnik (Heizung, Lüftung, Klima, Elektro, Sanitär)",
        "tags": ["miraglia", "kunde", "koster-ag"],
        "indirekte_kontakte": [
            ("Roger Kränzlin", "r.kraenzlin@kosterag.ch", "Geschäftsführer (Entscheider, kein Direktkontakt — läuft über Monika Kuhn / Heike Baumann)"),
        ],
    },
    "Hauswäckerling": {
        "slug": "Hauswaeckerling",
        "domain": "hauswaeckerling.ch",
        "people": [("Andreas Funke", "andreas.funke@hauswaeckerling.ch", "Projekt-Kontakt")],
        "typ": "kunde",
        "branche": "Betreuungs- und Pflegezentrum",
        "tags": ["miraglia", "kunde", "hauswaeckerling"],
    },
    "DOBI-Inter AG": {
        "slug": "DOBI-Inter-AG",
        "domain": "dobi.ch",
        "people": [
            ("Nenad Stojanovic", "nenad.stojanovic@dobi.ch", "Projekt-Kontakt"),
            ("Saveen Manocha", "saveen.manocha@dobi.ch", "Projekt-Kontakt"),
        ],
        "typ": "kunde",
        "branche": "Beauty-Fachhandel (Profi-Markt)",
        "tags": ["miraglia", "kunde", "dobi"],
    },
    "Hunnenberg": {
        "slug": "Hunnenberg",
        "domain": "hunnenberg.de",
        "people": [("TH Hunnenberg", "th@hunnenberg.de", "Projekt-Kontakt (Name unklar)")],
        "typ": "kunde",
        "branche": "Bodenbeläge, Teppich-Kettelei (Düsseldorf, DE)",
        "tags": ["miraglia", "kunde", "hunnenberg", "international"],
    },
}


def group_chats_for_firm(firm_emails):
    """Gruppen-Chats, in denen Personen dieser Firma teilnehmen."""
    out = []
    for gc in teams.get("group_chats", []):
        emails = [e.lower() for e in (gc.get("emails") or []) if e]
        if any(e in firm_emails for e in emails):
            out.append(gc)
    return sorted(out, key=lambda g: g["msg_count"], reverse=True)


def slug_for(name):
    return name.replace(" ", "-")


def build_firm_note(firm_name, info):
    slug = info["slug"]
    fpath = FIRMEN / f"{slug}.md"
    domain = info["domain"]

    # Profil (Webseite + Zefix)
    prof = profiles.get(firm_name, {})
    wd = prof.get("website", {}) or {}
    zefix = (prof.get("zefix", {}) or {}).get("matches", [])
    z0 = zefix[0] if zefix else {}

    # Personen-Aggregate
    person_lines = []
    total_mail = 0
    total_teams = 0
    latest_contact = ""
    firm_emails = set()
    for pname, pemail, prole in info["people"]:
        pemail_l = pemail.lower()
        firm_emails.add(pemail_l)
        m = mail_count.get(pemail_l, 0)
        t = teams_by_email.get(pemail_l, {})
        ti = t.get("interactions", 0)
        last = t.get("last", "")
        total_mail += m
        total_teams += ti
        if last > latest_contact:
            latest_contact = last
        person_lines.append(
            f"- [[50.work/25_People/{slug_for(pname)}|{pname}]] · {prole} · Mail {m} · Teams {ti} · letzter {last or '—'}"
        )

    # Gruppen-Chats / Projekte
    gc = group_chats_for_firm(firm_emails)
    project_lines = []
    for g in gc[:10]:
        topic = g.get("topic", "(ohne Titel)") or "(ohne Titel)"
        members = [m for m in (g.get("members") or []) if m]
        # Personen der eigenen Firma rausfiltern für „mit"-Liste
        own = {pname for pname, _, _ in info["people"]}
        externals = [m for m in members if m not in own][:5]
        line = f"- **{topic}** ({g['msg_count']} Nachrichten, letzter {g['last'] or '—'})"
        if externals:
            line += " — mit " + ", ".join(externals)
        project_lines.append(line)

    # Profil-Markdown-Block
    profile_block_lines = ["<!-- firmenprofil -->"]
    meta_parts = [z0.get("legalForm"), z0.get("legalSeat"), z0.get("uid")]
    meta = " · ".join(x for x in meta_parts if x)
    if meta:
        profile_block_lines += [f"*{meta}*", ""]
    if wd.get("title"):
        profile_block_lines.append(f"**Webseite-Titel:** {wd['title']}")
    if wd.get("description"):
        profile_block_lines.append(f"**Was sie tun:** {wd['description']}")
    if wd.get("url"):
        profile_block_lines.append(f"**Web:** {wd['url']}")
    if wd.get("_error"):
        profile_block_lines.append(f"_Hinweis: Webseite-Lookup fehlgeschlagen ({wd['_error']})_")
    if z0.get("canton") and z0.get("canton") != z0.get("legalSeat"):
        profile_block_lines.append(f"**Kanton:** {z0['canton']}")
    if z0.get("status") and z0["status"] != "active":
        profile_block_lines.append(f"**Status:** {z0['status']}")
    profile_block_lines.append("<!-- /firmenprofil -->")
    profile_block = "\n".join(profile_block_lines)

    # Frontmatter
    fm_lines = [
        "---",
        f"name: {firm_name}",
        f"slug: {slug}",
        f"domain: {domain}",
        f"typ: {info['typ']}",
        f"branche: {info['branche']}",
    ]
    if wd.get("url"):
        fm_lines.append(f"web: {wd['url']}")
    if z0.get("uid"):
        fm_lines.append(f"uid: {z0['uid']}")
    if z0.get("legalForm"):
        fm_lines.append(f"rechtsform: {z0['legalForm']}")
    if z0.get("legalSeat"):
        fm_lines.append(f"sitz: {z0['legalSeat']}")
    if z0.get("canton"):
        fm_lines.append(f"kanton: {z0['canton']}")
    fm_lines += [
        f"tags: [{', '.join(info['tags'])}]",
        "status: aktiv",
        "created: 2026-06-01",
        "source: m365-graph + claude-import",
        "---",
        "",
        f"# {firm_name}",
        "",
        f"**{info['branche']}**",
        "",
        "## Profil",
        "",
        profile_block,
        "",
        "## Personen",
        "",
        f"{len(info['people'])} Kontakt(e) bei {firm_name}:",
        "",
    ] + person_lines + [""]

    if project_lines:
        fm_lines += [
            "## Gemeinsame Projekte / Gruppen-Chats",
            "",
            *project_lines,
            "",
        ]
    else:
        fm_lines += [
            "## Gemeinsame Projekte / Gruppen-Chats",
            "",
            "_Keine Gruppen-Chats im aktuellen Scan-Fenster._",
            "",
        ]

    fm_lines += [
        "## Statistik (aggregiert über alle Personen der Firma)",
        "",
        f"- **Outlook-Mails:** {total_mail}",
        f"- **Teams-Interaktionen:** {total_teams}",
    ]
    if latest_contact:
        fm_lines.append(f"- **Letzter Kontakt:** {latest_contact}")

    # Indirekte Kontakte (Entscheider/Stakeholder ohne Direktkontakt)
    indirekte = info.get("indirekte_kontakte", [])
    if indirekte:
        fm_lines += [
            "",
            "## Indirekte Kontakte / Stakeholder",
            "",
            "_Personen bei der Firma, mit denen ich nicht direkt kommuniziere, "
            "die aber als Entscheider oder Informations-Knoten relevant sind._",
            "",
        ]
        for ip_name, ip_email, ip_rolle in indirekte:
            fm_lines.append(f"- **{ip_name}** (`{ip_email}`) — {ip_rolle}")

    fm_lines += [
        "",
        "## Persönliche Notizen",
        "",
        "_Manuelle Notizen zur Firma (Vertragsstand, Lieblings-Treffpunkt, "
        "Account-Manager-Wechsel, …) kommen hier hin._",
        "",
        "## Verwandt",
        "",
        "- [[50.work/26_Firmen/_Index|Firmen-Index]]",
        "- [[50.work/25_People/_Index|Personen-Index]]",
        "- [[50.work/m365-graph/04-company-enrich-workflow]] — Quelle des Profils",
    ]

    fpath.write_text("\n".join(fm_lines), encoding="utf-8")
    return fpath, total_mail, total_teams, len(info["people"]), len(gc)


def update_person_notes_with_firm_link():
    """Setzt in jede Personen-Notiz im Frontmatter `firma: [[50.work/26_Firmen/<slug>]]`."""
    updated = 0
    for firm_name, info in FIRMS.items():
        slug = info["slug"]
        for pname, _, _ in info["people"]:
            note = PEOPLE / f"{slug_for(pname)}.md"
            if not note.exists():
                continue
            txt = note.read_text(encoding="utf-8")
            # Ersetzt "firma: <Klartext>" durch Wikilink (nur im Frontmatter)
            # Frontmatter = zwischen erster und zweiter --- Zeile
            m = re.match(r"^(---\n)(.*?)(\n---\n)", txt, re.S)
            if not m:
                continue
            fm = m.group(2)
            # Nur ersetzen wenn noch nicht verlinkt
            if "[[50.work/26_Firmen/" in fm:
                continue
            fm_new = re.sub(
                r"^firma:\s*.*$",
                f"firma: \"[[50.work/26_Firmen/{slug}|{firm_name}]]\"",
                fm,
                count=1,
                flags=re.M,
            )
            if fm_new != fm:
                txt_new = m.group(1) + fm_new + m.group(3) + txt[m.end():]
                note.write_text(txt_new, encoding="utf-8")
                updated += 1
    return updated


def build_index():
    idx = FIRMEN / "_Index.md"
    lines = [
        "---", "source: m365-graph + claude-import", "imported: 2026-06-01",
        "type: firmen-index", "tags: [firmen, index, miraglia]", "---", "",
        "# Firmen-Index", "",
        f"Alle {len(FIRMS)} bekannten Firmen aus dem M365-Graph-Scan vom 01.06.2026.",
        "",
    ]
    by_typ = defaultdict(list)
    for firm_name, info in FIRMS.items():
        by_typ[info["typ"]].append((firm_name, info))
    for typ, label in [("intern", "Intern / Miraglia BI"),
                       ("partner", "Partner"),
                       ("kunde", "Kunden")]:
        if typ not in by_typ:
            continue
        lines += [f"## {label}", ""]
        for firm_name, info in by_typ[typ]:
            n_people = len(info["people"])
            # Aggregat
            tm = sum(mail_count.get(e.lower(), 0) for _, e, _ in info["people"])
            tt = sum(teams_by_email.get(e.lower(), {}).get("interactions", 0)
                     for _, e, _ in info["people"])
            lines.append(
                f"- [[{info['slug']}|{firm_name}]] · {info['branche']} · "
                f"{n_people} Person(en) · Mail {tm} · Teams {tt}"
            )
        lines.append("")

    lines += ["---", "",
              "_Generiert via Wrapper-Skript aus `company_profiles.json`, "
              "`teams_digest.json`, `mail_digest.json` und `25_People/`._"]
    idx.write_text("\n".join(lines), encoding="utf-8")
    return idx


def main():
    print(f"Build Firmen Notes → {FIRMEN}")
    print("-" * 60)
    for name, info in FIRMS.items():
        path, m, t, np, ng = build_firm_note(name, info)
        print(f"  ✓ {path.name:30s}  Mail:{m:4d}  Teams:{t:4d}  "
              f"Personen:{np}  Gruppen:{ng}")

    updated = update_person_notes_with_firm_link()
    print(f"\n  ✓ {updated} Personen-Notizen mit Firmen-Wikilink versehen")

    idx = build_index()
    print(f"  ✓ Index: {idx.name}")


if __name__ == "__main__":
    main()
