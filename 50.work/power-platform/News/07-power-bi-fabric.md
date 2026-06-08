---
created: 2026-06-08
source: PP Weekly Issues #112–#267
tags: [power-platform, news, power-bi, fabric, semantic-models, dax]
---

# 07 — Power BI & Microsoft Fabric

Power BI ist als Markenname stabil über alle Jahre hinweg, **Fabric** wächst aber stetig dazu. Fokus dieser Note: was sich in den letzten 12 Monaten verändert hat.

## Markenanteile im Newsletter

| Begriff | 2023 | 2024 | 2025 | H1 2026 |
|---|---:|---:|---:|---:|
| Power BI | 129 | 148 | 141 | 44 |
| Fabric | 21 | 46 | 73 | 33 |

→ Fabric explodiert in 2024/2025. Power BI bleibt stabil, ist aber zunehmend „inside Fabric".

## Themen-Schwerpunkte 2026

### 1. Agentic Analytics (Build 2026 Headline)

**Sujata Narayana**, Issue #267:
- **Agent Skills für Power BI** — Build 2026 angekündigt.
- **Fabric Apps für Semantic Models** — Apps können semantische Modelle bauen/deployen.
- AI-Agent unterstützt End-to-End: Rohdaten → semantisches Modell → App.

**Mohammad Ali**, Issue #267:
- „Power BI at Microsoft Build 2026: The Agentic Era of Analytics"
- Roundup für Analyst:innen + Developer.

### 2. DAX User-Defined Functions (Hauptlinie 2026)

- **GA in Issue #267** (Juni 2026), nach Public Preview Anfang 2026.
- *Kay Unkroth* (Microsoft) — wichtigste Stimme dazu.
- Für **Semantic Model Design** ein Meilenstein: Wiederverwendung von Logik, Maintainability.

### 3. Copilot in Power BI

- **Copilot in Web Modeling (Preview)** — Issue #267, *Jacinda Eng*
- AI-Assistent baut Semantic Models per natürlicher Sprache.
- → Verlängerung des „Agentic"-Themas auch in die Modeling-Erfahrung.

### 4. Sicherheit / Governance

- **Outbound Access Protection für Semantic Models (Preview)** — Issue #265, *Kay Unkroth*
- Standardmäßig **block external traffic**, allow-list für Trusted Destinations.
- **Power BI Tenant Migration Guide** — Issue #265, *Winnie Li*
  - Risiken, Dependencies, Sequencing für Enterprise-Migrations.

### 5. DAX & API-Erweiterungen

- **Execute DAX Queries REST API (Preview)** — Issue #263, *Kay Unkroth*
- **Apache Arrow IPC Format** als Output.
- Keine fixe Row-Limits, mehrere EVALUATE-Statements pro Request.
- → Wichtige Brücke zu **Pro-Code Analytics**.

### 6. Power Query Refresh

- **New Power Query Experience in Power BI Desktop (Preview)** — Issue #265
- *Sara Lammini Rodriguez* + *Miguel Escobar*
- Streamlined Data Preparation Flow.

### 7. Semantic Model UX

- **Semantic Model Settings Pane (Preview)** — Issue #263, *Kay Unkroth*
- Redesigned in-context Side Pane, kein Full-Page-Navigieren mehr.
- Collapsible Sections + Search.

### 8. Monthly Feature Summaries

- **Katie Murray** (Microsoft) — Monthly Power BI Feature Summary
- Regelmäßig im Newsletter referenziert. Mai 2026 (#265) etc.

## Microsoft Fabric — was im Newsletter auftaucht

- **MLflow Registry in Fabric** — Issue #266 via Fabric Architecture Podcast
  - Vier-Schicht-Registry-Modell, PREDICT vs Model Endpoints, Direct Lake Prediction Loop
  - Frage: ersetzt Fabric MLflow Azure ML?
- **Fabric IQ** (siehe Microsoft Mechanics Podcast #262)
  - Business Ontology aus Power BI Semantic Model generieren
  - Real-time operational signals + business rules
- **Direct Lake** — sehr oft erwähnt (30 Erwähnungen)
  - Brücke zwischen Lakehouse und Power BI ohne Import
- **Data Warehouse, Real-Time Intelligence, Data Factory** — November 2025 Feature Summary Part 3 (BIFocal #246)
- **Azure Key Vault Integration in Fabric** — landete Anfang 2025 (Knee-Deep in Tech #219)

## Personen, die Power BI / Fabric tragen

**Microsoft Product Team**
- **Kay Unkroth** ⭐ — Semantic Models, DAX. Hauptstimme der letzten 12 Monate (3+ Releases).
- **Katie Murray** — Monthly Feature Summaries.
- **Jacinda Eng** — Copilot in Web Modeling.
- **Sara Lammini Rodriguez**, **Miguel Escobar** — Power Query.
- **Sujata Narayana**, **Mohammad Ali** — Build 2026 Storytelling.

**Community**
- **Winnie Li** — Enterprise Tenant Migration.
- **BIFocal Hosts (John & Jason)** — Wöchentlicher Review aller PBI/Fabric Changes.
- **Simon Sabin** — SQL Bits Organisator, oft Gast in Figuring Out Fabric.

## Praktische Hinweise

### Migration aus klassischem Power BI Service nach Fabric

- Newsletter zeigt: Migration ist **kein Big-Bang**.
- Capacity-Modell, Workspace-Layout, Semantic Models müssen schrittweise umziehen.
- Direct Lake ist die wichtigste Brücke — keine Import-Datasets mehr nötig.
- Outbound Access Protection (#265) sollte **vor** Migration konfiguriert werden.

### DAX 2026 Best Practices

- UDFs nutzen für wiederkehrende Berechnungen → bessere Wartbarkeit.
- UDTs (auch GA in Q2 2026, siehe Power Fx — gleiche Idee) für strukturierte Records.
- REST API für **automatisierte Tests** der semantischen Modelle einsetzen.

### Agentic Analytics — wo stehen wir?

- Stand Juni 2026: **Build-Preview** für Agent Skills + Fabric Apps.
- Kein GA-Datum kommuniziert.
- → Bis dahin: klassisches Semantic Model + Copilot Studio Agent als Add-on.

## Querverweise

- Build 2026 + andere Releases → [[05-releases-2026]]
- Copilot Studio Verzahnung → [[06-copilot-studio-agents]]
- Dataverse als „Semantic Layer" zu Copilot → [[08-dataverse-mcp]]
- BIFocal & andere Podcasts → [[03-podcasts]]
