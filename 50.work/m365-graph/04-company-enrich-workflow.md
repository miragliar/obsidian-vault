---
source: claude-import
imported: 2026-06-01
related_emails: [Giovanni Miraglia 2026-06-01 Nachtrag]
tags: [miraglia, company, zefix, web-scrape, automation, anreicherung]
---

# Firmen-Steckbrief automatisch (Webseite + Zefix)

Nachtrag-Tooling von Giovanni: `company_enrich.py` baut für eine Firma einen Steckbrief aus zwei Quellen:

1. **Webseite** (kostenlos, ohne Login) — Title, Meta-Description, og:description
2. **Handelsregister Zefix** (kostenlos mit Registrierung) — UID, Rechtsform, Sitz, Kanton, Status

## Use Cases

- **Neuer Kunde / Lead:** Steckbrief generieren, in Personen-/Klienten-Notiz einfügen
- **Bestehende Kontakte enrichen:** Per Batch alle bekannten Firmen ergänzen (siehe [[#Batch-Anreicherung aller 9 Firmen|Batch unten]])
- **Vor Meeting:** UID + Sitz + Was-sie-tun in 5 Sek auf Notiz haben

## Setup (einmalig)

### Webseite — ohne Login (sofort einsatzbereit)

Funktioniert ohne weitere Konfiguration. Nur `requests` (bereits installiert):

```bash
cd 50.work/m365-graph/scripts
source .venv/bin/activate
python3 company_enrich.py --name "Nahrin AG" --url https://www.nahrin.ch --md
```

### Zefix — mit kostenloser API-Anmeldung

1. Auf https://www.zefix.ch → API-Login registrieren (kostenlos)
2. Bestätigungs-Mail → Account aktivieren
3. Username + Passwort als Env-Vars setzen:

```bash
export ZEFIX_USER="<dein-zefix-username>"
export ZEFIX_PASS="<dein-zefix-passwort>"
```

Oder persistent in `~/.zshrc` ergänzen.

Dann:

```bash
python3 company_enrich.py --name "Nahrin AG" --url https://www.nahrin.ch --zefix --md
```

→ Output enthält zusätzlich `zefix.matches[]` mit UID, Rechtsform, Sitz.

## Output-Format

### JSON (stdout)

```json
{
  "name": "Nahrin AG",
  "website": {
    "url": "https://www.nahrin.ch",
    "title": "Bouillons, Gewürze & Nahrungsergänzung. Schweizer Qualität",
    "description": "Nahrin AG - natürlich, gesund, wertvoll. …",
    "site_name": null
  },
  "zefix": {
    "matches": [
      {
        "name": "Nahrin AG",
        "uid": "CHE-XXX.XXX.XXX",
        "chid": "...",
        "legalSeat": "Sarnen",
        "canton": "OW",
        "legalForm": "Aktiengesellschaft",
        "status": "active"
      }
    ]
  }
}
```

### Markdown-Block (`--md`)

Wird zwischen `<!-- firmenprofil -->` und `<!-- /firmenprofil -->` ausgeliefert, ready zum Copy/Paste oder Auto-Insert in Klienten-Notizen.

## Vault-Integration

### Pattern in Personen-Notiz

```markdown
## Unternehmensprofil

<!-- firmenprofil -->
*Aktiengesellschaft · Sarnen · CHE-XXX.XXX.XXX*

**Webseite-Titel:** ...
**Was sie tun:** ...
**Web:** https://www.nahrin.ch
<!-- /firmenprofil -->
```

→ Der Marker erlaubt **inkrementelles Refresh** ohne Verlust manueller Notizen außerhalb des Blocks.

## Batch-Anreicherung aller 9 Firmen

Wrapper-Skript [[../../../_imports/enrich_companies.py]] hat am 01.06.2026 alle 9 bekannten Firmen aus `25_People/` verarbeitet:

| Firma | URL | Notiz angereichert |
|---|---|---|
| Miraglia Business-Intelligence | miraglia-bi.com | [[../../../25_People/Giovanni-Miraglia]] |
| Kipfer DP | kipfer-dp.com | [[../../../25_People/Michael-Kipfer]] |
| Castelli Solutions | castelli-solutions.ch | [[../../../25_People/Alessandro-Castelli]] |
| MVM AG | mvm-ag.ch | [[../../../25_People/Remo-Pfister]] |
| Nahrin AG | nahrin.ch | [[../../../25_People/Stefanie-Ringwald]], [[../../../25_People/Christoph-Kübler]] |
| Obrist Interior | obrist-interior.ch | [[../../../25_People/Barbara-Gilli]] |
| Bordoni Solutions | bordoni-solutions.com | [[../../../25_People/Mark-Bordoni]] |
| Cloud Champion | cloudchampion.ch | [[../../../25_People/Daniel-CloudChampion]] |
| Koster AG | kosterag.ch | [[../../../25_People/H.-Baumann]] |

**Output:** `scripts/company_profiles.json` mit allen Steckbriefen (gitignored).

**Lauf-Modus:** ohne Zefix, nur Webseite (API-Account fehlt noch). Wenn ZEFIX_USER/ZEFIX_PASS gesetzt sind, kann das Batch-Skript um `--zefix` erweitert werden.

## Refresh-Strategie

- Bei neuer Personen-Notiz: einmalig `company_enrich.py --md` → Block in Notiz einfügen
- Quartalsweise: `enrich_companies.py` neu laufen lassen — überschreibt `<!-- firmenprofil -->` Block, andere Inhalte bleiben unangetastet
- Bei Adress-/Status-Änderung: nur Zefix neu abfragen → UID bleibt, Sitz/Status updaten

## Wann nicht

- **Bei B2C-Endkunden / Privatpersonen:** Zefix ist nur sinnvoll für Firmen (juristische Personen). Privatpersonen → keine UID, keine Rechtsform.
- **Bei nicht-Schweizer Firmen:** Zefix deckt nur CH. Für DACH-Recherche → `northdata.com` oder ähnliche Quellen ergänzen.
- **Wenn die Webseite JavaScript-rendered ist** (SPA, React etc.): das simple `requests.get` sieht keine Inhalte. Workaround: Playwright/Puppeteer für headless Browser — Overhead, in diesem Kontext meist unnötig.
- **Bei großen Batches** (>100 Firmen): Rate-Limits beachten, Sleeps einbauen.
- **Wenn die Webseite no-robots / Bot-Detection hat:** UA spoof reicht oft nicht. Ggf. manuell Steckbrief aus LinkedIn/Webseite extrahieren.

## Sicherheit

- Webseite-Lookup ist ein normaler HTTP-GET — keine Bedenken
- Zefix-API: Basic-Auth, deine Credentials niemals in Notizen oder Repos
- `company_profiles.json` enthält **öffentliche** Informationen (Webseiten + Handelsregister) — kein Privacy-Issue, könnte sogar committable sein (aber `.gitignore` schließt es trotzdem aus, weil im Output-Format generiert)

## Verwandt

- [[setup-und-workflow]] — Outlook-Mail / Teams-Chat Aggregation (verwandte Tools)
- [[01-chef-mail-juni-2026]] — ursprüngliche Mail
- [[02-zugangsdaten-secrets]] — wo Zefix-Credentials hingehören
- [[03-personen-notiz-vorlage]] — Personen-Notiz-Struktur
- [[../../../_imports/enrich_companies.py|Batch-Wrapper]]
