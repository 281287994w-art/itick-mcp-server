"""HTTP client for iTick REST API."""

from __future__ import annotations

import logging
import os
from urllib.parse import urlencode

import httpx

log = logging.getLogger(__name__)


def api_base() -> str:
    return os.environ.get("ITICK_API_BASE", "https://api.itick.org").rstrip("/")


def itick_headers(token: str | None = None, is_stdio: bool = True) -> dict[str, str]:
    """构建请求头，支持透传 token。
    
    Args:
        token: 可选的认证 token
        is_stdio: 是否为 stdio 模式。stdio 模式下会回退到环境变量 ITICK_TOKEN
    """
    headers = {"accept": "application/json"}
    
    if is_stdio:
        # stdio 模式：优先使用传入的 token，否则从环境变量获取
        auth_token = (token or os.environ.get("ITICK_TOKEN", "")).strip()
        if auth_token:
            headers["token"] = auth_token
    else:
        # HTTP/SSE 模式：只使用传入的 token
        if token:
            headers["token"] = token.strip()
    
    return headers


def itick_get(path: str, params: dict | None = None, *, timeout: float = 60.0, token: str | None = None, is_stdio: bool = True) -> str:
    """GET path (leading slash), return response body text or error message.
    
    Args:
        path: API 路径
        params: 查询参数
        timeout: 超时时间（秒）
        token: 可选，透传的认证 token
        is_stdio: 是否为 stdio 模式，影响 token 的获取策略
    """
    q = {k: v for k, v in (params or {}).items() if v is not None}
    url = f"{api_base()}{path}"
    if q:
        url = f"{url}?{urlencode(q)}"
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.get(url, headers=itick_headers(token, is_stdio))
            response.raise_for_status()
            body = response.text
        log.info("✅ iTick %s ==>%s", url, body[:500] + ("..." if len(body) > 500 else ""))
        return body
    except Exception as e:
        log.exception("❌ iTick 请求失败：%s", url)
        return f"获取数据失败：{e!s}"
