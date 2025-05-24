"""
Provides asynchronous fetching of IP geolocation data from ipinfo.io
and a synchronous wrapper for ease of use.
"""
import asyncio
from typing import Dict

import aiohttp

class IPInfoRecord:
    """
    Container for IP information retrieved from ipinfo.io API.
    """
    def __init__(self, data: dict):
        self.ip: str = data.get("ip", "")
        self.city: str = data.get("city", "")
        self.region: str = data.get("region", "")
        self.country: str = data.get("country", "")
        self.loc: str = data.get("loc", "")
        self.org: str = data.get("org", "")
        self.hostname: str = data.get("hostname", "")

    def to_dict(self) -> dict:
        """
        Convert the IPInfoRecord to a dictionary.
        """
        return {
            "ip": self.ip,
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "loc": self.loc,
            "org": self.org,
            "hostname": self.hostname,
        }

    def display_info(self) -> str:
        """Returns a readable string representation of the IP info."""
        return f"IP: {self.ip}, City: {self.city}, Country: {self.country}, Org: {self.org}"



async def _fetch_with_retries(
    session: aiohttp.ClientSession,
    url: str,
    retries: int = 3,
    backoff_factor: float = 0.5
) -> dict:
    """
    Asynchronously GET the URL with retries and exponential backoff.
    Returns parsed JSON or empty dict on failure.
    """
    for attempt in range(1, retries + 1):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
        await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
    return {}


async def get_ip_info_async(domain_ip_map: Dict[str, str]) -> Dict[str, IPInfoRecord]:
    """
    Fetch IP geolocation for each resolved domain asynchronously.
    """
    results: Dict[str, IPInfoRecord] = {}

    async with aiohttp.ClientSession() as session:
        tasks = {
            domain: asyncio.create_task(
                _fetch_with_retries(session, f"https://ipinfo.io/{ip}/json")
            )
            for domain, ip in domain_ip_map.items()
        }

        for domain, task in tasks.items():
            data = await task
            results[domain] = IPInfoRecord(data)

    return results


def get_ip_info(domain_ip_map: Dict[str, str]) -> Dict[str, IPInfoRecord]:
    """
    Synchronous wrapper for get_ip_info_async().
    """
    return asyncio.run(get_ip_info_async(domain_ip_map))
