#!/usr/bin/env python3
"""
koster_dv.py — Read-only Dataverse-Abfragen gegen die **Koster-AG-Produktion**.

Nutzt den im Keychain (kosterag) liegenden FOCI-Login (siehe koster_login.py),
zieht silent ein Dataverse-Token für org9c15a4d2 und feuert eine OData-Query.

    ./.venv/bin/python koster_dv.py whoami
    ./.venv/bin/python koster_dv.py setname ks_eingangsqueue
    ./.venv/bin/python koster_dv.py raw "ks_eingangsqueues?%24top=3"
"""
import json
import sys

import msal
import requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "9d7f37af-5bc8-4945-a118-98bcf7572346"
RESOURCE = "https://org9c15a4d2.api.crm4.dynamics.com"
API = f"{RESOURCE}/api/data/v9.2"


def _token():
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache("kosterag"))
    accts = app.get_accounts()
    if not accts:
        sys.exit("❌ Kein Konto im Cache — zuerst koster_login.py --init/--poll.")
    res = app.acquire_token_silent([f"{RESOURCE}/.default"], account=accts[0])
    if not res or "access_token" not in res:
        sys.exit(f"❌ Dataverse-Token fehlgeschlagen: {res}")
    return res["access_token"]


def _get(token, path):
    url = path if path.startswith("http") else f"{API}/{path.lstrip('/')}"
    r = requests.get(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": 'odata.include-annotations="*"',
    }, timeout=120)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:1500]}")
    return r.json()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "whoami"
    tok = _token()
    if cmd == "whoami":
        print(json.dumps(_get(tok, "WhoAmI"), indent=2, ensure_ascii=False))
    elif cmd == "setname":
        ln = sys.argv[2]
        print(json.dumps(_get(
            tok, f"EntityDefinitions(LogicalName='{ln}')"
                 "?$select=LogicalName,EntitySetName,DisplayName"),
            indent=2, ensure_ascii=False))
    elif cmd == "attrs":
        ln = sys.argv[2]
        data = _get(tok, f"EntityDefinitions(LogicalName='{ln}')/Attributes"
                         "?$select=LogicalName,AttributeType")
        for a in sorted(data.get("value", []), key=lambda x: x["LogicalName"]):
            print(f"{a['LogicalName']}\t{a.get('AttributeType')}")
    elif cmd == "raw":
        data = _get(tok, sys.argv[2])
        rows = data.get("value", data)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        sys.exit(f"Unbekannter Befehl: {cmd}")


if __name__ == "__main__":
    main()
