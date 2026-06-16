#!/usr/bin/env python3
"""
pbi_item_history.py — READ-ONLY: dump the full refresh history of dataset(s) whose
name matches a substring, across all workspaces, for a date range. For pinning down
the exact refresh cadence of a suspect dataset during an incident.

Usage:
  ./.venv/bin/python pbi_item_history.py --tenant <t> --name "offene Debitoren" \
      --from 2026-06-03T00:00:00Z --to 2026-06-06T00:00:00Z
"""
import argparse, os, re, sys
from datetime import datetime, timedelta, timezone
import msal, requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"
CEST = timezone(timedelta(hours=2))


def token(tenant):
    # Token-Cache im macOS Keychain (verschlüsselt, kein Dropbox-Sync) — via auth_common.
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(CID, authority=f"https://login.microsoftonline.com/{tenant}", token_cache=build_pbi_cache(tenant))
    acc = app.get_accounts()
    r = app.acquire_token_silent(SCOPE, account=acc[0]) if acc else None
    if not r:
        fl = app.initiate_device_flow(scopes=SCOPE); print(fl["message"], file=sys.stderr)
        r = app.acquire_token_by_device_flow(fl)
    return r["access_token"]


def pdt(s):
    if not s: return None
    s = s.replace("Z", "+00:00"); s = re.sub(r"(\.\d{6})\d+", r"\1", s)
    try: d = datetime.fromisoformat(s)
    except ValueError: return None
    return d.astimezone(timezone.utc)


a = argparse.ArgumentParser()
a.add_argument("--tenant", required=True); a.add_argument("--name", required=True)
a.add_argument("--from", dest="f", required=True); a.add_argument("--to", dest="t", required=True)
a.add_argument("--top", type=int, default=500)
args = a.parse_args()
wf, wt = pdt(args.f), pdt(args.t)

s = requests.Session(); s.headers["Authorization"] = f"Bearer {token(args.tenant)}"
g = lambda u: (s.get(u if u.startswith("http") else BASE + u, timeout=60).json() or {}).get("value", [])

for grp in g("/groups"):
    gid, gn = grp["id"], grp.get("name", "?")
    for d in g(f"/groups/{gid}/datasets"):
        if args.name.lower() not in d.get("name", "").lower(): continue
        rows = g(f"/groups/{gid}/datasets/{d['id']}/refreshes?$top={args.top}")
        inwin = [r for r in rows if (pdt(r.get("startTime")) and wf <= pdt(r["startTime"]) <= wt)]
        if not inwin: continue
        print(f"\n=== {d['name']}  (workspace: {gn})  — {len(inwin)} run(s) in range ===")
        for r in sorted(inwin, key=lambda r: r["startTime"]):
            st, en = pdt(r.get("startTime")), pdt(r.get("endTime"))
            wd = st.astimezone(CEST).strftime("%a")
            dur = f"{(en-st).total_seconds():.0f}s" if en else "—"
            print(f"  {wd} {st.astimezone(CEST):%Y-%m-%d %H:%M:%S} CEST  dur={dur:>5}  {r.get('status'):<10} {r.get('refreshType')}")
