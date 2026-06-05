#!/usr/bin/env python3
"""
onenote_export.py
-----------------
Exportiert ein OneNote-Notizbuch nach Obsidian (Markdown).

Liest OneNote via Microsoft Graph (delegiert), wandelt den Seiten-HTML in Markdown
um, lädt eingebettete Bilder/Anhänge herunter und schreibt pro Seite eine .md-Datei
(mit Frontmatter) in den Vault.

Unterstützt drei Quellen:
  • persönliche Notizbücher        (/me/onenote …)          → Default
  • Team-/Gruppen-Notizbücher      (/groups/{id}/onenote …) → --team / --group-id
  • SharePoint-Site-Notizbücher    (/sites/{id}/onenote …)  → --site-id

➡ Nur LESEND auf der M365-Seite. Geschrieben wird ausschliesslich lokal in den Vault.

Benötigte (bereits konsentierte) Scopes: User.Read, Notes.Read.All, Team.ReadBasic.All.

Aufruf:
  # Teams (= Kunden) auflisten
  ./.venv/bin/python onenote_export.py --list-teams

  # Notizbücher einer Quelle ansehen
  ./.venv/bin/python onenote_export.py --team "Koster" --list

  # Ein Kunden-Notizbuch exportieren (Dry-Run zeigt nur die Struktur)
  ./.venv/bin/python onenote_export.py --team "Koster" --dry-run
  ./.venv/bin/python onenote_export.py --team "Koster"

  # Persönliches Notizbuch
  ./.venv/bin/python onenote_export.py --notebook "Power-BI"

Optionen:
  --out DIR     Zielordner relativ zum Vault-Root  (Default: 40_Resources/OneNote-Import)
  --dry-run     Nur anzeigen, was exportiert würde — nichts schreiben/laden
  --limit N     Max. Seiten pro Abschnitt (zum Testen)
"""
import argparse
import hashlib
import os
import re
import shutil
import sys
import time
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# --- Auth / Konstanten (gleiche App wie die übrigen M365-Skripte) ---------------
GRAPH = "https://graph.microsoft.com/v1.0"
PACE = float(os.environ.get("GRAPH_PACE", "1.0"))   # Sek. Pause vor jedem Graph-Call (Anti-Throttling)
# Notes.Read.All deckt auch Gruppen-/Site-Notizbücher ab; Team.ReadBasic.All für --team.
SCOPES = ["User.Read", "Notes.Read.All", "Team.ReadBasic.All"]

SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", SCRIPT_DIR.parent.parent))
DEFAULT_OUT = "40_Resources/OneNote-Import"


# --- Token (silent → sonst Device-Flow, wie mail_digest.py) ---------------------
def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


# --- Graph-Helfer: GET mit 429-Retry; JSON-Paginierung über @odata.nextLink -----
def graph_get(token, url, accept="application/json", binary=False):
    headers = {"Authorization": f"Bearer {token}", "Accept": accept}
    last = None
    for attempt in range(10):   # Retry bei 429 (Throttling) UND 5xx (OneNote-Content träge)
        time.sleep(PACE)        # gleichmäßiges Pacing gegen OneNote-Throttling
        try:
            r = requests.get(url, headers=headers, timeout=120)
        except requests.RequestException as e:
            last = e
            time.sleep(min(120, 5 * (2 ** attempt)))
            continue
        if r.status_code == 429 or 500 <= r.status_code < 600:
            last = r
            wait = r.headers.get("Retry-After")
            time.sleep(int(wait) if (wait and wait.isdigit()) else min(120, 5 * (2 ** attempt)))
            continue
        r.raise_for_status()
        return r.content if binary else r
    if isinstance(last, requests.Response):
        last.raise_for_status()
    raise last if last else RuntimeError(f"graph_get fehlgeschlagen: {url}")


def graph_list(token, url):
    """Holt eine komplette Collection (folgt @odata.nextLink)."""
    items = []
    while url:
        data = graph_get(token, url).json()
        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return items


# --- Dateinamen / YAML säubern --------------------------------------------------
_BAD = re.compile(r'[\\/:*?"<>|#^\[\]]')


def safe_name(name, fallback="Unbenannt"):
    name = (name or "").strip()
    name = _BAD.sub("-", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:120] or fallback


