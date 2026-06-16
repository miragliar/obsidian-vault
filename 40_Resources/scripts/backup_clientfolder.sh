#!/usr/bin/env bash
# backup_clientfolder.sh — versionierte ZIP-Sicherungen eines Kunden-Arbeitsordners.
#
# Sichert z. B. den UpGreat/averecura-Ordner (PBIX, Dataflow-JSON, PDF) als
# Zeitstempel-ZIP. Erstellt nur dann eine neue Sicherung, wenn sich der Inhalt
# seit der letzten Sicherung geändert hat (SHA-Vergleich) — so entstehen keine
# identischen Dubletten bei jedem Lauf. Alte Sicherungen werden rotiert (Retention).
#
# READ-ONLY auf der Quelle: liest nur, schreibt ausschließlich ins Backup-Ziel.
#
# Verwendung:
#   ./backup_clientfolder.sh                      # Default: averecura
#   ./backup_clientfolder.sh "/abs/pfad/zum/ordner"
#   KEEP=60 ./backup_clientfolder.sh              # mehr Snapshots behalten
#   ./backup_clientfolder.sh --force             # auch ohne Änderung sichern
#
# Scheduling (optional, macOS launchd) — Hinweise am Dateiende.

set -euo pipefail

# --- Konfiguration --------------------------------------------------------
DROPBOX_BASE="${DROPBOX_BASE:-/Users/miragliag/Dropbox/Miraglia-BI/UpGreat}"
DEFAULT_SRC="$DROPBOX_BASE/averecura"
KEEP="${KEEP:-30}"                 # wie viele Snapshots behalten
FORCE=0

# --- Argumente ------------------------------------------------------------
SRC="$DEFAULT_SRC"
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    -*)      echo "Unbekannte Option: $arg" >&2; exit 2 ;;
    *)       SRC="$arg" ;;
  esac
done

# Trailing-Slash entfernen
SRC="${SRC%/}"
NAME="$(basename "$SRC")"
DEST_DIR="$DROPBOX_BASE/_Sicherungen/$NAME"

if [ ! -d "$SRC" ]; then
  echo "✗ Quellordner nicht gefunden: $SRC" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"

# --- Änderungserkennung (Hash über alle Dateien, .DS_Store ignoriert) -----
current_hash() {
  # Inhalts-Hash: relativer Pfad + Datei-SHA, sortiert, dann ein Gesamt-SHA.
  ( cd "$SRC" && find . -type f ! -name '.DS_Store' -print0 \
      | sort -z \
      | xargs -0 shasum 2>/dev/null \
      | shasum | awk '{print $1}' )
}

HASH_FILE="$DEST_DIR/.lasthash"
NEW_HASH="$(current_hash)"
OLD_HASH=""
[ -f "$HASH_FILE" ] && OLD_HASH="$(cat "$HASH_FILE")"

if [ "$FORCE" -eq 0 ] && [ "$NEW_HASH" = "$OLD_HASH" ] && [ -n "$OLD_HASH" ]; then
  echo "= Keine Änderung seit letzter Sicherung — übersprungen ($NAME)."
  echo "  Letzte Sicherung: $(ls -1t "$DEST_DIR"/*.zip 2>/dev/null | head -1 | xargs -I{} basename {} 2>/dev/null || echo 'keine')"
  exit 0
fi

# --- Sicherung erstellen --------------------------------------------------
# Zeitstempel ohne Doppelpunkte (Dateisystem-sicher).
TS="$(date +%Y-%m-%d_%H%M%S)"
ZIP="$DEST_DIR/${NAME}_${TS}.zip"

# -r rekursiv, -X ohne macOS-Metadaten, .DS_Store ausschließen.
( cd "$SRC/.." && zip -r -X -q "$ZIP" "$NAME" -x '*/.DS_Store' '*.DS_Store' )

echo "$NEW_HASH" > "$HASH_FILE"

SIZE="$(du -h "$ZIP" | awk '{print $1}')"
echo "✓ Sicherung erstellt: $(basename "$ZIP")  ($SIZE)"

# --- Retention: nur die letzten $KEEP ZIPs behalten -----------------------
# Portabel für macOS Bash 3.2 (kein mapfile): neueste zuerst, ab Position KEEP+1 löschen.
ls -1t "$DEST_DIR"/*.zip 2>/dev/null | tail -n +"$((KEEP + 1))" | while IFS= read -r old; do
  [ -n "$old" ] || continue
  rm -f -- "$old"
  echo "  ↳ alt entfernt: $(basename "$old")"
done

COUNT="$(ls -1 "$DEST_DIR"/*.zip 2>/dev/null | wc -l | tr -d ' ')"
echo "  Stand: $COUNT Snapshot(s) in $DEST_DIR (Retention: $KEEP)"

# --------------------------------------------------------------------------
# OPTIONAL automatisch (macOS launchd), z. B. stündlich:
#   ~/Library/LaunchAgents/com.miragliabi.backup-averecura.plist
#   ProgramArguments: /bin/bash <pfad>/backup_clientfolder.sh
#   StartInterval: 3600
#   → launchctl load ~/Library/LaunchAgents/com.miragliabi.backup-averecura.plist
# Dank Hash-Vergleich kostet ein Lauf ohne Änderung praktisch nichts.
