#!/usr/bin/env python3
"""mvm_pp_dv.py — read-only Dataverse-Abfragen gegen MVM Prozesse Produktion (orgb0ca9fb2)."""
import json, sys, requests
from mvm_pp_login import _silent
ORG = "https://orgb0ca9fb2.api.crm4.dynamics.com"
API = f"{ORG}/api/data/v9.2"
def _h():
    return {"Authorization": f"Bearer {_silent([f'{ORG}/.default'])}", "Accept": "application/json",
            "OData-MaxVersion": "4.0", "OData-Version": "4.0",
            "Prefer": 'odata.include-annotations="*"'}
def get(path):
    url = path if path.startswith("http") else f"{API}/{path.lstrip('/')}"
    r = requests.get(url, headers=_h(), timeout=120)
    if not r.ok: sys.exit(f"HTTP {r.status_code}: {r.text[:1500]}")
    return r.json()
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "whoami"
    if cmd == "whoami": print(json.dumps(get("WhoAmI"), indent=2, ensure_ascii=False))
    elif cmd == "raw": print(json.dumps(get(sys.argv[2]).get("value", get(sys.argv[2])) if False else get(sys.argv[2]), indent=2, ensure_ascii=False))
    elif cmd == "setname":
        print(json.dumps(get(f"EntityDefinitions(LogicalName='{sys.argv[2]}')?$select=LogicalName,EntitySetName,DisplayName"), indent=2, ensure_ascii=False))
    elif cmd == "attrs":
        d = get(f"EntityDefinitions(LogicalName='{sys.argv[2]}')/Attributes?$select=LogicalName,AttributeType,DisplayName")
        for a in sorted(d.get("value", []), key=lambda x: x["LogicalName"]):
            dn = ((a.get("DisplayName",{}) or {}).get("UserLocalizedLabel") or {}).get("Label","")
            print(f"{a['LogicalName']:40s}\t{a.get('AttributeType'):18s}\t{dn}")
    else: sys.exit(f"Unbekannt: {cmd}")
