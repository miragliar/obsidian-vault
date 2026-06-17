---
type: anleitung
maintainer: Raoul
created: 2026-06-17
updated: 2026-06-17
tags: [meta, claude, claudian, setup, mcp, fabric, m365, power-bi]
source: "[[60.daily/]] · Mail Giovanni 2026-06-16 17:16"
---

# Claudian — Vollausstattung (Parität mit Giovannis Setup)

Diese Anleitung dokumentiert das vollständige Setup, mit dem Claudian (Obsidian-Plugin) **und** Claude Code auf demselben Mac alle Tools sehen, die auch Giovanni nutzt: M365-Mail/OneNote/Dataverse, Power BI Multi-Tenant, Microsoft Learn live, Fabric MCP, Semantic Vault MCP, GitHub.

> **Stand:** 2026-06-17 — durchgeführt zusammen mit Claudian nach Giovannis Mail „Claudian bei Dir aufrüsten — Microsoft Learn, Fabric & das MVM-Toolkit" (16.06.2026, 17:16 Uhr).

## Architektur — 4 Bausteine

| # | Baustein | Wer hat ihn? | Sync? |
|---|---|---|---|
| 1 | **Vault** (Notes, Skripte, Skills, CLAUDE.md) | Dropbox-Sync von Giovanni-Vault | ✅ automatisch |
| 2 | **Claude-Account** (Connectors auf claude.ai) | persönlich, an Login gebunden | ❌ manuell pro User |
| 3 | **Mac-lokale Bits** (venv, MCP-Eintrag in `~/.claude.json`, `~/.zshrc`) | mein Mac | ❌ pro Maschine |
| 4 | **Tokens** (Keychain) | mein Mac, mein Login | ❌ pro User — **NIE kopieren** |

Vault syncst automatisch. Den Rest mussten wir bei mir scharf schalten.

## Endstand — was läuft

| Kategorie | Komponente | Wie eingerichtet |
|---|---|---|
| **Skripte** | `40_Resources/scripts/` (78 Files) | aus Giovannis Vault kopiert (ohne `.venv`/`__pycache__`/Tokens) |
| **venv** | `40_Resources/scripts/.venv/` | `python3 -m venv .venv && pip install -r requirements.txt` |
| **Skills** | `.claude/skills/` (m365-email, obsidian-markdown/-bases/-cli, json-canvas, defuddle) | aus Giovannis `.claude/skills/` synct |
| **CLAUDE.md** | Vault-Root | Capability-Block ergänzt; bestehende Schreibstil-/PowerFx-/Token-Regeln bleiben |
| **Env-Vars** | `~/.zshrc` | `M365_CLIENT_ID`, `M365_TENANT_ID` (öffentliche IDs, keine Secrets) |
| **MCP `microsoft-learn`** | `~/.claude.json` | `https://learn.microsoft.com/api/mcp` (HTTP, kein Login) |
| **MCP `fabric-mcp`** | `~/.claude.json` | stdio via `~/.local/bin/fabmcp server start` (Symlink → VS-Code-Extension-Binary) |
| **MCP `semantic-vault-mcp`** | `~/.claude.json` | `http://10.211.55.2:3001/mcp` (Parallels-VM-Zugriff) |
| **claude.ai Connectors** | Browser/Account | Microsoft Learn (Web) + GitHub-Integration |
| **Token `MiragliaBI-M365`** | macOS Keychain | Device-Code-Login `raoul@miraglia-bi.com` |
| **Token `MiragliaBI-PBI / mvm-ag-ch`** | macOS Keychain | Device-Code-Login `powerplatform@mvm-ag.ch` |

## Die 9 Schritte (chronologisch)

### 1. Skripte aus Giovannis Vault übernehmen

```bash
cd "/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul"
mkdir -p 40_Resources/scripts
rsync -a \
  --exclude='.venv' --exclude='__pycache__' \
  --exclude='.token_cache*' --exclude='*.bin' \
  --exclude='.pbi_token_cache_*' --exclude='.env' \
  --exclude='launchd.*.log' \
  "/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian gimi/Miragliag/40_Resources/scripts/" \
  "40_Resources/scripts/"
```

> ⚠️ **NIE** `.venv/`, Tokens (`*.bin`, `.token_cache*`, `.pbi_token_cache_*`) oder `.env` mitkopieren — Tokens sind pro User/Mac, venv ist plattform-spezifisch.

### 2. venv anlegen & dependencies installieren

```bash
cd 40_Resources/scripts
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

Drin: `msal`, `msal-extensions`, `requests`, `beautifulsoup4` & Co.

### 3. Skills synct

```bash
mkdir -p .claude/skills
rsync -a \
  "/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian gimi/Miragliag/.claude/skills/" \
  ".claude/skills/"
