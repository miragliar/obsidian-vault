#!/usr/bin/env python3
"""
move_mail.py — Eine Mail (per Betreff-Suche) in einen Postfach-Ordner VERSCHIEBEN.

Nicht-destruktiv & reversibel (nur Ordnerwechsel). Braucht Mail.ReadWrite.
Es wird NIE gelöscht und NIE gesendet.

Usage:
    ./.venv/bin/python move_mail.py "betreff-suche" "Zielordner" ["betreff-filter"] ["absender-filter"]
    ./.venv/bin/python move_mail.py --list-folders                 # alle Ordner + IDs zeigen
    ./.venv/bin/python move_mail.py --dry-run "suche" "Zielordner" ["betreff-filter"]
"""
import sys
import requests
from auth_common import get_token, GRAPH

args = sys.argv[1:]
dry = False
if args and args[0] == "--dry-run":
    dry = True
    args = args[1:]

tok = get_token(["Mail.ReadWrite", "User.Read"])
H = {"Authorization": f"Bearer {tok}"}


def all_folders():
    """Alle Mail-Ordner rekursiv -> Liste (displayName, id, pfad)."""
    out = []

    def walk(fid=None, path=""):
        base = f"{GRAPH}/me/mailFolders" if fid is None else f"{GRAPH}/me/mailFolders/{fid}/childFolders"
        url = base + "?$top=100&$select=id,displayName,childFolderCount"
        while url:
            r = requests.get(url, headers=H, timeout=60); r.raise_for_status()
            data = r.json()
            for f in data.get("value", []):
                p = f"{path}/{f['displayName']}"
                out.append((f["displayName"], f["id"], p))
                if f.get("childFolderCount", 0) > 0:
                    walk(f["id"], p)
            url = data.get("@odata.nextLink")
    walk()
    return out


if args and args[0] == "--list-folders" or (sys.argv[1:2] == ["--list-folders"]):
    for name, fid, path in all_folders():
        print(f"{path}\t{fid}")
    sys.exit(0)

if len(args) < 2:
    sys.exit("Usage: move_mail.py \"suche\" \"Zielordner\" [betreff-filter] [absender-filter]")

query = args[0]
target_name = args[1]
subj_filter = (args[2].lower() if len(args) > 2 else "")
from_filter = (args[3].lower() if len(args) > 3 else "")

# Zielordner auflösen
folders = all_folders()
matches = [f for f in folders if f[0].lower() == target_name.lower()]
if not matches:
    sys.exit(f"Zielordner '{target_name}' nicht gefunden. (--list-folders zum Prüfen)")
if len(matches) > 1:
    print(f"⚠️  Mehrere Ordner namens '{target_name}':")
    for n, i, p in matches:
        print(f"    {p}")
    print("    -> nehme den ersten.")
target_id = matches[0][1]
print(f"Zielordner: {matches[0][2]}")

# Nachricht suchen
url = (f'{GRAPH}/me/messages?$search="{query}"'
       f'&$select=id,subject,from,receivedDateTime,parentFolderId&$top=10')
r = requests.get(url, headers=H, timeout=60); r.raise_for_status()
picked = None
for m in r.json().get("value", []):
    if subj_filter and subj_filter not in (m.get("subject") or "").lower():
        continue
    frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
    if from_filter and from_filter not in frm:
        continue
    picked = m
    break

if not picked:
    sys.exit("Keine passende Nachricht gefunden.")

frm = ((picked.get("from") or {}).get("emailAddress") or {}).get("address", "")
print(f"Nachricht: {picked.get('receivedDateTime')} | {frm}")
print(f"Betreff:   {picked.get('subject')}")

if picked.get("parentFolderId") == target_id:
    print("ℹ️  Liegt bereits im Zielordner — nichts zu tun.")
    sys.exit(0)

if dry:
    print("DRY-RUN: würde verschieben (keine Änderung).")
    sys.exit(0)

mv = requests.post(
    f"{GRAPH}/me/messages/{picked['id']}/move",
    headers={**H, "Content-Type": "application/json"},
    json={"destinationId": target_id}, timeout=60)
mv.raise_for_status()
print(f"✅ Verschoben nach '{matches[0][0]}'.")
