---
source: user-doc
imported: 2026-06-04
type: setup-howto
tags: [obsidian, mcp, claude-desktop, parallels, windows, networking]
related: [[40.meta/claude-projekte-und-custom-ai]]
---

# Obsidian MCP — Setup & Windows-Zugriff via Parallels

Setup-Notiz für den Obsidian-MCP-Server (Claudian-Plugin / lokaler MCP-Endpoint) — mit optionalem Zugriff aus einer Windows-VM in Parallels (z. B. für Power BI Desktop-Workflows).

## Grundprinzip

- Obsidian läuft **nur auf dem Mac**.
- Der MCP-Server (Plugin im Vault) horcht standardmäßig auf `http://localhost:3001/mcp`.
- Claude Desktop (Mac) verbindet sich direkt via `localhost`.
- Windows in Parallels greift über das **virtuelle Netz** zu — kein zweites Obsidian in Windows starten.

Quick-Verbindung (Mac-Standardfall):

```bash
claude mcp add --transport http obsidian http://localhost:3001/mcp \
  --header "Authorization: Bearer <token>"
```

(siehe auch [[40.meta/claude-projekte-und-custom-ai#Lokaler Server / MCP Integration (Stand Mai/Juni 2026)|Kurz-Notiz im Claude-Workflows-Hub]])

---

## Anhang — Zugriff aus Windows in Parallels (optional)

Nur nötig, wenn parallel eine Windows-VM (Parallels) das Obsidian-MCP nutzen soll, z. B. Claude Desktop unter Windows + Power BI Desktop im selben Workflow.

> [!warning]
> Obsidian läuft weiter **nur auf dem Mac**. Windows greift übers virtuelle Netz zu. **Kein zweites Obsidian** in Windows öffnen — sonst doppelte Vault-Locks und Race Conditions.

### Schritt 1 — Mac-Adresse im Parallels-Netz ermitteln

Im Mac-Terminal:

```bash
ifconfig | grep "10.211.55"
```

→ Ausgabe enthält i. d. R. **`10.211.55.2`** (Parallels Shared-Network-Gateway-Adresse des Macs).

### Schritt 2 — MCP-Plugin auf diese Adresse binden

Im Obsidian-Plugin-Settings-Tab (Claudian / Obsidian-Local-REST-API / o. ä.):

- Bind-Adresse von `127.0.0.1` (oder `0.0.0.0`) auf die fixe Adresse **`10.211.55.2`** stellen.
- Port unverändert (Standard `3001`).
- Obsidian **neu laden** (`Cmd+R` oder Quit + Restart).

> [!tip]
> Die fixe `10.211.55.2`-Bindung **überlebt WLAN-Wechsel**, weil das Parallels-Netz unabhängig vom Wi-Fi-Adapter ist. Damit nutzt **auch der Mac** danach `http://10.211.55.2:3001/mcp` statt `localhost`.

### Schritt 3 — macOS-Firewall freischalten

Beim ersten Verbindungsversuch erscheint:

> „Eingehende Verbindungen für Obsidian erlauben?"
> → **Erlauben**

Falls der Dialog ausbleibt: `Systemeinstellungen → Netzwerk → Firewall → Optionen` → Obsidian explizit erlauben.

### Schritt 4 — Verbindung aus Windows testen

In **Windows PowerShell**:

```powershell
curl.exe http://10.211.55.2:3001/mcp
```

> [!info]
> Bewusst `curl.exe` (nicht nur `curl`) — sonst greift der PowerShell-Alias auf `Invoke-WebRequest` und liefert keinen sauberen HTTP-Status.

**Erwartete Antwort:** `Authentication required` (HTTP 401) → Server ist erreichbar, Token fehlt nur noch. ✅

### Schritt 5 — Claude Desktop unter Windows einrichten

- Dieselbe `obsidian-mcp.mcpb` (Connector-Datei) in das Claude-Desktop-Window ziehen.
- URL: `http://10.211.55.2:3001/mcp`
- Bearer-Token: **derselbe** wie auf dem Mac.
- Node.js **nicht** zusätzlich installieren — Claude Desktop bringt die Runtime mit.

### Variante — `mcp-remote` via Windows-Terminal

Wenn du den Connector statt via Drag&Drop manuell mit `mcp-remote` startest, **zusätzlich** das Flag setzen:

```powershell
mcp-remote http://10.211.55.2:3001/mcp --allow-http
```

> [!warning]
> Ohne `--allow-http` bricht `mcp-remote` mit der Fehlermeldung
> *„Non-HTTPS URLs only for localhost"* ab — weil die Mac-IP aus Windows-Sicht kein Localhost ist.

---

## Troubleshooting

| Symptom | Ursache | Fix |
|---|---|---|
| `curl.exe` liefert nichts / Timeout | Plugin lauscht noch auf `127.0.0.1` | Schritt 2 — Bind auf `10.211.55.2` umstellen, Obsidian neu laden |
| Verbindung bricht nach WLAN-Wechsel | Plugin lauscht auf der dynamischen Wi-Fi-IP | Schritt 2 — fix auf `10.211.55.2` binden |
| `curl` (ohne `.exe`) liefert kein 401 | PowerShell-Alias → `Invoke-WebRequest` | `curl.exe` explizit verwenden |
| `mcp-remote` meldet „Non-HTTPS URLs only for localhost" | Sicherheits-Default | `--allow-http` ergänzen |
| Windows-Claude liest nichts trotz 200 OK | Token falsch oder Vault-Pfad nicht im Plugin freigegeben | Bearer-Token aus Mac-Settings 1:1 kopieren; Vault-Allowlist im Plugin prüfen |
| Mac-Firewall-Dialog erscheint nie | Obsidian wurde schon mal pauschal blockiert | `Systemeinstellungen → Netzwerk → Firewall → Optionen` → Obsidian-Eintrag löschen, dann Obsidian neu starten |
| Port 3001 ist belegt | anderes Tool / alter Obsidian-Prozess | `lsof -i :3001` auf dem Mac, Prozess killen oder im Plugin anderen Port wählen |

## Voraussetzungen / Annahmen

- **Parallels Desktop** mit Standard-Netzwerkmodus „Shared Network" (Default). Bei „Bridged" oder „Host-only" gilt eine andere Adresse — dann `ifconfig` auf dem Mac entsprechend prüfen.
- **macOS-Firewall** ist aktiv oder steht zumindest auf „Eingehende Verbindungen einzeln erlauben".
- **MCP-Plugin** in Obsidian unterstützt eine Bind-Adress-Option (gilt für Claudian und Obsidian Local REST API). Bei älteren Versionen ggf. nur `0.0.0.0` als Bind verfügbar.
- **Bearer-Token** für die MCP-API ist in den Obsidian-Plugin-Einstellungen sichtbar bzw. kopierbar.

## Sicherheitshinweis

- Die Bindung auf `10.211.55.2` öffnet den MCP-Endpoint **nur** im Parallels-internen Netz, nicht im LAN.
- Trotzdem sollte das **Bearer-Token niemals** in geteilten Repos/Notizen landen — gehört in `~/.zshrc` als Env-Var oder in das Plugin-Settings-File (lokal, nicht synchronisiert).
- Wenn der Vault über Dropbox synct, lokale Plugin-Configs prüfen, ob sie versehentlich mitsyncen (Bearer-Token-Leakage über Dropbox-Versionierung).

## Verwandt

- [[40.meta/claude-projekte-und-custom-ai]] — Claude Projects, MCP-Kurzbeschreibung, Übergabe zwischen Sessions
- [[40.meta/Claude-Workflows]] — Meta-Hub
- [[50.work/m365-graph/setup-und-workflow]] — paralleles Setup-Schema (Mail/Teams/Graph)
