#!/usr/bin/env python3
"""
create_event.py — Outlook-Kalendertermin via Microsoft Graph (delegiert, Calendars.ReadWrite).
Legt einen Termin im EIGENEN Kalender an. Ohne --attendee werden keine Einladungen versendet.

VORAUSSETZUNG: 'Calendars.ReadWrite' (Delegated) in Entra + admin-consent.

Aufruf:
  ./.venv/bin/python create_event.py --subject "Titel" \
      --start 2026-07-06T14:00 --end 2026-07-06T15:30 \
      --body "Beschreibung (HTML erlaubt)" [--location "Ort/Teams"] [--attendee mail@x] [--reminder 1440]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["User.Read", "Calendars.ReadWrite"]
TZ = "W. Europe Standard Time"
SCRIPT_DIR = Path(__file__).resolve().parent


def get_token():
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES)


def main():
    ap = argparse.ArgumentParser(description="Outlook-Kalendertermin anlegen (Graph).")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--start", required=True, help="z. B. 2026-07-06T14:00")
    ap.add_argument("--end", required=True, help="z. B. 2026-07-06T15:30")
    ap.add_argument("--body", default="")
    ap.add_argument("--location", default="")
    ap.add_argument("--attendee", action="append", default=[], help="kann mehrfach angegeben werden")
    ap.add_argument("--reminder", type=int, default=1440, help="Minuten vor Beginn (Default 1 Tag)")
    a = ap.parse_args()

    ev = {
        "subject": a.subject,
        "body": {"contentType": "HTML", "content": a.body},
        "start": {"dateTime": a.start, "timeZone": TZ},
        "end": {"dateTime": a.end, "timeZone": TZ},
        "isReminderOn": True,
        "reminderMinutesBeforeStart": a.reminder,
    }
    if a.location:
        ev["location"] = {"displayName": a.location}
    if a.attendee:
        ev["attendees"] = [{"emailAddress": {"address": x}, "type": "required"} for x in a.attendee]

    tok = get_token()
    r = requests.post(f"{GRAPH}/me/events",
                      headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                      json=ev, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"Fehler {r.status_code}: {r.text[:400]}")
    d = r.json()
    print(f"✓ Termin erstellt: {d.get('subject')} | {d.get('start', {}).get('dateTime')} ({TZ})")
    print(f"  webLink: {d.get('webLink', '')}")


if __name__ == "__main__":
    main()
