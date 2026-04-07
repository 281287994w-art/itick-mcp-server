"""iTick REST API as MCP tools — see https://docs.itick.org/"""

from __future__ import annotations

import argparse
import logging
import sys

from mcp.server.fastmcp import FastMCP

from config import TRANSPORT_MODE
from tools_register import register_rest_tools

log = logging.getLogger(__name__)

mcp = FastMCP("itick-mcp-server")
register_rest_tools(mcp)


def main() -> None:
    global TRANSPORT_MODE
    logging.basicConfig(level=logging.INFO)
    
    parser = argparse.ArgumentParser(description="iTick MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http","sse"],
        default="stdio",
        help="Transport mode: stdio (default) or http",
    )
    
    args = parser.parse_args()
    TRANSPORT_MODE = args.transport
    
    if args.transport == "http":
        log.info("Starting iTick MCP Server in HTTP mode")
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        log.info("Starting iTick MCP Server in sse mode")
        mcp.run(transport="sse")
    else:
        log.info("Starting iTick MCP Server in stdio mode")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
