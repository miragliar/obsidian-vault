---
created: 2026-06-08
source: PP Weekly Issues #112–#267
tags: [power-platform, news, methodik, quellen, pipeline]
---

# 09 — Newsletter, Quellen & Methodik

Wie diese Notes entstanden sind, wer den Newsletter macht, und wie wir ihn künftig aktuell halten.

## Über Power Platform Weekly

- **URL**: https://powerplatformweekly.substack.com/
- **Frequenz**: 1× pro Woche (Sonntag/Montag)
- **Absender**: ppweekly@substack.com
- **Format**: HTML-Email mit klar strukturierten Sektionen
- **Lizenz**: kostenlos, Opt-In

### Sektionen pro Ausgabe (Standard-Struktur)

1. 📰 **Articles** — Features + Other Articles (Community-Blog-Posts)
2. 📺 **Videos** — YouTube, MS Learn, Channel 9
3. 🎙️ **Podcasts** — Episodes der laufenden Woche
4. 📅 **Events & Webinars** — kommende Konferenzen
5. 💙 **Out of the Blue** — Microsoft Releases / Announcements
6. 🚀 **Releases** (manchmal eigene Sektion, manchmal in Out of the Blue)
7. 🛠 **Tools** — neue Community Tools
8. 💡 **Tips & Tricks** (selten)

### Persona-Icons (Stand 2026)

In den Newsletter-Texten markieren Emojis die Zielgruppe:

| Emoji | Persona |
|---|---|
| 🤵🏻 | Business User |
| 🦸🏻‍♀️ | Maker |
| 🧭 | Decision Maker |
| 👩‍💻 | Developer / Architect |
| 🚀 | Admin / Center of Excellence |
| 🛠️ | Tools |

## Editor-Team

