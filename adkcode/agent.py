"""adkcode — Multi-agent AI coding system powered by Google ADK."""

import os
import logging

from google.adk.agents import Agent

from . import tools
from .mcp_config import load_mcp_config

logger = logging.getLogger(__name__)

# --- Model Configuration ---
# Smart model for routing & analysis, fast model for coding & testing
MODEL_SMART = os.environ.get("ADKCODE_MODEL_SMART", "gemini-2.5-flash")
MODEL_FAST = os.environ.get("ADKCODE_MODEL_FAST", "gemini-2.0-flash")

logger.info(f"Models: smart={MODEL_SMART}, fast={MODEL_FAST}")

# --- Specialized Prompts ---

ORCHESTRATOR_PROMPT = """You are adkcode, an AI coding agent orchestrator. You coordinate specialized sub-agents:

- **coder** — for writing, editing, and creating code files
- **reviewer** — for reviewing code quality, finding bugs, and suggesting improvements
- **tester** — for running tests, analyzing results, and fixing test failures

Route user requests to the appropriate agent:
- Coding tasks (write, edit, create, fix, refactor) → coder
- Implement UI from screenshot/mockup → coder (has read_image)
- Code review, analysis, explain code → reviewer
- Compare screenshot with UI code → reviewer (has read_image)
- Run tests, check test results, fix failing tests → tester
- General questions, web search, research → handle yourself

You also have web search and URL fetching tools for research tasks.
Be concise and direct in your responses.
"""

CODER_PROMPT = """You are a specialized coding agent. Your job is to write, edit, and create code files.

Guidelines:
- Always read a file before editing it
- Use edit_file for small changes (find & replace), write_file for new files or full rewrites
- Write clean, well-structured code
- Use shell to run commands when needed (install packages, build, etc.)
- Use read_image to analyze screenshots, mockups, or diagrams and implement matching code
- Be concise — show what you changed, not lengthy explanations
"""

REVIEWER_PROMPT = """You are a specialized code review agent. Your job is to analyze code quality.

Guidelines:
- Read the code carefully before reviewing
- Look for: bugs, security issues, performance problems, code smells
- Suggest specific improvements with examples
- You have READ-ONLY access — you cannot modify files
- Use read_image to analyze screenshots/mockups and compare with actual UI implementation
- Be constructive and concise
- Rate severity: critical, warning, suggestion
"""

TESTER_PROMPT = """You are a specialized testing agent. Your job is to run tests and ensure code quality.

Guidelines:
- Use shell to run test commands (pytest, jest, go test, etc.)
- Analyze test output — identify failures and root causes
- Fix failing tests by editing test files or source code
- Create test files when asked
- Report test coverage and results clearly
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


def build_instruction(base_prompt: str) -> str:
    """Build the full instruction with AGENTS.md content if available."""
    instruction = base_prompt
    agents_md = load_agents_md()
    if agents_md:
        instruction += f"\n\n# Project Instructions (from AGENTS.md)\n\n{agents_md}"
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


# --- Sub-Agents ---

coder = Agent(
    model=MODEL_FAST,
    name="coder",
    description="Writes, edits, and creates code files. Use for any coding task: write new code, edit existing files, fix bugs, refactor, create projects. Can also read images/screenshots to implement matching code.",
    instruction=build_instruction(CODER_PROMPT),
    tools=[
        tools.read_file,
        tools.write_file,
        tools.edit_file,
        tools.list_files,
        tools.grep,
        tools.shell,
        tools.read_image,
    ],
)

reviewer = Agent(
    model=MODEL_SMART,
    name="reviewer",
    description="Reviews code for bugs, security issues, and best practices. Read-only analysis — does not modify files. Can read images/screenshots to review UI implementations.",
    instruction=build_instruction(REVIEWER_PROMPT),
    tools=[
        tools.read_file,
        tools.list_files,
        tools.grep,
        tools.read_image,
    ],
)

tester = Agent(
    model=MODEL_FAST,
    name="tester",
    description="Runs tests, analyzes test results, and fixes failing tests. Use for pytest, jest, go test, or any test framework.",
    instruction=build_instruction(TESTER_PROMPT),
    tools=[
        tools.read_file,
        tools.write_file,
        tools.edit_file,
        tools.list_files,
        tools.grep,
        tools.shell,
    ],
)

# --- Orchestrator (Root Agent) ---

orchestrator_tools = [
    tools.web_search,
    tools.web_fetch,
]
orchestrator_tools.extend(build_mcp_tools())

root_agent = Agent(
    model=MODEL_SMART,
    name="adkcode",
    description="AI coding agent orchestrator with specialized sub-agents for coding, reviewing, and testing.",
    instruction=build_instruction(ORCHESTRATOR_PROMPT),
    tools=orchestrator_tools,
    sub_agents=[coder, reviewer, tester],
)
