#!/usr/bin/env python3
"""
pbi_refresh_probe.py — READ-ONLY Power BI refresh/gateway forensics for a CLIENT tenant.

Purpose
-------
Correlate Power BI dataset/dataflow refreshes with on-prem SQL load (e.g. a PROFFIX
"blocked SQL sessions" incident). Given a time window, it lists every dataset refresh
and dataflow transaction that OVERLAPS that window, plus the gateway + datasource
(server / database) each one uses — so you can see which refresh hammered which DB.

Auth
----
Delegated **device-code** login (the user signs in interactively in a browser).
Read-only Power BI scope. Token is cached locally so repeat runs don't re-prompt.
No secret is stored. Nothing is ever written/changed in the tenant.

Usage
-----
  ./.venv/bin/python pbi_refresh_probe.py \
      --tenant directhandlingch.onmicrosoft.com \
      --from 2026-06-05T07:00:00Z --to 2026-06-05T08:30:00Z \
      [--db PXSHARKGROUP] [--server SHAR-SRV-10] \
      [--workspace Shark]        # substring filter on workspace name (repeatable)
      [--top 30]                 # refresh-history depth per dataset
      [--client-id <appId>]      # override public client (default: Azure CLI)
      [--json out.json]

Times: pass --from/--to in UTC (trailing Z). Swiss summer time (CEST) = UTC+2,
so 09:40–10:00 CEST == 07:40–08:00 UTC. Output shows both UTC and CEST.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import msal
import requests

# Azure CLI public client — Microsoft-owned, multi-tenant, pre-authorized for many
# first-party resources incl. Power BI. No app registration needed in most tenants.
DEFAULT_CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
PBI_SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"
CEST = timezone(timedelta(hours=2))  # Switzerland, June (summer time)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ----------------------------- auth -----------------------------------------
def get_token(tenant, client_id):
    # Token-Cache im macOS Keychain (verschlüsselt, kein Dropbox-Sync) — via auth_common.
    from auth_common import build_pbi_cache

    app = msal.PublicClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant}",
        token_cache=build_pbi_cache(tenant),
    )

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(PBI_SCOPE, account=accounts[0])

    if not result:
        flow = app.initiate_device_flow(scopes=PBI_SCOPE)
        if "user_code" not in flow:
            raise SystemExit(f"Device flow failed: {json.dumps(flow, indent=2)}")
        log("\n================ SIGN IN REQUIRED ================")
        log(flow["message"])  # "go to https://microsoft.com/devicelogin and enter CODE"
        log("Sign in as the CLIENT Power BI account (e.g. powerbi@directhandlingch.onmicrosoft.com).")
        log("=================================================\n")
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise SystemExit(
            f"Auth failed: {result.get('error')} — {result.get('error_description')}"
        )
    return result["access_token"]


# ----------------------------- http -----------------------------------------
class Api:
    def __init__(self, token):
        self.s = requests.Session()
        self.s.headers["Authorization"] = f"Bearer {token}"

    def get(self, url):
        """GET with light 429 backoff. Returns parsed JSON, or None on 4xx (skipped)."""
        full = url if url.startswith("http") else BASE + url
        for attempt in range(4):
            r = self.s.get(full, timeout=60)
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 20))
                log(f"  throttled (429), waiting {wait}s…")
                time.sleep(wait)
                continue
            if r.status_code == 401:
                raise SystemExit("401 Unauthorized — token rejected for this tenant.")
            if r.status_code >= 400:
                return None  # endpoint not supported for this item / no perms → skip
            return r.json()
        return None

    def value(self, url):
        j = self.get(url)
        return (j or {}).get("value", []) if j else []


# ----------------------------- time helpers ---------------------------------
def parse_dt(s):
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    # trim fractional seconds to 6 digits (PBI sometimes returns 7)
    m = re.match(r"(.*\.\d{6})\d*(\+\d{2}:\d{2})$", s)
    if m:
        s = m.group(1) + m.group(2)
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def fmt(dt):
    if not dt:
        return "—"
    return f"{dt.strftime('%H:%M:%S')}Z / {dt.astimezone(CEST).strftime('%H:%M:%S')} CEST"


def overlaps(start, end, win_from, win_to):
    """True if [start,end] intersects [win_from,win_to]. Open end = still running."""
    if start is None:
        return False
    if start > win_to:
        return False
    if end is None:  # in progress
        return True
    return end >= win_from


# ----------------------------- datasource fmt -------------------------------
def ds_summary(api, kind, gid, item_id, gw_names):
    """Return list of 'server/database (gateway)' strings for a dataset/dataflow."""
    path = (
        f"/groups/{gid}/datasets/{item_id}/datasources"
        if kind == "dataset"
        else f"/groups/{gid}/dataflows/{item_id}/datasources"
    )
    out = []
    for d in api.value(path):
        cd = d.get("connectionDetails", {}) or {}
        server = cd.get("server") or cd.get("url") or cd.get("path") or ""
        db = cd.get("database") or ""
        gw = d.get("gatewayId") or ""
        gwn = gw_names.get(gw, gw[:8] if gw else "—")
        dtype = d.get("datasourceType", "")
        out.append(
            {
                "type": dtype,
                "server": server,
                "database": db,
                "gateway": gwn,
                "raw": cd,
            }
        )
    return out


# ----------------------------- main -----------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tenant", required=True)
    ap.add_argument("--from", dest="w_from", required=True, help="window start, UTC ISO (…Z)")
    ap.add_argument("--to", dest="w_to", required=True, help="window end, UTC ISO (…Z)")
    ap.add_argument("--db", default=None, help="highlight datasources whose database matches (substring, ci)")
    ap.add_argument("--server", default=None, help="highlight datasources whose server matches (substring, ci)")
    ap.add_argument("--workspace", action="append", default=[], help="only scan workspaces whose name contains this (repeatable)")
    ap.add_argument("--top", type=int, default=30, help="refresh-history depth per dataset")
    ap.add_argument("--client-id", default=DEFAULT_CLIENT_ID)
    ap.add_argument("--json", default=None, help="write full machine-readable results here")
    args = ap.parse_args()

    win_from = parse_dt(args.w_from)
    win_to = parse_dt(args.w_to)
    if not win_from or not win_to:
        raise SystemExit("Could not parse --from/--to (use UTC ISO like 2026-06-05T07:00:00Z)")

    log(f"Window: {win_from.isoformat()} … {win_to.isoformat()} (UTC)")
    log(f"      = {win_from.astimezone(CEST).strftime('%Y-%m-%d %H:%M')} … {win_to.astimezone(CEST).strftime('%H:%M')} CEST")

    token = get_token(args.tenant, args.client_id)
    api = Api(token)

    # gateway id -> name (best effort; needs gateway perms)
    gw_names = {}
    for g in api.value("/gateways"):
        gw_names[g.get("id")] = g.get("name", g.get("id"))
    if gw_names:
        log(f"Gateways visible: {', '.join(sorted(gw_names.values()))}")

    groups = api.value("/groups")
    if args.workspace:
        wl = [w.lower() for w in args.workspace]
        groups = [g for g in groups if any(w in (g.get("name", "").lower()) for w in wl)]
    log(f"Scanning {len(groups)} workspace(s)…")
    if not groups:
        log("No workspaces visible to this account. It may need to be added as a "
            "workspace member/admin, or use a Fabric/PBI admin account for tenant-wide scan.")

    matches = []

    def hit(db, server):
        f = []
        if args.db and db and args.db.lower() in db.lower():
            f.append("DB")
        if args.server and server and args.server.lower() in server.lower():
            f.append("SERVER")
        return f

    for gi, g in enumerate(groups, 1):
        gid, gname = g.get("id"), g.get("name", "?")
        log(f"[{gi}/{len(groups)}] {gname}")

        # ---- datasets ----
        for d in api.value(f"/groups/{gid}/datasets"):
            did, dname = d.get("id"), d.get("name", "?")
            refreshes = api.value(f"/groups/{gid}/datasets/{did}/refreshes?$top={args.top}")
            wins = [
                r for r in refreshes
                if overlaps(parse_dt(r.get("startTime")), parse_dt(r.get("endTime")), win_from, win_to)
            ]
            if not wins:
                continue
            sources = ds_summary(api, "dataset", gid, did, gw_names)
            for r in wins:
                matches.append({
                    "workspace": gname, "kind": "dataset", "name": dname,
                    "start": parse_dt(r.get("startTime")), "end": parse_dt(r.get("endTime")),
                    "status": r.get("status"), "refreshType": r.get("refreshType"),
                    "sources": sources,
                })

        # ---- dataflows ----
        for f in api.value(f"/groups/{gid}/dataflows"):
            fid, fname = f.get("objectId"), f.get("name", "?")
            txns = api.value(f"/groups/{gid}/dataflows/{fid}/transactions")
            wins = [
                t for t in txns
                if overlaps(parse_dt(t.get("startTime")), parse_dt(t.get("endTime")), win_from, win_to)
            ]
            if not wins:
                continue
            sources = ds_summary(api, "dataflow", gid, fid, gw_names)
            for t in wins:
                matches.append({
                    "workspace": gname, "kind": "dataflow", "name": fname,
                    "start": parse_dt(t.get("startTime")), "end": parse_dt(t.get("endTime")),
                    "status": t.get("status"), "refreshType": t.get("refreshType"),
                    "sources": sources,
                })

    matches.sort(key=lambda m: (m["start"] or win_from))

    # ----------------------------- report -----------------------------------
    print("\n" + "=" * 78)
    print(f"REFRESHES OVERLAPPING {win_from.astimezone(CEST):%Y-%m-%d %H:%M}–{win_to.astimezone(CEST):%H:%M} CEST "
          f"({win_from:%H:%M}–{win_to:%H:%M} UTC)")
    print("=" * 78)
    if not matches:
        print("\nNo dataset/dataflow refresh overlaps this window in the visible workspaces.")
    for m in matches:
        flagged = []
        for s in m["sources"]:
            flagged += hit(s["database"], s["server"])
        mark = "  <<< MATCHES TARGET DB/SERVER" if flagged else ""
        print(f"\n• [{m['kind']}] {m['name']}  —  workspace: {m['workspace']}{mark}")
        print(f"    start {fmt(m['start'])}")
        print(f"    end   {fmt(m['end'])}   status={m['status']}  type={m['refreshType']}")
        for s in m["sources"]:
            tag = "  *" if hit(s["database"], s["server"]) else ""
            print(f"    src: {s['type']:<12} server={s['server'] or '—'}  db={s['database'] or '—'}  gateway={s['gateway']}{tag}")

    print("\n" + "-" * 78)
    print(f"{len(matches)} overlapping refresh(es). "
          f"Targets: db~'{args.db}' server~'{args.server}'.")

    if args.json:
        ser = []
        for m in matches:
            mm = dict(m)
            mm["start"] = m["start"].isoformat() if m["start"] else None
            mm["end"] = m["end"].isoformat() if m["end"] else None
            ser.append(mm)
        with open(args.json, "w") as fh:
            json.dump({"window": [win_from.isoformat(), win_to.isoformat()], "matches": ser}, fh, indent=2, default=str)
        log(f"Wrote {args.json}")


if __name__ == "__main__":
    main()
