"""
Retrieve and parse browsing history from a specified browser,
extract unique domains (with optional limit) and detect insecure schemes.
"""
from typing import Set, Dict, List
from urllib.parse import urlparse

from browser_history.browsers import Edge, Chrome, Firefox


class URL:
    """
    Parse URL records and extract actions, domains, and insecure schemes.
    """
    def __init__(self, url_info: List[tuple]):
        self._url_info: List[tuple] = url_info
        self._action: Set[str] = set()
        self._url: List[str] = []
        self._domain: Set[str] = set()
        self._insecure_scheme: Dict[str, str] = {}

    def parse(self) -> None:
        """Extract actions and URLs from history records."""
        self._action = {record[2] for record in self._url_info}
        self._url = [record[1] for record in self._url_info]

    def parse_domain(self, max_domains: int = None) -> None:
        """
        Parse URLs to build a list of unique domains and record insecure schemes.
        Optionally limit the number of domains to `max_domains`.
        """
        domains_list: List[str] = []
        for url in self._url:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith("www."):
                domain = domain[4:]
            if domain not in domains_list:
                domains_list.append(domain)
                if parsed.scheme != "https":
                    self._insecure_scheme[domain] = parsed.scheme
            if max_domains is not None and len(domains_list) >= max_domains:
                break
        self._domain = set(domains_list[:max_domains])

    def get_action(self) -> Set[str]:
        """Return parsed actions."""
        return self._action

    def get_domain(self) -> Set[str]:
        """Return parsed domains."""
        return self._domain

    def get_insecure_scheme(self) -> Dict[str, str]:
        """Return mapping of domains with non-https schemes."""
        return self._insecure_scheme


def get_history(browser: str = "edge", max_domains: int = 100) -> URL:
    """
    Fetch browsing history from the specified browser and return a parsed URL object.
    """
    browser_map = {
        "edge": Edge,
        "chrome": Chrome,
        "firefox": Firefox
    }
    key = browser.lower()
    if key not in browser_map:
        raise ValueError(f"Unsupported browser '{browser}'. Choose from: {', '.join(browser_map)}")
    if max_domains < 1 or max_domains > 100:
        raise ValueError(f"max_domains must be between 1 and 100. Got: {max_domains}")
    browser_cls = browser_map[key]()
    outputs = browser_cls.fetch_history()
    records = outputs.histories
    url_obj = URL(records)
    url_obj.parse()
    url_obj.parse_domain(max_domains)
    return url_obj
