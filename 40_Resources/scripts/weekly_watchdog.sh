#!/bin/zsh
# weekly_watchdog.sh
# -------------------
# Erinnert daran, den wöchentlichen M365-Refresh MANUELL zu starten, falls er
# nicht lief (z. B. Laptop war Freitag 23:40 aus). Prüft das Alter des jüngsten
# weekly_*.log; ist es älter als 7,5 Tage, kommt eine macOS-Notification + eine
# Flag-Notiz in 00_Inbox. Sobald wieder gelaufen wurde, verschwindet die
# Erinnerung von selbst (weekly_refresh.sh löscht das Flag beim Start, und dieser
# Watchdog räumt es ebenfalls weg, sobald wieder ein frisches Log da ist).
# Läuft via launchd: täglich 13:00 + bei jedem Login (RunAtLoad).

cd "$(dirname "$0")" || exit 1
VAULT="$(cd ../.. && pwd)"
FLAG="$VAULT/00_Inbox/⚠️ M365 Wochen-Refresh ueberfaellig.md"
MAXAGE=$(( (7*24 + 12) * 3600 ))    # 7,5 Tage in Sekunden

newest=$(ls -t weekly_*.log 2>/dev/null | head -1)

overdue=1
last="nie"
if [[ -n "$newest" ]]; then
  last="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$newest")"
  age=$(( $(date +%s) - $(stat -f %m "$newest") ))
  (( age <= MAXAGE )) && overdue=0
fi

if (( overdue )); then
  msg="Letzter Lauf: $last. Bitte manuell nachholen: weekly_refresh.sh"
  /usr/bin/osascript >/dev/null 2>&1 <<OSA
display notification "$msg" with title "⚠️ M365 Wochen-Refresh überfällig"
OSA
  cat > "$FLAG" <<EOF
---
type: reminder
created: $(date +%F)
tags: [reminder, m365-sync]
---
# ⚠️ M365 Wochen-Refresh überfällig

Der automatische Wochen-Refresh (geplant **Freitag 23:40**, launchd) ist seit über
7,5 Tagen nicht gelaufen — vermutlich war der Laptop zum geplanten Zeitpunkt aus.

**Letzter Lauf:** $last

## Jetzt manuell nachholen
~~~bash
cd "$VAULT/40_Resources/scripts"
./weekly_refresh.sh
~~~

Oder bei mir (Claudian) einfach sagen: *„starte den M365 Wochen-Refresh"*.

> Diese Notiz löscht sich automatisch, sobald der Refresh wieder gelaufen ist.
EOF
  echo "$(date) OVERDUE (letzter Lauf: $last) → erinnert."
else
  rm -f "$FLAG" 2>/dev/null
  echo "$(date) OK (letzter Lauf: $last)."
fi
