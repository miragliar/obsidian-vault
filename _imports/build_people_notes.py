#!/usr/bin/env python3
"""
build_people_notes.py
---------------------
Aus mail_digest.json + teams_digest.json baut dieses Skript Personen-Notizen
in 25_People/. Modus: nur Metadaten + Themen-Schlagwörter, keine Roh-Texte.
"""
import json
import re
from pathlib import Path
from collections import Counter

VAULT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul")
SCRIPTS = VAULT / "50.work" / "m365-graph" / "scripts"
PEOPLE = VAULT / "50.work" / "25_People"
PEOPLE.mkdir(exist_ok=True)

mail = json.loads((SCRIPTS / "mail_digest.json").read_text())
teams = json.loads((SCRIPTS / "teams_digest.json").read_text())

mail_count = {item["email"].lower(): item["total"] for item in mail.get("frequent_without_note", [])}
for p in mail.get("people", []):
    mail_count[p["email"].lower()] = p.get("total", 0)

# Merge mehrfacher Einträge (Person taucht oft 2× auf: intern + guest)
teams_by_email = {}
for p in teams.get("people", []):
    e = (p.get("email") or "").lower()
    if not e:
        continue
    if e not in teams_by_email:
        teams_by_email[e] = {
            "name": p.get("name", ""), "email": e,
            "interactions": 0, "msgs_from": 0, "my_replies_1to1": 0,
            "in_1to1": 0, "in_group": 0, "last": "", "samples": [],
        }
    t = teams_by_email[e]
    t["interactions"] += p.get("interactions", 0)
    t["msgs_from"] += p.get("msgs_from", 0)
    t["my_replies_1to1"] += p.get("my_replies_1to1", 0)
    t["in_1to1"] += p.get("in_1to1", 0)
    t["in_group"] += p.get("in_group", 0)
    if p.get("last", "") > t["last"]:
        t["last"] = p["last"]
    t["samples"].extend(p.get("samples", []))

person_groups = {}
for gc in teams.get("group_chats", []):
    topic = gc.get("topic", "") or "(ohne Titel)"
    members = gc.get("members") or []
    emails = gc.get("emails") or []
    for em in emails:
        em = em.lower()
        person_groups.setdefault(em, []).append({
            "topic": topic,
            "msg_count": gc.get("msg_count", 0),
            "members": [m for m in members if m]
        })

