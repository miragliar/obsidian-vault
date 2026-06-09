#!/usr/bin/env python3
"""
draft_reply_vloriana_ss.py
--------------------------
Antwort-Entwurf an Vloriana Schnellmann (Sachbearbeiterin HR, MVM AG, Sammelpostfach
personal@mvm-ag.ch) auf ihre Mail vom 2026-06-03 ("AW: Abschlusszeugnis für Kunz
Max") — Bestätigung, dass das scharfe S in der Zeugnis-Generierung nicht mehr
vorkommt.

Ablöser für draft_reply_loetscher_ss.py — die Mail war zwar über Nicoles
Sammelpostfach versandt, geschrieben hat aber Vloriana (im Mai 2026 ins HR-Team
gestartet). Lehre: bei geteilten Postfächern den Body/Signatur prüfen, nicht nur
die From-Adresse.

Verwendet die bewährten Helpers aus draft_replies_mvm.py.
"""
import base64
import sys
from pathlib import Path

import requests

# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr als
# Klartext-.bin im Vault/Dropbox. Regel: Tokens IMMER verschlüsselt im Keystore.
from auth_common import GRAPH, get_token as _ac_get_token

SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]

SCRIPT_DIR = Path(__file__).resolve().parent
LOGO_FILE = SCRIPT_DIR / "miraglia_logo.png"
LOGO_CID = "miragliabi-logo"


SIGNATURE_HTML = (
    "<br><br>"
    "<table cellspacing=\"0\" cellpadding=\"0\">"
    "<tbody><tr>"
    "<td style=\"padding-right:14px; vertical-align:middle\">"
    "<span style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt\">"
    "<a href=\"https://miraglia-bi.com\" style=\"text-decoration:none\">"
    f"<img src=\"cid:{LOGO_CID}\" alt=\"Miraglia-BI\" title=\"miraglia-bi.com\" "
    "width=\"64\" height=\"67\" style=\"width:64px; height:67px; display:block\">"
    "</a></span></td>"
    "<td style=\"border-left:3px solid rgb(74,167,46); padding-left:14px; vertical-align:middle\">"
    "<span style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt\">"
    "<b>Raoul Elias Miraglia</b><br>"
    "Microsoft Power Platform App Maker<br>"
    "Microsoft Power Automate RPA Developer<br>"
    "Tel. +41 76 674 30 91<br>"
    "mail: <a href=\"mailto:raoul@miraglia-bi.com\">raoul@miraglia-bi.com</a><br>"
    "web: <a href=\"https://miraglia-bi.com\">miraglia-bi.com</a>"
    "</span></td>"
    "</tr></tbody></table>"
)


def p(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:4px 0px\">{text}</p>"
    )


GRUSS = (
    "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
    "color:rgb(34,34,34); line-height:1.5; margin:16px 0px 4px\">"
    "Mit freundlichen Grüssen<br>Raoul</p>"
)


REPLY = {
    "search_subject": "AW: Abschlusszeugnis für Kunz Max",
    "from": "personal@mvm-ag.ch",
    "after": "2026-06-02T00:00:00Z",
    "body": (
        p("Hallo Vloriana")
        + p(
            "Danke für deinen Hinweis. Ich habe die Zeugnis-Generierung "
            "entsprechend angepasst — das scharfe S kommt ab sofort nicht mehr "
            "vor und wird durchgängig als „ss&#8220; geschrieben."
        )
        + p("Bei weiteren Auffälligkeiten melde dich gerne direkt.")
        + GRUSS
        + SIGNATURE_HTML
    ),
}


def get_token():
    return _ac_get_token(SCOPES)


def find_msg(token, subject, from_addr, after):
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"{GRAPH}/me/messages"
        f"?$select=id,subject,receivedDateTime,from"
        f"&$top=50&$orderby=receivedDateTime desc"
    )
    seen = 0
    while url and seen < 300:
        r = requests.get(url, headers=headers, timeout=30)
        if not r.ok:
            return None
        data = r.json()
        for m in data.get("value", []):
            seen += 1
            frm = ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
            subj = (m.get("subject") or "").strip()
            dt = m.get("receivedDateTime") or ""
            if frm == from_addr.lower() and subj == subject and dt >= after:
                return m
        url = data.get("@odata.nextLink")
    return None


def delete_existing_drafts(token, original_subject):
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"{GRAPH}/me/mailFolders/drafts/messages"
        f"?$select=id,subject"
        f"&$top=50&$orderby=createdDateTime desc"
    )
    r = requests.get(url, headers=headers, timeout=30)
    if not r.ok:
        return 0
    deleted = 0
    base = original_subject
    bare = base[4:] if base.lower().startswith("aw: ") or base.lower().startswith("re: ") else base
    for m in r.json().get("value", []):
        subj = (m.get("subject") or "").strip()
        for variant in (f"RE: {base}", f"AW: {base}", f"RE: {bare}", f"AW: {bare}"):
            if subj == variant:
                dr = requests.delete(f"{GRAPH}/me/messages/{m['id']}", headers=headers, timeout=30)
                if dr.ok:
                    print(f"  🗑  Alten Draft gelöscht: „{subj}\"")
                    deleted += 1
                break
    return deleted


def create_reply_draft(token, msg_id, html_body):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    r = requests.post(f"{GRAPH}/me/messages/{msg_id}/createReply", headers=headers, timeout=30)
    if not r.ok:
        print(f"  ⚠ createReply HTTP {r.status_code}: {r.text[:300]}")
        return None, None
    draft = r.json()
    draft_id = draft["id"]
    existing_body = draft.get("body", {}).get("content", "") or ""
    patch = {"body": {"contentType": "HTML", "content": html_body + existing_body}}
    r2 = requests.patch(f"{GRAPH}/me/messages/{draft_id}", headers=headers, json=patch, timeout=30)
    return draft_id, draft.get("subject", "")


def attach_inline_logo(token, draft_id, logo_bytes):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "miraglia_logo.png",
        "contentType": "image/png",
        "isInline": True,
        "contentId": LOGO_CID,
        "contentBytes": base64.b64encode(logo_bytes).decode("ascii"),
    }
    r = requests.post(
        f"{GRAPH}/me/messages/{draft_id}/attachments",
        headers=headers, json=payload, timeout=30,
    )
    return r.ok


def main():
    # CLIENT_ID/TENANT_ID werden in auth_common.py mit Defaults + Env-Overrides geprüft.
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    token = get_token()

    print("Lösche evtl. bestehende Drafts (auch falsch adressierte Nicole-Drafts) …")
    delete_existing_drafts(token, REPLY["search_subject"])

    print(f"\n→ Suche: „{REPLY['search_subject']}\" (von {REPLY['from']})")
    msg = find_msg(token, REPLY["search_subject"], REPLY["from"], REPLY["after"])
    if not msg:
        sys.exit("✗ Original-Mail nicht gefunden.")
    print(f"  ✓ Original: {msg['receivedDateTime'][:19]}")

    draft_id, subj = create_reply_draft(token, msg["id"], REPLY["body"])
    if not draft_id:
        sys.exit("✗ Draft-Erstellung fehlgeschlagen.")
    print(f"  ✓ Draft: „{subj}\"")

    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")

    print("\nFertig. Draft liegt im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
