# adkcode

AI coding agent powered by [Google ADK](https://google.github.io/adk-docs/) (Agent Development Kit). Same coding tools as [gocode](https://github.com/monthop-gmail/gocode) but built on Google's agent framework with Gemini models.

## Features

- **Google ADK framework** — agent loop, session management, streaming built-in
- **3 ways to use** — Web UI (`adk web`), CLI REPL (`adk run`), API server (`adk api_server`)
- **Multi-model** — smart model for analysis + fast model for execution (configurable)
- **Multi-agent system** — orchestrator + coder + reviewer + tester agents
- **11 coding tools** — read, write, edit, list, grep, shell, web_search, web_fetch, read_image, index_codebase, semantic_search
- **RAG search** — semantic code search using Gemini embeddings (free)
- **[AGENTS.md support](docs/agents-md.md)** — project-specific instructions loaded automatically
- **[MCP support](docs/mcp.md)** — connect to external tools via Model Context Protocol
- **Plugin system** — load knowledge-work plugins (skills, commands) from `plugins/` directory
- **[Getting started guide](docs/getting-started.md)** — คู่มือใช้งานเบื้องต้น (ภาษาไทย)

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
| `read_image` | Analyze images/screenshots with Gemini vision |
| `shell` | Execute shell commands |
| `index_codebase` | Build semantic search index of source files |
| `semantic_search` | Search code by meaning using Gemini embeddings |

## RAG (Semantic Code Search)

adkcode can search your codebase by meaning, not just keywords:

```
> "index the project"
→ index_codebase(".") → Indexed 5 files, 12 chunks

> "find code related to safety checks"
→ semantic_search("safety checks") → guardrails.py (score: 0.87)

> "where is the MCP configuration loaded?"
→ semantic_search("MCP configuration") → mcp_config.py (score: 0.91)
```

How it works:
1. `index_codebase` scans source files and generates Gemini embeddings
2. Index is saved to `.adkcode_index.json` (reused across sessions)
3. `semantic_search` finds code by meaning using cosine similarity
4. Embeddings are **free** via Gemini Embedding API

## AGENTS.md

Place an `AGENTS.md` file in your working directory to give adkcode project-specific instructions.

```markdown
# AGENTS.md
- Always respond in Thai
- Use Python conventions
- Write tests for every new function
```

See [examples/agents-md/](examples/agents-md/) for 21 ready-to-use templates and **[docs/agents-md.md](docs/agents-md.md)** for the full guide.

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

## Multi-Agent Architecture

adkcode uses a multi-agent system where each agent has a specialized role:

```
adkcode (orchestrator) — web search, URL fetch, MCP tools
    ├── coder    → write, edit, create code + read images (read, write, edit, list, grep, shell, read_image)
    ├── reviewer → review code quality, find bugs (read, list, grep, read_image — read-only)
    └── tester   → run tests, fix failures (read, write, edit, list, grep, shell)
```

The orchestrator automatically routes your requests to the right agent based on what you ask. You can also ask for a specific agent:

- *"สร้างไฟล์ hello.py"* → routes to **coder**
- *"ดู screenshot.png แล้วเขียน HTML ตามนี้"* → routes to **coder** (read_image)
- *"review โค้ดใน agent.py"* → routes to **reviewer**
- *"รัน pytest"* → routes to **tester**
- *"ค้นหาข่าว AI"* → handled by **orchestrator** directly

## Configuration

Set your API key in `.env`:

```bash
GOOGLE_API_KEY=your-api-key-here
```

### Multi-Model (optional)

adkcode uses two model tiers — a **smart** model for analysis and a **fast** model for execution:

```bash
# Smart model — orchestrator + reviewer (routing, analysis)
ADKCODE_MODEL_SMART=gemini-2.5-flash

# Fast model — coder + tester (speed, execution)
ADKCODE_MODEL_FAST=gemini-2.0-flash
```

| Agent | Default Model | Role |
|-------|--------------|------|
| orchestrator | smart (`gemini-2.5-flash`) | Route requests, web search |
| reviewer | smart (`gemini-2.5-flash`) | Code analysis, find bugs |
| coder | fast (`gemini-2.0-flash`) | Write/edit code |
| tester | fast (`gemini-2.0-flash`) | Run tests, fix failures |

Use `gemini-2.5-pro` for the smart model if you need maximum quality.

### Safety & Guardrails

adkcode has built-in safety features to protect against dangerous operations:

**Shell command safety:**
- Destructive commands are blocked automatically (`rm -rf /`, `mkfs`, fork bombs)
- Dangerous commands show warnings (`sudo`, `git push --force`, `DROP TABLE`)

**File access control (optional):**
```bash
# Restrict agent to specific directories only
ADKCODE_ALLOWED_DIRS=/workspace,/home/user/projects
```

**Audit log (optional):**
```bash
# Log all tool calls to a JSON lines file
ADKCODE_AUDIT_LOG=/var/log/adkcode/audit.jsonl
```

Audit log format:
```json
{"timestamp": "2026-03-06T12:00:00Z", "agent": "coder", "tool": "shell", "args": {"command": "ls"}, "result": "success"}
```

## Plugin System

adkcode supports knowledge-work plugins that add domain skills and commands. Drop a plugin into `plugins/` and it's automatically loaded. Compatible with [Anthropic Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) format.

### Included Plugins

| Plugin | Skills | Commands |
|--------|:------:|:--------:|
| **engineering** | 6 | `/review`, `/debug`, `/standup`, `/architecture`, `/incident`, `/deploy-checklist` |
| **data** | 7 | `/write-query`, `/analyze`, `/explore-data`, `/create-viz`, `/build-dashboard`, `/validate` |
| **productivity** | 2 | `/start`, `/update` |

Skills are auto-routed to the right agent: code-review → reviewer, testing → tester, debug/docs → coder.

### Plugin Control

```bash
# Load specific plugins only (saves context window)
ADKCODE_PLUGINS=engineering,data

# Disable all plugins
ADKCODE_PLUGINS=none

# Load all (default)
# ADKCODE_PLUGINS=
```

### Plugin Structure

```
plugins/
└── engineering/
    ├── .claude-plugin/plugin.json  # Plugin metadata
    ├── skills/*/SKILL.md           # Domain knowledge (auto-injected)
    └── commands/*.md               # Slash commands
```

## Project Structure

```
adkcode/
├── adkcode/
│   ├── __init__.py         # Exports root_agent
│   ├── agent.py            # Multi-agent system (orchestrator + sub-agents)
│   ├── tools.py            # 11 coding tools
│   ├── rag.py              # RAG: semantic code search with embeddings
│   ├── guardrails.py       # Safety checks, file access, audit log
│   ├── mcp_config.py       # MCP server config loader
│   └── plugin_loader.py    # Plugin system (skills, commands, MCP)
├── plugins/
│   ├── engineering/        # Engineering skills & commands
│   ├── data/               # Data analysis, SQL, visualization
│   └── productivity/       # Task management, memory
├── docs/
│   ├── getting-started.md  # Getting started guide (Thai)
│   ├── agents-md.md        # AGENTS.md guide
│   └── mcp.md              # MCP guide
├── examples/
│   └── agents-md/          # 21 AGENTS.md templates
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
| LLM | Any OpenAI-compatible (DeepSeek, Qwen, Groq, OpenAI, Ollama) | Gemini (multi-model: smart + fast) |
| Interface | CLI REPL + one-shot | Web UI + CLI REPL + API server |
| Multi-agent | - | Yes (orchestrator + 3 sub-agents) |
| MCP support | - (planned) | Yes (stdio + SSE) |
| Config | `.env` / `config.yaml` | `.env` |
| Session | In-memory | ADK built-in |
| Deployment | Docker Compose / binary | Docker Compose / `pip install` |
| Lines of code | ~1,500 | ~300 |
| Best for | ใช้กับ LLM provider ที่หลากหลาย | ใช้กับ Gemini + ต้องการ Web UI สำเร็จรูป |

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full development plan.

**Next up:**
- Better tools (git, test runner, code analysis)
- Production ready (auth, persistence, multi-user)

## Contributing

Contributions are welcome! Check the [Roadmap](ROADMAP.md) for ideas and open a PR.

## License

MIT
