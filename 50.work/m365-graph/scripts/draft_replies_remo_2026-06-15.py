#!/usr/bin/env python3
"""
draft_replies_remo_2026-06-15.py
--------------------------------
Erstellt 5 Antwort-Entwürfe (createReply) im Outlook-Postfach
für die offenen Themen mit Remo Pfister vom 10.–12.06.2026
(Regie-App und Magazin-App), Stand 15.06.2026.

Mail-Mapping (5 Replies für ToDos 1–6 aus 60.daily/2026-06-15.md):
1+2. KSTS 505 Meggen + Komma-Bug   → Reply auf „AW: Magazin-App --> KSTS 505 Meggen" (Remo, 12.06. 07:18)
3.   Pflichtfeld rotes Feld        → Reply auf „Neuer Regie-Rapport: Pflichtfeld machen" (Remo, 12.06. 14:07)
4.   VP-Kalkulation Label          → Reply auf „AW: Rechnung aus Magazin-App" (Remo, 11.06. 14:15)
5.   Kopierfunktion (nur Kopf)     → Reply auf „AW: NEUE Regie App" (Remo, 11.06. 11:10)
6.   Desktop-Ansicht leere Rapp.   → Reply auf „Neue Regie-App - Desktop-Ansicht" (Remo, 12.06. 14:52)

ToDo 7 (Aestico/Domus) ist noch offen — KEINE Antwort dazu in diesem Lauf.

Pattern: 1:1 nach draft_replies_mvm.py (Keychain-Auth, Inline-Logo,
Aptos/Calibri-Signatur, Idempotenz via Draft-Löschung bei gleichem Subject).
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


# ─── Inhalte der 5 Antworten ───────────────────────────────────────────

# 1+2. KSTS 505 Meggen + Komma-Bug (kombiniert in einem Reply)
BODY_1_2 = (
    p("Hoi Remo")
    + p("Zwei Punkte aus unserem Magazin-App-Strang sind erledigt:")
    + p(
        "<b>1. KSTS 505 Meggen</b> — die Auswahl ist jetzt analog zu KSTS 500 "
        "(Magazin / Baustelle Meggen). Antonio De Finis und Stefanie Furrer "
        "können das so nutzen."
    )
    + p(
        "<b>2. Der Komma-Bug bei den neuen Preisspalten</b> (3.01 wurde als "
        "301.00 angezeigt) ist behoben. Ursache war ein Typ-Konflikt: meine "
        "neuen Preisspalten waren als Float angelegt, der EP hingegen als "
        "Dezimal — die beiden vertragen sich beim Datenfluss nicht. Ich habe "
        "die Spalten frisch als Dezimal neu erstellt, jetzt sind die Preise "
        "korrekt."
    )
    + p("Gib mir Bescheid, falls etwas trotzdem noch schräg läuft.")
    + GRUSS
    + SIGNATURE_HTML
)

# 3. Pflichtfeld rotes Feld
BODY_3 = (
    p("Hoi Remo")
    + p(
        "Das rote Feld ist jetzt Pflichtfeld — wenn nichts ausgefüllt ist, "
        "kommt der User nicht weiter."
    )
    + p(
        "Bei der Gelegenheit habe ich gleich noch ein paar zusätzliche "
        "Pflichtfeld-Sperren eingebaut (Baustelle, Kalenderwoche, "
        "Empfänger-Typ). Das hängt mit deiner separaten Frage zu den blau/weiss "
        "leeren Rapporten in der Desktop-Ansicht zusammen — dazu antworte ich "
        "dir in jenem Mail-Strang."
    )
    + GRUSS
    + SIGNATURE_HTML
)

# 4. VP-Kalkulation Label
BODY_4 = (
    p("Hoi Remo")
    + p("Das Feld ist umbeschriftet auf «VP-Kalkulation».")
    + GRUSS
    + SIGNATURE_HTML
)

# 5. Kopierfunktion (nur Kopf)
BODY_5 = (
    p("Hoi Remo")
    + p(
        "Die Kopierfunktion ist eingebaut: beim Kopieren werden nur die "
        "Kopfdaten (Baustelle, Empfänger, Kalenderwoche, zuständiger PL) "
        "übernommen — Positionen und Stunden müssen neu erfasst werden, "
        "so wie du es haben wolltest."
    )
    + p(
        "Eine deiner Fragen aus dem ursprünglichen Mail ist bei mir noch "
        "offen: ob Rapporte aus der alten App in der neuen mit angezeigt "
        "werden sollen. Aktuell laufen die zwei Listen getrennt. Sag mir "
        "kurz, ob wir das so belassen oder ob du möchtest, dass ich die "
        "alten Rapporte in der neuen Übersicht mitanzeige."
    )
    + GRUSS
    + SIGNATURE_HTML
)

# 6. Desktop-Ansicht — leere Rapporte
BODY_6 = (
    p("Hoi Remo")
    + p(
        "Gute Beobachtung — das war kein Anzeige-Problem, sondern wirklich "
        "ein Bug in der Datenerfassung. Die Rapporte waren in der Tabelle "
        "tatsächlich ohne Baustelle abgelegt."
    )
    + p(
        "Ursache: an drei Stellen in der App liess sich ein Rapport "
        "speichern, ohne dass Baustelle / Kalenderwoche / Empfänger gefüllt "
        "waren (beim Anlegen eines neuen Rapports, beim Inline-Edit der "
        "Bezeichnung und beim „Rapport Kopf Edit&#8220; auf der PDF-Seite). "
        "Wer zu schnell durchklickte oder die Auswahl versehentlich löschte, "
        "produzierte einen leeren Datensatz."
    )
    + p(
        "Fix: an allen drei Stellen sind jetzt Pflichtfeld-Sperren aktiv — "
        "der Speichern-Button bleibt grau, bis die nötigen Felder gefüllt "
        "sind. Damit kann das nicht mehr passieren."
    )
    + p(
        "Den bestehenden Bestand an leeren Rapporten räume ich diese Woche "
        "noch auf. Ich gehe davon aus, dass die getrost gelöscht werden "
        "können — gib mir kurz dein OK, dann mache ich das."
    )
    + GRUSS
    + SIGNATURE_HTML
)


DRAFTS = [
    {
        "search_subject": "AW: Magazin-App --> KSTS 505 Meggen",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-12T00:00:00Z",
        "body": BODY_1_2,
        "label": "1+2 Meggen + Komma-Bug",
    },
    {
        "search_subject": "Neuer Regie-Rapport: Pflichtfeld machen",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-12T00:00:00Z",
        "body": BODY_3,
        "label": "3 Pflichtfeld",
    },
    {
        "search_subject": "AW: Rechnung aus Magazin-App",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-11T00:00:00Z",
        "body": BODY_4,
        "label": "4 VP-Kalkulation Label",
    },
    {
        "search_subject": "AW: NEUE Regie App",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-11T00:00:00Z",
        "body": BODY_5,
        "label": "5 Kopierfunktion",
    },
    {
        "search_subject": "Neue Regie-App - Desktop-Ansicht",
        "from": "r.pfister@mvm-ag.ch",
        "after": "2026-06-12T00:00:00Z",
        "body": BODY_6,
        "label": "6 Desktop-Ansicht leere Rapporte",
    },
]


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


def delete_existing_drafts(token: str, reply_subject_prefixes: list[str]):
    headers = {"Authorization": f"Bearer {token}"}
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
            if subj in (
                f"RE: {prefix_original}",
                f"AW: {prefix_original}",
                # falls original schon mit „AW: " beginnt: doppeltes Präfix vermeiden
                prefix_original,
            ):
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


def main():
    if not LOGO_FILE.exists():
        sys.exit(f"Logo fehlt: {LOGO_FILE}.")
    logo_bytes = LOGO_FILE.read_bytes()
    print(f"Logo geladen: {LOGO_FILE.name} ({len(logo_bytes)} bytes)")

    token = get_token()

    print("\nLösche evtl. bestehende Drafts mit gleichem Subject …")
    deleted = delete_existing_drafts(
        token, [d["search_subject"] for d in DRAFTS]
    )
    print(f"  → {deleted} alte Drafts gelöscht\n")

    print(f"Erstelle {len(DRAFTS)} Antwort-Entwürfe …\n")
    ok = 0
    for d in DRAFTS:
        print(f"→ [{d['label']}] Suche: „{d['search_subject']}\"")
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
            print("  ⚠ Inline-Logo NICHT angehängt")
        print()

    print(f"Fertig: {ok}/{len(DRAFTS)} Entwürfe im Outlook-Ordner „Entwürfe\".")


if __name__ == "__main__":
    main()
