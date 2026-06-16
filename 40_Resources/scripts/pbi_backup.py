#!/usr/bin/env python3
"""
pbi_backup.py — Backup von Power BI Inhalten pro Workspace.

Lädt über die REST-API "Export Report In Group" alle Reports als **.pbix**
herunter (bei Import-Modellen inkl. semantischem Modell + Daten) und exportiert
zusätzlich die **Dataflow-Definitionen** (model.json mit den Power-Query/M-Schritten).
Jeder Lauf erzeugt einen versionierten Schnappschuss (Zeitstempel-Ordner) plus ein
Manifest (JSON), das pro Element Workspace, Report/Dataflow, Dataset, Größe, Status
und ggf. Fehler dokumentiert.

Hintergrund (Anlass): Lädt jemand einen *verlinkten* Thin-Report herunter und
publiziert ihn wieder, kann das geteilte semantische Modell durch eine datenlose
Kopie überschrieben werden. Ein regelmäßiger .pbix-Export im Service ist die
Versicherung dagegen — man kann jederzeit eine intakte Datei zurückspielen.

Auth: Device-Code (bzw. gecachter Token) pro Tenant; Token im macOS Keychain (auth_common.build_pbi_cache).
Bei langen Läufen wird das Access-Token periodisch + bei 401/403 automatisch erneuert (TokenManager).
NUR LESEND gegenüber Power BI (Export-GETs) — es wird NICHTS überschrieben/gelöscht.

Usage:
  # 1) Workspaces + Reports/Dataflows nur auflisten (keine Downloads):
  ./.venv/bin/python pbi_backup.py --tenant telama.onmicrosoft.com --list

  # 2) Backup eines Workspaces (Substring-Filter, case-insensitive):
  ./.venv/bin/python pbi_backup.py --tenant telama.onmicrosoft.com --workspace "Cockpit MM"

  # 3) Backup ALLER Workspaces des Tenants:
  ./.venv/bin/python pbi_backup.py --tenant telama.onmicrosoft.com --all

Zielordner (Default): ~/PowerBI-Backups/<tenant>/<YYYY-MM-DD-HH-MM>/<workspace>/
Mit --out <pfad> landet der datierte Ordner direkt unter <pfad> — z. B.
--out ".../<Kunde>/Sicherungen" für die bestehende PowerShell-Backup-Struktur.
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import msal
import requests

# Microsoft "Azure CLI" Public Client — wie in den übrigen pbi_*-Skripten.
CID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]
BASE = "https://api.powerbi.com/v1.0/myorg"


def log(*a):
    print(*a, file=sys.stderr, flush=True)


class TokenManager:
    """Hält ein gültiges Access-Token und erneuert es bei Bedarf. Gegen Token-Ablauf
    bei langen Läufen (vorher: 1 Token am Anfang -> 403 TokenExpired gegen Ende):
    proaktiv alle REFRESH_AFTER Sekunden + reaktiv bei 401/403 (force_refresh).
    acquire_token_silent nutzt den Refresh-Token im Keychain — i. d. R. ohne neuen Login."""
    REFRESH_AFTER = 40 * 60  # vor dem üblichen 60–90-min-Ablauf erneuern

    def __init__(self, tenant):
        # Token-Cache im macOS Keychain (verschlüsselt, kein Dropbox-Sync) — via auth_common.
        from auth_common import build_pbi_cache
        self.app = msal.PublicClientApplication(
            CID, authority=f"https://login.microsoftonline.com/{tenant}",
            token_cache=build_pbi_cache(tenant))
        self._tok = None
        self._ts = 0.0

    def _acquire(self, force=False):
        acc = self.app.get_accounts()
        r = self.app.acquire_token_silent(SCOPE, account=acc[0], force_refresh=force) if acc else None
        if not r:
            fl = self.app.initiate_device_flow(scopes=SCOPE)
            if "user_code" not in fl:
                sys.exit(f"Device-Flow fehlgeschlagen: {fl.get('error_description')}")
            log("\n" + "=" * 64 + f"\n{fl['message']}\n" + "=" * 64 + "\n")
            r = self.app.acquire_token_by_device_flow(fl)
        if not r or "access_token" not in r:
            sys.exit(f"Token-Erwerb fehlgeschlagen: {r}")
        return r["access_token"]

    def token(self, force=False):
        if force or self._tok is None or (time.time() - self._ts) > self.REFRESH_AFTER:
            first = self._tok is None
            self._tok = self._acquire(force=force)
            self._ts = time.time()
            if not first:
                log("   ↻ Access-Token erneuert")
        return self._tok


def safe(name):
    """Dateisystem-sicherer Name."""
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name or "").strip().rstrip(".")
    return name or "unnamed"


class Api:
    def __init__(self, tm):
        self.tm = tm                       # TokenManager (periodischer + reaktiver Refresh)
        self.s = requests.Session()

    def _auth(self, force=False):
        self.s.headers["Authorization"] = f"Bearer {self.tm.token(force=force)}"

    def get_json(self, path):
        self._auth()
        refreshed = False
        for _ in range(5):
            r = self.s.get(BASE + path, timeout=120)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 20)))
                continue
            if r.status_code in (401, 403) and not refreshed:
                self._auth(force=True)
                refreshed = True
                continue
            if r.status_code >= 400:
                return None
            return r.json()
        return None

    def value(self, path):
        j = self.get_json(path)
        return (j or {}).get("value", []) if j else []

    def export_bytes(self, path, timeout=600):
        """GET, der eine Datei (bytes) zurückgibt. Rückgabe: (bytes, None) | (None, fehler)."""
        self._auth()
        refreshed = False
        for _ in range(5):
            r = self.s.get(BASE + path, timeout=timeout)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 30)))
                continue
            if r.status_code in (401, 403) and not refreshed:
                self._auth(force=True)
                refreshed = True
                continue
            if r.status_code == 200:
                return r.content, None
            try:
                msg = (r.json().get("error", {}) or {}).get("code") or r.text[:200]
            except Exception:
                msg = r.text[:200]
            return None, f"HTTP {r.status_code}: {msg}"
        return None, "429 (zu viele Versuche)"


def list_tenant(api, groups):
    for g in sorted(groups, key=lambda g: g.get("name", "")):
        gid, gn = g["id"], g.get("name", "?")
        reports = api.value(f"/groups/{gid}/reports")
        datasets = {d["id"]: d.get("name", "?") for d in api.value(f"/groups/{gid}/datasets")}
        dataflows = api.value(f"/groups/{gid}/dataflows")
        print(f"\n📁 {gn}   (id={gid})")
        print(f"   Reports: {len(reports)} · Datasets: {len(datasets)} · Dataflows: {len(dataflows)}")
        for r in sorted(reports, key=lambda r: r.get("name", "")):
            ds = datasets.get(r.get("datasetId"), r.get("datasetId") or "—")
            print(f"   • [report]   {r.get('name','?'):<42} → modell: {ds}")
        for f in sorted(dataflows, key=lambda f: f.get("name", "")):
            print(f"   • [dataflow] {f.get('name','?')}")


def backup(api, groups, out, stamp):
    root = Path(out) / safe(stamp)
    manifest = {"stamp": stamp, "generated": datetime.now().isoformat(timespec="seconds"),
                "items": []}
    n_ok = n_err = 0
    total = 0
    for g in sorted(groups, key=lambda g: g.get("name", "")):
        gid, gn = g["id"], g.get("name", "?")
        reports = api.value(f"/groups/{gid}/reports")
        datasets = {d["id"]: d.get("name", "?") for d in api.value(f"/groups/{gid}/datasets")}
        dataflows = api.value(f"/groups/{gid}/dataflows")
        if not reports and not dataflows:
            continue
        wsdir = root / safe(gn)
        wsdir.mkdir(parents=True, exist_ok=True)
        log(f"\n📁 {gn} — {len(reports)} Report(s), {len(dataflows)} Dataflow(s)")

        # --- Reports als .pbix ---
        for r in sorted(reports, key=lambda r: r.get("name", "")):
            rid, rn = r["id"], r.get("name", "?")
            content, err = api.export_bytes(f"/groups/{gid}/reports/{rid}/Export")
            rec = {"workspace": gn, "type": "report", "name": rn, "id": rid,
                   "datasetId": r.get("datasetId"),
                   "dataset": datasets.get(r.get("datasetId"))}
            if err:
                rec["status"], rec["error"] = "FEHLER", err
                n_err += 1
                log(f"   ✗ [report]   {rn}  → {err}")
            else:
                fp = wsdir / f"{safe(rn)}.pbix"
                fp.write_bytes(content)
                rec["status"], rec["file"], rec["bytes"] = "OK", str(fp), len(content)
                n_ok += 1
                total += len(content)
                log(f"   ✓ [report]   {rn}  ({len(content)/1e6:.1f} MB)")
            manifest["items"].append(rec)

        # --- Dataflow-Definitionen (model.json) ---
        for f in sorted(dataflows, key=lambda f: f.get("name", "")):
            fid, fn = f.get("objectId"), f.get("name", "?")
            rec = {"workspace": gn, "type": "dataflow", "name": fn, "id": fid}
            content, err = api.export_bytes(f"/groups/{gid}/dataflows/{fid}", timeout=120)
            if err:
                rec["status"], rec["error"] = "FEHLER", err
                n_err += 1
                log(f"   ✗ [dataflow] {fn}  → {err}")
            else:
                fp = wsdir / f"{safe(fn)}.dataflow.json"
                fp.write_bytes(content)
                rec["status"], rec["file"], rec["bytes"] = "OK", str(fp), len(content)
                n_ok += 1
                total += len(content)
                log(f"   ✓ [dataflow] {fn}  ({len(content)/1e3:.0f} KB)")
            manifest["items"].append(rec)

    root.mkdir(parents=True, exist_ok=True)
    mf = root / "_manifest.json"
    json.dump(manifest, open(mf, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    log(f"\n✅ Backup fertig: {n_ok} OK, {n_err} Fehler, {total/1e6:.1f} MB gesamt")
    log(f"   Ordner:   {root}")
    log(f"   Manifest: {mf}")
    return n_ok, n_err


def main():
    ap = argparse.ArgumentParser(description="Power BI Report/Dataflow-Backup (read-only).")
    ap.add_argument("--tenant", required=True)
    ap.add_argument("--workspace", help="Substring-Filter (case-insensitive) auf Workspace-Namen")
    ap.add_argument("--all", action="store_true", help="alle Workspaces des Tenants sichern")
    ap.add_argument("--list", action="store_true", help="nur auflisten, nichts herunterladen")
    ap.add_argument("--out", default=None,
                    help="Zielordner, in dem der datierte Snapshot-Ordner entsteht "
                         "(Default: ~/PowerBI-Backups/<tenant>). Für die bestehende "
                         "Struktur: --out '<Kunde>/Sicherungen'.")
    ap.add_argument("--stamp", help="Zeitstempel-Ordnername (Default: jetzt)")
    a = ap.parse_args()

    if not (a.list or a.all or a.workspace):
        sys.exit("Bitte --list, --workspace <name> oder --all angeben.")

    api = Api(TokenManager(a.tenant))
    groups = api.value("/groups")
    log(f"{len(groups)} Workspace(s) im Tenant {a.tenant}")
    if a.workspace:
        wsl = a.workspace.lower()
        groups = [g for g in groups if wsl in (g.get("name") or "").lower()]
        log(f"{len(groups)} Workspace(s) nach Filter '{a.workspace}'")
        if not groups:
            sys.exit("Kein Workspace passt zum Filter. Mit --list die Namen prüfen.")

    if a.list:
        list_tenant(api, groups)
        return

    # --out (falls gesetzt) ist direkt die Basis für den datierten Snapshot-Ordner
    # (passt auf die bestehende Konvention <Kunde>/Sicherungen/<Datum>/<Workspace>).
    # Sonst Default ~/PowerBI-Backups/<tenant>/. Stamp im Stil der bestehenden Ordner.
    base = a.out if a.out else str(Path.home() / "PowerBI-Backups" / safe(a.tenant))
    stamp = a.stamp or datetime.now().strftime("%Y-%m-%d-%H-%M")
    backup(api, groups, base, stamp)


if __name__ == "__main__":
    main()
