#!/usr/bin/env python3
"""
draft_mail_rafael_mottl_aestico_2026-06-16.py
----------------------------------------------
Legt einen NEUEN Mail-Entwurf an Rafael Mottl (aestico.ch) im Drafts-Ordner
von raoul@miraglia-bi.com an. Remo Pfister (MVM AG) ist im CC.

Kontext (2026-06-16):
- Domus-Revision 28 geht heute live → Aestico-Schnittstelle bei MVM AG ist
  ab heute offen (siehe [[50.work/projekte/MVM-AG/Regieapp-Aestico-Domus-Import]]).
- Auftrag von Remo Pfister (Mail 2026-06-10): bis 31.10.2026 vollautomatisierte
  Rechnungserstellung aus Regie-App → Domus über Aestico-Schnittstelle.
- Lizenz Optiwork ↔ MVM Ziffer 6 (signiert 2026-06-15) erlaubt die Nutzung.
- Raoul / Giovanni / Alessandro Castelli hatten Rafael vor ca. 1.5 Jahren im
  Büro getroffen — damals Doku erhalten (Google-Drive-Ordner-Link).

Ziel der Mail:
- Status-Update (Schnittstelle ab heute bei MVM offen, wir wollen sie nutzen)
- Frage nach aktueller Doku (oder ob die damals geteilte noch gilt)
- Remo Pfister in CC

Signatur + Logo wie in den anderen draft_mail_*.py-Skripten.
Idempotenz: alter Draft mit identischem Subject wird vor Neuanlage gelöscht.

Aufruf:
  python3 draft_mail_rafael_mottl_aestico_2026-06-16.py
"""
import base64
import sys
from pathlib import Path

import requests

# Auth via macOS Keychain (v2-Pattern) — siehe auth_common.py
from auth_common import get_token as _ac_get_token, GRAPH

SCOPES = ["User.Read", "Mail.Read", "Mail.ReadWrite"]

SCRIPT_DIR = Path(__file__).resolve().parent
LOGO_FILE = SCRIPT_DIR / "miraglia_logo.png"
LOGO_CID = "miragliabi-logo"

SUBJECT = "Aestico-Schnittstelle zu BRZ — bei MVM AG ab heute offen, Frage zur Doku"

TO_RECIPIENTS = [
    {"emailAddress": {"address": "rafael.mottl@aestico.ch", "name": "Rafael Mottl"}},
]
CC_RECIPIENTS = [
    {"emailAddress": {"address": "r.pfister@mvm-ag.ch", "name": "Remo Pfister"}},
]


# Signatur 1:1 wie in den anderen draft_mail_*.py-Skripten
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
    "Vielen Dank und liebe Grüsse<br>Raoul</p>"
)


def p(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:4px 0px\">{text}</p>"
    )


BODY = (
    p("Hoi Rafael")
    + p(
        "Ich hoffe, dir geht es gut. Wir hatten uns vor ca. 1.5 Jahren bei "
        "dir im Büro getroffen, zusammen mit Alessandro Castelli und meinem "
        "Vater Giovanni Miraglia."
    )
    + p(
        "Worum es mir in dieser Mail geht: Die Aestico-Schnittstelle zu BRZ "
        "wird bei der MVM AG ab heute (mit der Domus-Revision 28) offen "
        "sein — und wir möchten sie nutzen."
    )
    + p(
        "Konkret: Über meine Power-Platform-App werden bei MVM die "
        "Regierapporte digital erfasst. Diese sollen künftig automatisiert "
        "in eine Rechnung im Domus überführt werden. Remo Pfister (CC) "
        "hat das als ToDo bis Ende Oktober gesetzt; ich werde mich in den "
        "nächsten Wochen — voraussichtlich nach meinen Ferien — daran setzen."
    )
    + p(
        "Wir hatten nach unserem damaligen Treffen von dir eine Doku zur "
        "Schnittstelle erhalten. Gibt es inzwischen eine aktuellere Version, "
        "oder kann ich die damals geteilte Doku weiter nutzen? Hier zur "
        "Sicherheit der Ordner, in dem die Unterlagen damals abgelegt wurden:"
    )
    + p(
        "<a href=\"https://drive.google.com/drive/folders/17C7ce0jjchkLJzKqzO-Sw-jZ0czIbhLO\">"
        "https://drive.google.com/drive/folders/17C7ce0jjchkLJzKqzO-Sw-jZ0czIbhLO"
        "</a>"
    )
    + p(
        "Wenn du sonst noch Hinweise hast — Versions-Abhängigkeiten zu "
        "Domus-Rev. 28, Sample-Import-Files, häufige Stolpersteine — sehr gerne."
    )
    + GRUSS
    + SIGNATURE_HTML
)


