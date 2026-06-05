#!/usr/bin/env python3
"""
m365_people_sync.py
-------------------
Zieht aus deinem Microsoft-365-Postfach (delegierter Graph-Zugriff) die Personen,
mit denen du in Kontakt stehst, und erzeugt pro Person eine Obsidian-Notiz
im Ordner 25_People/.

Quellen:
  - /me/people     -> relevanz-sortierte Kontaktpersonen (Kern)
  - /me/contacts   -> dein Adressbuch
  - /me/messages   -> (optional, --with-mail) letzter Kontakt + Häufigkeit

Login: MSAL Device-Code-Flow (kein Client-Secret nötig, Public Client).
Der Token wird lokal gecacht (.token_cache.bin) -> kein Re-Login bei Folgeläufen.

Aufruf-Beispiele:
  python3 m365_people_sync.py                 # People + Contacts
  python3 m365_people_sync.py --with-mail     # zusätzlich letzter Kontakt aus Mails
  python3 m365_people_sync.py --force         # bestehende Notizen überschreiben
  python3 m365_people_sync.py --max-mail 2000 # wie viele Mails scannen (Default 1000)
"""

import argparse
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Fehlende Pakete. Bitte:  pip install -r requirements.txt")

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURATION  — die beiden IDs aus der App-Registrierung hier eintragen
#   (oder per Umgebungsvariable M365_CLIENT_ID / M365_TENANT_ID setzen)
# ─────────────────────────────────────────────────────────────────────────────
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES_BASE = ["User.Read", "People.Read", "Contacts.Read"]
SCOPE_MAIL = "Mail.Read"

SCRIPT_DIR = Path(__file__).resolve().parent
# Vault-Root = zwei Ebenen über diesem Script (40_Resources/scripts/ -> Vault)
VAULT_ROOT = Path(os.environ.get("VAULT_ROOT", SCRIPT_DIR.parent.parent))
# Pfad per Env-Var anpassbar — siehe scripts/.env
PEOPLE_DIR = VAULT_ROOT / os.environ.get("PEOPLE_DIR", "25_People")


# ─────────────────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────────────────
def get_token(scopes):
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(scopes)


def graph_get_all(token, url):
    """GET mit automatischem Paging über @odata.nextLink."""
    headers = {"Authorization": f"Bearer {token}"}
    items = []
    while url:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 429:  # throttling
            import time
            time.sleep(int(r.headers.get("Retry-After", 5)))
            continue
        r.raise_for_status()
        data = r.json()
        items.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return items


# ─────────────────────────────────────────────────────────────────────────────
# DATEN HOLEN & MERGEN
# ─────────────────────────────────────────────────────────────────────────────
def norm_email(e):
    return (e or "").strip().lower()


def fetch_people(token, store):
    url = f"{GRAPH}/me/people?$top=50"
    for p in graph_get_all(token, url):
        emails = p.get("scoredEmailAddresses") or []
        primary = norm_email(emails[0]["address"]) if emails else ""
        if not primary:
            continue
        rec = store.setdefault(primary, _blank(primary))
        rec["name"] = p.get("displayName") or rec["name"]
        rec["company"] = p.get("companyName") or rec["company"]
        rec["role"] = p.get("jobTitle") or rec["role"]
        for ph in (p.get("phones") or []):
            if ph.get("number"):
                rec["phones"].add(ph["number"])
        score = emails[0].get("relevanceScore")
        if score is not None:
            rec["relevance"] = round(float(score), 3)
        rec["sources"].add("people")


def fetch_contacts(token, store):
    sel = "displayName,emailAddresses,companyName,jobTitle,department,businessPhones,mobilePhone"
    url = f"{GRAPH}/me/contacts?$top=100&$select={sel}"
    for c in graph_get_all(token, url):
        emails = c.get("emailAddresses") or []
        primary = norm_email(emails[0]["address"]) if emails else ""
        if not primary:
            continue
        rec = store.setdefault(primary, _blank(primary))
        rec["name"] = c.get("displayName") or rec["name"]
        rec["company"] = c.get("companyName") or rec["company"]
        rec["role"] = c.get("jobTitle") or rec["role"]
        rec["department"] = c.get("department") or rec["department"]
        for ph in (c.get("businessPhones") or []):
            rec["phones"].add(ph)
        if c.get("mobilePhone"):
            rec["phones"].add(c["mobilePhone"])
        rec["sources"].add("contacts")


def fetch_mail_signals(token, store, max_mail):
    """Letzter Kontakt + Häufigkeit aus den letzten N Mails (Posteingang + Gesendet)."""
    sel = "from,toRecipients,receivedDateTime,sentDateTime"
    url = f"{GRAPH}/me/messages?$top=100&$select={sel}&$orderby=receivedDateTime desc"
    headers = {"Authorization": f"Bearer {token}"}
    seen = 0
    while url and seen < max_mail:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        for m in data.get("value", []):
            seen += 1
            dt = m.get("receivedDateTime") or m.get("sentDateTime")
            parties = []
            frm = (m.get("from") or {}).get("emailAddress", {}).get("address")
            if frm:
                parties.append(frm)
            for rcp in (m.get("toRecipients") or []):
                a = rcp.get("emailAddress", {}).get("address")
                if a:
                    parties.append(a)
            for addr in parties:
                key = norm_email(addr)
                if key not in store:
                    continue  # nur bekannte Personen anreichern, keine neuen anlegen
                rec = store[key]
                rec["mail_count"] += 1
                if dt and (not rec["last_contact"] or dt > rec["last_contact"]):
                    rec["last_contact"] = dt
        url = data.get("@odata.nextLink") if seen < max_mail else None


