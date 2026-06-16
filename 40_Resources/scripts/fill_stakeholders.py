#!/usr/bin/env python3
"""
fill_stakeholders.py
--------------------
Trägt in die Kundenakten (20_Clients/) unter '## Stakeholder' die verknüpften
Personen (25_People/, Feld `client: [[...]]`) als Wikilinks ein.

Die Personen stehen in einem abgegrenzten Block:
    <!-- people-sync -->
    - [[Person|Name]] — Rolle
    <!-- /people-sync -->
Manuelle Einträge ausserhalb des Blocks bleiben erhalten.
Re-Läufe aktualisieren nur den Block.

Standard = Trockenlauf. Mit --apply wird geschrieben.
"""
import argparse
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE = ROOT / "25_People"
CLIENTS = ROOT / "20_Clients"

START, END = "<!-- people-sync -->", "<!-- /people-sync -->"


def fm_value(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"')


def h1_title(text, fallback):
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else fallback


def collect():
    by_client = defaultdict(list)
    for note in sorted(PEOPLE.glob("*.md")):
        text = note.read_text(encoding="utf-8")
        client = fm_value(text, "client")  # z.B. [[Upgreat]]
        if not client:
            continue
        m = re.search(r"\[\[([^\]|]+)", client)
        if not m:
            continue
        cname = m.group(1).strip()
        name = h1_title(text, note.stem)
        role = fm_value(text, "role")
        rel = fm_value(text, "relevance")
        by_client[cname].append({
            "base": note.stem, "name": name, "role": role,
            "rel": float(rel) if rel else -1.0,
        })
    return by_client


def make_block(people):
    # nach Relevanz absteigend, dann Name
    people = sorted(people, key=lambda p: (-p["rel"], p["name"]))
    lines = [START]
    for p in people:
        same = unicodedata.normalize("NFC", p["name"]) == unicodedata.normalize("NFC", p["base"])
        link = f"[[{p['base']}]]" if same else f"[[{p['base']}|{p['name']}]]"
        lines.append(f"- {link}" + (f" — {p['role']}" if p["role"] else ""))
    lines.append(END)
    return "\n".join(lines)


def update_note(text, block):
    # 1) bestehenden Block ersetzen
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    # 2) unter '## Stakeholder' einfügen, Platzhalter entfernen
    m = re.search(r"^##\s+Stakeholder[^\n]*\n", text, re.M)
    if m:
        insert_at = m.end()
        rest = text[insert_at:]
        # Platzhalterzeilen direkt darunter entfernen (- _tbd_, leere Bullets)
        rest = re.sub(r"\A(?:\s*-\s*(?:_tbd_)?\s*\n)+", "", rest)
        return text[:insert_at] + block + "\n" + rest
    # 3) keine Stakeholder-Sektion -> nach dem Frontmatter/H1 anlegen
    m = re.search(r"^#\s+.+\n", text, re.M)
    pos = m.end() if m else 0
    return text[:pos] + f"\n## Stakeholder\n{block}\n" + text[pos:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    by_client = collect()
    changed = 0
    for cname, people in sorted(by_client.items()):
        cfile = CLIENTS / f"{cname}.md"
        if not cfile.exists():
            print(f"  ⚠ Client-Notiz fehlt: {cname}.md ({len(people)} Personen) — übersprungen")
            continue
        block = make_block(people)
        print(f"\n### {cname} ({len(people)}) ###")
        for line in block.splitlines()[1:-1]:
            print(f"  {line}")
        if args.apply:
            text = cfile.read_text(encoding="utf-8")
            new = update_note(text, block)
            if new != text:
                cfile.write_text(new, encoding="utf-8")
                changed += 1

    if args.apply:
        print(f"\n✓ {changed} Kundenakten aktualisiert.")
    else:
        print("\n(Trockenlauf — nichts geschrieben. Mit --apply anwenden.)")


if __name__ == "__main__":
    main()
