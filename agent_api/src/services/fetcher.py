from __future__ import annotations

import time
import urllib.robotparser
from dataclasses import dataclass
from urllib.parse import urlsplit

import httpx

from src.config import get_settings

ROBOTS_TTL_SECONDS = 3600
_robots_cache =  {}

settings = get_settings()

class FetchError(Exception):
    """Disallowed by robots.txt or response exceeded max_article_bytes."""

@dataclass
class FetchedPage:
    url: str
    html: str
    status_code: int

def _empty_parser() -> urllib.robotparser.RobotFileParser:
    parser = urllib.robotparser.RobotFileParser()
    parser.parse([])
    return parser

async def _get_robot_parser(host: str, scheme: str) -> urllib.robotparser.RobotFileParser:
    if host in _robots_cache:
        return _robots_cache[host]

    parser = urllib.robotparser.RobotFileParser()
    try:
        async with httpx.AsyncClient(headers = {"User-Agent": settings.user_agent}, timeout = settings.request_timeout_s) as client:
            response = await client.get(f"{scheme}://{host}/robots.txt")

        if response.status_code == 404 or not response.is_success:
            parser = _empty_parser()
        else:
            parser.parse(response.text.splitlines())
    except httpx.HTTPError:
        parser = _empty_parser()

    _robots_cache[host] = parser
    return parser

async def _is_allowed(url: str) -> bool:
    parts = urlsplit(url)
    host = parts.netloc or parts.hostname or ""
    if not host:
        return True
    parser = await _get_robot_parser(host, parts.scheme or "https")
    return parser.can_fetch(settings.user_agent, url)

async def fetch_article(url: str) -> FetchedPage:
    if not await _is_allowed(url):
        raise FetchError(f"robots.txt disallows fetching {url}")

    async with (
        httpx.AsyncClient(
            headers = {"User-Agent": settings.user_agent} , timeout = settings.request_timeout_s
    ) as client,
    client.stream("GET",url,follow_redirects = True) as response,
):
        response.raise_for_status()
        final_url = str(response.url)
        if final_url != url and not await is_allowed(final_url):
            raise FetchError(f"robots.txt disallows redirected URL {final_url!r}")

        body = bytearray()
        async for chunk in response.aiter_bytes():
            body.extend(chunk)
            if len(body) > settings.max_article_bytes:
                raise FetchError(f"Response exceeded max_article_bytes ({settings.max_article_bytes})")
        html = bytes(body).decode(response.encoding or "utf-8" , errors = "replace")
        status_code = response.status_code

    return FetchedPage(url = url , html = html , status_code = status_code)
        