def _blank(email):
    return {
        "name": "", "company": "", "role": "", "department": "",
        "email": email, "phones": set(), "relevance": None,
        "last_contact": "", "mail_count": 0, "sources": set(),
    }


# ─────────────────────────────────────────────────────────────────────────────
# NOTIZEN SCHREIBEN
# ─────────────────────────────────────────────────────────────────────────────
def safe_filename(name, email):
    base = (name or email.split("@")[0]).strip()
    base = re.sub(r'[\\/:*?"<>|#^\[\]]', "", base)
    base = re.sub(r"\s+", " ", base).strip()
    return base or email.split("@")[0]


def yq(s):
    """YAML-sicherer String (in Anführungszeichen, escaped)."""
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


def fmt_date(iso):
    if not iso:
        return ""
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return iso[:10]


def build_note(rec, today):
    fm = ["---", "type: person", "status: active", f"created: {today}",
          f"email: {rec['email']}"]
    if rec["company"]:
        fm.append(f"company: {yq(rec['company'])}")
    if rec["role"]:
        fm.append(f"role: {yq(rec['role'])}")
    if rec["department"]:
        fm.append(f"department: {yq(rec['department'])}")
    if rec["phones"]:
        fm.append("phones: [" + ", ".join(yq(p) for p in sorted(rec["phones"])) + "]")
    if rec["relevance"] is not None:
        fm.append(f"relevance: {rec['relevance']}")
    if rec["last_contact"]:
        fm.append(f"last_contact: {fmt_date(rec['last_contact'])}")
    if rec["mail_count"]:
        fm.append(f"mail_count: {rec['mail_count']}")
    fm.append(f"source: [{', '.join(sorted(rec['sources']))}]")
    fm.append("tags: [person, contact]")
    fm.append("---")

    name = rec["name"] or rec["email"]
    body = [f"# {name}", "", "## Contact",
            f"- **Email:** {rec['email']}"]
    if rec["phones"]:
        body.append(f"- **Phone:** {', '.join(sorted(rec['phones']))}")
    if rec["company"]:
        body.append(f"- **Company:** [[{rec['company']}]]")
    if rec["role"]:
        body.append(f"- **Role:** {rec['role']}")
    body += ["", "## Relationship", "- ", "", "## Log",
             f"- {today} — Importiert aus M365 ({', '.join(sorted(rec['sources']))})"]
    return "\n".join(fm) + "\n" + "\n".join(body) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--with-mail", action="store_true", help="letzter Kontakt aus Mails (braucht Mail.Read)")
    ap.add_argument("--max-mail", type=int, default=1000, help="wie viele Mails scannen (Default 1000)")
    ap.add_argument("--force", action="store_true", help="bestehende Notizen überschreiben")
    args = ap.parse_args()

    scopes = SCOPES_BASE + ([SCOPE_MAIL] if args.with_mail else [])
    token = get_token(scopes)

    store = {}
    print("→ /me/people …")
    fetch_people(token, store)
    print("→ /me/contacts …")
    fetch_contacts(token, store)
    if args.with_mail:
        print(f"→ /me/messages (max {args.max_mail}) …")
        fetch_mail_signals(token, store, args.max_mail)

    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).date().isoformat()
    # Bereits erfasste E-Mail-Adressen sammeln (email + alt_emails) —
    # verhindert, dass manuell umbenannte/zusammengeführte Notizen neu angelegt werden.
    known = set()
    for n in PEOPLE_DIR.glob("*.md"):
        t = n.read_text(encoding="utf-8")
        for mm in re.finditer(r"^email:\s*(\S+)", t, re.M):
            known.add(mm.group(1).strip().lower())
        am = re.search(r"^alt_emails:\s*\[(.*?)\]", t, re.M)
        if am:
            for e in am.group(1).split(","):
                known.add(e.strip().strip('"\'').lower())
    created = skipped = 0
    for rec in store.values():
        if rec["email"].lower() in known and not args.force:
            skipped += 1
            continue
        fname = safe_filename(rec["name"], rec["email"]) + ".md"
        path = PEOPLE_DIR / fname
        if path.exists() and not args.force:
            skipped += 1
            continue
        path.write_text(build_note(rec, today), encoding="utf-8")
        created += 1

    print(f"\n✓ Fertig. {len(store)} Personen gefunden — {created} geschrieben, {skipped} übersprungen (existierten).")
    print(f"  Ordner: {PEOPLE_DIR}")


if __name__ == "__main__":
    main()
