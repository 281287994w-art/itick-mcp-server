"""HTTP client for iTick REST API."""

from __future__ import annotations

import logging
import os
from urllib.parse import urlencode

import httpx

log = logging.getLogger(__name__)


def api_base() -> str:
    return os.environ.get("ITICK_API_BASE", "https://api.itick.org").rstrip("/")


def itick_headers() -> dict[str, str]:
    token = os.environ.get("ITICK_TOKEN", "").strip()
    headers = {"accept": "application/json"}
    if token:
        headers["token"] = token
    return headers


def itick_get(path: str, params: dict | None = None, *, timeout: float = 60.0) -> str:
    """GET path (leading slash), return response body text or error message."""
    q = {k: v for k, v in (params or {}).items() if v is not None}
    url = f"{api_base()}{path}"
    if q:
        url = f"{url}?{urlencode(q)}"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, headers=itick_headers())
            response.raise_for_status()
            body = response.text
        log.info("✅ iTick %s ==>%s", url, body[:500] + ("..." if len(body) > 500 else ""))
        return body
    except Exception as e:
        log.exception("❌ iTick 请求失败：%s", url)
        return f"获取数据失败：{e!s}"
