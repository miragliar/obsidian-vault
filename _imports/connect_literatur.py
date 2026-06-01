#!/usr/bin/env python3
"""connect_literatur.py — Verbindung der Literatur-Notizen."""
import re
from pathlib import Path

LIT = Path("/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/Miraglia-BI/0_Internal/Obsidian Raoul/20.studies/Anneliese-Michel/Literatur")
START = "<!-- connections-start -->"
END = "<!-- connections-end -->"

# Daten als plain ASCII-Strings — keine getrennten Quotes
CONNECTIONS = {
    "Bauer & Doole 2024": {
        "verwandt": [
            ("Wilkens 2019", "auch religionswissenschaftlich anti-essentialistisch, ergänzt um Körperdimension und Religionsästhetik"),
            ("Demmrich 2020", "psychologisches Komplement: Demmrich rezipiert Oesterreich (1921), Bauer/Doole liefern die zeitgenössische anthropologische Theorie"),
            ("Dinzelbacher 1994", "religionsphänomenologisch-kulturhistorischer Hintergrund für die kulturelle Vielfalt der Phänomene"),
        ],
        "bezug": [
            ("Kap. 3.2 Anthropologische Brille", "Moderner Kontrapunkt zu Goodmans biologisch-essentialistischer Position (1980)"),
            ("Kap. 3.3 Religionswiss./kulturpsych.", "Theoretischer Rahmen: 'Besessenheit als kontextuelle Zuschreibung' — Lambek/Boddy/Johnson"),
            ("Einleitung — methodische Prämisse", "Stützt Diskursanalyse als Methode (Besessenheit als Bedeutungs-Zuschreibung, nicht als Phänomen-an-sich)"),
        ],
        "arbeitsnotizen": [
            "[[04-Methodische-Reflexion]] — Bauer/Doole begründet, warum Goodman 1980 als Einzelposition (essentialistisch) behandelt werden muss",
            "[[02-Quellen-und-Positionen]] — als zeitgenössische religionswiss./anthropologische Quelle in der Übersicht eintragen",
        ],
    },
    "Demmrich 2020": {
        "verwandt": [
            ("Wilkens 2019", "beide arbeiten mit Körperdimension; McCloud (bei Wilkens) parallelisiert Oesterreich-Phänomenologie"),
            ("Bauer & Doole 2024", "anthropologische Theorie ergänzt religionspsychologische Befunde — Demmrich erklärt das 'Wie', Bauer/Doole das 'Was zählt als'"),
            ("Leimgruber 2010", "gemeinsame Anwendung auf Anneliese; Leimgruber theologisch, Demmrich religionspsychologisch"),
            ("Niemann 1999", "Mischo-Parapsychologie-Erbe: Niemann verweist auf Mischo (Freiburg), Demmrich rezipiert Oesterreich-Linie"),
        ],
        "bezug": [
            ("Kap. 3.1 Psychiatrisch-psychologisch", "Oesterreichs vier Symptome auf Anneliese angewendet (Magersucht, fremdsuggestive Induktion, kulturpsychologisch verstärkt)"),
            ("Kap. 3.3 Religionswiss./kulturpsych.", "Kulturpsychologische Erklärung des weltweiten Exorzismus-Anstiegs (Demmrich S. 79)"),
            ("Kap. 4 Mediale Rezeption (sekundär)", "Demmrich: 'Tageszeitungen berichten' — Verbindung zwischen Boulevard-Diskurs und Praxis"),
        ],
        "arbeitsnotizen": [
            "[[02-Quellen-und-Positionen]] — Pflicht-Fußnote: Demmrich ist Rezeption von Oesterreich 1921 (siehe Formulierung in [[05-Schreibwerkstatt-Konsistenz-Zitate]])",
            "[[04-Methodische-Reflexion]] — Demmrich ist keine Anthropologin (anders als Goodman) → relevant für die 'Anthropologische-Brille'-Klarstellung",
        ],
    },
    "Dinzelbacher 1994": {
        "verwandt": [
            ("Müller 2002", "Müller behandelt liturgisch-praktische Folgen, Dinzelbacher die religionsphänomenologische Grundlage"),
            ("Leimgruber 2010", "historische Tiefe für theologische Bewertung; Loudun, Elisabeth v. Ranfaing als Präzedenzfälle"),
            ("Bauer & Doole 2024", "Dinzelbacher liefert die historische Variations-Basis, Bauer/Doole die zeitgenössische theoretische Lesart"),
        ],
        "bezug": [
            ("Einleitung — Hinführung & Relevanz", "Religionshistorische Längsperspektive: Phänomen ist alt, kulturspezifisch ausgeformt"),
            ("Kap. 2 Fallrekonstruktion (Hintergrund)", "Anneliese im Kontext einer langen Tradition (Loudun, Ursulinen)"),
            ("Kap. 3.3 Religionswiss./kulturpsych.", "Religionsphänomenologische Typologie (zentral/peripher, freiwillig/unfreiwillig)"),
        ],
        "arbeitsnotizen": [
            "[[02-Quellen-und-Positionen]] — als Lexikon-/Überblickartikel klar markieren (Sekundärquelle für historischen Kontext)",
        ],
    },
    "Leimgruber 2010": {
        "verwandt": [
            ("Müller 2002", "beide rekonstruieren Anneliese-Fall + Liturgiereform 1999, unterschiedliche Schwerpunkte"),
            ("Niemann 1999", "kritisch-pastoraltheologische Auseinandersetzung mit dem neuen Ritus"),
            ("Niemann 2005", "pastoral-praktische Folge-Position desselben Reform-Diskurses"),
            ("Demmrich 2020", "religionspsychologisches Komplement zur theologischen Fall-Rekonstruktion"),
        ],
        "bezug": [
            ("Kap. 2 Fall-Rekonstruktion", "**Hauptquelle** neben Ney-Hellmuth — biographischer Hintergrund, Krankheitsverlauf, Prozess, Sühnebesessenheit"),
            ("Kap. 3.3 Religionswiss./theol. Brille", "Bewertung des Falls: 'Anliegen pervertiert zugunsten wahnhafter Vorstellungen'"),
            ("Kap. 4 Mediale Nachwirkung", "'Mittlerweile wird sie in gewissen Kreisen bereits in Gebete aufgenommen' — Heiligen-Diskurs"),
        ],
        "arbeitsnotizen": [
            "[[02-Quellen-und-Positionen]] — bereits als Hauptquelle gelistet; Leimgruber 2004/2010 ist die roter-Faden-Quelle für Kap. 2",
            "[[03-Filmanalyse-Requiem-2006]] — Hintergrund für die Borchert-Katharina-Sühnebesessenheits-Verknüpfung in Schmid 2006b",
            "[[05-Schreibwerkstatt-Konsistenz-Zitate]] — Zahlenangaben gegen Ney-Hellmuth abgleichen (z.B. Bewährungsstrafen, Bischof Stangl)",
        ],
    },
    "Müller 2002": {
        "verwandt": [
            ("Leimgruber 2010", "gleicher Untersuchungsgegenstand: Anneliese als Auslöser + 1999er Reform"),
            ("Niemann 1999", "Müller deskriptiv-systematisch zur Reform, Niemann pointiert-kritisch"),
            ("Dinzelbacher 1994", "historische Vorgeschichte der Liturgie (Rituale Romanum 1614)"),
            ("Niemann 2005", "pastoral-praktische Vertiefung der Reform-Diskussion"),
        ],
        "bezug": [
            ("Kap. 3.1 Psychiatrisch-psychologisch", "Hinweis auf 1985er-Empfehlung der Bischofskonferenz: Zusammenarbeit Seelsorge/Psychotherapie/Medizin"),
            ("Kap. 3.3 Religionswiss./theol.", "Liturgiegeschichtliche Tiefe, Kontextualisierung der theologischen Position"),
            ("Kap. 4 Mediale Rezeption", "**Brücke**: Popkultur (*Der Exorzist* 1973, Metal, Okkultwelle 80er) ↔ kirchliche Reform-Reaktion"),
        ],
        "arbeitsnotizen": [
            "[[03-Filmanalyse-Requiem-2006]] — Müllers Popkultur-Analyse (*Exorzist* 1973) ist der diskursive Vorlauf zu Schmid 2006",
            "[[02-Quellen-und-Positionen]] — zentrale theologische Sekundärquelle, in die Übersicht aufnehmen",
        ],
    },
    "Niemann 1999": {
        "verwandt": [
            ("Niemann 2005", "**Folge-Text desselben Autors** — 2005 erweitert um pastoral-praktische Dimension"),
            ("Leimgruber 2010", "gemeinsamer Bezug auf Gemischte Arbeitsgruppe 1984 nach Anneliese-Tod"),
            ("Müller 2002", "gleicher Untersuchungsgegenstand (Reform 1999), unterschiedliche Tonalität"),
        ],
        "bezug": [
            ("Kap. 3.1 Psychiatrisch-psychologisch", "**Mischo-Erbe**: explizite Würdigung von Johannes Mischos parapsychologisch-psychiatrischen Beiträgen für die Gemischte Arbeitsgruppe 1984"),
            ("Kap. 3.3 Religionswiss./theol.", "Vier Kriterien des Rituale Romanum 1614 (kritisch beurteilt)"),
            ("Kap. 5 Synthese", "Rahner-Zitat: 'Wie wir heute ohne Hexen auskommen, so könnte man auch ohne Besessenheit auskommen'"),
        ],
        "arbeitsnotizen": [
            "[[02-Quellen-und-Positionen]] — als kritisch-pastoraltheologische Stimme einordnen",
            "[[05-Schreibwerkstatt-Konsistenz-Zitate]] — Notiz besteht primär aus wörtlichen Exzerpten → Zitierform exakt einhalten",
        ],
    },
    "Niemann 2005": {
        "verwandt": [
            ("Niemann 1999", "**Vortext desselben Autors** — 2005 baut auf 1999er-Position auf"),
            ("Leimgruber 2010", "gemeinsame pastoral-praktische Tendenz (psychiatrische Hilfe + Seelsorge)"),
            ("Müller 2002", "gleicher theologischer Reform-Rahmen, ähnlicher Aktualitäts-Bezug (post-9/11)"),
        ],
        "bezug": [
            ("Kap. 3.1 Psychiatrisch-psychologisch", "Fortsetzung der Mischo-Linie: humanwissenschaftliche Diagnose **vor** theologischer Bewertung"),
            ("Kap. 5 Synthese", "11 Thesen pastoraler Handhabung — programmatischer Schlusspunkt"),
            ("Kap. 4 (Sekundär)", "Post-9/11-Aktualität als Diskurs-Kontextualisierung"),
        ],
        "arbeitsnotizen": [
            "[[02-Quellen-und-Positionen]] — Doppelreferenz-Paar mit Leimgruber laut Notiz-Hinweis prüfen (S. 853)",
            "[[05-Schreibwerkstatt-Konsistenz-Zitate]] — Notiz besteht primär aus wörtlichen Exzerpten",
        ],
    },
    "Wilkens 2019": {
        "verwandt": [
            ("Bauer & Doole 2024", "moderne anti-essentialistische Linie; Wilkens religionsästhetisch-methodisch, Bauer/Doole theoretisch-übersichtsartig"),
            ("Demmrich 2020", "beide arbeiten mit Körperdimension; McCloud bei Wilkens parallelisiert Oesterreichs psychophysische Symptome"),
        ],
        "bezug": [
            ("Kap. 3.2 Anthropologische Brille", "**Kontrapunkt zu Goodman 1980** — religionsästhetischer Zugang statt biologische Konstante"),
            ("Kap. 3.3 Religionswiss./kulturpsych.", "Religionsästhetik als methodischer Zugang; Materialität, Medium, Trance, McCloud/Bourdieu-Habitus"),
            ("Einleitung — Methodik", "Bezug zur Diskursanalyse: Religionsästhetik als komparatistischer Forschungszugang"),
        ],
        "arbeitsnotizen": [
            "[[04-Methodische-Reflexion]] — Wilkens ist **kein** Anthropologe (anders als Goodman) → relevant für die 'Goodman als Einzelposition'-Klarstellung in der Arbeit",
            "[[02-Quellen-und-Positionen]] — bereits gelistet, als Kontrapunkt zu Goodman markieren",
        ],
    },
}


