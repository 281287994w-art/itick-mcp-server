"""Register iTick REST endpoints as MCP tools (see https://docs.itick.org/)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mcp.server.fastmcp import Context
from pydantic import Field

from client import itick_get
from config import TRANSPORT_MODE
from texts import *

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_rest_tools(mcp: "FastMCP") -> None:
    _register_basics(mcp)
    _register_stock_extras(mcp)
    for api_path, tool_prefix, region_desc in _ASSETS:
        _register_asset_family(mcp, api_path, tool_prefix, region_desc)


_ASSETS = [
    ("stock", "stock", REGION_STOCK),
    ("crypto", "crypto", REGION_CRYPTO),
    ("forex", "forex", REGION_FOREX),
    ("indices", "indices", REGION_INDICES),
    ("future", "future", REGION_FUTURE),
    ("fund", "fund", REGION_FUND),
]


def _extract_token(ctx: Context) -> str | None:
    """从请求 header 中提取 token。"""
    try:
        if ctx.request_context and ctx.request_context.request:
            # 尝试多种常见的 token header 名称
            for header_name in ["token", "ITICK_TOKEN"]:
                token = ctx.request_context.request.headers.get(header_name)
                if token:
                    return token.strip()
    except Exception:
        pass
    return None


def _get_is_stdio() -> bool:
    """判断当前是否为 stdio 模式。"""
    return TRANSPORT_MODE == "stdio"


def _register_basics(mcp: "FastMCP") -> None:
    @mcp.tool(
        name="symbolList",
        description="基础数据：按类型与区域查询产品列表（GET /symbol/list）",
    )
    def symbol_list(
        asset_type: str = Field(
            description=f"{SYMBOL_TYPE}（REST 查询参数名 type）",
        ),
        region: str = Field(description="市场区域代码"),
        code: str | None = Field(default=None, description="可选，产品代码筛选"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(
            "/symbol/list",
            {"type": asset_type, "region": region, "code": code},
            token=token,
            is_stdio=_get_is_stdio(),
        )

    @mcp.tool(
        name="symbolHolidays",
        description="基础数据：市场休市日历（GET /symbol/v2/holidays）",
    )
    def symbol_holidays(
        code: str = Field(description="国家/地区代码，如 HK、US"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get("/symbol/v2/holidays", {"code": code}, token=token, is_stdio=_get_is_stdio())


def _register_stock_extras(mcp: "FastMCP") -> None:
    @mcp.tool(
        name="stockInfo",
        description="股票：公司信息（GET /stock/info）",
    )
    def stock_info(
        asset_type: str = Field(
            description="市场类型（REST 参数 type），如 stock",
        ),
        region: str = Field(description=REGION_STOCK),
        code: str = Field(description="股票代码"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(
            "/stock/info",
            {"type": asset_type, "region": region, "code": code},
            token=token,
            is_stdio=_get_is_stdio(),
        )

    @mcp.tool(
        name="stockIpo",
        description="股票：IPO 日历（GET /stock/ipo）",
    )
    def stock_ipo(
        ipo_kind: str = Field(
            description="REST 参数 type：upcoming=待上市，recent=新近上市",
        ),
        region: str = Field(description=REGION_STOCK),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get("/stock/ipo", {"type": ipo_kind, "region": region}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name="stockSplit",
        description="股票：拆股/复权等调整因子列表（GET /stock/split）",
    )
    def stock_split(
        region: str = Field(description=REGION_STOCK),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get("/stock/split", {"region": region}, token=token, is_stdio=_get_is_stdio())


def _register_asset_family(
    mcp: "FastMCP",
    api_path: str,
    tool_prefix: str,
    region_desc: str,
) -> None:
    base = f"/{api_path}"

    @mcp.tool(
        name=f"{tool_prefix}Tick",
        description=f"[{api_path}] 单笔实时 Tick（GET {base}/tick）",
    )
    def single_tick(
        region: str = Field(description=region_desc),
        code: str = Field(description="产品代码"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/tick", {"region": region, "code": code}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Quote",
        description=f"[{api_path}] 单笔实时报价（GET {base}/quote）",
    )
    def single_quote(
        region: str = Field(description=region_desc),
        code: str = Field(description="产品代码"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/quote", {"region": region, "code": code}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Depth",
        description=f"[{api_path}] 单笔盘口深度（GET {base}/depth）",
    )
    def single_depth(
        region: str = Field(description=region_desc),
        code: str = Field(description="产品代码"),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/depth", {"region": region, "code": code}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Kline",
        description=f"[{api_path}] 单笔 K 线（GET {base}/kline）",
    )
    def single_kline(
        region: str = Field(description=region_desc),
        code: str = Field(description="产品代码"),
        k_type: int = Field(description=KTYPE),
        et: int | None = Field(
            default=None,
            description="截止毫秒时间戳；不传则默认当前",
        ),
        limit: int | None = Field(
            default=None,
            description="返回条数",
        ),
        ctx: Context = None,
    ) -> str:
        params: dict = {"region": region, "code": code, "kType": k_type}
        if et is not None:
            params["et"] = et
        if limit is not None:
            params["limit"] = limit
        token = _extract_token(ctx)
        return itick_get(f"{base}/kline", params, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Ticks",
        description=f"[{api_path}] 批量实时 Tick（GET {base}/ticks）",
    )
    def batch_ticks(
        region: str = Field(description=region_desc),
        codes: str = Field(description=CODES_BATCH),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/ticks", {"region": region, "codes": codes}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Quotes",
        description=f"[{api_path}] 批量实时报价（GET {base}/quotes）",
    )
    def batch_quotes(
        region: str = Field(description=region_desc),
        codes: str = Field(description=CODES_BATCH),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/quotes", {"region": region, "codes": codes}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Depths",
        description=f"[{api_path}] 批量盘口深度（GET {base}/depths）",
    )
    def batch_depths(
        region: str = Field(description=region_desc),
        codes: str = Field(description=CODES_BATCH),
        ctx: Context = None,
    ) -> str:
        token = _extract_token(ctx)
        return itick_get(f"{base}/depths", {"region": region, "codes": codes}, token=token, is_stdio=_get_is_stdio())

    @mcp.tool(
        name=f"{tool_prefix}Klines",
        description=f"[{api_path}] 批量 K 线（GET {base}/klines）",
    )
    def batch_klines(
        region: str = Field(description=region_desc),
        codes: str = Field(description=CODES_BATCH),
        k_type: int = Field(description=KTYPE),
        limit: int | None = Field(default=None, description="每个标的返回条数"),
        et: int | None = Field(
            default=None,
            description="截止毫秒时间戳；不传则默认当前",
        ),
        ctx: Context = None,
    ) -> str:
        params: dict = {"region": region, "codes": codes, "kType": k_type}
        if et is not None:
            params["et"] = et
        if limit is not None:
            params["limit"] = limit
        token = _extract_token(ctx)
        return itick_get(f"{base}/klines", params, token=token, is_stdio=_get_is_stdio())
