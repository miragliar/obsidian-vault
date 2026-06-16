#!/usr/bin/env python3
"""Rangliste der (externen) Kontakte aus 25_People/-Frontmatter.
Filtert internes Team (team:true) und @miraglia-bi.com raus. Stdlib-only."""
import re, glob, os
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
PEOPLE = VAULT / "25_People"
DONE = {"alessandro@castelli-solutions.ch", "michael@kipfer-dp.com",
        "raoul@miraglia-bi.com", "elvira@miraglia-bi.com"}

rows = []
for p in glob.glob(str(PEOPLE / "*.md")):
    txt = open(p, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    d = {}
    for line in (m.group(1).splitlines() if m else []):
        mm = re.match(r"([a-zA-Z_0-9]+):\s*(.*)", line)
        if mm:
            d[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    d["_name"] = os.path.basename(p)[:-3]
    rows.append(d)

def num(d, k):
    try:
        return float(d.get(k, "") or 0)
    except Exception:
        return 0

def internal(d):
    e = (d.get("email") or "").lower()
    return d.get("team", "").lower() == "true" or e.endswith("@miraglia-bi.com")

cust = [d for d in rows if not internal(d) and (d.get("email") or "").lower() not in DONE]
cust.sort(key=lambda d: (num(d, "interaktionen_12m"), num(d, "interaktionen")), reverse=True)

print(f"{'#':>2} {'name':30} {'email':40} {'12m':>5} {'tot':>5} {'out':>4} {'in':>4} {'status':8} {'client'}")
for i, d in enumerate(cust[:45], 1):
    print(f"{i:2d} {d['_name'][:30]:30} {(d.get('email') or '')[:40]:40} "
          f"{int(num(d,'interaktionen_12m')):5d} {int(num(d,'interaktionen')):5d} "
          f"{int(num(d,'mail_out')):4d} {int(num(d,'mail_in')):4d} "
          f"{(d.get('status') or '')[:8]:8} {d.get('client','')}")
print(f"\n# {len(cust)} externe Kontakte gesamt (ohne Team/Familie & bereits erfasste 4).")
