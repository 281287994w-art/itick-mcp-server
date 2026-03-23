#!/bin/bash

# iTick MCP Server 快速启动脚本（SSE 模式）

echo "🚀 iTick MCP Server - SSE 模式快速启动"
echo "======================================"

# 检查是否设置了 ITICK_TOKEN
if [ -z "$ITICK_TOKEN" ]; then
    echo "⚠️  警告：未设置 ITICK_TOKEN 环境变量"
    echo "请先设置：export ITICK_TOKEN=\"your_token\""
    echo ""
fi

# 设置默认端口
export ITICK_SSE_PORT=${ITICK_SSE_PORT:-8000}

echo "📋 配置信息:"
echo "  - SSE 端口：$ITICK_SSE_PORT"
echo "  - API Base: ${ITICK_API_BASE:-https://api.itick.org}"
echo "  - Token: ${ITICK_TOKEN:+已配置} ${ITICK_TOKEN:-未配置}"
echo ""

# 启动服务
echo "🔌 正在启动 SSE 服务器..."
echo "访问地址：http://localhost:$ITICK_SSE_PORT/sse"
echo ""

python3 -m itick_mcp_server
