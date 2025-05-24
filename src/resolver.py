"""
Module for resolving domain names from browsing history and returning a sorted domain-IP mapping.
"""

import os
import sys
import socket
from typing import Dict

sys.path.insert(0, os.path.dirname(__file__))

from history.history import URL, get_history


def resolve_domains(url_obj: URL) -> Dict[str, str]:
    """
    Resolve each domain in the URL object to its IP address.
    """
    domain_ip_map: Dict[str, str] = {}
    for domain in url_obj.get_domain():
        try:
            ip_address = socket.gethostbyname(domain)
            domain_ip_map[domain] = ip_address
        except socket.gaierror:
            # Skip domains that cannot be resolved
            continue
    return domain_ip_map


def get_sorted_domain_ip_map() -> Dict[str, str]:
    """
    Retrieve browsing history, resolve domains to IP addresses, and return a sorted mapping.
    """
    history_obj = get_history()
    domain_ip_map = resolve_domains(history_obj)
    return dict(sorted(domain_ip_map.items()))


if __name__ == "__main__":
    mapping = get_sorted_domain_ip_map()
    for domena, ip in mapping.items():
        print(f"{domena}: {ip}")
