#!/usr/bin/env python3
"""READ-ONLY: dump the DocumentItems query M from the Green 'AllTablesDailyTps Green'
dataflow to confirm AboStart/AboEnd logic + whether DateEarliestTermination is in output."""
import sys, json
import msal, requests
from auth_common import build_pbi_cache

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"
TENANT = "green.ch"
WS = "6868e26d-9361-498f-9d49-af4f21f8031e"     # Dataflow Premium
DF = "13a57d23-ebbc-44c4-afc7-3e571d52c807"     # AllTablesDailyTps Green (has DateLogicFlag)

app = msal.PublicClientApplication(CID, authority=f"https://login.microsoftonline.com/{TENANT}",
                                   token_cache=build_pbi_cache(TENANT))
acc = app.get_accounts()
r = app.acquire_token_silent(SCOPE, account=acc[0]) if acc else None
if not r:
    print("NO_CACHED_TOKEN — bitte erneut interaktiv anmelden"); sys.exit(1)
s = requests.Session(); s.headers["Authorization"] = f"Bearer {r['access_token']}"

d = s.get(f"{BASE}/groups/{WS}/dataflows/{DF}", timeout=180)
print("HTTP", d.status_code, "| size", len(d.content), "bytes")
j = d.json()
print("TOP-LEVEL KEYS:", list(j.keys()))
ents = [e.get("name") for e in j.get("entities", [])]
print(f"\nENTITIES ({len(ents)}):", ents)

mashup = (j.get("pbi:mashup") or {}).get("document", "") or ""
print("\nMASHUP M length:", len(mashup))

# Isolate the DocumentItems shared query
key = "shared DocumentItems"
i = mashup.find(key)
block = ""
if i >= 0:
    # next 'shared ' at line start after this one delimits the query
    nxt = mashup.find("\nshared ", i + len(key))
    block = mashup[i: nxt if nxt > 0 else i + 12000]
print(f"\nDocumentItems block found: {i >= 0} | length: {len(block)}")

KWS = ["DateEarliestTermination", "AboEndCorrected", "DateLogicFlag", "AboEndeffective",
       "AboEnd", "AboStart", "ContractEnd", "ContractStart", "BillingEnd", "BillingStart"]
print("\n=== Vorkommen (im DocumentItems-Block | im ganzen Dataflow-M) ===")
for kw in KWS:
    print(f"  {kw:28s}  block={kw in block!s:5s}  | M={kw in mashup}")

print("\n=== DocumentItems-Block (Schritt-Zeilen mit Datums-Logik) ===")
for ln in block.splitlines():
    if any(k in ln for k in ["AboEnd", "AboStart", "DateLogicFlag", "DateEarliestTermination",
                              "ContractEnd", "BillingEnd", "Merge", "Documents", "Expand"]):
        print("  ", ln.strip()[:200])
