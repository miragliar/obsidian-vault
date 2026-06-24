#!/usr/bin/env python3
"""koster_xref.py — Cross-Check Manuell-Einträge (Dataverse) vs. echte Dateien (Graph/SharePoint)."""
import sys
from collections import Counter

import msal
import requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "9d7f37af-5bc8-4945-a118-98bcf7572346"
DV = "https://org9c15a4d2.api.crm4.dynamics.com"
GRAPH = "https://graph.microsoft.com/v1.0"
SP_HOSTPATH = "kosterag.sharepoint.com:/sites/Subunternehmer_Produktion"
LIB_PREFIX = "/Freigegebene Dokumente"  # entspricht der Drive-Root


def _app():
    from auth_common import build_pbi_cache
    return msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache("kosterag"))


def _tok(resource):
    app = _app()
    acc = app.get_accounts()
    return app.acquire_token_silent([f"{resource}/.default"], account=acc[0])["access_token"]


def _g(tok, url):
    r = requests.get(url if url.startswith("http") else GRAPH + url,
                     headers={"Authorization": f"Bearer {tok}"}, timeout=60)
    return r


def dv_manuell():
    tok = _tok(DV)
    sel = ("ks_eq_attachmentname,ks_eq_dateipfad_manuell,ks_eq_erkanntals,"
           "ks_eq_mailid,createdon")
    r = requests.get(f"{DV}/api/data/v9.2/ks_eingangsqueues"
                     f"?$select={sel}&$filter=ks_eq_status eq 124080003&$orderby=createdon desc",
                     headers={"Authorization": f"Bearer {tok}", "Accept": "application/json"}, timeout=60)
    r.raise_for_status()
    return r.json()["value"]


def main():
    gtok = _tok("https://graph.microsoft.com")
    site = _g(gtok, f"/sites/{SP_HOSTPATH}?$select=id,name,webUrl").json()
    print(f"# Site: {site.get('name')}  {site.get('webUrl')}")
    drives = _g(gtok, f"/sites/{site['id']}/drives?$select=id,name,webUrl").json()["value"]
    print("# Drives (Bibliotheken):")
    for d in drives:
        print(f"   - {d['name']}  ({d['webUrl']})")
    # Drive der Haupt-Bibliothek
    drive = next((d for d in drives if d["name"] in ("Freigegebene Dokumente", "Dokumente", "Documents")), drives[0])
    did = drive["id"]
    print(f"\n# Verwende Drive: {drive['name']}  id={did}\n")

    # Top-Level
    print("## ROOT-Ordner der Bibliothek:")
    root = _g(gtok, f"/drives/{did}/root/children?$select=name,folder,file,size,lastModifiedDateTime&$top=200").json()
    for it in sorted(root.get("value", []), key=lambda x: x["name"]):
        kind = "DIR " if "folder" in it else "FILE"
        cnt = it.get("folder", {}).get("childCount", "")
        print(f"   [{kind}] {it['name']}  {('items='+str(cnt)) if kind=='DIR ' else str(it.get('size'))+'B'}")

    # 03_Eingang_Temp
    print("\n## 03_Eingang_Temp Inhalt (LIVE):")
    tmp = _g(gtok, f"/drives/{did}/root:/03_Eingang_Temp:/children?$select=name,size,createdDateTime,lastModifiedDateTime&$top=200")
    if tmp.status_code == 404:
        print("   [ORDNER FEHLT]")
        tmpfiles = []
    else:
        tmpfiles = tmp.json().get("value", [])
        for it in sorted(tmpfiles, key=lambda x: x["name"]):
            print(f"   {it['name']}   {it.get('size')}B  mod={it.get('lastModifiedDateTime','')[:16]}")
    print(f"   => {len(tmpfiles)} Datei(en) physisch vorhanden")

    # Cross-Check Manuell-Pfade
    print("\n## CROSS-CHECK: Manuell-dateipfad_manuell vs. physische Datei")
    man = dv_manuell()
    paths = [m.get("ks_eq_dateipfad_manuell") for m in man if m.get("ks_eq_dateipfad_manuell")]
    pc = Counter(paths)
    for p in sorted(set(paths)):
        rel = p[len(LIB_PREFIX):] if p.startswith(LIB_PREFIX) else p
        chk = _g(gtok, f"/drives/{did}/root:{rel}:/?$select=name,size,lastModifiedDateTime")
        if chk.ok:
            j = chk.json()
            state = f"EXISTS {j.get('size')}B mod={j.get('lastModifiedDateTime','')[:16]}"
        elif chk.status_code == 404:
            state = "MISSING"
        else:
            state = f"ERR{chk.status_code}"
        mult = f"  <== {pc[p]}× kollidierend" if pc[p] > 1 else ""
        print(f"   [{state:38}] {rel}{mult}")


if __name__ == "__main__":
    main()
