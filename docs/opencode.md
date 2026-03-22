# 将 itick-mcp-server 接入 OpenCode

[OpenCode](https://open-code.ai) 通过配置文件里的 **`mcp`** 段加载 MCP。本教程说明如何把本仓库的 **stdio** MCP 装进 OpenCode，并与仓库 [README](../README.md) 中的环境变量、工具列表保持一致。

## 前置条件

- 已安装 **OpenCode**，且能编辑其配置文件（见下文「配置文件放哪里」）。
- 本机 **Python ≥ 3.10**，以及 `pip`（或 `pip3`）。
- 在 [iTick 文档](https://docs.itick.org/) 申请 **`ITICK_TOKEN`**（调用接口时必填）。

## 1. 安装本 MCP（可编辑安装）

在仓库根目录执行：

```bash
cd /path/to/itick-mcp-server
pip install -e .
```

若系统只有 `python3`：

```bash
pip3 install -e .
```

安装成功后，终端应能直接运行：

```bash
itick-mcp
```

按 `Ctrl+C` 退出即可；OpenCode 会自行拉起进程，一般不需要长期手动运行。

### 使用虚拟环境（推荐）

```bash
cd /path/to/itick-mcp-server
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e .
```

记下虚拟环境里 **Python 可执行文件的绝对路径**（例如 macOS/Linux 上多为 `.../itick-mcp-server/.venv/bin/python`），下面「方式 B」会用到。

## 2. 在 OpenCode 里写入 `mcp` 配置

OpenCode 要求 **本地 MCP** 使用：

- `"type": "local"`
- **`command` 为字符串数组**（第一个元素是可执行文件，后面是参数）
- 环境变量写在 **`environment`** 里（不是 Cursor 的 `env`）

官方说明：[OpenCode MCP Servers](https://open-code.ai/docs/en/mcp-servers)。

### 方式 A：`itick-mcp` 已在 PATH 中

在 **`opencode.json`** 或 **`opencode.jsonc`** 中加入（可与现有配置合并）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "itick": {
      "type": "local",
      "command": ["itick-mcp"],
      "enabled": true,
      "environment": {
        "ITICK_TOKEN": "你的_itick_token"
      }
    }
  }
}
```

若你的环境使用 `https://api.itick.io` 作为 API 根地址，可追加：

```json
"ITICK_API_BASE": "https://api.itick.io"
```

### 方式 B：使用 `python -m`（适合未进 PATH 或固定某解释器）

把 **`/绝对路径/到/python`** 换成你本机的 Python（虚拟环境则用 `.venv/bin/python` 的绝对路径）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "itick": {
      "type": "local",
      "command": [
        "/绝对路径/到/python",
        "-m",
        "itick_mcp_server"
      ],
      "enabled": true,
      "environment": {
        "ITICK_TOKEN": "你的_itick_token"
      }
    }
  }
}
```

前提：该 Python 对应的环境里已执行过 `pip install -e .`，能 `import itick_mcp_server`。

### 可选：延长工具发现超时

本服务注册工具较多，若 OpenCode 启动时报获取工具超时，可为该 MCP 增加 **`timeout`**（毫秒），例如：

```json
"timeout": 15000
```

具体字段见 [Local Options](https://open-code.ai/docs/en/mcp-servers)。

## 3. 配置文件放哪里

OpenCode 会按优先级合并多处配置，常见位置包括：

- **全局**：`~/.config/opencode/opencode.json`
- **项目根目录**：`opencode.json` / `opencode.jsonc`
- 或通过环境变量 **`OPENCODE_CONFIG`** / **`OPENCODE_CONFIG_CONTENT`** 指定（见 [OpenCode Config](https://open-code.ai/docs/en/config)）

任选其一保存上述 `mcp.itick` 块即可；项目内配置便于团队共享结构（令牌建议仍用环境变量引用或本地覆盖，勿提交密钥）。

## 4. 用 CLI 检查（可选）

若已安装 OpenCode CLI，可尝试：

```bash
opencode mcp list
```

也可使用交互添加：

```bash
opencode mcp add
```

按提示填写与「方式 A」等价的 **`command` 数组** 和 **`environment`**。

## 5. 在对话里使用

配置生效并连接成功后，MCP 工具会出现在 OpenCode 的工具列表中。可在提示里写明使用 **itick** 相关工具（名称以 OpenCode 实际展示为准），例如查询行情、K 线等。工具与 REST 路径的对应关系见 [README 工具一览](../README.md)。

## 6. 常见问题

| 现象 | 处理 |
|------|------|
| 找不到 `itick-mcp` | 改用「方式 B」，或激活 venv 后确认 `which itick-mcp` |
| `ModuleNotFoundError: itick_mcp_server` | 对「方式 B」里用的那个 Python 执行 `pip install -e .` |
| 401 / 无数据 | 检查 `ITICK_TOKEN` 是否正确、是否过期 |
| 接口域名不对 | 设置 `ITICK_API_BASE` 为文档或控制台提供的地址 |

---

更多关于 iTick 能力与限制，见仓库根目录 [README](../README.md)。
