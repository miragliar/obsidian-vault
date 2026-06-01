#!/usr/bin/env python3
"""
company_enrich.py — Firmen-Steckbrief automatisch holen:
  • Webseite: Titel, Meta-Description, og:description (frei, ohne Login)
  • Handelsregister via Zefix-API: UID, Rechtsform, Sitz, Kanton, Status
    (braucht KOSTENLOSE Zefix-API-Zugangsdaten – Registrierung: https://www.zefix.ch → "API")

Aufruf:
  python3 company_enrich.py --name "Zindel United AG" --url https://www.zindel-united.swiss --md
  ZEFIX_USER=... ZEFIX_PASS=... python3 company_enrich.py --name "Zindel" --zefix --md

Ausgabe: JSON (stdout) + optional ein Markdown-'Unternehmensprofil'-Block (--md),
den du in eine Klienten-Notiz übernehmen kannst.
"""
import argparse
import html
import json
import os
import re
import sys

import requests

UA = {"User-Agent": "Mozilla/5.0 (company_enrich)"}


def fetch_website(url):
    try:
        r = requests.get(url, headers=UA, timeout=20)
        r.raise_for_status()
        h = r.text
    except Exception as e:
        return {"_error": f"website: {e}", "url": url}

    def meta(prop, attr="name"):
        pats = [
            rf'<meta[^>]+{attr}=["\']{re.escape(prop)}["\'][^>]+content=["\']([^"\']+)["\']',
            rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+{attr}=["\']{re.escape(prop)}["\']',
        ]
        for p in pats:
            m = re.search(p, h, re.I)
            if m:
                return html.unescape(m.group(1).strip())
        return None

    t = re.search(r"<title[^>]*>(.*?)</title>", h, re.I | re.S)
    return {
        "url": url,
        "title": html.unescape(re.sub(r"\s+", " ", t.group(1)).strip()) if t else None,
        "description": meta("description") or meta("og:description", "property"),
        "site_name": meta("og:site_name", "property"),
    }


def zefix_search(name, user, pw):
    url = "https://www.zefix.ch/ZefixPublicREST/api/v1/firm/search.json"
    try:
        r = requests.post(url, json={"name": name, "languageKey": "de", "maxEntries": 5, "activeOnly": True},
                          auth=(user, pw), headers={"Accept": "application/json"}, timeout=20)
        if r.status_code == 401:
            return {"_error": "Zefix 401 – ZEFIX_USER/ZEFIX_PASS falsch oder API-Zugang nicht freigeschaltet"}
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"_error": f"zefix: {e}"}
    out = []
    for f in (data or [])[:5]:
        lf = f.get("legalForm")
        out.append({
            "name": f.get("name"), "uid": f.get("uid"), "chid": f.get("chid"),
            "legalSeat": f.get("legalSeat"), "canton": f.get("canton"),
            "legalForm": lf.get("name") if isinstance(lf, dict) else lf,
            "status": "deleted" if f.get("deleteDate") else "active",
        })
    return {"matches": out}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="Firmenname")
    ap.add_argument("--url", help="Firmen-Webseite (Homepage)")
    ap.add_argument("--zefix", action="store_true", help="Handelsregister via Zefix abfragen (ZEFIX_USER/ZEFIX_PASS)")
    ap.add_argument("--md", action="store_true", help="zusätzlich Markdown-Profilblock ausgeben")
    a = ap.parse_args()

    prof = {"name": a.name}
    if a.url:
        prof["website"] = fetch_website(a.url)
    if a.zefix:
        u, p = os.environ.get("ZEFIX_USER"), os.environ.get("ZEFIX_PASS")
        if not (u and p):
            prof["zefix"] = {"_error": "ZEFIX_USER/ZEFIX_PASS nicht gesetzt – kostenlose Registrierung: https://www.zefix.ch → API"}
        else:
            prof["zefix"] = zefix_search(a.name, u, p)

    print(json.dumps(prof, ensure_ascii=False, indent=2))

    if a.md:
        wd = prof.get("website", {}) or {}
        matches = (prof.get("zefix", {}) or {}).get("matches", [])
        z0 = matches[0] if matches else {}
        meta = " · ".join(x for x in [z0.get("legalForm"), z0.get("legalSeat"), z0.get("uid")] if x)
        print("\n----- Markdown -----\n## Unternehmensprofil")
        print("<!-- firmenprofil -->")
        if meta:
            print(f"*{meta}*\n")
        if wd.get("description"):
            print(f"**Was sie tun:** {wd['description']}")
        if a.url:
            print(f"**Web:** {a.url}")
        print("<!-- /firmenprofil -->")


if __name__ == "__main__":
    main()
