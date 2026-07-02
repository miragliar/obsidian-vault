---
type: anleitung
audience: Raoul · Alessandro · Mike
created: 2026-07-02
tags: [dataverse, accounting, journal, claude, obsidian, setup]
---
# Journal-Einträge & Audit mit Claude in Obsidian — Setup

> [!abstract] Was das ist
> Zwei Python-Skripte für euer Obsidian-Claude-Setup: **`journal_create.py`** legt Journal-Einträge in der Accounting-App (Dataverse) an — ihr diktiert eurem Claude den Eintrag im Chat, er löst Firma/Kontakt/Leistungspaket auf und erstellt ihn. **`journal_audit.py`** überwacht read-only die Einträge des Monats (Regeln wie „Leistungspaket Pflicht" oder „DE-Kunden ohne MwSt") und schreibt bei Verstössen eine ⚠️-Notiz in den Vault-Inbox-Ordner.

## ⚠️ Zuerst: Sicherheits-Grundsätze (bitte einhalten)
1. **Immer zuerst mit Vorsicht testen:** `journal_create.py` schreibt per Default NICHTS (Dry-Run). Erst `--commit` legt an, mit Rückfrage. Wenn vorhanden, zuerst gegen die **Test-Umgebung** (`--org "https://<test>.crm4.dynamics.com"`), erst dann Prod.
2. **Tokens nur im OS-Keystore** (macOS Keychain / Windows DPAPI, via `msal-extensions`) — nie als Klartext-Datei in Vault/Dropbox/Git. Die Skripte machen das automatisch richtig; bitte nichts „vereinfachen".
3. **Read-only wo möglich:** `--suggest` und `journal_audit.py` sind reine GET-Aufrufe.

## 1) Voraussetzungen
- Python 3.10+ · `pip install msal msal-extensions requests`
- **App-Registrierung** im eigenen Entra-Tenant (delegiert): API-Berechtigung **Dynamics CRM `user_impersonation`**, admin-consented. Client-/Tenant-ID sind öffentliche Identifikatoren, keine Secrets.
- Eigene **Dataverse-Org-URL** (`https://<org>.crm4.dynamics.com`).

## 2) Installation im Obsidian-Vault
```bash
# z. B. <Vault>/40_Resources/scripts/
mkdir -p 40_Resources/scripts && cd 40_Resources/scripts
python3 -m venv .venv && ./.venv/bin/pip install msal msal-extensions requests
# Dateien hierhin: journal_create.py · journal_audit.py · auth_common.py
# (auth_common.py = gemeinsame Keystore-Auth; wird von journal_audit.py gebraucht
#  und von journal_create.py automatisch genutzt, falls vorhanden)

export M365_CLIENT_ID="<deine-app-id>"
export M365_TENANT_ID="<dein-tenant>"
export DATAVERSE_URL="https://<deine-org>.crm4.dynamics.com"

./.venv/bin/python journal_create.py --login --suggest "Testkunde"   # einmalig Device-Code-Login
```
Windows: `.venv\Scripts\python` statt `./.venv/bin/python`; der Token-Cache landet dann automatisch in DPAPI statt Keychain.

