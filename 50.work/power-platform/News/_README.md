---
created: 2026-06-08
source: Power Platform Weekly Newsletter (ppweekly@substack.com)
issues_analyzed: 156
date_range: 2023-01-16 — 2026-06-08
tags: [power-platform, news, hub, copilot, dataverse, mvp]
---

# Power Platform News — Hub

Strukturierte Ablage zu **156 Ausgaben Power Platform Weekly** (Issue #112 → #267, Januar 2023 bis Juni 2026). Quelle: `ppweekly@substack.com`, abgelegt im Outlook-Ordner `0_Emails`.

> **Was ist Power Platform Weekly?** Wöchentlicher Community-Newsletter, kuratiert von **Carina M. Claesson**, **Daniel Laskewitz**, **Ed Gonzales** und **Magnus Gether Sørensen**. Sammelt Artikel, Podcasts, Videos, Events und Microsoft-Releases aus dem gesamten Power-Platform-/Dynamics-365-/Copilot-Ökosystem.

## Navigation

| # | Note | Inhalt |
|---|---|---|
| 01 | [[01-uebersicht-trends]] | Themen-Entwicklung 2023 → 2026 (Copilot-Boom, Agents-Welle, MCP) |
| 02 | [[02-top-personen-mvps]] | Wichtigste MVPs & Autoren (Megan V. Walker, Matthew Devaney, …) |
| 03 | [[03-podcasts]] | Podcast-Katalog (Microsoft Mechanics, PP Boost, BIFocal …) |
| 04 | [[04-events-konferenzen]] | Konferenzen 2024–2026 (EPPC, MPPC, Nordic Summit …) |
| 05 | [[05-releases-2026]] | GA-/Preview-Releases der letzten 12 Monate |
| 06 | [[06-copilot-studio-agents]] | Tiefenanalyse Copilot Studio & Agent-Plattform |
| 07 | [[07-power-bi-fabric]] | Power BI + Microsoft Fabric Updates |
| 08 | [[08-dataverse-mcp]] | Dataverse, MCP-Server & Connector-Strategie |
| 09 | [[09-newsletter-quellen]] | Methodik, Hosts, technische Verarbeitungs-Pipeline |

## Kern-Erkenntnisse (TL;DR)

### 1. Copilot ist die dominanteste Bewegung der letzten 3 Jahre
- **Copilot**-Erwähnungen: 112 (2023) → 313 (2024) → 329 (2025) → 247 (nur H1 2026)
- **Copilot Studio** (vormals Power Virtual Agents): 6 → 59 → 175 → 133 Erwähnungen
- **Agent**-Erwähnungen: 39 → 51 → 290 → 275 → erkennbarer Bruch Q4 2024 / Q1 2025

### 2. Power Virtual Agents wurde 2024 von Copilot Studio abgelöst
- 2023: 34 Erwähnungen → ab 2024: praktisch 0
- Migrationspfad und Naming-Wechsel klar im Newsletter dokumentiert

### 3. Model Context Protocol (MCP) ist die neue Integrations-Welle
- 0 Erwähnungen vor 2025 → 42 in 2025 → 40 in H1 2026
- Microsoft brachte Dataverse-MCP-Server, Power Apps MCP-Server, Snowflake-MCP usw.
- Mistral & Claude Marketplace-Integration in Copilot Studio (2026)

### 4. Code Apps ist das nächste Wachstumsfeld
- Tauchten erstmals 2025 auf, schon 11 Erwähnungen in H1 2026
- Power Pages + GitHub Copilot CLI + Claude Code Integration (GA Juni 2026)

### 5. Power Apps / Power Automate (klassisch) zurückgegangen
- Power Apps: 183 → 110 → 67 → 35 Erwähnungen
- Power Automate: 212 → 117 → 73 → 20 Erwähnungen
- → Fokus verschiebt sich zu Agenten, MCP, Pro-Code-Hybriden

## Wer steht im Zentrum der Community?

**Top-5-Autoren über alle Jahre:**
1. Megan V. Walker (162 Beiträge) — D365 Marketing, Customer Insights
2. Dian Taylor (66) — Customer Engagement, Power Virtual Agents → Copilot
3. David Wyatt (66) — Power Automate, Solution Architect
4. Matthew Devaney (56) — Canvas Apps, Power Fx
5. Ana Inés Urrutia (50) — HR & D365, Microsoft Build Coverage

→ Vollständige Liste in [[02-top-personen-mvps]]

## Aktivste Podcasts

1. **Microsoft Mechanics** (21 Erwähnungen) — Microsoft offiziell
2. **Power Platform Boost** (20) — Carina Claesson & Daniel Laskewitz
3. **BIFocal Podcast** (14) — Power BI tief
4. **Knee-Deep in Tech** (13) — Microsoft-Konsulent:innen Schwerpunkt
5. **Low Code Approach** (12 + 11 Varianten) — Citizen Dev / Pro Dev Brücke

→ Vollständiger Katalog in [[03-podcasts]]

## Datenherkunft & Reproduzierbarkeit

- **Quelle**: Outlook-Ordner `0_Emails` (raoul@miraglia-bi.com)
- **Filter**: `from/emailAddress/address eq 'ppweekly@substack.com'`
- **Skripte** (lokal, nicht im Vault):
  - `50.work/m365-graph/scripts/fetch_ppweekly.py` — Mails via Graph holen
  - `50.work/m365-graph/scripts/analyze_ppweekly.py` — Sektionen + Personen + Themen extrahieren
- **JSON-Output** (lokal, nicht synchronisiert): `ppweekly_digest.json` (1.9 MB), `ppweekly_analysis.json`, `ppweekly_releases.json`
- **Update-Workflow**: Beim nächsten Lauf wird der gesamte Ordner neu eingelesen — Inkrementeller Sync nicht nötig bei 1× pro Woche.

## Verknüpfte Themen im Vault

- [[50.work/power-platform/_README]] — Hauptbereich Power Platform
- [[50.work/m365-graph/_README]] — M365 Graph Tooling (das Daten-Backend dieser Notes)
- [[50.work/25_People/_README|Personen]] — verlinke MVPs hier rein, wenn relevant
