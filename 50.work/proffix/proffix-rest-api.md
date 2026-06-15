---
name: PROFFIX Px5 REST API — Übersicht & Integrationsleitfaden
slug: proffix-rest-api
tags: [proffix, rest-api, erp, integration, auftragsbearbeitung]
type: tech-reference
status: draft
created: 2026-06-15
quellen:
  - https://portal.proffix.net:11011/api-docs/
  - https://documenter.getpostman.com/view/4270070/TzsYPpWh
  - https://github.com/PROFFIX-NET/RestApiPublicAccessDemo
  - https://github.com/pitwch/go-wrapper-proffix-restapi
  - https://pub.dev/packages/dart_proffix_rest
  - https://www.proffix.net/entwickler/restapi/handbuch
---

# PROFFIX Px5 REST API — Übersicht & Integrationsleitfaden

> **Zweck dieser Notiz:** Schneller Einstieg in die PROFFIX-REST-API für Integrationsprojekte (z. B. [[50.work/projekte/Sharkgroup-Enia/Automatisierung-Bestellverarbeitung|Sharkgroup/enia — Automatisierung Bestellverarbeitung]]). Sammlung der zentralen Konzepte, ohne das Handbuch zu duplizieren — mit Links zu offiziellen Quellen für die Details.

## Was die API kann

PROFFIX Px5 stellt ihre Module über eine REST-API mit JSON-Payloads bereit. Die API ist die **offizielle, supportete** Schnittstelle für Drittsysteme (Shops, Power-Automate-Flows, Custom-Apps).

**Typische Use-Cases:**
- Lesen/Schreiben in Stammdaten (Adressen, Artikel, Lager)
- Aufträge anlegen, Positionen verbuchen
- Belege erzeugen, Status abfragen
- Automatisierungen aus Microsoft Power Platform, Custom-Backends, ETL-Jobs

## Architektur in einem Bild

```
┌──────────────────┐       HTTPS / JSON        ┌──────────────────────┐
│  Power Automate  │ ──────────────────────►   │  PROFFIX REST-API    │
│  / Custom-App    │      PxSessionId-Header   │  Port > 10000 (TLS)  │
└──────────────────┘                           └──────────┬───────────┘
                                                          │
                                                ┌─────────▼──────────┐
                                                │  PROFFIX Px5 DB    │
                                                │  (pro Mandant 1×)  │
                                                └────────────────────┘
```

