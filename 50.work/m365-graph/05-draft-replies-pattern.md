---
source: chat-context 2026-06-04
imported: 2026-06-04
type: pattern
tags: [m365, microsoft-graph, outlook, drafts, signatur, automation]
related_projects: ["[[50.work/projekte/Regieapp-Neubau-MVM|Regie-Rapport-App MVM]]", "[[50.work/projekte/Magazin-App-MVM|Magazin-App MVM]]", "[[50.work/projekte/Mahnprozess-MVM|Mahnprozess MVM]]"]
---

# M365 Graph Pattern: Antwort-Entwürfe mit Inline-Signatur

Pattern für das **batchweise Erstellen von Antwort-Entwürfen (Drafts)** im eigenen Outlook-Postfach via Microsoft Graph — mit replizierter HTML-Signatur (inkl. Logo als Inline-Attachment) eines Kollegen / einer Vorlagen-Mail. Entstanden 2026-06-04 im MVM-Kontext (3 Drafts an Remo Pfister).

## Use-Case

- Du musst auf mehrere Mails reagieren mit ähnlich strukturierten Inhalten.
- Du willst Entwürfe (nicht direkt gesendete Mails) — Mensch reviewt vor Send.
- Du willst eine **konsistente, hochwertige Signatur** wie sie ein Kollege bereits in seinen Mails verwendet, ohne sie händisch aus dem Outlook-Signatur-Editor zu konfigurieren.

## Lösung im Überblick

```
┌──── inspect_signature.py ────────────┐
│ holt jüngste Mail eines Kollegen     │
│ → giovanni_sample.html               │
│ (zeigt HTML-Struktur seiner Signatur)│
└──────────────────────────────────────┘
              │
              ▼
┌──── extract_logo.py ──────────────────┐
│ findet Inline-Attachment              │
│ (contentId='miragliabi-logo')         │
│ → miraglia_logo.png                   │
└───────────────────────────────────────┘
              │
              ▼
┌──── draft_replies_mvm.py ─────────────┐
│ 1. findet Original-Mail (Absender +   │
│    Subject + Datum-After)             │
│ 2. createReply → Draft mit Zitat      │
│ 3. PATCH body (Antwort + Sig + Zitat) │
│ 4. POST Inline-Attachment (Logo)      │
│ 5. Idempotenz: alte Drafts mit        │
│    gleichem Subject vorher löschen    │
└───────────────────────────────────────┘
              │
              ▼
┌──── preview_draft.py / list_drafts.py ┐
│ Sichtkontrolle: Body + Attachments    │
│ + Empfänger der erstellten Drafts     │
└───────────────────────────────────────┘
```

## Voraussetzungen

- M365 App-Registrierung mit delegiertem Scope **`Mail.ReadWrite`** (zusätzlich zu `Mail.Read`).
- Admin-Consent bereits erteilt (war bei Miraglia BI Public Client der Fall).
- Logo / Inline-Image als PNG/JPG aus einer existierenden Mail des Kollegen extrahierbar (siehe `extract_logo.py`).

## HTML-Signatur-Aufbau (am Beispiel Giovanni → Raoul)

Giovannis Signatur (`giovanni_sample.html`) verwendet:

- **2-spaltige Tabelle** (`<table>`)
  - Linke Spalte: Logo via `<img src="cid:miragliabi-logo">` mit fixen Maßen (`width="64" height="67"`), verlinkt auf `miraglia-bi.com`
  - Rechte Spalte: Daten-Block mit `border-left:3px solid rgb(74,167,46)` (grüner Vertikal-Strich)
- **Schrift:** `font-family:Aptos,Calibri,Arial,sans-serif; font-size:11pt`
- **Hierarchie:** Name fett, Titel-Zeilen, Tel, Mail (Mailto-Link), Web (URL-Link)
- **Vor der Tabelle:** `<br><br>` (Abstand zur letzten Body-Zeile)

→ Diese Struktur lässt sich 1:1 für andere Personen wiederverwenden: nur Name, Titel, Tel, Mail tauschen + ggf. Logo durch Personen-/Firmen-Logo ersetzen.

## Wichtige Graph-API-Details

### createReply

```http
POST /me/messages/{id}/createReply
```

