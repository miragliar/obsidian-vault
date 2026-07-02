#!/usr/bin/env python3
"""
journal_audit.py — READ-ONLY Kontrolle der Journal-Einträge (cr55b_journal) für den
laufenden (oder gewählten) Monat, vor der Rechnungsstellung. Prüft zwei Geschäftsregeln:

  REGEL A — Kunden in Deutschland: KEINE Mehrwertsteuer.
      Firmen: Heike Hunnenberg GmbH, Fuchs & Söhne Service GmbH.
      Verstoss: cr55b_mwstpflichtig == Ja  ODER  cr55b_mwstbetrag > 0.

  REGEL B — Leistungspaket ist auf dem Journaleintrag PFLICHT.
      Firmen: Upgreat AG, Green.ch AG, MVM Services AG.
      Verstoss: _new_leistungspaket_value ist leer (kein LP gesetzt).

Firmen werden über den EXAKTEN account.name → GUID aufgelöst (bewusst NICHT 'contains':
'Green' würde sonst auch 'Big Green Egg Head' treffen, 'MVM' würde 'MVM AG' und
'MVM Services AG' vermischen).

Nur GET (read-only). Bei Funden wird eine Alarm-Notiz '00_Inbox/⚠️ Journal-Audit.md'
geschrieben; ohne Funde wird eine evtl. alte Notiz entfernt (selbst-aufräumend).
Läuft im wöchentlichen Job (weekly_refresh.sh) und ist jederzeit manuell aufrufbar.

  ./.venv/bin/python journal_audit.py                 # laufender Monat
  ./.venv/bin/python journal_audit.py --month 2026-06 # bestimmter Monat
  ./.venv/bin/python journal_audit.py --no-inbox      # nur Konsole, kein 00_Inbox
  ./.venv/bin/python journal_audit.py --login         # einmalig interaktiv anmelden
"""
import argparse
import os
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = SCRIPT_DIR.parent.parent          # …/Obsidian Raoul (Vault-Root)
# Inbox-Ordner für die Alarm-Notiz. Raouls Vault hat kein '00_Inbox' (Giovannis Struktur),
# daher: Env-Override, sonst erster existierender Kandidat, sonst '_imports' (wird angelegt).
def _pick_inbox():
    override = os.environ.get("JOURNAL_AUDIT_INBOX")
    if override:
        return VAULT_ROOT / override
    for cand in ("00_Inbox", "_imports", "00.index"):
        if (VAULT_ROOT / cand).is_dir():
            return VAULT_ROOT / cand
    return VAULT_ROOT / "_imports"
INBOX = _pick_inbox()
ALERT_FILE = INBOX / "⚠️ Journal-Audit.md"

RESOURCE = os.environ.get("DATAVERSE_URL", "https://org62e5ae4f.crm4.dynamics.com")
API = f"{RESOURCE}/api/data/v9.2"
SCOPES = [f"{RESOURCE}/.default"]

# Exakte account.name (bewusst exakt — siehe Modul-Docstring).
NO_VAT_FIRMS = ["Heike Hunnenberg GmbH", "Fuchs & Söhne Service GmbH"]   # DE → keine MwSt
LP_REQUIRED_FIRMS = ["Upgreat AG", "Green.ch AG", "MVM Services AG"]      # Leistungspaket Pflicht


# ---------------------------------------------------------------- Auth (Keychain, silent)
def get_token(interactive=False):
    # gemeinsamer Token-Cache im macOS Keychain (siehe auth_common.py / dataverse_query.py)
    sys.path.insert(0, str(SCRIPT_DIR))
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES, allow_device_flow=interactive)


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": 'odata.include-annotations="*"',
    }


def api_get(token, path):
    url = path if path.startswith("http") else f"{API}/{path.lstrip('/')}"
    r = requests.get(url, headers=_headers(token), timeout=60)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code} GET {path}\n{r.text[:600]}")
    return r.json()


def esc(s):
    """OData-String-Literal: einfaches Anführungszeichen verdoppeln."""
    return s.replace("'", "''")


def build_path(entityset, params):
    """Query bauen; nur die WERTE URL-encoden (Schlüssel wie $filter bleiben lesbar).
    Wichtig: '&' in Namen (z. B. 'Fuchs & Söhne') muss als %26 codiert werden,
    sonst zerschneidet es die Query."""
    qs = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
    return f"{entityset}?{qs}"


