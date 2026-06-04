#!/usr/bin/env python3
"""
draft_replies_mvm.py
--------------------
Erstellt drei Antwort-Entwürfe (createReply) im Outlook-Postfach
für die letzten MVM-AG-Mails (Remo Pfister, 02.–03.06.2026).

Signatur: nachgebaut nach Giovannis Outlook-Signatur (Logo + grüne Trennlinie),
Logo als Inline-Attachment (contentId 'miragliabi-logo').

Voraussetzung:
- Scope Mail.ReadWrite konsent (zusätzlich zu Mail.Read).
- miraglia_logo.png im Script-Verzeichnis (via extract_logo.py einmalig erzeugt).

Verhalten:
- Sucht in den letzten 300 Mails die Original-Mails (Absender + exaktes Subject)
- Löscht ggfs. bestehende Drafts mit identischem Reply-Subject (Idempotenz)
- Erstellt frische createReply-Drafts
- Patcht Body (Antworttext + Signatur + zitiertes Original)
- Hängt Logo als Inline-Attachment an

Aufruf:
  python3 draft_replies_mvm.py
"""
import base64
import os
import sys
from pathlib import Path
from urllib.parse import quote

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


# Signatur nachgebaut nach Giovannis Outlook-Signatur:
# - 2-spaltige Tabelle (Logo | grüner Vertikal-Strich + Text)
# - Aptos/Calibri 11pt
# - Logo via cid: aus Inline-Attachment
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
    "Mit freundlichen Grüssen<br>Raoul</p>"
)


def p(text: str) -> str:
    """Absatz in Giovannis Stil (Aptos/Calibri 11pt)."""
    return (
        "<p style=\"font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt; "
        f"color:rgb(34,34,34); line-height:1.5; margin:4px 0px\">{text}</p>"
    )


DRAFTS = [
    {
        "search_subject": "Neue Regie-Rapport App - Nr. 26-1039",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-02T00:00:00Z",
        "body": (
            p("Hoi Remo")
            + p(
                "Der Fall mit Christoph Räbers Rapport 26-1039 ist mittlerweile geklärt: "
                "Es lag an einer fehlenden Berechtigung. Er hatte zum Zeitpunkt der "
                "Erfassung noch keinen Zugriff auf den SharePoint-Speicherort, an dem "
                "der Flow das fertige PDF ablegt. Der Flow selbst hatte alles korrekt "
                "durchgerechnet und das PDF auch generiert — einzig das Speichern "
                "(und damit der nachgelagerte Mail-Versand) ist deshalb fehlgeschlagen. "
                "Daraus ist auch die irreführende Bestätigung „an ihn selbst gesendet&#8220; entstanden."
            )
            + p("Die Berechtigung ist nachgetragen, der Rapport ist sauber durchgelaufen.")
            + GRUSS
            + SIGNATURE_HTML
        ),
    },
    {
        "search_subject": "Mahnprozess - Christoph Räber",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-02T00:00:00Z",
        "body": (
            p("Hoi Remo")
            + p(
                "Christoph Räber sowie Richy Schön und Jan Schwitter sind nun im "
                "Mahnprozess hinterlegt."
            )
            + p(
                "Sobald aus dem BRZ über ihre Mailadresse eine Mahnungs-Entscheidung "
                "anliegt, werden sie per Mail benachrichtigt und sind für die "
                "entsprechende Registerkarte in Teams berechtigt."
            )
            + p(
                "Für zukünftige Anpassungen kannst du den Prozess selbständig handhaben: "
                "Es genügt, die gewünschten Personen zu dieser Teams-Registerkarte "
                "hinzuzufügen — mehr braucht es meines Wissens nicht."
            )
            + p("Bei Fragen oder falls noch etwas nicht greift, melde dich gerne.")
            + GRUSS
            + SIGNATURE_HTML
        ),
    },
    {
        "search_subject": "Rechnung aus Magazin-App",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-01T00:00:00Z",
        "body": (
            p("Hoi Remo")
            + p("Genau, aktuell beziehe ich mich für die Rechnung auf den Einstandspreis (EP).")
            + p(
                "Wenn du in der KANBAN-Liste die Spalte mit den internen Verkaufspreisen "
                "ergänzt, baue ich die Rechnungslogik gerne so um, dass sie sich auf "
                "diese neue Spalte stützt. Sag mir einfach Bescheid, sobald die Spalte "
                "verfügbar ist, dann mache ich die Anpassung."
            )
            + GRUSS
            + SIGNATURE_HTML
        ),
    },
]


# ─── Auth ─────────────────────────────────────────────────────────────


