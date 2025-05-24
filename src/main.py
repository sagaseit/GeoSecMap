#!/usr/bin/env python3
"""
Orchestrates the full pipeline:
1. Fetch & parse history from chosen browser (limit domains)
2. Resolve domains → IPs
3. Fetch geolocation
4. Threat‑intel checks
5. Build & export map
"""

import os
import sys
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from history.history import get_history
from resolver import resolve_domains
from threat_intel.threat_intel import load_bad_ips, check_bad_ips

from geolocate.geolocate import get_ip_info
from geolocate.mapper import build_map, export_map

HELP_TEXT = """
Examples:
  # Edge, default 100 domains:
  python3 main.py

  # Firefox, limit 50 domains:
  python3 main.py --browser firefox --max-domains 50
"""


def validateDomainNumber(value: str) -> int:
    """
    Validates the number of domains user wants to resolve
    """
    try:
        result = int(value)
    except ValueError as not_integer:
        raise argparse.ArgumentTypeError(f"‘{value}’ is not an integer") from not_integer
    if result < 1 or result > 100:
        raise argparse.ArgumentTypeError(f"max-domains must be between 1 and 100, got {result}")
    return result


def main():
    """
        Main function handles user input
    """
    p = argparse.ArgumentParser(
        prog="server-map",
        description="Visualize your browsing history servers on a map with threat intel",
        epilog=HELP_TEXT,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "-b", "--browser",
        choices=["edge", "chrome", "firefox"],
        default="edge",
        help="Which browser to pull history from (default: edge)"
    )
    p.add_argument(
        "-n", "--max-domains",
        type=validateDomainNumber,
        default=100,
        metavar="N",
        help="Max number of unique domains to include (1–100, default: 50)"
    )
    args = p.parse_args()

    print(f"🔍  Fetching history from {args.browser!r}, limiting to {args.max_domains} domains…")
    url_obj = get_history(browser=args.browser, max_domains=args.max_domains)

    print("🌐  Resolving domains to IP addresses…")
    domain_ip_map = resolve_domains(url_obj)
    if not domain_ip_map:
        print(
            "⚠️  No domains found in browsing history. Nothing to process. It seems like you haven't visited a single website yet!")
        sys.exit(0)
    print(f"   ✅ Resolved {len(domain_ip_map)} domains to IPs\n")

    print("🛰️  Fetching geolocation data…")
    ip_info_map = get_ip_info(domain_ip_map)
    print(f"   ✅ Got geolocation for {len(ip_info_map)} IPs\n")

    print("🛡️  Checking bad‑IP list…")
    bad_list_file = os.path.join(os.path.dirname(__file__), "..", "data", "ipsum.txt")
    if not os.path.isfile(bad_list_file):
        print(f"⚠️  Bad-IP list file not found: {bad_list_file}")
        sys.exit(0)

    bad_ips = load_bad_ips(bad_list_file)
    found = check_bad_ips(domain_ip_map, bad_ips)
    if found:
        print("   ⚠️  Found bad IPs:")
        for ip in sorted(found):
            domains = [d for d, addr in domain_ip_map.items() if addr == ip]
            print(f"     • {ip} ← domains: {', '.join(domains)}")
    else:
        print("   ✅ No bad IPs detected\n")

    print("🗺️  Building interactive map…")
    map_obj = build_map(ip_info_map)
    map_filename = f"map_{args.browser}_history.html"
    export_map(map_obj, filename=map_filename)
    print(f"   ✅ {map_filename} written\n")


if __name__ == "__main__":
    main()