- **Pro Mandant** eine eigene Datenbank-Verbindung → Login muss korrekt auf den Mandanten gesetzt sein.
- **Port > 10000**, ausschliesslich **HTTPS** (SSL erzwungen).
- Generalist-Endpoints — für Public-Web-Zugriffe wird ein eigener Backend-Layer dazwischen empfohlen (siehe [Demo-Repo](https://github.com/PROFFIX-NET/RestApiPublicAccessDemo)).

## Basis-URL & Versionierung

```
https://<host>:<port>/pxapi/v4/<MODUL>/<Entity>
```

- Aktuelle Major-Version: **v4** (Stand 2026)
- Modul-Präfix in CAPS, Entity in CamelCase (z. B. `AUF/Auftrag`)
- In älteren Doku-Snippets taucht auch `/pro/v4/` auf — heute Standard `/pxapi/v4/`

## Authentifizierung — PxSessionId

**Login-Flow:**

1. `POST /pxapi/v4/PRO/Login` mit JSON-Body:
   ```json
   {
     "Benutzer": "API_USER",
     "Passwort": "<SHA256-Hash des Klartext-Passworts>",
     "Datenbank": { "Name": "DEMO" },
     "Module": ["VOL", "ADR", "LAG", "FIB"]
   }
   ```
2. Antwort enthält Header `PxSessionId: <token>`
3. **Jeder folgende Request** muss diesen Header mitschicken
4. `DELETE /pxapi/v4/PRO/Login` zum sauberen Logout → gibt Lizenz frei

> ⚠️ **Lizenzfalle:** Jede aktive Session belegt eine PROFFIX-Lizenz. Hängende Sessions blockieren Logins. Wrapper wie der [Go-Wrapper](https://github.com/pitwch/go-wrapper-proffix-restapi) führen automatischen Logout bei Fehlern durch — bei eigener Implementierung muss das **manuell sichergestellt** werden (try/finally, idempotenter Logout).

> **Token-Storage:** Wenn der Flow den PxSessionId zwischen Aufrufen wiederverwendet (z. B. Power-Automate-Variable, Azure-Key-Vault) → **immer verschlüsselt** speichern, nie als Klartext-Datei im Repo. Vault-Regel: [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore]].

## Modul-Mapping (Auswahl)

| Modul-Präfix | Bereich | Beispiel-Entitäten |
|---|---|---|
| `PRO` | System, Login, Datenbank, Info | `Login`, `Info`, `Datenbank`, `Datei` |
| `ADR` | Adress-/CRM-Modul | `Adresse`, `Kontakt`, `Ansprechpartner` |
| `LAG` | Artikel- & Lagerverwaltung | `Artikel`, `Lagerort`, `Lagerbestand` |
| `AUF` | Auftragsbearbeitung | `Auftrag`, `Auftragsposition`, `Lieferschein`, `Rechnung` |
| `FIB` | Finanzbuchhaltung | `Konto`, `Buchung`, `Belegart` |
| `VOL` | Volltextsuche | `Datensatz` |
| `STU` | Stundenerfassung / Rapporte | `Rapport`, `Mitarbeiter` |

> Vollständige Auflistung im offiziellen Entwicklerhandbuch: <https://www.proffix.net/entwickler/restapi/handbuch> sowie in der [Postman-Collection](https://documenter.getpostman.com/view/4270070/TzsYPpWh).

## Workflow „Auftrag anlegen" (typische Sequenz)

```
1. POST  PRO/Login                      → PxSessionId
2. GET   ADR/Adresse?Filter=KundenNr eq '12345'
                                        → AdressNr ermitteln
3. GET   LAG/Artikel?Filter=ArtikelNr eq '34150'
                                        → interne ArtNr validieren
4. POST  AUF/Auftrag                    → Auftragskopf anlegen
                                        Response enthält Auftrags-ID/Nr
5. POST  AUF/Auftragsposition (n×)      → Positionen anhängen
6. (optional) POST AUF/Lieferschein     → Beleg erzeugen
7. DELETE PRO/Login                     → Session schliessen
```

**Wichtig:**
- `AUF/Auftrag` wird **vor** den Positionen angelegt — die `AuftragsNr` aus der Response wird in jeder Position referenziert
- POST-Bodies erwartet PROFFIX als JSON mit den DB-Feldnamen (Pascal-Case)
- IDs / Beleg-Nummern werden von PROFFIX vergeben → nicht clientseitig generieren

## Offene Wrapper / Referenzimplementierungen

| Tech | Repo | Was es bietet |
|---|---|---|
| Go | [pitwch/go-wrapper-proffix-restapi](https://github.com/pitwch/go-wrapper-proffix-restapi) | Vollständiger Client mit Session-Mgmt, generische `Get/Put/Post/Patch/Delete` |
| Dart | [dart_proffix_rest](https://pub.dev/packages/dart_proffix_rest) | Flutter-tauglich, ähnliche API |
| Node | [proffix-rest auf npm](https://www.npmjs.com/package/proffix-rest) | JS-Wrapper |
| .NET | [PROFFIX-NET/RestApiErweiterungenTemplate](https://github.com/PROFFIX-NET/RestApiErweiterungenTemplate) | VS-Template für API-Extensions (server-seitig) |
| PHP | [PROFFIX-NET/RestApiPublicAccessDemo](https://github.com/PROFFIX-NET/RestApiPublicAccessDemo) | Pattern für Public-Web-Zugriff über eigenen Backend-Layer |

> Für Power Automate gibt es **keinen offiziellen Connector** — Zugriff erfolgt über die generischen `HTTP`-Actions oder eine Custom-Connector-Definition. Bei Sharkgroup vermutlich relevant: einmaliges Aufsetzen eines Custom-Connectors mit den 4–6 benötigten Endpoints + PxSessionId-Refresh-Logik.

## Häufige Stolpersteine

1. **Lizenz blockiert** durch hängende Sessions → strikter Logout im `finally`-Block; Monitoring über `GET PRO/Info`.
2. **SHA256-Hash vergessen** — Passwort wird **nicht** im Klartext gesendet, sondern als Hex-codierter SHA256-Hash.
3. **Filter-Syntax** ist OData-ähnlich (`?Filter=Feld eq 'Wert'`), nicht 1:1 OData.
4. **Pro Mandant separate Credentials** — bei Multi-Mandanten-Setup (z. B. enia vertriebs gmbh als eigener Mandant innerhalb der Sharkgroup-Installation) muss die Schnittstelle für diesen Mandanten freigeschaltet sein.
5. **Number-Locale:** PROFFIX akzeptiert in JSON Standard-Dezimalpunkt (`12.50`), nicht Komma — Quelle Power Automate liefert oft Komma (siehe Hunnenberg-Pattern, [[50.work/projekte/Hunnenberg/Prompt-Auftragserstellung-2026-06-09#3 Locale-Falle bei Zahlen-Export ins CSV Sage]]).

## Wann eigene Schicht zwischen Client und PROFFIX?

- **Direkt aus Power Automate:** bei wenigen, klar definierten Endpoints und geringer Last (≤ einige hundert Aufrufe/Tag) — am einfachsten via HTTP-Action + Custom Connector.
- **Eigene Middleware (Azure Function / .NET):** wenn mehrere Quellsysteme gegen PROFFIX schreiben, komplexere Validierung nötig ist, oder die Lizenzökonomie wichtig wird (gepoolte Session, Rate-Limiting).
- **PROFFIX-Erweiterung (.NET In-Process):** wenn Logik **innerhalb** von PROFFIX laufen soll (z. B. Trigger auf Buchung) → siehe Erweiterungs-Template.

## Verwandt

- [[50.work/projekte/Sharkgroup-Enia/Automatisierung-Bestellverarbeitung|Sharkgroup/enia — Automatisierung Bestellverarbeitung]] (laufendes Projekt 2026)
- [[50.work/projekte/Hunnenberg/Prompt-Auftragserstellung-2026-06-09|Hunnenberg — AI-Prompt-Pattern Auftragserstellung]] (verwandtes Pattern, anderes ERP)
- [[50.work/m365-graph/09-regel-tokens-verschluesselt-keystore|Regel: Tokens verschlüsselt im Keystore]]
- [[40.meta/prompt-strukturierte-extraktion|Pattern: Strukturierte JSON-Extraktion]]

## Offene Punkte / TODOs

- [ ] Custom Connector für PROFFIX in Power Automate bauen (einmalig)
- [ ] Klären: ist API für Mandant `enia vertriebs gmbh` bereits freigeschaltet? (Sharkgroup-IT / Alessandro Castelli)
- [ ] SHA256-Login-Helper-Snippet für Power Automate dokumentieren
- [ ] Test-Endpoint / Sandbox-DB von Sharkgroup für Entwicklung beschaffen
