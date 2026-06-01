---
source: claude-import
imported: 2026-06-01
conv_uuids: [ee352a3f-cd81-409b-9f99-27ec69ebf9a7, 964b1f42-6bc0-4f4c-98e1-4ab3ee9fc494, a5d3a52d-c279-40f9-93b7-8b04f05e1d5e, 04fe91f9-d60b-40ec-afd8-8351f5863313, 6a42a0fc-b1f6-4047-b124-7a63f8862931, 998e87ca-3a28-4e48-8665-4030c290d8b1, 216711ea-0186-450f-b2f3-00a98b8924ed, dd6048ab-937d-49a8-b9f1-2b006832a53f, 58f34535-ad93-4069-9569-188001042e23]
tags: [claude, projects, custom-ai, knowledge, sharing, team, obsidian]
---

# Claude Projects & Custom AI — Setup und Teilen

Verdichtete Notizen zu Claude Projects, Custom AI mit Kontext, Team-Lizenzierung und dem Übergang zwischen Sessions.

## Claude Projects — Use Cases

Ein **Projekt** ist ein Container für mehrere Conversations + persistente Knowledge Base. Im Datenexport sichtbar als 7 Projekte:

- Wissenschaftliche Arbeiten
- How to use Claude
- Zusammenfassung
- Wiss. Mitarbeiter
- Org. Economics
- SA – Anneliese Michel (20 Docs)
- Gesundheit working poor (8 Docs)

**Sinnvoller Schnitt:** ein Projekt pro Forschungs-/Arbeits-Thread mit eigener Quellen-Sammlung. Nicht: ein Mega-Projekt für „alles Studium".

## Knowledge Base — was reinkommt

| Was | Beispiel | Begründung |
|---|---|---|
| **Quellen-PDFs** | Burla 2025, Ney-Hellmuth 2014 | Wiederholtes Zitieren, Quellenkritik |
| **Eigene Notizen** | Filmnotizen, Disposition | Kontext für Folgegespräche |
| **Vorlesungs-ZF** | PDF der Sitzungs-ZF | Cross-Topic-Verbindungen |
| **Beispiele eigener Schreibe** | bisherige Kapitel | KI lernt Stil & Vokabular |
| **Glossare / Definitionen** | Eigenes Begriffslexikon | Konsistenz über Konversationen |
| **Anti-Beispiele** | „so NICHT formulieren" | Negativ-Steuerung |

**Was nicht reingehört:**
- Veraltete Versionen (verwirrt die KI)
- Sehr lange Bücher (Vision/Token-Budget)
- Privates (s. [[40.meta/Claude-Workflows]])

## Custom Instructions pro Projekt

Wirkungsvolle Bausteine:

```
Du bist Co-Autor für [Projekt-Titel]. Sprache: Schweizer
Standarddeutsch (ss statt ß). Stil: wissenschaftlich-präzise,
keine Em-Dashes. Bei Quellenangaben Format: (Autor, Jahr, S. X).

Bevor du eine inhaltliche Aussage triffst, prüfe gegen die
Knowledge-Base. Wenn etwas nicht belegt ist, sag es klar.

Wenn ich dir Screenshots schicke, gib die Zusammenfassung
im Stichwort-Stil pro Seite zurück (s. dokumentenanalyse-Pattern).
```

→ Vermeidet die häufigsten Stil-Drifts in jeder neuen Conversation.

## Custom AI mit spezifischem Kontext

Drei Ebenen:

| Ebene | Tool | Wann |
|---|---|---|
| **Pro-Conversation** | Custom Instructions oben einbauen | Einmalige Aufgabe |
| **Pro-Projekt** | Claude-Project Settings | Wiederkehrendes Thema |
| **Pro-Organisation** | Claude Teams / Enterprise | Geteilte Standards in einer Gruppe |

## Claude Team — Lizenzanforderungen (Stand 2025/2026)

