#!/usr/bin/env python3
"""
extend_and_rebuild.py
---------------------
Erweitert FIRMS/CONTACTS in den drei Generator-Skripten um die neu gefundenen
regelmässigen Kontakte und Firmen, und führt sie der Reihe nach aus:
  1. enrich_companies.py  → company_profiles.json mit allen 12 Firmen
  2. build_people_notes.py → 25_People/ mit allen 18 Personen
  3. build_firmen_notes.py → 26_Firmen/ mit allen 12 Firmen
"""
import re
import subprocess
from pathlib import Path

VAULT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul")
IMP = VAULT / "_imports"

# ---- NEUE FIRMEN (3) ----
NEW_FIRMS_ENRICH = '''    "Hauswäckerling": {"url": "https://www.hauswaeckerling.ch",
                       "people": ["Andreas-Funke.md"]},
    "DOBI-Inter AG": {"url": "https://www.dobi.ch",
                      "people": ["Nenad-Stojanovic.md", "Saveen-Manocha.md"]},
    "Hunnenberg": {"url": "https://www.hunnenberg.de",
                   "people": ["TH-Hunnenberg.md"]},
'''

# ---- NEUE FIRMEN in build_firmen_notes ----
NEW_FIRMS_BUILD = '''    "Hauswäckerling": {
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
'''

# ---- NEUE PERSONEN in build_people_notes (8 neue) ----
NEW_CONTACTS = '''    # Erweiterungen 01.06.2026 — nach Recherche regelmässiger Kontakte (last 18 Monate)
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
'''

# Zusätzlich Personen-Erweiterungen für die existierenden Firmen
# (in build_firmen_notes.py die "people"-Listen erweitern)
OBRIST_PEOPLE_NEW = '''        "people": [
            ("Barbara Gilli", "b.gilli@obrist-interior.ch", "Projekt-Kontakt"),
            ("Tobias Lamprecht", "t.lamprecht@obrist-interior.ch", "Projekt-Kontakt (Zeugnis-App)"),
            ("Bianca Tschuppert", "b.tschuppert@obrist-interior.ch", "Projekt-Kontakt (Zeugnis-App)"),
        ],'''
OBRIST_PEOPLE_OLD = '''        "people": [("Barbara Gilli", "b.gilli@obrist-interior.ch", "Projekt-Kontakt")],'''

KOSTER_PEOPLE_NEW = '''        "people": [
            ("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt"),
            ("Monika Kuhn", "m.kuhn@kosterag.ch", "Projekt-Kontakt (App-Wartung)"),
        ],'''
KOSTER_PEOPLE_OLD = '''        "people": [("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt")],'''

MVM_PEOPLE_NEW = '''        "people": [
            ("Remo Pfister", "r.pfister@mvm-ag.ch", "Power Platform Ansprechperson"),
            ("M. Schärli", "m.schaerli@mvm-ag.ch", "Mail-Kontakt"),
        ],'''
MVM_PEOPLE_OLD = '''        "people": [("Remo Pfister", "r.pfister@mvm-ag.ch", "Power Platform Ansprechperson")],'''


def patch_file(path, replacements):
    """Liste von (old, new) tuples — jeweils im Text ersetzen."""
    txt = path.read_text(encoding="utf-8")
    for old, new in replacements:
        if old in txt:
            txt = txt.replace(old, new)
        else:
            print(f"   ⚠ Pattern nicht gefunden in {path.name}: {old[:60]!r}…")
    path.write_text(txt, encoding="utf-8")


def patch_enrich_companies():
    f = IMP / "enrich_companies.py"
    OLD = '''    "Koster AG": {"url": "https://www.kosterag.ch",
                  "people": ["H.-Baumann.md"]},
}'''
    NEW = '''    "Koster AG": {"url": "https://www.kosterag.ch",
                  "people": ["H.-Baumann.md", "Monika-Kuhn.md"]},
''' + NEW_FIRMS_ENRICH + "}"

    # auch existierende person-listen erweitern
    patches = [
        ('"people": ["Barbara-Gilli.md"]',
         '"people": ["Barbara-Gilli.md", "Tobias-Lamprecht.md", "Bianca-Tschuppert.md"]'),
        ('"people": ["Remo-Pfister.md"]',
         '"people": ["Remo-Pfister.md", "M.-Schärli.md"]'),
        (OLD, NEW),
    ]
    patch_file(f, patches)
    print(f"  ✓ Patched: {f.name}")


