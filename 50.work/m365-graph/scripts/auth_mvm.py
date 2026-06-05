#!/usr/bin/env python3
"""
auth_mvm.py — MSAL-Authentifizierung gegen den MVM-AG-Tenant.

Analog zu auth_common.py (Miraglia-BI-Tenant), aber gegen den MVM-Tenant
`3becd9bb-f602-4c6b-8e86-f1e42db365ea` (EU). Wiederverwendung der bestehenden
Miraglia-BI-Multi-Tenant-App (Client-ID `0c8e309d-…`). Token landet im
macOS-Keychain unter einem separaten Item, damit MVM- und Miraglia-BI-
Tokens nebeneinander existieren können.

Verwendung in einem Skript:
    from auth_mvm import get_token, GRAPH
    SCOPES = ["Mail.Read.Shared"]
    token = get_token(SCOPES)

Erstanmeldung (interaktiv):
    ./.venv/bin/python auth_mvm.py            # Device-Flow gegen MVM-Tenant
    ./.venv/bin/python auth_mvm.py --probe    # nur diagnostischer Probe-Login,
                                              # zeigt klar an, ob User-Consent
                                              # reicht oder Admin-Consent nötig ist
"""
import os
import sys
from pathlib import Path

import msal
from msal_extensions import KeychainPersistence, PersistedTokenCache

# --- MVM-Tenant + Miraglia-BI-App (Multi-Tenant) ----------------------------
CLIENT_ID = os.environ.get("M365_CLIENT_ID", "0c8e309d-d02e-4244-ae2a-dbb5551cb550")
MVM_TENANT_ID = os.environ.get(
    "MVM_TENANT_ID", "3becd9bb-f602-4c6b-8e86-f1e42db365ea")
AUTHORITY = f"https://login.microsoftonline.com/{MVM_TENANT_ID}"
GRAPH = "https://graph.microsoft.com/v1.0"

# --- Keychain-Koordinaten (separates Item, NICHT mit Miraglia-BI gemischt) --
_KEYCHAIN_SERVICE = "MVM-Offerte-Scan"
_KEYCHAIN_ACCOUNT = "graph-token-cache"

# Signal-/Lock-Datei für Cross-Prozess-Locking. Lokal, außerhalb Dropbox.
_SIGNAL_DIR = Path(os.environ.get(
    "MVM_CACHE_DIR", str(Path.home() / ".config" / "m365-mvm")))
_SIGNAL_FILE = _SIGNAL_DIR / "token_cache.signal"


def _persistence():
    _SIGNAL_DIR.mkdir(parents=True, exist_ok=True)
    return KeychainPersistence(str(_SIGNAL_FILE), _KEYCHAIN_SERVICE, _KEYCHAIN_ACCOUNT)


def build_cache():
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
                "❌ Kein gültiger MVM-Token im Keychain und keine interaktive Sitzung.\n"
                "   Bitte einmal manuell anmelden:\n"
                "       ./.venv/bin/python auth_mvm.py")
        flow = app.initiate_device_flow(scopes=scopes)
        if "user_code" not in flow:
            sys.exit(f"Device-Flow fehlgeschlagen: {flow.get('error_description')}")
        print("\n" + "=" * 60 + f"\n{flow['message']}\n" + "=" * 60 + "\n", flush=True)
        result = app.acquire_token_by_device_flow(flow)
    if not result or "access_token" not in result:
        # Rückgabe enthält die Fehler-Details (z.B. AADSTS-Code) — wertvoll für Diagnose.
        err = result or {}
        err_code = err.get("error", "")
        err_desc = err.get("error_description", "")
        diag = _interpret_error(err_code, err_desc)
        sys.exit(
            f"❌ Token-Erwerb fehlgeschlagen.\n"
            f"   error: {err_code}\n"
            f"   description: {err_desc[:400]}\n"
            f"\n📋 Diagnose: {diag}"
        )
    return result["access_token"]


def _interpret_error(err_code: str, err_desc: str) -> str:
    """Macht die nackten Azure-Fehler-Codes für den User lesbar."""
    desc_low = (err_desc or "").lower()
    if "aadsts65001" in desc_low or "consent" in desc_low and "admin" in desc_low:
        return (
            "Admin-Consent erforderlich. Die Miraglia-BI-App ist im MVM-Tenant "
            "noch nicht freigegeben. Remo (oder ein anderer MVM-Admin) muss "
            "einen einmaligen Consent-Klick machen. Consent-Link kann generiert "
            "werden — siehe README im Repo."
        )
    if "aadsts50020" in desc_low:
        return (
            "Der angemeldete User existiert im MVM-Tenant nicht. Hast du dich "
            "wirklich mit einem MVM-User (Endung @mvm-ag.ch) eingeloggt?"
        )
    if "aadsts70016" in desc_low:
        return (
            "Device-Code-Flow Timeout — User hat sich nicht (rechtzeitig) "
            "eingeloggt. Skript einfach nochmal starten."
        )
    if err_code in ("invalid_grant", "interaction_required"):
        return (
            "Interaktion erforderlich (z.B. Re-Auth / MFA). Skript nochmal "
            "starten, Login wiederholen."
        )
    return (
        "Unbekannter Fehler. Bitte den vollständigen Fehler-Text googeln oder "
        "an Raoul melden."
    )


