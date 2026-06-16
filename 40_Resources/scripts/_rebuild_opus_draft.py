#!/usr/bin/env python3
"""
Baut den Opus-1M-Entwurf neu auf:
  1) 3 Screenshots INLINE an der jeweils richtigen Textstelle (cid:), NICHT als Anhang
  2) Logo-Bug behoben: ALLE Inline-Bilder (Logo + 3 Shots) werden EINZELN per
     Folge-POST an den fertigen Entwurf gehängt — nicht im Create-POST.
     (Im Create-POST verknüpft Graph Inline-Bilder unzuverlässig -> Broken-Image.)
Alter Entwurf wird vorher gelöscht. Es wird NICHTS gesendet.
"""
import base64
from pathlib import Path

import requests
from auth_common import get_token

GRAPH = "https://graph.microsoft.com/v1.0"
SD = Path(__file__).resolve().parent
IMG = SD / "_opus_draft"
SIG = SD / "signatur.html"
LOGO = SD / "logo_sig.png"

TO = ["raoul@miraglia-bi.com", "michael@kipfer-dp.com", "alessandro@castelli-solutions.ch"]
SUBJECT = "Claudian: Opus 4.8 (Opus 1M) aktivieren — kurze Anleitung"

# (Datei im _opus_draft, cid, Anzeigebreite px, alt-Text)
SHOTS = [
    ("1_Claudian-Optionen-oeffnen.png", "claudian-shot-1", 640, "Screenshot 1 — Claudian-Optionen öffnen"),
    ("2_Opus-1M-aktivieren.png",        "claudian-shot-2", 600, "Screenshot 2 — Opus 1M einschalten"),
    ("3_Modell-Opus-1M-waehlen.png",    "claudian-shot-3", 300, "Screenshot 3 — Modell „Opus 1M“ auswählen"),
]
LOGO_CID = "miragliabi-logo"


def img_tag(cid, width, alt):
    return (f'<div style="margin:12px 0 18px 0;">'
            f'<img src="cid:{cid}" width="{width}" alt="{alt}" '
            f'style="display:block; width:{width}px; max-width:100%; height:auto; '
            f'border:1px solid #d0d0d0; border-radius:6px;"></div>')


I1 = img_tag(SHOTS[0][1], SHOTS[0][2], SHOTS[0][3])
I2 = img_tag(SHOTS[1][1], SHOTS[1][2], SHOTS[1][3])
I3 = img_tag(SHOTS[2][1], SHOTS[2][2], SHOTS[2][3])

signature = "<br><br>" + SIG.read_text(encoding="utf-8").strip() if SIG.exists() else ""

BODY = f"""Hallo zusammen<br><br>
kurzer Tipp für <b>Claudian</b> (unser Obsidian-KI-Plugin): Ihr könnt <b>Opus 4.8</b> freischalten — im Modell-Wähler heisst es <b>„Opus 1M“</b> (1-Mio-Token-Kontextfenster). Damit habt Ihr im Picker mehr Auswahl und aktuell das stärkste Modell zur Hand.<br><br>
⚠️ <b>Gerade jetzt wichtig:</b> „Claude 5“ (Fable 5) ist momentan <b>weltweit temporär abgeschaltet</b>. Bis es zurückkommt, ist <b>Opus 4.8 (Opus 1M)</b> die beste Wahl.<br><br>
<b>Anleitung — bitte genau in dieser Reihenfolge:</b><br><br>
<b>1) Claudian-Optionen öffnen</b><br>
Obsidian → Einstellungen → links unter <b>„Externe Erweiterungen“</b> → bei <b>Claudian</b> auf das <b>Zahnrad (Optionen)</b> klicken.<br>
{I1}
<b>2) Opus 1M einschalten</b><br>
Oben den Tab <b>„Claude“</b> wählen → runterscrollen zu <b>„Models“</b> → den Schalter <b>„Opus 1M context window“</b> auf <b>AN</b> stellen.<br>
<span style="color:#666">(Optional: Im Feld „Custom models“ steht <code>claude-fable-5</code> — das ist Claude 5 und greift erst wieder, sobald es weltweit reaktiviert ist.)</span><br>
{I2}
<b>3) Modell auswählen</b><br>
Zurück im Chat oben auf den <b>Modell-Wähler</b> (die Tabs 1 · 2 · 3) klicken → <b>„Opus 1M“</b> auswählen. Fertig ✅<br>
{I3}
<b>Wichtig:</b> Schritt 2 nicht überspringen — ohne den aktivierten Schalter erscheint „Opus 1M“ im Wähler gar nicht.<br><br>
Liebe Grüsse{signature}"""


def inline_att(path, cid, name, ctype="image/png"):
    return {"@odata.type": "#microsoft.graph.fileAttachment", "name": name,
            "contentType": ctype, "isInline": True, "contentId": cid,
            "contentBytes": base64.b64encode(Path(path).read_bytes()).decode()}


tok = get_token(["Mail.ReadWrite", "User.Read"])
h = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}

# 1) alten Entwurf löschen
old = requests.get(f"{GRAPH}/me/mailFolders/drafts/messages", headers=h,
                   params={"$search": '"Opus 1M"', "$select": "id,subject", "$top": "25"}, timeout=60)
for m in old.json().get("value", []):
    if "Opus" in (m.get("subject") or ""):
        requests.delete(f"{GRAPH}/me/messages/{m['id']}", headers=h, timeout=30)
        print("  alten Entwurf gelöscht:", m["id"][:24], "…")

# 2) neuen Entwurf NUR mit Body anlegen (keine Inline-Bilder im Create-POST!)
msg = {"subject": SUBJECT, "body": {"contentType": "HTML", "content": BODY},
       "toRecipients": [{"emailAddress": {"address": a}} for a in TO]}
r = requests.post(f"{GRAPH}/me/messages", headers=h, json=msg, timeout=60)
r.raise_for_status()
mid = r.json()["id"]
print("✓ Neuer Entwurf angelegt:", mid[:24], "…")

# 3) ALLE Inline-Bilder einzeln per Folge-POST anhängen (zuverlässige Methode)
posts = [inline_att(LOGO, LOGO_CID, "miraglia-bi.png")]
for fname, cid, _w, alt in SHOTS:
    posts.append(inline_att(IMG / fname, cid, fname))

for att in posts:
    ra = requests.post(f"{GRAPH}/me/messages/{mid}/attachments", headers=h, json=att, timeout=120)
    ra.raise_for_status()
    print(f"  + inline angehängt: {att['name']}  (cid={att['contentId']})")

# 4) Kontrolle
chk = requests.get(f"{GRAPH}/me/messages/{mid}/attachments", headers=h,
                   params={"$select": "name,isInline,contentId,size,contentType"}, timeout=60).json()
print("\nKontrolle — Anhänge am Entwurf:")
for a in chk.get("value", []):
    print(f"  - {a['name']:34s} inline={a['isInline']}  cid={a.get('contentId')}  {a['size']} B")
link = requests.get(f"{GRAPH}/me/messages/{mid}", headers=h, params={"$select": "webLink"}, timeout=30).json()
print("\nÖffnen:", link.get("webLink", "—"))
print("→ NICHT gesendet. Bitte in Outlook prüfen & selbst senden.")
