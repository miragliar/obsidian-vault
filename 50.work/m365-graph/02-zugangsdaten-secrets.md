---
source: claude-import
imported: 2026-06-01
type: secrets
sensitivity: internal
do_not_share: true
do_not_commit_externally: true
tags: [miraglia, m365, secrets, internal]
---

# Zugangsdaten — M365 App-Registrierung Miraglia BI

> [!warning] Interne Werte — nicht extern teilen
> CLIENT_ID und TENANT_ID sind kein „Secret" im engsten Sinn (Public Client, keine Client-Secret), aber sie identifizieren den Miraglia-Tenant und die App-Registrierung. Nicht in öffentliche Repos, Pastebins oder externe Chats kopieren.
> Falls dieser Vault jemals in ein externes Git-Repo gespiegelt würde: diese Datei muss vor dem Push in `.gitignore` aufgenommen werden.

## Werte (aus separater Mail Giovanni Miraglia, Juni 2026)

```
M365_CLIENT_ID = 0c8e309d-d02e-4244-ae2a-dbb5551cb550
M365_TENANT_ID = ae7f72de-197d-4ba0-a852-40ee367a5150
```

## Setzen pro Plattform

### macOS / Linux (Bash / Zsh)

Einmalig im Terminal:

```bash
export M365_CLIENT_ID="0c8e309d-d02e-4244-ae2a-dbb5551cb550"
export M365_TENANT_ID="ae7f72de-197d-4ba0-a852-40ee367a5150"
```

Persistent (z.B. `~/.zshrc`):

```bash
# Miraglia BI — M365 Graph (Public Client)
export M365_CLIENT_ID="0c8e309d-d02e-4244-ae2a-dbb5551cb550"
export M365_TENANT_ID="ae7f72de-197d-4ba0-a852-40ee367a5150"
```

Danach `source ~/.zshrc` oder Terminal neu starten.

### Windows PowerShell

```powershell
$env:M365_CLIENT_ID="0c8e309d-d02e-4244-ae2a-dbb5551cb550"
$env:M365_TENANT_ID="ae7f72de-197d-4ba0-a852-40ee367a5150"
```

Persistent (User-Scope):

```powershell
[System.Environment]::SetEnvironmentVariable("M365_CLIENT_ID", "0c8e309d-d02e-4244-ae2a-dbb5551cb550", "User")
[System.Environment]::SetEnvironmentVariable("M365_TENANT_ID", "ae7f72de-197d-4ba0-a852-40ee367a5150", "User")
```

### Per `.env`-Datei (empfohlen, wenn Skripte oft laufen)

Datei `scripts/.env`:

```
M365_CLIENT_ID=0c8e309d-d02e-4244-ae2a-dbb5551cb550
M365_TENANT_ID=ae7f72de-197d-4ba0-a852-40ee367a5150
```

Im Terminal aktivieren:

```bash
cd scripts && set -a && source .env && set +a
```

→ `scripts/.gitignore` enthält `.env` bereits.

## Kontext / Eigenschaften der App-Registrierung

- **Tenant:** Miraglia Business-Intelligence
- **Public Client:** ja (kein Client-Secret nötig, Device-Code-Flow erlaubt)
- **Delegierte Permissions (mit Admin-Consent):**
  - `User.Read` (Standard)
  - `Mail.Read`
  - `Chat.Read`
- **Authority-URL:** `https://login.microsoftonline.com/ae7f72de-197d-4ba0-a852-40ee367a5150`

## Verifikation

Nach dem Setzen der Env-Vars:

```bash
echo $M365_CLIENT_ID
echo $M365_TENANT_ID
```

→ sollten beide GUIDs ausgeben. Falls leer: Shell-Profile neu sourcen oder Terminal-Tab neu öffnen.

## Zefix-API (für company_enrich.py --zefix)

Optional, kostenlose Registrierung: https://www.zefix.ch → API

Nach Registrierung + Bestätigung:

```bash
export ZEFIX_USER="<dein-zefix-username>"
export ZEFIX_PASS="<dein-zefix-passwort>"
```

→ noch nicht angelegt (Stand 01.06.2026). Für reine Webseite-Lookups nicht nötig.

## 🔐 Token-Storage-Regel (Giovanni 2026-06-09)

> **Tokens IMMER verschlüsselt im OS-Keystore, NIE als Klartext im Vault.**
>
> Mail-Referenz: Giovanni Miraglia → Raoul/Ale, 2026-06-09:
> „Wichtig: Tokens immer verschlüsselt (Keychain/DPAPI) — nie als Klartext in unseren Skripten"
>
> Voll-Dokumentation der Regel und Umsetzung: [[09-regel-tokens-verschluesselt-keystore]]

**Umsetzung in Kürze:**
- macOS → **Keychain** via `msal_extensions.KeychainPersistence` + `PersistedTokenCache`
- Windows → **DPAPI** via `msal_extensions.build_encrypted_persistence()` (automatische Wahl)
- M365-Token: `auth_common.build_cache()` (Service `MiragliaBI-M365`, Account `graph-token-cache`)
- Power-BI Multi-Tenant: `auth_common.build_pbi_cache(tenant)` (Service `MiragliaBI-PowerBI`, Account = Tenant-Slug)
- MVM-AG Tenant: `auth_mvm.build_cache()` (Service `MVM-Offerte-Scan`)
- `.gitignore` deckt `*.bin`, `.token_cache*`, `.pbi_token_cache_*` als Defense-in-Depth

**Verboten:**
- `msal.SerializableTokenCache()` → `.token_cache.bin`-Datei im Vault
- `cache.serialize()` / `cache.deserialize()` in eigene Datei
- Token in Env-Vars oder `.env` ablegen
- Token in Logs / Output committen

## Verwandt

- [[setup-und-workflow]]
- [[01-chef-mail-juni-2026]]
- [[04-company-enrich-workflow]]
- [[09-regel-tokens-verschluesselt-keystore]] — Token-Verschlüsselungs-Regel (Detail)