- Mindestens **5 Seats** für Team-Plan
- Pro Seat eigener Login
- Shared Projects unter den Seats teilbar
- Knowledge-Base in geteilten Projekten von allen Mitgliedern lesbar/erweiterbar
- Admin-Console für Berechtigungen

→ Für Einzelnutzung **nicht** sinnvoll; ab Gruppen-/Kunden-Arbeit (Miraglia BI) sehr wohl.

## Claude-Projekte teilen

**Status (2025/2026):** Direktes Teilen einzelner Projekte zwischen Free/Pro-Accounts ist **nicht** möglich. Optionen:

1. **Team-Plan** mit gemeinsamen Seats → Projekt geteilt
2. **Workaround:** Custom Instructions + Knowledge-Base-PDFs exportieren und beim Empfänger im eigenen Projekt importieren
3. **Conversation teilen** als Link (read-only) — keine echte Co-Arbeit, aber Wissensübergabe möglich

## „Gedächtnis aktualisiert" — wann es ausgelöst wird

Claude markiert manche Aussagen mit „Gedächtnis aktualisiert":

- Bei expliziten Präferenzen („Ich bevorzuge X")
- Bei wiederkehrenden Stil-Anforderungen
- Bei Identitäts-/Rollenangaben

Nur in **Memory-fähigen Plänen** (Pro/Team). Es lohnt sich, **gezielt zu instruieren**: „Merk dir, dass ich Em-Dashes vermeide" — das setzt eine persistente Note, statt jedes Mal neu erklären zu müssen.

## Übergabe zwischen Sessions („von Grund auf neu beginnen")

Wenn eine Conversation zu lang wird (Token-Budget) oder ein neuer Chat sauberer wäre:

**Pattern:** „Übergabe-Prompt" am Ende der alten Session:

> Fasse für mich in 200–300 Wörtern den aktuellen Stand zusammen:
> - Worum geht es?
> - Was wurde entschieden?
> - Welche offenen Fragen / Aufgaben sind als nächstes dran?
> - Welche Quellen werden referenziert?
>
> Schreib es so, dass ich es in eine neue Conversation als Kontext-Prompt einfügen kann.

→ Resultat 1:1 als ersten Prompt im neuen Chat verwenden. Continuity ist überraschend gut.

## Lokaler Server / MCP Integration (Stand Mai/Juni 2026)

Conv „Local server configuration" und „Obsidian-Vault Notizen auflisten" zeigen: Lokale Tools (MCP, Obsidian-Plugins) sind via Konfigurationsdatei (`settings.json`, Bearer-Token) anschließbar. Pattern:

```
claude mcp add --transport http <name> http://localhost:<port>/mcp \
  --header "Authorization: Bearer <token>"
```

→ Verbindet Claude direkt mit lokalem Obsidian-Vault o.ä. Bedingung: lokaler Server läuft + Token gültig.

## Zusammenfassungs-Bot für Vorlesungen (Pattern)

Häufige Frage: "Wie nutze ich Claude als Zusammenfassungs-Bot für eine Vorlesung mit Übungen?"

**Setup:**

1. Projekt anlegen: „Vorlesung X HS26"
2. Knowledge-Base: Folien jeder Sitzung + Übungsblätter + eigene Notizen
3. Custom Instructions: Stil (s.o.), Notations-Konvention für ZF
4. Pro Sitzung: ZF im etablierten Format, dann Übungs-Lösung im Anschluss
5. Vor Klausur: Cross-Topic-Quiz aus Knowledge-Base (siehe [[20.studies/Organizational-Economics/lernstrategie-pruefung-19-juni]])

## Verwandt

- [[40.meta/dokumentenanalyse-vorlesung-zusammenfassen]]
- [[40.meta/prompt-strukturierte-extraktion]]
- [[20.studies/Bourdieu-Theorie/mindmap-religion-ethik-seminar]] — Übergabe-Anleitung für KI
- [[40.meta/_conversation-index]]
