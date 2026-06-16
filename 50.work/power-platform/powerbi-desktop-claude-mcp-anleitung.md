---
name: Power BI Desktop ↔ Claude Desktop verbinden (MCP)
slug: powerbi-desktop-claude-mcp-anleitung
type: anleitung
kategorie: power-platform
tags: [powerbi, claude-desktop, mcp, anleitung, kunden-ready]
status: aktiv
created: 2026-06-16
quelle: Giovanni Miraglia (Mail vom 2026-06-01)
verifiziert: Raoul 2026-06-16 (Parallels Windows, arm64)
---

# Power BI Desktop ↔ Claude Desktop verbinden (MCP)

> **Erprobter Weg:** Standalone-`.exe` aus der VS-Code-Extension von Microsoft — **kein Node.js, keine npm-Pakete** nötig. Funktioniert beim Kunden auf Anhieb (so getestet von Giovanni 06/2026, von Raoul 06/2026 verifiziert).

## Voraussetzungen

- **Windows** (bei Mac-Usern: Parallels-VM, Power BI Desktop läuft nicht nativ auf macOS)
- **Power BI Desktop** installiert
- **Claude Desktop** installiert
- **Visual Studio Code** — wird nur als „Lieferant" der Server-`.exe` benutzt, kein Coding nötig

## Schritt 1 — VS Code: Extension installieren

1. VS Code öffnen. Beim Begrüssungsscreen **„Continue without Signing In"** wählen (der GitHub-Login dient nur Copilot — für unseren Zweck nicht nötig).
2. Links auf **Extensions** klicken (oder `Strg+Shift+X`).
3. Suchen nach: **Power BI Modeling MCP** — Publisher: `analysis-services` (Microsoft).
4. **Install** klicken.

