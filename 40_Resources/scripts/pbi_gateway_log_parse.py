#!/usr/bin/env python3
"""
pbi_gateway_log_parse.py — Parse an On-premises Data Gateway *QueryExecutionReport*
CSV to attribute SQL load by database and time, for correlating gateway refresh
activity with an on-prem SQL blocking incident.

The report's timestamps are UTC. --tz prints a local column (e.g. 2 = CEST).
Each row has QueryExecutionEndTimeUTC + QueryExecutionDuration(ms), so the active
interval is reconstructed as [end-duration, end].

Usage:
  ./.venv/bin/python pbi_gateway_log_parse.py \
      --file /tmp/odg/QueryExecutionReport_*.log \
      --date 2026-06-05 --from 07:00 --to 08:30 --tz 2
"""
import argparse, csv, re, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ap = argparse.ArgumentParser()
ap.add_argument("--file", required=True)
ap.add_argument("--date", required=True, help="UTC date YYYY-MM-DD")
ap.add_argument("--from", dest="f", default="00:00", help="window start UTC HH:MM")
ap.add_argument("--to", dest="t", default="23:59", help="window end UTC HH:MM")
ap.add_argument("--tz", type=int, default=2, help="local offset hours for display (CEST=2)")
a = ap.parse_args()

day = datetime.strptime(a.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
wf = day + timedelta(hours=int(a.f[:2]), minutes=int(a.f[3:5]))
wt = day + timedelta(hours=int(a.t[:2]), minutes=int(a.t[3:5]))
TZ = timezone(timedelta(hours=a.tz))
csv.field_size_limit(10_000_000)


def ptime(s):
    s = s.strip().replace("Z", "")
    s = re.sub(r"(\.\d{6})\d*", r"\1", s)
    try:
        return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def db_of(datasource):
    m = re.search(r"proffix;([A-Za-z0-9_]+)", datasource)
    if m:
        return m.group(1).upper()
    if '\\"kind\\":\\"SQL' in datasource or '"kind":"SQL' in datasource:
        return "SQL(other)"
    return None  # non-SQL (dataflow/file/powerbi)


buckets = defaultdict(lambda: defaultdict(int))   # 5min -> db -> count
win_db = defaultdict(lambda: [0, 0, 0])           # db -> [count, total_ms, fails]
shg_times = []
total_in_win = 0

with open(a.file, newline="") as fh:
    r = csv.reader(fh)
    head = next(r)
    iEnd = head.index("QueryExecutionEndTimeUTC")
    iDur = head.index("QueryExecutionDuration(ms)")
    iSrc = head.index("DataSource")
    iOk = head.index("Success")
    for row in r:
        if len(row) <= iOk:
            continue
        end = ptime(row[iEnd])
        if not end:
            continue
        try:
            dur = int(row[iDur]) if row[iDur].strip() else 0
        except ValueError:
            dur = 0
        start = end - timedelta(milliseconds=dur)
        # active interval overlaps window?
        if start > wt or end < wf:
            continue
        total_in_win += 1
        db = db_of(row[iSrc]) or "non-SQL"
        b = end.replace(second=0, microsecond=0, minute=(end.minute // 5) * 5)
        buckets[b][db] += 1
        win_db[db][0] += 1
        win_db[db][1] += dur
        if row[iOk].strip().upper() != "Y":
            win_db[db][2] += 1
        if db == "PXSHARKGROUP":
            shg_times.append((start, end, dur, row[iOk].strip()))

def cest(dt): return dt.astimezone(TZ).strftime("%H:%M")

print(f"\n=== Gateway SQL queries active in window {a.date} {a.f}-{a.t} UTC "
      f"({cest(wf)}-{cest(wt)} CEST) ===  total={total_in_win}\n")

print("Per database (active in window):")
for db, (c, ms, fails) in sorted(win_db.items(), key=lambda x: -x[1][0]):
    print(f"  {db:<16} queries={c:<6} total={ms/1000:8.1f}s  avg={ms/max(c,1):7.0f}ms  fails={fails}")

print("\nPer 5-min bucket (queries ending; UTC / CEST):  total  [PXSHARKGROUP]  top-other-DB")
for b in sorted(buckets):
    dbs = buckets[b]
    tot = sum(dbs.values())
    shg = dbs.get("PXSHARKGROUP", 0)
    others = {k: v for k, v in dbs.items() if k != "PXSHARKGROUP"}
    top = max(others.items(), key=lambda x: x[1]) if others else ("-", 0)
    bar = "#" * min(tot, 60)
    print(f"  {b.strftime('%H:%M')}Z /{cest(b)}  {tot:4d}  shg={shg:3d}  {top[0]}={top[1]:<4}  {bar}")

if shg_times:
    print(f"\nPXSHARKGROUP queries in window: {len(shg_times)}")
    print(f"  first start {cest(min(s for s,_,_,_ in shg_times))} CEST, "
          f"last end {cest(max(e for _,e,_,_ in shg_times))} CEST")
    longest = sorted(shg_times, key=lambda x: -x[2])[:5]
    print("  longest pxsharkgroup queries (CEST start–end, dur):")
    for s, e, d, ok in longest:
        print(f"    {cest(s)}–{cest(e)}  {d/1000:6.1f}s  ok={ok}")
