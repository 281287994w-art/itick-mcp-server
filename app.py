"""
魔搭社区部署配置文件
用于在魔搭社区 (ModelScope) 上部署 iTick MCP Server

使用说明：
1. 在魔搭社区创建实例时，设置以下环境变量：
   - ITICK_TOKEN: 你的 iTick API Token（必填）
   - ITICK_SSE_PORT: SSE 服务端口，默认 8000（可选）
   - ITICK_API_BASE: iTick API 基础地址，默认 https://api.itick.org（可选）

2. 启动命令：python app.py

3. 访问地址：http://<your-instance-url>:<ITICK_SSE_PORT>/sse
"""

import os
from itick_mcp_server.server import mcp, main

if __name__ == "__main__":
    # 确保设置了 SSE 端口
    if not os.environ.get("ITICK_SSE_PORT"):
        os.environ["ITICK_SSE_PORT"] = "8000"
    
    # 确保设置了 Token（魔搭社区环境下需要手动配置）
    token = os.environ.get("ITICK_TOKEN")
    if not token:
        print("⚠️  警告：未设置 ITICK_TOKEN 环境变量")
        print("请在魔搭社区实例配置中添加环境变量 ITICK_TOKEN")
        print("你可以从 https://itick.org 获取 API Token")
    
    print("=" * 60)
    print("🚀 iTick MCP Server - 魔搭社区部署版")
    print("=" * 60)
    print(f"SSE Port: {os.environ.get('ITICK_SSE_PORT')}")
    print(f"API Base: {os.environ.get('ITICK_API_BASE', 'https://api.itick.org')}")
    print(f"Token Configured: {'✅ Yes' if token else '❌ No'}")
    print("=" * 60)
    
    main()
