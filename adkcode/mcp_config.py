"""MCP server configuration loader for adkcode."""

import json
import os
from typing import Any


def load_mcp_config() -> dict[str, Any]:
    """Load MCP server config from mcp.json in working directory or agent directory.

    Expected format (same as Claude Code / Cursor):
    {
        "mcpServers": {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
            },
            "remote-server": {
                "url": "https://my-mcp-server.com/sse",
                "headers": {
                    "Authorization": "Bearer xxx"
                }
            }
        }
    }
    """
    candidates = [
        os.path.join(os.getcwd(), "mcp.json"),
        os.path.join(os.path.dirname(__file__), "..", "mcp.json"),
    ]

    for path in candidates:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                if "mcpServers" in config:
                    return config
            except Exception:
                pass

    return {"mcpServers": {}}
