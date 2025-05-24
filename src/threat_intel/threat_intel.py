"""
Load a list of known-bad IPs from data/ipsum.txt and compare them to
resolved domain→IP mappings.
"""

from typing import Set, Dict


def load_bad_ips(file_path: str) -> Set[str]:
    """
    Read a bad-IP list (one IP and optional score per line) and return
    a set of IP addresses marked as malicious.
    """
    bad_ips: Set[str] = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            ip = line.split()[0]
            bad_ips.add(ip)
    return bad_ips


def check_bad_ips(resolved_mapping: Dict[str, str], bad_ips: Set[str]) -> Set[str]:
    """
    Identify which IPs in the resolved_mapping appear in the bad_ips set.
    """
    return set(resolved_mapping.values()) & bad_ips
