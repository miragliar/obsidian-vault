#!/usr/bin/env python3
"""
create_teams_people.py
----------------------
Legt Personen-Notizen für NEUE Teams-Kontakte an (aus teams_people.json),
mit Firmenzugehörigkeit (Domain), Client-Link und Teams-Charakterisierung.
Statistik (Interaktionen/letzter) kommt aus teams_digest.json.
Bestehende Notizen werden NICHT überschrieben.

Standard = Trockenlauf; --apply schreibt.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PEOPLE = SCRIPT_DIR.parent.parent / "25_People"
DATA = SCRIPT_DIR / "teams_people.json"
DIGEST = SCRIPT_DIR / "teams_digest.json"
TODAY = "2026-05-30"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def safe(name):
    return re.sub(r"\s+", " ", re.sub(r'[\\/:*?"<>|#^\[\]]', "", name)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding="utf-8"))
    stats = {nfc((p.get("email") or "").lower()): p
             for p in json.loads(DIGEST.read_text(encoding="utf-8"))["people"]}
    existing = {nfc(p.name) for p in PEOPLE.glob("*.md")}

    created = skipped = 0
    for email, d in data.items():
        fname = safe(d["name"]) + ".md"
        if nfc(fname) in existing:
            print(f"= existiert: {d['name']}"); skipped += 1; continue
        st = stats.get(nfc(email.lower()), {})
        tags = ["person", "contact", "teams"] + ([d["kind"]] if d.get("kind") else [])
        fm = ["---", "type: person", "status: active", f"created: {TODAY}", f"email: {email}",
              f'company: "{d["company"]}"']
        if d.get("client"):
            fm.append(f'client: "[[{d["client"]}]]"')
        fm.append(f"source: [teams]")
        fm.append(f"tags: [{', '.join(tags)}]")
        fm.append("---")
        beziehung = d.get("beziehung", "")
        body = [f"# {d['name']}", "",
                "## Profil",
                f"- **Firma:** {d['company']}" + (f" → [[{d['client']}]]" if d.get("client") else ""),
                f"- **Rolle:** {d.get('role','_tbd_')}",
                f"- **Beziehung:** {beziehung}",
                "", "## Contact", f"- **Email:** {email}",
                "", "## 💬 Teams-Kontext",
                "<!-- teams-summary -->",
                f"*Stand: {TODAY} · {st.get('interactions','?')} Interaktionen "
                f"({st.get('in_1to1','?')}×1:1 / {st.get('in_group','?')}×Gruppe) · "
                f"letzter Kontakt {st.get('last','?')}*", "",
                d["char"], "<!-- /teams-summary -->",
                "", "## Log", f"- {TODAY} — Aus Teams-Analyse angelegt"]
        text = "\n".join(fm) + "\n" + "\n".join(body) + "\n"
        print(f"+ {d['name']:26s} → {d['company']}" + (f" [[{d['client']}]]" if d.get('client') else ""))
        if args.apply:
            (PEOPLE / fname).write_text(text, encoding="utf-8")
            created += 1
    print(f"\n{'✓ ' + str(created) + ' angelegt' if args.apply else '(Trockenlauf)'}, {skipped} übersprungen.")


if __name__ == "__main__":
    main()
