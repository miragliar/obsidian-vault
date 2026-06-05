#!/usr/bin/env python3
"""
draft_mail.py
-------------
Legt einen E-Mail-ENTWURF im M365-Postfach an (Graph, delegiert, Mail.ReadWrite).
Der Entwurf erscheint im Drafts-Ordner → Outlook App/Web/Mobile. Es wird NICHTS
versendet (kein Mail.Send). Versand machst du selbst in Outlook.

Eingabe wahlweise:
  (a) per Argumente:   --to a@b.ch[,c@d.ch] --subject "..." --body "..." [--cc ...] [--text]
  (b) per JSON-Datei:  --file draft.json   (keys: to, cc, subject, body, body_type, reply_to_message_id)
  (c) Body aus Datei:  --body-file pfad.html

Beispiele:
  python3 draft_mail.py --to giovanni@miraglia-bi.com --subject "Test" --body "Hallo<br>Welt"
  python3 draft_mail.py --file draft.json
"""
import argparse
import json
import os
import sys
from pathlib import Path

import requests

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.ReadWrite"]
import base64

SCRIPT_DIR = Path(__file__).resolve().parent
SIGNATURE_FILE = SCRIPT_DIR / "signatur.html"
LOGO_FILE = SCRIPT_DIR / "logo_sig.png"
LOGO_CID = "miragliabi-logo"


def logo_attachment():
    b = base64.b64encode(LOGO_FILE.read_bytes()).decode()
    return {"@odata.type": "#microsoft.graph.fileAttachment", "name": "miraglia-bi.png",
            "contentType": "image/png", "isInline": True, "contentId": LOGO_CID, "contentBytes": b}


def load_signature(body_type):
    if not SIGNATURE_FILE.exists():
        return ""
    html = SIGNATURE_FILE.read_text(encoding="utf-8").strip()
    if body_type == "HTML":
        return "<br><br>" + html
    # Text-Variante: Tags grob entfernen
    import re as _re
    txt = _re.sub(r"<[^>]+>", "", html)
    return "\n\n" + "\n".join(l.strip() for l in txt.splitlines() if l.strip())


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def recip(addrs):
    return [{"emailAddress": {"address": a.strip()}} for a in addrs if a and a.strip()]


def create_draft(token, to, cc, subject, body, body_type="HTML", reply_to=None, signature=True):
    if signature:
        body = (body or "") + load_signature(body_type)
    needs_logo = body_type == "HTML" and LOGO_FILE.exists() and f"cid:{LOGO_CID}" in (body or "")
    h = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if reply_to:
        # Antwort-Entwurf im bestehenden Thread erzeugen, dann Body/Empfänger setzen
        r = requests.post(f"{GRAPH}/me/messages/{reply_to}/createReply", headers=h, timeout=30)
        r.raise_for_status()
        did = r.json()["id"]
        patch = {"body": {"contentType": body_type, "content": body}}
        if to:
            patch["toRecipients"] = recip(to)
        if cc:
            patch["ccRecipients"] = recip(cc)
        r2 = requests.patch(f"{GRAPH}/me/messages/{did}", headers=h, json=patch, timeout=30)
        r2.raise_for_status()
        if needs_logo:
            ra = requests.post(f"{GRAPH}/me/messages/{did}/attachments", headers=h,
                               json=logo_attachment(), timeout=30)
            ra.raise_for_status()
        return r2.json()
    msg = {"subject": subject or "", "body": {"contentType": body_type, "content": body or ""}}
    if to:
        msg["toRecipients"] = recip(to)
    if cc:
        msg["ccRecipients"] = recip(cc)
    r = requests.post(f"{GRAPH}/me/messages", headers=h, json=msg, timeout=30)
    r.raise_for_status()
    created = r.json()
    if needs_logo:
        # Inline-Logo zuverlässig NACH dem Erstellen anhängen (wie im Reply-Pfad).
        # Als "attachments" im Create-POST klebt das Inline-Bild bei Graph nicht
        # zuverlässig — die Mail geht dann ohne Logo raus (Broken-Image).
        ra = requests.post(f"{GRAPH}/me/messages/{created['id']}/attachments", headers=h,
                           json=logo_attachment(), timeout=30)
        ra.raise_for_status()
    return created


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", help="JSON-Datei mit Entwurfsdaten")
    ap.add_argument("--to", help="Empfänger, komma-getrennt")
    ap.add_argument("--cc", help="CC, komma-getrennt")
    ap.add_argument("--subject")
    ap.add_argument("--body", help="Body-Text (HTML erlaubt)")
    ap.add_argument("--body-file", help="Body aus Datei lesen")
    ap.add_argument("--text", action="store_true", help="Body als Text statt HTML")
    ap.add_argument("--reply-to", help="Message-ID, um Antwort-Entwurf im Thread zu erstellen")
    ap.add_argument("--no-signature", action="store_true", help="Standard-Signatur NICHT anhängen")
    args = ap.parse_args()

    if args.file:
        d = json.loads(Path(args.file).read_text(encoding="utf-8"))
        to = d.get("to", []); cc = d.get("cc", [])
        to = to.split(",") if isinstance(to, str) else to
        cc = cc.split(",") if isinstance(cc, str) else cc
        subject = d.get("subject", ""); body = d.get("body", "")
        body_type = d.get("body_type", "HTML"); reply_to = d.get("reply_to_message_id")
        signature = d.get("signature", not args.no_signature)
    else:
        to = (args.to or "").split(",") if args.to else []
        cc = (args.cc or "").split(",") if args.cc else []
        subject = args.subject or ""
        body = Path(args.body_file).read_text(encoding="utf-8") if args.body_file else (args.body or "")
        body_type = "Text" if args.text else "HTML"
        reply_to = args.reply_to
        signature = not args.no_signature

    token = get_token()
    draft = create_draft(token, to, cc, subject, body, body_type, reply_to, signature)
    print("✓ Entwurf angelegt (NICHT gesendet) im Drafts-Ordner.")
    print(f"  Betreff : {draft.get('subject')}")
    print(f"  An      : {', '.join(r['emailAddress']['address'] for r in draft.get('toRecipients', [])) or '—'}")
    print(f"  Öffnen  : {draft.get('webLink', '—')}")


if __name__ == "__main__":
    main()
