#!/usr/bin/env python3
"""
draft_mail_ki_ausmass_summary.py
---------------------------------
Erstellt einen NEUEN Mail-Entwurf (kein Reply) im Outlook-Drafts-Ordner
mit der Zusammenfassung des KI-Ausmass-Tages 2026-06-04 vor dem Kickoff mit Reto.

To:  Giovanni Miraglia <giovanni@miraglia-bi.com>
Cc:  Michael Kipfer  <michael@kipfer-dp.com>

Signatur + Logo wie in draft_replies_mvm.py (Inline-CID).

Idempotenz: alter Draft mit identischem Subject wird vor Neuanlage gelöscht.

Aufruf:
  python3 draft_mail_ki_ausmass_summary.py
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

SUBJECT = "KI-Ausmass MVM — Stand 04.06.2026 / Vorbereitung Kickoff mit Reto"

TO_RECIPIENTS = [
    {"emailAddress": {"address": "giovanni@miraglia-bi.com", "name": "Giovanni Miraglia"}},
]
CC_RECIPIENTS = [
    {"emailAddress": {"address": "michael@kipfer-dp.com", "name": "Michael Kipfer"}},
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
    p("Hallo Giovanni, hallo Mike")
    + p(
        "Kurzes Update zum heutigen Stand am KI-Ausmass-Projekt für MVM. "
        "Ich möchte euch vor dem Kickoff mit Reto Limacher (Donnerstag/Freitag) "
        "auf gleichen Stand bringen und ein paar Fragen ablegen, die zwischen uns drei "
        "vorab geklärt werden sollten."
    )

    + h2("Was heute erreicht wurde")
    + p("<b>Toolchain-Grundgerüst</b> (Tagsüber, ca. 5 h fokussiert):")
    + ul([
        "SIA-451-Parser läuft sauber auf allen 9 CRBX-Anfragen aus Retos Trainingsdaten "
        "(Cerutti, Eberli, blu architekten)",
        "Plan-Text-Extraktor (PyMuPDF + Cluster-Box) findet ~30 Räume pro Cerutti-Geschoss "
        "inkl. BF/RH-Tags",
        "Excel-Generator im Mike-Kipfer-Goldstandard 1:1 (14 Spalten, Annahmen, Formeln, "
        "Konfidenz, Korrektur-Log)",
        "CRBX-Round-Trip-Writer (Mengen-Injection in SIA-Fixed-Width; reverse-engineered)",
        "End-to-End-Demo: 2100 Bleicherstrasse → 200 Räume / 3'017 m² Bodenfläche / "
        "5'732 m² Wand brutto",
    ])
    + p("<b>Robuster Generic-Runner</b> (Abend) — das war heute der eigentliche Sprung:")
    + ul([
        "Aus dem hardgecodeten Demo ist ein generischer Pipeline-Runner geworden: "
        "Konvention „alles im selben Ordner&#8220; (CRBX + Pläne/) — man wirft einen beliebigen "
        "Projekt-Ordner rein, der Runner findet sich zurecht",
        "File-Discovery rekursiv bis 3 Ebenen tief; PDF-Klassifikation (Plan vs. "
        "Anleitung/Konzept/Datenblatt) mit mehrsprachigen Keywords <b>DE/IT/FR</b> "
        "(für Tessin und Romandie)",
        "Plan-Only-Modus für Tessin-Anfragen (kein CRBX, nur PDFs/Excel)",
        "Self-Diagnose: pro Lauf ein <code>_diagnose.md</code> mit Status-Bewertung "
        "(🟢 GRÜN / 🟡 GELB / 🔴 ROT) und konkreten Empfehlungen für die nächste Iteration",
        "<b>Vision-AI-Fallback</b> mit Claude Opus 4.7 (für Pläne ohne BF/RH-Tags — also "
        "alles ausser Cerutti-Stil)",
    ])

    + h2("Drei reale Tests = drei lehrreiche Erkenntnisse")
    + p("Live durchgespielt an drei echten Projekten aus dem Trainingsset bzw. aus dem "
        "Downloads-Ordner — jedes hat eine eigene Lehre geliefert:")
    + ul([
        "<b>Bleicherstrasse-Gipser (Cerutti)</b> → 🟡 GELB: Text-Extraktion klappt sauber "
        "(200 Räume). Einzige Restschuld: Pseudo-Geschoss-Werte aus Schnitt-Plänen.",
        "<b>Submissionsversand Baila (DE, Kompetenzzentrum G'ART)</b> → 🟡 GELB: "
        "Anfrage automatisch gefunden in <code>01 LV/</code>, Pläne in <code>02 Pläne/</code>. "
        "2 PDFs als Nicht-Plan aussortiert (Lackierungsanleitung, Konzept Materialisierung). "
        "Aber: <b>0 echte Räume</b> aus Text-Extraktion — Baila nutzt keine BF/RH-Annotations. "
        "→ <b>Vision-AI nötig</b>.",
        "<b>La Mobiliare, Bellinzona (IT)</b> → 🔴 ROT: Tessin-Anfrage ganz ohne SIA-CRBX, "
        "nur 4 italienische PDFs (Piano Arredo, Piani esecutivi, Piano luci, Appalto gessatore) "
        "+ 2 Excel-Dateien (BASWA-Schalldämmung). IT-Keyword-Filter hat sauber funktioniert. "
        "Aber wieder: <b>0 Räume</b> — Vision-AI nötig.",
    ])
    + p(
        "<b>Wichtige Schlussfolgerung:</b> Das Bottleneck ist NICHT der Workflow oder das "
        "Drumherum — File-Discovery, PDF-Klassifikation, Anfrage-Parsing funktionieren "
        "alle robust. Das Bottleneck ist der <b>Plan-Extraktor</b>, der nur bei Cerutti-Stil "
        "echte Räume liefert. Vision-AI wird damit nicht ein „nice-to-have&#8220; sondern "
        "Pflicht für die meisten echten Anfragen."
    )

    + h2("Architektur-Idee für die Trigger-Mechanik")
    + p(
        "Wie ich mir die Test-/Pilot-Phase vorstelle (offen für Korrekturen):"
    )
    + p("<b>Phase 1 — Test (ab nächste Woche)</b>: Watch-Folder als Trigger")
    + ul([
        "Reto/Sekretariat legt einen Projekt-Ordner per Drag-and-Drop in einen dedizierten "
        "SharePoint-Folder (z.B. <code>Offertwesen/KI-Test/01_Eingang/</code>)",
        "Ein lokaler Python-Watcher (initial bei mir auf dem Mac, später auf einem "
        "dedizierten NUC bei MVM oder im Azure-Container) merkt den neuen Drop, "
        "ruft die Pipeline auf",
        "Output landet in <code>02_Ergebnis/&lt;projektname&gt;/</code>: Excel im Mike-Goldstandard "
        "+ ggf. mutiertes CRBX + <code>_diagnose.md</code>",
        "Mail-Notification an Reto „Anfrage X ausgewertet, hier ist der Link&#8220;",
    ])
    + p("<b>Phase 2 — Produktiv (Q4 2026)</b>: Postfach-Überwachung")
    + ul([
        "Power Automate Cloud Flow triggert auf neuen Mails in einem dedizierten "
        "<code>offerte@mvm-ag.ch</code>-Subfolder „KI&#8220;",
        "Anhänge entpacken, SharePoint-Projektordner anlegen (Mike's Konzept), Plan-Links "
        "verfolgen (SharePoint/WeTransfer)",
        "Pipeline aufrufen über Custom Connector / Azure Function",
        "Output landet in der Power-App Reviewer (siehe Output-Format-Frage unten)",
    ])

    + h2("Offene Fragen für den Reto-Kickoff")
    + p("<b>1. Output-Format</b> — was bringt Reto am meisten?")
    + ul([
        "<b>(a) Excel-Vergleich</b> zum manuellen Mengenübertrag ins BAUAD (Mike's Pattern)",
        "<b>(b) Vorausgefülltes CRBX</b> zum direkten Import in Messerli (was wir gebaut haben)",
        "<b>(c) Power-App Review-UI</b> mit Akzeptieren/Korrigieren pro Position (Phase 3)",
    ])
    + p(
        "Meine Wette: er sagt zuerst (a) zum Vergleichen, nach 2-3 Iterationen erkennt er "
        "(b) als zeitsparender. Wir bringen beide Artefakte zur Demo."
    )
    + p("<b>2. Architekten-Landschaft</b>: welche Büros zeichnen wie Cerutti (mit BF/RH als Text "
        "im Plan)? Wenn 80 % → Tool ab Tag 1 nützlich. Wenn nur 20 % → Vision-AI sofort priorisieren.")
    + p("<b>3. Tessin-Anfragen</b>: wie häufig sind italienische Anfragen ohne SIA-CRBX? "
        "Wenn regelmäßig → eigener Scope-Strang.")
    + p("<b>4. NPK-Mapping-Regeln</b>: Reto soll die Regel-Tabelle für BKP 285.1 (innere "
        "Malerarbeiten) mitbringen — welche NPK-Position = welche Mengen-Formel. Das ist "
        "Phase-2-Voraussetzung.")
    + p("<b>5. Messerli BAUAD</b>: Demo-Lizenz für mich oder Screenshare-Termin in Retos BAUAD "
        "für den CRBX-Round-Trip-Test?")

    + h2("Was ich euch beide gerne fragen würde")
    + p("<b>Mike:</b>")
    + ul([
        "Erfahrungen mit deinen 9 Excel-Vorlagen — was hat wirklich funktioniert, was war frustig?",
        "Welche Architekten kennst du als „Plan-anfreundlich&#8220; (BF/RH-Tags vorhanden) vs. "
        "„Plan-feindlich&#8220; (nur Vektorgrafik)?",
        "Türen-Erkennung mit Dimensionsmustern (Breite cm / Höhe m) — können wir deinen "
        "Algorithmus übernehmen statt Vision-AI neu zu bauen?",
        "Hast du 30 Min nächste Woche für einen Sync vor dem Reto-Termin?",
    ])
    + p("<b>Giovanni:</b>")
    + ul([
        "BRZ/DOMUS-Anbindung für Preisvorschläge (Phase 4) — kannst du mir die SQL-Datenstruktur "
        "schon mal teilen?",
        "Hitrate-App-Code als Vorlage für die Mengen-Review-Power-App (Phase 3) — nutzbar?",
        "Strategisch: ist MVM bereit für eine Anthropic API-Subscription? Vision-AI kostet "
        "~$0.10 pro Plan, ~16 Pläne pro Anfrage = $1.60 pro Anfrage auf Opus 4.7. "
        "Alternative: Sonnet 4.6 (~10× billiger) oder Azure AI Foundry mit Bedrock.",
    ])

    + h2("Nächste Schritte morgen")
    + ul([
        "Vision-AI-Test mit echtem API-Key auf Baila + Mobiliare Bellinzona (Beweis: "
        "Räume werden korrekt erkannt → beide Projekte gehen auf 🟢/🟡)",
        "Mail an Reto mit Excel-Vorabschau Bleicherstrasse-Gipser vor dem Kickoff",
        "Kickoff-Agenda finalisieren (Entwurf liegt in "
        "<code>50.work/projekte/MVM-AG/KI-Ausmass MVM/docs/kickoff-agenda-reto.md</code>)",
    ])
    + p(
        "Code-Stand liegt zentral im Obsidian-Vault unter "
        "<code>50.work/projekte/MVM-AG/KI-Ausmass MVM/</code> — Repo, Docs, Demo-Output, "
        "Diagnose-Markdowns, alles dort. Bei Interesse kann ich euch beiden Zugriff geben "
        "oder die Files direkt teilen."
    )
    + GRUSS
    + SIGNATURE_HTML
)


# ─── Auth (Pattern aus draft_replies_mvm.py) ─────────────────────────────


def get_token():
    cache = msal.SerializableTokenCache()
    if CACHE_FILE.exists():
        cache.deserialize(CACHE_FILE.read_text())
    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}",
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
    if not CLIENT_ID or not TENANT_ID:
        sys.exit(
            "M365_CLIENT_ID und M365_TENANT_ID müssen in der Umgebung gesetzt sein.\n"
            "Werte in 50.work/m365-graph/02-zugangsdaten-secrets.md"
        )

    print("=" * 70)
    print("📧 KI-Ausmass MVM — Mail-Entwurf erstellen")
    print("=" * 70)
    print(f"   To:  Giovanni Miraglia <giovanni@miraglia-bi.com>")
    print(f"   Cc:  Michael Kipfer  <michael@kipfer-dp.com>")
    print(f"   Subj: {SUBJECT}")
    print()

    token = get_token()

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
