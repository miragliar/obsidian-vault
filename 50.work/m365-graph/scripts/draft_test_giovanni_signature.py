#!/usr/bin/env python3
"""
draft_test_giovanni_signature.py
--------------------------------
Erstellt einen Test-Draft an Giovanni Miraglia, um zu verifizieren ob die
Outlook-Auto-Signatur bei Graph-erstellten Drafts dazukommt (→ zwei Signaturen)
oder nicht (→ eine Signatur).

Unterschied zu den Reply-Skripten:
- POST /me/messages (NEUE Mail, keine Reply)
- toRecipients gesetzt
- Subject + Body + Inline-Logo wie gehabt
"""
import base64
import os
import sys
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
TENANT_ID = os.environ.get("M365_TENANT_ID", "")
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".token_cache.bin"
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


BODY_HTML = (
    p("Hoi Papi")
    + p(
        "Kurzer Test, ob meine Outlook-Auto-Signatur bei Graph-erstellten Drafts "
        "dazukommt (würde dann zwei Signaturen ergeben) oder nicht."
    )
    + p(
        "Wenn du diese Mail bekommst mit <b>genau einer</b> Signatur unten (Logo "
        "Miraglia-BI + grüne Trennlinie + meine Daten), passt mein Setup. Wenn du "
        "<b>zwei</b> Signaturen siehst, sag bitte kurz Bescheid — dann strippe ich "
        "die Script-Signatur und überlasse das Outlook."
    )
    + p("Danke.")
    + GRUSS
    + SIGNATURE_HTML
)


SUBJECT = "Test – Signatur-Prüfung Graph-Draft"
RECIPIENT = "giovanni@miraglia-bi.com"


def get_token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    for acc in app.get_accounts():
        r = app.acquire_token_silent(SCOPES, account=acc)
        if r:
            if cache.has_state_changed:
                CACHE_FILE.write_text(cache.serialize())
            return r["access_token"]
    sys.exit("Kein Token im Cache.")


def delete_existing_test_drafts(token):
    """Räumt evtl. ältere Test-Drafts mit gleichem Subject auf."""
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
    for m in r.json().get("value", []):
        subj = (m.get("subject") or "").strip()
        if subj == SUBJECT:
            dr = requests.delete(f"{GRAPH}/me/messages/{m['id']}", headers=headers, timeout=30)
            if dr.ok:
                print(f"  🗑  Alten Test-Draft gelöscht: „{subj}\"")
                deleted += 1
    return deleted


def create_test_draft(token):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "subject": SUBJECT,
        "body": {"contentType": "HTML", "content": BODY_HTML},
        "toRecipients": [{"emailAddress": {"address": RECIPIENT}}],
    }
    r = requests.post(f"{GRAPH}/me/messages", headers=headers, json=payload, timeout=30)
    if not r.ok:
        print(f"  ⚠ createMessage HTTP {r.status_code}: {r.text[:300]}")
        return None
    return r.json()["id"]


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
    if not r.ok:
        print(f"  ⚠ Inline-Logo HTTP {r.status_code}: {r.text[:300]}")
        return False
    return True


def main():
    if not CLIENT_ID or not TENANT_ID:
        sys.exit("M365_CLIENT_ID / M365_TENANT_ID nicht gesetzt.")
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    token = get_token()

    print("Räume alte Test-Drafts auf …")
    delete_existing_test_drafts(token)

    print(f"\n→ Erstelle neuen Test-Draft an {RECIPIENT}")
    draft_id = create_test_draft(token)
    if not draft_id:
        sys.exit("✗ Draft-Erstellung fehlgeschlagen.")
    print(f"  ✓ Draft: „{SUBJECT}\"")

    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")

    print("\nFertig. Draft liegt im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
