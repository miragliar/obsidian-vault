#!/usr/bin/env python3
"""
pbi_inventory.py — READ-ONLY tenant inventory of Power BI datasets + dataflows with
refresh schedule, datasources, and ON-PREM GATEWAY binding. Builds the refresh/gateway
matrix and flags cloud-only items that are needlessly pinned to the on-prem gateway.

Outputs a printed matrix + a JSON file (incl. DatasetId->name map for log attribution).
Cached device-code token (same cache as pbi_refresh_probe.py).

Usage:
  ./.venv/bin/python pbi_inventory.py --tenant directhandlingch.onmicrosoft.com --json /tmp/pbi_inventory.json
"""
import argparse, json, os, re, sys, time
from collections import Counter, defaultdict
import msal, requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"
# datasource types that imply an on-prem (gateway-requiring) connection
ONPREM = {"Sql", "File", "Folder", "Odbc", "OleDb", "Oracle", "SapHana", "SapBw",
          "Teradata", "MySql", "PostgreSql", "Db2", "Informix", "Sybase", "Exchange"}
CLOUD = {"PowerPlatformDataflows", "Extension", "Web", "OData", "SharePointList",
         "AzureBlobs", "AzureDataLakeStorage", "PowerBI", "AnalysisServices"}


def log(*a): print(*a, file=sys.stderr, flush=True)


def get_token(tenant):
    # Token-Cache im macOS Keychain (verschlüsselt, kein Dropbox-Sync) — via auth_common.
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(CID, authority=f"https://login.microsoftonline.com/{tenant}", token_cache=build_pbi_cache(tenant))
    acc = app.get_accounts()
    r = app.acquire_token_silent(SCOPE, account=acc[0]) if acc else None
    if not r:
        fl = app.initiate_device_flow(scopes=SCOPE); log(fl["message"]); r = app.acquire_token_by_device_flow(fl)
    return r["access_token"]


class Api:
    def __init__(self, tok):
        self.s = requests.Session(); self.s.headers["Authorization"] = f"Bearer {tok}"
    def get(self, path):
        for _ in range(4):
            r = self.s.get(BASE + path, timeout=60)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 20))); continue
            if r.status_code >= 400: return None
            return r.json()
        return None
    def value(self, path):
        j = self.get(path); return (j or {}).get("value", []) if j else []


