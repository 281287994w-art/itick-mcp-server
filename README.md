# itick-mcp-server

Python [MCP](https://modelcontextprotocol.io/) server exposing [iTick REST API](https://docs.itick.org/) as tools: **基础数据**、**股票**（含信息 / IPO / 复权因子）、以及 **Crypto / Forex / Indices / Future / Fund** 各产品线的单笔与批量 **Tick / Quote / Depth / Kline**。

未实现文档中的 **WebSocket**、**FIX**（非 REST）。

## Setup

```bash
cd itick-mcp-server
pip install -e .
# 若只有 python3：pip3 install -e .
```

环境变量：

| 变量 | 说明 |
|------|------|
| `ITICK_TOKEN` | 必填（实际调用时）：请求头 `token`，见 [官方文档](https://docs.itick.org/) |
| `ITICK_API_BASE` | 可选，默认 `https://api.itick.org`（与文档示例一致）。若你环境使用 `https://api.itick.io`，可设为该地址 |

```bash
export ITICK_TOKEN="your_token"
# export ITICK_API_BASE="https://api.itick.io"
```

## Run (stdio)

```bash
itick-mcp
# 或
python3 -m itick_mcp_server
```

## Cursor / Claude Desktop

```json
{
  "mcpServers": {
    "itick": {
      "command": "itick-mcp",
      "env": {
        "ITICK_TOKEN": "your_token"
      }
    }
  }
}
```

未装到 PATH 时（安装 editable 后一般可省略 `PYTHONPATH`）：

```json
{
  "mcpServers": {
    "itick": {
      "command": "python3",
      "args": ["-m", "itick_mcp_server"],
      "cwd": "/absolute/path/to/itick-mcp-server",
      "env": {
        "ITICK_TOKEN": "your_token"
      }
    }
  }
}
```

## MCP 工具一览（53）

与 [REST 文档](https://docs.itick.org/) 路径对应：

**基础**

- `symbolList` → `GET /symbol/list`
- `symbolHolidays` → `GET /symbol/v2/holidays`

**股票（额外）**

- `stockInfo` → `GET /stock/info`
- `stockIpo` → `GET /stock/ipo`
- `stockSplit` → `GET /stock/split`

**各产品线**（`stock` / `crypto` / `forex` / `indices` / `future` / `fund`）

| 工具名 | REST |
|--------|------|
| `{prefix}Tick` | `GET /{prefix}/tick` |
| `{prefix}Quote` | `GET /{prefix}/quote` |
| `{prefix}Depth` | `GET /{prefix}/depth` |
| `{prefix}Kline` | `GET /{prefix}/kline` |
| `{prefix}Ticks` | `GET /{prefix}/ticks` |
| `{prefix}Quotes` | `GET /{prefix}/quotes` |
| `{prefix}Depths` | `GET /{prefix}/depths` |
| `{prefix}Klines` | `GET /{prefix}/klines` |

批量接口中 `codes` 为英文逗号分隔。K 线参数在工具中为 `k_type`，请求中会编码为 **`kType`**；可选 `et`（毫秒时间戳）、`limit`。

与早期 Java 示例一致的股票单笔 K 线工具名仍为 **`stockKline`**。

## 代码结构

- `itick_mcp_server/client.py` — HTTP GET、`ITICK_API_BASE` / `ITICK_TOKEN`
- `itick_mcp_server/tools_register.py` — 注册全部 REST 工具
- `itick_mcp_server/server.py` — FastMCP 入口
