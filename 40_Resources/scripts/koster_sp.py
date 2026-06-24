#!/usr/bin/env python3
"""koster_sp.py — Read-only SharePoint-Listing (Subunternehmer_Produktion)."""
import sys

import msal
import requests

CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
TENANT = "9d7f37af-5bc8-4945-a118-98bcf7572346"
HOST = "kosterag.sharepoint.com"
SITE = "/sites/Subunternehmer_Produktion"
BASE = f"https://{HOST}{SITE}"


def _tok():
    from auth_common import build_pbi_cache
    app = msal.PublicClientApplication(
        CID, authority=f"https://login.microsoftonline.com/{TENANT}",
        token_cache=build_pbi_cache("kosterag"))
    acc = app.get_accounts()
    r = app.acquire_token_silent([f"https://{HOST}/.default"], account=acc[0])
    return r["access_token"]


def _h(tok):
    return {"Authorization": f"Bearer {tok}", "Accept": "application/json;odata=nometadata"}


def _srv(path):
    """Site-relativ (/Freigegebene Dokumente/...) -> server-relativ (/sites/.../...)."""
    if path.startswith(SITE):
        return path
    return SITE + "/" + path.lstrip("/")


def ls(path):
    tok = _tok()
    srv = _srv(path)
    print(f"# {srv}")
    fr = requests.get(f"{BASE}/_api/web/GetFolderByServerRelativeUrl('{srv}')/Folders",
                      headers=_h(tok), timeout=60)
    if fr.status_code == 404:
        print("  [FOLDER NOT FOUND]")
        return
    if not fr.ok:
        sys.exit(f"HTTP {fr.status_code}: {fr.text[:600]}")
    for f in fr.json().get("value", []):
        if f["Name"] in ("Forms",):
            continue
        print(f"  [DIR ] {f['Name']}/   (items={f.get('ItemCount')})")
    xr = requests.get(
        f"{BASE}/_api/web/GetFolderByServerRelativeUrl('{srv}')/Files"
        "?$select=Name,Length,TimeCreated,TimeLastModified",
        headers=_h(tok), timeout=60)
    for f in xr.json().get("value", []):
        kb = int(f.get("Length", 0)) / 1024
        print(f"  [FILE] {f['Name']}   {kb:8.1f} KB   created={f.get('TimeCreated','')[:16]}  mod={f.get('TimeLastModified','')[:16]}")


def exists(paths):
    """Prüft eine Liste site-relativer Pfade auf Existenz."""
    tok = _tok()
    for p in paths:
        srv = _srv(p)
        r = requests.get(
            f"{BASE}/_api/web/GetFileByServerRelativeUrl('{srv}')"
            "?$select=Name,Length,TimeCreated,TimeLastModified",
            headers=_h(tok), timeout=60)
        if r.ok:
            j = r.json()
            kb = int(j.get("Length", 0)) / 1024
            print(f"  EXISTS  {kb:8.1f}KB  mod={j.get('TimeLastModified','')[:16]}  {p}")
        elif r.status_code == 404:
            print(f"  MISSING ----      ----              {p}")
        else:
            print(f"  ERR{r.status_code}  {p}: {r.text[:120]}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ls"
    if cmd == "ls":
        ls(sys.argv[2] if len(sys.argv) > 2 else "/Freigegebene Dokumente")
    elif cmd == "exists":
        exists([l.strip() for l in sys.stdin if l.strip()])
