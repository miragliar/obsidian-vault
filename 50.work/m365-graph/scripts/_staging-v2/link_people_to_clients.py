#!/usr/bin/env python3
"""
link_people_to_clients.py
-------------------------
Matcht das `company:`-Feld der Personen-Notizen (25_People/) gegen die
Client-Notizen (20_Clients/) und ergänzt bei sicheren Treffern ein
`client: "[[Clientnote]]"`-Feld im Frontmatter der Personen-Notiz.

Standard = Trockenlauf (zeigt nur Vorschläge). Mit --apply wird geschrieben.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE = ROOT / "25_People"
CLIENTS = ROOT / "20_Clients"

LEGAL = {"ag", "sa", "gmbh", "ltd", "llc", "inc", "holding", "group",
         "schweiz", "switzerland", "international", "services"}

# Feste Zuordnungen (normalisierter Firmenname -> Client-Notiz).
# Für Fälle, die das Token-Matching nicht erkennt – z.B. Brands einer Gruppe.
ALIASES = {
    "direct handling": "SHARKGROUP",   # Brand der SharkGroup
    "enia flooring": "SHARKGROUP",     #   "
    "enia": "SHARKGROUP",              #   "
    "profloor": "SHARKGROUP",          #   "
    "shg": "SHARKGROUP",               #   "
    "bertschi baeckerei zum brotkorb": "Bertschi",  # Logistik-Kunde = die Bäckerei
    "domba": "Bader",                  # DOMBA = Bader Immobilien
    "bader immobilien": "Bader",       #   "
    "bader immobilien domba": "Bader", #   "
    "thoma": "Thoma_Group",            # Thoma Group / TPS / La Goccia
    "thoma group": "Thoma_Group",      #   "
    "tps servizi": "Thoma_Group",      #   "
    "tps": "Thoma_Group",              #   "
    "team personnel solutions": "Thoma_Group",  # "
    "goccia": "Thoma_Group",           #   "
    "secusuisse": "SecuSuisse",
    "lachat": "Lachat",
    "robotec": "Robotec",
    "robotec systembaustoffe": "Robotec",
    "anifit": "ANiFit",
    "sme technik": "SME_Technik",
    "smetechnik": "SME_Technik",
    "ennio ferrari": "Ennio_Ferrari",
    "ennio ferrari holding": "Ennio_Ferrari",
    "nahrin": "Nahrin",
    "4b": "4B_AG",
    "ewo": "EWO",
    "elektrizitaetswerk obwalden": "EWO",
    "bwt": "BWT",
    "martello": "Martello_Manutenzione",
    "martello manutenzione": "Martello_Manutenzione",
    "invias": "Invias",
    "hiltl": "Hiltl",
}


def normalize(s):
    s = s.lower()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[._/&,]", " ", s)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    tokens = [t for t in s.split() if len(t) >= 2 and t not in LEGAL]
    return tokens


def client_cores():
    cores = {}
    for f in sorted(CLIENTS.glob("*.md")):
        name = f.stem
        # Projekt-/Themen-Notizen (mehrteilige technische Namen) als schwächer markieren
        toks = normalize(name.replace("_", " "))
        if toks:
            cores[name] = toks
    return cores


def read_company(note):
    for line in note.read_text(encoding="utf-8").splitlines():
        if line.startswith("company:"):
            return line[len("company:"):].strip().strip('"')
        if line.strip() == "---" and line is not note:
            pass
    return None


def match(company_toks, cores):
    """Gibt (clientname, confidence) zurück. confidence: high | low | None."""
    best = None
    for cname, ctoks in cores.items():
        cset, pset = set(ctoks), set(company_toks)
        if not cset:
            continue
        # exakte Übereinstimmung der Kerntokens
        if cset == pset:
            return cname, "high"
        # Client-Kern vollständig in Firmenname enthalten
        if cset <= pset:
            if len(cset) >= 2:
                conf = "high"                       # mehrere Kerntokens decken sich
            elif len(ctoks[0]) >= 4 and len(pset) <= 2:
                conf = "high"                       # 1 markantes Wort + max. 1 Zusatz (z.B. "Upgreat AG")
            else:
                conf = "low"                        # Einzelwort, aber viele Zusätze -> unsicher
            if best is None or conf == "high":
                best = (cname, conf)
    return best if best else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Treffer wirklich in Notizen schreiben")
    ap.add_argument("--include-low", action="store_true", help="auch unsichere (low) Treffer anwenden")
    args = ap.parse_args()

    cores = client_cores()
    high, low, none = [], [], []

    for note in sorted(PEOPLE.glob("*.md")):
        company = read_company(note)
        if not company:
            continue
        toks = normalize(company)
        if not toks:
            continue
        alias = ALIASES.get(" ".join(toks))
        if alias:
            cname, conf = alias, "high"
        else:
            cname, conf = match(toks, cores)
        entry = (note.name, company, cname)
        if conf == "high":
            high.append(entry)
        elif conf == "low":
            low.append(entry)

    def show(title, rows):
        print(f"\n### {title} ({len(rows)}) ###")
        for fn, comp, cn in rows:
            print(f"  {comp:42s} → [[{cn}]]   ({fn})")

    show("SICHER (high)", high)
    show("UNSICHER – bitte prüfen (low)", low)

    if not args.apply:
        print("\n(Trockenlauf — nichts geschrieben. Mit --apply anwenden, --include-low für die unsicheren.)")
        return

    targets = high + (low if args.include_low else [])
    written = 0
    for fn, comp, cn in targets:
        p = PEOPLE / fn
        text = p.read_text(encoding="utf-8")
        if re.search(r"^client:", text, re.M):
            continue  # schon verlinkt
        # client-Feld nach der company-Zeile einfügen
        new = re.sub(r"(^company:.*$)", rf'\1\nclient: "[[{cn}]]"', text, count=1, flags=re.M)
        if new != text:
            p.write_text(new, encoding="utf-8")
            written += 1
    print(f"\n✓ {written} Personen-Notizen mit client-Link ergänzt"
          f"{' (inkl. unsicherer)' if args.include_low else ''}.")


if __name__ == "__main__":
    main()
