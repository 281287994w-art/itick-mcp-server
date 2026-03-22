# itick-mcp-server

面向 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的 Python 服务，将 [iTick REST API](https://docs.itick.org/) 暴露为工具：**基础数据**、**股票**（含信息 / IPO / 复权因子），以及 **Crypto / Forex / Indices / Future / Fund** 各产品线的单笔与批量 **Tick / Quote / Depth / Kline**。

## 关于 iTick

[iTick](https://itick.org) 提供涵盖 **FIX**、**REST** 与 **Websocket** 的 API 套件，面向机构与专业场景；数据覆盖主流市场股票（美国、香港、中国、新加坡、日本等）、全球外汇、指数与加密货币的实时与历史行情。详见 [英文文档](https://docs.itick.org/)、组织内 [英文文档站仓库](https://github.com/itick-org/docs.en) / [中文文档仓库](https://github.com/itick-org/docs) / [繁体文档仓库](https://github.com/itick-org/docs.hk)。

- **官网**：[https://itick.org](https://itick.org)  
- **GitHub 组织**：[https://github.com/itick-org](https://github.com/itick-org)（含各语言 [SDK](https://github.com/itick-org/python-sdk) 等）

### 特点（摘自官方介绍）

- **开发者友好**：标准易用接口、简明文档与丰富示例，便于快速接入。  
- **产品线丰富**：多市场股票、外汇、指数、加密货币等实时与历史数据。  
- **多场景适用**：量化团队、金融科技与专业分析等场景。  
- **服务与基础设施**：专业数据源、多地区加速与链路热备份，侧重实时与稳定。  
- **定制化**：机构与专业用户可洽谈定制数据方案。

### iTick API 类型与本项目范围

| 类型 | 说明 | 本 MCP |
|------|------|--------|
| **REST** | 通过市场数据端点获取报价、K 线等；请求需按文档携带 token 等鉴权信息。 | **已实现**（仅 HTTP GET 覆盖的 REST 能力） |
| **Websocket** | 发布/订阅，推送订单、成交、行情等，减少轮询。 | **未实现** |
| **FIX** | 高吞吐、机构级连接；当前主要面向机构客户。 | **未实现**（非 REST） |

FIX 仅机构开放时，可联系官方客服：[Telegram @iticksupport](https://t.me/iticksupport)、[WhatsApp +852 59046663](https://wa.me/85259046663)。

### 技术支持（摘要）

- **邮件**：[support@itick.org](mailto:support@itick.org)（建议主题中注明环境、身份与问题描述）  
- **营业时间**：周一至周五 9:00–18:00（香港时间）；紧急生产问题以官方说明为准。  
- **非办公时间**：可登录 [itick.org](https://itick.org) 通过站内即时消息联系在线客服。

---

## Setup

```bash
cd itick-mcp-server
pip install -e .
# 若只有 python3：pip3 install -e .
```

环境变量：

| 变量 | 说明 |
|------|------|
| `ITICK_TOKEN` | 必填（实际调用时）：请求头 `token`，见 [REST 文档](https://docs.itick.org/) |
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

## OpenCode

完整步骤（虚拟环境、配置文件路径、`opencode mcp` CLI、超时与排错）见 **[docs/opencode.md](docs/opencode.md)**。

OpenCode 使用 `opencode.json` / `opencode.jsonc` 的 `mcp` 键，本地服务需将 `type` 设为 `"local"`，`command` 为字符串数组，环境变量放在 `environment` 中（与 Cursor 的 `mcpServers` / `env` 不同）。最小示例：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "itick": {
      "type": "local",
      "command": ["itick-mcp"],
      "enabled": true,
      "environment": {
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

## 相关资源

- 官方 Python SDK（含 REST / WebSocket 等）：[itick-org/python-sdk](https://github.com/itick-org/python-sdk)  
- 其他语言 SDK 见 [github.com/itick-org](https://github.com/itick-org) 组织仓库列表

## 代码结构

- `itick_mcp_server/client.py` — HTTP GET、`ITICK_API_BASE` / `ITICK_TOKEN`
- `itick_mcp_server/tools_register.py` — 注册全部 REST 工具
- `itick_mcp_server/server.py` — FastMCP 入口
