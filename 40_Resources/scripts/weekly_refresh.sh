#!/bin/zsh
# Wöchentlicher M365 → Obsidian Refresh (deterministischer Teil) + Gap-Report.
# Wird per launchd ausgeführt. KI-Teil (Research/Charakterisierung) erledigt
# danach Claudian anhand von 00_Inbox/M365 Wochen-Report.md.

cd "$(dirname "$0")" || exit 1

# --- Konfiguration ---
export M365_CLIENT_ID="0c8e309d-d02e-4244-ae2a-dbb5551cb550"
export M365_TENANT_ID="ae7f72de-197d-4ba0-a852-40ee367a5150"

LOG="weekly_$(date +%Y%m%d_%H%M).log"
exec > "$LOG" 2>&1
echo "=== Weekly refresh START $(date) ==="

# Überfällig-Erinnerung des Watchdogs entfernen — wir laufen ja jetzt gerade.
rm -f "$(cd ../.. && pwd)/00_Inbox/⚠️ M365 Wochen-Refresh ueberfaellig.md" 2>/dev/null

source .venv/bin/activate || { echo "venv fehlt"; exit 1; }

run() { echo "\n--- $* ---"; python "$@" || echo "WARN: '$*' fehlgeschlagen (weiter)"; }

run m365_people_sync.py                                            # neue Kontakte
run mail_digest.py --top 0 --max 6000 --min-total 1 --sort sent    # Mail-Digest
run teams_digest.py --max-chats 600                                # Teams-Digest
run first_contact.py --apply                                       # kontakt_seit (Mail)
run teams_first_contact.py --apply                                 # kontakt_seit (Teams)
run link_people_to_clients.py --apply                              # Firma→Kunde matchen
run fill_stakeholders.py --apply                                   # Stakeholder
run apply_firmenprofile.py --apply                                 # bestehende Firmenprofile
run contact_stats.py --apply                                       # Interaktions-Stats (voll)
run weekly_report.py                                               # Gap-Report → 00_Inbox

echo "=== Weekly refresh DONE $(date) ==="
# alte Logs aufräumen (älter als 60 Tage)
find . -maxdepth 1 -name 'weekly_*.log' -mtime +60 -delete 2>/dev/null
