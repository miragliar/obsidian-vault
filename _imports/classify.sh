#!/usr/bin/env bash
# Classify each conversation into a cluster based on title + first messages.
# Produces _imports/manifest.json with one entry per conversation.
# Pure jq/bash, no LLM calls.

set -euo pipefail
EXPORT="${1:-/Users/raouleliasmiraglia/Downloads/data-748e8622-99b9-47c9-a862-42418badafb9-1780294569-dfab5eca-batch-0000/conversations.json}"
OUT="$(dirname "$0")/manifest.json"

# Extract: uuid, name, updated_at, msg_count, first 600 chars of human-text (lowercased) for classification
jq -r '
  [
    .[] | select(.chat_messages|length>0) | {
      uuid,
      name,
      updated_at,
      created_at,
      msg_count: (.chat_messages|length),
      total_chars: ([.chat_messages[].text // "" | length] | add),
      blob: (
        (.name // "") + " " +
        ([.chat_messages[] | select(.sender=="human") | (.text // "")] | join(" "))[0:1500]
      ) | ascii_downcase
    }
  ]
' "$EXPORT" > "$OUT.tmp"

# Cluster assignment (priority order – first match wins)
python3 - "$OUT.tmp" "$OUT" <<'PY'
import json, re, sys

src, dst = sys.argv[1], sys.argv[2]
with open(src) as f:
    convs = json.load(f)

# Cluster rules: (cluster_id, regex over blob)
RULES = [
    # Privates / Smalltalk / Persönliches – ÜBERSPRINGEN
    ("privat", r"\b(motivationsschreiben|spontanbewerbung|anschreiben|geburtstag|kuchen|steuererklärung|behinderungsbedingte|email an frau|nachfrage zur tutoriats|frau sigg|zivildienst|tutoriatsstelle|frau kistler|rechnung|fehlende angaben|lehrbeauftragte|unfallnummer|zahnbehandlung|zahnfüllung|krankenversicherung|krankenversicherungsprämien|netflix|nordeuropa|reise|reisen|reklamation|woodupp|lohntabelle|persönliche einordnung|putzroutine|maschinentiefenreiniger|haltbarkeit|karriereempfehlung|lehrdiplom|master und lehrdiplom|praktikum 1 und 2|abrissfraktur|processus styloideus|schwindel|desensibilisierung|italienische sätze|stellenanzahl|english language|verfügbarkeit für zusammenarbeit|bewerbung abgelehnt|feedback zur abgabe|besuch in der klasse|nachsorge- und sozialberatung|bewerbung als lehrbeauftragte|nachfrage bei bewerbung|lernplan für prüfung am 26)\b"),
    # Anneliese Michel – Seminararbeit
    ("anneliese-michel", r"\b(anneliese|michel|exorzismus|besessenheit|ney-hellmuth|catholic exorcism|goodman|serena bindi|katholisch.*exorzismus)\b"),
    # Working Poor & Gesundheit/Sozialarbeit (Gruppenarbeit + verwandte Themen)
    ("working-poor", r"\b(working poor|okp|leistungskatalog|gesundheitskapitel|gesundheitsversorgung|gesundheitliche ungleichheiten|healthcare access|healthcare.*geneva|fallvertiefung|ukrainische juristin|arbeitsintegration|heilsarmee|jugend und soziale probleme|psychosoziale versorgung|gesundheit.*schweiz|kapitel 4)\b"),
    # Organizational Economics
    ("org-economics", r"\b(organizational economics|org\. economics|economics fundamentals|paper analyses|lernplan für prüfung am 19|deriving with respect to p|randomisierung.*omitted|omitted variable bias|principal.*agent|moral hazard|adverse selection)\b"),
    # Ägyptologie  (no trailing \b so suffixes match: pharaonische, persönlichkeiten)
    ("aegyptologie", r"\b(pharao|osiris|ägyptolog|aegyptolog|hieroglyph|persönlichkeiten|altes ägypten|altägypt)"),
    # Bourdieu / Theorie / Ethik / Religion (analytisch)
    ("bourdieu-theorie", r"\b(bourdieu|habitus|religionsökonomie|moral und ethik|ethik als werkzeug|ethics of the act|luhmann|moralbegriff|frauenemanzipat|textanalyse.*perspektive|soziale rollen|religiosität|muslime|serena bindi|bindis artikel)\b"),
    # Power Platform – breiteres Match
    ("power-platform", r"\b(power apps|power automate|powerfx|power fx|power-?fx|dataverse|\bflow\b|m365|copilot|telemarketing-app|power platform|power-?app|gallery|lookup-?feld|powerapps|environment variable|dax-?abfrage|deklaration|archivierungslogik|wöchentliche erinnerung|subunternehmer|regieapp|app-?testphase|dokumentenstatus|dokumente typ divers|anhänge.*buchstaben|code-?formel|formelberechnung|wertsubstitution|tabelle environment|leere werte|array-?variable|filter expression|dateipfad|e-mail-filter|listing performance|api request|api response|tage zwischen.*berechnen|offlineprofil|pfad aus ordner|inaktive kunden|word claude add-?in|pdf-?dokument aufteilen|screenshot auflistungen|prozessoptimierung)\b"),
    # R / Statistik / Data
    ("r-statistik", r"\b(r-studio|rstudio|ggplot|base r|bmj dataset|r course|summary statistics|datensatz|tidyverse|dplyr|importing.*validating|sparse values|patient characteristics|rounding displayed|x and y axis|polygon with six)\b"),
    # Wiss. Schreiben
    ("wiss-schreiben", r"\b(zitation|zitate|literaturverzeichnis|kohärenz|argumentation|wissenschaftliche formulierung|seminararbeit|quellenkritik|quellen im film|paper discussion|wissenschaftliche arbeiten|volume in wissenschaftlichen|argumentative congruence|ewa-assessment|studienmethodik|bindi|wissenschaftliche.*formulierung|überprüfung.*argumentation)\b"),
    # Video / Media Production
    ("video-media", r"\b(davinci|voice-?over|talking head|filmage|zoom-?effekt|video-?feedback|videoprojekt|disposition.*video|science to public|bild- und videogenerierung|videobeitrag)\b"),
    # Text-Formatting / Unicode
    ("text-formatting", r"\b(subscript|superscript|chemical notation|text transformation|unicode|sonderzeichen)\b"),
    # Claude / Obsidian / KI-Meta
    ("claude-meta", r"\b(claude-?projekt|custom ai|prompt|chat gpt entwicklung|obsidian|claude team|screen sharing|gedächtnis aktualisiert|summarize|zusammenfassungsbot|von grund auf neu|local server|zusammenfassungen erstellen|notizen vorbereiten|notizen im hintergrund|notizen auflisten|ki-antworten|cas ki|cas.*unterricht|onenote)\b"),
]

# Manual overrides for the remaining named conversations the rules don't catch
MANUAL = {
    "7168948c-3faa-41d2-abf1-7c6124bd9495": "org-economics",     # Deriving with respect to p1
    "366ff44f-70a3-4e59-9042-080740e9f0d9": "r-statistik",        # Paper summary for R coding homework
    "eaee47ae-5ef8-4539-8ab2-2ab2bebd9162": "claude-meta",        # Code extraction from text
    "74779f30-8453-472d-8a55-2b584a4efe41": "power-platform",     # Subunternehmerprozess
    "de41dbbc-78f9-4ab9-9ad6-635335121aea": "power-platform",     # Pfad aus Ordnervariable extrahieren
    "89ac079f-217e-4cf9-9266-72661f175281": "privat",             # Karriereempfehlungen
    "d93fe569-3f36-4ee4-9a49-a035071b5b5c": "bourdieu-theorie",   # Frauenemanzipation
    "76539b1a-33cd-4e2f-bc7a-1b8bff6ef677": "privat",             # Putzroutinen
    "21852b51-9c5a-40ae-b384-f261f0eb03e2": "privat",             # Arbeitszeit einteilen
    "964b1f42-6bc0-4f4c-98e1-4ab3ee9fc494": "claude-meta",        # Claude-Projekte teilen
    "7c667b6d-d7f1-49b9-81ba-c6288cd114cf": "r-statistik",        # CSV/R Analysis-Tool, code in code-blocks
}

def classify(uuid, blob, name, total_chars):
    if uuid in MANUAL:
        return MANUAL[uuid]
    if not total_chars or total_chars == 0:
        return "empty"
    for cid, rx in RULES:
        if re.search(rx, blob, re.I):
            return cid
    return "unsorted"

out = []
for c in convs:
    cid = classify(c["uuid"], c["blob"], c["name"], c.get("total_chars") or 0)
    out.append({
        "uuid": c["uuid"],
        "name": c["name"] or "(untitled)",
        "updated_at": c["updated_at"],
        "created_at": c["created_at"],
        "msgs": c["msg_count"],
        "chars": c.get("total_chars") or 0,
        "cluster": cid,
    })

with open(dst, "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

# Print distribution
from collections import Counter
dist = Counter(o["cluster"] for o in out)
for cid, n in dist.most_common():
    print(f"{cid:25s} {n}")
print(f"{'TOTAL':25s} {len(out)}")
PY

rm -f "$OUT.tmp"
echo "Manifest written to $OUT"
