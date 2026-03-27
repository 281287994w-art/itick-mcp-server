"""Shared Field descriptions for MCP tools (aligned with docs.itick.org)."""

from textwrap import dedent

REGION_STOCK = dedent(
    """
    股票区域代码（文档常见大写 HK/US/SH…，小写如 us、hk 亦常见），例如：
    us, eu, de, jp, cn, sz, sh, hk, in, sg, tr, es, tw, th, my, mx, nl, id, vn, it, fr, kr, il, au, ar, pk, ca, pe, ng 等。
    """
).strip()

REGION_CRYPTO = dedent(
    """
    加密市场区域：BA、BT、PB 等（见 iTick 文档 Crypto）。
    """
).strip()

REGION_FOREX = "外汇区域代码，常见为 GB。"

REGION_INDICES = "指数区域代码，常见为 GB。"

REGION_FUTURE = dedent(
    """
    期货区域：US、HK、CN 等。
    """
).strip()

REGION_FUND = "基金区域代码，常见为 US。"

KTYPE = dedent(
    """
    K 线周期（参数名 kType）：1 分钟、2 五分钟、3 十五分钟、4 三十分钟、5 一小时、8 日、9 周、10 月。
    """
).strip()

CODES_BATCH = "多个产品代码，英文逗号分隔，如 700,9988 或 BTCUSDT,ETHUSDT。"

SYMBOL_TYPE = "产品大类：stock | forex | indices | crypto | future | fund。"