Stand Juni 2026 (Issue #267):

| Name | Rolle | Public Identity |
|---|---|---|
| **Carina M. Claesson** | Lead Editor | MVP, Host *Power Platform Boost Podcast* |
| **Daniel Laskewitz** | Editor | Microsoft, ehem. MVP, Host *Power Platform Boost* |
| **Ed Gonzales** | Editor | Microsoft, Host *Awkward Silence Podcast* |
| **Magnus Gether Sørensen** | Editor | Dänemark/Nordic, Konferenz-Co-Organisator |

Gastkurator:innen pro Ausgabe (rotierend für die Article-Features):
- Issue #267: Angeliki Patsiavou, Vivian Voss, Dennis Chi.
- Andere Ausgaben: wechselnd, oft aktuelle MVPs.

## Datenherkunft & Pipeline (Vault-intern)

### Schritt 1 — Mail-Abruf via Microsoft Graph

- **Skript**: `50.work/m365-graph/scripts/fetch_ppweekly.py`
- **Auth**: Delegated, MSAL Token Cache im macOS Keychain (`auth_common.py`)
- **Scopes**: `Mail.Read`, `User.Read`
- **Filter**:
  - Outlook-Ordner: `0_Emails`
  - Sender: `ppweekly@substack.com`
- **Output**: `ppweekly_digest.json` (lokal, ~1.9 MB, .gitignore-geschützt)

```bash
cd 50.work/m365-graph/scripts
./.venv/bin/python fetch_ppweekly.py
```

### Schritt 2 — Strukturierte Analyse

- **Skript**: `50.work/m365-graph/scripts/analyze_ppweekly.py`
- **Extrahiert**:
  - Sektionen pro Issue (Articles / Podcasts / Videos / Events / Out of the Blue)
  - Top-Autoren (regex auf `by <Name>`)
  - Top-Personen (heuristisch, „Vorname Nachname" Pattern)
  - Podcast-Namen
  - Events mit Datum
  - „Out of the Blue" Items (Releases)
- **Output**:
  - `ppweekly_analysis.json` — strukturierter Auszug pro Issue
  - `ppweekly_releases.json` — alle 1388 Out-of-Blue-Items, datiert

```bash
./.venv/bin/python analyze_ppweekly.py
```

### Schritt 3 — Notes-Erstellung

Diese Notes (01–09) wurden auf Basis der JSON-Outputs erstellt. Sie sind **nicht** automatisch regeneriert — sondern manuell kuratiert.

### Update-Workflow

Wenn neue Newsletter-Ausgaben einlaufen (1× pro Woche):

1. Mails landen automatisch im Outlook-Ordner `0_Emails`.
2. `fetch_ppweekly.py` neu laufen lassen → JSON aktualisiert.
3. `analyze_ppweekly.py` → Analyse aktualisiert.
4. Diese Notes prüfen:
   - **05-releases-2026**: neue Out-of-Blue-Einträge nachtragen.
   - **02-top-personen-mvps**: Counter auffrischen, neue Stimmen hinzufügen.
   - **03-podcasts**: neue Episodes der Top-Podcasts ergänzen.
   - **04-events-konferenzen**: kommende Events einpflegen.

> Optional: Ein Skript könnte die Notes auch teilweise auto-regenerieren. Aktuell ist die kuratierte Variante besser, weil die Synthese (Narrative, Empfehlungen) menschlich getroffen wurde.

## Datenintegrität & Bekannte Limitierungen

### Was zuverlässig ist
- Anzahl Erwähnungen pro Begriff (regex-basierte Zählung)
- Daten und Issue-Nummern
- Autor:innen-Namen (über `by <Name>` Pattern extrahiert)
- Sektions-Aufteilung

### Was mit Vorsicht zu lesen ist
- **Top-Personen-Liste** ist heuristisch — enthält false positives wie „Business User", „Decision Maker", „The Netherlands" (geographische Bezeichnungen).
- **Podcast-Namen** sind teilweise mit/ohne Bindestrich doppelt gezählt (Low Code vs Low-Code).
- **Events**-Liste enthält gelegentlich verstümmelte Namen, weil mehrere Events im Newsletter manchmal mit unterschiedlicher Trennung erscheinen.

### Korrigiert-für die Notes
- Die Top-20-Listen wurden manuell gegen die Heuristik-Ergebnisse abgeglichen.
- Personen-/Podcast-/Event-Tabellen sind als kuratiert zu betrachten.

## Quellen-Verlinkung (für Tiefenrecherche)

Statt jeden Newsletter zu verlinken, kann man auf den Online-Archiv-Eintrag verweisen:

- `https://powerplatformweekly.substack.com/p/power-platform-weekly-issue-{NN}` (Heuristik, Substack-Pattern)
- Direkt-Links zu Issues stehen in den ursprünglichen Mails (`webLink` Feld des Graph-API-Responses)

Aus dem JSON-Digest können wir bei Bedarf den Outlook-`webLink` jeder Mail extrahieren — Pfad: `ppweekly_digest.json` → Feld `webLink` pro Eintrag.

## Stichproben & nächste Schritte

### Wenn ein bestimmtes Issue tiefer gelesen werden soll

```bash
# JSON laden, gewünschte Issue-Nummer rausziehen
cd 50.work/m365-graph/scripts
./.venv/bin/python -c "
import json
d = json.load(open('ppweekly_digest.json'))
issue = [m for m in d if 'Issue #267' in m['subject']][0]
print(issue['body_text'])
"
```

### Wenn nur Releases recherchiert werden sollen

```bash
./.venv/bin/python -c "
import json
r = json.load(open('ppweekly_releases.json'))
# Letzte 30 Releases
for item in r[:30]:
    print(f\"#{item['issue']:>3} {item['received']}: {item['text'][:200]}\")
"
```

### Nächste mögliche Skript-Erweiterungen

- [ ] Auto-Link-Extraktion (URLs aus HTML → Markdown)
- [ ] Bild-Extraktion (Issue-Thumbnails)
- [ ] Personen-Notiz-Stub-Generierung (für MVPs mit ≥5 Erwähnungen automatisch leere Notiz in `25_People/` anlegen)
- [ ] Inkrementeller Sync (nur neue Mails seit letztem Lauf)

## Querverweise

- Hub → [[_README]]
- Themen-Trends → [[01-uebersicht-trends]]
- M365 Graph Setup im Allgemeinen → [[50.work/m365-graph/_README]]
- M365 Graph Skripte → [[50.work/m365-graph/setup-und-workflow]]