def _probe():
    """Diagnostischer Probe-Lauf — direkt mit Device-Flow, ohne TTY-Sperre.

    Anders als get_token() ist dieser Pfad bewusst auch für Hintergrund-Tasks
    geeignet (Background-Bash, dem User wird die URL+Code zugespielt).
    """
    print("=" * 70)
    print("🔍 MVM-Tenant Auth-Probe")
    print("=" * 70)
    print(f"   Tenant:    MVM AG ({MVM_TENANT_ID})")
    print(f"   App:       Miraglia-BI ({CLIENT_ID}) — Multi-Tenant-fähig")
    print(f"   Scopes:    Mail.Read.Shared + User.Read")
    print(f"   Keychain:  {_KEYCHAIN_SERVICE} / {_KEYCHAIN_ACCOUNT}")
    print()
    print("📋 Was zu erwarten ist (in Reihenfolge):")
    print("   1. Skript zeigt URL + Code")
    print("   2. Du öffnest URL in einem Browser")
    print("   3. Du loggst dich mit dem MVM-User-Account ein (inkl. MFA)")
    print("   4a. Wenn User-Consent erlaubt: Consent-Dialog erscheint, du klickst zustimmen → Token")
    print("   4b. Wenn Admin-Consent erzwungen: Fehler AADSTS65001 → Diagnose zeigt nächste Schritte")
    print()
    print("─" * 70, flush=True)

    scopes = ["Mail.Read.Shared", "User.Read"]
    app = build_app()

    # Erst silent-acquire probieren (falls Token schon im Keychain)
    for acc in app.get_accounts():
        result = app.acquire_token_silent(scopes, account=acc)
        if result and "access_token" in result:
            print("✅ Token aus Keychain (silent refresh) — kein neuer Login nötig.")
            print(f"   Token-Länge: {len(result['access_token'])} Zeichen")
            print(f"   Account: {acc.get('username','?')}")
            print()
            print("🎉 Setup steht. Reto's Datenschutz-OK abwarten, dann Scan starten.")
            return

    # Sonst Device-Flow direkt starten (TTY-Check bewusst übersprungen)
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        sys.exit(f"❌ Device-Flow konnte nicht initiiert werden: {flow.get('error_description')}")

    # URL + Code prominent anzeigen
    print()
    print("┌" + "─" * 68 + "┐")
    print("│  🌐  Login-URL + Code  (15 Min gültig)" + " " * 28 + "│")
    print("├" + "─" * 68 + "┤")
    print(f"│  URL:  {flow.get('verification_uri','https://microsoft.com/devicelogin'):<60}│")
    print(f"│  Code: {flow.get('user_code',''):<60}│")
    print("└" + "─" * 68 + "┘")
    print()
    print("📝 Microsoft's Original-Nachricht:")
    print(f"   {flow['message']}")
    print()
    print("⏳ Warte auf Login (timeout 15 Min)…", flush=True)

    # Blockiert bis User eingeloggt oder Timeout
    result = app.acquire_token_by_device_flow(flow)

    if not result or "access_token" not in result:
        err = result or {}
        err_code = err.get("error", "")
        err_desc = err.get("error_description", "")
        diag = _interpret_error(err_code, err_desc)
        print()
        print("❌ Token-Erwerb fehlgeschlagen.")
        print(f"   error: {err_code}")
        print(f"   description: {err_desc[:600]}")
        print()
        print(f"📋 Diagnose: {diag}")
        sys.exit(1)

    print()
    print("✅ Token erfolgreich erhalten!")
    print(f"   Token-Länge: {len(result['access_token'])} Zeichen")
    print(f"   Scopes erhalten: {result.get('scope', '(unbekannt)')}")
    print()

    # Token wurde via PersistedTokenCache im Keychain abgelegt — verifizieren
    print("🔐 Token-Cache im Keychain unter "
          f"Service={_KEYCHAIN_SERVICE} / Account={_KEYCHAIN_ACCOUNT}")
    print()
    print("🎉 Setup steht. User-Consent hat ausgereicht — Remo unnötig.")
    print("    Nächster Schritt: Reto's Datenschutz-OK abwarten, dann Scan starten.")


def _self_test():
    """Funktionstest ohne Device-Flow: holt einen Token rein aus dem Keychain-Cache."""
    token = get_token(["User.Read"], allow_device_flow=False)
    print(f"✅ MVM-Keychain-Auth funktioniert — Access-Token erhalten ({len(token)} Zeichen).")


if __name__ == "__main__":
    if "--test" in sys.argv:
        _self_test()
    else:
        _probe()
