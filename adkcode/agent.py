"""adkcode — AI coding agent powered by Google ADK."""

import os
import logging

from google.adk.agents import Agent

from . import tools
from .mcp_config import load_mcp_config

logger = logging.getLogger(__name__)

# Base system prompt
BASE_PROMPT = """You are a helpful coding assistant. You have access to tools for:
- Reading, writing, and editing files
- Listing directories and searching text in files
- Executing shell commands
- Searching the web and fetching URLs

You may also have access to additional tools from MCP servers.

Use these tools to help the user with their coding tasks.
Be concise and direct in your responses.
Always read a file before editing it.
"""


def load_agents_md() -> str:
    """Load AGENTS.md from the current working directory if it exists."""
    candidates = ["agents.md", "AGENTS.md", "Agents.md"]
    for name in candidates:
        path = os.path.join(os.getcwd(), name)
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    return content
            except Exception:
                pass
    return ""


def build_instruction() -> str:
    """Build the full instruction with AGENTS.md content if available."""
    instruction = BASE_PROMPT
    agents_md = load_agents_md()
    if agents_md:
        instruction += f"\n\n# Project Instructions (from agents.md)\n\n{agents_md}"
    return instruction


def build_mcp_tools() -> list:
    """Load MCP tools from mcp.json config."""
    config = load_mcp_config()
    servers = config.get("mcpServers", {})

    if not servers:
        return []

    mcp_tools = []

    try:
        from google.adk.tools.mcp_tool import McpToolset
        from google.adk.tools.mcp_tool.mcp_session_manager import (
            SseConnectionParams,
            StdioConnectionParams,
        )
        from mcp import StdioServerParameters
    except ImportError:
        logger.warning("MCP dependencies not installed. Run: pip install google-adk[mcp]")
        return []

    for name, server_config in servers.items():
        try:
            tool_filter = server_config.get("tool_filter")

            if "url" in server_config:
                # Remote MCP server (SSE)
                params = SseConnectionParams(
                    url=server_config["url"],
                    headers=server_config.get("headers", {}),
                )
                logger.info(f"MCP [{name}]: SSE → {server_config['url']}")
            elif "command" in server_config:
                # Local MCP server (stdio)
                env = {**os.environ, **server_config.get("env", {})}
                params = StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command=server_config["command"],
                        args=server_config.get("args", []),
                        env=env,
                    ),
                )
                logger.info(f"MCP [{name}]: stdio → {server_config['command']} {' '.join(server_config.get('args', []))}")
            else:
                logger.warning(f"MCP [{name}]: skipped — need 'command' or 'url'")
                continue

            toolset_kwargs = {"connection_params": params}
            if tool_filter:
                toolset_kwargs["tool_filter"] = tool_filter

            mcp_tools.append(McpToolset(**toolset_kwargs))
        except Exception as e:
            logger.error(f"MCP [{name}]: failed — {e}")

    return mcp_tools


# Build tools list
agent_tools = [
    tools.read_file,
    tools.write_file,
    tools.edit_file,
    tools.list_files,
    tools.grep,
    tools.shell,
    tools.web_search,
    tools.web_fetch,
]

# Add MCP tools if configured
agent_tools.extend(build_mcp_tools())

root_agent = Agent(
    model="gemini-2.0-flash",
    name="adkcode",
    description="AI coding agent with file, shell, search, web, and MCP tools.",
    instruction=build_instruction(),
    tools=agent_tools,
)
