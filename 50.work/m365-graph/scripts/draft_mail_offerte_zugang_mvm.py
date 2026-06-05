#!/usr/bin/env python3
"""
draft_mail_offerte_zugang_mvm.py
---------------------------------
Erstellt einen NEUEN Mail-Entwurf an Reto Limacher (TO), Remo Pfister (TO),
Sascha Ziswiler (TO), Giovanni Miraglia (CC), in dem wir vor dem Kickoff
um zwei Dinge bitten:

  1. Datenschutz-OK für eine read-only Sample-Auswertung der letzten ~500
     eingegangenen Mails auf `offerte@mvm-ag.ch`.
  2. Technischen Zugriff: Outlook-Vollzugriff für Raoul auf die Shared
     Mailbox + Admin-Consent für die Permission `Mail.Read.Shared` der
     bestehenden Miraglia-BI-App im MVM-Tenant.

Hintergrund: Giovanni hat im Feedback vom 04.06.2026 vorgeschlagen, vor
dem Kickoff mit Reto echte Daten zu sammeln (welche Architekturbüros,
welche Plan-Tagging-Quoten, DE/IT-Verhältnis, Anhang vs. Link) statt
Reto schätzen zu lassen.

Signatur + Logo wie in draft_replies_mvm.py (Inline-CID).
Idempotenz: alter Draft mit identischem Subject wird vor Neuanlage gelöscht.

Aufruf:
  python3 draft_mail_offerte_zugang_mvm.py
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

SUBJECT = (
    "KI-Ausmass MVM — vor dem Kickoff: read-only Sample-Auswertung "
    "offerte@mvm-ag.ch?"
)

TO_RECIPIENTS = [
    {"emailAddress": {"address": "r.limacher@mvm-ag.ch", "name": "Reto Limacher"}},
    {"emailAddress": {"address": "r.pfister@mvm-ag.ch", "name": "Remo Pfister"}},
    {"emailAddress": {"address": "s.ziswiler@mvm-ag.ch", "name": "Sascha Ziswiler"}},
]
CC_RECIPIENTS = [
    {"emailAddress": {"address": "giovanni@miraglia-bi.com", "name": "Giovanni Miraglia"}},
]


# Signatur 1:1 nachgebaut nach Giovannis Outlook-Signatur (Logo + grüner Vertikal-Strich)
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
    "Liebe Grüsse<br>Raoul</p>"
)


def p(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:4px 0px\">{text}</p>"
    )


def h2(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:12pt; "
        f"color:rgb(0,40,90); line-height:1.4; margin:18px 0px 6px; font-weight:bold\">{text}</p>"
    )


def ul(items: list[str]) -> str:
    body = "".join(
        f"<li style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:2px 0px\">{it}</li>"
        for it in items
    )
    return f"<ul style=\"margin:4px 0px 8px 24px; padding:0\">{body}</ul>"


# ─── Body ─────────────────────────────────────────────────────────────

BODY = (
    p("Hallo Reto, hallo Remo, hallo Sascha")
    + p(
        "Kurz vor dem Kickoff zum KI-Ausmass-Projekt eine Anfrage zur "
        "Datengrundlage."
    )
    + p(
        "Giovanni hat in seinem Feedback gestern vorgeschlagen, dass wir vor "
        "dem Kickoff zwei wichtige Fragen mit Zahlen statt Bauchgefühl beantworten:"
    )
    + ul([
        "Wie viele Architekturbüros liefern Pläne mit ausgewerteten Räumen "
        "(Bodenfläche / Raumhöhe als Text im Plan) — und wie viele nicht? Davon "
        "hängt direkt ab, ob das Tool ab Tag 1 nützt oder erst mit teurer "
        "Vision-AI greift.",
        "Wie häufig kommen italienische / französische Anfragen ohne SIA-CRBX "
        "(z. B. aus dem Tessin) — eigener Scope-Strang ja oder nein?",
    ])
    + p(
        "Statt euch dazu zu interviewen, würden wir das gerne empirisch "
        "messen: ein read-only Scan der letzten ~500 eingegangenen Mails auf "
        "<b><code>offerte@mvm-ag.ch</code></b>, danach 5–10 zufällige Anfragen "
        "pro Top-Büro als Plan-Stichprobe nachladen."
    )

    + h2("Was wir technisch machen würden")
    + ul([
        "Read-only Zugriff via Microsoft Graph auf <code>offerte@mvm-ag.ch</code>",
        "Für jede Mail extrahieren: Absender-Domain, Datum, Subject, Anhang-"
        "Liste (Name + Typ + Grösse), Body-Links (WeTransfer / SharePoint), "
        "Sprache (DE / IT / FR per Heuristik)",
        "Aggregat-Report: Top 20 Architekturbüros, CRBX-Quote, "
        "Anhang-vs-Link-Quote, Sprach-Verteilung, Anfragen pro Monat",
        "Für 5–10 Anfragen pro Top-Büro: Anhänge (oder Cloud-Link-Inhalte) "
        "ziehen, ein Plan-PDF mit unserer Pipeline scannen — Quote „Plan-"
        "anfreundlich“ vs. „Plan-feindlich“ pro Büro",
    ])

    + h2("Was wir ausdrücklich NICHT machen")
    + ul([
        "Keine Mail-Inhalte ins Vault / in Logs schreiben (nur Metadaten + "
        "Anhang-Listen, aggregiert)",
        "Keine Weitergabe von Architekten-/Bauherrn-Identitäten ausserhalb von "
        "uns dreien (Reto, Remo, Giovanni, Raoul) und dem internen Bericht",
        "Kein Schreiben in die Mailbox (kein Senden, kein Verschieben, kein "
        "Antworten, keine Markierungen)",
        "Roh-Scan-Daten (JSON-Lines) liegen lokal verschlüsselt auf meinem "
        "Mac, sind nicht im Git / Cloud-Backup",
    ])

    + h2("Was wir konkret von euch brauchen")
    + p("<b>Reto</b> — Datenschutz-OK:")
    + ul([
        "Kurzes Einverständnis, dass wir die letzten ~500 Mails der Offert-"
        "Mailbox scannen dürfen (read-only, Aggregat, lokal). Output ist ein "
        "Markdown-Bericht, den wir gemeinsam im Kickoff anschauen.",
    ])
    + p("<b>Remo</b> — technischer Zugriff (Exchange + Entra):")
    + ul([
        "<b>Exchange Admin Center → Postfächer → <code>offerte@mvm-ag.ch</code> "
        "→ Postfachdelegierung → Vollzugriff</b>: Raoul "
        "(<code>raoul@miraglia-bi.com</code>) als externe Adresse hinzufügen — "
        "alternativ als MVM-Guest-User, je nachdem was bei euch der etablierte "
        "Pfad ist.",
        "<b>Entra ID → Enterprise Applications → Admin Consent</b> für die "
        "bestehende Miraglia-BI-App (Client-ID "
        "<code>0c8e309d-d02e-4244-ae2a-dbb5551cb550</code>) im MVM-Tenant "
        "(<code>3becd9bb-f602-4c6b-8e86-f1e42db365ea</code>) — nur die "
        "delegierte Permission <code>Mail.Read.Shared</code>. Direkter Consent-"
        "Link kann ich liefern sobald du grünes Licht gibst.",
        "Alternative falls einfacher: kurze Teams-Session, wir machen es "
        "gemeinsam in 10 Minuten.",
    ])
    + p("<b>Sascha</b> — zur Info:")
    + ul([
        "Falls du Bedenken hast, gerne kurz melden. Sonst läuft das schlank "
        "zwischen Reto, Remo und uns.",
    ])

    + h2("Zeitfenster")
    + p(
        "Ideal bis <b>Mittwoch Mittag nächste Woche</b>, damit ich den Bericht "
        "vor dem Kickoff am Donnerstag/Freitag mitbringen kann. Wenn schneller "
        "geht: ich kann den Scan und Bericht in 2–3 Stunden ab Zugriff "
        "liefern."
    )

    + p(
        "Bei Fragen — Datenschutz-Detail, technische Alternative, Scope-Frage "
        "— kurz Teams-Chat oder Tel <a href=\"tel:+41766743091\">+41 76 674 "
        "30 91</a>."
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


def create_draft_message(token: str, subject: str, html_body: str) -> str | None:
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
        "toRecipients": TO_RECIPIENTS,
        "ccRecipients": CC_RECIPIENTS,
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
    print("📧 KI-Ausmass MVM — Mail-Entwurf „offerte-Zugang“ erstellen")
    print("=" * 70)
    print(f"   To:  Reto Limacher    <r.limacher@mvm-ag.ch>")
    print(f"        Remo Pfister     <r.pfister@mvm-ag.ch>")
    print(f"        Sascha Ziswiler  <s.ziswiler@mvm-ag.ch>")
    print(f"   Cc:  Giovanni Miraglia <giovanni@miraglia-bi.com>")
    print(f"   Subj: {SUBJECT}")
    print()

    token = _ac_get_token(SCOPES)

    # Idempotenz: alter Draft mit gleichem Subject vorher löschen
    n_deleted = delete_existing_drafts_with_subject(token, SUBJECT)
    if n_deleted > 0:
        print()

    msg_id = create_draft_message(token, SUBJECT, BODY)
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
