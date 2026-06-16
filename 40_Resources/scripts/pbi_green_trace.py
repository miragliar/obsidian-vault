#!/usr/bin/env python3
"""READ-ONLY: Green report -> dataset -> upstream dataflow(s); find the dataflow that
holds the `DocumentItems` query (Abo model) and report whether DateEarliestTermination /
AboEndCorrected / DateLogicFlag are already present. Token cached in macOS Keychain
(auth_common.build_pbi_cache). Nothing is written to Power BI."""
import sys, json, time
import msal, requests
from auth_common import build_pbi_cache

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"          # Azure CLI public client (device-code, PBI)
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"
TENANT = "green.ch"
GROUP = "1fab866d-43e5-4e93-8165-d5cff353b50c"
REPORT = "3daa2bac-7677-4fa9-ba1d-0a2a8b462725"
NEEDLE_M = ["DocumentItems", "AboStart", "AboEnd", "AboEndeffective", "DateLogicFlag",
            "AboEndCorrected", "DateEarliestTermination", "ContractEnd", "BillingEnd"]


def get_token():
    app = msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache(TENANT))
    acc = app.get_accounts()
    r = app.acquire_token_silent(SCOPE, account=acc[0]) if acc else None
    if not r:
        print("INTERACTIVE: Ein Browser-Fenster sollte sich jetzt fuer den Login oeffnen ...", flush=True)
        try:
            r = app.acquire_token_interactive(SCOPE, prompt="select_account")
        except Exception as e:
            print("INTERACTIVE_FAILED:", repr(e), file=sys.stderr, flush=True)
            sys.exit(2)
    if not r or "access_token" not in r:
        print("AUTH_FAILED:", (r or {}).get("error"), (r or {}).get("error_description"),
              file=sys.stderr, flush=True)
        sys.exit(2)
    return r["access_token"]


def main():
    tok = get_token()
    print("AUTH_OK", flush=True)
    s = requests.Session(); s.headers["Authorization"] = f"Bearer {tok}"

    def get(path):
        r = s.get(BASE + path, timeout=90)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 20))); r = s.get(BASE + path, timeout=90)
        return r

    grp = get(f"/groups/{GROUP}")
    gname = grp.json().get("name") if grp.ok else "?"
    print(f"\nWORKSPACE: {gname}  ({GROUP})")

    rep = get(f"/groups/{GROUP}/reports/{REPORT}")
    if not rep.ok:
        print("REPORT fetch failed:", rep.status_code, rep.text[:300]); sys.exit(3)
    rj = rep.json(); dsid = rj.get("datasetId")
    print(f"REPORT : {rj.get('name')}")
    ds = get(f"/groups/{GROUP}/datasets/{dsid}")
    dsname = ds.json().get("name") if ds.ok else "?"
    print(f"DATASET: {dsname}  ({dsid})")

    dss = get(f"/groups/{GROUP}/datasets/{dsid}/datasources")
    if dss.ok:
        print("DATASET DATASOURCES:")
        for d in dss.json().get("value", []):
            print("   -", d.get("datasourceType"),
                  json.dumps(d.get("connectionDetails", {}), ensure_ascii=False))

    dfs = get(f"/groups/{GROUP}/dataflows")
    dflist = dfs.json().get("value", []) if dfs.ok else []
    print(f"\nDATAFLOWS in workspace ({len(dflist)}):")
    for df in dflist:
        print("   -", df.get("name"), "|", df.get("objectId"))

    def scan(gid, df):
        dfid = df.get("objectId"); name = df.get("name")
        defn = get(f"/groups/{gid}/dataflows/{dfid}")
        if not defn.ok:
            print(f"   [{name}] definition fetch failed: {defn.status_code}"); return None
        text = defn.text
        try:
            entities = [e.get("name") for e in defn.json().get("entities", [])]
        except Exception:
            entities = []
        hitsM = [n for n in NEEDLE_M if n in text]
        is_match = ("DocumentItems" in entities) or ("DocumentItems" in text)
        print(f"   [{name}] entities={entities}")
        print(f"       M-hits: {hitsM}{'   <<< MATCH (DocumentItems)' if is_match else ''}")
        if is_match:
            return {"workspace": gname if gid == GROUP else gid, "workspaceId": gid,
                    "dataflow": name, "dataflowId": dfid, "entities": entities,
                    "has_DateEarliestTermination": "DateEarliestTermination" in text,
                    "has_AboEndCorrected": "AboEndCorrected" in text,
                    "has_DateLogicFlag": "DateLogicFlag" in text}
        return None

    print("\n=== ENTITY / M SCAN (this workspace) ===")
    hits = [h for h in (scan(GROUP, df) for df in dflist) if h]

    if not hits:
        print("\nKein DocumentItems-Dataflow in diesem Workspace — scanne alle erreichbaren Workspaces ...")
        for g in get("/groups").json().get("value", []):
            gid = g.get("id")
            if gid == GROUP:
                continue
            d2 = get(f"/groups/{gid}/dataflows")
            for df in (d2.json().get("value", []) if d2.ok else []):
                defn = get(f"/groups/{gid}/dataflows/{df['objectId']}")
                if defn.ok and "DocumentItems" in defn.text:
                    print(f"   MATCH: workspace '{g.get('name')}' ({gid}) -> dataflow '{df.get('name')}' ({df['objectId']})")
                    hits.append({"workspace": g.get("name"), "workspaceId": gid,
                                 "dataflow": df.get("name"), "dataflowId": df["objectId"],
                                 "has_DateEarliestTermination": "DateEarliestTermination" in defn.text,
                                 "has_AboEndCorrected": "AboEndCorrected" in defn.text,
                                 "has_DateLogicFlag": "DateLogicFlag" in defn.text})

    print("\n=== RESULT ===")
    print(json.dumps(hits, ensure_ascii=False, indent=2))
    with open("/tmp/pbi_green_trace.json", "w") as f:
        json.dump({"workspace": gname, "report": rj.get("name"), "dataset": dsname,
                   "datasetId": dsid,
                   "dataflows": [{"name": d.get("name"), "id": d.get("objectId")} for d in dflist],
                   "matches": hits}, f, ensure_ascii=False, indent=2)
    print("-> /tmp/pbi_green_trace.json")


if __name__ == "__main__":
    main()
