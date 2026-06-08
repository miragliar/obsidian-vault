---
created: 2026-06-08
source: PP Weekly Issues #112–#267
tags: [power-platform, news, dataverse, mcp, connector, integration]
---

# 08 — Dataverse, MCP & Integrations-Strategie

Wie Dataverse sich von einer „Datenbank" zur **Agent Data Platform** entwickelt hat, und warum **MCP (Model Context Protocol)** die wichtigste neue Integrations-Konvention ist.

## Trends in Zahlen

| Begriff | 2023 | 2024 | 2025 | H1 2026 |
|---|---:|---:|---:|---:|
| **Dataverse** | 121 | 119 | 128 | 71 |
| **Connector** | (im Newsletter sporadisch erwähnt) | | | 146 (gesamt) |
| **MCP** | 0 | 0 | **42** | **40** |
| Plugin | (eher Dynamics) | | | 100 |

→ **MCP ist die explosionsartigste neue Technologie** im gesamten Newsletter-Korpus.

## Was ist MCP überhaupt?

**Model Context Protocol** — von Anthropic eingeführt, breit von Microsoft adoptiert.
- Standardisierte Schnittstelle zwischen LLM-Agents und Datenquellen.
- Ersetzt nicht Custom Connectors, **ergänzt sie**.
- Erste Erwähnung im Newsletter: Issue #222 (Juni 2025) — Knee-Deep in Tech zu Microsoft Build 2025: „Windows AI Foundry and the new Model Context Protocol".

## Dataverse-Story 2026

### Issue #263 (Mai 2026) — Die zentrale Botschaft

**Julie Koesmarno** (Microsoft, Dataverse Product Lead): „Dataverse is your agent data platform: here's what's new"

Vier große Punkte zusammen:

1. **Business Skills in Public Preview**
2. **Dataverse Plugin im Claude Marketplace** ⭐
   → Microsoft veröffentlicht aktiv in Anthropic's Marketplace = strategische Multi-LLM-Öffnung.
3. **M365 Copilot Integration via Intelligent Semantic Layer**
4. **6× faster Agentic Search Initialization**

### Issue #264 (Mai 2026) — Admin Skills

**Anirudha Bakore**: „Agentic administration: Dataverse Admin Skills (dv-admin) now available in public preview"
- Natürliche Sprache in Coding-Tools für Dataverse-Admin
- Plugin mappt Intent → PAC CLI Commands mit Guardrails
- Settings Management, Bulk Delete, Retention Workflows
- → Admin-Aufgaben werden zu **Prompts** statt Klick-Sequenzen.

### Issue #267 (Juni 2026) — Architekturentscheidung

**Angeliki Patsiavou**: „Stairway to Dataverse Heaven"
- Drei Wege, Daten in einen Agenten zu bringen:
  1. **Dataverse als Knowledge Source** (RAG, Embeddings)
  2. **Dataverse Connector** (klassisch, REST-basiert)
  3. **Dataverse MCP Server**
- Entscheidungsmatrix: Welcher Pfad wann?

> Diese Note werden wir referenzieren, wenn die nächste Architektur-Entscheidung ansteht. **Aufgabe**: Den Original-Artikel im Newsletter-Link verlinken und im Vault verlinken.

## Konkrete MCP-Server, die Microsoft / Community 2025–2026 brachte

| MCP Server | Zweck | Quelle |
|---|---|---|
| **Dataverse MCP** | Datenzugriff für LLM-Agents | #263 (GA), #267 (Stairway-Artikel) |
| **Power Apps MCP** | Agent-Builder + Closed-Loop Learning | #264 |
| **Power Pages MCP** (via Plugin + CLI) | Site-Building per Conversational Workflow | #266 |
| **Dataverse Admin (dv-admin) MCP** | Admin-Aufgaben per Prompt | #264 |
| **Snowflake-managed MCP** | Drittanbieter, Delegated OAuth | #265 |

## Closed-Loop Learning (Power Apps MCP)

**Srihari Srinivasa**, Issue #264:
- Agent-Feed-Corrections (was Benutzer:innen korrigieren) → organisationsweite Verbesserung.
- **Memory-based Optimization**
- **Genetic-Pareto Optimization**
- Use Case: Data Entry Agents, die mit jedem Korrekturlauf besser werden.

**Implikation**: MCP-Server sind nicht statisch. Sie haben „Gedächtnis" und „Lernen". Das ist neu gegenüber klassischen Connectors.

