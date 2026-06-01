---
source: claude-import
imported: 2026-06-01
conv_uuids: [3d2a5a7c-fedd-4502-abfb-e827d508827e, 1389ba6d-6333-4669-b320-a21a116edb5c, ee8fa39c-8695-4e2b-8d63-1203a0e8456b, 9b61a794-23f3-462c-87c8-0b39528d8586, 7883c2a7-73b9-416f-bead-8555a31d2272, 9ca804d0-8655-4b3b-9a3f-bf832d55bfa3]
tags: [claude, prompt, zusammenfassung, vorlesung, screenshot, workflow]
---

# Workflow: Vorlesungs-/Dokumenten-Zusammenfassung per Screenshot-Stream

Wiederkehrendes Pattern: ein PDF oder Buch wird seiten- oder doppelseitenweise als Screenshot an die KI geschickt, die liefert pro Screenshot strukturierte Notizen zurück. Geeignet für Vorlesungsfolien, Sekundärliteratur, Filmhefte, Protokoll-Dokumente.

## Problem

Lange Dokumente (>30 Seiten) komplett hochzuladen ist ineffizient:
- Vision-Modelle verlieren Detail-Treue bei vielen Seiten
- Eigenständige Strukturierung der KI ist nicht steuerbar
- Notation-Stile schwanken pro Antwort

Manuelle Zusammenfassungen dauern zu lange.

## Lösung

**Setup-Prompt (einmalig am Anfang einer Session):**

> Ich werde dir mehrere Screenshots schicken von einem Dokument, welches du lesen musst. Die Seitenzahlen sind entweder unten links oder unten rechts zu sehen.
>
> Halte dich an eine sehr genaue aber auch stichwortartige Zusammenfassung in folgendem Stil:
>
> ```
> S. X
> - Stichpunkt
> - Stichpunkt
>
> S. Y
> - Stichpunkt
> ```
>
> Ich werde dir immer mehrere Seiten gleichzeitig schicken. Gib mir dann den Text im obigen Stil zurück. Am Schluss brauche ich die Notizen für meine wissenschaftliche Arbeit.

**Dann pro Prompt 1–2 Screenshots ohne weiteren Text** → KI liefert die strukturierte Antwort.

## Stil-Varianten je Verwendung

| Verwendung | Stil |
|---|---|
| Eigene Lernzusammenfassung | Stichworte, kurze Halbsätze |
| Material für wissenschaftliche Arbeit | Ganze Sätze, fließend, mit Seitenangabe |
| Filmanalyse (Beobachtungsraster) | Bullets nach Beobachtungsfeldern (siehe [[20.studies/Anneliese-Michel/03-Filmanalyse-Requiem-2006]]) |
| Klausur-Lernkarten | Frage–Antwort-Paare |
| Glossar-Extraktion | Begriffe + Definition + Kontext-Seitenzahl |

## Sequenzprotokoll (bei Filmheften)

Wenn das Dokument ein Filmheft mit Sequenzbeschreibung ist:

> Mach das Sequenzprotokoll bitte ausführlicher und in ganzen Sätzen.

→ schiebt vom Stichwort-Modus in den Fließtext-Modus, ohne den Rest umstellen zu müssen.

## Iteration & Korrekturen

Schwerpunkt-Verschiebungen mid-conversation:

| Wunsch | Prompt |
|---|---|
| Mehr Detail | „Ergänze für die letzten 3 Seiten alle Datums-/Namens-/Zahlangaben." |
| Weniger Detail | „Verdichte die letzten 5 Seiten auf je 3 Stichpunkte." |
| Andere Struktur | „Ordne die Notizen ab S. X neu nach Thema, nicht nach Seite." |
| Querverbindung | „Welche Begriffe von früheren Seiten tauchen hier wieder auf?" |

## Nachbearbeitung

Nach 30+ Seiten Notizen entstehen Doppelungen über Sitzungen. Standard-Nachfrage:

> Vergleiche die ZF von Sitzung 2 mit der von Sitzung 3 und identifiziere, was in 3 fehlt. Gib mir die Kapitelnummer und den ergänzenden Stichpunkt — ich integriere selbst.

→ statt komplett neu zu schreiben, gezielt ergänzen.

## Wann nicht

- **Bei sehr kurzen Dokumenten** (<10 Seiten): direkter Upload + ein einziger Zusammenfassungs-Prompt reicht.
- **Bei reinen Text-PDFs** (durchsuchbar, keine Scans): OCR + Text-Extraktion + direkte Übergabe statt Screenshots. Schneller, vollständiger.
- **Bei sehr kleinem Text in Screenshots:** Vision-Modell verliert Treue. Lieber jeweils nur eine Seite groß.
- **Bei Formel-/Mathematik-lastigen Texten:** Vision-OCR der KI ist fehleranfällig bei Sub-/Superscripts. Lieber LaTeX-Quelle oder ausgedruckte Fotos hoher Qualität.

## Verwandt

- [[40.meta/prompt-strukturierte-extraktion]] — JSON-Extraktion aus Geschäfts-Dokumenten
- [[40.meta/claude-projekte-und-custom-ai]]
- [[20.studies/Anneliese-Michel/03-Filmanalyse-Requiem-2006]] — konkrete Anwendung des Workflows
- [[20.studies/Aegyptologie/01-Quellen-Koenigschronologie]] — konkrete Anwendung
- [[40.meta/_conversation-index]]
