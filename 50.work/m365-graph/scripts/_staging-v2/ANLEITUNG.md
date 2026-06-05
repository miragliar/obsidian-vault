---
type: resource
created: 2026-05-30
tags: [resource, anleitung, codebase, m365, graph, obsidian, macos, windows]
audience: technisch-mac-und-windows
---
# 🧠 M365 → Obsidian Wissensbasis — Codebase-Anleitung (macOS & Windows)

> [!abstract] Was diese Codebase macht
> Sie zieht aus deinem **Microsoft-365-Konto** (Kontakte, Mails, Teams-Chats) automatisch eine gepflegte Wissensbasis in **Obsidian**:
> - pro **Person** eine Notiz (`25_People/`) mit Firma, Rolle, Relevanz, `kontakt_seit`, E-Mail-/Teams-Charakterisierung
> - pro **Kunde** eine Notiz (`20_Clients/`) mit Stakeholdern + offiziellem **Firmenprofil** (Zefix/Handelsregister)
> - Verknüpfungen Person ↔ Kunde, Gruppen-Strukturen, Bases-Übersichten
>
> Alle Scripts sind **idempotent** (mehrfach ausführbar) und schreiben Inhalte in **managed Blocks** (`<!-- … -->`), sodass manuelle Edits erhalten bleiben.

