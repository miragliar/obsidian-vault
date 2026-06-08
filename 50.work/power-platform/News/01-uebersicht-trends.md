---
created: 2026-06-08
source: PP Weekly Issues #112–#267 (156 Ausgaben)
tags: [power-platform, news, trends, copilot, mcp, agents]
---

# 01 — Übersicht & Themen-Trends

Quantitative Auswertung: wie sich die Power-Platform-Sprache über 3.5 Jahre verändert hat. Zahlen = Erwähnungen pro Jahr in allen 156 Newslettern.

## Themen-Heatmap 2023 → 2026

| Thema | 2023 | 2024 | 2025 | 2026 (H1) | Trend |
|---|---:|---:|---:|---:|---|
| **Copilot** (gesamt) | 112 | 313 | 329 | 247 | 📈 stabil hoch |
| **Copilot Studio** | 6 | 59 | 175 | 133 | 📈📈 stark wachsend |
| **Agent** | 39 | 51 | 290 | 275 | 📈📈 Boom seit 2025 |
| Power BI | 129 | 148 | 141 | 44 | ➡️ konstant |
| Dataverse | 121 | 119 | 128 | 71 | ➡️ konstant |
| Power Apps (klassisch) | 183 | 110 | 67 | 35 | 📉 abnehmend |
| Power Automate (klassisch) | 212 | 117 | 73 | 20 | 📉📉 stark abnehmend |
| Power Pages | 105 | 109 | 95 | 44 | ➡️ leicht abnehmend |
| Power Fx | 22 | 30 | 7 | 3 | 📉 nicht mehr Headline |
| Fabric | 21 | 46 | 73 | 33 | 📈 wachsend |
| AI Builder | 23 | 21 | 4 | 2 | 📉 ersetzt durch Copilot Studio |
| **MCP** | 0 | 0 | 42 | 40 | 🚀 brandneu |
| Code Apps | 1 | 0 | 2 | 11 | 🚀 entsteht 2026 |
| Generative AI | 6 | 26 | 5 | 4 | 📉 (Begriff verschwindet, „Agent" gewinnt) |
| Power Virtual Agents | 34 | 0 | 1 | 0 | ⛔ eingestellt → Copilot Studio |

## Die drei großen Narrative

### Narrativ 1: „Vom Bot zum Agent" (2023 → 2025)

Sequenz erkennbar an den Newsletter-Headlines:

1. **2023, Issue #112ff.**: „Power Virtual Agents Deep Dive" — klassische Bots, Topic-basiert, Q&A.
2. **2023 H2 → 2024 H1**: Renaming. Power Virtual Agents → **Copilot Studio**. Erste Generative-Answer-Features.
3. **2024 H2**: „Autonomous Agents" tauchen auf. Copilot Studio bekommt Tool-Calling, Connectors als Skills, MCP-Vorgänger.
4. **2025**: Computer-using Agents (CUA), Multi-Agent Orchestration, Voice Agents.
5. **2026**: Mistral & Claude Modelle wählbar, Real-Time Voice GA, „Agent Evaluation" als eigene Disziplin.

**Konsequenz für Beratung/Projekte:**
- Wer 2023 mit PVA gestartet hat, muss aktiv migrieren — Newsletter dokumentiert Pfade.
- ALM für Agents (CI/CD, Test) ist 2026 erstmals breit thematisiert — Foundation-Note: James Papadimitriou, Issue #267.
- Voice-Agent-Governance (Eskalation, Recording, Compliance) wird Q2 2026 zum Thema (Issue #265).

### Narrativ 2: „Daten dorthin, wo die Agenten sind" (2024 → heute)

- **Dataverse** wird ab 2024 explizit als „Agent Data Platform" positioniert (Julie Koesmarno, Issue #263).
- **Microsoft Fabric** wächst stetig (21 → 46 → 73), Brückenkopf zu Power BI.
- **MCP (Model Context Protocol)** ist 2025 aus dem Nichts aufgetaucht und etabliert sich als Standard:
  - Dataverse MCP Server
  - Power Apps MCP Server (closed-loop learning, Issue #264)
  - Snowflake-managed MCP Server (Issue #265)
  - Dataverse-Plugin im **Claude Marketplace** (!) (Issue #263)
- **Mistral** als Modell-Option in Copilot Studio (Issue #266) — Microsoft öffnet die Modell-Wahl bewusst.

**Konsequenz:**
- „Klassische" Connectoren werden weiter relevant bleiben, aber MCP-Server entstehen parallel und sind oft mächtiger.
- Power BI wird durch „Agent Skills" und „Fabric Apps" (Build 2026) selbst zur agentischen Plattform.

### Narrativ 3: „Pro-Code zurück in Low-Code" (2025 → 2026)

- Klassische Power Apps / Power Automate Erwähnungen halbieren sich jedes Jahr.
- Stattdessen: **Code Apps** (Pro-Code in Power Platform), **MCP-Server-Bau**, **PCF Components** weiter dabei (66 Erwähnungen).
- Power Pages bekommt **GitHub Copilot CLI & Claude Code Integration** (GA Juni 2026, Issue #266).
- **Carike Botha** (MVP) im M365 FM Podcast (Issue #267): „Citizen Development blendet sich mit Pro-Software-Engineering".

**Konsequenz:**
- Für Beratung wichtig: das Skillprofil verschiebt sich Richtung Hybrid. JS/TS, Python (für MCP-Server), und PowerFx parallel.

## Zeitliche Klammern / „Was passierte wann?"

| Datum | Issue | Highlight |
|---|---|---|
| 2023-01-16 | #112 | ChatGPT-Plugin-Experiment, Power Virtual Agents als Hauptthema |
| 2024-Q1 | ~#170 | Copilot Studio offizieller Name, AI Builder im Hintergrund |
| 2024-Q4 | ~#205 | Erste „Autonomous Agents" Erwähnungen |
| 2025-Q1 | ~#215 | MCP taucht erstmals auf |
| 2025-Q3 | ~#235 | Multi-Agent + Real-Time Voice Previews |
| 2026-04 | #258 | Power Fx UDF/UDT GA |
| 2026-05 | #263 | Dataverse als Agent Data Platform offiziell |
| 2026-05 | #264 | Dataverse Admin Skills (dv-admin) Preview |
| 2026-05 | #266 | Mistral in Copilot Studio + Power Pages CLI GA |
| 2026-06 | #267 | Microsoft Build 2026 Aftermath, Agent Skills für Power BI |

## Was beobachten wir gerade live?

> Auswertungen aus Issue #267 vom 8. Juni 2026 (aktuellste Ausgabe):

- **Microsoft Build 2026** war die letzte Woche. Klassisches Book of News durch „Microsoft Build 2026 Live" ersetzt.
- **Build Highlights**: Agent Skills für Power BI, Fabric Apps für Semantic Models.
- **„Stairway to Dataverse Heaven"** (Angeliki Patsiavou) — Dataverse als Knowledge Source vs. Connector vs. MCP Server. → Vermutlich kommende Architektur-Referenz.
- **Agent Evaluation** in Copilot Studio (Vivian Voss) — Test-Disziplin entsteht.
- **Code Apps Juni 2026**: Mobile Play, CLI-Connection-Creation (Dennis Chi).

## Querverweise

- Releases im Detail → [[05-releases-2026]]
- Tiefenanalyse Copilot Studio → [[06-copilot-studio-agents]]
- Power BI / Fabric Bewegungen → [[07-power-bi-fabric]]
- Dataverse + MCP → [[08-dataverse-mcp]]
- Top-Personen hinter den Trends → [[02-top-personen-mvps]]