## Snowflake-Integration (#265, Adi Leibowitz)

- Wie verbindet man einen **Snowflake-managed MCP Server** mit Copilot Studio?
- **Delegated OAuth** via Microsoft Entra ID.
- Cortex Agent Prerequisites in Snowflake.
- Manueller OAuth-Flow nötig.
- → Standard-Pattern für Third-Party MCP-Server.

## Custom Human-in-the-Loop (#265, Adi Leibowitz)

- MCP-Workflow wird unterbrochen, geht an menschlichen Approver.
- Routing per Custom Connector.
- Orchestration bleibt im Agent.
- → Wichtig für regulierte Branchen (Finance, Healthcare).

## Klassische Dataverse-Themen (weiterhin relevant)

Auch ohne MCP-Hype bleibt Dataverse als Plattform aktiv:

- **Dataverse Web API** — *Nishant Rana* (Issue #267): „Returning Record Data During Create Using Prefer: return=representation"
- **Pay-as-you-go Billing Policies** — *Rranjit Sekitekin* (Issue #264): Bulk Assignment + Unlinking Pipeline
- **Plugins** — weiterhin core, oft Temmy Wahyu Raharjo, Nishant Rana, Diana Birkelbach

## Entscheidungsrahmen: Connector vs MCP vs Knowledge Source

**Anlehnung an Angeliki Patsiavou's „Stairway":**

### Knowledge Source (RAG)
- Wenn Inhalte **textuell, lesbar, citation-fähig** sein müssen.
- Beispiel: SharePoint, Confluence, Wikis.
- Power BI Pages, Reports als citations (Lewis Baybutt / Remi Dyon Pattern).

### Connector
- Wenn **strikt strukturiert** (CRUD-Operationen, Transaktionen).
- OAuth-basierte SaaS-Services.
- Power Automate kann den Flow ohne Agent triggern.
- Custom Connector wenn keine MCP-Variante existiert.

### MCP Server
- Wenn der **Agent direkt mit dem System reden** soll, mit eigenem Context.
- Wenn **Closed-Loop Learning** gewünscht ist.
- Wenn **mehrere LLMs** (OpenAI, Claude, Mistral) den gleichen Datenquellen-Pfad nutzen sollen.
- **2026 Default-Wahl** für neue Integrationen.

## Personen, die diesen Bereich treiben

**Microsoft**
- **Julie Koesmarno** ⭐ — Dataverse-Lead
- **Anirudha Bakore** — Admin Skills
- **Srihari Srinivasa** — Power Apps MCP
- **Neeraj Nandwana** — Power Pages Plugin
- **Mark Carrington** — FetchXML / Dataverse-Devs

**Community**
- **Angeliki Patsiavou** ⭐ — Architektur „Stairway to Dataverse Heaven"
- **Adi Leibowitz** ⭐ — Snowflake + Human-in-the-Loop Patterns
- **Nishant Rana** — Web API
- **Temmy Wahyu Raharjo**, **Diana Birkelbach** — Plugins veteran

→ Profile in [[02-top-personen-mvps]].

## Praktische Empfehlungen für unsere Projekte

### Wenn wir 2026 ein neues Integrations-Projekt starten:

1. **Prüfen, ob es einen MCP Server gibt**.
2. Wenn ja: MCP-Route gehen, Delegated OAuth (Entra ID) konfigurieren, Snowflake-Pattern als Vorlage.
3. Wenn nein, aber Connector existiert: klassisch Power Automate + Connector.
4. Wenn nichts: Custom Connector bauen, **gleichzeitig MCP-Server-Bau als Folgeprojekt vormerken**.
5. Bei vertraulichen Daten: **Outbound Access Protection** (Power BI) + **In-Region Modell-Wahl** (Mistral z.B.) berücksichtigen.

### Closed-Loop Learning aktivieren — wann?

- Wenn Endnutzer:innen häufig Agent-Output korrigieren.
- Wenn Daten **Org-spezifisch** sind (Begriffe, Codes, Workflows).
- Wenn der Agent **transaktional** arbeitet (nicht nur Q&A).

## Querverweise

- Copilot Studio + Agents allgemein → [[06-copilot-studio-agents]]
- Power BI + Fabric Verbindung → [[07-power-bi-fabric]]
- Recent Releases → [[05-releases-2026]]
- Personen → [[02-top-personen-mvps]]
