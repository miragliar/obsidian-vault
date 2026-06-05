#!/usr/bin/env python3
"""
_fetch_v2_toolkit.py
--------------------
Einmaliger Helper: Findet Giovannis Mail mit dem v2-Toolkit und schreibt alle
Anhaenge nach scripts/_staging-v2/. Macht KEINE Aenderungen an bestehenden Skripten.

Aufruf:
  M365_CLIENT_ID=... M365_TENANT_ID=... ./.venv/bin/python3 _fetch_v2_toolkit.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
from pathlib import Path

import msal
import requests

CLIENT_ID = os.environ["M365_CLIENT_ID"]
TENANT_ID = os.environ["M365_TENANT_ID"]
GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Mail.Read"]
SUBJECT_NEEDLE = "M365-Toolkit v2"
SENDER_HINT = "giovanni@miraglia-bi.com"

SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_FILE = SCRIPT_DIR / ".token_cache.bin"
STAGING = SCRIPT_DIR / "_staging-v2"
STAGING.mkdir(exist_ok=True)


def get_token() -> str:
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
        print("\n" + "=" * 60 + f"\n{flow['message']}\n" + "=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if cache.has_state_changed:
        CACHE_FILE.write_text(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"Login fehlgeschlagen: {result.get('error_description')}")
    return result["access_token"]


def find_message(token: str) -> dict:
    """Suche nach dem v2-Mail. $search braucht ConsistencyLevel: eventual."""
    headers = {
        "Authorization": f"Bearer {token}",
        "ConsistencyLevel": "eventual",
    }
    # 1) Per $search ueber Subject + Absender
    url = (
        f'{GRAPH}/me/messages?$search="subject:{SUBJECT_NEEDLE}"'
        "&$select=id,subject,from,receivedDateTime,hasAttachments"
        "&$top=10"
    )
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    items = r.json().get("value", [])
    # Filter: vom richtigen Absender, mit Anhaengen, neueste zuerst
    def _from(m: dict) -> str:
        return ((m.get("from") or {}).get("emailAddress") or {}).get("address", "").lower()
    cands = [
        m for m in items
        if SENDER_HINT.lower() in _from(m) and m.get("hasAttachments")
    ]
    cands.sort(key=lambda m: m.get("receivedDateTime", ""), reverse=True)
    if not cands:
        # 2) Fallback ohne Absender-Filter
        cands = [m for m in items if m.get("hasAttachments")]
        cands.sort(key=lambda m: m.get("receivedDateTime", ""), reverse=True)
    if not cands:
        print("Suchergebnisse (ohne hasAttachments-Filter):")
        for m in items:
            print(f"  - {m.get('receivedDateTime')} | {_from(m)} | {m.get('subject')!r} | att={m.get('hasAttachments')}")
        sys.exit("Keine passende Mail mit Anhang gefunden.")
    chosen = cands[0]
    print(f"Gefunden: {chosen['receivedDateTime']} | {_from(chosen)} | {chosen['subject']!r} (id={chosen['id'][:20]}...)")
    return chosen


def dump_attachments(token: str, msg_id: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    # Wir holen alles inkl. contentBytes via $expand
    url = f"{GRAPH}/me/messages/{msg_id}/attachments"
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    atts = r.json().get("value", [])
    manifest = []
    for att in atts:
        atype = att.get("@odata.type", "")
        name = att.get("name") or f"unnamed_{att.get('id','x')[:8]}"
        if "fileAttachment" not in atype:
            print(f"  -> SKIP non-file attachment: {name} ({atype})")
            continue
        b64 = att.get("contentBytes")
        if not b64:
            # Bei grossen Anhaengen muss man explizit GET /attachments/{id} machen
            r2 = requests.get(f"{url}/{att['id']}", headers=headers, timeout=60)
            r2.raise_for_status()
            b64 = r2.json().get("contentBytes", "")
        data = base64.b64decode(b64)
        target = STAGING / name
        target.write_bytes(data)
        sha = hashlib.sha256(data).hexdigest()[:16]
        manifest.append({
            "name": name,
            "size": len(data),
            "sha256_16": sha,
            "contentType": att.get("contentType"),
        })
        print(f"  -> wrote {name} ({len(data):,} bytes, sha256[:16]={sha})")
    return manifest


def main() -> None:
    token = get_token()
    msg = find_message(token)
    manifest = dump_attachments(token, msg["id"])
    summary = {
        "message_id": msg["id"],
        "subject": msg["subject"],
        "received": msg["receivedDateTime"],
        "from": ((msg.get("from") or {}).get("emailAddress") or {}).get("address"),
        "attachments": manifest,
        "staging_dir": str(STAGING),
    }
    (STAGING / "_manifest.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nFertig: {len(manifest)} Anhaenge -> {STAGING}")
    print(f"Manifest: {STAGING / '_manifest.json'}")


if __name__ == "__main__":
    main()
