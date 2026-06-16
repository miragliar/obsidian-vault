#!/usr/bin/env python3
"""
journal_create.py — Referenz-Implementierung: Journal-Eintrag (cr55b_journal) in der
Castelli "DebitorenRechnungen"/AccountingApp via Dataverse Web API anlegen.

⚠️  DRY-RUN als Default (schreibt NICHTS). Erst mit --commit wird angelegt (mit Bestätigung).

MINIMALER INPUT:  --firma  --kontakt  --beschreibung  --stunden   (+ --leistungspaket, falls die Firma welche hat)
DEFAULTS (bestätigt):  homeoffice=Ja · mwstpflichtig=Ja · inrechnunganzeigen=Ja · kostenlos=Nein · verrechnet=Nein · verrechnungvorziehen=Nein
SERVERSEITIG BERECHNET (NICHT senden):  Stundensatz, BetragOhneMWST/MWST/InklMWST, J-Nummer, MwSt-Satz.
WÄHRUNG:  wird aus der Firma (account) übernommen (spiegelt das Form-JS) — sonst CHF.

Lookups werden per Name → GUID aufgelöst:
  • Firma   = account.name (exakt)
  • Kontakt = contact.fullname, EINGESCHRÄNKT auf die Firma (parentcustomerid)
  • Leistungspaket = new_leistungspaket.new_id (LP-####) oder Teil der new_bezeichnung, je Firma, aktiv
Regel: 0 oder >1 Treffer  →  ABBRUCH mit Kandidatenliste  (nachfragen statt raten).
Regel: Firma hat aktive Leistungspakete, aber keines angegeben  →  ABBRUCH (Auswahl Pflicht).

ZIEL-UMGEBUNG / AUTH:
  --org URL                 Dataverse-Env (Default: $DATAVERSE_URL oder Prod-Org)
  M365_CLIENT_ID / M365_TENANT_ID   (Env) — App-Registrierung (delegiert, Dynamics user_impersonation)
  Auth nutzt – falls vorhanden – das gemeinsame auth_common (macOS Keychain, silent);
  sonst portabler MSAL Device-Code-Flow (Cache unter ~/.config/journal-create, ausserhalb Dropbox).

BEISPIELE:
  ./.venv/bin/python journal_create.py \
      --firma "Green.ch AG" --kontakt "Solange Silva" --leistungspaket "LP-1001" \
      --stunden 0.5 --beschreibung "Gateway-Migration ..."            # DRY-RUN
  ... --commit            # tatsächlich anlegen (fragt nach; --yes zum Überspringen)
  ... --org "https://<test>.crm4.dynamics.com" --login              # andere Env, neu anmelden
"""
import argparse
import json
import os
import sys
from datetime import date

import requests

DEFAULT_ORG = os.environ.get("DATAVERSE_URL", "https://org62e5ae4f.crm4.dynamics.com")
ENTITYSET = "cr55b_journals"


# ---------------------------------------------------------------- Auth
def get_token(org, force_login=False):
    scopes = [f"{org}/.default"]
    # 1) Gemeinsames auth_common (Keychain, silent) — bevorzugt in Giovannis Umgebung
    if not force_login:
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from auth_common import get_token as _gt
            return _gt(scopes, allow_device_flow=True)
        except SystemExit:
            raise
        except Exception:
            pass
    # 2) Portabler Device-Code-Flow (jedes OS), Cache ausserhalb synchronisierter Ordner
    import msal
    client_id = os.environ.get("M365_CLIENT_ID", "0c8e309d-d02e-4244-ae2a-dbb5551cb550")
    tenant_id = os.environ.get("M365_TENANT_ID", "ae7f72de-197d-4ba0-a852-40ee367a5150")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    cache_dir = os.environ.get("JOURNAL_CACHE_DIR",
                               os.path.join(os.path.expanduser("~"), ".config", "journal-create"))
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "token_cache.json")
    cache = msal.SerializableTokenCache()
    if os.path.exists(cache_file):
        cache.deserialize(open(cache_file, encoding="utf-8").read())
    app = msal.PublicClientApplication(client_id, authority=authority, token_cache=cache)
    result = None
    if not force_login:
        for acc in app.get_accounts():
            result = app.acquire_token_silent(scopes, account=acc)
            if result:
                break
    if not result:
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60 + f"\n{flow['message']}\n" + "=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        open(cache_file, "w", encoding="utf-8").write(cache.serialize())
    if not result or "access_token" not in result:
        sys.exit(f"Token-Erwerb fehlgeschlagen: {result}")
    return result["access_token"]


