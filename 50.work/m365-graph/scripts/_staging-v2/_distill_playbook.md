# Playbook: OneNote-Export → Obsidian-Kunden-Hub destillieren

Du destillierst den OneNote-Export **eines** Kunden in seinen Obsidian-Kunden-Hub.
Kontext: **Miraglia BI** ist eine Power-BI / Business-Intelligence-Beratung. Die Kunden-Hubs leben in `20_Clients/`.

**WICHTIG:** Arbeite NUR mit lokalen Dateien. Rufe KEINE Microsoft-/Graph-API auf, starte KEIN Export-Skript (`onenote_export.py`/`onenote_batch_export.py`) — die Daten liegen bereits lokal.

VAULT-ROOT: `/Users/miragliag/Dropbox/Miraglia-BI/0_Internal/Obsidian gimi/Miragliag`
Heutiges Datum für Log-Einträge: **2026-06-03**.

Der Orchestrator nennt dir pro Auftrag: **Export-Ordner**, **Ziel-Hub** und ggf. **Sonderhinweise**.

## Schritte

1. **Alles lesen.** Lies alle `.md` unter dem Export-Ordner. Bei vielen Seiten zuerst ein Digest bauen (kleines Python via `40_Resources/scripts/.venv/bin/python`, das Frontmatter strippt und Titel+Body je Seite ausgibt). Verstehe den Inhalt vollständig. Schau bei Bedarf in `_attachments/` (Bilder via Read).

2. **Journal vs. Wissen trennen.**
   - **Journal-/Datumseinträge** ("Journal vom DD.MM", Meeting-/Remote-Logs, To-dos) duplizieren das **Dataverse-Projektjournal** → **NICHT** kopieren.
   - Extrahiere nur **durable Wissen**: Systeme/Stack (ERP, DBs, Gateways, Power-BI-Modelle & Workspaces, Power-Platform-Apps & Environments, Schnittstellen), Apps & Prozesse (Datenmodelle, Security-Gruppen, Deployment-Wege, Architektur), Stakeholder/Kontakte (Name, Rolle, E-Mail, Tel.), wichtige Entscheidungen/Konventionen/offene Punkte.
   - **Auch in Journalen stecken durable Nuggets** (ein Kontakt, ein Environment-Name, ein Systemfakt, eine Architekturentscheidung) — heb sie heraus, obwohl du die chronologische Erzählung verwirfst.

3. **Hub anreichern oder anlegen.**
   - **Existiert der Ziel-Hub:** script-verwaltete Blöcke **UNANGETASTET** lassen — alles zwischen `<!-- firmenprofil -->…<!-- /firmenprofil -->`, `<!-- ppnews-client -->…`, `<!-- people-sync -->…` sowie das YAML-Frontmatter. Niemals diese Blöcke editieren.
   - Bestehende Abschnitte **anreichern** (`## Stakeholder` außerhalb des people-sync-Blocks, `## Systems / Stack`, `## Active Topics`) und neue Abschnitte hinzufügen: `## Systems / Stack` (falls fehlt), `## Power Platform Apps & Prozesse` (falls zutreffend), `## OneNote-Destillat — Kontakte` und/oder `## OneNote-Destillat — Entscheidungen & Konventionen`. **Nichts duplizieren**, was schon im Hub steht.
   - **Existiert der Hub NICHT:** prüfe am Inhalt, ob es ein **echter Kunde** ist. Falls ja → Hub aus `_Templates/Client.md`-Konvention anlegen (Frontmatter `type: client`, `status: active`, `tags: [client]`, `created: 2026-06-03`) + H1 + die destillierten Abschnitte. Falls es **intern/Partner/Demo/leer ohne durable Wissen** ist → **keinen** Hub anlegen, sondern im Bericht klar sagen (mit dem, was du gesehen hast).
   - **Log-Eintrag** (Abschnitt `## Log`, anlegen falls fehlt): `- 2026-06-03 — OneNote „<Notizbuch>" (N Seiten) destilliert → <was ergänzt>. Journale ≈ Dataverse (kein 1:1-Import). Source of Record: OneNote + Dataverse.`

4. **Sicherheit.** KEINE rohen Passwörter/Credentials/Secrets/Connection-Strings/Subscription-Keys in den Vault. Security-Gruppen-GUIDs, App-/Play-URLs, IPs nur als „im OneNote dokumentiert" **referenzieren**, nicht einfügen. Falls du Secrets findest, weise im Hub knapp darauf hin (Callout), ohne sie zu kopieren.

5. **Export-Ordner NICHT löschen** (zentrale Aufräumung später durch den Orchestrator).

6. **Stil.** Scannbar, fettgedruckte Labels, Bullet-Points — wie die durable Wissensnotiz eines Senior-BI-Beraters. **Deutsch.** Vault-Dateien als Wikilinks `[[…]]`.

## Rückgabe (für den Orchestrator, < 180 Wörter)
Kunde · #Seiten · Journal-vs-Wissen-Split · Hub angereichert/neu/keiner (Begründung) · welche Abschnitte · auffällige Systeme/Kontakte · Secrets gefunden (ja/nein, ausgelassen).