> Die Extension installiert im Hintergrund die `powerbi-modeling-mcp.exe` im User-Profil unter `.vscode\extensions\`. Diese .exe brauchen wir gleich — VS Code selbst muss danach nicht mehr offen sein.

## Schritt 2 — Pfad zur Server-.exe finden

**PowerShell** öffnen und ausführen:

```powershell
Get-ChildItem "$env:USERPROFILE\.vscode\extensions" -Recurse -Filter "powerbi-modeling-mcp.exe" | Select-Object -ExpandProperty FullName
```

Bei mehreren Versionen die **höchste Versionsnummer** nehmen. Beispiel:

```
C:\Users\<user>\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.5.8-win32-x64\server\powerbi-modeling-mcp.exe
```

**Bei Raoul (Parallels arm64) sieht es so aus:**

```
C:\Users\raouleliasmiraglia\.vscode\extensions\analysis-services.powerbi-modeling-mcp-0.4.0-win32-arm64\server\powerbi-modeling-mcp.exe
```

Wichtig:
- Der Pfad mit `arm64` ist normal in Parallels — Windows-on-ARM lädt automatisch die passende Variante.
- Die genaue Versionsnummer (`0.4.0`, `0.5.8`, …) ändert sich — nimm immer den Pfad, den `Get-ChildItem` *bei dir* ausgibt.

## Schritt 3 — Claude Desktop konfigurieren

> **Wichtig — Missverständnis vermeiden:** „Edit Config" ist ein **Button in Claude Desktop**, nicht im Windows-Explorer. Die .exe selbst niemals starten; sie öffnet sonst nur einen Hilfe-Screen mit einem **VS-Code-Format-JSON** (`"servers"`) — Claude Desktop braucht aber das **Claude-Format** (`"mcpServers"`).

1. **Claude Desktop** öffnen.
2. **Settings** (Zahnrad oder Menü oben links).
3. Links: **Developer**.
4. Rechts: **Edit Config** klicken.
   → Öffnet automatisch `%APPDATA%\Claude\claude_desktop_config.json` im Default-Editor (Notepad / VS Code).

### Fall A — Datei ist leer oder enthält nur `{}`

Komplette Datei mit folgendem Inhalt überschreiben (Pfad anpassen!):

```json
{
  "mcpServers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "C:\\Users\\<user>\\.vscode\\extensions\\analysis-services.powerbi-modeling-mcp-0.5.8-win32-x64\\server\\powerbi-modeling-mcp.exe",
      "args": ["--start"]
    }
  }
}
```

### Fall B — Datei hat schon Inhalt (z. B. `"preferences": {...}`)

`mcpServers` als **eigenen Top-Level-Eintrag** ergänzen, mit **Komma** vom Vorherigen getrennt:

```json
{
  "preferences": { ... },
  "mcpServers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "C:\\Users\\<user>\\.vscode\\extensions\\analysis-services.powerbi-modeling-mcp-0.5.8-win32-x64\\server\\powerbi-modeling-mcp.exe",
      "args": ["--start"]
    }
  }
}
```

### Die drei häufigsten Fehler

- ❌ Backslashes **einfach** `\` → ✅ **doppelt** `\\` (JSON-Escaping)
- ❌ **Zwei** öffnende `{` ganz oben → ✅ nur **EINE**
- ❌ Komma **nach** dem letzten Eintrag → ✅ kein Trailing-Comma

Dann **Strg+S** zum Speichern.

## Schritt 4 — Claude Desktop neu starten

Claude **komplett über das Tray-Icon** (rechts unten neben der Uhr) beenden — **nicht** nur das Fenster zu klicken (das minimiert nur in den Tray):

- Rechtsklick auf Tray-Icon → **Quit**.
- Danach Claude Desktop neu öffnen.

Erfolgsindikator: Im Chat-Eingabefeld erscheint das **Tool-/🔌-Symbol** mit dem Eintrag `powerbi-modeling-mcp`.

## Schritt 5 — Verbinden & testen

1. **Power BI Desktop** mit der gewünschten `.pbix` öffnen und **offen lassen** (der MCP-Server findet die laufende Instanz lokal).
2. In Claude Desktop:
   > „Connect to '`<Dateiname.pbix>`' in Power BI Desktop"
3. Test-Prompt:
   > „Liste alle Tabellen und Beziehungen meines Modells auf."

→ Claude liefert die Tabellenliste plus Beziehungen. **Wenn das kommt, läuft die Verbindung.**

## Troubleshooting

| Symptom | Ursache / Lösung |
|---|---|
| Tool-Symbol fehlt nach Claude-Neustart | JSON-Syntax prüfen (Komma, doppelte Backslashes, eine einzige öffnende `{`); Claude wirklich über Tray-„Quit" beendet? |
| „Kein Modell gefunden" / „No instance" | Power BI Desktop tatsächlich mit offener .pbix? Erst .pbix öffnen, **dann** in Claude den Connect-Prompt absetzen. |
| .exe-Pfad stimmt nicht | Schritt 2 erneut in PowerShell ausführen — vielleicht hat sich die Versionsnummer der Extension geändert. |
| Verbindung steht, aber keine Daten | .pbix im Power BI Desktop einmal aktualisieren / Modell laden. |
| Logs ansehen | `%APPDATA%\Claude\logs\` (Explorer-Adresszeile reinkopieren) |

## ⚠️ Schreibzugriff — Backup!

Der MCP-Server schreibt **direkt ins offene Power-BI-Modell** (Tabellen, Beziehungen, Measures können von Claude modifiziert werden). Vor jeder Session mit „kreativen" Prompts:

- **`.pbix` vorher sichern** (Copy als `.pbix.bak` oder in Sharepoint-Versionsverlauf).
- Bei Kunden-Modellen: lieber zuerst auf einer Kopie testen.

## Quellen & Links

- Microsoft Repo: <https://github.com/microsoft/powerbi-modeling-mcp>
- VS-Code-Extension: `analysis-services.powerbi-modeling-mcp` (Marketplace)
- Original-Anleitung: Giovanni Miraglia, Mail vom **2026-06-01** „Anleitung: Power BI Desktop mit Claude verbinden (MCP)"

## Verwandt

- [[40.meta/claude-projekte-und-custom-ai|Claude-Integration im Vault — Übersicht]]
- [[50.work/m365-graph/02-zugangsdaten-secrets|M365 Zugangsdaten]] — falls Power-BI-Service-Auth dazukommt (anderer Use-Case)
- [[50.work/power-platform/_README|Power-Platform Pattern-Index]]
