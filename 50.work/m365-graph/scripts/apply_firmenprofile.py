#!/usr/bin/env python3
"""
apply_firmenprofile.py
----------------------
Schreibt Unternehmensdaten (aus firmenprofile.json) in die Client-Notizen:
- Frontmatter-Eigenschaften: branche, rechtsform, gegruendet, uid, hauptsitz, website
- Abschnitt '## Unternehmensprofil' (managed <!-- firmenprofil -->-Block, idempotent)

Standard = Trockenlauf; --apply schreibt.
"""
import argparse
import json
import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
# Pfad per Env-Var anpassbar — Default = Michaels PARA-Layout.
# Bei Raoul z.B. CLIENTS_DIR=26_Firmen (siehe scripts/.env).
CLIENTS = SCRIPT_DIR.parent.parent / os.environ.get("CLIENTS_DIR", "20_Clients")
DATA = SCRIPT_DIR / "firmenprofile.json"
FM_KEYS = ["branche", "rechtsform", "gegruendet", "uid", "hauptsitz", "website"]
START, END = "<!-- firmenprofil -->", "<!-- /firmenprofil -->"


def q(v):
    return '"' + str(v).replace("\\", "\\\\").replace('"', '\\"') + '"'


def set_frontmatter(text, key, value):
    """Setzt key:value im Frontmatter (ersetzt vorhandene Zeile oder fügt vor schliessendem --- ein)."""
    line = f"{key}: {q(value)}"
    if re.search(rf"^{key}:.*$", text, re.M):
        return re.sub(rf"^{key}:.*$", line, text, count=1, flags=re.M)
    # vor dem schliessenden --- des Frontmatters einfügen
    m = re.search(r"^---\n.*?\n(---)\n", text, re.S)
    if not m:
        return text
    pos = m.start(1)
    return text[:pos] + line + "\n" + text[pos:]


def build_block(d):
    facts = []
    if d.get("rechtsform"):
        facts.append(d["rechtsform"])
    if d.get("gegruendet"):
        facts.append(f"gegründet {d['gegruendet']}")
    if d.get("hauptsitz"):
        facts.append(d["hauptsitz"])
    if d.get("uid"):
        facts.append(f"UID {d['uid']}")
    if d.get("website"):
        facts.append(f"[Web]({d['website']})")
    lines = [START, "*" + " · ".join(facts) + "*", ""]
    if d.get("kurzbeschrieb"):
        lines.append(f"**Was sie tun:** {d['kurzbeschrieb']}")
    if d.get("branche"):
        lines.append(f"**Branche:** {d['branche']}")
    if d.get("produkte"):
        lines.append(f"**Produkte / Services:** {d['produkte']}")
    if d.get("merkmale"):
        lines.append(f"**Merkmale:** {d['merkmale']}")
    lines.append(END)
    return "\n".join(lines)


def insert_block(text, block):
    if START in text and END in text:
        return re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    section = f"## Unternehmensprofil\n{block}\n\n"
    # vor '## Stakeholder' einfügen, sonst nach dem Frontmatter/H1
    m = re.search(r"^## Stakeholder", text, re.M)
    if m:
        return text[:m.start()] + section + text[m.start():]
    m = re.search(r"^# .+\n", text, re.M)
    pos = m.end() if m else 0
    return text[:pos] + "\n" + section + text[pos:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    data = json.loads(DATA.read_text(encoding="utf-8"))

    done = missing = 0
    for key, d in data.items():
        note = CLIENTS / f"{key}.md"
        if not note.exists():
            print(f"⚠ fehlt: {key}.md"); missing += 1; continue
        text = note.read_text(encoding="utf-8")
        for k in FM_KEYS:
            if d.get(k):
                text = set_frontmatter(text, k, d[k])
        text = insert_block(text, build_block(d))
        print(f"✓ {key:24s} {d.get('rechtsform','?')} · {d.get('gegruendet','?')} · {d.get('hauptsitz','?')}")
        if args.apply:
            note.write_text(text, encoding="utf-8"); done += 1
    print(f"\n{('✓ ' + str(done) + ' Notizen aktualisiert') if args.apply else '(Trockenlauf)'}, {missing} fehlen.")


if __name__ == "__main__":
    main()