def patch_build_people():
    f = IMP / "build_people_notes.py"
    # Vor dem schliessenden "]" der CONTACTS-Liste die neuen anhängen
    txt = f.read_text(encoding="utf-8")
    marker = '''    {"name": "H. Baumann", "email": "h.baumann@kosterag.ch",
     "firma": "Koster AG", "typ": "kunde",
     "rolle": "Projekt-Kontakt", "tags": ["miraglia", "kunde", "koster-ag"]},
]'''
    if marker not in txt:
        print(f"  ⚠ Marker nicht gefunden in {f.name} — versuche generic")
        return
    new = marker.rstrip("]") + NEW_CONTACTS + "]"
    txt = txt.replace(marker, new)
    f.write_text(txt, encoding="utf-8")
    print(f"  ✓ Patched: {f.name}")


def patch_build_firmen():
    f = IMP / "build_firmen_notes.py"
    txt = f.read_text(encoding="utf-8")
    patches = [
        (OBRIST_PEOPLE_OLD, OBRIST_PEOPLE_NEW),
        (KOSTER_PEOPLE_OLD, KOSTER_PEOPLE_NEW),
        (MVM_PEOPLE_OLD, MVM_PEOPLE_NEW),
    ]
    for old, new in patches:
        if old in txt:
            txt = txt.replace(old, new)
        else:
            print(f"   ⚠ Pattern nicht gefunden: {old[:60]!r}…")
    # Neue Firmen vor schliessender Klammer einfügen
    marker = '''    "Koster AG": {
        "slug": "Koster-AG",
        "domain": "kosterag.ch",
        "people": [("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt")],
        "typ": "kunde",
        "branche": "Haustechnik (Heizung, Lüftung, Klima, Elektro, Sanitär)",
        "tags": ["miraglia", "kunde", "koster-ag"],
    },
}'''
    if marker in txt:
        # Ersetze koster-people zuerst, dann Block-Ende mit neuen Firmen erweitern
        new_marker = marker.replace(
            '"people": [("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt")],',
            '''"people": [
            ("H. Baumann", "h.baumann@kosterag.ch", "Projekt-Kontakt"),
            ("Monika Kuhn", "m.kuhn@kosterag.ch", "Projekt-Kontakt (App-Wartung)"),
        ],'''
        )
        new_marker = new_marker.rstrip("}").rstrip() + "\n" + NEW_FIRMS_BUILD + "}"
        txt = txt.replace(marker, new_marker)
    else:
        # Falls Koster-Block schon abgewandelt — alternativer Marker
        # NEW firms am Ende der FIRMS dict einfügen
        last_close = txt.rfind('}\n\n\ndef')
        if last_close == -1:
            last_close = txt.rfind('}\n\n\n')
        if last_close > 0:
            # Find the FIRMS dict's closing }
            firms_end = txt.index('\n}\n', txt.index('FIRMS = {'))
            insert_at = firms_end
            txt = txt[:insert_at] + "\n" + NEW_FIRMS_BUILD.rstrip() + txt[insert_at:]
    f.write_text(txt, encoding="utf-8")
    print(f"  ✓ Patched: {f.name}")


def run(script):
    """Run a script in the vault root."""
    print(f"\n▶ Running {script}")
    result = subprocess.run(["python3", str(IMP / script)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"   ✗ FAILED:\n{result.stderr}")
        return False
    # Show last 20 lines of stdout
    for line in result.stdout.splitlines()[-25:]:
        print(f"   {line}")
    return True


def main():
    print("=== Patching Generator-Scripts ===")
    patch_enrich_companies()
    patch_build_people()
    patch_build_firmen()

    print("\n=== Re-running Pipeline ===")
    # 1. Company-Profile neu holen (für 3 neue Firmen)
    if not run("enrich_companies.py"):
        print("Abbruch: enrich_companies fehlgeschlagen")
        return
    # 2. Personen-Notizen neu (alle 18)
    if not run("build_people_notes.py"):
        print("Abbruch: build_people_notes fehlgeschlagen")
        return
    # 3. Firmen-Notizen neu (alle 12)
    if not run("build_firmen_notes.py"):
        print("Abbruch: build_firmen_notes fehlgeschlagen")
        return

    print("\n=== Fertig ===")


if __name__ == "__main__":
    main()