```

Skills: `m365-email`, `obsidian-markdown`, `obsidian-bases`, `obsidian-cli`, `json-canvas`, `defuddle`.

### 4. CLAUDE.md erweitern

Capability-Block (Mail/OneNote/Dataverse/Power BI/MCP) oben einfügen, bestehende Regeln zu Schreibstil (UZH), PowerFx-Lokalisierung, Token-Storage und Giovanni-Vault-Zugriff erhalten. **Keine Secrets in CLAUDE.md**.

### 5. Env-Vars in `~/.zshrc`

```bash
# Miraglia-BI / M365 Graph App (Tenant: Miraglia-BI)
export M365_CLIENT_ID=0c8e309d-d02e-4244-ae2a-dbb5551cb550
export M365_TENANT_ID=ae7f72de-197d-4ba0-a852-40ee367a5150
```

> Defaults stehen auch in `auth_common.py` — Env-Vars sind nur Override.

### 6. MCP `semantic-vault-mcp` registrieren

Plugin-Konfig auslesen unter `.obsidian/plugins/semantic-vault-mcp/data.json` (`customBindHost`, `httpPort`, `apiKey`), dann:

```bash
claude mcp add --transport http --scope user \
  semantic-vault-mcp \
  http://10.211.55.2:3001/mcp \
  --header "Authorization: Bearer <apiKey>"
```

> 🔒 **Token nur lokal** — nie ins Repo, nie teilen.
> Bind-Host: aktuell `10.211.55.2` (Parallels-Host-IP). Mac-Shells erreichen das nicht direkt — wenn Claudian/Claude Code aus der Parallels-VM laufen, passt's; auf reinem Mac-Pfad → Plugin-Bind auf `127.0.0.1` umstellen.

### 7. Device-Code-Login Miraglia-BI

```bash
cd 40_Resources/scripts
./.venv/bin/python auth_common.py
```

→ Device-Code-URL erscheint → Browser → `microsoft.com/devicelogin` → einloggen als **`raoul@miraglia-bi.com`** → Token landet verschlüsselt im Keychain (`Service: MiragliaBI-M365 / Account: graph-token-cache`).

**Verifikation:**

```bash
./.venv/bin/python -c "
from auth_common import get_token, GRAPH
import requests
tok = get_token(['User.Read'])
print(requests.get(GRAPH+'/me', headers={'Authorization':f'Bearer {tok}'}).status_code)
"
# erwartet: 200
```

### 8. Device-Code-Login MVM Power BI

```bash
./.venv/bin/python pbi_inventory.py --tenant mvm-ag.ch --json /tmp/pbi_mvm_inventory.json
```

→ Device-Code → Browser → einloggen als **`powerplatform@mvm-ag.ch`** (gleicher Kunden-User wie Giovanni) → PBI-Token landet im Keychain (`Service: MiragliaBI-PBI / Account: mvm-ag-ch`).

> MVM-Tenant-ID: `3becd9bb-f602-4c6b-8e86-f1e42db365ea` (resolved via `https://login.microsoftonline.com/mvm-ag.ch/.well-known/openid-configuration`).

### 9. MCP `fabric-mcp` registrieren (NEU, nicht in Giovannis Mail)

Voraussetzung: VS-Code-Extension `fabric.vscode-fabric-mcp-server` ist installiert (liefert die Standalone-Binary `fabmcp` mit, ca. 80 MB).

**Stabilen Symlink anlegen** (damit Extension-Updates nichts brechen):

```bash
mkdir -p ~/.local/bin
ln -sfn "$(ls -d ~/.vscode/extensions/fabric.vscode-fabric-mcp-server-*-darwin-arm64 | sort -V | tail -1)/server/fabmcp" \
  ~/.local/bin/fabmcp
```

**Als stdio-MCP in `~/.claude.json` registrieren:**

```bash
claude mcp add --scope user fabric-mcp ~/.local/bin/fabmcp -- server start
```

**Nach jedem Extension-Update** — Symlink neu setzen (1 Befehl, MCP-Eintrag bleibt):

```bash
ln -sfn "$(ls -d ~/.vscode/extensions/fabric.vscode-fabric-mcp-server-*-darwin-arm64 | sort -V | tail -1)/server/fabmcp" ~/.local/bin/fabmcp
```

> `fabmcp` ist **local-first**: kennt nur die offiziellen Fabric-OpenAPI-Specs/Item-Schemas/Best-Practices — verbindet **nicht** zu deinen Fabric-Workspaces.