> [!tip] 🤖 Für Claude Code: so begleitest du das Setup (an die KI, die diese Datei erhält)
> Du bekommst diese Anleitung, um eine Person **interaktiv durch die Einrichtung zu führen**:
> 1. **Begrüsse** kurz und erkläre in 2 Sätzen, was am Ende entsteht (siehe „Zweck & Nutzen").
> 2. **Frag, welche Bausteine** gewünscht sind — alles ist **modular & skippbar**:
>    - 👤 Personen (Kontakte/People) — *Basis*
>    - 📧 Mail-Charakterisierung · 🕓 Erstkontakt (`kontakt_seit`)
>    - 💬 Teams-Analyse · 📊 Interaktions-Statistik (Relevanz)
>    - 🔗 Person↔Kunde-Verknüpfung · 🔎 Firmen-Research (Web + Zefix/Handelsregister)
>    - ✉️ E-Mail-Entwürfe
> 3. **Nur die nötigen Graph-Berechtigungen** für die gewählten Bausteine nennen (Spalte „Feature" in Teil 1).
> 4. Führe durch **Teil 1 → 2 → 3** Schritt für Schritt; zeige Trockenläufe **vor** `--apply`; prüfe nach jedem Schritt das Ergebnis.
> 5. Die **Claude-gestützten Schritte** (Teil 4 — Zusammenfassungen, Firmen-Research) übernimmst **du selbst**.
> 6. Erkläre nichts, was die Person nicht braucht. Freundlich, konkret, Schritt für Schritt.

---

## Warum diese Codebase? (Zweck & Nutzen)

Ziel: das Wissen aus M365 — **mit wem arbeite ich, an welchen Themen, für welche Firmen** — **automatisch** in einen durchsuchbaren, verlinkten Obsidian-Wissensspeicher („zweites Gehirn" / CRM-light) überführen, statt es von Hand zu pflegen.

Ohne Handarbeit entsteht:
- 👤 **Personen automatisch** — aus **Kontakten, „People" (Relevanz) und Teams-Chats** wird pro Person eine Notiz erstellt: Firma (aus der E-Mail-Domain), Rolle, **„Kontakt seit"** (frühester Mail-/Teams-Kontakt) und eine **Charakterisierung** aus Mail-/Chat-Inhalten.
- 🏢 **Firmen/Kunden automatisch verknüpft** — Personen werden ihren **Kunden** zugeordnet (Firma → Kundenakte), **Gruppen-Strukturen** erkannt und **Stakeholder-Listen** in den Kundenakten gefüllt.
- 🔎 **Firmen-Research integriert** — pro Kunde ein **offizielles Unternehmensprofil**, recherchiert über **Firmenwebseite + Handelsregister/Zefix**: Rechtsform, Gründungsdatum, UID, Sitz/Kanton, Branche, Produkte/Services → als Notiz-Eigenschaften + **Bases-Übersichten** (nach Branche/Kanton).
- ✉️ **E-Mail-Entwürfe** — Claude formuliert aus den Notizen **kontextbezogene Mail-Entwürfe** (mit Logo-Signatur) direkt in dein Outlook; **Versand bleibt bei dir**.

**Nutzen:** schnelleres Eintauchen in Kundenkontexte, saubere Beziehungs- & Firmenübersicht, KI-Unterstützung bei der Korrespondenz — alles **lokal im Vault**, du behältst die Kontrolle (nur Lese-Rechte + Entwürfe, kein automatischer Versand).

---

> [!info] Aufbau-Konvention
> Die Scripts liegen in **`<Vault>/40_Resources/scripts/`** und gehen davon aus, dass der Vault **zwei Ebenen darüber** liegt. Ordner so belassen, dann findet alles automatisch `25_People/` und `20_Clients/`.

---

## Architektur
```
Microsoft 365  ──(Graph, delegiert: du meldest dich selbst an)──►  Python-Scripts  ──►  Obsidian-Vault
  Kontakte · People · Mails · Teams-Chats                                                 25_People/ · 20_Clients/
```
**Kein Client-Secret, kein Server.** Login per Geräte-Code (MSAL), Token wird lokal gecacht (`.token_cache.bin`).

---

# TEIL 1 — App-Registrierung (einmalig, Entra ID)

[entra.microsoft.com](https://entra.microsoft.com) → **App registrations → New registration** → Single tenant, Redirect URI leer.
Dann **API permissions → Microsoft Graph → Delegated** — diese hinzufügen und **„Grant admin consent"**:

| Permission (alle **Delegated**) | Wofür | Feature |
|---|---|---|
| `User.Read` | Basis-Login | alle |
| `People.Read` | relevante Kontaktpersonen | Personen |
| `Contacts.Read` | Adressbuch | Personen |
| `Mail.Read` | Mail-Analyse + `kontakt_seit` | Personen / Charakterisierung |
| `Chat.Read` | **Teams-Chats** (1:1 & Gruppen) lesen | Teams-Analyse |
| `Mail.ReadWrite` | **E-Mail-Entwürfe** anlegen — **kein Versand** | `draft_mail.py` |
| `Notes.Read.All` | **OneNote** lesen (inkl. Team-/Gruppen-Notizbücher) | `onenote_export.py` |
| `Team.ReadBasic.All` | Teams (= Kunden) auflisten → Notizbuch finden | `onenote_export.py --team` |
| `Sites.Read.All` | SharePoint-Sites-Discovery (optional) | OneNote / Sites |

> [!note] Umfang
> Die **vollständige** Wissensbasis (inkl. **Teams-Analyse** und **E-Mail-Entwürfen**) nutzt **alle 6** Berechtigungen. Wer nur Personen/Kunden ohne Teams & Entwürfe will, kann `Chat.Read` und `Mail.ReadWrite` weglassen.
> **Wichtig:** Es sind ausschliesslich **Lese**-Rechte — die einzige Schreib-Berechtigung (`Mail.ReadWrite`) wird nur für **Entwürfe** verwendet; nichts wird automatisch gesendet oder gelöscht.

**Authentication → Allow public client flows → Yes.** Dann **Application (client) ID** + **Directory (tenant) ID** notieren.

---

# TEIL 2 — Setup (Python)

> [!tip] Terminal öffnen — 🍎 macOS: cmd+Leertaste → „Terminal". 🪟 Windows: Start → „Terminal" (PowerShell).

### 2.1 Python prüfen
🍎 **macOS:** `python3 --version`  (sonst [python.org](https://www.python.org/downloads/) oder `brew install python`)
🪟 **Windows:** `python --version`  (sonst „Python 3.12" aus dem Microsoft Store)

### 2.2 venv + Pakete (im scripts-Ordner)
🍎 **macOS:**
```bash
cd "<Vault>/40_Resources/scripts"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
🪟 **Windows:**
```powershell
cd "<Vault>\40_Resources\scripts"
python -m venv .venv ; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
> Windows: falls `Activate.ps1` blockiert → einmal `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 2.3 IDs als Umgebungsvariablen setzen
🍎 **macOS** (für die aktuelle Terminal-Sitzung):
```bash
export M365_CLIENT_ID="deine-client-id"
export M365_TENANT_ID="deine-tenant-id"
```
🪟 **Windows (PowerShell):**
```powershell
$env:M365_CLIENT_ID="deine-client-id"
$env:M365_TENANT_ID="deine-tenant-id"
```
> Optional: `VAULT_ROOT` setzen, falls der Vault nicht zwei Ebenen über dem scripts-Ordner liegt.

Beim **ersten** Lauf erscheint ein **Geräte-Code** → unter `microsoft.com/devicelogin` eingeben, als dein M365-Konto anmelden. Danach läuft alles still aus dem Token-Cache.

---

# TEIL 3 — Die Pipeline (Reihenfolge)

> Befehle: 🍎 macOS = `python3 …`, 🪟 Windows = `python …`. Erst **ohne** `--apply` (Trockenlauf), dann **mit** `--apply` schreiben. Reihenfolge empfohlen, aber jeder Schritt ist eigenständig.

| # | Script | Zweck | Wichtige Optionen | Schreibt nach |
|---|---|---|---|---|
| 1 | `m365_people_sync.py` | Kontakte + People → Personen-Notizen | `--with-mail`, `--force` | `25_People/` |
| 2 | `mail_digest.py` | Mail-Scan: häufigste Kontakte + Vorschauen | `--top 0 --max 5000 --min-total 4 --sort sent` | `mail_digest.json` |
| 3 | `apply_mail_summaries.py` | schreibt **📧 E-Mail-Kontext** in Notizen | `--apply` | `25_People/` |
| 4 | `first_contact.py` | frühestes Mail-Datum → `kontakt_seit` | `--apply` | `25_People/` |
| 5 | `teams_digest.py` | Teams-Scan: Chat-Partner, Themen, Domain | `--max-chats`, `--per-chat` | `teams_digest.json` |
| 6 | `create_teams_people.py` | neue Teams-Kontakte als Notizen anlegen | `--apply` | `25_People/` |
| 7 | `teams_first_contact.py` | frühestes Teams-Datum → `kontakt_seit` (frühestes gewinnt) | `--apply` | `25_People/` |
| 8 | `link_people_to_clients.py` | Firma → Kunde matchen → `client:` setzen | `--apply`, `--include-low` | `25_People/` |
| 9 | `fill_stakeholders.py` | Stakeholder-Listen in Kundenakten füllen | `--apply` | `20_Clients/` |
| 10 | `apply_firmenprofile.py` | Firmenprofil (Zefix-Daten) in Kundenakten | `--apply` | `20_Clients/` |
| 11 | `contact_stats.py` | Interaktions-Zähler (Mail in/out + Teams) → Relevanz-Felder | `--apply`, `--no-teams`, `--no-mail` | `25_People/` |

> **Schritt 11 – Relevanz/Interaktionen:** zählt pro Person `mail_in`, `mail_out`, `teams_total` (**lebenslang**) sowie `interaktionen` (Summe lebenslang) und `interaktionen_12m` (**rollierend 12 Monate**, zeigt die *aktiven* Kontakte). Voller Postfach- + Teams-Scan → als periodischer Job sinnvoll (`stats_stand` zeigt die Frische).

### Beispiel-Durchlauf (macOS)
```bash
python3 m365_people_sync.py --with-mail
python3 mail_digest.py --top 0 --max 5000 --min-total 4 --sort sent
python3 first_contact.py --apply
python3 teams_digest.py
python3 teams_first_contact.py --apply
python3 link_people_to_clients.py --apply
python3 fill_stakeholders.py --apply
```
(Windows: identisch, nur `python` statt `python3`.)

---

# TEIL 4 — Claude-gestützte Schritte (Urteil nötig)

Drei Schritte brauchen **inhaltliches Urteil** — diese Daten erzeugt am besten **Claudian** (Claude direkt in Obsidian) und legt sie als JSON in den scripts-Ordner; danach schreibt das passende `apply_*`-Script sie in die Notizen.

| Daten-Datei | Wird gelesen von | So erzeugen (Claudian bitten) |
|---|---|---|
| `mail_summaries*.json` | `apply_mail_summaries.py` | „Lies `mail_digest.json` und schreibe pro Person eine kompakte Charakterisierung (Rolle, Beziehung, Themen) als JSON `{dateiname.md: text}`." |
| `teams_people.json` | `create_teams_people.py` | „Aus `teams_digest.json` die neuen Chat-Partner (≥15 Interaktionen, mit E-Mail) als JSON mit Firma (aus Domain), Client, Rolle, Charakterisierung." |
| `firmenprofile.json` | `apply_firmenprofile.py` | „Recherchiere je Kunde über Webseite (E-Mail-Domain) + **Zefix/Handelsregister** Rechtsform, Gründung, UID, Hauptsitz, Branche, Kurzbeschrieb, Produkte, Merkmale — als JSON." |

> So bleibt die **Mechanik** (Graph-Zugriff, Schreiben in Notizen) in den Scripts, das **Urteil** (Zusammenfassen, Recherche) bei Claude.

---

# TEIL 4b — E-Mail-Entwürfe (`draft_mail.py`)

Legt einen **Entwurf** im Drafts-Ordner an (Scope `Mail.ReadWrite`) → erscheint in Outlook App/Web/Mobile. **Es wird nichts gesendet.**
```bash
# einfacher Entwurf
python3 draft_mail.py --to person@firma.ch --subject "Betreff" --body "Hallo<br>…"
# per JSON (für reiche Inhalte / Reply im Thread)
python3 draft_mail.py --file draft.json    # keys: to, cc, subject, body, body_type, reply_to_message_id
```
Typischer Ablauf: **Claudian** formuliert den Text aus einer Personen-/Kundennotiz → schreibt `draft.json` → `draft_mail.py --file draft.json` → du prüfst & sendest in Outlook.
> `draft.json` enthält Mailtext → ist per `.gitignore` ausgeschlossen.

**Signatur:** Graph-Entwürfe übernehmen die Outlook-Signatur NICHT automatisch. Daher hängt `draft_mail.py` die Datei **`signatur.html`** (editierbar) automatisch an jeden Entwurf an. Abschalten mit `--no-signature` bzw. `"signature": false`.

---

# TEIL 4c — OneNote → Obsidian  (`onenote_export.py`)

Liest OneNote via Graph (Scope **Notes.Read.All**; für Kundenzuordnung **Team.ReadBasic.All**), wandelt Seiten-HTML → Markdown, lädt Bilder/Anhänge (Originalnamen) und schreibt pro Seite eine `.md` mit Frontmatter. **Nur lesend** auf der M365-Seite.

Drei Quellen: persönlich (`/me`), **Team/Kunde** (`--team "Name"` / `--group-id`), SharePoint-Site (`--site-id`).
```bash
./.venv/bin/python onenote_export.py --list-teams                # Kunden (Teams) auflisten
./.venv/bin/python onenote_export.py --team "Koster" --dry-run   # Struktur-Vorschau (schreibt nichts)
./.venv/bin/python onenote_export.py --team "Koster"             # exportieren
./.venv/bin/python onenote_export.py --team "X" --all-notebooks --clean --out 40_Resources/OneNote-Import/X
./.venv/bin/python onenote_export.py --notebook "Power-BI"       # persönliches Notizbuch
```
Batch über alle inhaltsreichen Kunden-Teams: **`onenote_batch_export.py`** (sequentiell → kein Token-Race).

### Strategie: destillieren statt spiegeln
Kunden-Notizbücher sind meist **Journale** (chronologisch) + wenige **Wissens-Seiten**. Die Journale **doppeln Dataverse** → nicht 1:1 importieren. Pro Kunde:
1. Export als **Ingest-Schicht** (temporär in `40_Resources/OneNote-Import/`)
2. Journal verwerfen, **durable Wissen** extrahieren (Systeme, Apps, Prozesse, Personen, Entscheidungen, offene Punkte)
3. Bestehenden `20_Clients/<Kunde>.md` **anreichern** (managed Blöcke `<!-- … -->` nicht anfassen) — oder neu aus `_Templates/Client.md`
4. Roh-Export löschen · **Secrets** (Passwörter, GUIDs) bleiben in OneNote, nicht im Vault

**Wissens-Notizbücher** (z. B. `MSSQL-Knowledge`, `Power-BI`) sind bereits kuratiert → **voller Import** nach `30_Domains` sinnvoll.

---

# TEIL 5 — Was in den Notizen entsteht

**Personen** (`25_People/<Name>.md`): Frontmatter `email, company, client, kontakt_seit, relevance, mail_in, mail_out, teams_total, interaktionen, interaktionen_12m, stats_stand, os, skills, tags`; Sektionen `## Contact`, `## Profil`, `## 📧 E-Mail-Kontext`, `## 💬 Teams-Kontext` (managed Blocks).

**Kunden** (`20_Clients/<Name>.md`): Frontmatter `branche, sektor, kanton, hauptsitz, rechtsform, gegruendet, uid, website`; Sektionen `## Unternehmensprofil` (managed), `## Stakeholder` (managed `<!-- people-sync -->`), `## Systems/Active Topics/Log`.

**Bases:** `20_Clients/Clients.base` (Ansichten: Nach Sektor / Nach Kanton / Firmen-Steckbrief …), `25_People/People.base`.

---

# 🔒 Sicherheit & .gitignore
Diese Dateien bleiben **lokal** und gehören in die `.gitignore` (enthalten Token bzw. Mail-/Chat-Inhalte):
```
40_Resources/scripts/.token_cache.bin
40_Resources/scripts/.venv/
40_Resources/scripts/mail_digest.json
40_Resources/scripts/teams_digest.json
40_Resources/scripts/mail_summaries*.json
40_Resources/scripts/teams_summaries*.json
40_Resources/scripts/batch_export.log
40_Resources/OneNote-Import/
**/__pycache__/
```
- Nur **`…​.Read`**-Rechte → die Scripts können nichts senden/löschen.
- Du liest **nur dein eigenes** Postfach/Chats.
- **NICHT** in den Vault legen: Passwörter, Bank-/Gesundheitsdaten.

---

# 🆘 Troubleshooting
| Problem | Lösung |
|---|---|
| `command not found: python` (Mac) | `python3` verwenden |
| `CLIENT_ID/TENANT_ID nicht gesetzt` | Umgebungsvariablen aus Teil 2.3 setzen |
| `AADSTS65001 / consent_required` | „Grant admin consent" in Teil 1 fehlt |
| `403` bei Teams | `Chat.Read` fehlt (Admin consent) — einzelne 403-Chats werden sonst übersprungen |
| `Activate.ps1` blockiert (Win) | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Geräte-Code abgelaufen | Script neu starten (Code ~15 Min gültig) |
| Notiz wurde nicht gefunden | Personen-Notiz fehlt das `email:`-Feld, oder Datei umbenannt |
| Umlaute im Dateinamen wirken „doppelt" | macOS/Windows-Unicode (NFD/NFC) — kosmetisch, Links/Matching funktionieren (Scripts normalisieren) |

---

# TEIL 5c — Automatischer Wochen-Job (launchd, macOS)

Hält alles automatisch aktuell — **deterministischer Teil vollautomatisch**, KI-Teil per Report.

- **`weekly_refresh.sh`** läuft die ganze deterministische Pipeline (Schritte 1–11): neue Kontakte, `kontakt_seit`, Verknüpfung, Stakeholder, Firmenprofile anwenden, Stats — und erzeugt **`weekly_report.py`** → **`00_Inbox/M365 Wochen-Report.md`**.
- **`com.miragliabi.m365-weekly.plist`** = launchd-Job (montags 07:30). Installieren:
  ```bash
  cp com.miragliabi.m365-weekly.plist ~/Library/LaunchAgents/
  launchctl load -w ~/Library/LaunchAgents/com.miragliabi.m365-weekly.plist
  launchctl start com.miragliabi.m365-weekly   # sofort testen
  ```
- **Der KI-Teil** (neue Firmen via Web/Zefix recherchieren, neue Personen charakterisieren, Privat/Dienstleister markieren) bleibt bei dir: einfach **Claudian** öffnen und den **Auftrag aus dem Wochen-Report** ausführen lassen.
- **`m365_people_sync.py` ist e-mail-bewusst**: bereits erfasste Adressen (auch unter Klarnamen / `alt_emails`) werden übersprungen → **manuell zusammengeführte/umbenannte Notizen bleiben erhalten**.

> [!note] Token-Frische: Der Job nutzt den gecachten Refresh-Token (kein Login nötig). Solange er **mind. alle ~90 Tage** läuft, bleibt er gültig. Auf einem anderen Rechner / anderer Person: `Variante B` in Teil 6.

> [!tip] Manuell statt Job
> Alles ist idempotent — du kannst `weekly_refresh.sh` auch jederzeit von Hand starten, oder einzelne Scripts erneut laufen lassen. Neue Kontakte/Firmen kommen dazu, manuelle Edits bleiben erhalten.

---

# TEIL 6 — Weitergabe an andere (Rollout)

Die Codebase ist self-contained und kann weitergegeben werden — **jede Person nutzt ihr eigenes M365-Konto**.

**Variante A — Selbst registrieren** (Standard, z. B. **Alessandro, Raoul, Michael**):
1. Empfänger:in registriert in **ihrem** Entra-Tenant eine eigene App (Teil 1) + Admin-Consent.
2. Scripts-Ordner kopieren, eigene **Client-/Tenant-ID** als Umgebungsvariablen setzen (Teil 2.3), `pip install -r requirements.txt`.
3. Pipeline durchlaufen (Teil 3). Fertig.

**Variante B — Vorkonfiguriert ausliefern** (für weniger technische Nutzer / Kunden, z. B. **Oliver Bader**):
1. Der Admin registriert die App **im Tenant der Person** (mit deren Zustimmung) + Admin-Consent.
2. **Client-ID + Tenant-ID** werden direkt in die Script-Defaults / eine `config` eingetragen, sodass die Person **nichts** mehr konfigurieren muss — nur ausführen und sich beim ersten Lauf per Geräte-Code anmelden.
3. Ordner als ZIP / via Dropbox übergeben.

> [!warning] Was NICHT mitschicken
> Niemals den **`.token_cache.bin`** oder persönliche **Daten-/Digest-Dateien** weitergeben (siehe .gitignore). Übergeben werden nur **Code + Anleitung + `signatur.html`/Logo**; die Empfänger:in erzeugt ihre **eigenen** Daten und meldet sich mit ihrem **eigenen** Konto an.

---

> [!info] Verwandte Anleitungen
> - Einsteiger-Setup Obsidian + Claude: [[Setup-Anleitung Obsidian + Claude (Windows 11)]]
> - Schlanke Team-Version (nur Kontakte-Sync): [[40_Resources/Team-Setup M365 Kontakte-Sync/ANLEITUNG]]
> - Native Outlook-Signatur einrichten: [[40_Resources/Outlook-Signatur einrichten (Mac & Windows)]]
