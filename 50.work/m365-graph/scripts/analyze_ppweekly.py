#!/usr/bin/env python3
"""
analyze_ppweekly.py
-------------------
Analysiert das ppweekly_digest.json (156 Newsletter-Ausgaben) nach:
- Sektionen pro Issue (Articles, Podcasts, Videos, Events, Out of the Blue)
- Häufig erwähnte Personen (Autoren, Hosts, Guests)
- Releases / GA Announcements
- Wiederkehrende Podcasts
- Events / Conferences

Schreibt:
  ppweekly_analysis.json  — strukturierter Datensatz fürs Note-Building
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

SD = Path(__file__).resolve().parent
IN = SD / "ppweekly_digest.json"
OUT = SD / "ppweekly_analysis.json"

# Sektions-Marker im Newsletter
SECTION_PATTERNS = [
    (r"📰\s*Articles", "articles"),
    (r"📺\s*Videos", "videos"),
    (r"🎙️\s*Podcasts", "podcasts"),
    (r"🎙\s*Podcasts", "podcasts"),
    (r"📅\s*Events\s*&\s*Webinars", "events"),
    (r"💙\s*Out of the Blue", "out_of_blue"),
    (r"🚀\s*Releases", "releases"),
    (r"📚\s*Books", "books"),
    (r"💡\s*Tips\s*&\s*Tricks", "tips"),
    (r"🛠\s*Tools", "tools"),
    (r"💼\s*Jobs", "jobs"),
]


def split_sections(body: str):
    """Teilt den Mail-Body in Sektionen."""
    sections = {}
    # Erst alle Marker mit Position finden
    matches = []
    for pat, key in SECTION_PATTERNS:
        for m in re.finditer(pat, body):
            matches.append((m.start(), key, m.end()))
    matches.sort()
    # Body in Stücke zwischen den Markern teilen
    for i, (start, key, end) in enumerate(matches):
        next_start = matches[i + 1][0] if i + 1 < len(matches) else len(body)
        chunk = body[end:next_start].strip()
        sections.setdefault(key, []).append(chunk)
    return sections


def extract_issue_number(subject: str) -> int | None:
    m = re.search(r"#(\d+)", subject)
    return int(m.group(1)) if m else None


def extract_authors_from_chunk(chunk: str) -> list[str]:
    """
    Holt 'by <Person Name>' und 'Name <whitespace> Name' nach Emojis (🦸🏻‍♀️, 👩‍💻 etc.)
    Beispiele:
      "by Megan V. Walker"
      "Angeliki Patsiavou shows us"
    """
    out = []
    # 'by <Name>'
    for m in re.finditer(r"\bby\s+([A-Z][A-Za-zÀ-ÿ\.\-]+(?:\s+[A-Z][A-Za-zÀ-ÿ\.\-]+){1,3})", chunk):
        name = m.group(1).strip().rstrip(".,;:")
        if 6 <= len(name) <= 60:
            out.append(name)
    return out


def extract_people_global(body: str) -> list[str]:
    """Sammelt Personennamen 'Vorname Nachname' Muster + Standard MVP/Microsoft Namen die wir erkennen."""
    # Konservativ: "X Y" wo X und Y beide großgeschrieben sind
    candidates = re.findall(
        r"\b([A-Z][a-zà-ÿ]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-zà-ÿ]+(?:\s+[A-Z][a-zà-ÿ]+)?)\b",
        body,
    )
    # Filter Müll
    out = []
    blacklist = {
        "Power Platform", "Microsoft Build", "Microsoft 365", "Microsoft Power",
        "Power Apps", "Power Automate", "Power BI", "Power Pages", "Power Fx",
        "Copilot Studio", "Customer Insights", "Customer Service",
        "Business Central", "Business Applications", "Business Process",
        "App Source", "AppSource", "United States", "United Kingdom", "New York",
        "Microsoft Dataverse", "Microsoft Fabric", "Microsoft Teams", "Las Vegas",
        "Out of", "Read More", "Subscribe Now", "Subscribe Here", "Welcome to",
        "Nordic Summit", "Scottish Summit", "Community Summit", "Power Platform Conference",
        "Power Platform Weekly", "Book Of", "Book of", "Click Here", "View in",
        "On Demand", "Demo App", "Microsoft Build", "Last Week",
    }
    for c in candidates:
        if c in blacklist:
            continue
        if any(b in c for b in ["Microsoft", "Platform", "Apps", "Studio", "Dataverse",
                                "Fabric", "Copilot", "Summit", "Conference", "Webinar"]):
            continue
        out.append(c)
    return out


def main():
    digest = json.loads(IN.read_text())

    issues = []
    all_authors = Counter()
    all_people = Counter()
    podcast_names = Counter()
    releases = []
    events = []

    for m in digest:
        issue_num = extract_issue_number(m["subject"])
        body = m["body_text"]
        secs = split_sections(body)

        articles_text = "\n".join(secs.get("articles", []))
        podcasts_text = "\n".join(secs.get("podcasts", []))
        videos_text = "\n".join(secs.get("videos", []))
        events_text = "\n".join(secs.get("events", []))
        out_of_blue_text = "\n".join(secs.get("out_of_blue", []))

        # Autoren in Articles + Releases
        for a in extract_authors_from_chunk(articles_text):
            all_authors[a] += 1
        for a in extract_authors_from_chunk(out_of_blue_text):
            all_authors[a] += 1

        # Personen global
        for p in extract_people_global(body):
            all_people[p] += 1

        # Podcast Names (vor "Podcast")
        for pm in re.finditer(r"([A-Z][\w\.\s&\-]+Podcast)", podcasts_text):
            name = pm.group(1).strip()
            if 5 <= len(name) <= 60:
                podcast_names[name] += 1

        # Events: extrahiere "Name (📅 Datum)"
        for em in re.finditer(r"([A-Z][\w\s\-&\.]+?)\s*\(📅\s*([^\)]+)\)", events_text):
            events.append({
                "issue": issue_num,
                "received": m["received"][:10],
                "name": em.group(1).strip(),
                "when": em.group(2).strip(),
            })

        # Releases: gesamter "Out of the Blue" Text in Items splitten
        # Jeder Item beginnt typischerweise mit Titel und endet mit Autorenname
        if out_of_blue_text:
            # Lose Aufteilung an doppelten Newlines
            items = re.split(r"\n\s*\n+", out_of_blue_text)
            for it in items:
                it_clean = it.strip()
                if 30 < len(it_clean) < 1500:
                    releases.append({
                        "issue": issue_num,
                        "received": m["received"][:10],
                        "text": it_clean,
                    })

        issues.append({
            "issue": issue_num,
            "received": m["received"][:10],
            "subject": m["subject"],
            "webLink": m.get("webLink", ""),
            "section_lengths": {k: sum(len(x) for x in v) for k, v in secs.items()},
            "articles": articles_text,
            "podcasts": podcasts_text,
            "videos": videos_text,
            "events": events_text,
            "out_of_blue": out_of_blue_text,
        })

    result = {
        "n_issues": len(issues),
        "issues": issues,
        "top_authors": all_authors.most_common(50),
        "top_people": all_people.most_common(80),
        "podcast_names": podcast_names.most_common(40),
        "events": events,
        "releases_count": len(releases),
    }

    # Releases separat (groß)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (SD / "ppweekly_releases.json").write_text(
        json.dumps(releases, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Analyse gespeichert -> {OUT.name}")
    print(f"  Issues:           {len(issues)}")
    print(f"  Top-Autoren:      {len(all_authors)} eindeutige")
    print(f"  Top-Personen:     {len(all_people)} eindeutige")
    print(f"  Podcast-Namen:    {len(podcast_names)} eindeutige")
    print(f"  Events:           {len(events)}")
    print(f"  'Out of Blue' Items: {len(releases)}")
    print()
    print("Top 20 Autoren (Artikel + Out of the Blue):")
    for name, cnt in all_authors.most_common(20):
        print(f"  {cnt:3d}  {name}")
    print()
    print("Top 15 Podcast-Sektionen:")
    for name, cnt in podcast_names.most_common(15):
        print(f"  {cnt:3d}  {name}")


if __name__ == "__main__":
    main()