CONTACTS = [
    {"name": "Giovanni Miraglia", "email": "giovanni@miraglia-bi.com",
     "firma": "Miraglia Business-Intelligence", "typ": "kollege",
     "rolle": "Chef / Gründer", "tags": ["miraglia", "kollege", "miraglia-bi"]},
    {"name": "Michael Kipfer", "email": "michael@kipfer-dp.com",
     "firma": "Kipfer DP", "typ": "partner",
     "rolle": "Power Platform Partner", "tags": ["miraglia", "partner", "kipfer-dp"]},
    {"name": "Alessandro Castelli", "email": "alessandro@castelli-solutions.ch",
     "firma": "Castelli Solutions", "typ": "partner",
     "rolle": "Power Platform Partner", "tags": ["miraglia", "partner", "castelli-solutions"]},
    {"name": "Remo Pfister", "email": "r.pfister@mvm-ag.ch",
     "firma": "MVM AG", "typ": "kunde",
     "rolle": "Power Platform Ansprechperson", "tags": ["miraglia", "kunde", "mvm-ag"]},
    {"name": "Stefanie Ringwald", "email": "stefanie.ringwald@nahrin.ch",
     "firma": "Nahrin AG", "typ": "kunde",
     "rolle": "Power Platform Ansprechperson", "tags": ["miraglia", "kunde", "nahrin"]},
    {"name": "Christoph Kübler", "email": "christoph.kuebler@nahrin.ch",
     "firma": "Nahrin AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt", "tags": ["miraglia", "kunde", "nahrin"]},
    {"name": "Barbara Gilli", "email": "b.gilli@obrist-interior.ch",
     "firma": "Obrist Interior", "typ": "kunde",
     "rolle": "Projekt-Kontakt", "tags": ["miraglia", "kunde", "obrist-interior"]},
    {"name": "Mark Bordoni", "email": "mark@bordoni-solutions.com",
     "firma": "Bordoni Solutions", "typ": "partner",
     "rolle": "Solutions Partner", "tags": ["miraglia", "partner", "bordoni-solutions"]},
    {"name": "Daniel CloudChampion", "email": "daniel@cloudchampion.ch",
     "firma": "Cloud Champion", "typ": "partner",
     "rolle": "Cloud / M365 Partner", "tags": ["miraglia", "partner", "cloud-champion"]},
    {"name": "H. Baumann", "email": "h.baumann@kosterag.ch",
     "firma": "Koster AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt", "tags": ["miraglia", "kunde", "koster-ag"]},
    # Erweiterungen 01.06.2026 — nach Recherche regelmässiger Kontakte (last 18 Monate)
    {"name": "Tobias Lamprecht", "email": "t.lamprecht@obrist-interior.ch",
     "firma": "Obrist Interior", "typ": "kunde",
     "rolle": "Projekt-Kontakt (Zeugnis-App)",
     "tags": ["miraglia", "kunde", "obrist-interior"]},
    {"name": "Bianca Tschuppert", "email": "b.tschuppert@obrist-interior.ch",
     "firma": "Obrist Interior", "typ": "kunde",
     "rolle": "Projekt-Kontakt (Zeugnis-App)",
     "tags": ["miraglia", "kunde", "obrist-interior"]},
    {"name": "Monika Kuhn", "email": "m.kuhn@kosterag.ch",
     "firma": "Koster AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt (App-Wartung)",
     "tags": ["miraglia", "kunde", "koster-ag"]},
    {"name": "M. Schärli", "email": "m.schaerli@mvm-ag.ch",
     "firma": "MVM AG", "typ": "kunde",
     "rolle": "Mail-Kontakt",
     "tags": ["miraglia", "kunde", "mvm-ag"]},
    {"name": "Andreas Funke", "email": "andreas.funke@hauswaeckerling.ch",
     "firma": "Hauswäckerling", "typ": "kunde",
     "rolle": "Projekt-Kontakt (Averecura)",
     "tags": ["miraglia", "kunde", "hauswaeckerling"]},
    {"name": "Nenad Stojanovic", "email": "nenad.stojanovic@dobi.ch",
     "firma": "DOBI-Inter AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt",
     "tags": ["miraglia", "kunde", "dobi"]},
    {"name": "Saveen Manocha", "email": "saveen.manocha@dobi.ch",
     "firma": "DOBI-Inter AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt",
     "tags": ["miraglia", "kunde", "dobi"]},
    {"name": "TH Hunnenberg", "email": "th@hunnenberg.de",
     "firma": "Hunnenberg", "typ": "kunde",
     "rolle": "Projekt-Kontakt (Bodenbeläge, Name unklar — TH = Initialen)",
     "tags": ["miraglia", "kunde", "hunnenberg", "international"]},
    # Nachtrag 2026-06-01 — direkter Koster-Kontakt (älter aber relevant)
    {"name": "Franc Lechthaler", "email": "f.lechthaler@kosterag.ch",
     "firma": "Koster AG", "typ": "kunde",
     "rolle": "Direkter Kontakt (älter — 2023)",
     "tags": ["miraglia", "kunde", "koster-ag"]},
]

STOPWORDS = set("""der die das ein eine einer einen einem und oder aber denn doch
wenn dann als wie so zu zum zur in im an am auf aus bei mit nach von vom für gegen
ohne über unter durch bis dass dafür darauf darin damit dazu hier dort heute
gestern morgen jetzt immer noch schon mal nur sehr auch nicht kein keine
keinem keiner keines mein dein sein unser euer ihrer
habe hat hatte haben hatten ist sind war waren werde wird wurde
worden mache machst macht bisschen kannst kann sollte würde
würden also dann eigentlich genau weil halt wieder hallo guten morgen abend
könnte können müssen sollst denke meine cmd cmdlet über ach gibts gibt
geht weiter unter danke gerne gesagt schon glaub get yes okay ohne wenn
ueber waere weiss kenne moeglich heisst kommen einfach evtl jedoch jedem aber
naechste klein gross sache""".split())


def extract_topics(samples, top_n=5):
    if not samples:
        return []
    words = []
    for s in samples:
        text = s.get("text", "")
        for w in re.findall(r"[A-Za-zÄÖÜäöü][A-Za-zÄÖÜäöü0-9_-]{3,}", text):
            wl = w.lower()
            if wl in STOPWORDS or len(wl) < 4:
                continue
            words.append(w)
    if not words:
        return []
    cap_counter = Counter(w for w in words if w[0].isupper())
    lower_counter = Counter(w.lower() for w in words if not w[0].isupper())
    topics = []
    for w, c in cap_counter.most_common(top_n * 2):
        if c >= 2:
            topics.append((w, c))
    for w, c in lower_counter.most_common(top_n * 2):
        if c >= 2 and not any(t[0].lower() == w for t in topics):
            topics.append((w, c))
    return [t[0] for t in topics[:top_n]]


def slug(name):
    return name.replace(" ", "-")


