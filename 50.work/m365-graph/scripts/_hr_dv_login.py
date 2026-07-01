#!/usr/bin/env python3
"""Device-Code-Login (MVM-Tenant) fuer Dataverse-Zugriff auf die HR-Umgebung.

Die Miraglia-App (0c8e309d) ist im MVM-Tenant nicht fuer Dynamics freigegeben
(AADSTS700016). Deshalb First-Party Public Client 'Azure CLI', der in jedem
Tenant existiert und fuer Dynamics CRM vorautorisiert ist. Token landet in einem
eigenen Keychain-Item, damit nichts vermischt wird."""
import sys
import msal
from pathlib import Path
from msal_extensions import KeychainPersistence, PersistedTokenCache

CLIENT_ID = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"  # Azure CLI (public, multi-tenant)
TENANT_ID = "3becd9bb-f602-4c6b-8e86-f1e42db365ea"   # MVM AG
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://globaldisco.crm.dynamics.com/user_impersonation"]

sig = str(Path.home() / ".config" / "m365-mvm" / "hr_dataverse.signal")
Path(sig).parent.mkdir(parents=True, exist_ok=True)
cache = PersistedTokenCache(KeychainPersistence(sig, "MVM-HR-Dataverse", "azcli-dv"))
app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

for acc in app.get_accounts():
    r = app.acquire_token_silent(SCOPES, account=acc)
    if r and "access_token" in r:
        print("SILENT_OK", acc.get("username"), len(r["access_token"]), flush=True)
        sys.exit(0)

flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    print("INITIATE_FAILED:", flow.get("error"), "|", flow.get("error_description"), flush=True)
    sys.exit(1)
print("DEVICELOGIN_URL:", flow["verification_uri"], flush=True)
print("DEVICELOGIN_CODE:", flow["user_code"], flush=True)
print("FULL_MESSAGE:", flow["message"], flush=True)
res = app.acquire_token_by_device_flow(flow)
if "access_token" in res:
    print("AUTH_OK token_len", len(res["access_token"]), flush=True)
else:
    print("AUTH_FAILED:", res.get("error"), "|", res.get("error_description"), flush=True)