# ---------------------------------------------------------------- Dataverse client
class DV:
    def __init__(self, org, token):
        self.api = f"{org}/api/data/v9.2"
        self.h = {"Authorization": f"Bearer {token}", "Accept": "application/json",
                  "OData-MaxVersion": "4.0", "OData-Version": "4.0",
                  "Prefer": 'odata.include-annotations="*"'}

    def get(self, path):
        url = path if path.startswith("http") else f"{self.api}/{path.lstrip('/')}"
        r = requests.get(url, headers=self.h, timeout=60)
        if not r.ok:
            sys.exit(f"HTTP {r.status_code} GET {path}\n{r.text[:600]}")
        return r.json()

    def create(self, entityset, payload):
        h = dict(self.h)
        h["Content-Type"] = "application/json"
        h["Prefer"] = 'return=representation,odata.include-annotations="*"'
        r = requests.post(f"{self.api}/{entityset}", headers=h,
                          data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=60)
        if not r.ok:
            sys.exit(f"HTTP {r.status_code} POST {entityset}\n{r.text[:800]}")
        return r.json()


def esc(s):
    return s.replace("'", "''")


# ---------------------------------------------------------------- Resolver (nachfragen statt raten)
def resolve_firma(dv, name):
    rows = dv.get(f"accounts?$select=accountid,name,_transactioncurrencyid_value"
                  f"&$filter=name eq '{esc(name)}'").get("value", [])
    if len(rows) != 1:
        c = "; ".join(r["name"] for r in rows) or "(keine)"
        sys.exit(f"❌ Firma '{name}': {len(rows)} Treffer → bitte eindeutig. Kandidaten: {c}")
    return rows[0]


def resolve_kontakt(dv, account_id, name):
    rows = dv.get(f"contacts?$select=contactid,fullname"
                  f"&$filter=_parentcustomerid_value eq {account_id} and fullname eq '{esc(name)}'").get("value", [])
    if len(rows) == 1:
        return rows[0]
    if len(rows) == 0:
        sys.exit(f"❌ Kontakt '{name}' @ Firma: 0 Treffer. Name prüfen oder Kontakt zuerst anlegen "
                 f"(Kontakt ist Pflicht — nicht raten).")
    sys.exit(f"❌ Kontakt '{name}': {len(rows)} Treffer → bitte eindeutig (Rückfrage).")


def resolve_leistungspaket(dv, account_id, token):
    base = (f"new_leistungspakets?$select=new_leistungspaketid,new_id,new_bezeichnung"
            f"&$filter=_new_firma_value eq {account_id} and statecode eq 0&$orderby=new_id asc")
    allp = dv.get(base).get("value", [])
    if not token:
        if allp:  # Geschäftsregel: hat die Firma Pakete, ist die Auswahl Pflicht
            opts = " | ".join(f"{p['new_id']} {p.get('new_bezeichnung')}" for p in allp)
            sys.exit(f"❌ Firma hat {len(allp)} Leistungspaket(e) → --leistungspaket ist PFLICHT. Optionen: {opts}")
        return None  # Firma ohne Pakete → ok
    hits = [p for p in allp if (p.get("new_id") or "").lower() == token.lower()]
    if not hits:
        hits = [p for p in allp if token.lower() in (p.get("new_bezeichnung") or "").lower()
                or token.lower() in (p.get("new_id") or "").lower()]
    if len(hits) == 1:
        return hits[0]
    opts = " | ".join(f"{p['new_id']} {p.get('new_bezeichnung')}" for p in (hits or allp))
    sys.exit(f"❌ Leistungspaket '{token}': {len(hits)} Treffer → bitte eindeutig. Optionen: {opts}")


def resolve_chf(dv):
    rows = dv.get("transactioncurrencies?$select=transactioncurrencyid,isocurrencycode"
                  "&$filter=isocurrencycode eq 'CHF'").get("value", [])
    return rows[0]["transactioncurrencyid"] if rows else None


# ---------------------------------------------------------------- main
def yn(default):
    return {"type": str, "choices": ["ja", "nein"], "default": default}


def is_ja(v):
    return str(v).strip().lower() in ("ja", "j", "true", "1", "yes", "y")


