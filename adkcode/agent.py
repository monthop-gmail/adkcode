"""adkcode — AI coding agent powered by Google ADK."""

import os

from google.adk.agents import Agent

from . import tools

# Base system prompt
BASE_PROMPT = """You are a helpful coding assistant. You have access to tools for:
- Reading, writing, and editing files
- Listing directories and searching text in files
- Executing shell commands
- Searching the web and fetching URLs

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


root_agent = Agent(
    model="gemini-2.0-flash",
    name="adkcode",
    description="AI coding agent with file, shell, search, and web tools.",
    instruction=build_instruction(),
    tools=[
        tools.read_file,
        tools.write_file,
        tools.edit_file,
        tools.list_files,
        tools.grep,
        tools.shell,
        tools.web_search,
        tools.web_fetch,
    ],
)
