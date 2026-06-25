#!/usr/bin/env python3
"""
mvm_pp_login.py — Device-Code-Login in den **MVM-AG-Tenant** für die
Power-Platform-Umgebung **„Prozesse Produktion"** (read-only Diagnose).

Meldet `raoul@miraglia-bi.com` (Gast in MVM AG) per Device-Code-Flow am
MVM-Tenant an. Verwendet den **Azure-CLI-First-Party-Client**
(`04b07795-…`), der in JEDEM Tenant vorkonsentiert ist und zur FOCI-Familie
gehört — d. h. EIN Login liefert ein Refresh-Token, mit dem danach
Dataverse **und** BAP (Power-Platform-Admin) **und** PowerApps **silent**
(ohne erneuten Code) bedient werden können.

Token-Cache liegt im **macOS Keychain** (Service=MiragliaBI-PowerBI,
Account=mvm_pp) — nie als Klartext im Vault (siehe CLAUDE.md Token-Regel).

Zwei-Phasen, damit der Code SOFORT erscheint:
    ./.venv/bin/python mvm_pp_login.py --init     # zeigt URL + Code, beendet sofort
    ./.venv/bin/python mvm_pp_login.py --poll      # pollt (blockiert bis Login fertig) — im Hintergrund
    ./.venv/bin/python mvm_pp_login.py --test      # silent: WhoAmI gegen Graph (/me)

Resource-Helfer für die spätere Analyse:
    ./.venv/bin/python mvm_pp_login.py --discover-dataverse  # listet alle Dataverse-Orgs (Friendly/Url/ApiUrl)
    ./.venv/bin/python mvm_pp_login.py --bap-environments    # listet Power-Platform-Environments via BAP
    ./.venv/bin/python mvm_pp_login.py --dataverse-token URL # druckt Dataverse-Token für eine Org-URL (silent)
"""
import json
import sys
from pathlib import Path

import msal
import requests

# --- Azure CLI First-Party Client (public, device-code-fähig, FOCI) ---
CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "3becd9bb-f602-4c6b-8e86-f1e42db365ea"  # MVM AG
AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"

# Anker-Scope für den Device-Flow: Graph .default + offline_access.
# Über das FOCI-Refresh-Token lassen sich danach andere Resources silent ziehen.
INIT_SCOPES = ["https://graph.microsoft.com/.default"]

# Power-Platform-/Dataverse-Resources (alle FOCI-silent nach einem Login)
DISCO_SCOPES = ["https://globaldisco.crm.dynamics.com/.default"]
BAP_SCOPES = ["https://api.bap.microsoft.com/.default"]

_SLUG = "mvm_pp"
_FLOW_FILE = Path.home() / ".config" / "m365-sync" / "mvm_pp_deviceflow.json"


def _cache():
    from auth_common import build_pbi_cache
    return build_pbi_cache(_SLUG)


def _app():
    return msal.PublicClientApplication(CID, authority=AUTHORITY, token_cache=_cache())


def cmd_init():
    app = _app()
    flow = app.initiate_device_flow(scopes=INIT_SCOPES)
    if "user_code" not in flow:
        sys.exit(f"❌ Device-Flow konnte nicht gestartet werden: {flow.get('error_description', flow)}")
    _FLOW_FILE.parent.mkdir(parents=True, exist_ok=True)
    _FLOW_FILE.write_text(json.dumps(flow))
    # Maschinen-lesbar für den Aufrufer:
    print("URL=" + flow.get("verification_uri", "https://microsoft.com/devicelogin"))
    print("CODE=" + flow["user_code"])
    print("EXPIRES_IN=" + str(flow.get("expires_in", 900)))
    print("---")
    print(flow["message"])


def cmd_poll():
    if not _FLOW_FILE.exists():
        sys.exit("❌ Kein Device-Flow gefunden — zuerst --init ausführen.")
    flow = json.loads(_FLOW_FILE.read_text())
    app = _app()
    result = app.acquire_token_by_device_flow(flow)  # blockiert bis Login/Timeout
    if "access_token" not in result:
        sys.exit(f"❌ Login fehlgeschlagen: {result.get('error_description', result)}")
    try:
        _FLOW_FILE.unlink()
    except OSError:
        pass
    accts = app.get_accounts()
    who = accts[0]["username"] if accts else "?"
    print(f"✅ Login erfolgreich als {who} — Token im Keychain ({_SLUG}).")


def _silent(scopes):
    app = _app()
    accts = app.get_accounts()
    if not accts:
        sys.exit("❌ Kein Konto im Cache — zuerst --init + --poll (Login) ausführen.")
    res = app.acquire_token_silent(scopes, account=accts[0])
    if not res or "access_token" not in res:
        sys.exit(f"❌ Silent-Token fehlgeschlagen für {scopes}: {res}")
    return res["access_token"]


def cmd_test():
    tok = _silent(INIT_SCOPES)
    r = requests.get("https://graph.microsoft.com/v1.0/me",
                     headers={"Authorization": f"Bearer {tok}"}, timeout=30)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:500]}")
    me = r.json()
    print(f"✅ Eingeloggt als {me.get('userPrincipalName')} "
          f"({me.get('displayName')}) im MVM-Tenant — Graph erreichbar.")


def cmd_discover_dataverse():
    """Findet alle Dataverse-Org-URLs über die Global-Discovery-API."""
    tok = _silent(DISCO_SCOPES)
    r = requests.get(
        "https://globaldisco.crm.dynamics.com/api/discovery/v2.0/Instances",
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
        timeout=60)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:800]}")
    insts = r.json().get("value", [])
    print(f"# {len(insts)} Dataverse-Instanz(en) sichtbar\n", file=sys.stderr)
    for inst in insts:
        print(f"{inst.get('FriendlyName')}\t{inst.get('UrlName')}\t{inst.get('ApiUrl')}\t{inst.get('EnvironmentId')}")


def cmd_bap_environments():
    """Listet Power-Platform-Environments via BAP-Admin-API."""
    tok = _silent(BAP_SCOPES)
    r = requests.get(
        "https://api.bap.microsoft.com/providers/Microsoft.BusinessAppPlatform/"
        "environments?api-version=2021-04-01",
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"},
        timeout=60)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:800]}")
    for env in r.json().get("value", []):
        props = env.get("properties", {})
        di = props.get("linkedEnvironmentMetadata", {})
        print(f"{props.get('displayName')}\t{env.get('name')}\t{di.get('instanceApiUrl', '-')}")


def cmd_dataverse_token():
    if len(sys.argv) < 3:
        sys.exit("Usage: --dataverse-token https://orgXXXX.api.crmN.dynamics.com")
    base = sys.argv[2].rstrip("/")
    print(_silent([f"{base}/.default"]))


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--test"
    {
        "--init": cmd_init,
        "--poll": cmd_poll,
        "--test": cmd_test,
        "--discover-dataverse": cmd_discover_dataverse,
        "--bap-environments": cmd_bap_environments,
        "--dataverse-token": cmd_dataverse_token,
    }.get(arg, cmd_test)()
