#!/usr/bin/env python3
"""
style_corpus.py — Zieht Giovannis EIGENE gesendete Mails an eine/mehrere Adressen,
schneidet zitierte Original-Mails (Outlook-Reply-Blöcke) und Signatur/Disclaimer ab.
Zweck: Schreibstil-Analyse pro Empfänger. Rein lesend, gibt nur auf stdout aus
(speichert KEINE Mailinhalte auf Platte).

Aufruf:
    ./.venv/bin/python style_corpus.py michael@kipfer-dp.com alessandro@castelli-solutions.ch ...
Optional pro Adresse Anzahl:  email:12
"""
import sys, re, html, time
from pathlib import Path
import requests

GRAPH = "https://graph.microsoft.com/v1.0"
ME = "giovanni@miraglia-bi.com"
from auth_common import get_token as _tok
TOKEN = _tok(["Mail.Read", "User.Read"])
H = {"Authorization": f"Bearer {TOKEN}"}

# Grenzen, an denen Giovannis eigener Text endet (zitiertes Original / Signatur / Disclaimer).
CUTS = [
    r"\nVon:\s",                      # Outlook DE Reply-Header
    r"\nFrom:\s",
    r"\n_{5,}",                       # lange Unterstrich-Linie von Outlook
    r"\nAm\s.{0,80}?schrieb",         # "Am 12.06.2026 schrieb ...:"
    r"\nOn\s.{0,90}?wrote:",
    r"\n-{2,}\s*Urspr",               # "----- Ursprüngliche Nachricht"
    r"\nGesendet von meinem",         # Mobile-Footer
    r"\nGesendet:\s",
    r"Microsoft Teams-Besprechung",   # Kalender-/Meeting-Einladung (keine Prosa)
    r"_{10,}",                         # lange Trennlinie (Outlook/Teams)
    r"\bMiraglia Business[- ]?Intelligence\b",
    r"www\.miraglia",
    r"\[cid:",                        # eingebettetes Logo
    r"\nTel\.?\s*[:+]",
    r"\n\+41\s?\d",
    r"Diese E-?Mail",                 # Disclaimer
    r"This e-?mail",
]
CUT_RE = re.compile("|".join(CUTS), re.I | re.S)


def clean(body, ctype):
    if ctype == "html":
        body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", body, flags=re.S | re.I)
        body = re.sub(r"(?i)<br\s*/?>", "\n", body)
        body = re.sub(r"(?i)</p>", "\n", body)
        body = re.sub(r"<[^>]+>", " ", body)
        body = html.unescape(body)
    m = CUT_RE.search(body)
    if m:
        body = body[:m.start()]
    body = re.sub(r"[ \t ]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n\n", body)
    return body.strip()


def fetch(email, n):
    url = (f'{GRAPH}/me/messages?$search="{email}"'
           f"&$select=subject,from,toRecipients,ccRecipients,sentDateTime,"
           f"receivedDateTime,body&$top=60")
    r = requests.get(url, headers=H, timeout=90)
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5)))
        r = requests.get(url, headers=H, timeout=90)
    r.raise_for_status()
    out = []
    for m in r.json().get("value", []):
        frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
        if frm != ME:
            continue
        rec = " ".join(
            ((x.get("emailAddress") or {}).get("address") or "").lower()
            for x in (m.get("toRecipients") or []) + (m.get("ccRecipients") or []))
        if email.lower() not in rec:
            continue
        b = clean((m.get("body") or {}).get("content", ""),
                  (m.get("body") or {}).get("contentType", ""))
        if len(b) < 12:   # leere/triviale Mails überspringen
            continue
        date = (m.get("sentDateTime") or m.get("receivedDateTime") or "")[:10]
        out.append((date, m.get("subject", ""), b))
    out.sort(key=lambda t: t[0], reverse=True)
    return out[:n]


def main():
    args = sys.argv[1:]
    for a in args:
        email, _, cnt = a.partition(":")
        n = int(cnt) if cnt else 12
        rows = fetch(email, n)
        print("\n" + "#" * 78)
        print(f"# GESENDET AN: {email}   ({len(rows)} eigene Mails)")
        print("#" * 78)
        for date, subj, body in rows:
            print(f"\n--- {date} | {subj}")
            print(body[:1300])


if __name__ == "__main__":
    main()
