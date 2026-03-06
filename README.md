# adkcode

AI coding agent powered by [Google ADK](https://google.github.io/adk-docs/) (Agent Development Kit). Same coding tools as [gocode](https://github.com/monthop-gmail/gocode) but built on Google's agent framework with Gemini models.

## Features

- **Google ADK framework** — agent loop, session management, streaming built-in
- **3 ways to use** — Web UI (`adk web`), CLI REPL (`adk run`), API server (`adk api_server`)
- **Gemini models** — powered by `gemini-2.0-flash` (configurable)
- **8 coding tools** — read, write, edit, list, grep, shell, web_search, web_fetch
- **AGENTS.md support** — project-specific instructions loaded automatically
- **[MCP support](docs/mcp.md)** — connect to external tools via Model Context Protocol

## Quick Start

### 1. Clone & configure

```bash
git clone https://github.com/monthop-gmail/adkcode.git
cd adkcode
cp .env.example .env
# Edit .env — add your Gemini API key from https://aistudio.google.com
```

### 2. Run with Docker Compose

```bash
docker compose up -d
```

Open http://localhost:8000 — select `adkcode` from the dropdown and start chatting!

### 3. Run locally (without Docker)

```bash
pip install -r requirements.txt

# Web UI
adk web --port 8000

# CLI REPL
adk run adkcode

# API Server
adk api_server --port 8000
```

## Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create or overwrite files |
| `edit_file` | Partial edit via find & replace |
| `list_files` | List directory contents |
| `grep` | Search text in files recursively |
| `web_search` | Search the web via DuckDuckGo |
| `web_fetch` | Fetch content from a URL |
| `shell` | Execute shell commands |

## AGENTS.md

Place an `AGENTS.md` file in your working directory to give adkcode project-specific instructions.

```markdown
# AGENTS.md
- Always respond in Thai
- Use Python conventions
- Write tests for every new function
```

See [gocode/examples/agents-md/](https://github.com/monthop-gmail/gocode/tree/master/examples/agents-md) for 21 ready-to-use templates.

## MCP (Model Context Protocol)

adkcode supports MCP servers out of the box. Create a `mcp.json` in your project root:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx" }
    },
    "remote-server": {
      "url": "https://my-mcp-server.com/sse",
      "headers": { "Authorization": "Bearer xxx" }
    }
  }
}
```

Supports both **stdio** (local) and **SSE** (remote) MCP servers. Uses the same format as Claude Code / Cursor.

See `mcp.json.example` for more examples and **[docs/mcp.md](docs/mcp.md)** for the full guide.

## Configuration

Set your API key in `.env`:

```bash
GOOGLE_API_KEY=your-api-key-here
```

To change the model, edit `adkcode/agent.py`:

```python
root_agent = Agent(
    model="gemini-2.0-flash",  # or "gemini-2.5-pro", "gemini-2.5-flash"
    ...
)
```

## Project Structure

```
adkcode/
├── adkcode/
│   ├── __init__.py         # Exports root_agent
│   ├── agent.py            # Agent definition + AGENTS.md + MCP loader
│   ├── tools.py            # 8 coding tools
│   └── mcp_config.py       # MCP server config loader
├── docs/
│   └── mcp.md              # MCP guide
├── requirements.txt
├── mcp.json.example
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## gocode vs adkcode

Both are open-source AI coding agents with the same 8 tools and AGENTS.md support — but built differently:

| | [gocode](https://github.com/monthop-gmail/gocode) | [adkcode](https://github.com/monthop-gmail/adkcode) |
|---|--------|---------|
| Language | Go | Python |
| Framework | Custom HTTP + WebSocket server | Google ADK |
| LLM | Any OpenAI-compatible (DeepSeek, Qwen, Groq, OpenAI, Ollama) | Gemini |
| Interface | CLI REPL + one-shot | Web UI + CLI REPL + API server |
| MCP support | - (planned) | Yes (stdio + SSE) |
| Config | `.env` / `config.yaml` | `.env` |
| Session | In-memory | ADK built-in |
| Deployment | Docker Compose / binary | Docker Compose / `pip install` |
| Lines of code | ~1,500 | ~300 |
| Best for | ใช้กับ LLM provider ที่หลากหลาย | ใช้กับ Gemini + ต้องการ Web UI สำเร็จรูป |

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full development plan.

**Next up:**
- Multi-Agent (orchestrator + coder + reviewer + test agents)
- Multi-Model (Pro for hard tasks, Flash for easy tasks)
- Safety guardrails (confirm before dangerous commands)

## Contributing

Contributions are welcome! Check the [Roadmap](ROADMAP.md) for ideas and open a PR.

## License

MIT
