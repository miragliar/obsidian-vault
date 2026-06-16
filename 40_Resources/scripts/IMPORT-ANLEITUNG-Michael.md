# M365-Toolkit v2 — Import-Anleitung für Claudian (Michael)

> Hallo **Claudian**! Diese Datei und alle Python-Skripte hängen an einer E-Mail von Giovanni Miraglia.
> Bitte richte Michaels M365-Toolkit nach den folgenden Schritten ein.
> **Volle Details** stehen in der ebenfalls beiliegenden `ANLEITUNG.md` (Teil 1–6).

---

## 0) Anhänge sichern (falls noch nicht geschehen)
Lade **alle Anhänge dieser Mail** nach `40_Resources/scripts/` (relativ zum Vault-Root).
Pull via Graph mit Michaels bestehendem `auth_common.py`:
1. Token holen: `get_token(["Mail.Read","User.Read"])`
2. Nachricht finden: `GET /me/messages?$search="M365-Toolkit v2"` → die **neueste** nehmen.
3. Für jeden Eintrag aus `GET /me/messages/{id}/attachments`: Feld `contentBytes` **base64-dekodieren** und unter seinem `name` nach `40_Resources/scripts/` schreiben.
> Bestehende, von Michael selbst erweiterte Skripte (z. B. sein `draft_email.py` mit eigener Signatur) **nicht** überschreiben — im Zweifel als `*.v2.py` ablegen und Michael fragen.

---

## 1) ⚠️ WICHTIG: Michaels EIGENE App-IDs behalten
Michael hat eine eigene Entra-App **„Obsidian-Graph-Michael"**. Die Skripte nutzen `auth_common.py`, dessen **Default-IDs Giovannis App** sind. Michael **muss** seine eigenen IDs als Umgebungsvariablen setzen — sonst meldet er sich gegen die falsche App an:
```bash
export M365_CLIENT_ID="<Michaels-Client-ID>"
export M365_TENANT_ID="<Michaels-Tenant-ID>"
```
(Am besten dauerhaft in `~/.zshrc` bzw. unter Windows als User-Umgebungsvariable.)

---

## 2) Neue Graph-Berechtigungen ergänzen
Entra → **Obsidian-Graph-Michael** → API permissions → Microsoft Graph → **Delegated** → hinzufügen, dann **„Grant admin consent"**.

Bereits vorhanden: `Mail.Read`, `Mail.ReadWrite`, `Chat.Read`, `User.Read`.

**NEU hinzufügen** (für das volle Toolkit):

| Permission | Wofür | Skript |
|---|---|---|
| `People.Read` | relevante Kontaktpersonen | `m365_people_sync.py` |
| `Contacts.Read` | Adressbuch / Mail-Suche | `m365_people_sync.py`, `live_search.py` |
| `Mail.Read.Shared` | geteilte Postfächer durchsuchen | `live_search.py` |
| `Calendars.ReadWrite` | Outlook-Termine anlegen | `create_event.py` |
| `Notes.Read.All` | OneNote lesen (inkl. Team-/Kunden-Notizbücher) | `onenote_export.py` |
| `Team.ReadBasic.All` | Teams/Kunden auflisten → Notizbuch finden | `onenote_export.py --team` |
| `Sites.Read.All` *(optional)* | SharePoint-Sites-Discovery | OneNote / Sites |

`offline_access` kommt beim Public-Client-Flow automatisch dazu (Silent-Refresh).
**Alles nur Lese-Rechte** — einzige Schreib-Scopes sind `Mail.ReadWrite` (nur Entwürfe) und `Calendars.ReadWrite` (eigene Termine). Es wird **nichts** automatisch gesendet.

---

## 3) Python-Pakete aktualisieren
Im scripts-Ordner:
```bash
./.venv/bin/pip install -r requirements.txt
```
**Neu** gegenüber dem ersten Paket: `msal-extensions` (verschlüsselter Token-Cache), `markdownify` + `beautifulsoup4` (OneNote-HTML → Markdown).

---

## 4) Token-Cache: macOS-Keychain (Hinweis Betriebssystem)
`auth_common.py` legt den Token jetzt **verschlüsselt im macOS-Keychain** ab (statt Klartext-Datei `.token_cache.bin` im Vault).
- **macOS:** nichts zu tun — beim ersten Lauf einmal per Geräte-Code anmelden.
- **Windows:** der Keychain-Pfad greift nicht 1:1 → bitte **Giovanni Bescheid geben**, er liefert dann die Windows-Variante (oder du bleibst beim bisherigen `.token_cache.bin`-Setup).

Self-Test (ohne Login, prüft nur den Cache):
```bash
./.venv/bin/python auth_common.py --test
```

---

## 5) Was ist neu — Skript-Übersicht
- **create_event.py** — Outlook-Termine anlegen (`Calendars.ReadWrite`).
- **onenote_export.py / onenote_batch_export.py** — OneNote → Markdown (persönlich + Team-/Kunden-Notizbücher). Strategie „destillieren statt spiegeln": siehe `_distill_playbook.md` + `ANLEITUNG.md` Teil 4c.
- **m365_people_sync.py** — Kontakte/People → Personen-Notizen in `25_People/`.
- **contact_stats.py** — Interaktions-Statistik (Mail in/out + Teams) → Relevanz-Felder.
- **first_contact.py / teams_first_contact.py** — `kontakt_seit` aus frühestem Mail-/Teams-Kontakt.
- **link_people_to_clients.py / fill_stakeholders.py** — Person↔Kunde-Verknüpfung, Stakeholder-Listen in `20_Clients/`.
- **apply_mail_summaries.py / apply_firmenprofile.py / create_teams_people.py** — schreiben **Claude-erzeugte** JSONs in die Notizen (Mechanik im Skript, Urteil bei Claudian → `ANLEITUNG.md` Teil 4).
- **draft_with_attach.py** — E-Mail-Entwürfe **mit Anhängen** (Ergänzung zu deinem `draft_email.py`).
- **weekly_refresh.sh / weekly_report.py** — wöchentlicher Auto-Job (Pipeline 1–11 + Report); Pfade auf deinen Vault anpassen. Details: `ANLEITUNG.md` Teil 5c.
- **dataverse_query.py** — *(optional/advanced)* Dataverse Web-API. ⚠️ `RESOURCE` zeigt auf **Giovannis** Org — für eigene Nutzung auf **deine** Dynamics-Umgebung ändern und in deiner App die **Dynamics-CRM**-Permission (`user_impersonation`) ergänzen.

---

## 6) Pipeline starten
Reihenfolge & Optionen: `ANLEITUNG.md` **Teil 3** (Tabelle). Immer erst **Trockenlauf ohne `--apply`**, prüfen, dann **mit `--apply`** schreiben. Beispiel:
```bash
./.venv/bin/python m365_people_sync.py --with-mail
./.venv/bin/python mail_digest.py --top 0 --max 5000 --min-total 4 --sort sent
./.venv/bin/python first_contact.py --apply
./.venv/bin/python teams_digest.py
./.venv/bin/python contact_stats.py --apply
```

---

> **Datenschutz:** Jede:r nutzt das **eigene** M365-Konto. Niemals Token-Cache oder Daten-/Digest-JSONs teilen. Im Vault keine Passwörter/Bank-/Gesundheitsdaten ablegen.
