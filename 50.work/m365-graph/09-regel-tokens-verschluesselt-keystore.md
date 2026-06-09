---
source: claude-import
imported: 2026-06-09
from: giovanni@miraglia-bi.com
to: raoul@miraglia-bi.com
cc: ale@... (windows-user)
date: 2026-06-09
type: regel-security
tags: [miraglia, security, tokens, keychain, dpapi, msal, m365, power-bi]
status: in-kraft-ab-2026-06-09
sensitivity: internal
---

# 🔐 Regel: Tokens immer verschlüsselt im OS-Keystore (Keychain/DPAPI)

> **Ab sofort gültige Regel** (Giovanni Miraglia, 2026-06-09):
> Tokens / Secrets **immer verschlüsselt** im OS-Keystore (macOS Keychain bzw.
> Windows DPAPI), **nie als Klartext** in einer `.bin`-/`.json`-Datei im Vault.

## Warum

Der Vault (`Miraglia-BI/0_Internal/Obsidian Raoul/`) ist über **Dropbox synchronisiert** und teilweise über **Git nach GitHub** verbunden. Eine Klartext-Token-Datei landet damit **effektiv in der Cloud** — Refresh-Token = persistente Identität gegen MS Graph / Power BI / Dataverse. Das ist genau das, was wir **nicht** wollen.

## Die Regel im Detail

- **Kein** `msal.SerializableTokenCache` mehr, das eine `.bin`-Datei schreibt.
- **Stattdessen verschlüsselt** im OS-Keystore:
  - **macOS** → `KeychainPersistence` + `PersistedTokenCache` (`msal_extensions`)
  - **Windows** → DPAPI via `build_encrypted_persistence()` (`msal_extensions` wählt automatisch).
- **Vorlagen** stecken in `auth_common.py` (Mac/Linux):
  - `build_cache()` — M365-Tenant (Miraglia-BI)
  - `build_pbi_cache(tenant)` — Power-BI / Kunden-Tenants (pro Tenant ein Keychain-Item)
  - `build_pbi_persistence(tenant)` / `migrate_pbi_bin(tenant, script_dir)` — Hilfen für Migration
- **`.gitignore`** muss Token-Pfade abdecken: `*.bin`, `.token_cache*`, `.pbi_token_cache_*` — Defense-in-Depth, falls doch mal eine Klartext-Datei entsteht.
- **Vor jedem Commit** `git status` + Diff prüfen, ob ein Secret im Diff liegt.
- **Falls doch mal ein Token unverschlüsselt auftaucht:**
  1. in den Keystore migrieren (Helper-Funktion nutzen)
  2. Klartext-Datei löschen (`rm -P` oder Keychain-UI)
  3. aus der Git-Historie purgen (`git filter-repo` o. ä.)

## Plattform-Spezifika

### macOS
```python
from msal_extensions import KeychainPersistence, PersistedTokenCache
persistence = KeychainPersistence(signal_file, "MiragliaBI-M365", "graph-token-cache")
cache = PersistedTokenCache(persistence)
```

### Windows (für Ale!)
```python
from msal_extensions import build_encrypted_persistence, PersistedTokenCache
persistence = build_encrypted_persistence(location=...)  # nutzt automatisch DPAPI
cache = PersistedTokenCache(persistence)
```

`msal_extensions` erkennt die Plattform automatisch — auf Windows greift DPAPI, auf Mac Keychain, auf Linux libsecret. Es muss nur die richtige Helper-Funktion verwendet werden.

## Status der Umsetzung (Raoul / 2026-06-09)

