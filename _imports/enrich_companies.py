#!/usr/bin/env python3
"""enrich_companies.py — Batch-Firmen-Profile + Personen-Notiz-Anreicherung.

Standard: nur Webseite. Mit ZEFIX_USER + ZEFIX_PASS in der Umgebung wird
automatisch auch Zefix abgefragt (UID, Rechtsform, Sitz, Kanton, Status).
"""
import json
import os
import re
import subprocess
from pathlib import Path

VAULT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul")
SCRIPTS = VAULT / "50.work" / "m365-graph" / "scripts"
PEOPLE = VAULT / "50.work" / "25_People"
COMPANY_SCRIPT = SCRIPTS / "company_enrich.py"
PROFILES_OUT = SCRIPTS / "company_profiles.json"
VENV_PY = SCRIPTS / ".venv" / "bin" / "python3"

FIRMS = {
    "Miraglia Business-Intelligence": {"url": "https://www.miraglia-bi.com",
                                       "people": ["Giovanni-Miraglia.md"]},
    "Kipfer DP": {"url": "https://www.kipfer-dp.com",
                  "people": ["Michael-Kipfer.md"]},
    "Castelli Solutions": {"url": "https://www.castelli-solutions.ch",
                           "people": ["Alessandro-Castelli.md"]},
    "MVM AG": {"url": "https://www.mvm-ag.ch",
               "people": ["Remo-Pfister.md", "M.-Schärli.md"]},
    "Nahrin AG": {"url": "https://www.nahrin.ch",
                  "people": ["Stefanie-Ringwald.md", "Christoph-Kübler.md"]},
    "Obrist Interior": {"url": "https://www.obrist-interior.ch",
                        "people": ["Barbara-Gilli.md", "Tobias-Lamprecht.md", "Bianca-Tschuppert.md"]},
    "Bordoni Solutions": {"url": "https://www.bordoni-solutions.com",
                          "people": ["Mark-Bordoni.md"]},
    "Cloud Champion": {"url": "https://www.cloudchampion.ch",
                       "people": ["Daniel-CloudChampion.md"]},
    "Koster AG": {"url": "https://www.kosterag.ch",
                  "people": ["H.-Baumann.md", "Monika-Kuhn.md"]},
    "Hauswäckerling": {"url": "https://www.hauswaeckerling.ch",
                       "people": ["Andreas-Funke.md"]},
    "DOBI-Inter AG": {"url": "https://www.dobi.ch",
                      "people": ["Nenad-Stojanovic.md", "Saveen-Manocha.md"]},
    "Hunnenberg": {"url": "https://www.hunnenberg.de",
                   "people": ["TH-Hunnenberg.md"]},
}


USE_ZEFIX = bool(os.environ.get("ZEFIX_USER") and os.environ.get("ZEFIX_PASS"))


def run_enrich(name, url):
    cmd = [str(VENV_PY), str(COMPANY_SCRIPT), "--name", name, "--url", url]
    if USE_ZEFIX:
        cmd.append("--zefix")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        stdout = result.stdout.split("----- Markdown -----")[0]
        return json.loads(stdout)
    except subprocess.TimeoutExpired:
        return {"name": name, "_error": "Timeout"}
    except json.JSONDecodeError as e:
        return {"name": name, "_error": f"JSONDecode: {e}", "raw": (result.stdout if 'result' in locals() else '')[:300]}


def build_md_block(profile):
    wd = profile.get("website", {}) or {}
    zefix = (profile.get("zefix", {}) or {}).get("matches", [])
    z0 = zefix[0] if zefix else {}
    meta = " · ".join(x for x in [z0.get("legalForm"), z0.get("legalSeat"), z0.get("uid")] if x)
    lines = ["<!-- firmenprofil -->"]
    if meta:
        lines += [f"*{meta}*", ""]
    if wd.get("title"):
        lines.append(f"**Webseite-Titel:** {wd['title']}")
    if wd.get("description"):
        lines.append(f"**Was sie tun:** {wd['description']}")
    if wd.get("url"):
        lines.append(f"**Web:** {wd['url']}")
    if wd.get("_error"):
        lines.append(f"_Hinweis: Webseite-Lookup fehlgeschlagen ({wd['_error']})_")
    lines.append("<!-- /firmenprofil -->")
    return "\n".join(lines)


def insert_firmenprofil(note_path, md_block):
    if not note_path.exists():
        print(f"   ✗ Notiz fehlt: {note_path.name}")
        return False
    txt = note_path.read_text(encoding="utf-8")
    existing = re.search(r"<!-- firmenprofil -->.*?<!-- /firmenprofil -->", txt, re.S)
    if existing:
        txt_new = txt[:existing.start()] + md_block + txt[existing.end():]
        note_path.write_text(txt_new, encoding="utf-8")
        return True
    marker = "<!-- /mail-summary -->"
    if marker in txt:
        idx = txt.index(marker) + len(marker)
        new_section = "\n\n## Unternehmensprofil\n\n" + md_block
        txt_new = txt[:idx] + new_section + txt[idx:]
        note_path.write_text(txt_new, encoding="utf-8")
        return True
    txt_new = txt.rstrip() + "\n\n## Unternehmensprofil\n\n" + md_block + "\n"
    note_path.write_text(txt_new, encoding="utf-8")
    return True


def main():
    print(f"Enrich Companies → {len(FIRMS)} firms"
          f" {'(mit Zefix)' if USE_ZEFIX else '(nur Webseite, kein Zefix)'}")
    print("-" * 60)
    all_profiles = {}
    for name, info in FIRMS.items():
        print(f"\n▶ {name} ({info['url']})")
        prof = run_enrich(name, info["url"])
        all_profiles[name] = prof
        wd = prof.get("website", {}) or {}
        if wd.get("_error"):
            print(f"   ⚠ {wd['_error']}")
        elif wd.get("description"):
            print(f"   ✓ {wd['description'][:80]}…")
        elif wd.get("title"):
            print(f"   ✓ Title: {wd['title'][:80]}")
        md = build_md_block(prof)
        for person_file in info["people"]:
            path = PEOPLE / person_file
            ok = insert_firmenprofil(path, md)
            print(f"   {'✓' if ok else '✗'} → {person_file}")
    PROFILES_OUT.write_text(json.dumps(all_profiles, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    print(f"\n✓ Profile gespeichert: {PROFILES_OUT.name}")


if __name__ == "__main__":
    main()