def classify(sources):
    types, dbs, gws, onprem = set(), set(), set(), False
    for d in sources:
        dt = d.get("datasourceType", "?")
        types.add(dt)
        cd = d.get("connectionDetails", {}) or {}
        server = (cd.get("server") or cd.get("path") or cd.get("url") or "")
        db = cd.get("database") or ""
        if d.get("gatewayId"): gws.add(d["gatewayId"])
        if dt in ONPREM: onprem = True
        if db and ("proffix" in server.lower() or "shar-srv" in server.lower() or db.upper().startswith("PX")):
            dbs.add(db.upper())
    return types, dbs, gws, onprem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tenant", required=True)
    ap.add_argument("--json", default="/tmp/pbi_inventory.json")
    a = ap.parse_args()

    api = Api(get_token(a.tenant))
    gw_names = {g.get("id"): g.get("name", g.get("id")) for g in api.value("/gateways")}
    log(f"Gateways: {gw_names}")

    groups = api.value("/groups")
    log(f"{len(groups)} workspaces")
    records, ds_id_name = [], {}
    sched_hist = Counter()         # hour-of-day -> count of scheduled dataset refreshes
    for i, g in enumerate(groups, 1):
        gid, gn = g["id"], g.get("name", "?")
        log(f"[{i}/{len(groups)}] {gn}")
        for d in api.value(f"/groups/{gid}/datasets"):
            did, dn = d.get("id"), d.get("name", "?")
            ds_id_name[did] = dn
            sched = api.get(f"/groups/{gid}/datasets/{did}/refreshSchedule") or {}
            srcs = api.value(f"/groups/{gid}/datasets/{did}/datasources")
            types, dbs, gws, onprem = classify(srcs)
            times = sched.get("times", []) or []
            if sched.get("enabled"):
                for t in times:
                    try: sched_hist[int(t[:2])] += 1
                    except Exception: pass
            records.append({
                "ws": gn, "type": "dataset", "name": dn, "id": did,
                "owner": d.get("configuredBy"), "refreshable": d.get("isRefreshable"),
                "sched_enabled": sched.get("enabled"), "times": times,
                "days": len(sched.get("days", []) or []), "tz": sched.get("localTimeZoneId"),
                "src_types": sorted(types), "proffix_dbs": sorted(dbs),
                "gw_bound": bool(gws), "gateways": sorted(gw_names.get(x, x) for x in gws),
                "needs_onprem": onprem,
            })
        for f in api.value(f"/groups/{gid}/dataflows"):
            fid, fn = f.get("objectId"), f.get("name", "?")
            srcs = api.value(f"/groups/{gid}/dataflows/{fid}/datasources")
            types, dbs, gws, onprem = classify(srcs)
            txns = api.value(f"/groups/{gid}/dataflows/{fid}/transactions")[:6]
            last = [t.get("startTime", "")[:16] for t in txns if t.get("startTime")]
            records.append({
                "ws": gn, "type": "dataflow", "name": fn, "id": fid,
                "recent_runs": last, "src_types": sorted(types), "proffix_dbs": sorted(dbs),
                "gw_bound": bool(gws), "gateways": sorted(gw_names.get(x, x) for x in gws),
                "needs_onprem": onprem,
            })

    json.dump({"records": records, "ds_id_name": ds_id_name, "gateways": gw_names,
               "sched_hist": dict(sorted(sched_hist.items()))}, open(a.json, "w"), indent=2)
    log(f"Wrote {a.json}  ({len(records)} items)")

    # ---- printed matrix ----
    def row(r):
        sched = ("OFF" if r.get("sched_enabled") is False else
                 ("/".join(r.get("times", [])[:6]) or "—")) if r["type"] == "dataset" else \
                ("run:" + (r.get("recent_runs", [""])[0][11:] if r.get("recent_runs") else "—"))
        flag = ""
        if r["gw_bound"] and not r["needs_onprem"]: flag = "⚠cloud-only→GW"
        elif r["proffix_dbs"]: flag = "PROFFIX:" + ",".join(d.replace("PX", "") for d in r["proffix_dbs"])
        gw = "Y" if r["gw_bound"] else "n"
        return f"{r['ws'][:14]:<14} {r['type'][:2]:<2} {r['name'][:30]:<30} {sched[:24]:<24} gw={gw} {flag}"

    print("\n=== REFRESH / GATEWAY MATRIX (datasets=ds, dataflows=df) ===")
    print(f"{'workspace':<14} {'T':<2} {'item':<30} {'schedule / last-run':<24} gw   flag")
    for r in sorted(records, key=lambda r: (r["ws"], r["type"], r["name"])):
        print(row(r))

    # ---- summary ----
    nds = sum(1 for r in records if r["type"] == "dataset")
    ndf = sum(1 for r in records if r["type"] == "dataflow")
    gwb = [r for r in records if r["gw_bound"]]
    cloud_only_gw = [r for r in records if r["gw_bound"] and not r["needs_onprem"]]
    proffix = [r for r in records if r["proffix_dbs"]]
    print(f"\nItems: {nds} datasets, {ndf} dataflows. Gateway-bound: {len(gwb)}. "
          f"Touch PROFFIX SQL: {len(proffix)}. ⚠ Cloud-only but GW-bound: {len(cloud_only_gw)}.")
    print("\nScheduled dataset refreshes by hour-of-day (local):")
    sh = Counter();
    for r in records:
        if r["type"] == "dataset" and r.get("sched_enabled"):
            for t in r.get("times", []):
                try: sh[int(t[:2])] += 1
                except Exception: pass
    for h in sorted(sh): print(f"  {h:02d}:00  {'█'*sh[h]} {sh[h]}")
    print("\nPROFFIX-touching items by DB:")
    dbc = Counter()
    for r in proffix:
        for db in r["proffix_dbs"]: dbc[db] += 1
    for db, c in dbc.most_common(): print(f"  {db:<14} {c}")
    if cloud_only_gw:
        print("\n⚠ Cloud-only items pinned to on-prem gateway (candidates to unbind):")
        for r in cloud_only_gw: print(f"  [{r['ws']}] {r['type']} {r['name']}  src={r['src_types']}")


if __name__ == "__main__":
    main()