### Phase 1 — `auth_common.py` mit Keychain ✅
- M365-Token-Cache: `MiragliaBI-M365 / graph-token-cache` ✅
- Self-Test: `./.venv/bin/python auth_common.py --test` → grünes Häkchen ✅
- Legacy `.token_cache.bin.legacy` (9'880 Bytes Klartext) **sicher gelöscht** via `rm -P` (Overwrite) ✅

### Phase 2 — `build_pbi_cache(tenant)` für Power BI ✅
- Aus dem Mail-Anhang in `auth_common.py` übernommen (1:1 wie Giovannis Referenz) ✅
- `_PBI_SERVICE = "MiragliaBI-PowerBI"`, Account = Tenant-Slug
- `migrate_pbi_bin(tenant, script_dir)` für einmalige Migration

### Phase 3 — 12 Skripte refaktoriert ✅

Alle Skripte, die zuvor `msal.SerializableTokenCache()` + `.token_cache.bin` benutzten, sind jetzt auf `auth_common.get_token(SCOPES)` umgestellt:

| Skript | Vorher | Jetzt |
|---|---|---|
| `list_drafts.py` | `.token_cache.bin` | Keychain ✅ |
| `preview_draft.py` | `.token_cache.bin` | Keychain ✅ |
| `extract_logo.py` | `.token_cache.bin` | Keychain ✅ |
| `inspect_signature.py` | `.token_cache.bin` | Keychain ✅ |
| `fetch_vloriana_mail.py` | `.token_cache.bin` | Keychain ✅ |
| `mvm_extras.py` | `.token_cache.bin` | Keychain ✅ |
| `_fetch_v2_toolkit.py` | `.token_cache.bin` | Keychain ✅ |
| `draft_giovanni_darkmode_signatur.py` | `.token_cache.bin` | Keychain ✅ |
| `draft_test_giovanni_signature.py` | `.token_cache.bin` | Keychain ✅ |
| `draft_reply_vloriana_ss.py` | `.token_cache.bin` | Keychain ✅ |
| `draft_mail_ki_ausmass_summary.py` | `.token_cache.bin` | Keychain ✅ |
| `draft_replies_mvm.py` | `.token_cache.bin` | Keychain ✅ |

**Bereits konform vorher:**
- `auth_common.py` (M365) — Mac Keychain ✅
- `auth_mvm.py` (MVM-AG Tenant) — Mac Keychain (`MVM-Offerte-Scan / graph-token-cache`) ✅
- Alle Skripte, die `from auth_common import …` nutzen: `live_search.py`, `fetch_body.py`, `mail_digest.py`, `teams_digest.py`, `m365_people_sync.py`, `apply_*`, `first_contact.py`, `contact_stats.py`, `fill_stakeholders.py`, `link_people_to_clients.py`, `create_event.py`, `onenote_export.py`, `onenote_batch_export.py`, `dataverse_query.py`, `draft_mail.py`, `draft_with_attach.py`, `draft_mail_offerte_zugang_mvm.py`, `analyze_ppweekly.py`, `fetch_ppweekly.py`, `weekly_report.py`, … ✅

### Phase 4 — `.gitignore` erweitert ✅
`50.work/m365-graph/scripts/.gitignore` deckt jetzt:
```
*.bin
.token_cache*
.pbi_token_cache_*
```

Verifiziert via `git check-ignore -v`: alle drei Pattern greifen.

### Phase 5 — Git-Historie clean ✅
`git log --all --diff-filter=A` → keine `.bin`/`.token_cache`-Datei wurde jemals committet. Kein History-Purge nötig.

### Phase 6 — Doku aktualisiert ✅
- `_README.md`: Keychain-Hinweis statt `.token_cache.bin`-Hinweis
- `setup-und-workflow.md`: Sicherheits-Tabelle + Troubleshooting auf Keychain umgestellt
- `07-anleitung-v2-toolkit.md`: Architektur-Diagramm + .gitignore-Block + Lieferung-Hinweis aktualisiert
- `02-zugangsdaten-secrets.md`: Verweis auf diese Regel

## Verifikation / Test-Befehle

```bash
cd 50.work/m365-graph/scripts

# 1) M365-Auth via Keychain
./.venv/bin/python auth_common.py --test
# → ✅ Keychain-Auth funktioniert — Access-Token erhalten (… Zeichen).

# 2) Stichprobe: gepatchtes Skript
./.venv/bin/python list_drafts.py
# → Drafts-Folder: id=…  total=…

# 3) Keine Klartext-.bin im Scripts-Ordner
ls -la *.bin .token_cache* .pbi_token_cache_* 2>&1 | grep -v "No such"
# → leer (= gut)

# 4) .gitignore greift
git check-ignore -v 50.work/m365-graph/scripts/.token_cache.bin
git check-ignore -v 50.work/m365-graph/scripts/.pbi_token_cache_acme.bin
git check-ignore -v 50.work/m365-graph/scripts/foo.bin
# → jeweils Pfad zur passenden Regel
```

## Originale Mail-Body (Auszug, verbatim)

> Hoi zäme
>
> Kurzer, aber wichtiger Sicherheits-Hinweis zu unseren M365-/Graph-/Power-BI-Skripten (`auth_common.py` & Co.): MSAL-Tokens können — je nach Implementierung — als Klartext-Datei (ein `.bin`-Token-Cache) im Vault-Ordner landen. Da der Vault über Dropbox synchronisiert wird (und teils via Git nach GitHub), liegt ein Refresh-Token damit effektiv in der Cloud. Genau das wollen wir nicht.
>
> **Feste Regel ab sofort — Tokens/Secrets immer verschlüsselt im OS-Keystore, nie als Klartext:**
>
> - Kein `msal.SerializableTokenCache`, das eine `.bin`-Datei schreibt.
> - Stattdessen verschlüsselt: macOS → Keychain, Windows → DPAPI. Beides erledigt `msal_extensions` (`PersistedTokenCache` + `KeychainPersistence` bzw. `build_encrypted_persistence()`).
> - Vorlage steckt schon in `auth_common.py`: `build_cache()` für M365, `build_pbi_cache(tenant)` für Power BI / Kunden-Tenants.
> - `.gitignore` muss Token-Pfade abdecken (`*.bin`, `.token_cache*`, `.pbi_token_cache_*`); vor jedem Commit prüfen, ob ein Secret im Diff liegt.
> - Falls doch mal ein Token unverschlüsselt auftaucht: in den Keystore migrieren → Klartext löschen → aus der Git-Historie purgen
>
> **@Ale:** Du bist auf Windows — bei dir ist es DPAPI statt Keychain; `msal_extensions` wählt das automatisch, wenn man `build_encrypted_persistence()` nutzt.
>
> Die aktuelle, korrigierte `auth_common.py` hängt als Referenz an (Keychain-Stand) — zum direkten Abgleich/Übernehmen. Die ANLEITUNG.md habe ich entsprechend aktualisiert.
>
> Fragen? Einfach melden.
>
> Beste Grüsse
> Giovanni

## Verwandt

- [[02-zugangsdaten-secrets]] — CLIENT_ID / TENANT_ID
- [[07-anleitung-v2-toolkit]] — Hauptanleitung (mit aktualisiertem Sicherheits-Abschnitt)
- [[06-mail-giovanni-v2-toolkit-juni-2026]] — Erst-Migration zu Keychain (Juni 2026)
- [[setup-und-workflow]] — Sicherheits-Tabelle
- `scripts/auth_common.py` (Code)
- `scripts/auth_mvm.py` (MVM-AG Tenant, separater Keychain-Eintrag)
