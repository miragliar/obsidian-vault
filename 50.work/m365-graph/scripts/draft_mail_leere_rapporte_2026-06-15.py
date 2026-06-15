#!/usr/bin/env python3
"""
draft_mail_leere_rapporte_2026-06-15.py
---------------------------------------
Neue Mail (kein Reply) an die drei Ersteller der leeren Geister-Rapporte
in der Regie-App, mit Bitte um Bereinigung. Remo Pfister in Cc.

Subject:  Regie-App: leere Rapporte in eurer Liste — kurz bereinigen bitte

To:
  - Dominik Bieri  (mvmdb@mvm-ag.ch)      → 26-1026, 26-1027, 26-1067
  - Roman Saxer    (r.saxer@mvm-ag.ch)    → 26-1047, 26-1062
  - Tobias Nowak   (t.nowak@mvm-ag-zug.ch) → 26-1048

Cc:
  - Remo Pfister   (r.pfister@mvm-ag.ch)

Pattern: 1:1 nach draft_reply_remo_garofano_2026-06-15.py, aber:
- statt createReply: POST /me/messages (neuer Draft)
- explizite toRecipients + ccRecipients
"""
import base64
import sys
from pathlib import Path

import requests

from auth_common import GRAPH, get_token as _ac_get_token

SCOPES = ["User.Read", "Mail.ReadWrite"]

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

GRUSS = (
    "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
    "color:rgb(34,34,34); line-height:1.5; margin:16px 0px 4px\">"
    "Gruss<br>Raoul</p>"
)


def p(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:4px 0px\">{text}</p>"
    )


SUBJECT = "Regie-App: leere Rapporte in eurer Liste — kurz bereinigen bitte"

TO = [
    {"emailAddress": {"address": "mvmdb@mvm-ag.ch",      "name": "Dominik Bieri"}},
    {"emailAddress": {"address": "r.saxer@mvm-ag.ch",    "name": "Roman Saxer"}},
    {"emailAddress": {"address": "t.nowak@mvm-ag-zug.ch","name": "Tobias Nowak"}},
]

CC = [
    {"emailAddress": {"address": "r.pfister@mvm-ag.ch", "name": "Remo Pfister"}},
]

BODY = (
    p("Hoi zusammen")
    + p(
        "Ich schreibe euch wegen ein paar Rapporten in der Regie-App, "
        "denen die Baustellen-Bezeichnung fehlt. Das war ein Bug von meiner "
        "Seite — ich hatte versehentlich zugelassen, dass beim Anlegen eines "
        "neuen Rapports auf „Weiter“ geklickt werden konnte, bevor eine "
        "Baustelle ausgewählt war. Der Rapport wurde dann ohne Baustelle "
        "gespeichert und bleibt seither in der Liste stehen."
    )
    + p(
        "Inzwischen ist das gefixt: der Weiter-Button bleibt blockiert, "
        "solange Baustelle, Kalenderwoche oder Empfänger-Typ fehlen. "
        "Übrig bleibt das Aufräumen des bestehenden Bestands — dafür "
        "brauche ich euch kurz."
    )
    + p("<b>Folgende Rapporte sind bei euch betroffen:</b>")
    + p(
        "• Dominik Bieri: <b>26-1026</b>, <b>26-1027</b>, <b>26-1067</b><br>"
        "• Roman Saxer: <b>26-1047</b>, <b>26-1062</b><br>"
        "• Tobias Nowak: <b>26-1048</b>"
    )
    + p("<b>Pro Rapport habt ihr zwei Möglichkeiten:</b>")
    + p(
        "<b>1. Löschen oder archivieren</b> — falls ihr nicht mehr wisst, "
        "wofür der Rapport gedacht war. Schnell und sauber."
    )
    + p(
        "<b>2. Im besten Fall: Baustelle nachtragen</b> — falls ihr euch "
        "noch erinnert, für welche Baustelle der Rapport war: in der "
        "PDF-Ansicht oben rechts den <b>braunen Edit-Knopf</b> drücken und "
        "die richtige Baustelle auswählen. Dann ist der Rapport gerettet "
        "und ihr könnt ihn normal weiterverwenden."
    )
    + p(
        "<b>Heads-up für die Zukunft:</b> falls ihr in der App seht, dass "
        "nach der Rapport-Nummer und dem Komma keine Baustellen-Bezeichnung "
        "erscheint — meldet euch bitte <b>sofort</b> bei mir. Eigentlich "
        "sollte das nicht mehr passieren, aber wenn doch, läuft noch "
        "irgendwo etwas schief und ich muss nochmal ran."
    )
    + p("Bei Fragen einfach direkt zu mir.")
    + GRUSS
    + SIGNATURE_HTML
)


