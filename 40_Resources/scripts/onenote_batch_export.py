#!/usr/bin/env python3
"""
onenote_batch_export.py  (resumierbar)
--------------------------------------
Exportiert alle inhaltsreichen Kunden-Team-Notizbücher SEQUENTIELL nach
40_Resources/OneNote-Import/<Team>/.  Robust gegen Throttling: das Pacing
steckt in onenote_export.py (GRAPH_PACE). Fertige Teams bekommen eine
`.done`-Markierung und werden bei erneutem Lauf übersprungen (Resume).
"""
import re
import subprocess
import time
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
VAULT = SCRIPTS.parent.parent
PY = str(SCRIPTS / ".venv" / "bin" / "python")
EXPORT = str(SCRIPTS / "onenote_export.py")
BASE_REL = "40_Resources/OneNote-Import"
BASE_ABS = VAULT / BASE_REL

TEAMS = [
    ("Up-Great AG", "2954caf0-cf96-42fe-a465-48600ebe4935"),
    ("Sharkgroup", "e837b22f-771f-4faa-83cc-cd7a67b5b17e"),
    ("PK-Rück", "d5104d82-328d-4e08-816a-d4335f0ab6c2"),
    ("MVM AG", "20ce25ad-050b-4ebf-8053-f14c86417630"),
    ("Hunnenberg", "c5a31e6e-fb3d-425d-99bc-de020b73917c"),
    ("DOMBA", "f713c598-2b40-43d5-8988-81b15f5be112"),
    ("tibits ag", "7d96c998-e00e-41cf-925e-ac48c1dd6f8f"),
    ("FC Luzern", "b0884eba-d587-4c8a-b955-4329de23f41f"),
    ("Nahrin", "2e2a58dd-a06b-4c59-ad8f-bdcd6e763930"),
    ("Green.ch", "a24427d9-80aa-4685-bc74-78fac0f2231a"),
    ("Sefag Components AG", "a72f178a-2bda-4069-a162-c3fa13b2b2cd"),
    ("DOBI-Inter AG", "f037a5af-0c77-4104-aeba-fd361529f006"),
    ("SACAC AG", "20838fdc-5805-445c-bc63-a82999ee1908"),
    ("SIGA", "31cc2011-f429-402f-bf4f-91b8f6a311cf"),
    ("Allreal", "c5bd91b0-383a-4e1e-b871-6bf9fc7ab261"),
    ("Mindpearl", "c93d44b0-f691-4a8c-b70c-680e77e380b5"),
    ("Calanda Gruppe", "16fe832d-22d1-4531-9ad8-71049baf25f8"),
    ("Robotec-Schomburg", "8affae39-3f93-43ed-a6a7-8a8658cb8b55"),
    ("4B AG", "14e43348-9e42-4df3-9c64-f9794824c142"),
    ("Elektrizitätswerk Obwalden", "ae3982e8-e0b6-414d-b386-56716090b75f"),
    ("SAGE", "72826ae8-2fb1-4a1b-81ab-4c36955a4126"),
    ("abbvie", "9c53dbd8-2895-4a3c-8164-79b2a80ca114"),
    ("FUCHS Die Firmenfamilie", "16f3a4d9-c8df-45f8-889f-81ff30dff3f1"),
    ("The Advisory House AG", "fe60bb19-c764-46de-996f-2521926f97ea"),
    ("Activ Innovation", "b543bccb-ae1f-4122-81ad-3e74cac48ab4"),
    ("Kampmeyer Immobilien GmbH", "e4f6bce1-a43d-4412-8043-79fe9582d354"),
    ("UBS AG", "3e9d96f7-fd17-4039-9f6c-90272d24abf6"),
]


def slug(name):
    return re.sub(r"\s+", " ", name).replace("/", "-").strip()


def main():
    n = len(TEAMS)
    print(f"==== BATCH-EXPORT (resume) · {n} Teams ====", flush=True)
    for i, (name, gid) in enumerate(TEAMS, 1):
        s = slug(name)
        out_rel = f"{BASE_REL}/{s}"
        out_abs = BASE_ABS / s
        done = out_abs / ".done"
        if done.exists():
            print(f"[{i}/{n}] {name} — übersprungen (.done)", flush=True)
            continue
        print(f"\n########## [{i}/{n}] {name}  →  {out_rel} ##########", flush=True)
        try:
            r = subprocess.run(
                [PY, EXPORT, "--group-id", gid, "--all-notebooks", "--clean", "--out", out_rel],
                timeout=3000)
            if r.returncode == 0:
                out_abs.mkdir(parents=True, exist_ok=True)
                done.write_text("ok")
                print(f"[exit 0 ✓] {name}", flush=True)
            else:
                print(f"[exit {r.returncode}] {name} — kein .done (wird beim nächsten Lauf erneut versucht)", flush=True)
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT >3000s] {name}", flush=True)
        except Exception as e:
            print(f"[FEHLER] {name}: {e}", flush=True)
        time.sleep(15)   # Pause zwischen Teams → Throttling-Budget erholt sich
    print("\n==== BATCH FERTIG ====", flush=True)


if __name__ == "__main__":
    main()
