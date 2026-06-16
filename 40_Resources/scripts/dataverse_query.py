#!/usr/bin/env python3
"""Dataverse Web API client using the existing MSAL token cache.

Sister script to live_search.py — same CLIENT_ID/TENANT_ID and token cache,
but acquires a token for the Dataverse resource instead of Microsoft Graph.

Usage:
    ./.venv/bin/python dataverse_query.py whoami
    ./.venv/bin/python dataverse_query.py setname cr55b_journal
    ./.venv/bin/python dataverse_query.py entity cr55b_journal --top 5
    ./.venv/bin/python dataverse_query.py entity cr55b_journal --top 10 \
        --select "cr55b_name,createdon" --filter "statecode eq 0" \
        --orderby "createdon desc"
    ./.venv/bin/python dataverse_query.py raw "cr55b_journals?$top=3"

First run may need consent: add --login to perform an interactive
device-code sign-in once (token is then cached for silent reuse).
"""
import argparse
import json
import sys
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent

# Dataverse environment
RESOURCE = "https://org62e5ae4f.crm4.dynamics.com"
API = f"{RESOURCE}/api/data/v9.2"
SCOPES = [f"{RESOURCE}/.default"]


def get_token(interactive=False):
    # Token-Cache liegt im macOS Keychain (siehe auth_common.py), nicht mehr im Vault/Dropbox.
    from auth_common import get_token as _ac_get_token
    return _ac_get_token(SCOPES, allow_device_flow=interactive)


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": 'odata.include-annotations="*"',
    }


def api_get(token, path):
    url = path if path.startswith("http") else f"{API}/{path.lstrip('/')}"
    r = requests.get(url, headers=_headers(token), timeout=60)
    if not r.ok:
        sys.exit(f"HTTP {r.status_code}: {r.text[:1000]}")
    return r.json()


def cmd_whoami(token, _args):
    data = api_get(token, "WhoAmI")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_setname(token, args):
    """Resolve the EntitySetName (plural, used in URLs) for a logical name."""
    data = api_get(
        token,
        f"EntityDefinitions(LogicalName='{args.logical_name}')"
        "?$select=LogicalName,EntitySetName,DisplayName",
    )
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_entity(token, args):
    # logical name -> entity set name
    meta = api_get(
        token,
        f"EntityDefinitions(LogicalName='{args.logical_name}')?$select=EntitySetName",
    )
    setname = meta["EntitySetName"]

    qs = []
    if args.select:
        qs.append(f"$select={args.select}")
    if args.filter:
        qs.append(f"$filter={args.filter}")
    if args.orderby:
        qs.append(f"$orderby={args.orderby}")
    qs.append(f"$top={args.top}")
    path = setname + ("?" + "&".join(qs) if qs else "")

    data = api_get(token, path)
    rows = data.get("value", [])
    print(f"# {setname}: {len(rows)} row(s)\n", file=sys.stderr)
    print(json.dumps(rows, indent=2, ensure_ascii=False))


def cmd_raw(token, args):
    data = api_get(token, args.path)
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description="Dataverse Web API client")
    p.add_argument("--login", action="store_true",
                   help="interactive device-code sign-in (first-time consent)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")

    s = sub.add_parser("setname")
    s.add_argument("logical_name")

    e = sub.add_parser("entity")
    e.add_argument("logical_name")
    e.add_argument("--top", type=int, default=5)
    e.add_argument("--select")
    e.add_argument("--filter")
    e.add_argument("--orderby")

    r = sub.add_parser("raw")
    r.add_argument("path")

    args = p.parse_args()
    token = get_token(interactive=args.login)

    {
        "whoami": cmd_whoami,
        "setname": cmd_setname,
        "entity": cmd_entity,
        "raw": cmd_raw,
    }[args.cmd](token, args)


if __name__ == "__main__":
    main()
