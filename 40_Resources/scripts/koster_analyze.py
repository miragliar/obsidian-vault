#!/usr/bin/env python3
"""koster_analyze.py — Live-Bild der Eingangsqueue (read-only)."""
import sys
from collections import Counter

import msal
import requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "9d7f37af-5bc8-4945-a118-98bcf7572346"
DV = "https://org9c15a4d2.api.crm4.dynamics.com"

STATUS = {124080000: "Neu", 124080001: "Verarbeitet",
          124080002: "Fehlgeschlagen", 124080003: "Manuell"}


def _tok(resource):
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache("kosterag"))
    acc = app.get_accounts()
    r = app.acquire_token_silent([f"{resource}/.default"], account=acc[0])
    return r["access_token"]


def dv_get(path):
    tok = _tok(DV)
    r = requests.get(f"{DV}/api/data/v9.2/{path}", headers={
        "Authorization": f"Bearer {tok}", "Accept": "application/json",
        "Prefer": 'odata.include-annotations="*"'}, timeout=120)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:1000]}")
    return r.json().get("value", [])


def main():
    sel = ("ks_eingangsqueueid,ks_eq_attachmentname,ks_eq_dateipfad_manuell,"
           "ks_eq_erkanntals,ks_eq_fehlertext,ks_eq_mailid,ks_eq_status,createdon")
    rows = dv_get(f"ks_eingangsqueues?$select={sel}&$orderby=createdon desc&$top=300")
    print(f"### TOTAL Eingangsqueue-Zeilen: {len(rows)}\n")

    dist = Counter(r.get("ks_eq_status") for r in rows)
    print("### Status-Verteilung:")
    for code, n in sorted(dist.items(), key=lambda x: -x[1]):
        print(f"  {STATUS.get(code, code)} ({code}): {n}")
    print()

    manuell = [r for r in rows if r.get("ks_eq_status") == 124080003]
    print(f"### MANUELL-Einträge: {len(manuell)}\n")
    for r in manuell:
        cd = (r.get("createdon") or "")[:16].replace("T", " ")
        print(f"--- {cd} | erkanntAls={r.get('ks_eq_erkanntals')!r}")
        print(f"    attachmentname = {r.get('ks_eq_attachmentname')!r}")
        print(f"    dateipfad_man  = {r.get('ks_eq_dateipfad_manuell')!r}")
        print(f"    fehlertext     = {r.get('ks_eq_fehlertext')!r}")
        print(f"    mailid         = {(r.get('ks_eq_mailid') or '')[:60]!r}")
        print(f"    id             = {r.get('ks_eingangsqueueid')}")

    # Pfad-Sammlung für SP-Cross-Check
    print("\n### DISTINCT dateipfad_manuell (Manuell):")
    paths = [r.get("ks_eq_dateipfad_manuell") for r in manuell if r.get("ks_eq_dateipfad_manuell")]
    for p in sorted(set(paths)):
        print(f"  {p}")
    dups = [p for p, n in Counter(paths).items() if n > 1]
    if dups:
        print("\n### KOLLIDIERENDE Pfade (mehrfach in Manuell):")
        for p in dups:
            print(f"  ({Counter(paths)[p]}×) {p}")


if __name__ == "__main__":
    main()
