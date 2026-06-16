---
type: resource
created: 2026-06-09
tags: [resource, anleitung, onboarding, claude, m365, graph, powerbi, windows, dobi]
audience: technisch-windows
recipients: [Stojanovic Nenad, Manocha Saveen]
---
# 🧰 M365 + Power BI Toolkit — Setup-Anleitung (Nenad & Saveen, Windows)

> Hallo **Claudian** (bzw. Nenad/Saveen)! Diese Datei liegt zusammen mit den Python-Skripten
> in der ZIP an Giovannis E-Mail. Sie führt euch durch die Einrichtung des Toolkits, mit dem
> ihr aus eurem **eigenen** Microsoft-365-Konto (Mail + Teams-Chat) und eurem **Power BI**
> direkt aus Obsidian/Claude lesen könnt. **Volle Details** stehen in der beiliegenden
> `scripts/ANLEITUNG.md`. Die Obsidian-/Claude-Grundinstallation steht in
> `Setup-Anleitung Obsidian + Claude (Windows 11).md`.

> [!important] Grundprinzip
> **Jede:r nutzt das EIGENE M365-Konto und die EIGENE Entra-App im DOBI-Tenant.** Es werden
> ausschließlich **Lese-Rechte** vergeben; die einzigen Schreib-Rechte sind **Entwürfe anlegen**
> und **Mails verschieben** — **es wird NIE automatisch gesendet und NIE gelöscht**. Power BI ist
> **read-only**.

---

## 0) Was ist in der ZIP?
```
Obsidian-Claude-Toolkit/
├─ IMPORT-ANLEITUNG-DOBI (Nenad & Saveen).md   ← diese Datei (zuerst lesen)
├─ Setup-Anleitung Obsidian + Claude (Windows 11).md   ← Obsidian + Claude installieren
└─ scripts/
   ├─ auth_common.py        ← gemeinsame Anmeldung (Cross-Platform-Token-Cache, s. Schritt 4)
   ├─ requirements.txt      ← Python-Pakete
   ├─ ANLEITUNG.md          ← ausführliches Handbuch (Referenz)
   ├─ .gitignore            ← schützt Token/Daten vor versehentlichem Commit
   ├─ live_search.py · fetch_body.py · download_attachments.py · move_mail.py · draft_mail.py   (Mail)
   ├─ teams_read.py · teams_digest.py                                                            (Teams-Chat)
   └─ pbi_inventory.py · pbi_item_history.py · pbi_refresh_probe.py · pbi_schedule_matrix.py     (Power BI)
```

---

