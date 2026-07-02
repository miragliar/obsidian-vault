#!/usr/bin/env python3
"""
journal_create.py — Referenz-Implementierung: Journal-Eintrag (cr55b_journal) in der
Castelli "DebitorenRechnungen"/AccountingApp via Dataverse Web API anlegen.

⚠️  DRY-RUN als Default (schreibt NICHTS). Erst mit --commit wird angelegt (mit Bestätigung).

MINIMALER INPUT:  --firma  --kontakt  --beschreibung  --stunden   (+ --leistungspaket, falls die Firma welche hat)
BESCHREIBUNG:  sachlich · deutsch · kurz (1–3 Sätze, was geleistet wurde; keine Floskeln).
DEFAULTS (bestätigt):  homeoffice=Ja · mwstpflichtig=Ja · inrechnunganzeigen=Ja · kostenlos=Nein · verrechnet=Nein · verrechnungvorziehen=Nein
SERVERSEITIG BERECHNET (NICHT senden):  Stundensatz, BetragOhneMWST/MWST/InklMWST, J-Nummer, MwSt-Satz.
WÄHRUNG:  wird aus der Firma (account) übernommen (spiegelt das Form-JS) — sonst CHF.
HOMEOFFICE:  schaltet den berechneten Satz (account.cr55b_stundensatz vs. account.cr55b_stundensatzremote).
             Vor-Ort-Tage = "--homeoffice nein", sonst rechnet die App still den Remote-Satz.
STUNDEN:  nur die VERRECHENBAREN Stunden. Gratis-Anteile gehören inline in die Beschreibung
          ("(2h Kostenlos)"), nicht als zweiter Eintrag und nicht über --kostenlos (= GANZER Eintrag gratis).

Lookups werden per Name → GUID aufgelöst:
  • Firma   = account.name (exakt). ROUTING-REGEL (deterministisch): Existiert der Kunde als account
              in Dataverse → DIREKT verrechnen (Firma = Endkunde; alle Direktkunden sind zuerst als
              Kunde erfasst). Existiert er NICHT als account (z. B. Staiger Rechtsanwälte, Zindel) →
              ÜBER Upgreat: Firma = "Upgreat AG", und es MUSS ein Leistungspaket geben (LP-Name enthält
              Endkunde/TSK). "journal_create.py --suggest <Kunde>" (read-only) wendet diese Regel an.
  • Kontakt = contact.fullname, EINGESCHRÄNKT auf die Firma (parentcustomerid)
  • Leistungspaket = new_leistungspaket (LP-####), je Firma, aktiv. Match auf new_id (LP-####)
              ODER auf Text/TSK-Nr. IM new_bezeichnung (z. B. "TSK0153367" → LP-1045
              "TSK0153367 Zindel - Logbau Cockpit").
NACHFRAGEN STATT RATEN — verbindliche Regel für ALLE Aufrufer (Mensch UND KI-Assistent):
  • 0 oder >1 Treffer (Firma/Kontakt/Leistungspaket) → Skript BRICHT AB und listet Kandidaten.
  • Der Aufrufer zeigt die Kandidaten dem Nutzer und lässt ihn WÄHLEN. Ein KI-Assistent wählt
    NIE selbst "das plausibelste" und ruft still erneut auf; auch bei 0 Treffern nicht
    eigenmächtig einen ähnlichen Namen probieren. Nur genau 1 Treffer gilt als eindeutig.
  • Firma hat aktive Leistungspakete, aber keines angegeben → ABBRUCH (Auswahl ist Pflicht).
  Die Fehlermeldungen instruieren den Aufrufer entsprechend (Design-Prinzip: das Wissen reist
  mit dem Skript). Gilt sinngemäss für jede Portierung auf andere Accounting-Apps
  (andere Dataverse-Orgs/Entitäten): Resolver immer mit Abbruch + Kandidatenliste bauen.

WICHTIG — Leistungspaket ≠ Task:
  new_leistungspaket (LP-####) = Verrechnungs-/Arbeitspaket, wird gesetzt.
  new_task (→ Standard-Activity 'task', TSK-####) = SEPARATER Lookup, Legacy (nur wenige alte Records),
  wird hier bewusst NICHT gesetzt. Das tägliche "TSK…" ist TEXT IM LP-NAMEN (Upgreat), nicht dieser Lookup.

EINMALIGES SETUP beim Übernehmen des Skripts (pro Nutzer & Accounting-App/Org):
  1) Org & App-Registrierung setzen: --org bzw. $DATAVERSE_URL, M365_CLIENT_ID / M365_TENANT_ID.
  2) LP_PFLICHT_FIRMEN (Konstante unten im Code) definieren: Bei welchen Firmen ist ein
     Leistungspaket bei JEDEM Journaleintrag zwingend ("immer Ja")? Beispiel Giovanni:
     "MVM Services AG" — alle Arbeiten für MVM laufen dort und IMMER mit Leistungspaket.
     Die Datenregel (Firma hat aktive Pakete → Auswahl Pflicht) gilt automatisch zusätzlich;
     die Liste macht die Geschäftsregel explizit und schützt vor Datenlücken (Pakete
     versehentlich deaktiviert → Abbruch statt still ohne LP zu buchen).
  3) GESPERRTE_FIRMEN definieren: alte/abgelöste Gesellschaften, auf die NICHT mehr gebucht
     werden darf. Beispiel Giovanni: "MVM AG" → seit 2025-11 läuft alle Verrechnung über
     "MVM Services AG". Das Skript bricht bei gesperrten Firmen ab und nennt das Ziel.

ZIEL-UMGEBUNG / AUTH:
  --org URL                 Dataverse-Env (Default: $DATAVERSE_URL oder Prod-Org)
  M365_CLIENT_ID / M365_TENANT_ID   (Env) — App-Registrierung (delegiert, Dynamics user_impersonation)
  Auth nutzt – falls vorhanden – das gemeinsame auth_common (macOS Keychain, silent);
  sonst portabler MSAL Device-Code-Flow. Token-Cache IMMER verschlüsselt im OS-Keystore
  (macOS Keychain / Windows DPAPI), nie als Klartext-Datei (eiserne Regel).

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

# ─── EINMALIGES SETUP (pro Nutzer/Org anpassen, siehe Docstring) ─────────────────────
# Firmen, bei denen ein Journaleintrag IMMER ein Leistungspaket braucht ("LP-Pflicht: Ja").
# Format: exakter account.name → kurze Begründung (erscheint in der Fehlermeldung).
LP_PFLICHT_FIRMEN = {
    "MVM Services AG": "alle MVM-Arbeiten immer mit Leistungspaket erfassen",
    "Green.ch AG": "Kunde führt Leistungspakete → immer zuordnen",
    "Upgreat AG": "vermittelte Endkunden → das LP identifiziert den Endkunden (Pflicht)",
}

# Firmen, auf die NICHT mehr gebucht werden darf (alte/abgelöste Gesellschaften).
# Format: exakter account.name → Grund + wohin stattdessen.
GESPERRTE_FIRMEN = {
    "MVM AG": "alte Gesellschaft, seit 2025-11 keine Verrechnung mehr → 'MVM Services AG' verwenden",
}


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
    # 2) Portabler Device-Code-Flow — Token-Cache VERSCHLÜSSELT im OS-Keystore
    #    (macOS Keychain / Windows DPAPI), NIE als Klartext-Datei (eiserne Regel).
    import msal
    try:
        from msal_extensions import PersistedTokenCache
    except ImportError:
        sys.exit("❌ Paket 'msal-extensions' fehlt (pip install msal-extensions).\n"
                 "   Ohne OS-Keystore wird kein Token gespeichert (Regel: nie Klartext).")
    client_id = os.environ.get("M365_CLIENT_ID", "0c8e309d-d02e-4244-ae2a-dbb5551cb550")
    tenant_id = os.environ.get("M365_TENANT_ID", "ae7f72de-197d-4ba0-a852-40ee367a5150")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    cache_dir = os.environ.get("JOURNAL_CACHE_DIR",
                               os.path.join(os.path.expanduser("~"), ".config", "journal-create"))
    os.makedirs(cache_dir, exist_ok=True)
    if sys.platform == "darwin":    # macOS: Keychain; die Datei ist nur Lock-/Signal-Marker
        from msal_extensions import KeychainPersistence
        persistence = KeychainPersistence(os.path.join(cache_dir, "token_cache.signal"),
                                          "MiragliaBI-Journal", "dataverse-token-cache")
    elif sys.platform == "win32":   # Windows: DPAPI (nur vom angemeldeten User lesbar)
        from msal_extensions import FilePersistenceWithDataProtection
        persistence = FilePersistenceWithDataProtection(os.path.join(cache_dir, "token_cache.dpapi"))
    else:
        sys.exit("❌ Kein OS-Keystore verfügbar (unterstützt: macOS Keychain, Windows DPAPI).\n"
                 "   Tokens werden nie als Klartext gespeichert — Abbruch.")
    # Einmalige Migration: alten Klartext-Cache übernehmen, Datei danach löschen.
    legacy = os.path.join(cache_dir, "token_cache.json")
    if os.path.exists(legacy):
        with open(legacy, encoding="utf-8") as f:
            persistence.save(f.read())
        os.remove(legacy)
        print("ℹ️  Alt-Cache (Klartext-JSON) in den OS-Keystore migriert und gelöscht.\n"
              "    Empfehlung: sicherheitshalber einmal mit --login neu anmelden.")
    app = msal.PublicClientApplication(client_id, authority=authority,
                                       token_cache=PersistedTokenCache(persistence))
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


# Verbindliche Aufrufer-Regel (Mensch UND KI) — siehe Docstring "NACHFRAGEN STATT RATEN".
ASK = ("→ NACHFRAGEN STATT RATEN: Optionen dem Nutzer zeigen und ihn entscheiden lassen. "
       "KI-Assistent: NIE selbst eines wählen oder den Namen still 'korrigieren' und erneut aufrufen.")


# ---------------------------------------------------------------- Resolver (nachfragen statt raten)
def resolve_firma(dv, name):
    # Satzfelder mitlesen (cr55b_stundensatz/…remote) → nur zur Kontroll-Anzeige des Satz-Basis (read-only).
    rows = dv.get(f"accounts?$select=accountid,name,_transactioncurrencyid_value,"
                  f"cr55b_stundensatz,cr55b_stundensatzremote"
                  f"&$filter=name eq '{esc(name)}'").get("value", [])
    if len(rows) == 0:
        sys.exit(f"❌ Firma '{name}': 0 Treffer als account. Falls über Upgreat vermittelter Endkunde "
                 f"(nicht als eigener Kunde erfasst) → Firma = 'Upgreat AG' + passendes Leistungspaket. "
                 f"Tipp: --suggest \"{name}\".\n   {ASK}")
    if len(rows) > 1:
        c = "; ".join(r["name"] for r in rows)
        sys.exit(f"❌ Firma '{name}': {len(rows)} Treffer → bitte eindeutig. Kandidaten: {c}\n   {ASK}")
    if rows[0]["name"] in GESPERRTE_FIRMEN:  # Setup-Regel: abgelöste Gesellschaft
        sys.exit(f"❌ Firma '{rows[0]['name']}' ist GESPERRT: {GESPERRTE_FIRMEN[rows[0]['name']]}.\n   {ASK}")
    return rows[0]


def resolve_kontakt(dv, account_id, name):
    rows = dv.get(f"contacts?$select=contactid,fullname"
                  f"&$filter=_parentcustomerid_value eq {account_id} and fullname eq '{esc(name)}'").get("value", [])
    if len(rows) == 1:
        return rows[0]
    if len(rows) == 0:
        sys.exit(f"❌ Kontakt '{name}' @ Firma: 0 Treffer. Name prüfen oder Kontakt zuerst anlegen "
                 f"(Kontakt ist Pflicht — nicht raten).\n   {ASK}")
    sys.exit(f"❌ Kontakt '{name}': {len(rows)} Treffer → bitte eindeutig (Rückfrage).\n   {ASK}")


def resolve_leistungspaket(dv, account_id, token, firma_name=""):
    """Leistungspaket (new_leistungspaket, LP-####) je Firma auflösen — NICHT der new_task-Lookup.
    Match: exakt auf new_id (LP-####), sonst Substring in new_bezeichnung/new_id (deckt 'TSK…'-Namen ab)."""
    base = (f"new_leistungspakets?$select=new_leistungspaketid,new_id,new_bezeichnung"
            f"&$filter=_new_firma_value eq {account_id} and statecode eq 0&$orderby=new_id asc")
    allp = dv.get(base).get("value", [])
    if not token:
        if allp:  # Geschäftsregel: hat die Firma Pakete, ist die Auswahl Pflicht
            opts = " | ".join(f"{p['new_id']} {p.get('new_bezeichnung')}" for p in allp)
            sys.exit(f"❌ Firma hat {len(allp)} Leistungspaket(e) → --leistungspaket ist PFLICHT. "
                     f"Optionen: {opts}\n   {ASK}")
        if firma_name in LP_PFLICHT_FIRMEN:  # Setup-Regel: LP-Pflicht trotz fehlender Pakete → Datenlücke
            sys.exit(f"❌ '{firma_name}' ist als LP-PFLICHT-Firma definiert "
                     f"({LP_PFLICHT_FIRMEN[firma_name]}), aber es sind KEINE aktiven Leistungspakete "
                     f"vorhanden → Datenlage klären, NICHT ohne LP buchen.\n   {ASK}")
        return None  # Firma ohne Pakete → ok
    hits = [p for p in allp if (p.get("new_id") or "").lower() == token.lower()]
    if not hits:
        hits = [p for p in allp if token.lower() in (p.get("new_bezeichnung") or "").lower()
                or token.lower() in (p.get("new_id") or "").lower()]
    if len(hits) == 1:
        return hits[0]
    opts = " | ".join(f"{p['new_id']} {p.get('new_bezeichnung')}" for p in (hits or allp))
    sys.exit(f"❌ Leistungspaket '{token}': {len(hits)} Treffer → bitte eindeutig. Optionen: {opts}\n   {ASK}")


def resolve_chf(dv):
    rows = dv.get("transactioncurrencies?$select=transactioncurrencyid,isocurrencycode"
                  "&$filter=isocurrencycode eq 'CHF'").get("value", [])
    return rows[0]["transactioncurrencyid"] if rows else None


def find_possible_duplicates(dv, firma_id, datum):
    """Bereits erfasste Journale gleicher Firma am selben Tag (Idempotenz-Vorabprüfung, read-only)."""
    return dv.get(f"cr55b_journals?$select=cr55b_journalname,cr55b_stunden,cr55b_beschreibung"
                  f"&$filter=_cr55b_firma_value eq {firma_id} "
                  f"and cr55b_journaldatum eq {datum}").get("value", [])


def _last_journal_contact(dv, firma_id):
    """Hinweis: zuletzt im Journal verwendeter Kontakt dieser Firma (read-only)."""
    rows = dv.get(f"cr55b_journals?$select=cr55b_journaldatum&$expand=cr55b_Kontakt($select=fullname)"
                  f"&$filter=_cr55b_firma_value eq {firma_id}"
                  f"&$orderby=cr55b_journaldatum desc&$top=1").get("value", [])
    return ((rows[0].get("cr55b_Kontakt") or {}).get("fullname") if rows else None)


def suggest_routing(dv, term):
    """Deterministisches Routing (Regel Giovanni):
      • Kunde existiert als account in Dataverse  → DIREKT (Firma = Endkunde). Alle Direktkunden sind
        zuerst als Kunde erfasst. Hat der account aktive Leistungspakete → LP ist Pflicht.
      • Kunde existiert NICHT als account (z. B. Staiger Rechtsanwälte, Zindel) → ÜBER UPGREAT:
        Firma = Upgreat AG, es MUSS ein Leistungspaket geben (LP-Name enthält Endkunde/TSK).
    Read-only."""
    e = esc(term)
    accts = dv.get(f"accounts?$select=accountid,name&$filter=contains(name,'{e}')&$top=10").get("value", [])
    print(f"── Routing für '{term}' (deterministisch, read-only) ─────────────")
    if accts:
        print("  ✓ Als Kunde (account) erfasst → DIREKT verrechnen (Firma = Endkunde).")
        for a in accts:
            if a['name'] in GESPERRTE_FIRMEN:
                print(f"    • {a['name']}: 🚫 GESPERRT — {GESPERRTE_FIRMEN[a['name']]}")
                continue
            lps = dv.get(f"new_leistungspakets?$select=new_id,new_bezeichnung"
                         f"&$filter=_new_firma_value eq {a['accountid']} and statecode eq 0"
                         f"&$orderby=new_id asc").get("value", [])
            if lps:
                opts = " | ".join(((p.get('new_id') or '') + ' ' + (p.get('new_bezeichnung') or '')).strip()
                                  for p in lps)
                print(f"    • {a['name']}: {len(lps)} aktive(s) Leistungspaket(e) → LP PFLICHT. {opts}")
            elif a['name'] in LP_PFLICHT_FIRMEN:
                print(f"    • {a['name']}: ⚠️ LP-PFLICHT definiert ({LP_PFLICHT_FIRMEN[a['name']]}), "
                      f"aber KEINE aktiven Pakete → Datenlage klären, nicht ohne LP buchen!")
            else:
                print(f"    • {a['name']}: keine aktiven Leistungspakete → ohne LP.")
            kc = _last_journal_contact(dv, a['accountid'])
            if kc:
                print(f"      letzter Journal-Kontakt: {kc} (Hinweis, bestätigen)")
        return
    print("  ✗ NICHT als Kunde (account) erfasst → ÜBER UPGREAT (Firma = Upgreat AG, Leistungspaket PFLICHT).")
    upg = dv.get("accounts?$select=accountid,name&$filter=name eq 'Upgreat AG'").get("value", [])
    if not upg:
        print("    ⚠️ 'Upgreat AG' nicht gefunden → manuell klären.")
        return
    lps = dv.get(f"new_leistungspakets?$select=new_id,new_bezeichnung"
                 f"&$filter=_new_firma_value eq {upg[0]['accountid']} and statecode eq 0 "
                 f"and contains(new_bezeichnung,'{e}')&$orderby=new_id asc").get("value", [])
    if not lps:
        print(f"    Kein aktives Upgreat-Leistungspaket enthält '{term}' → Name prüfen oder LP neu anlegen/erfragen.")
    elif len(lps) == 1:
        p = lps[0]
        print(f"    → Eindeutig: Firma = Upgreat AG · LP = {p.get('new_id')} {p.get('new_bezeichnung')}")
    else:
        print(f"    {len(lps)} mögliche Leistungspakete → bitte eines wählen:")
        for p in lps:
            print(f"      • {p.get('new_id')}  {p.get('new_bezeichnung')}")


# ---------------------------------------------------------------- main
def yn(default):
    return {"type": str, "choices": ["ja", "nein"], "default": default}


def is_ja(v):
    return str(v).strip().lower() in ("ja", "j", "true", "1", "yes", "y")


def main():
    p = argparse.ArgumentParser(description="Dataverse Journal-Eintrag anlegen (DRY-RUN per Default).")
    p.add_argument("--firma", help="Firmenname (account.name, exakt); Pflicht ausser im --suggest-Modus")
    p.add_argument("--kontakt", help="Kontakt (contact.fullname, je Firma); Pflicht ausser im --suggest-Modus")
    p.add_argument("--beschreibung",
                   help="Leistungsbeschreibung (sachlich, deutsch, kurz); Pflicht ausser im --suggest-Modus")
    p.add_argument("--stunden", type=float, help="Stunden, z. B. 0.5; Pflicht ausser im --suggest-Modus")
    p.add_argument("--leistungspaket", help="LP-#### oder TSK/Text im LP-Namen (Pflicht, falls Firma Pakete hat)")
    p.add_argument("--suggest", metavar="KUNDE",
                   help="Read-only: deterministisches Routing (account vorhanden = direkt, sonst über Upgreat) + LP zeigen und beenden")
    p.add_argument("--datum", default=date.today().isoformat(), help="JournalDatum YYYY-MM-DD (Default: heute)")
    p.add_argument("--homeoffice", **yn("ja"))
    p.add_argument("--mwstpflichtig", **yn("ja"))
    p.add_argument("--inrechnung", **yn("ja"))
    p.add_argument("--kostenlos", **yn("nein"))
    p.add_argument("--fixpreis", type=float, help="optional: Fixpreis statt Std×Satz")
    p.add_argument("--org", default=DEFAULT_ORG, help=f"Dataverse-URL (Default: {DEFAULT_ORG})")
    p.add_argument("--commit", action="store_true", help="WIRKLICH anlegen (sonst Dry-Run)")
    p.add_argument("--allow-duplicate", action="store_true",
                   help="Duplikatschutz übergehen (gleiche Firma+Datum+Stunden existiert bereits)")
    p.add_argument("--yes", action="store_true", help="Bestätigung überspringen (für nicht-interaktive Läufe)")
    p.add_argument("--login", action="store_true", help="interaktiver Device-Code-Login erzwingen")
    args = p.parse_args()

    token = get_token(args.org, force_login=args.login)
    dv = DV(args.org, token)

    if args.suggest:
        suggest_routing(dv, args.suggest)
        return

    missing = [f"--{n}" for n in ("firma", "kontakt", "beschreibung", "stunden")
               if getattr(args, n) in (None, "")]
    if missing:
        sys.exit(f"❌ Fehlende Pflichtargumente: {', '.join(missing)}  (oder --suggest <Kunde> für Präzedenz).")

    firma = resolve_firma(dv, args.firma)
    kontakt = resolve_kontakt(dv, firma["accountid"], args.kontakt)
    lp = resolve_leistungspaket(dv, firma["accountid"], args.leistungspaket, firma["name"])
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
    ho = is_ja(args.homeoffice)
    rate = firma.get("cr55b_stundensatzremote") if ho else firma.get("cr55b_stundensatz")
    print(f"  Datum/Stunden : {args.datum} / {args.stunden}  · HomeOffice={ho}")
    print(f"  Satz-Basis    : {'REMOTE (stundensatzremote)' if ho else 'VOR ORT (stundensatz)'} ≈ {rate}"
          f"   (App rechnet final; nur Kontrolle)")
    if ho:
        print("    ⚠️  HomeOffice=Ja → Remote-Satz. Bei Vor-Ort-Terminen --homeoffice nein setzen.")
    print(f"  Org           : {args.org}")
    print("── Payload (POST {API}/" + ENTITYSET + ") ─────────────────")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    if not args.commit:
        print("\n💡 DRY-RUN — es wurde NICHTS angelegt. Mit --commit tatsächlich erstellen.")
        return

    # Idempotenz: gleiche Firma + Datum + Stunden bereits vorhanden? (gegen versehentliche Doppel-Erfassung)
    dups = [d for d in find_possible_duplicates(dv, firma["accountid"], args.datum)
            if abs((d.get("cr55b_stunden") or 0) - float(args.stunden)) < 1e-6]
    if dups and not args.allow_duplicate:
        names = ", ".join(d.get("cr55b_journalname", "?") for d in dups)
        sys.exit(f"⚠️  Duplikatschutz: bereits {len(dups)} Eintrag/Einträge an {args.datum} für "
                 f"{firma['name']} mit {args.stunden} h ({names}). Mit --allow-duplicate trotzdem anlegen.")

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
