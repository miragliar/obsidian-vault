---
name: m365-email
description: Read/search the user's Microsoft 365 mailbox and create Outlook DRAFT emails via the Microsoft Graph API (Azure/Entra app, delegated, MSAL token cache). The user DOES have email access — NEVER say you cannot read or write email. Use whenever the user wants to find/read an email, look up email history or contact details from mail, coordinate based on an email, or draft/prepare an email. Reading is via Python scripts in 40_Resources/scripts (live_search.py, fetch_body.py); drafting via draft_mail.py (creates a draft only — never sends).
---

# M365 E-Mail via Microsoft Graph (Azure App)

The user has a registered **Azure/Entra app** with **delegated** Microsoft Graph access to **their own** mailbox. Auth is via **MSAL**; the token cache lives **encrypted in the macOS Keychain** (via `msal_extensions`, see `auth_common.py`) — **no secret, no server, silent refresh, never a plaintext file**. You operate it through ready-made Python scripts.

> **CRITICAL:** You have working email access. Do **not** claim "I have no email/Gmail/Outlook access" or that the mail "isn't in Dropbox/Drive." Use the scripts below.

## Where
- Scripts: `40_Resources/scripts/` — always run with the venv: `./.venv/bin/python`
- App: CLIENT_ID `0c8e309d-d02e-4244-ae2a-dbb5551cb550` · TENANT_ID `ae7f72de-197d-4ba0-a852-40ee367a5150`
- Scopes: `Mail.Read`, `Mail.Read.Shared`, `Contacts.Read`, `User.Read` (read) · `Mail.ReadWrite` (drafts only — **no `Mail.Send`**)

## 1) Search / read mail headers + preview
Searches `/me/messages` across **all folders incl. Sent** via Graph `$search`.
```bash
cd "/Users/miragliag/Dropbox/Miraglia-BI/0_Internal/Obsidian gimi/Miragliag/40_Resources/scripts"
./.venv/bin/python live_search.py "search term" "another term"
```
Prints per hit: date · from · to · subject · body preview.

## 2) Read full body of a message
```bash
./.venv/bin/python fetch_body.py "search query" "optional subject filter substring"
```
Prints date, from, to, hasAttachments, and the full body (HTML stripped). Top 5 matches; the 2nd arg filters by subject substring.

## 3) Create an Outlook DRAFT (never sends)
Creates a draft in the Drafts folder (Mail.ReadWrite). Auto-attaches `signatur.html`/logo. **Sending stays with the user.**
draft_mail.py reads the app IDs from env vars — set them inline:
```bash
M365_CLIENT_ID=0c8e309d-d02e-4244-ae2a-dbb5551cb550 \
M365_TENANT_ID=ae7f72de-197d-4ba0-a852-40ee367a5150 \
./.venv/bin/python draft_mail.py --to "a@b.ch,c@d.ch" --subject "Betreff" --body "Hallo<br><br>…"
```
Options: `--cc`, `--text` (plain text), `--body-file file.html`, `--reply-to <messageId>` (reply draft in thread), `--no-signature`.
Rich/threaded drafts via JSON: `./.venv/bin/python draft_mail.py --file draft.json` — keys: `to, cc, subject, body, body_type, reply_to_message_id, signature`.

## ✍️ Schreibstil — drafts MUST sound like Giovanni (Pflicht)
Every draft you write **in Giovanni's name** must match **his** voice, not the default assistant tone. Full profile + per-recipient details: **`40_Resources/Schreibstil — Giovanni (E-Mail).md`** — read it before drafting for a regular contact. Hard rules:
- **Swiss spelling: always „ss", never „ß"** (Grüsse, müssen, heisst). Numbers with apostrophe (`27'700`).
- **Do not repeat name/signature in the body** — `draft_mail.py` appends the HTML signature automatically. Body ends with only the human greeting + first name.
- **Open with thanks/praise/reference**, then the point. Explain the **why**, then numbered steps. Concrete numbers, clear recommendation, **action-oriented close** („melde dich, wenn's klemmt"). „wir"-framing for the team.
- **Emojis functional & sparse** (✅ ⚠️ 👍 🙏), never in formal client mails. Keep short mails short (often no greeting for quick internal replies).
- **Match register + language to the recipient.** Greetings/closings:
  - Internal/peer (Du): `Hoi <Vorname>` / `Hoi zäme` → `Gruss` · `Gruss Giovi` · `Liebe Grüsse`
  - Warm: `Hallo/Lieber <Vorname>` → `Liebe Grüsse` + `Giovanni`
  - Client formal (Sie): `Guten Tag Herr/Frau <Nachname>` → `Freundliche Grüsse` + `Giovanni Miraglia`
  - Italian (Ticino/family): `Ciao <Nome>` / `Buongiorno a tutti` → `Abbraccio` · `Abbraccio Giovi`
- **Regular customers are mostly on Du** (`Hoi <Vorname>`), warm & first-name. Use `Sie` / `Guten Tag Herr/Frau` only for **new/unknown/escalation/official** mails. Language follows the **account**: Italian for Ticino (e.g. Ennio Ferrari/Compul → „Ciao …", „Saluti", „Buona giornata!"), English for international (e.g. Green → „Dear …", „Best regards"). In a running thread, **mirror the tone already there**. Standing **Sie-by-house-style** accounts: **SHARKGROUP**, **Hunnenberg** (DE). Invoice cover mails are semi-formal even to Du-customers (`Guten Tag <Vorname> … Vielen Dank für die tolle Zusammenarbeit. Freundliche Grüsse`). Per-customer roster in the style note.
- **Key contacts:** Ale (`alessandro@castelli-solutions.ch`) = Hoi Ale, deep-tech peer · Mike (`michael@kipfer-dp.com`) = Hoi Mike, encouraging coach · Raoul (`raoul@miraglia-bi.com`) = Hoi Raoul, familiar/appreciative · Elvira (`elvira@miraglia-bi.com`) = family/"amore", ultra-short, `Abbraccio`.

## Conventions
- Default workflow: **you draft, the user reviews & sends** in Outlook. Never imply a mail was sent.
- After reading mail for a task, prefer capturing durable facts (contacts, decisions, dates) into the relevant vault note.
- If the silent token ever fails (`Silent token failed`), tell the user to run any script once interactively to refresh the device-code login (cache valid as long as used ≥ every ~90 days).
- Privacy: read-only on the user's **own** mailbox; never put passwords/bank/health data into the vault. **Tokens/secrets live in the macOS Keychain (Windows: DPAPI) — never as a plaintext file in the vault/Dropbox/Git** (see CLAUDE.md → „🔒 Sicherheit").

## Related
- Full pipeline / setup: `40_Resources/scripts/ANLEITUNG.md`
- Human-readable note: `40_Resources/Claude-Skills/M365 E-Mail via Graph (Azure App).md`