# Mapping Kurzname → tatsächlicher Dateiname (ohne .md)
FILENAMES = {
    "Bauer & Doole 2024": "Bauer & Doole 2024 — Possession as Contextual Ascription",
    "Demmrich 2020": "Demmrich 2020 — Oesterreich-Rezeption & Besessenheitspsychologie",
    "Dinzelbacher 1994": "Dinzelbacher 1994 — Besessenheit (Lexikonartikel, S. 311–314)",
    "Leimgruber 2010": "Leimgruber 2010 — Fall Klingenberg & neuer Exorzismus",
    "Müller 2002": "Müller 2002 — Exorzismus zwischen Popkultur & Liturgiereform",
    "Niemann 1999": "Niemann 1999 — Großer Exorzismus 1999 (Kritik)",
    "Niemann 2005": "Niemann 2005 — Befreiung vom Bösen & Pastorale Hilfen",
    "Wilkens 2019": "Wilkens 2019 — Religionsästhetik, Geister & Materialität",
}


def build_section(conns):
    lines = [START, "", "## Verwandte Literatur", ""]
    for short, why in conns["verwandt"]:
        full = FILENAMES.get(short, short)
        lines.append(f"- [[{full}|{short}]] — {why}")
    lines += ["", "## Bezug zur Seminararbeit", ""]
    for kapitel, was in conns["bezug"]:
        lines.append(f"- **{kapitel}** — {was}")
    if conns.get("arbeitsnotizen"):
        lines += ["", "## Verknüpfung mit Arbeits-Notizen", ""]
        for an in conns["arbeitsnotizen"]:
            lines.append(f"- {an}")
    lines += ["", END]
    return "\n".join(lines)


def patch_note(short_name, conns):
    full = FILENAMES.get(short_name)
    if not full:
        print(f"   ✗ Kein Filename-Mapping: {short_name}")
        return
    f = LIT / f"{full}.md"
    if not f.exists():
        print(f"   ✗ Nicht gefunden: {f.name}")
        return
    txt = f.read_text(encoding="utf-8")
    new_section = build_section(conns)
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pat.search(txt):
        txt = pat.sub(new_section, txt)
    else:
        txt = txt.rstrip() + "\n\n" + new_section + "\n"
    f.write_text(txt, encoding="utf-8")
    print(f"   ✓ {f.name}")


def main():
    print("Connect Literatur-Notizen")
    print("-" * 60)
    for short, conns in CONNECTIONS.items():
        patch_note(short, conns)


if __name__ == "__main__":
    main()