## Manuell (Claudian kann nicht klicken)

- **claude.ai Connectors**: Settings → Connectors → **Microsoft Learn** hinzufügen (gratis) + **GitHub** verbinden. Bei GitHub-OAuth „**All repositories**" wählen, sonst sieht Claude nur ausgewählte Repos (Check: <https://github.com/settings/installations> → Claude → Repository access).

## Verifikation — was muss ✓ sein

```bash
# 1) M365 Token + Mail
cd 40_Resources/scripts && ./.venv/bin/python live_search.py "test"

# 2) Power BI MVM
./.venv/bin/python -c "
from auth_common import build_pbi_cache
import msal, requests
cache = build_pbi_cache('mvm-ag.ch')
app = msal.PublicClientApplication('04b07795-8ddb-461a-bbee-02f9e1bf7b46',
  authority='https://login.microsoftonline.com/mvm-ag.ch', token_cache=cache)
accts = app.get_accounts()
res = app.acquire_token_silent(['https://analysis.windows.net/powerbi/api/.default'], account=accts[0])
print(requests.get('https://api.powerbi.com/v1.0/myorg/groups?\$top=1',
  headers={'Authorization':f'Bearer {res[\"access_token\"]}'}).status_code)
"

# 3) MCP-Status
claude mcp list
```

**Erwartung:**
- `microsoft-learn` ✓ Connected
- `fabric-mcp` ✓ Connected
- `semantic-vault-mcp` ✓ Connected (nur wenn Obsidian läuft + Bind-Host erreichbar)
- `claude.ai Google Drive` ✓
- `claude.ai Gmail / Calendar` — irrelevant, ignorieren

## Test-Prompts für Claudian

- *„Lies meine letzten 10 Mails von Stefan Zumbühl und fass zusammen."* — M365-Mail
- *„Erstell einen Entwurf an Dino: …"* — `draft_mail.py` → Entwurf in Outlook-Drafts
- *„Prüf mal, ob die Dataflows bei MVM sauber refreshen."* — Power BI MVM
- *„Welche Fabric-Workload-Typen gibt es?"* — Fabric MCP
- *„Zeig mir das JSON-Schema für ein Lakehouse-Item."* — Fabric MCP
- *„Frag die Microsoft-Doku, wie ich in Power Fx einen Patch mit Lookup mache."* — Microsoft Learn MCP

## Eiserne Regeln (Giovanni)

1. **Tokens NIE kopieren** — jeder macht seinen eigenen Device-Code-Login in seinen eigenen Keychain (auch beim geteilten MVM-User: eigener Token).
2. **Skripte ja, `.venv`/Tokens nein** beim Sync zwischen Vaults.
3. **Token-Storage immer verschlüsselt** im OS-Keystore (Mac Keychain / Windows DPAPI). Nie als `.bin`/`.json` im Vault — Dropbox synct sonst Secrets in die Cloud.
4. **Vor Commits**: `git status` + Diff auf Secrets prüfen.

## Bei Problemen

| Symptom | Ursache | Fix |
|---|---|---|
| `Silent token failed` | Keychain leer oder >90 Tage ungenutzt | irgendein Skript des Toolkits interaktiv neu starten → Device-Code |
| MCP `fabric-mcp ✗` nach VS-Code-Update | Extension-Version-Pfad geändert | Symlink-Befehl aus Schritt 9 erneut ausführen |
| MCP `semantic-vault-mcp ✗` | Obsidian zu / Plugin aus / VM nicht erreichbar | Obsidian + Plugin starten; oder Bind-Host auf `127.0.0.1` ändern |
| Mail-Skripte sehen keine MVM-Mails | nur eigenes Postfach, keine Shared Mailbox | `auth_mvm.py` benutzen (in `50.work/m365-graph/scripts/`, MVM-Tenant, Scope `Mail.Read.Shared`) |

## Verwandt

- [[CLAUDE.md]] — Vault-Regeln (Schreibstil, PowerFx, Token-Storage)
- [[40.meta/claude-projekte-und-custom-ai]] — Claude-Integration generell
- [[40.meta/obsidian-mcp-setup-parallels-windows]] — Parallels/Windows-MCP-Setup
- [[50.work/m365-graph/02-zugangsdaten-secrets]] — CLIENT_ID / TENANT_ID
- [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore]] — Token-Regel im Detail
- `40_Resources/scripts/ANLEITUNG.md` — Toolkit-Doku (Giovanni)
- Mail-Quelle: Giovanni → Raoul, 2026-06-16 17:16 — „Claudian bei Dir aufrüsten — Microsoft Learn, Fabric & das MVM-Toolkit"
