"""
SSE 客户端使用示例

此脚本演示如何连接到以 SSE 模式运行的 iTick MCP Server。

使用前请确保：
1. iTick MCP Server 已以 SSE 模式启动（设置 ITICK_SSE_PORT 环境变量）
2. 已正确配置 ITICK_TOKEN
"""

import asyncio
from mcp.client.sse import sse_client


async def main():
    # SSE 服务器地址
    sse_url = "http://localhost:8000/sse"
    
    print(f"🔌 正在连接到 {sse_url} ...")
    
    async with sse_client(sse_url) as client:
        print("✅ 连接成功！\n")
        
        # 列出所有可用工具
        print("📋 可用工具列表:")
        tools = await client.list_tools()
        for i, tool in enumerate(tools.tools, 1):
            print(f"  {i}. {tool.name}: {tool.description}")
        
        print(f"\n共 {len(tools.tools)} 个工具\n")
        
        # 示例：调用股票 Tick 工具
        print("📊 示例：获取腾讯控股 (00700.HK) 实时行情")
        result = await client.call_tool(
            name="stockTick",
            arguments={"region": "HK", "code": "00700"}
        )
        print(f"结果：{result}\n")
        
        # 示例：调用 K 线工具
        print("📈 示例：获取腾讯控股 (00700.HK) K 线数据")
        kline_result = await client.call_tool(
            name="stockKline",
            arguments={
                "region": "HK",
                "code": "00700",
                "k_type": 1,  # 1 分钟 K 线
                "limit": 5
            }
        )
        print(f"结果：{kline_result}\n")
        
        # 示例：批量获取行情
        print("📊 示例：批量获取多只股票行情")
        batch_result = await client.call_tool(
            name="stockTicks",
            arguments={
                "region": "HK",
                "codes": "00700,09988,03690"
            }
        )
        print(f"结果：{batch_result}\n")


if __name__ == "__main__":
    asyncio.run(main())
