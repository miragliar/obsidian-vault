#!/usr/bin/env python3
"""
draft_reply_remo_garofano_2026-06-15.py
---------------------------------------
Nachzügler-Draft zum Garofano-Foto-Upload-Strang.

Reply auf den letzten Mail in der „Neue Regie App - Giuseppe Garofano"-Thread
(Remo Pfister, 2026-06-11 07:02 „Sehr gut, Danke für die Info…"), in dem ich
heute die Diagnose nachliefere: Ursache (SharePoint-Liste nicht zuverlässig
offline-fähig auf nativem Power Apps Mobile), Quick-Fix bleibt Teams,
mittelfristige Lösung (Migration Foto-Ablage SharePoint → Dataverse) nach
Aestico/Domus.

Pattern: 1:1 nach draft_replies_remo_2026-06-15.py
"""
import base64
import sys
from pathlib import Path

import requests

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


BODY = (
    p("Hoi Remo")
    + p(
        "Kurzes Update zum Garofano-Thema:"
    )
    + p(
        '<b>Fehlermeldung beim App-Start</b> („Fehler beim Abrufen von '
        'Daten aus dem Netzwerk") — ist <b>gefixt</b>. Ursache lag bei '
        'einem Office-365-Gruppen-Aufruf beim Start, der offline nicht '
        'funktioniert hat. Habe das mit einer hinterlegten Fallback-Liste '
        'abgefangen — die Meldung sollte nicht mehr auftauchen.'
    )
    + p(
        "<b>Foto-Upload</b> — bleibt vorerst <b>wie gehabt</b>: Bilder "
        "laufen weiterhin über die SharePoint-Liste, und die ist offline "
        "auf der nativen Power-Apps-App nicht zuverlässig. Garofano (und "
        "alle anderen mit demselben Symptom) sollen die App weiterhin "
        "über Teams nutzen — dort funktioniert es."
    )
    + GRUSS
    + SIGNATURE_HTML
)


DRAFT = {
    "search_subject": "AW: Neue Regie App - Giuseppe Garofano",
    "from": "r.pfister@mvm-ag.ch",
    "after": "2026-06-11T00:00:00Z",
    "body": BODY,
    "label": "Garofano Foto-Upload Update",
}


def get_token():
    return _ac_get_token(SCOPES)


def find_msg(token: str, subject: str, from_addr: str, after: str):
    headers = {"Authorization": f"Bearer {token}"}
    url = (
        f"{GRAPH}/me/messages"
        f"?$select=id,subject,receivedDateTime,from"
        f"&$top=50"
        f"&$orderby=receivedDateTime desc"
    )
    seen = 0
    while url and seen < 300:
        r = requests.get(url, headers=headers, timeout=30)
        if not r.ok:
            print(f"  ⚠ HTTP {r.status_code}: {r.text[:300]}")
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


def delete_existing_drafts(token: str, original_subject: str):
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
        subj = (m.get("subject") or "").strip()
        if subj in (f"RE: {original_subject}",
                    f"AW: {original_subject}",
                    original_subject):
            dr = requests.delete(f"{GRAPH}/me/messages/{m['id']}",
                                 headers=headers, timeout=30)
            if dr.ok:
                print(f"  🗑  Alten Draft gelöscht: „{subj}\"")
                deleted += 1
    return deleted


def create_reply_draft(token: str, msg_id: str, html_body: str):
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    r = requests.post(f"{GRAPH}/me/messages/{msg_id}/createReply",
                      headers=headers, timeout=30)
    if not r.ok:
        print(f"  ⚠ createReply HTTP {r.status_code}: {r.text[:400]}")
        return None, None
    draft = r.json()
    draft_id = draft["id"]
    existing_body = draft.get("body", {}).get("content", "") or ""
    new_html = html_body + existing_body
    r2 = requests.patch(
        f"{GRAPH}/me/messages/{draft_id}",
        headers=headers,
        json={"body": {"contentType": "HTML", "content": new_html}},
        timeout=30,
    )
    if not r2.ok:
        print(f"  ⚠ patch HTTP {r2.status_code}: {r2.text[:400]}")
    return draft_id, draft.get("subject", "")


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

    print("\nLösche evtl. bestehende Drafts mit gleichem Subject …")
    deleted = delete_existing_drafts(token, DRAFT["search_subject"])
    print(f"  → {deleted} alte Drafts gelöscht\n")

    print(f"→ [{DRAFT['label']}] Suche: „{DRAFT['search_subject']}\"")
    msg = find_msg(token, DRAFT["search_subject"], DRAFT["from"], DRAFT["after"])
    if not msg:
        sys.exit("  ✗ Original-Mail nicht gefunden — abgebrochen.")
    print(f"  ✓ Original: {msg['receivedDateTime'][:19]}")
    draft_id, subj = create_reply_draft(token, msg["id"], DRAFT["body"])
    if not draft_id:
        sys.exit("  ✗ Draft-Erstellung fehlgeschlagen")
    print(f"  ✓ Draft: „{subj}\"")
    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")
    else:
        print("  ⚠ Inline-Logo NICHT angehängt")

    print("\nFertig — 1 Entwurf im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
