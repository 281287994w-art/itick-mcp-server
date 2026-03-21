"""iTick REST API as MCP tools — see https://docs.itick.org/"""

from __future__ import annotations

import logging

from mcp.server.fastmcp import FastMCP

from itick_mcp_server.tools_register import register_rest_tools

log = logging.getLogger(__name__)

mcp = FastMCP("itick-mcp-server")
register_rest_tools(mcp)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    mcp.run()


if __name__ == "__main__":
    main()
