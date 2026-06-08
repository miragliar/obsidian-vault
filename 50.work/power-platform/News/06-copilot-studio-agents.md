---
created: 2026-06-08
source: PP Weekly Issues #112–#267
tags: [power-platform, news, copilot, copilot-studio, agents, ai]
---

# 06 — Copilot Studio & Agent-Plattform

Tiefenanalyse des **dominantesten Themas** der letzten 3 Jahre. Copilot Studio hat sich von Power Virtual Agents zum **zentralen Agenten-Konstruktor** der gesamten Microsoft-BizApps-Welt entwickelt.

## Die Evolution (2023 → 2026)

### Phase 1 — Power Virtual Agents (2023)
- **34 Erwähnungen** in 2023, **0** in 2024.
- Klassische Bots, Topic-basiert, Q&A-Style.
- Hauptautorin früher: **Dian Taylor** mit „Question Options Deep Dive" Serie.
- Limitation: regelbasiert, kein generatives Verständnis.

### Phase 2 — Renaming + Generative Answers (2024)
- Power Virtual Agents → **Copilot Studio**.
- 59 Erwähnungen in 2024 (war 6 in 2023).
- Erste **Generative Answers** ohne explizite Topics.

### Phase 3 — Agentic Era (2025) ⭐
- **175 Erwähnungen** in 2025 (Verdreifachung).
- „Agent" als Begriff explodiert: **290 Erwähnungen** in 2025 (51 in 2024).
- Multi-Agent Orchestration, Tool Calling, Connectors als Skills.
- Public Previews für Voice und Computer-Using Agents.

