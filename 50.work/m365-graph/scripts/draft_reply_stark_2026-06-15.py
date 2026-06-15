#!/usr/bin/env python3
"""
draft_reply_stark_2026-06-15.py
--------------------------------
Antwort-Entwurf an Stephanie Stark (Sharkgroup AG / enia vertriebs gmbh,
ID-Leitung@sharkgroup.swiss) auf ihre Mail vom 2026-06-11 — Anfrage zu einem
ungefähren Kostenvorschlag für die Automatisierung der Bestellverarbeitung mit
PROFFIX-Integration.

Tenor der Antwort:
- KEINE formelle Aufwandschätzung / Offerte
- Stattdessen: 1 Tag vor Ort, im besten Fall durch, sonst seriöse Restschätzung
- Hinweis auf Prozess-Knowledge-Erfahrung aus früheren Projekten → ggf.
  selbständige Weiterentwicklung durch die Innendienst-Seite möglich
- PROFFIX-Schnittstelle: nur Hinweis, dass Abstimmung mit Alessandro Castelli läuft
- Terminvorschlag + Frage nach Standort (Uster oder Oberhasli — NICHT Pratteln!)

Verwendet die bewährten Helpers aus draft_reply_vloriana_ss.py.
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
    "Freundliche Grüsse<br>Raoul Miraglia</p>"
)


REPLY = {
    "search_subject": "evg_Anfrage zu einem ungefähren Kostenvorschlag - Umsetzung Automatisierung Bestellverarbeitung inkl. Proffix-Integration",
    "from": "ID-Leitung@sharkgroup.swiss",
    "after": "2026-06-10T00:00:00Z",
    "body": (
        p("Guten Tag Frau Stark")
        + p(
            "Besten Dank für Ihre Anfrage und die beiden Musterbestellungen."
        )
        + p(
            "Die beschriebene Umsetzung — PDF-Bestellungen via AI-Prompt auslesen, "
            "externe Lieferanten-Artikelnummern (Hoegner, bodecor, Werkhaus) gegen "
            "Ihre interne <code>ArtikelNrLAG</code> mappen, Musterbestellungen mit "
            "„M&#8220;-Präfix kennzeichnen und über die PROFFIX-REST-API als Auftrag "
            "anlegen — passt sehr gut in unser Standard-Repertoire. Ein vergleichbares "
            "Szenario betreiben wir bereits produktiv (anderes ERP, gleiche Logik: "
            "Extraktion &#8594; Mapping &#8594; automatisierte Auftragserfassung), "
            "sodass wir auf einem bewährten Pattern aufsetzen können."
        )
        + p(
            "Statt vorab eine Aufwandschätzung „ins Blaue&#8220; zu liefern, schlage "
            "ich Ihnen folgendes Vorgehen vor, das uns beiden mehr Klarheit bringt:"
        )
        + p(
            "<b>Ich komme einen Tag zu Ihnen vor Ort</b> und setze die Lösung "
            "direkt mit Ihnen auf — Prompt-Logik, Mapping gegen <code>LAG_Artikel</code>, "
            "erster End-to-End-Durchgang mit Ihren echten Bestellungen. Im "
            "<b>besten Fall sind wir an diesem Tag durch</b> und die Automatisierung "
            "läuft produktiv. Im anspruchsvolleren Fall können wir nach diesem Tag "
            "den Restaufwand seriös beziffern, weil wir dann konkret wissen, wo es klemmt."
        )
        + p(
            "Aus vergleichbaren Kundenaufträgen habe ich die Erfahrung gemacht, dass "
            "es bei dieser Art von Automatisierung viel enges Prozess-Wissen aus Ihrem "
            "Innendienst braucht — die Spezialfälle, die Ausnahmen pro Lieferant, das "
            "stille Wissen rund um die Artikelnummern. Wenn wir einen Tag gemeinsam "
            "daran arbeiten, sehe ich gute Chancen, dass Sie die Lösung danach in "
            "vielen Punkten selbständig weiterentwickeln und feinjustieren können — "
            "ohne dass jede kleine Anpassung wieder bei mir landen muss."
        )
        + p(
            "Bezüglich der PROFFIX-Schnittstelle stimme ich mich vorab mit "
            "Alessandro Castelli ab — er hat in dem Bereich bereits Arbeiten gemacht, "
            "auf denen wir aufsetzen können."
        )
        + p(
            "Können Sie mir bitte zwei, drei mögliche Termine in den nächsten zwei "
            "bis drei Wochen vorschlagen, und mir kurz mitteilen, an welchem Standort "
            "(Uster oder Oberhasli) der Termin stattfindet?"
        )
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
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    token = get_token()

    print("Lösche evtl. bestehende Drafts …")
    delete_existing_drafts(token, REPLY["search_subject"])

    print(f"\n→ Suche: „{REPLY['search_subject'][:60]}…\" (von {REPLY['from']})")
    msg = find_msg(token, REPLY["search_subject"], REPLY["from"], REPLY["after"])
    if not msg:
        sys.exit("✗ Original-Mail nicht gefunden.")
    print(f"  ✓ Original: {msg['receivedDateTime'][:19]}")

    draft_id, subj = create_reply_draft(token, msg["id"], REPLY["body"])
    if not draft_id:
        sys.exit("✗ Draft-Erstellung fehlgeschlagen.")
    print(f"  ✓ Draft: „{subj[:80]}…\"")

    if attach_inline_logo(token, draft_id, logo_bytes):
        print("  ✓ Inline-Logo angehängt")

    print("\nFertig. Draft liegt im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