# ---------------------------------------------------------------- Resolver
def resolve_firms(token, names):
    """Exakte account.name → {name: accountid}. Meldet fehlende/mehrdeutige Namen."""
    flt = " or ".join(f"name eq '{esc(n)}'" for n in names)
    path = build_path("accounts", [("$select", "accountid,name"), ("$filter", flt)])
    rows = api_get(token, path).get("value", [])
    by_name = {}
    for r in rows:
        by_name.setdefault(r["name"], []).append(r["accountid"])
    resolved, problems = {}, []
    for n in names:
        ids = by_name.get(n, [])
        if len(ids) == 1:
            resolved[n] = ids[0]
        elif len(ids) == 0:
            problems.append(f"'{n}': 0 Treffer (Name geändert? gelöscht?)")
        else:
            problems.append(f"'{n}': {len(ids)} Treffer (mehrdeutig)")
    return resolved, problems


def month_bounds(month):
    if month:
        y, m = (int(x) for x in month.split("-"))
    else:
        t = date.today()
        y, m = t.year, t.month
    start = date(y, m, 1)
    nxt = date(y + (1 if m == 12 else 0), 1 if m == 12 else m + 1, 1)
    return start.isoformat(), nxt.isoformat(), f"{y:04d}-{m:02d}"


def fetch_journals(token, firm_ids, start, end):
    """Aktive Journale der gegebenen Firmen im Datumsfenster [start, end). Folgt nextLink."""
    firm_filter = " or ".join(f"_cr55b_firma_value eq {fid}" for fid in firm_ids)
    flt = (f"({firm_filter}) and cr55b_journaldatum ge {start} "
           f"and cr55b_journaldatum lt {end} and statecode eq 0")
    select = ("cr55b_journalid,cr55b_journalname,cr55b_journaldatum,cr55b_stunden,"
              "cr55b_mwstpflichtig,cr55b_mwstbetrag,cr55b_beschreibung,cr55b_verrechnet,"
              "_cr55b_firma_value,_new_leistungspaket_value")
    path = build_path("cr55b_journals", [
        ("$select", select),
        ("$filter", flt),
        ("$orderby", "cr55b_journaldatum asc"),
    ])
    rows = []
    while path:
        data = api_get(token, path)
        rows.extend(data.get("value", []))
        path = data.get("@odata.nextLink")
    return rows


# ---------------------------------------------------------------- Evaluate
def short_desc(row, n=70):
    txt = (row.get("cr55b_beschreibung") or "").strip().replace("\n", " ")
    return (txt[:n] + "…") if len(txt) > n else txt


def evaluate(rows, no_vat_ids, lp_ids, id2name):
    vat_hits, lp_hits = [], []
    for r in rows:
        fid = r.get("_cr55b_firma_value")
        rec = {
            "tag": r.get("cr55b_journaldatum"),
            "kunde": id2name.get(fid, r.get("_cr55b_firma_value@OData.Community.Display.V1.FormattedValue", "?")),
            "jnr": r.get("cr55b_journalname") or "(neu)",
            "stunden": r.get("cr55b_stunden"),
            "verrechnet": bool(r.get("cr55b_verrechnet")),
            "desc": short_desc(r),
        }
        if fid in no_vat_ids:
            mwst = r.get("cr55b_mwstbetrag") or 0
            if r.get("cr55b_mwstpflichtig") or mwst > 0:
                fv = r.get("cr55b_mwstbetrag@OData.Community.Display.V1.FormattedValue")
                vat_hits.append({**rec, "mwst": fv or mwst})
        if fid in lp_ids and not r.get("_new_leistungspaket_value"):
            lp_hits.append(rec)
    vat_hits.sort(key=lambda x: (x["tag"], x["kunde"]))
    lp_hits.sort(key=lambda x: (x["tag"], x["kunde"]))
    return vat_hits, lp_hits