# ─── Graph-Helpers ───────────────────────────────────────────────────────


def delete_existing_drafts_with_subject(token: str, subject: str) -> int:
    """Löscht alte Drafts mit identischem Subject (Idempotenz)."""
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH}/me/mailFolders/drafts?$select=id",
        headers=headers,
        timeout=30,
    )
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
            dr = requests.delete(
                f"{GRAPH}/me/messages/{m['id']}",
                headers=headers,
                timeout=30,
            )
            if dr.ok:
                print(f"  🗑  Alten Draft gelöscht: „{subject}\"")
                deleted += 1
    return deleted


def create_draft_message(token: str, subject: str, html_body: str,
                         to_recipients: list[dict],
                         cc_recipients: list[dict]) -> str | None:
    """POST /me/messages → erstellt einen neuen Draft (kein Reply). Returns msg_id."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "subject": subject,
        "body": {
            "contentType": "HTML",
            "content": html_body,
        },
        "toRecipients": to_recipients,
        "ccRecipients": cc_recipients,
    }
    r = requests.post(
        f"{GRAPH}/me/messages",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not r.ok:
        print(f"  ⚠ Draft-Erstellung HTTP {r.status_code}: {r.text[:400]}")
        return None
    return r.json().get("id")


def attach_inline_logo(token: str, msg_id: str) -> bool:
    """Inline-Logo (cid:miragliabi-logo) als Attachment anhängen."""
    if not LOGO_FILE.exists():
        print(f"  ⚠ Logo-Datei fehlt: {LOGO_FILE}")
        return False
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": "miraglia_logo.png",
        "contentId": LOGO_CID,
        "isInline": True,
        "contentBytes": base64.b64encode(LOGO_FILE.read_bytes()).decode("utf-8"),
        "contentType": "image/png",
    }
    r = requests.post(
        f"{GRAPH}/me/messages/{msg_id}/attachments",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not r.ok:
        print(f"  ⚠ Attachment HTTP {r.status_code}: {r.text[:400]}")
        return False
    return True


# ─── Main ────────────────────────────────────────────────────────────────


def main() -> None:
    print("=" * 70)
    print("📧 Mail an Rafael Mottl (Aestico) — Schnittstelle MVM AG offen")
    print("=" * 70)
    print("   To:  Rafael Mottl <rafael.mottl@aestico.ch>")
    print("   Cc:  Remo Pfister <r.pfister@mvm-ag.ch>")
    print(f"   Subj: {SUBJECT}")
    print()

    token = _ac_get_token(SCOPES)

    # Idempotenz: alten Draft mit gleichem Subject löschen
    n = delete_existing_drafts_with_subject(token, SUBJECT)
    if n:
        print()

    msg_id = create_draft_message(token, SUBJECT, BODY, TO_RECIPIENTS, CC_RECIPIENTS)
    if not msg_id:
        sys.exit(1)
    print(f"✓ Draft erstellt: {msg_id}")

    if attach_inline_logo(token, msg_id):
        print(f"✓ Logo als Inline-Attachment angehängt (cid:{LOGO_CID})")

    print()
    print("Fertig — Draft liegt in Outlook unter Entwürfe.")
    print("Bitte vor dem Senden im Outlook reviewen.")


if __name__ == "__main__":
    main()
