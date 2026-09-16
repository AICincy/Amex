#!/usr/bin/env python3
"""Build credential-free EnformionGO call plans; live requests are disabled."""

from __future__ import annotations

import argparse
import json
import os
import sys

DEFAULT_BASE = "https://devapi.enformion.com"

# Untrusted cache. Override with --path / --search-type after a live docs fetch.
ALIASES = {
    "contact-enrich": ("DevAPIContactEnrich", "/Contact/Enrich"),
    "contact-enrich-plus": ("DevAPIContactEnrichPlus", "/Contact/EnrichPlus"),
    "caller-id": ("DevAPICallerID", "/Phone/Enrich"),
    "caller-id-plus": ("DevAPICallerIDPlus", "/Phone/EnrichPlus"),
    "email-id": ("DevAPIEmailID", "/Email/Enrich"),
    "email-id-plus": ("DevAPIEmailIDPlus", "/Email/EnrichPlus"),
    "contact-id": ("DevAPIContactID", "/Contact/Id"),
    "contact-id-plus": ("DevAPIContactIDPlus", "/Contact/IdPlus"),
    "address-id": ("DevAPIAddressID", "/Address/Id"),
    "address-id-plus": ("DevAPIAddressIDPlus", "/Address/IdPlus"),
    "address-autocomplete": ("DevAPIAddressAutoComplete", "/Address/AutoComplete"),
    "elead-verify": ("LeadVerify", "/eIDV/eLeadVerify"),
    "person-search": ("Person", "/PersonSearch"),
    "person-teaser": ("Teaser", "/PersonSearch"),
    "reverse-phone-person-teaser": ("ReversePhonePersonTeaser", "/PersonSearch"),
    "reverse-phone-person": ("ReversePhonePerson", "/PersonSearch"),
    "id-verification": ("DevAPIIDVerification", "/Identity/Verify_Id"),
    "census-search": ("Census", "/CensusSearch"),
    "debt-v2": ("DebtV2", "/DebtSearch/V2"),
    "divorce-search": ("Divorce", "/DivorceSearch"),
    "marriage-search": ("Marriage", "/MarriageSearch"),
    "reverse-phone": ("ReversePhone", "/ReversePhoneSearch"),
    "linkedin-id": ("LinkedinID", "/LinkedIn/Id"),
    "business-search": ("BusinessV2", "/BusinessV2Search"),
    "domain-search": ("Domain", "/DomainSearch"),
    "workplace-search": ("Workplace", "/WorkplaceSearch"),
    "business-id": ("BusinessID", "/Business/Id"),
    "property-v2": ("PropertyV2", "/PropertyV2Search"),
    "criminal-v2": ("CriminalV2", "/CriminalSearch/V2"),
    "eviction": ("Eviction", "/EvictionSearch"),
    "pre-foreclosure": ("ForeclosureV2", "/ForeclosureV2Search"),
    "ofac": ("Ofac", "/OfacSearch"),
    "vehicle-ownership": ("VehicleRegistrationSearch", "/VehicleRegistrationSearch"),
    "dea": ("Dea", "/deasearch"),
    "professional-license": ("ProLicense", "/ProLicenseSearch"),
    "alerts-add": ("DataAlertsAddSubscription", "/DataAlerts/AddSubscription"),
    "alerts-get": ("DataAlertsGetSubscription", "/DataAlerts/GetSubscription"),
    "alerts-remove": ("DataAlertsRemoveSubscription", "/DataAlerts/RemoveSubscription"),
    "alerts-get-alert": ("DataAlertsGetAlert", "/DataAlerts/GetAlert"),
    "alerts-count": ("DataAlertsCountAlert", "/DataAlerts/CountAlert"),
}


def parse_body(raw: str | None) -> dict:
    if raw is None or raw == "":
        return {}
    if raw.startswith("@") or (os.path.isfile(raw) and raw.endswith(".json")):
        path = raw[1:] if raw.startswith("@") else raw
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    return json.loads(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description="POST to EnformionGO")
    parser.add_argument("alias", nargs="?", help="route alias")
    parser.add_argument("--path", help="override URL path, e.g. /Contact/Enrich")
    parser.add_argument("--search-type", help="override galaxy-search-type")
    parser.add_argument("--body", default="{}", help="JSON object or path to .json")
    parser.add_argument("--session-id", default="", help="optional galaxy-client-session-id")
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.list:
        rows = [
            {"alias": name, "search_type": spec[0], "path": spec[1]}
            for name, spec in ALIASES.items()
        ]
        json.dump({"ok": True, "route": "alias_list", "aliases": rows}, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    search_type = args.search_type
    path = args.path
    if args.alias:
        if args.alias not in ALIASES:
            sys.stderr.write(f"BLOCKED: unknown alias {args.alias}\n")
            return 2
        cached_type, cached_path = ALIASES[args.alias]
        search_type = search_type or cached_type
        path = path or cached_path
    if not search_type or not path:
        sys.stderr.write("BLOCKED: need alias or both --path and --search-type\n")
        return 2
    if not path.startswith("/"):
        path = "/" + path

    try:
        body = parse_body(args.body)
    except Exception as exc:
        sys.stderr.write(f"BLOCKED: invalid body: {exc}\n")
        return 2
    if not isinstance(body, dict):
        sys.stderr.write("BLOCKED: body must be a JSON object\n")
        return 2

    if args.dry_run:
        json.dump(
            {
                "ok": True,
                "route": "enformion_dry_run",
                "method": "POST",
                "url": DEFAULT_BASE + path,
                "galaxy_search_type": search_type,
                "headers_sent": [
                    "galaxy-ap-name",
                    "galaxy-ap-password",
                    "galaxy-search-type",
                    "accept",
                    "content-type",
                ],
                "body": body,
                "billed": False,
            },
            sys.stdout,
            indent=2,
        )
        sys.stdout.write("\n")
        return 0

    sys.stderr.write(
        "BLOCKED: live Enformion requests are disabled until a trusted authorization controller "
        "can verify a current, scope-bound authorization receipt. Use --dry-run.\n"
    )
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