# ---------------------------------------------------------------- Output
def render_markdown(month_label, vat_hits, lp_hits, problems):
    today = date.today().isoformat()
    n = len(vat_hits) + len(lp_hits)
    L = [
        "---", "type: alert", f"created: {today}", "tags: [journal, accounting, audit]",
        f"month: {month_label}", "status: to-check", "---",
        f"# ⚠️ Journal-Audit {month_label} — {n} Punkt(e) zu prüfen",
        "",
        "> READ-ONLY Kontrolle vor der Rechnungsstellung. Bitte **manuell** in der "
        "Accounting-App korrigieren (dieses Skript ändert nichts).",
        "",
    ]
    L += [f"## 🇩🇪 Deutschland-Kunden mit MwSt — sollte 0 sein ({len(vat_hits)})"]
    if vat_hits:
        L += ["", "| Tag | Kunde | J-Nr | MwSt | Std | verrechnet | Beschreibung |",
              "|---|---|---|---|---|---|---|"]
        L += [f"| {h['tag']} | {h['kunde']} | {h['jnr']} | {h['mwst']} | {h['stunden']} "
              f"| {'✅' if h['verrechnet'] else '—'} | {h['desc']} |" for h in vat_hits]
    else:
        L += ["", "_keine_"]
    L += ["", f"## 📦 Fehlendes Leistungspaket — Pflicht ({len(lp_hits)})"]
    if lp_hits:
        L += ["", "| Tag | Kunde | J-Nr | Std | verrechnet | Beschreibung |",
              "|---|---|---|---|---|---|"]
        L += [f"| {h['tag']} | {h['kunde']} | {h['jnr']} | {h['stunden']} "
              f"| {'✅' if h['verrechnet'] else '—'} | {h['desc']} |" for h in lp_hits]
    else:
        L += ["", "_keine_"]
    if problems:
        L += ["", "## ⚙️ Hinweise zur Firmenauflösung"]
        L += [f"- {p}" for p in problems]
    L += ["", "---", f"_Geprüft: {today} · Regel A (keine MwSt): {', '.join(NO_VAT_FIRMS)} · "
          f"Regel B (LP Pflicht): {', '.join(LP_REQUIRED_FIRMS)}._"]
    return "\n".join(L) + "\n"


def main():
    p = argparse.ArgumentParser(description="Read-only Journal-Audit (MwSt-DE + Leistungspaket-Pflicht).")
    p.add_argument("--month", help="YYYY-MM (Default: laufender Monat)")
    p.add_argument("--no-inbox", action="store_true", help="nicht nach 00_Inbox schreiben (nur Konsole)")
    p.add_argument("--login", action="store_true", help="interaktiver Device-Code-Login erzwingen")
    args = p.parse_args()

    token = get_token(interactive=args.login)
    start, end, label = month_bounds(args.month)

    resolved, problems = resolve_firms(token, NO_VAT_FIRMS + LP_REQUIRED_FIRMS)
    no_vat_ids = {resolved[n] for n in NO_VAT_FIRMS if n in resolved}
    lp_ids = {resolved[n] for n in LP_REQUIRED_FIRMS if n in resolved}
    id2name = {v: k for k, v in resolved.items()}

    print(f"# Journal-Audit {label}  ({start} … {end}, exklusiv)", file=sys.stderr)
    for n in NO_VAT_FIRMS + LP_REQUIRED_FIRMS:
        print(f"  {'✓' if n in resolved else '✗'} {n}"
              f"{'  ['+resolved[n]+']' if n in resolved else '  NICHT AUFGELÖST'}", file=sys.stderr)

    all_ids = list(no_vat_ids | lp_ids)
    rows = fetch_journals(token, all_ids, start, end) if all_ids else []
    vat_hits, lp_hits = evaluate(rows, no_vat_ids, lp_ids, id2name)

    print(f"\n{len(rows)} Journaleintrag/-einträge geprüft.")
    print(f"  🇩🇪 MwSt bei DE-Kunden (sollte 0): {len(vat_hits)} Verstoss/Verstösse")
    for h in vat_hits:
        print(f"    • {h['tag']}  {h['kunde']}  {h['jnr']}  MwSt={h['mwst']}  ({h['stunden']}h"
              f"{', verrechnet' if h['verrechnet'] else ''})")
    print(f"  📦 fehlendes Leistungspaket (Pflicht): {len(lp_hits)} Verstoss/Verstösse")
    for h in lp_hits:
        print(f"    • {h['tag']}  {h['kunde']}  {h['jnr']}  ({h['stunden']}h"
              f"{', verrechnet' if h['verrechnet'] else ''})")
    if problems:
        print("  ⚙️ Firmenauflösung:")
        for pr in problems:
            print(f"    ! {pr}")

    if not args.no_inbox:
        INBOX.mkdir(parents=True, exist_ok=True)
        if vat_hits or lp_hits:
            ALERT_FILE.write_text(render_markdown(label, vat_hits, lp_hits, problems), encoding="utf-8")
            print(f"\n⚠️  Alarm-Notiz geschrieben: {ALERT_FILE.relative_to(VAULT_ROOT)}")
        elif ALERT_FILE.exists():
            ALERT_FILE.unlink()
            print(f"\n✓ Keine Funde — alte Alarm-Notiz entfernt: {ALERT_FILE.relative_to(VAULT_ROOT)}")
        else:
            print("\n✓ Keine Funde.")


if __name__ == "__main__":
    main()
