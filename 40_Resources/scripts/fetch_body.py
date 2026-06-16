import sys,re,html
from pathlib import Path
import requests
SD=Path(__file__).resolve().parent
GRAPH="https://graph.microsoft.com/v1.0"
# Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
from auth_common import get_token as _ac_get_token
tok=_ac_get_token(["Mail.Read","User.Read"])
q=sys.argv[1]
url=f'{GRAPH}/me/messages?$search="{q}"&$select=subject,from,toRecipients,receivedDateTime,body,hasAttachments&$top=5'
r=requests.get(url,headers={"Authorization":f"Bearer {tok}"},timeout=60); r.raise_for_status()
for m in r.json().get("value",[]):
    subj=m.get("subject","")
    flt=sys.argv[2].lower() if len(sys.argv)>2 else ""
    if flt and flt not in subj.lower(): continue
    frm=((m.get("from") or {}).get("emailAddress") or {}).get("address","")
    print("DATE:",m.get("receivedDateTime"))
    print("FROM:",frm,"| ATTACH:",m.get("hasAttachments"))
    print("SUBJ:",subj)
    body=(m.get("body") or {}).get("content","")
    if (m.get("body") or {}).get("contentType")=="html":
        body=re.sub(r"<(script|style)[^>]*>.*?</\1>","",body,flags=re.S|re.I)
        body=re.sub(r"<[^>]+>"," ",body)
        body=html.unescape(body)
    body=re.sub(r"[ \t]+"," ",body); body=re.sub(r"\n\s*\n+","\n\n",body)
    print("----- BODY -----"); print(body.strip()[:4000]); print("================\n")