## 1) Voraussetzungen
- **Obsidian + Claude** installiert und lauffähig → siehe `Setup-Anleitung Obsidian + Claude (Windows 11).md` (Claude Code, Claudian-Plugin, Vault in Dropbox).
- **Python 3** (`python --version`; sonst „Python 3.12" aus dem Microsoft Store).
- Den Ordner **`scripts/`** aus der ZIP in euren Vault legen: `…\<Vault>\40_Resources\scripts\`.

---

## 2) Eigene Entra-App registrieren (einmalig, im DOBI-Tenant)
[entra.microsoft.com](https://entra.microsoft.com) → **App registrations → New registration** → *Single tenant*, Redirect URI leer.
Dann **Authentication → Allow public client flows → Yes**.
**API permissions → Microsoft Graph → Delegated** — hinzufügen und **„Grant admin consent"**:

| Scope (delegiert) | Wofür | Skript |
|---|---|---|
| `User.Read` | Basis-Login | alle Graph-Skripte |
| `Mail.Read` | Mails lesen/suchen, Anhänge laden | `live_search`, `fetch_body`, `download_attachments` |
| `Mail.Read.Shared` | geteilte Postfächer (von `live_search` mit-angefragt) | `live_search` *(weglassbar — s. Hinweis)* |
| `Mail.ReadWrite` | **Entwürfe** anlegen, Mails **verschieben** (kein Senden/Löschen) | `draft_mail`, `move_mail` |
| `Chat.Read` | **Teams-Chats** (1:1 + Gruppen) lesen | `teams_read`, `teams_digest` |

> [!note] `Mail.Read.Shared`
> `live_search.py` fragt diesen Scope mit an. Wollt ihr ihn nicht konsentieren, entfernt in
> `live_search.py` einfach `"Mail.Read.Shared"` aus der `SCOPES`-Liste.

Danach **Application (client) ID** und **Directory (tenant) ID** notieren.
> **Power BI braucht KEINE eigene App** — es nutzt den Microsoft-eigenen Azure-CLI-Public-Client + Device-Code (s. Schritt 7).

---

## 3) Python-Setup (PowerShell, im `scripts`-Ordner)
```powershell
cd "$HOME\<Pfad-zum-Vault>\40_Resources\scripts"
python -m venv .venv ; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
> Falls `Activate.ps1` blockiert: einmal `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

**Eigene IDs als dauerhafte Umgebungsvariablen** (dann neues Terminal öffnen):
```powershell
setx M365_CLIENT_ID "<deine-client-id>"
setx M365_TENANT_ID "<deine-tenant-id>"
```

---

## 4) Token-Speicher — Windows DPAPI (wichtig, neu portiert)
`auth_common.py` legt den Token-Cache **verschlüsselt im OS-Keystore** ab:
- 🪟 **Windows → DPAPI** (an euer Windows-Benutzerkonto gebundene, verschlüsselte Datei unter `%LOCALAPPDATA%\m365-sync\`).
- 🍎 macOS → Keychain · 🐧 Linux → libsecret.

Es wird **nie** ein Klartext-Token im Vault/Dropbox abgelegt. **Ihr müsst dafür nichts tun** — das passiert automatisch je nach Betriebssystem.

> [!warning] Bitte einmal gegentesten
> Diese Windows-DPAPI-Variante ist **frisch portiert** (Giovannis Original lief nur auf macOS). Sie ist mit
> `msal-extensions` Standard-Bausteinen gebaut, aber bitte beim ersten Lauf kurz verifizieren. Erstanmeldung
> z. B. mit `python live_search.py test` → einmal Device-Code unter `microsoft.com/devicelogin` eingeben,
> als euer DOBI-Konto anmelden. Danach läuft alles still aus dem Cache. Self-Test ohne Login:
> `python auth_common.py --test`.

---

## 5) Mail (Microsoft Graph, euer Postfach)
```powershell
python live_search.py "suchbegriff"                 # Betreff/Body/Absender durchsuchen (Vorschau)
python fetch_body.py "suchbegriff" "betreff-filter" # Volltext einer Mail
python download_attachments.py "suchbegriff" ".\out" "betreff-filter"   # Anhänge laden
python draft_mail.py --to person@firma.ch --subject "Betreff" --body "Hallo<br>…"  # ENTWURF (kein Versand)
python move_mail.py "suchbegriff" "Zielordner" "betreff-filter" "absender-filter"  # verschieben (nicht löschen)
```
> `draft_mail.py` erzeugt nur **Entwürfe** im Drafts-Ordner (erscheinen in Outlook). Den Versand macht ihr selbst.
> (Die mitgelieferte Signatur-/Logo-Mechanik ist Giovannis Branding — ohne eigene `signatur.html` bleibt der Entwurf einfach ohne Signatur.)

---

## 6) Teams-Chat (Microsoft Graph, Scope `Chat.Read`)
```powershell
python teams_read.py "nachname-oder-email" --limit 40        # einen 1:1-Chat live lesen
python teams_digest.py --max-chats 300 --per-chat 80         # Chats scannen → teams_digest.json (lokal)
```

---

## 7) Power BI (read-only, kein App-Registration nötig)
Nutzt den **Azure-CLI-Public-Client** + **Device-Code** gegen euren Tenant; Token-Cache pro Tenant im Keystore.
Anmeldung mit einem Konto, das die betreffenden **Workspaces sehen** darf (tenantweit: Fabric/Power-BI-Admin).
```powershell
# Inventar: Workspaces, Datasets/Dataflows, Refresh-Zeitplan, Datenquellen, Gateway-Bindung
python pbi_inventory.py --tenant <dein-tenant>.onmicrosoft.com --json .\pbi_inventory.json

# Refresh-Historie eines bestimmten Datasets in einem Zeitfenster
python pbi_item_history.py --tenant <dein-tenant>.onmicrosoft.com --name "<dataset-name>" --from 2026-06-03T00:00:00Z --to 2026-06-06T00:00:00Z

# Welche Refreshes überlappten ein Zeitfenster (Datenquelle/Gateway je Refresh)
python pbi_refresh_probe.py --tenant <dein-tenant>.onmicrosoft.com --from 2026-06-05T07:00:00Z --to 2026-06-05T08:30:00Z

# Excel-Heatmap der Refresh-Last pro Stunde (braucht openpyxl)
python pbi_schedule_matrix.py --tenant <dein-tenant>.onmicrosoft.com --inv .\pbi_inventory.json --out .\Refresh_Matrix.xlsx --days 14
```
> Die Beispiel-Platzhalter (`<dein-tenant>`, `<dein-sql-server>`, `<deine-db>`) durch eure Werte ersetzen.
> Alle Power-BI-Skripte sind **rein lesend** — sie ändern nie etwas im Tenant.

---

## 8) 🔒 Sicherheit (eiserne Regel)
- **Tokens/Secrets gehören in den OS-Keystore (DPAPI), nie als Klartext** in Vault/Dropbox/Git. Das erledigt `auth_common.py` automatisch.
- Nur **Lese-Rechte** + **Entwürfe/Verschieben** — **kein Senden, kein Löschen**. Power BI read-only.
- Ihr lest **nur euer eigenes** Postfach/Chats und die euch sichtbaren Power-BI-Workspaces.
- **Nicht** in den Vault legen: Passwörter, API-Keys, Bank-/Gesundheitsdaten — Claude kann den ganzen Vault lesen.
- `.token_cache*`, `*.bin`, `.venv/` und die `*_digest.json` sind per `.gitignore` ausgeschlossen — **Token-Cache und Daten-/Digest-Dateien NIE teilen**.

---

## 9) Schnellstart-Checkliste
1. [ ] Obsidian + Claude installiert (`Setup-Anleitung … (Windows 11).md`).
2. [ ] `scripts\` in den Vault gelegt.
3. [ ] Entra-App registriert + Admin-Consent (Schritt 2), IDs per `setx` gesetzt.
4. [ ] `venv` + `pip install -r requirements.txt`.
5. [ ] `python live_search.py test` → einmal per Device-Code anmelden.
6. [ ] Mail/Teams/Power BI nach Bedarf nutzen (Schritte 5–7).

> Fragen jederzeit an Giovanni. Viel Spaß mit dem zweiten Gehirn 🚀
