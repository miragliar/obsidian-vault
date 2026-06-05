#!/usr/bin/env python3
"""
auth_common.py — Gemeinsame MSAL-Authentifizierung für alle M365/Graph-Skripte.

Der Token-Cache liegt im **macOS Keychain** (verschlüsselt, ACL-geschützt, KEIN
Cloud-Sync) — nicht mehr als Klartext-Datei im Dropbox-synchronisierten Vault.

Verwendung in einem Skript:
    from auth_common import get_token, CLIENT_ID, TENANT_ID, GRAPH
    SCOPES = ["User.Read", "Mail.Read"]
    token = get_token(SCOPES)

Erstanmeldung (einmalig, interaktiv): Fehlt ein gültiger Token im Keychain und
läuft das Skript in einem Terminal, wird automatisch der Device-Code-Flow
gestartet. Unbeaufsichtigte Läufe (launchd) ohne gültigen Token brechen mit
klarer Meldung ab, statt zu hängen.

Einmalige Migration / Self-Test:
    ./.venv/bin/python auth_common.py            # migriert evtl. vorhandene .token_cache.bin → Keychain, dann Test
    ./.venv/bin/python auth_common.py --test     # nur Funktionstest (kein Device-Flow)
"""
import os
import sys
from pathlib import Path

import msal
from msal_extensions import KeychainPersistence, PersistedTokenCache

# --- Öffentliche Identifikatoren (KEINE Secrets) — per Env-Var überschreibbar ---
CLIENT_ID = os.environ.get("M365_CLIENT_ID", "0c8e309d-d02e-4244-ae2a-dbb5551cb550")
TENANT_ID = os.environ.get("M365_TENANT_ID", "ae7f72de-197d-4ba0-a852-40ee367a5150")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH = "https://graph.microsoft.com/v1.0"

# --- Keychain-Koordinaten des Token-Items ---
_KEYCHAIN_SERVICE = "MiragliaBI-M365"
_KEYCHAIN_ACCOUNT = "graph-token-cache"

# Signal-/Lock-Datei für Cross-Prozess-Locking (enthält KEINE Token-Daten —
# die liegen im Keychain). Lokal, außerhalb von Dropbox/iCloud/OneDrive.
_SIGNAL_DIR = Path(os.environ.get("M365_CACHE_DIR", str(Path.home() / ".config" / "m365-sync")))
_SIGNAL_FILE = _SIGNAL_DIR / "token_cache.signal"

# Alt-Speicherort (Klartext im Vault/Dropbox) — nur noch für die einmalige Migration.
_LEGACY_CACHE = Path(__file__).resolve().parent / ".token_cache.bin"


def _persistence():
    _SIGNAL_DIR.mkdir(parents=True, exist_ok=True)
    return KeychainPersistence(str(_SIGNAL_FILE), _KEYCHAIN_SERVICE, _KEYCHAIN_ACCOUNT)


def build_cache():
    """Persistenter MSAL-Token-Cache im macOS Keychain."""
    return PersistedTokenCache(_persistence())


def build_app(cache=None):
    return msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY, token_cache=cache or build_cache())


def get_token(scopes, allow_device_flow=True):
    """Access-Token holen: silent refresh aus Keychain; sonst Device-Flow (nur im TTY)."""
    scopes = list(scopes)
    app = build_app()
    result = None
    for acc in app.get_accounts():
        result = app.acquire_token_silent(scopes, account=acc)
        if result:
            break
    if not result:
        interactive_ok = allow_device_flow and sys.stdin is not None and sys.stdin.isatty()
        if not interactive_ok:
            sys.exit(
                "❌ Kein gültiger Token im Keychain und keine interaktive Sitzung.\n"
                "   Bitte einmal manuell anmelden, z. B.:\n"
                "       ./.venv/bin/python live_search.py test")
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60 + f"\n{flow['message']}\n" + "=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if not result or "access_token" not in result:
        sys.exit(f"Token-Erwerb fehlgeschlagen: {result}")
    return result["access_token"]


def migrate_legacy_cache(path=_LEGACY_CACHE):
    """Einmalig: vorhandenen Klartext-Cache (.token_cache.bin) in den Keychain übernehmen."""
    path = Path(path)
    if not path.exists():
        print(f"ℹ️  Kein Alt-Cache unter {path} — nichts zu migrieren.")
        return False
    data = path.read_text()
    persistence = _persistence()
    persistence.save(data)
    if persistence.load() != data:
        sys.exit("❌ Verifikation fehlgeschlagen: Keychain-Inhalt ≠ Quelldatei.")
    print(f"✅ Token-Cache aus {path.name} in den Keychain übernommen "
          f"(Service={_KEYCHAIN_SERVICE}, Account={_KEYCHAIN_ACCOUNT}).")
    return True


def _self_test():
    """Funktionstest ohne Device-Flow: holt einen Token rein aus dem Keychain-Cache."""
    token = get_token(["User.Read"], allow_device_flow=False)
    print(f"✅ Keychain-Auth funktioniert — Access-Token erhalten ({len(token)} Zeichen).")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _self_test()
    else:
        migrate_legacy_cache()
        _self_test()