def yaml_str(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


# --- Quellen: Teams auflisten / nach Name auflösen ------------------------------
def list_teams(token):
    teams = graph_list(token, f"{GRAPH}/me/joinedTeams?$select=id,displayName")
    return sorted(teams, key=lambda t: (t.get("displayName") or "").lower())


def resolve_team(token, name):
    teams = list_teams(token)
    matches = [t for t in teams if name.lower() in (t.get("displayName") or "").lower()]
    if not matches:
        sys.exit(f"Kein Team passt zu '{name}'. → mit --list-teams alle ansehen.")
    if len(matches) > 1:
        sys.exit(f"Mehrere Teams für '{name}':\n  " +
                 "\n  ".join(f"{t['displayName']}  (id: {t['id']})" for t in matches) +
                 "\n→ mit --group-id präzisieren.")
    return matches[0]


# --- Struktur einlesen (root = .../onenote) -------------------------------------
def list_notebooks(token, root):
    return graph_list(token, f"{root}/notebooks?$select=id,displayName&$top=100")


def find_notebook(token, root, name=None, nb_id=None):
    nbs = list_notebooks(token, root)
    if nb_id:
        for nb in nbs:
            if nb["id"] == nb_id:
                return nb
        sys.exit(f"Kein Notizbuch mit ID {nb_id}.")
    if name:
        matches = [nb for nb in nbs if name.lower() in (nb.get("displayName") or "").lower()]
        if not matches:
            sys.exit(f"Kein Notizbuch passt zu '{name}'. Verfügbar:\n  " +
                     "\n  ".join(nb.get("displayName", "?") for nb in nbs))
        if len(matches) > 1:
            sys.exit(f"Mehrere Treffer für '{name}':\n  " +
                     "\n  ".join(f"{nb['displayName']}  (id: {nb['id']})" for nb in matches))
        return matches[0]
    # ohne Filter: bei genau einem Notizbuch automatisch wählen (Teams-Standardfall)
    if len(nbs) == 1:
        return nbs[0]
    if not nbs:
        sys.exit("Diese Quelle hat keine Notizbücher.")
    sys.exit("Mehrere Notizbücher — mit --notebook \"Name\" wählen:\n  " +
             "\n  ".join(nb.get("displayName", "?") for nb in nbs))


def collect_sections(token, root, notebook_id):
    """Liefert Liste von (section, [pfad-teile]) — Direkt-Sektionen + Section-Groups."""
    out = []
    for s in graph_list(token, f"{root}/notebooks/{notebook_id}/sections?$select=id,displayName&$top=100"):
        out.append((s, [s.get("displayName", "Abschnitt")]))

    def walk_group(group_id, prefix):
        for s in graph_list(token, f"{root}/sectionGroups/{group_id}/sections?$select=id,displayName&$top=100"):
            out.append((s, prefix + [s.get("displayName", "Abschnitt")]))
        for g in graph_list(token, f"{root}/sectionGroups/{group_id}/sectionGroups?$select=id,displayName&$top=100"):
            walk_group(g["id"], prefix + [g.get("displayName", "Gruppe")])

    for g in graph_list(token, f"{root}/notebooks/{notebook_id}/sectionGroups?$select=id,displayName&$top=100"):
        walk_group(g["id"], [g.get("displayName", "Gruppe")])
    return out


def list_pages(token, root, section_id):
    url = (f"{root}/sections/{section_id}/pages"
           f"?$select=id,title,createdDateTime,lastModifiedDateTime&$top=100")
    return graph_list(token, url)


# --- HTML einer Seite → Markdown (+ Bilder/Anhänge lokal speichern) -------------
def ext_from_type(t, default=".bin"):
    return {"image/png": ".png", "image/jpeg": ".jpg", "image/jpg": ".jpg",
            "image/gif": ".gif", "image/webp": ".webp",
            "application/pdf": ".pdf"}.get((t or "").lower(), default)


def convert_page(token, root, page, attach_dir, dry_run):
    """Lädt Seiten-HTML, ersetzt Ressourcen durch lokale Embeds, gibt Markdown zurück."""
    pid = page["id"]
    try:
        html = graph_get(token, f"{root}/pages/{pid}/content",
                         accept="text/html").text
    except requests.HTTPError as e:
        print(f"      ! Inhalt übersprungen ({e})", flush=True)
        return None

    soup = BeautifulSoup(html, "html.parser")
    body = soup.body or soup
    # Präfix MUSS pro Seite eindeutig sein (Page-ID-Hash) — sonst kollidieren
    # gleichnamige Bilder verschiedener Seiten desselben Abschnitts.
    short = hashlib.md5(pid.encode("utf-8")).hexdigest()[:10]
    tokens = {}   # XRES0X → dateiname
    n = 0

    def grab(src, type_hint, base_ext, orig_name=None):
        nonlocal n
        if not src:
            return None
        if orig_name:   # <object>: Originalnamen + Endung aus data-attachment übernehmen
            stem = safe_name(Path(orig_name).stem, "Datei")
            ext = Path(orig_name).suffix or ext_from_type(type_hint, base_ext)
            fname = f"{short}_{n}_{stem}{ext}"
        else:
            fname = f"{short}_{n}{ext_from_type(type_hint, base_ext)}"
        if not dry_run:
            try:
                blob = graph_get(token, src, accept="*/*", binary=True)
            except requests.HTTPError as e:
                print(f"      ! Ressource übersprungen ({e})", flush=True)
                return None
            attach_dir.mkdir(parents=True, exist_ok=True)
            (attach_dir / fname).write_bytes(blob)
        key = f"XRES{n}X"
        tokens[key] = fname
        n += 1
        return key

    # Bilder: volle Auflösung bevorzugen
    for img in body.find_all("img"):
        src = img.get("data-fullres-src") or img.get("src")
        type_hint = img.get("data-fullres-src-type") or img.get("data-src-type")
        key = grab(src, type_hint, ".png")
        img.replace_with(soup.new_string(key)) if key else img.decompose()

    # Datei-Anhänge (<object>): Originaldateiname aus data-attachment
    for obj in body.find_all("object"):
        key = grab(obj.get("data"), obj.get("type"), ".bin", obj.get("data-attachment"))
        obj.replace_with(soup.new_string(key)) if key else obj.decompose()

    markdown = md(str(body), heading_style="ATX", strip=["title"]).strip()
    # Platzhalter → Obsidian-Embeds  (eindeutiger Dateiname → ![[name]] genügt)
    for key, fname in tokens.items():
        markdown = markdown.replace(key, f"![[{fname}]]")
    # Whitespace-Rauschen aus OneNote bereinigen (Trailing-Spaces, Leerzeilen-Häufung)
    markdown = "\n".join(ln.rstrip() for ln in markdown.split("\n"))
    markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()
    return markdown


def page_to_file(token, root, page, src_label, sec_path, out_dir, attach_dir, dry_run, today):
    title = page.get("title") or "Ohne Titel"
    fpath = out_dir / (safe_name(title) + ".md")
    i = 2
    while fpath.exists():   # Titel-Kollision in derselben Sektion
        fpath = out_dir / f"{safe_name(title)} ({i}).md"
        i += 1

    if dry_run:   # Vorschau: nur Zielpfad, kein Inhalt/Bilder laden
        print(f"      · {fpath.relative_to(VAULT_ROOT)}", flush=True)
        return True

    body_md = convert_page(token, root, page, attach_dir, dry_run)
    if body_md is None:
        return False
    fm = "\n".join([
        "---",
        "source: onenote",
        f"onenote_source: {yaml_str(src_label)}",
        f"section: {yaml_str(' / '.join(sec_path))}",
        f"title: {yaml_str(title)}",
        f"created: {page.get('createdDateTime', '')}",
        f"modified: {page.get('lastModifiedDateTime', '')}",
        f"onenote_page_id: {yaml_str(page['id'])}",
        f"exported: {today}",
        "tags: [onenote-import]",
        "---",
        "",
        f"# {title}",
        "",
        body_md,
        "",
    ])
    out_dir.mkdir(parents=True, exist_ok=True)
    fpath.write_text(fm, encoding="utf-8")
    print(f"      ✓ {fpath.relative_to(VAULT_ROOT)}", flush=True)
    return True


def export_notebook(token, root, nb, src_label, args, today):
    nb_name = nb.get("displayName", "OneNote")
    nb_dir = VAULT_ROOT / args.out / safe_name(nb_name)
    attach_dir = nb_dir / "_attachments"
    mode = "  [DRY-RUN]" if args.dry_run else ""
    print(f"\n▶ Quelle: {src_label}   Notizbuch: {nb_name}{mode}")
    print(f"  Ziel: {args.out}/{safe_name(nb_name)}/\n")

    if args.clean and not args.dry_run and nb_dir.exists():
        shutil.rmtree(nb_dir)
        print("  (Zielordner geleert)\n")

    sections = collect_sections(token, root, nb["id"])
    if not sections:
        print("  (keine Abschnitte gefunden)")
        return 0

    total = 0
    for section, sec_path in sections:
        pages = list_pages(token, root, section["id"])
        if args.limit:
            pages = pages[:args.limit]
        print(f"  ▸ {' / '.join(sec_path)}  ({len(pages)} Seiten)", flush=True)
        sec_dir = nb_dir
        for part in sec_path:
            sec_dir = sec_dir / safe_name(part)
        for page in pages:
            if page_to_file(token, root, page, src_label, sec_path, sec_dir,
                            attach_dir, args.dry_run, today):
                total += 1

    verb = "würden exportiert" if args.dry_run else "exportiert"
    print(f"\n✓ {total} Seiten {verb} → {args.out}/{safe_name(nb_name)}/")
    return total


# --- Hauptlogik -----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="OneNote → Obsidian (Markdown) Export.")
    ap.add_argument("--list-teams", action="store_true", help="Beigetretene Teams (= Kunden) auflisten")
    ap.add_argument("--team", help="Team-/Kundenname (Teilstring) → Gruppen-Notizbuch")
    ap.add_argument("--group-id", help="Gruppen-/Team-ID (exakt)")
    ap.add_argument("--site-id", help="SharePoint-Site-ID (exakt)")
    ap.add_argument("--list", action="store_true", help="Notizbücher der Quelle auflisten")
    ap.add_argument("--notebook", help="Notizbuch-Name (Teilstring)")
    ap.add_argument("--notebook-id", help="Notizbuch-ID (exakt)")
    ap.add_argument("--all-notebooks", action="store_true", help="Alle Notizbücher der Quelle exportieren")
    ap.add_argument("--out", default=DEFAULT_OUT, help=f"Zielordner (Default: {DEFAULT_OUT})")
    ap.add_argument("--clean", action="store_true", help="Notizbuch-Zielordner vor Export leeren (sauberer Re-Sync)")
    ap.add_argument("--dry-run", action="store_true", help="Nur anzeigen, nichts schreiben")
    ap.add_argument("--limit", type=int, default=0, help="Max. Seiten pro Abschnitt")
    args = ap.parse_args()

    token = get_token()
    today = date.today().isoformat()

    if args.list_teams:
        teams = list_teams(token)
        print(f"\n{len(teams)} Teams:\n")
        for t in teams:
            print(f"  • {t.get('displayName','?')}")
        return

    # Quelle bestimmen
    if args.group_id:
        root, src_label = f"{GRAPH}/groups/{args.group_id}/onenote", f"group:{args.group_id}"
    elif args.team:
        t = resolve_team(token, args.team)
        root = f"{GRAPH}/groups/{t['id']}/onenote"
        src_label = f"Team: {t['displayName']}"
    elif args.site_id:
        root, src_label = f"{GRAPH}/sites/{args.site_id}/onenote", f"site:{args.site_id}"
    else:
        root, src_label = f"{GRAPH}/me/onenote", "Persönlich"

    if args.list:
        nbs = list_notebooks(token, root)
        print(f"\n{len(nbs)} Notizbücher in '{src_label}':\n")
        for nb in nbs:
            print(f"  • {nb.get('displayName','?')}\n      id: {nb['id']}")
        return

    if args.all_notebooks:
        nbs = list_notebooks(token, root)
        if not nbs:
            print("Keine Notizbücher in dieser Quelle.")
            return
        grand = 0
        for nb in nbs:
            grand += export_notebook(token, root, nb, src_label, args, today)
        print(f"\n══ Gesamt: {grand} Seiten aus {len(nbs)} Notizbüchern → {args.out}/")
        return

    nb = find_notebook(token, root, args.notebook, args.notebook_id)
    export_notebook(token, root, nb, src_label, args, today)


if __name__ == "__main__":
    main()
