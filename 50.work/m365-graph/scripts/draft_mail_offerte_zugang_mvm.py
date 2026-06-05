#!/usr/bin/env python3
"""
draft_mail_offerte_zugang_mvm.py
---------------------------------
Erstellt einen NEUEN Mail-Entwurf an Giovanni Miraglia (TO, alleine)
mit einem Konzept-Check für die geplante MVM-Mail.

Hintergrund: Giovanni hat im Feedback vom 04.06.2026 vorgeschlagen, vor
dem Kickoff mit Reto echte Daten zu sammeln (welche Architekturbüros,
welche Plan-Tagging-Quoten, DE/IT-Verhältnis, Anhang vs. Link) statt
Reto schätzen zu lassen. Bevor wir die Anfrage an MVM (Reto/Remo/Sascha)
rausschicken, lassen wir Giovanni 1:1 drüberschauen, ob Tonfall,
Auth-Variante und Datenschutz-Wording passen.

Auth-Variante: bestehender MVM-User mit Vollzugriff auf `offerte@mvm-ag.ch`
loggt sich einmalig 30 Sek. per Device-Code-Flow ein. Spart Exchange-
Vollzugriff-Setup + Guest-Account für Raoul.

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
    "KI-Ausmass MVM — Konzept-Check vor Versand an MVM: "
    "Sample-Auswertung offerte@mvm-ag.ch"
)

TO_RECIPIENTS = [
    {"emailAddress": {"address": "giovanni@miraglia-bi.com", "name": "Giovanni Miraglia"}},
]
CC_RECIPIENTS: list[dict] = []


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


# ─── Zitat-Block (geplante MVM-Mail eingebettet) ──────────────────────


def quote_block(html_inner: str) -> str:
    """Eingebetteter Zitatblock — visuell wie ein klassisches Mail-Zitat."""
    return (
        "<div style=\"border-left:3px solid rgb(180,180,180); "
        "padding:8px 14px; margin:8px 0px 16px; background:rgb(248,248,248)\">"
        f"{html_inner}"
        "</div>"
    )


def quoted_p(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:10.5pt; "
        f"color:rgb(60,60,60); line-height:1.45; margin:4px 0px\">{text}</p>"
    )


def quoted_ul(items: list[str]) -> str:
    body = "".join(
        f"<li style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:10.5pt; "
        f"color:rgb(60,60,60); line-height:1.45; margin:2px 0px\">{it}</li>"
        for it in items
    )
    return f"<ul style=\"margin:4px 0px 8px 24px; padding:0\">{body}</ul>"


def quoted_h(text: str) -> str:
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(0,40,90); line-height:1.4; margin:12px 0px 4px; font-weight:bold\">{text}</p>"
    )


# Der geplante MVM-Mail-Text (1:1 wie wir ihn senden würden)
MVM_MAIL_DRAFT = (
    quoted_p(
        "<b>To:</b> Reto Limacher, Remo Pfister, Sascha Ziswiler &nbsp;·&nbsp; "
        "<b>Cc:</b> Giovanni Miraglia<br>"
        "<b>Subject:</b> KI-Ausmass MVM — vor dem Kickoff: read-only "
        "Sample-Auswertung <code>offerte@mvm-ag.ch</code>?"
    )
    + quoted_p("Hallo Reto, hallo Remo, hallo Sascha")
    + quoted_p(
        "Kurz vor dem Kickoff zum KI-Ausmass-Projekt eine Anfrage zur "
        "Datengrundlage."
    )
    + quoted_p(
        "Giovanni hat in seinem Feedback gestern vorgeschlagen, dass wir vor "
        "dem Kickoff zwei wichtige Fragen mit Zahlen statt Bauchgefühl beantworten:"
    )
    + quoted_ul([
        "Wie viele Architekturbüros liefern Pläne mit ausgewerteten Räumen "
        "(Bodenfläche / Raumhöhe als Text im Plan) — und wie viele nicht? "
        "Davon hängt direkt ab, ob das Tool ab Tag 1 nützt oder erst mit "
        "teurer Vision-AI greift.",
        "Wie häufig kommen italienische / französische Anfragen ohne SIA-CRBX "
        "(z. B. aus dem Tessin) — eigener Scope-Strang ja oder nein?",
    ])
    + quoted_p(
        "Statt euch dazu zu interviewen, würden wir das gerne empirisch "
        "messen: ein read-only Scan der letzten ~500 eingegangenen Mails auf "
        "<b><code>offerte@mvm-ag.ch</code></b>, danach 5–10 zufällige Anfragen "
        "pro Top-Büro als Plan-Stichprobe nachladen."
    )

    + quoted_h("Was wir technisch machen würden")
    + quoted_ul([
        "Read-only Zugriff via Microsoft Graph auf "
        "<code>offerte@mvm-ag.ch</code>",
        "Für jede Mail extrahieren: Absender-Domain, Datum, Subject, Anhang-"
        "Liste (Name + Typ + Grösse), Body-Links (WeTransfer / SharePoint), "
        "Sprache (DE / IT / FR per Heuristik)",
        "Aggregat-Report: Top 20 Architekturbüros, CRBX-Quote, "
        "Anhang-vs-Link-Quote, Sprach-Verteilung, Anfragen pro Monat",
        "Für 5–10 Anfragen pro Top-Büro: Anhänge (oder Cloud-Link-Inhalte) "
        "ziehen, ein Plan-PDF mit unserer Pipeline scannen — Quote „Plan-"
        "anfreundlich“ vs. „Plan-feindlich“ pro Büro",
    ])

    + quoted_h("Was wir ausdrücklich NICHT machen")
    + quoted_ul([
        "Keine Mail-Inhalte ins Vault / in Logs schreiben (nur Metadaten + "
        "Anhang-Listen, aggregiert)",
        "Keine Weitergabe von Architekten- / Bauherrn-Identitäten ausserhalb "
        "von uns (Reto, Remo, Giovanni, Raoul) und dem internen Bericht",
        "Kein Schreiben in die Mailbox (kein Senden, kein Verschieben, kein "
        "Antworten, keine Markierungen)",
        "Roh-Scan-Daten (JSON-Lines) liegen lokal verschlüsselt auf meinem "
        "Mac, sind nicht im Git / Cloud-Backup; werden nach Kickoff binnen "
        "7 Tagen automatisch gelöscht",
    ])

    + quoted_h("Was wir konkret von euch brauchen")
    + quoted_p("<b>Reto</b> — Datenschutz-OK:")
    + quoted_ul([
        "Kurzes Einverständnis, dass wir die letzten ~500 Mails der Offert-"
        "Mailbox scannen dürfen (read-only, Aggregat, lokal). Output ist ein "
        "Markdown-Bericht, den wir gemeinsam im Kickoff anschauen.",
    ])
    + quoted_p("<b>Remo</b> — einmalig App-Freigabe im MVM-Tenant:")
    + quoted_ul([
        "<b>Entra ID → Enterprise Applications → Admin Consent</b> für die "
        "bestehende Miraglia-BI-App (Client-ID "
        "<code>0c8e309d-d02e-4244-ae2a-dbb5551cb550</code>) im MVM-Tenant "
        "(<code>3becd9bb-f602-4c6b-8e86-f1e42db365ea</code>) — nur die "
        "delegierte Permission <code>Mail.Read.Shared</code>. Direkter "
        "Consent-Link kann ich liefern sobald du grünes Licht gibst.",
        "Alternative falls einfacher: kurze Teams-Session, wir machen es "
        "gemeinsam in 5 Minuten.",
    ])
    + quoted_p(
        "<b>Auth-Praxis</b> (kein neuer User-Account für Raoul, kein "
        "Exchange-Setup nötig):"
    )
    + quoted_ul([
        "Ein bestehender MVM-User mit Vollzugriff auf "
        "<code>offerte@mvm-ag.ch</code> (z. B. du, Reto) loggt sich einmalig "
        "ca. 30 Sekunden per Device-Code-Flow ein. Mein Skript zeigt eine "
        "URL und einen Code, du öffnest die URL auf deinem PC, gibst den "
        "Code ein, loggst dich normal mit MFA ein.",
        "Danach läuft der Scan bei mir lokal mit deinem Token "
        "(~90 Tage gültig, danach erneuter 30-Sek-Login). Du kannst den "
        "Token jederzeit revoken (Entra → My sign-ins → Sessions revoken).",
    ])
    + quoted_p("<b>Sascha</b> — zur Info:")
    + quoted_ul([
        "Falls du Bedenken hast, gerne kurz melden. Sonst läuft das schlank "
        "zwischen Reto, Remo und uns.",
    ])

    + quoted_h("Zeitfenster")
    + quoted_p(
        "Ideal bis <b>Mittwoch Mittag nächste Woche</b>, damit ich den "
        "Bericht vor dem Kickoff am Donnerstag/Freitag mitbringen kann. "
        "Wenn schneller geht: ich kann den Scan und Bericht in 2–3 Stunden "
        "ab Zugriff liefern."
    )
    + quoted_p(
        "Bei Fragen — Datenschutz-Detail, technische Alternative, Scope-"
        "Frage — kurz Teams-Chat oder Tel "
        "<a href=\"tel:+41766743091\">+41 76 674 30 91</a>."
    )
    + quoted_p("Liebe Grüsse<br>Raoul")
)


# ─── Body der Review-Mail an Giovanni ─────────────────────────────────

BODY = (
    p("Hoi Giovanni")
    + p(
        "Bevor ich die Anfrage an Reto / Remo / Sascha rausschicke, hätte "
        "ich gerne deinen Sanity-Check — du hast den Vorschlag gestern "
        "aufgebracht, also schaust du auch besser auf das fertige Wording."
    )

    + h2("Was sich gegenüber deiner Idee geändert hat")
    + p(
        "Du hast in deinem Feedback geschrieben „App-only "
        "<code>Mail.Read</code> mit Application Access Policy nur auf diese "
        "eine Mailbox — du weisst, was sauberer ist“. Ich habe dazu nochmal "
        "die Praxis durchgespielt:"
    )
    + ul([
        "<b>Auth-Variante umgestellt</b> auf <b>Delegated mit "
        "<code>Mail.Read.Shared</code></b>, weil das Setup bei MVM massiv "
        "einfacher wird (keine App Access Policy via PowerShell-Cmdlet "
        "nötig, keine Client-Secret-Verwaltung, kein Cert-Rotation).",
        "<b>Auth-Identität: bestehender MVM-User mit Vollzugriff</b> (z. B. "
        "Reto selber) statt mein User. Spart Exchange-Vollzugriff-Setup + "
        "Guest-Account für mich. Der MVM-User loggt sich einmalig "
        "30 Sekunden per Device-Code-Flow ein, danach läuft alles bei mir "
        "lokal.",
        "<b>Audit-Spur bleibt sauber</b>: der echte Inhaber der Berechtigung "
        "autorisiert den Token, ich bin nur Konsument. Token revokebar "
        "jederzeit aus dem User-Self-Service.",
    ])
    + p(
        "Damit reduziert sich Remos Arbeit auf <b>einen</b> Schritt "
        "(Enterprise-App-Consent), statt drei (Guest-User + Exchange-"
        "Vollzugriff + App-Consent)."
    )

    + h2("Vorab-Klärungs-Punkte, bevor ich an MVM schicke")
    + p("Konkret bitte ich dich um Sicht auf:")
    + ul([
        "<b>Tonfall</b> — ist die Mail für GL-Ebene (Sascha) angemessen "
        "knapp? Oder zu lang? Oder zu technisch?",
        "<b>Datenschutz-Wording</b> — reicht das, was unter „NICHT machen“ "
        "steht? Wir hatten gestern explizit „kurz mit Reto die Datenschutz-"
        "Seite klären“ als deinen Punkt — bin ich da deutlich genug?",
        "<b>Auth-User-Empfehlung</b> — soll ich Reto explizit als "
        "Vorschlags-User für die Auth nennen, oder offen lassen und Remo "
        "den geeignetsten User wählen lassen?",
        "<b>Zeitfenster</b> — „Mittwoch Mittag“ realistisch? Oder eher "
        "puffern auf Donnerstag früh?",
        "<b>Sascha-Rolle</b> — ist „zur Info, bei Bedenken melden“ "
        "ausreichend? Oder soll Sascha aktiv freigeben?",
    ])

    + h2("Hier der Entwurf, den ich an MVM senden würde")
    + quote_block(MVM_MAIL_DRAFT)

    + h2("Wenn alles passt")
    + p(
        "Gib mir kurz „passt“ oder konkrete Änderungswünsche zurück — ich "
        "passe an, idempotenter Skript-Lauf ersetzt den Draft, und ich "
        "schicke die Mail dann an MVM raus."
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


def delete_obsolete_drafts(token: str, subjects: list[str]) -> int:
    """Löscht auch Drafts mit ALTEN Subject-Versionen (Aufräumen nach Iteration)."""
    total = 0
    for s in subjects:
        total += delete_existing_drafts_with_subject(token, s)
    return total


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


# Auch alte Subject-Varianten der vorherigen Iterationen abräumen
OBSOLETE_SUBJECTS = [
    "KI-Ausmass MVM — vor dem Kickoff: read-only Sample-Auswertung "
    "offerte@mvm-ag.ch?",
]


def main() -> None:
    print("=" * 70)
    print("📧 KI-Ausmass MVM — Konzept-Check-Mail an Giovanni erstellen")
    print("=" * 70)
    print(f"   To:  Giovanni Miraglia <giovanni@miraglia-bi.com>")
    print(f"   Cc:  (keine)")
    print(f"   Subj: {SUBJECT}")
    print()

    token = _ac_get_token(SCOPES)

    # Idempotenz: alter Draft mit gleichem Subject + obsolete Subjects löschen
    n_current = delete_existing_drafts_with_subject(token, SUBJECT)
    n_obsolete = delete_obsolete_drafts(token, OBSOLETE_SUBJECTS)
    if n_current + n_obsolete > 0:
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
