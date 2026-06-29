#!/usr/bin/env python3
"""
koster_flow.py — Read-only Power-Automate-Run-History gegen die **Koster-AG-Prod**.

Nutzt den im Keychain (kosterag) liegenden FOCI-Login (siehe koster_login.py) und
zieht silent ein Token fuer die Flow-Service-API. REIN LESEND.

    ./.venv/bin/python koster_flow.py envs
    ./.venv/bin/python koster_flow.py flows  <envName>
    ./.venv/bin/python koster_flow.py find   <envName> <substr>      # Flow per Name-Substring
    ./.venv/bin/python koster_flow.py runs   <envName> <flowName> [top]
    ./.venv/bin/python koster_flow.py run    <envName> <flowName> <runName>
    ./.venv/bin/python koster_flow.py actions<envName> <flowName> <runName>
"""
import json
import sys

import msal
import requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "9d7f37af-5bc8-4945-a118-98bcf7572346"
FLOW_RES = "https://service.flow.microsoft.com"
API = "https://api.flow.microsoft.com/providers/Microsoft.ProcessSimple"
APIV = "api-version=2016-11-01"


def _token():
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache("kosterag"))
    accts = app.get_accounts()
    if not accts:
        sys.exit("❌ Kein Konto im Cache — zuerst koster_login.py --init/--poll.")
    res = app.acquire_token_silent([f"{FLOW_RES}/.default"], account=accts[0])
    if not res or "access_token" not in res:
        sys.exit(f"❌ Flow-Token fehlgeschlagen: {res}")
    return res["access_token"]


def _get(tok, url):
    r = requests.get(url, headers={
        "Authorization": f"Bearer {tok}", "Accept": "application/json"}, timeout=120)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:1500]}")
    return r.json()


def _get_all(tok, url):
    """Folgt @odata.nextLink und sammelt alle 'value'-Eintraege."""
    items = []
    while url:
        d = _get(tok, url)
        items.extend(d.get("value", []))
        url = d.get("nextLink") or d.get("@odata.nextLink")
    return items


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "envs"
    tok = _token()

    if cmd == "envs":
        d = _get(tok, f"{API}/environments?{APIV}")
        for e in d.get("value", []):
            p = e.get("properties", {})
            print(f"{e['name']}\t{p.get('displayName')}\tdefault={p.get('isDefault')}")

    elif cmd == "flows":
        env = sys.argv[2]
        for f in _get_all(tok, f"{API}/environments/{env}/flows?{APIV}&$top=50"):
            p = f.get("properties", {})
            print(f"{f['name']}\t{p.get('displayName')}\tstate={p.get('state')}")

    elif cmd == "find":
        env, sub = sys.argv[2], sys.argv[3].lower()
        for f in _get_all(tok, f"{API}/environments/{env}/flows?{APIV}&$top=50"):
            p = f.get("properties", {})
            if sub in (p.get("displayName") or "").lower():
                print(f"{f['name']}\t{p.get('displayName')}\tstate={p.get('state')}")

    elif cmd == "runs":
        env, flow = sys.argv[2], sys.argv[3]
        top = sys.argv[4] if len(sys.argv) > 4 else "30"
        d = _get(tok, f"{API}/environments/{env}/flows/{flow}/runs?{APIV}&$top={top}")
        for r in d.get("value", []):
            p = r.get("properties", {})
            err = (p.get("error") or {}).get("message", "")
            print(f"{r['name']}\t{p.get('status')}\t{p.get('startTime')}\t"
                  f"{p.get('endTime')}\tcode={p.get('code')}\t{err[:80]}")

    elif cmd == "run":
        env, flow, run = sys.argv[2], sys.argv[3], sys.argv[4]
        d = _get(tok, f"{API}/environments/{env}/flows/{flow}/runs/{run}?{APIV}")
        print(json.dumps(d, indent=2, ensure_ascii=False))

    elif cmd == "actions":
        env, flow, run = sys.argv[2], sys.argv[3], sys.argv[4]
        d = _get(tok, f"{API}/environments/{env}/flows/{flow}/runs/{run}/actions?{APIV}")
        print(json.dumps(d, indent=2, ensure_ascii=False))

    elif cmd == "definition":
        env, flow = sys.argv[2], sys.argv[3]
        d = _get(tok, f"{API}/environments/{env}/flows/{flow}?{APIV}&$expand=properties.flowEntitySummary,properties.definitionSummary")
        print(json.dumps(d, indent=2, ensure_ascii=False))

    elif cmd == "reps":
        # Repetitions einer (Scope-/Loop-)Action in einem Run
        env, flow, run, action = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        d = _get(tok, f"{API}/environments/{env}/flows/{flow}/runs/{run}/actions/{action}/scopedRepetitions?{APIV}")
        print(json.dumps(d, indent=2, ensure_ascii=False))

    else:
        sys.exit(f"Unbekannter Befehl: {cmd}")


if __name__ == "__main__":
    main()