### Phase 4 — Production-Ready (2026 H1)
- **133 Erwähnungen in nur 6 Monaten** = on track für ~270 (überholt 2025).
- GA-Welle:
  - **Computer-Using Agents (CUA) GA** (#266, Mai 2026)
  - **Real-Time Voice GA** mit Governance Framework (#265)
  - **Mistral als zusätzliches Modell** (#266)
- ALM, Evaluation, Voice-Governance werden eigene Disziplinen.

## Wesentliche Konzepte (Stand Mitte 2026)

### Computer-Using Agents (CUA)
- **Was?** Agent, der GUI bedient, klickt, scrollt — wie ein Mensch.
- **GA Mai 2026.**
- Use Case: Legacy-System ohne API.
- Risiko: Governance — was darf der Agent „klicken"?

### Real-Time Voice Agents
- **Was?** Synchrones Voice Interface, Latenz unter 1 Sekunde.
- **GA Mai 2026** + Governance Framework.
- Use Cases: Customer Service, Phone-Based Banking, Voice-First Triage.
- Microsoft Copilot Studio Team (#265): „Escalation Design, Security Controls, Monitoring, Compliance Readiness for production-scale deployments."

### Multi-Modell-Strategie
- Bis 2025: nur OpenAI-Modelle in Copilot Studio.
- **Mai 2026 (#266):** Mistral Medium 3.5 verfügbar.
- → Modell-Wahl pro Agent. Strategische Achse: **Kosten + In-Region-Data-Control + Multilingual Performance**.

### Agent Skills / Tools
- Connector-Calls werden zu „Skills" eines Agents.
- Bestehende Power Automate Flows können als Skill registriert werden.
- **MCP (Model Context Protocol)** wird neuer Standardpfad — siehe [[08-dataverse-mcp]].

### Closed-Loop Learning (Power Apps MCP Server)
- Issue #264, Srihari Srinivasa.
- Agent-Feed-Corrections werden in Org-weite Modell-Verbesserungen umgewandelt.
- Memory-based + **Genetic-Pareto Optimization**.
- → Implikation: Agents werden mit jeder Korrektur besser, ohne Re-Training durch IT.

### Human-in-the-Loop Patterns
- Issue #265, Adi Leibowitz.
- Custom Connector route Workflow-Schritte für menschliche Validierung.
- Orchestration bleibt im Agent — Mensch ist „Approver", nicht „Operator".

## ALM für Agenten — neu in Q2 2026

**James Papadimitriou** (Issue #267): „ALM for Copilot Studio Agents — The Foundation"
- **Environment-Strategie** für Agenten (Dev / Test / Prod analog Power Platform).
- **Deployment-Confidence**: was muss vor Produktivsetzung gemessen werden?
- **Governance** über Environments.

**Vivian Voss** (Issue #267): „Agent Evaluation in Copilot Studio"
- Test Sets aufbauen.
- Integration mit **Copilot Studio Kit** + **Playwright** (UI Testing).
- → Test-Disziplin entsteht analog zu klassischer Software-QA.

**Craig White** (Issue #267): „Copilot Studio Evaluations" — komplementäre Sicht.

## Schlüssel-Releases Copilot Studio H1 2026

| Issue | Datum | Was | Status |
|---|---|---|---|
| #263 | 2026-05-11 | Dataverse-Plugin im Claude Marketplace | Live |
| #263 | 2026-05-11 | M365 Copilot Integration via Semantic Layer | Live |
| #264 | 2026-05-18 | Power Apps MCP Server Closed-Loop Learning | GA |
| #264 | 2026-05-18 | Copilot Studio April Roundup (Governance/Workflows) | Live |
| #265 | 2026-05-25 | Snowflake-managed MCP Server | Pattern |
| #265 | 2026-05-25 | Custom Human-in-the-loop Pattern | Pattern |
| #265 | 2026-05-25 | Real-Time Voice Governance | GA |
| #266 | 2026-06-01 | Computer-Using Agents | GA |
| #266 | 2026-06-01 | Workflows Experience redesign | GA |
| #266 | 2026-06-01 | Mistral Medium 3.5 | Verfügbar |
| #267 | 2026-06-08 | ALM Foundation (Article) | Practice |
| #267 | 2026-06-08 | Agent Evaluation (Article) | Practice |
| #267 | 2026-06-08 | Page-Level PDF Citations | Live |

## Personen, die diesen Bereich treiben

**Microsoft-intern**
- **Julie Koesmarno** — Dataverse Product Lead, „Dataverse als Agent Data Platform" Botschaft
- **Nitasha Chopra** — Copilot Studio Monthly Roundups
- **Microsoft Copilot Studio Team** (kollektiv) — Voice Governance Guide
- **Ben Appleby** — Mistral Integration

**Community / MVPs**
- **James Papadimitriou** — ALM für Agents
- **Vivian Voss** — Agent Evaluation
- **Craig White** — Evaluations
- **Adi Leibowitz** — MCP + Human-in-the-Loop Patterns
- **Lewis Baybutt, Remi Dyon** — Citations, Power Pages Integration
- **Angeliki Patsiavou** — Architekturentscheidung Dataverse vs MCP vs Connector
- **Jukka Niiranen** — Reality Checks (häufig kritisch zu „production-ready" Aussagen)
- **Mikko Koskinen** (MVP, Copilot Studio) — Voices of the Neighborhood Episode
- **Heather Orta-Olmo** — Low Code Approach Podcast zu Workflows Agent + Agent Flows

→ Vollständige Profile in [[02-top-personen-mvps]].

## Praktische Anwendungs-Heuristiken (was wir daraus mitnehmen)

### Wenn ich einen Copilot Studio Agent baue 2026…

1. **Modell-Wahl bewusst treffen** — OpenAI default, Mistral wenn Multilingual oder Kostenargument.
2. **MCP first** für Dateninteg­ration. Custom Connector nur wenn MCP nicht verfügbar.
3. **Closed-loop Learning aktivieren** wenn Agent Daten korrigieren kann (Power Apps MCP).
4. **Voice nur mit Governance-Framework** — Eskalation, Compliance, Recording-Strategie.
5. **Agent Evaluation Setup von Anfang an** — Test Sets, Playwright für UI-Flows.
6. **ALM strikt** — Dev/Test/Prod Environments, kein direkter Live-Edit.
7. **Citations sichtbar** — Page-Level PDF Citations sind seit #267 verfügbar, das schafft Trust.

### Warnsignale aus dem Newsletter

- Jukka Niiranen's Reality Checks (im Boost Podcast erwähnt): „Production-ready" Aussagen kritisch prüfen.
- Agent-Drift: Modell-Updates können bestehende Test Sets brechen → Versioning der Evaluation Suite nötig.
- Pay-as-you-go-Kosten skalieren mit Agent-Calls → Bulk-Billing-Pattern (Rranjit Sekitekin, #264).

## Querverweise

- Releases im Detail → [[05-releases-2026]]
- Dataverse als Agent Data Platform → [[08-dataverse-mcp]]
- Power BI Agent Skills (Build 2026) → [[07-power-bi-fabric]]
- Personen → [[02-top-personen-mvps]]