def main():
    p = argparse.ArgumentParser(description="Dataverse Journal-Eintrag anlegen (DRY-RUN per Default).")
    p.add_argument("--firma", required=True, help="Firmenname (account.name, exakt)")
    p.add_argument("--kontakt", required=True, help="Kontakt (contact.fullname, je Firma)")
    p.add_argument("--beschreibung", required=True, help="Leistungsbeschreibung")
    p.add_argument("--stunden", required=True, type=float, help="Stunden, z. B. 0.5")
    p.add_argument("--leistungspaket", help="LP-#### oder Teil der Bezeichnung (Pflicht, falls Firma Pakete hat)")
    p.add_argument("--datum", default=date.today().isoformat(), help="JournalDatum YYYY-MM-DD (Default: heute)")
    p.add_argument("--homeoffice", **yn("ja"))
    p.add_argument("--mwstpflichtig", **yn("ja"))
    p.add_argument("--inrechnung", **yn("ja"))
    p.add_argument("--kostenlos", **yn("nein"))
    p.add_argument("--fixpreis", type=float, help="optional: Fixpreis statt Std×Satz")
    p.add_argument("--org", default=DEFAULT_ORG, help=f"Dataverse-URL (Default: {DEFAULT_ORG})")
    p.add_argument("--commit", action="store_true", help="WIRKLICH anlegen (sonst Dry-Run)")
    p.add_argument("--yes", action="store_true", help="Bestätigung überspringen (für nicht-interaktive Läufe)")
    p.add_argument("--login", action="store_true", help="interaktiver Device-Code-Login erzwingen")
    args = p.parse_args()

    token = get_token(args.org, force_login=args.login)
    dv = DV(args.org, token)

    firma = resolve_firma(dv, args.firma)
    kontakt = resolve_kontakt(dv, firma["accountid"], args.kontakt)
    lp = resolve_leistungspaket(dv, firma["accountid"], args.leistungspaket)
    cur_id = firma.get("_transactioncurrencyid_value") or resolve_chf(dv)

    payload = {
        "cr55b_journaldatum": args.datum,
        "cr55b_stunden": args.stunden,
        "cr55b_beschreibung": args.beschreibung,
        "cr55b_homeoffice": is_ja(args.homeoffice),
        "cr55b_mwstpflichtig": is_ja(args.mwstpflichtig),
        "cr55b_inrechnunganzeigen": is_ja(args.inrechnung),
        "cr55b_kostenlos": is_ja(args.kostenlos),
        "cr55b_verrechnet": False,
        "new_verrechnungvorziehen": False,
        "cr55b_Firma@odata.bind": f"/accounts({firma['accountid']})",
        "cr55b_Kontakt@odata.bind": f"/contacts({kontakt['contactid']})",
    }
    if cur_id:
        payload["transactioncurrencyid@odata.bind"] = f"/transactioncurrencies({cur_id})"
    if lp:
        payload["new_Leistungspaket@odata.bind"] = f"/new_leistungspakets({lp['new_leistungspaketid']})"
    if args.fixpreis is not None:
        payload["new_fixpreis"] = args.fixpreis

    print("── Aufgelöst ─────────────────────────────────────────────")
    print(f"  Firma         : {firma['name']}  ({firma['accountid']})")
    print(f"  Kontakt       : {kontakt['fullname']}  ({kontakt['contactid']})")
    print(f"  Leistungspaket: {(lp['new_id']+' '+(lp.get('new_bezeichnung') or '')) if lp else '— (Firma ohne Pakete)'}")
    print(f"  Datum/Stunden : {args.datum} / {args.stunden}  · HomeOffice={is_ja(args.homeoffice)}")
    print(f"  Org           : {args.org}")
    print("── Payload (POST {API}/" + ENTITYSET + ") ─────────────────")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if not args.commit:
        print("\n💡 DRY-RUN — es wurde NICHTS angelegt. Mit --commit tatsächlich erstellen.")
        return

    if not args.yes:
        if not sys.stdin or not sys.stdin.isatty():
            sys.exit("⛔ --commit ohne TTY: bitte --yes setzen, um nicht-interaktiv zu bestätigen.")
        if input("\n⚠️  Wirklich in Dataverse anlegen? [j/N] ").strip().lower() not in ("j", "ja", "y", "yes"):
            sys.exit("Abgebrochen.")

    rec = dv.create(ENTITYSET, payload)
    fv = lambda k: rec.get(k + "@OData.Community.Display.V1.FormattedValue") or rec.get(k)
    print("\n✅ ANGELEGT:")
    print(f"  {fv('cr55b_journalname')} · {fv('cr55b_journaldatum')} · {firma['name']}")
    print(f"  Stundensatz={fv('cr55b_stundensatz')} · OhneMWST={fv('cr55b_betragohnemwst')} "
          f"· MWST={fv('cr55b_mwstbetrag')} · InklMWST={fv('cr55b_betraginklmwst')}")
    print(f"  journalid={rec.get('cr55b_journalid')}")
    print("  ↪ Hinweis: Create triggert automatisch den Fabric-Sync-Flow.")


if __name__ == "__main__":
    main()