## 3) Einmaliges Setup: Geschäftsregeln im Skriptkopf definieren
Im Kopf von `journal_create.py` (Konstanten, gut sichtbar kommentiert):
- **`LP_PFLICHT_FIRMEN`** — bei welchen Firmen ist ein **Leistungspaket bei jedem Eintrag zwingend** („immer Ja"). Beispiel bei uns: `MVM Services AG` (alle MVM-Arbeiten laufen immer mit Leistungspaket).
- **`GESPERRTE_FIRMEN`** — alte/abgelöste Gesellschaften, auf die **nicht mehr gebucht** werden darf. Beispiel bei uns: `MVM AG` → seit 2025-11 läuft alles über `MVM Services AG`. Das Skript bricht dort ab und nennt das richtige Ziel.

In `journal_audit.py` analog anpassen: `NO_VAT_FIRMS` (DE-Kunden ohne MwSt) und `LP_REQUIRED_FIRMS`.

Die Datenregel „Firma hat aktive Leistungspakete → Auswahl Pflicht" gilt automatisch zusätzlich; die Listen machen eure Geschäftsregeln **explizit** und schützen vor Datenlücken (z. B. versehentlich deaktivierte Pakete → Abbruch statt still ohne LP zu buchen).

## 4) Nutzung (immer in dieser Reihenfolge)
```bash
# 1. Routing prüfen (read-only): existiert der Kunde? welche Leistungspakete?
./.venv/bin/python journal_create.py --suggest "MVM"

# 2. Dry-Run: löst Firma/Kontakt/LP auf, zeigt den Payload — schreibt NICHTS
./.venv/bin/python journal_create.py \
  --firma "MVM Services AG" --kontakt "Remo Pfister" --leistungspaket "LP-1041" \
  --stunden 0.25 --beschreibung "Telefonat: Testsystem, offene Punkte besprochen."

# 3. Erst wenn alles stimmt: anlegen (fragt nach; --yes für nicht-interaktive Läufe)
#    … gleicher Befehl … --commit
```
- Defaults: `homeoffice/mwstpflichtig/inrechnung=Ja`, Rest=Nein — per Flag übersteuerbar (`--homeoffice nein` bei Vor-Ort-Terminen: schaltet den Satz).
- Beträge/Stundensatz/AutoNumber rechnet die App **serverseitig** — nie mitsenden.
- **Duplikatschutz:** gleiche Firma + Datum + Stunden → Abbruch (bewusst übersteuern mit `--allow-duplicate`).
- Beschreibung: sachlich, kurz (1–3 Sätze); Gratis-Anteile inline „(2h Kostenlos)", nicht als zweiter Eintrag.

## 5) Die wichtigste Regel: NACHFRAGEN STATT RATEN
Bei 0 oder >1 Treffern (Firma/Kontakt/Leistungspaket) **bricht das Skript ab und listet die Kandidaten**. Die Fehlermeldungen instruieren dabei ausdrücklich auch eure Claude-Instanz: **Kandidaten dem Nutzer zeigen, wählen lassen — nie selbst „das plausibelste" nehmen oder Namen still „korrigieren"**. Bitte nicht aufweichen; genau das macht die automatische Erfassung vertrauenswürdig.

## 6) Überwachung: `journal_audit.py`
```bash
./.venv/bin/python journal_audit.py                 # laufender Monat
./.venv/bin/python journal_audit.py --month 2026-06 # bestimmter Monat (vor Rechnungslauf)
./.venv/bin/python journal_audit.py --no-inbox      # nur Konsole, keine Vault-Notiz
```
Read-only. Bei Funden entsteht `00_Inbox/⚠️ Journal-Audit.md` im Vault; ist alles sauber, räumt sich die Notiz selbst weg. Bei uns läuft das wöchentlich automatisch (macOS launchd); unter Windows: Task Scheduler.

## 7) CLAUDE.md-Snippet für euren Vault (anpassen + einfügen)
```markdown
- **Journal-Einträge (Dataverse, Skript `40_Resources/scripts/journal_create.py`):**
  Eintrag braucht nur: Firma · Kontakt (Pflicht) · [Leistungspaket, falls Firma welche hat]
  · Beschreibung (sachlich/kurz) · Stunden. IMMER zuerst Dry-Run zeigen, `--commit` erst
  nach meiner Freigabe. Bei mehrdeutigen Treffern: Kandidaten zeigen und fragen, nie raten.
  Geschäftsregeln (LP_PFLICHT_FIRMEN, GESPERRTE_FIRMEN) stehen im Skriptkopf.
  Überwachung: `journal_audit.py` (read-only, Alarm-Notiz in 00_Inbox).
```

## 8) Eigene Accounting-App? (Portierung)
`journal_create.py` ist für die Castelli-Solution (`cr55b_journal`) gebaut — für Giovanni/Raoul (gleiche Org) und Alessandros eigene Org läuft es direkt. Für eine **andere** App:
- Entity-/Feldnamen anpassen (`ENTITYSET`, Payload-Felder, Lookups via `@odata.bind`).
- **Prinzipien beibehalten:** Dry-Run als Default + Commit-Gate · Resolver mit Abbruch + Kandidatenliste (nachfragen statt raten) · serverseitig berechnete Felder nie senden · Duplikatschutz · Setup-Konstanten für Geschäftsregeln · Tokens nur im OS-Keystore.
- Der Docstring im Skript dokumentiert alle Details (Setup, Routing, Satz-Logik).

Fragen → Giovanni. Viel Spass! 🙂
