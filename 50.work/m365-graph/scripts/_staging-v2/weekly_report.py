#!/usr/bin/env python3
"""
weekly_report.py
----------------
Erstellt nach dem deterministischen Refresh einen „Was ist neu / zu prüfen"-Report
in 00_Inbox/ — die Punkte, die KI-Urteil brauchen (Research/Charakterisierung).
Schreibt KEINE Personen/Kunden, nur den Report. Kein Graph-Zugriff nötig.
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PEOPLE = ROOT / "25_People"
CLIENTS = ROOT / "20_Clients"
INBOX = ROOT / "00_Inbox"
SCRIPT_DIR = Path(__file__).resolve().parent
THRESH = 20  # ab so vielen Interaktionen relevant
LEGAL = {"ag", "sa", "gmbh", "ltd", "holding", "group", "sagl", "co"}


def norm(s):
    s = (s or "").lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = re.sub(r"[._/&,]", " ", s)
    return {t for t in re.sub(r"[^a-z0-9 ]", "", s).split() if len(t) >= 2 and t not in LEGAL}


def fm(text, key):
    m = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else None


def main():
    client_tokens = [norm(f.stem) for f in CLIENTS.glob("*.md")]
    clients_wo_profil = [f.stem for f in CLIENTS.glob("*.md")
                         if "## Unternehmensprofil" not in f.read_text(encoding="utf-8")
                         and fm(f.read_text(encoding="utf-8"), "type") == "client"]

    unlinked, no_char = [], []
    firms = {}
    for n in PEOPLE.glob("*.md"):
        t = n.read_text(encoding="utf-8")
        try:
            inter = int(fm(t, "interaktionen") or 0)
        except ValueError:
            inter = 0
        if inter < THRESH:
            continue
        client = fm(t, "client")
        company = fm(t, "company") or ""
        has_char = ("<!-- mail-summary -->" in t) or ("<!-- teams-summary -->" in t)
        if not client:
            unlinked.append((inter, n.stem, company))
            ct = norm(company)
            if ct and not any(ct & tok for tok in client_tokens):
                firms.setdefault(company, [0, 0])
                firms[company][0] += 1
                firms[company][1] += inter
        if not has_char:
            no_char.append((inter, n.stem, company))

    unlinked.sort(reverse=True); no_char.sort(reverse=True)
    firms_sorted = sorted(firms.items(), key=lambda x: x[1][1], reverse=True)
    today = date.today().isoformat()

    L = [f"---\ntype: report\ncreated: {today}\ntags: [report, m365-sync]\n---",
         f"# 🔄 M365 Wochen-Report ({today})",
         "",
         "> Der deterministische Refresh (neue Kontakte, Verknüpfung, Stakeholder, Stats) lief automatisch. "
         "Unten die Punkte, die **KI-Urteil** brauchen — am besten mit **Claudian** abarbeiten (Auftrag s. unten).",
         ""]

    L += [f"## 🆕 Neue Firmen-Kandidaten ({len(firms_sorted)}) — evtl. Client anlegen + Research",
          "_Firmen aus Personen ohne passende Kundenakte (Web + Zefix/Handelsregister recherchieren):_"]
    L += [f"- **{c}** — {n} Person(en), {i} Interaktionen" for c, (n, i) in firms_sorted[:25]] or ["- _keine_"]

    L += ["", f"## 🔗 Personen ohne Kunden-Link ({len(unlinked)}) — verknüpfen oder Privat/Dienstleister markieren"]
    L += [f"- [[{nm}]] — {co or '—'} ({i})" for i, nm, co in unlinked[:30]] or ["- _keine_"]

    L += ["", f"## 📝 Personen ohne Charakterisierung ({len(no_char)}) — 📧/💬 Kontext ergänzen"]
    L += [f"- [[{nm}]] — {co or '—'} ({i})" for i, nm, co in no_char[:30]] or ["- _keine_"]

    L += ["", f"## 🏢 Kunden ohne Firmenprofil ({len(clients_wo_profil)})"]
    L += [f"- [[{c}]]" for c in clients_wo_profil] or ["- _keine_"]

    L += ["", "---", "## 🤖 Auftrag für Claudian (kopieren)",
          "> Arbeite den M365 Wochen-Report ab:",
          "> 1. Für die **neuen Firmen-Kandidaten**: recherchiere via Webseite (E-Mail-Domain) + **Zefix/Handelsregister** "
          "(Rechtsform, Gründung, UID, Sitz, Branche, Produkte), lege fehlende **Client-Notizen** an und schreibe das **Unternehmensprofil** "
          "(`apply_firmenprofile.py`). Erkenne Gruppen/Schwesterfirmen.",
          "> 2. **Personen ohne Kunden-Link**: verknüpfe sie (Firma→Kunde) bzw. markiere **Privat/Dienstleister**.",
          "> 3. **Personen ohne Charakterisierung**: lies `mail_digest.json` / `teams_digest.json` und ergänze 📧/💬-Kontext.",
          "> 4. Danach `fill_stakeholders.py --apply` neu laufen lassen.",
          "",
          f"_Daten-Snapshots: `40_Resources/scripts/mail_digest.json`, `teams_digest.json` (Stand {today})._"]

    INBOX.mkdir(parents=True, exist_ok=True)
    out = INBOX / "M365 Wochen-Report.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ Report: {out}  | Firmen-Kandidaten {len(firms_sorted)}, unverknüpft {len(unlinked)}, "
          f"ohne Charakterisierung {len(no_char)}, Clients ohne Profil {len(clients_wo_profil)}")


if __name__ == "__main__":
    main()