Liefert einen **Draft mit bereits eingefügtem Zitat-Block** des Originals (inkl. „From: / Sent: / Subject:" Header). Subject wird automatisch auf `RE: <original>` gesetzt (locale-abhängig, im DE-Tenant zT auch `AW:`).

### Body komplett ersetzen (PATCH)

```http
PATCH /me/messages/{draftId}
Body: { "body": { "contentType": "HTML", "content": "<our reply HTML>" + existing_body } }
```

Wichtig: **unsere Antwort + Zitat-HTML** wird vollständig ersetzt. Also `our_html + existing_body` zusammensetzen, sonst geht das Zitat verloren.

### Inline-Image-Attachment

```http
POST /me/messages/{draftId}/attachments
Body:
{
  "@odata.type": "#microsoft.graph.fileAttachment",
  "name": "miraglia_logo.png",
  "contentType": "image/png",
  "isInline": true,
  "contentId": "miragliabi-logo",
  "contentBytes": "<base64>"
}
```

- `isInline: true` + `contentId` korrespondiert mit dem `cid:<contentId>` im HTML.
- Reihenfolge: ERST Draft + Body, DANN Attachment. Sonst greift das HTML `cid:` nicht.

### $filter-Restriktionen bei `me/messages`

Graph erlaubt nicht beliebige Kombinationen aus `$filter` + `$orderby` auf Messages. Sicher:
- Filter NUR auf `from/emailAddress/address` → liefert `InefficientFilter` wenn mit `$orderby receivedDateTime` kombiniert
- Lösung: Mails breit holen (Top 50, Sort by date), **Filter-Logik in Python** (Absender + Subject + Datum).

## Idempotenz-Trick

Beim erneuten Lauf alte Drafts mit identischem Reply-Subject löschen, bevor neue erstellt werden:

```python
GET /me/mailFolders/drafts/messages?$top=50&$orderby=createdDateTime desc
# filter local für "RE: <original>" / "AW: <original>"
DELETE /me/messages/{id}
```

So bleibt der Drafts-Ordner sauber, auch wenn das Script mehrfach läuft (z.B. nach Signatur-Tuning).

## Script-Inventar (Stand 2026-06-04)

Im Verzeichnis `50.work/m365-graph/scripts/`:

| Script | Zweck | Wiederverwendbar? |
|---|---|---|
| `inspect_signature.py` | Speichert jüngste HTML-Mail einer Person als Sample | ja, Person als Parameter |
| `extract_logo.py` | Findet Inline-Attachment per `contentId` | ja, contentId als Parameter |
| `draft_replies_mvm.py` | Erstellt batch Reply-Drafts mit Signatur + Logo | als Template, DRAFTS-Liste anpassen |
| `preview_draft.py` | Speichert HTML eines Drafts als `preview_draft.html` | ja |
| `list_drafts.py` | Listet Drafts mit Subject + Empfänger | ja |
| `mvm_extras.py` | Fokus-Suche letzte 500 Mails nach Tag/Domain/Keyword | ja, Filter-Logik anpassen |

## Sicherheitshinweise

- `mail_digest.json`, `mvm_extras.json`, `giovanni_sample.html`, `preview_draft.html` enthalten echte Mail-Inhalte → liegen unter `.gitignore`, nicht extern teilen.
- Logo-Bytes (`miraglia_logo.png`) sind nicht sensitiv (öffentliches Firmen-Logo) — könnten committed werden; Aktuelle `.gitignore` lässt sie aber raus.

## Wann nicht

- Wenn du nur EINE Antwort schreiben willst — schneller per Hand im Outlook.
- Wenn der Tenant `Mail.ReadWrite` nicht consented hat → entweder Admin-Consent anfragen oder als HTML-Datei ablegen und manuell ins Outlook kopieren.
- Wenn die Signatur in Outlook-Settings konfiguriert ist und vom User selbst nachgepflegt werden soll — dann unsere Script-Signatur weglassen und Outlook nachträglich anhängen lassen (klappt aber bei `createReply` nicht automatisch).

## Verwandt

- [[50.work/m365-graph/setup-und-workflow|M365 Graph Setup]] — Basis-Config
- [[50.work/m365-graph/_README|M365 Graph README]]
- [[50.work/m365-graph/02-zugangsdaten-secrets|Zugangsdaten]]
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04]] — ursprünglicher Anwendungsfall