def get_token():
    return _ac_get_token(SCOPES)


def delete_existing_drafts(token: str, subject: str):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{GRAPH}/me/mailFolders/drafts?$select=id",
                     headers=headers, timeout=30)
    if not r.ok:
        return 0
    drafts_id = r.json().get("id")
    if not drafts_id:
        return 0
    url = (
        f"{GRAPH}/me/mailFolders/{drafts_id}/messages"
        f"?$select=id,subject,createdDateTime"
        f"&$top=50"
        f"&$orderby=createdDateTime desc"
    )
    r = requests.get(url, headers=headers, timeout=30)
    if not r.ok:
        return 0
    deleted = 0
    for m in r.json().get("value", []):
        if (m.get("subject") or "").strip() == subject:
            dr = requests.delete(f"{GRAPH}/me/messages/{m['id']}",
                                 headers=headers, timeout=30)
            if dr.ok:
                print(f"  🗑  Alten Draft gelöscht: „{m.get('subject')}\"")
                deleted += 1
    return deleted


def create_new_draft(token: str):
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    payload = {
        "subject": SUBJECT,
        "body": {"contentType": "HTML", "content": BODY},
        "toRecipients": TO,
        "ccRecipients": CC,
    }
    r = requests.post(f"{GRAPH}/me/messages", headers=headers,
                      json=payload, timeout=30)
    if not r.ok:
        print(f"  ⚠ create draft HTTP {r.status_code}: {r.text[:400]}")
        return None
    return r.json().get("id")


def attach_inline_logo(token: str, draft_id: str, logo_bytes: bytes):
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    payload = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "miraglia_logo.png",
        "contentType": "image/png",
        "isInline": True,
        "contentId": LOGO_CID,
        "contentBytes": base64.b64encode(logo_bytes).decode("ascii"),
    }
    r = requests.post(f"{GRAPH}/me/messages/{draft_id}/attachments",
                      headers=headers, json=payload, timeout=30)
    if not r.ok:
        print(f"  ⚠ Inline-Logo HTTP {r.status_code}: {r.text[:300]}")
        return False
    return True


def main():
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    print(f"Logo geladen: {LOGO_FILE.name} ({len(logo_bytes)} bytes)")

    token = get_token()

    print("\nLösche evtl. bestehenden Draft mit gleichem Subject …")
    deleted = delete_existing_drafts(token, SUBJECT)
    print(f"  → {deleted} alter Draft gelöscht\n")

    print(f"→ Erstelle neuen Draft: „{SUBJECT}\"")
    draft_id = create_new_draft(token)
    if not draft_id:
        sys.exit("  ✗ Draft-Erstellung fehlgeschlagen")
    print(f"  ✓ Draft erstellt")
    print(f"  To: {', '.join(t['emailAddress']['name'] for t in TO)}")
    print(f"  Cc: {', '.join(c['emailAddress']['name'] for c in CC)}")
    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")
    else:
        print("  ⚠ Inline-Logo NICHT angehängt")

    print("\nFertig — 1 Entwurf im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
