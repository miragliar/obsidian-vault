#!/usr/bin/env python3
"""
pbi_querystart_attribute.py — Attribute on-prem gateway SQL queries to the Power BI
DATASET that issued them, by decoding the QueryStartReport's EvaluationContext
(carries DatasetId / WorkspaceId). For "which report caused the load at HH:MM?".

Times in the report are UTC. --tz prints local (CEST=2). Optionally pass an
inventory JSON (--names) to resolve DatasetId -> dataset name.

Usage:
  ./.venv/bin/python pbi_querystart_attribute.py \
     --files /tmp/odg/QueryStartReport_*.log \
     --date 2026-06-05 --windows 07:05-07:14 07:28-07:42 --db pxsharkgroup --tz 2 \
     --names /tmp/pbi_inventory.json
"""
import argparse, csv, json, re, sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone

ap = argparse.ArgumentParser()
ap.add_argument("--files", nargs="+", required=True)
ap.add_argument("--date", required=True)
ap.add_argument("--windows", nargs="+", required=True, help="UTC HH:MM-HH:MM ...")
ap.add_argument("--db", default=None, help="substring filter on DataSource (e.g. pxsharkgroup)")
ap.add_argument("--tz", type=int, default=2)
ap.add_argument("--names", default=None, help="inventory JSON with ds_id_name map")
a = ap.parse_args()

TZ = timezone(timedelta(hours=a.tz))
csv.field_size_limit(20_000_000)
day = datetime.strptime(a.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
wins = []
for w in a.windows:
    f, t = w.split("-")
    wins.append((w,
                 day + timedelta(hours=int(f[:2]), minutes=int(f[3:5])),
                 day + timedelta(hours=int(t[:2]), minutes=int(t[3:5]))))

names = {}
if a.names:
    try: names = json.load(open(a.names)).get("ds_id_name", {})
    except Exception as e: print(f"(names load failed: {e})", file=sys.stderr)

def ptime(s):
    s = s.strip().replace("Z", ""); s = re.sub(r"(\.\d{6})\d*", r"\1", s)
    try: return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    except ValueError: return None

def ctx_ids(s):
    did = wid = None
    try:
        j = json.loads(s)
        for c in j.get("serviceTraceContexts", []):
            for tr in c.get("traceIds", []):
                if tr.get("key") == "DatasetId": did = tr.get("value")
                if tr.get("key") == "WorkspaceId": wid = tr.get("value")
    except Exception:
        m = re.search(r'DatasetId"?,"?value"?:"?([0-9A-Fa-f-]{36})', s)
        if m: did = m.group(1)
    return (did or "").lower(), (wid or "").lower()

# window -> dataset -> count ; window -> dbset
tally = {w[0]: Counter() for w in wins}
dbs = {w[0]: Counter() for w in wins}
for path in a.files:
    try: fh = open(path, newline="")
    except FileNotFoundError: continue
    r = csv.reader(fh)
    head = next(r)
    iSrc, iStart, iCtx = head.index("DataSource"), head.index("QueryExecutionStartTimeUTC"), head.index("EvaluationContext")
    for row in r:
        if len(row) <= iCtx: continue
        if a.db and a.db.lower() not in row[iSrc].lower(): continue
        st = ptime(row[iStart])
        if not st: continue
        for wname, wf, wt in wins:
            if wf <= st <= wt:
                did, wid = ctx_ids(row[iCtx])
                tally[wname][did] += 1
                m = re.search(r"proffix;([A-Za-z0-9_]+)", row[iSrc])
                if m: dbs[wname][m.group(1).upper()] += 1
                break
    fh.close()

print(f"\nAttribution for {a.date}  (db filter: {a.db or 'ALL'})  times CEST=UTC+{a.tz}\n")
for wname, wf, wt in wins:
    lo, hi = wf.astimezone(TZ).strftime("%H:%M"), wt.astimezone(TZ).strftime("%H:%M")
    total = sum(tally[wname].values())
    print(f"=== window {wname} UTC = {lo}-{hi} CEST — {total} SQL queries ===")
    print(f"    DBs: {dict(dbs[wname])}")
    for did, c in tally[wname].most_common(12):
        nm = names.get(did, "(unknown dataset)")
        print(f"    {c:4d}  {nm[:40]:<40} {did}")
    print()
