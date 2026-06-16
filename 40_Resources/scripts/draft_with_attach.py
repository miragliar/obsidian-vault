import sys, json, base64, mimetypes
from pathlib import Path
import requests
SD=Path(__file__).resolve().parent
GRAPH="https://graph.microsoft.com/v1.0"
SCOPES=["Mail.ReadWrite","User.Read"]
LOGO=SD/"logo_sig.png"; SIG=SD/"signatur.html"; LOGO_CID="miragliabi-logo"

def token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)

def file_att(path, inline=False, cid=None, name=None):
    p=Path(path); ct=mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    a={"@odata.type":"#microsoft.graph.fileAttachment","name":name or p.name,
       "contentType":ct,"contentBytes":base64.b64encode(p.read_bytes()).decode()}
    if inline:
        a["isInline"]=True; a["contentId"]=cid
    return a

cfg=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
tok=token(); h={"Authorization":f"Bearer {tok}","Content-Type":"application/json"}

# delete previous drafts with same subject
if cfg.get("delete_old"):
    q=requests.get(f"{GRAPH}/me/mailFolders/drafts/messages?$filter=subject eq '{cfg['subject']}'&$select=id,subject",headers=h,timeout=60)
    for m in q.json().get("value",[]):
        requests.delete(f"{GRAPH}/me/messages/{m['id']}",headers=h,timeout=30)
        print("  deleted old draft:",m['id'][:20],"…")

body=cfg["body"]
if SIG.exists(): body+= "<br><br>"+SIG.read_text(encoding="utf-8").strip()

# Reguläre (NICHT-inline) Datei-Anhänge dürfen im Create-POST mitfahren.
regular=[file_att(fp) for fp in cfg.get("attachments",[])]
msg={"subject":cfg["subject"],"body":{"contentType":"HTML","content":body},
     "toRecipients":[{"emailAddress":{"address":a}} for a in cfg.get("to",[])],
     "ccRecipients":[{"emailAddress":{"address":a}} for a in cfg.get("cc",[])],
     "attachments":regular}
r=requests.post(f"{GRAPH}/me/messages",headers=h,json=msg,timeout=120); r.raise_for_status()
d=r.json(); mid=d["id"]

# WICHTIG: Inline-Bilder (Logo + per cfg["inline_images"]) erst NACH dem Erstellen
# einzeln per Folge-POST anhängen. Im Create-POST verknüpft Graph Inline-Bilder
# unzuverlässig mit ihrem cid: -> Broken-Image (das berühmte "?"-Kästchen).
# inline_images: Liste von {"path": "...", "cid": "...", "name": "optional.png"};
# der jeweilige cid muss als <img src="cid:..."> im Body/Signatur stehen.
inline_posts=[]
if LOGO.exists() and f"cid:{LOGO_CID}" in body:
    inline_posts.append(file_att(LOGO, inline=True, cid=LOGO_CID, name="miraglia-bi.png"))
for im in cfg.get("inline_images",[]):
    inline_posts.append(file_att(im["path"], inline=True, cid=im["cid"], name=im.get("name")))
for att in inline_posts:
    ra=requests.post(f"{GRAPH}/me/messages/{mid}/attachments",headers=h,json=att,timeout=120); ra.raise_for_status()
    print("  + inline angehängt:",att["name"],"(cid="+att["contentId"]+")")

print("✓ Entwurf erstellt (NICHT gesendet)")
print("  An      :", ", ".join(x['emailAddress']['address'] for x in d.get('toRecipients',[])) or "—")
print("  Betreff :", d.get("subject"))
print("  Öffnen  :", d.get("webLink","—"))
