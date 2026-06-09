#!/usr/bin/env python3
"""
draft_giovanni_darkmode_signatur.py
-----------------------------------
Erstellt einen Draft an Giovanni Miraglia mit konkreten Hinweisen, wie er
seine Outlook-Signatur dark-mode-tauglich machen kann.

Hintergrund: Raoul hat seine eigene Signatur dark-mode-stabil eingerichtet —
bei Giovanni kommt sie im Dark-Mode noch als heller Block durchgeschlagen.
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


SUBJECT = "Signatur dark-mode-tauglich machen"
RECIPIENT = "giovanni@miraglia-bi.com"


BODY_HTML = (
    p("Hoi Papi")
    + p(
        "Habe das Dark-Mode-Thema bei meiner Signatur jetzt sauber: bei mir bleibt "
        "sie auch in Outlook Mac / iOS / Web mit Dark-Mode lesbar und passt sich an. "
        "Bei dir kommt sie noch als heller Block durchgeschlagen — hier die drei "
        "Stellen, an denen es typischerweise hakt:"
    )
    + (
        "<ol style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        "color:rgb(34,34,34); line-height:1.5; margin:8px 0px; padding-left:22px\">"
        "<li style=\"margin-bottom:8px\">"
        "<b>Logo-PNG mit weissem Hintergrund.</b> Wenn unser Globus-Logo als PNG "
        "mit weisser Bounding-Box hinterlegt ist, bleibt es immer ein weisses "
        "Quadrat — auch wenn der Mail-Client dunkel rendert. Lösung: dasselbe "
        "Logo nochmals exportieren mit <b>echtem transparenten Hintergrund</b> "
        "(Photoshop/GIMP/Online-Tool) und im Outlook-Signatur-Editor das Bild "
        "ersetzen."
        "</li>"
        "<li style=\"margin-bottom:8px\">"
        "<b>Explizite weisse Hintergründe im Signatur-HTML.</b> Im Outlook → "
        "Datei → Optionen → E-Mail → Signaturen → deine Signatur → „Bearbeiten\". "
        "Alternativ direkt die HTML-Datei unter "
        "<code>C:\\Users\\&lt;user&gt;\\AppData\\Roaming\\Microsoft\\Signatures\\&lt;name&gt;.htm</code> "
        "öffnen und nach <code>background-color:white</code>, "
        "<code>bgcolor=\"#ffffff\"</code> oder <code>background:#fff</code> "
        "suchen und entfernen. Die Tabelle erbt dann den Hintergrund vom "
        "Mail-Client und passt sich an Light/Dark an."
        "</li>"
        "<li>"
        "<b>Schriftfarbe ohne explizite Vorgabe.</b> Wenn der Text keine "
        "<code>color:</code>-Vorgabe hat, lässt Outlook (Mac/Web) im Dark-Mode "
        "den Hintergrund hell, macht aber den Text trotzdem dunkel → schwer "
        "lesbar. Setze auf den äusseren <code>&lt;span&gt;</code> ein "
        "<code>color:#1f1f1f</code> (oder ähnlichen mittel-dunklen Wert). Im "
        "Light-Mode wirkt das normal, im Dark-Mode rendert Outlook ihn "
        "automatisch passend hell."
        "</li>"
        "</ol>"
    )
    + p(
        "Schnellster Test: nachdem du die Anpassungen gemacht hast, schick mir "
        "eine kurze Test-Mail. Ich öffne sie im iOS-Outlook (Dark-Mode) und im "
        "Outlook for Mac und sage dir, ob sie sauber rendert."
    )
    + p("Bei Fragen ruf mich gerne an.")
    + GRUSS
    + SIGNATURE_HTML
)


def get_token():
    return _ac_get_token(SCOPES)


def delete_existing_drafts(token):
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
                print(f"  🗑  Alten Draft gelöscht: „{subj}\"")
                deleted += 1
    return deleted


def create_draft(token):
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
    return r.ok


def main():
    # CLIENT_ID/TENANT_ID werden in auth_common.py mit Defaults + Env-Overrides geprüft.
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    token = get_token()

    print("Räume alte Drafts mit gleichem Subject auf …")
    delete_existing_drafts(token)

    print(f"\n→ Erstelle Draft an {RECIPIENT}")
    draft_id = create_draft(token)
    if not draft_id:
        sys.exit("✗ Draft-Erstellung fehlgeschlagen.")
    print(f"  ✓ Draft: „{SUBJECT}\"")

    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")

    print("\nFertig. Draft liegt im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
