#!/usr/bin/env python3
"""
apply_mail_summaries.py
-----------------------
Schreibt pro Person einen Abschnitt '## 📧 E-Mail-Kontext' in die Notiz (25_People/).
- Statistik (Anzahl Mails, letzter Kontakt) kommt aus mail_digest.json
- Prosa-Zusammenfassung kommt aus mail_summaries.json (von Hand/Claude verfasst)
Der Abschnitt steht in einem <!-- mail-summary -->-Block (idempotent; Re-Lauf aktualisiert).

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
DIGEST = SCRIPT_DIR / "mail_digest.json"
SUMM = SCRIPT_DIR / "mail_summaries.json"

START, END = "<!-- mail-summary -->", "<!-- /mail-summary -->"


def nfc(s):
    return unicodedata.normalize("NFC", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    digest = json.loads(DIGEST.read_text(encoding="utf-8"))
    stats = {nfc(p["file"]): p for p in digest["people"]}
    # Alle mail_summaries*.json zusammenführen (mail_summaries.json + _extra etc.)
    summaries = {}
    for f in sorted(SCRIPT_DIR.glob("mail_summaries*.json")):
        summaries.update(json.loads(f.read_text(encoding="utf-8")))
    gen_date = "2026-05-29"

    # Map NFC(dateiname) -> echter Pfad (macOS-Umlaut-sicher)
    notes = {nfc(p.name): p for p in PEOPLE.glob("*.md")}

    written = missing = 0
    for fname, prose in summaries.items():
        key = nfc(fname)
        path = notes.get(key)
        if not path:
            print(f"  ⚠ Notiz nicht gefunden: {fname}")
            missing += 1
            continue
        st = stats.get(key, {})
        statline = (f"*Stand: {gen_date} · {st.get('total','?')} Mails "
                    f"({st.get('recv','?')} erhalten / {st.get('sent','?')} gesendet) · "
                    f"letzter Kontakt {st.get('last','?')}*")
        block = f"{START}\n{statline}\n\n{prose}\n{END}"

        text = path.read_text(encoding="utf-8")
        if START in text and END in text:
            new = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
        else:
            new = text.rstrip() + f"\n\n## 📧 E-Mail-Kontext\n{block}\n"

        print(f"  ✓ {fname[:-3]}")
        if args.apply and new != text:
            path.write_text(new, encoding="utf-8")
            written += 1

    if args.apply:
        print(f"\n✓ {written} Notizen aktualisiert ({missing} nicht gefunden).")
    else:
        print(f"\n(Trockenlauf — {len(summaries)} Zusammenfassungen bereit, {missing} Notiz(en) fehlen. Mit --apply schreiben.)")


if __name__ == "__main__":
    main()