def get_token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        token_cache=cache,
    )
    result = None
    for acc in app.get_accounts():
        result = app.acquire_token_silent(SCOPES, account=acc)
        if result:
            break
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60)
        print(flow["message"])
        print("=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE_FILE.write_text(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"Login fehlgeschlagen: {result.get('error_description')}")
    return result["access_token"]


# ─── Graph-Helpers ─────────────────────────────────────────────────────


def odata_escape(s: str) -> str:
    return s.replace("'", "''")


def find_msg(token: str, subject: str, from_addr: str, after: str):
    """Letzte 300 Inbox-Mails durchgehen, Match auf Absender + Subject + Datum."""
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


def delete_existing_drafts(token: str, reply_subject_prefixes: list[str]):
    """Löscht Drafts mit Subject 'RE: <original>' oder 'AW: <original>' im Drafts-Ordner."""
    headers = {"Authorization": f"Bearer {token}"}
    # Drafts-Folder ID holen
    r = requests.get(
        f"{GRAPH}/me/mailFolders/drafts?$select=id",
        headers=headers, timeout=30,
    )
    if not r.ok:
        print(f"  ⚠ Drafts-Folder-Lookup HTTP {r.status_code}")
        return 0
    drafts_id = r.json().get("id")
    if not drafts_id:
        return 0
    # Letzte 50 Drafts holen
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
        for prefix_original in reply_subject_prefixes:
            # Outlook liefert RE: oder AW:
            if subj in (f"RE: {prefix_original}", f"AW: {prefix_original}"):
                dr = requests.delete(
                    f"{GRAPH}/me/messages/{m['id']}",
                    headers=headers, timeout=30,
                )
                if dr.ok:
                    print(f"  🗑  Alten Draft gelöscht: „{subj}\"")
                    deleted += 1
                break
    return deleted


def create_reply_draft(token: str, msg_id: str, html_body: str):
    """Reply-Draft anlegen + Body patchen."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    r = requests.post(
        f"{GRAPH}/me/messages/{msg_id}/createReply",
        headers=headers, timeout=30,
    )
    if not r.ok:
        print(f"  ⚠ createReply HTTP {r.status_code}: {r.text[:400]}")
        return None, None
    draft = r.json()
    draft_id = draft["id"]
    existing_body = draft.get("body", {}).get("content", "") or ""
    new_html = html_body + existing_body
    patch = {"body": {"contentType": "HTML", "content": new_html}}
    r2 = requests.patch(
        f"{GRAPH}/me/messages/{draft_id}",
        headers=headers, json=patch, timeout=30,
    )
    if not r2.ok:
        print(f"  ⚠ patch HTTP {r2.status_code}: {r2.text[:400]}")
    return draft_id, draft.get("subject", "")


def attach_inline_logo(token: str, draft_id: str, logo_bytes: bytes):
    """Inline-Attachment Logo (contentId=miragliabi-logo) zum Draft hinzufügen."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
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


# ─── Main ──────────────────────────────────────────────────────────────


def main():
    if not CLIENT_ID or not TENANT_ID:
        sys.exit("M365_CLIENT_ID / M365_TENANT_ID nicht gesetzt.")
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}. Vorher extract_logo.py laufen lassen.")
    logo_bytes = LOGO_FILE.read_bytes()
    print(f"Logo geladen: {LOGO_FILE.name} ({len(logo_bytes)} bytes)")

    token = get_token()

    # 1. Alte Drafts mit gleichen Subjects aufräumen
    print("\nLösche evtl. bestehende Drafts mit gleichem Subject …")
    deleted = delete_existing_drafts(
        token, [d["search_subject"] for d in DRAFTS]
    )
    print(f"  → {deleted} alte Drafts gelöscht\n")

    # 2. Drafts neu erstellen
    print(f"Erstelle {len(DRAFTS)} Antwort-Entwürfe (mit Signatur + Inline-Logo) …\n")
    ok = 0
    for d in DRAFTS:
        print(f"→ Suche: „{d['search_subject']}\" (von {d['from']})")
        msg = find_msg(token, d["search_subject"], d["from"], d["after"])
        if not msg:
            print("  ✗ Original-Mail nicht gefunden — übersprungen\n")
            continue
        print(f"  ✓ Original: {msg['receivedDateTime'][:19]}")
        draft_id, subj = create_reply_draft(token, msg["id"], d["body"])
        if not draft_id:
            print("  ✗ Draft-Erstellung fehlgeschlagen\n")
            continue
        print(f"  ✓ Draft: „{subj}\"")
        if attach_inline_logo(token, draft_id, logo_bytes):
            print("  ✓ Inline-Logo angehängt")
            ok += 1
        else:
            print("  ⚠ Inline-Logo NICHT angehängt — Signatur ohne Logo dargestellt")
        print()

    print(f"Fertig: {ok}/{len(DRAFTS)} Entwürfe im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
