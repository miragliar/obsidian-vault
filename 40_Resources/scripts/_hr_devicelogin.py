#!/usr/bin/env python3
"""Einmaliger Device-Code-Login für den HR-Zeugnistool-Tenant (3becd9bb...).
Holt einen Global-Discovery-Token, ermittelt die Org-URL der Umgebung
252f3c4a-8224-e820-88be-dc407bc16756 und speichert den Token in einem
lokalen Keychain-Item (getrennt vom Miraglia-Cache)."""
import sys
import msal
from msal_extensions import KeychainPersistence, PersistedTokenCache

CLIENT_ID = "0c8e309d-d02e-4244-ae2a-dbb5551cb550"
TENANT_ID = "3becd9bb-f602-4c6b-8e86-f1e42db365ea"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://globaldisco.crm.dynamics.com/user_impersonation"]

sig = str((__import__("pathlib").Path.home() / ".config" / "m365-sync" / "hr_tenant.signal"))
__import__("pathlib").Path(sig).parent.mkdir(parents=True, exist_ok=True)
cache = PersistedTokenCache(KeychainPersistence(sig, "MiragliaBI-HR-Tenant", "globaldisco"))
app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    print("INITIATE_FAILED:", flow.get("error"), flow.get("error_description"), flush=True)
    sys.exit(1)
print("DEVICELOGIN_URL:", flow["verification_uri"], flush=True)
print("DEVICELOGIN_CODE:", flow["user_code"], flush=True)
print("FULL_MESSAGE:", flow["message"], flush=True)
result = app.acquire_token_by_device_flow(flow)  # blockiert bis Login/Timeout
if "access_token" in result:
    print("AUTH_OK token_len", len(result["access_token"]), flush=True)
else:
    print("AUTH_FAILED:", result.get("error"), result.get("error_description"), flush=True)