def build_note(contact):
    email = contact["email"].lower()
    domain = email.split("@")[1] if "@" in email else ""
    name = contact["name"]
    fpath = PEOPLE / f"{slug(name)}.md"

    m_total = mail_count.get(email, 0)
    t = teams_by_email.get(email, {})
    t_interactions = t.get("interactions", 0)
    t_msgs_from = t.get("msgs_from", 0)
    t_my_replies = t.get("my_replies_1to1", 0)
    t_in_1to1 = t.get("in_1to1", 0)
    t_in_group = t.get("in_group", 0)
    t_last = t.get("last", "")
    samples = t.get("samples", [])
    topics = extract_topics(samples, top_n=8)
    groups = person_groups.get(email, [])

    fm = [
        "---",
        f"name: {name}",
        f"email: {email}",
        f"firma: {contact['firma']}",
        f"domain: {domain}",
        f"typ: {contact['typ']}",
        f"rolle: {contact['rolle']}",
        f"tags: [{', '.join(contact['tags'])}]",
        "status: aktiv",
        "created: 2026-06-01",
        "source: m365-graph + claude-import",
        "---",
        "",
        f"# {name}",
        "",
        f"**{contact['firma']} — {contact['rolle']}**",
        "",
        "## Persönliche Notizen",
        "",
        "_Manuelle Notizen kommen hier hin._",
        "",
        "## Mail- & Chat-Verlauf",
        "",
        "<!-- mail-summary -->",
        "**Stand: 2026-06-01** (M365 Graph Digest)",
        "",
        "**Statistik:**",
    ]
    if m_total:
        fm.append(f"- Outlook-Mails (in 2'500 letzten): **{m_total}**")
    if t_interactions:
        fm.append(f"- Teams-Interaktionen: **{t_interactions}** "
                  f"({t_msgs_from} von Person, {t_my_replies} meine 1:1-Antworten)")
        fm.append(f"  - 1:1-Nachrichten: {t_in_1to1}")
        fm.append(f"  - Gruppen-Nachrichten: {t_in_group}")
        if t_last:
            fm.append(f"- Letzter Teams-Kontakt: **{t_last}**")
    if not m_total and not t_interactions:
        fm.append("- Keine Aktivität im aktuellen Scan-Fenster.")

    if groups:
        fm.append("")
        fm.append("**Gemeinsame Projekte / Gruppen-Chats:**")
        for g in sorted(groups, key=lambda x: x["msg_count"], reverse=True)[:6]:
            others = [m for m in g["members"] if m and m != name]
            othertext = f" — mit {', '.join(others[:3])}" if others else ""
            fm.append(f"- **{g['topic']}** ({g['msg_count']} Nachrichten){othertext}")

    if topics:
        fm.append("")
        fm.append("**Wiederkehrende Begriffe / Themen** (aus Chat-Samples extrahiert):")
        fm.append("- " + " · ".join(topics))

    fm += [
        "<!-- /mail-summary -->",
        "",
        "## Verwandt",
        "",
        f"- [[50.work/m365-graph/setup-und-workflow]] — Quelle der Aggregation",
        f"- [[50.work/power-platform/_README]]",
    ]

    fpath.write_text("\n".join(fm), encoding="utf-8")
    return fpath, m_total, t_interactions, len(groups), len(topics)


def main():
    print(f"Build People Notes → {PEOPLE}")
    print("-" * 60)
    for c in CONTACTS:
        path, m, t, g, k = build_note(c)
        print(f"  ✓ {path.name:30s}  Mail:{m:4d}  Teams:{t:4d}  Groups:{g}  Topics:{k}")

    idx = PEOPLE / "_Index.md"
    lines = [
        "---", "source: m365-graph + claude-import", "imported: 2026-06-01",
        "type: people-index", "tags: [people, index, miraglia]", "---", "",
        "# Personen-Index", "",
        "Top humane Kontakte aus dem M365-Graph-Scan vom 01.06.2026 "
        f"(2'500 Mails / 1'621 Teams-Nachrichten / 300 Chats).", "",
    ]
    by_typ = {"kollege": [], "partner": [], "kunde": []}
    for c in CONTACTS:
        by_typ.setdefault(c["typ"], []).append(c)
    for typ, label in [("kollege", "Kollegen / Miraglia BI"),
                       ("partner", "Partner"),
                       ("kunde", "Kunden")]:
        if not by_typ.get(typ):
            continue
        lines += [f"## {label}", ""]
        for c in by_typ[typ]:
            t = teams_by_email.get(c["email"].lower(), {})
            m = mail_count.get(c["email"].lower(), 0)
            ti = t.get("interactions", 0)
            last = t.get("last", "—")
            lines.append(f"- [[{slug(c['name'])}|{c['name']}]] · {c['firma']} · Mail {m} · Teams {ti} · letzter {last}")
        lines.append("")

    lines += ["---", "",
              "_Generiert von `_imports/build_people_notes.py` aus den "
              "`mail_digest.json` + `teams_digest.json` Outputs._"]
    idx.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  ✓ Index: {idx.name}")


if __name__ == "__main__":
    main()
