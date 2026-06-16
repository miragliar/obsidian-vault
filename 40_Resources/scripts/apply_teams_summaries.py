#!/usr/bin/env python3
"""
apply_teams_summaries.py
------------------------
Schreibt pro Person einen Abschnitt '## 💬 Teams-Kontext' in die Notiz (25_People/).
- Statistik (1:1/Gruppe, letzter Kontakt) kommt aus teams_digest.json
- Prosa-Charakterisierung kommt aus teams_summaries*.json (von Hand/Claude verfasst)
Der Abschnitt steht in einem <!-- teams-summary -->-Block (idempotent; Re-Lauf aktualisiert).

Gegenstück zu apply_mail_summaries.py. teams_digest.json ist nach Name/E-Mail (nicht
nach Dateiname) indexiert; das Matching läuft daher über das `email:`-Feld der Notiz
bzw. den Dateinamen (NFC-normalisiert, macOS-Umlaut-sicher).

Standard = Trockenlauf. Mit --apply wird geschrieben.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent.parent
PEOPLE = ROOT / "25_People"
DIGEST = SCRIPT_DIR / "teams_digest.json"
GEN_DATE = "2026-06-13"

START, END = "<!-- teams-summary -->", "<!-- /teams-summary -->"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def fm_value(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    digest = json.loads(DIGEST.read_text(encoding="utf-8"))
    by_email = {(p.get("email") or "").lower(): p for p in digest["people"] if p.get("email")}
    by_name = {nfc(p["name"]): p for p in digest["people"]}

    summaries = {}
    for f in sorted(SCRIPT_DIR.glob("teams_summaries*.json")):
        summaries.update(json.loads(f.read_text(encoding="utf-8")))

    notes = {nfc(p.name): p for p in PEOPLE.glob("*.md")}

    written = missing = 0
    for fname, prose in summaries.items():
        path = notes.get(nfc(fname))
        if not path:
            print(f"  ⚠ Notiz nicht gefunden: {fname}")
            missing += 1
            continue
        text = path.read_text(encoding="utf-8")
        email = (fm_value(text, "email") or "").lower()
        st = by_email.get(email) or by_name.get(nfc(path.stem)) or {}
        statline = (f"*Stand: {GEN_DATE} · Teams {st.get('in_1to1','?')}×1:1 / "
                    f"{st.get('in_group','?')}×Gruppe · {st.get('msgs_from','?')} Nachrichten · "
                    f"letzter Kontakt {st.get('last','?')}*")
        block = f"{START}\n{statline}\n\n{prose}\n{END}"

        if START in text and END in text:
            new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
        else:
            new = text.rstrip() + f"\n\n## 💬 Teams-Kontext\n{block}\n"

        print(f"  ✓ {fname[:-3]}")
        if args.apply and new != text:
            path.write_text(new, encoding="utf-8")
            written += 1

    if args.apply:
        print(f"\n✓ {written} Notizen aktualisiert ({missing} nicht gefunden).")
    else:
        print(f"\n(Trockenlauf — {len(summaries)} Teams-Charakterisierungen bereit, {missing} Notiz(en) fehlen. Mit --apply schreiben.)")


if __name__ == "__main__":
    main()
