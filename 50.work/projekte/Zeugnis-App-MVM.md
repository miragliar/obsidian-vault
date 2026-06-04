---
name: Zeugnis-App MVM
slug: Zeugnis-App-MVM
klient: MVM AG
klient_link: "[[50.work/26_Firmen/MVM-AG|MVM AG]]"
status: Live + Bugfixes
zeitraum: produktiv (Bestand) — laufende Anpassungen Mai/Juni 2026
kategorie: kunde
tags: [miraglia, projekt, mvm-ag, zeugnis, hr, personal, power-apps]
type: projekt-hub
source: chat-context 2026-06-04 (Personal MVM-Gruppe, 4 Mails 11.05.–03.06.2026)
created: 2026-06-04
---

# Zeugnis-App MVM (Zeugnistool)

**Klient:** [[50.work/26_Firmen/MVM-AG|MVM AG]] · HR-Bereich
**Status:** Live + laufende Bugfixes

> Verwandt mit [[50.work/projekte/Zeugnis-App-Obrist|Zeugnis-Test-App Obrist Interior]]. Beide Tools sind **„Zeugnis-Tools"** für die Verwaltung von Mitarbeiter-Zeugnissen — ob es sich um die gleiche Lösung (multi-tenant) oder zwei eigenständige Implementierungen handelt, ist offen und sollte beim nächsten Touch geklärt werden.

## Worum geht es

Power-Apps-/Dataverse-Lösung bei MVM AG für die HR-seitige Erstellung und Verwaltung von Mitarbeiter-Zeugnissen (insbesondere **Abschlusszeugnisse**). Workflow zwischen **PL (Vorgesetzte)** und **HR (Sachbearbeitung)**, mit Word-Export für finale Aufbereitung.

## Beteiligte

- [[50.work/25_People/Nicole-Lötscher|Nicole Lötscher]] · **Sachbearbeiterin HR** — Anwenderin/Feedback-Geberin (Sammelpostfach `personal@mvm-ag.ch`)
- PL = Führungskräfte (Linien-Vorgesetzte) — geben das Zeugnis frei / erstellen Initialfassung
- HR = finale Bearbeitung, Versand

## Workflow (rekonstruiert)

```
PL erstellt Zeugnis ─► Tool-Status: „in Bearbeitung bei PL"
        │
        ▼
PL gibt frei ──────► Tool-Status: → HR
        │
        ▼
HR bearbeitet ─────► Word-Export → manuelle Feinarbeit
        │
        ▼
HR „verschickt"     (Status soll zurück, bleibt aber „in Bearbeitung bei PL" 🐛)
```

## Bekannte Bugs + offene Anliegen (Mai/Juni 2026)

### 🐛 Status-Bug „in Bearbeitung bei PL" bleibt stehen
- **Mail:** Nicole Lötscher · 2026-05-12
- HR-versandte Zeugnisse zeigen im Tool weiterhin „in Bearbeitung bei PL". HR-Send-Trigger setzt den Status nicht zurück.
- **ToDo:** Trigger-Logik / Status-Übergänge im Dataverse-Workflow prüfen.

### Scharfes S (ß) in Zeugnissen
- **Mail:** Nicole Lötscher · 2026-06-03
- Anforderung: **kein „ß" mehr** in generierten Zeugnissen — Swiss-German-Konvention nutzt „ss".
- Tritt vor allem bei Deutschland-Zeugnissen oder Word-Roundtrips auf.
- **ToDo:** Generation-Step (Template / Power Automate Word-Action / Replace-Logik): `ß → ss` als globale Ersetzung.

### PL-Notification: Link statt nur Text
- **Mail:** Nicole Lötscher · 2026-05-11
- PL erhält aktuell nur einen Text-Hinweis, dass ein Zeugnis zur Bearbeitung bereit liegt. Sie sollten stattdessen einen **klickbaren Link** zum Zeugnistool erhalten.
- **ToDo:** Mail-Template (Power Automate) um Deep-Link zur App / direkt zum betreffenden Zeugnis-Record erweitern.

### Roundtrip Tool ↔ Word
- **Mail:** Nicole Lötscher · 2026-05-27
- Aktuell: Export Tool → Word → manuelle Korrektur. Wunsch: Änderungen im Word direkt zurück ins Tool.
- **Backlog-Diskussion:** Mit Nicole klären, was sie genau braucht. Mögliche Wege: (a) Word-Online-Edit am eingebetteten Doc, (b) JSON-Round-Trip via Strukturierung, (c) Verzicht auf Word-Export und Markup-Editor in der App.

### Hasanovic Hamid pendent
- **Mail:** Nicole Lötscher · 2026-05-15
- Manuelle Umschreibung durch Raoul war OK. „Weitere störende Punkte" folgen separat.

## Generator-Prompt (LLM)

- 🆕 [[50.work/projekte/Zeugnis-App-MVM-prompt|Prompt v2 (2026-06-04)]] — überarbeitete Version mit:
  - Priority Rule 1: **kein „ß" mehr** (Swiss-German de-CH, mit Beispiel-Tabelle + Self-Check)
  - Priority Rule 2: Tense gemäß `Typ` (Zwischen-/Abschluss-)
  - Priority Rule 3: Name/Geschlecht-Ersetzung mit Edge-Cases
  - Explizites JSON-Schema (6 Keys) — vor Einsatz mit Power-Automate-Parser abgleichen
  - Verpflichtende Verification-Checklist vor Output

## Verwandte Pattern-Notizen

- (zukünftig: ß→ss-Replace Belt-and-Suspenders im Flow, Mail-Template Deep-Link)

## Verwandt

- [[50.work/projekte/_Index|Projekt-Index]]
- [[50.work/projekte/Zeugnis-App-Obrist|Zeugnis-Test-App Obrist Interior]] — verwandte Lösung (möglicherweise gleiche Solution)
- [[50.work/26_Firmen/MVM-AG|MVM AG]]
- [[50.work/25_People/Nicole-Lötscher|Nicole Lötscher]]
- [[60.daily/2026-06-04|Tagesnotiz 2026-06-04]] — ToDo #8
