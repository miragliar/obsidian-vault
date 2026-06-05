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
atts=[]
if LOGO.exists() and f"cid:{LOGO_CID}" in body:
    atts.append({"@odata.type":"#microsoft.graph.fileAttachment","name":"miraglia-bi.png",
                 "contentType":"image/png","isInline":True,"contentId":LOGO_CID,
                 "contentBytes":base64.b64encode(LOGO.read_bytes()).decode()})
for fp in cfg.get("attachments",[]):
    p=Path(fp); ct=mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    atts.append({"@odata.type":"#microsoft.graph.fileAttachment","name":p.name,
                 "contentType":ct,"contentBytes":base64.b64encode(p.read_bytes()).decode()})
msg={"subject":cfg["subject"],"body":{"contentType":"HTML","content":body},
     "toRecipients":[{"emailAddress":{"address":a}} for a in cfg.get("to",[])],
     "ccRecipients":[{"emailAddress":{"address":a}} for a in cfg.get("cc",[])],
     "attachments":atts}
r=requests.post(f"{GRAPH}/me/messages",headers=h,json=msg,timeout=120); r.raise_for_status()
d=r.json()
print("✓ Entwurf erstellt (NICHT gesendet)")
print("  An      :", ", ".join(x['emailAddress']['address'] for x in d.get('toRecipients',[])) or "—")
print("  Betreff :", d.get("subject"))
print("  Anhänge :", ", ".join(a['name'] for a in d.get('attachments',[])) if d.get('attachments') else d.get('hasAttachments'))
print("  Öffnen  :", d.get("webLink","—"))
