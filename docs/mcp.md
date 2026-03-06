# MCP (Model Context Protocol) Guide

## MCP คืออะไร?

MCP (Model Context Protocol) เป็น open standard ที่สร้างโดย Anthropic เพื่อให้ AI agents สามารถเชื่อมต่อกับ tools, data sources และ services ภายนอกได้แบบมาตรฐาน

แทนที่จะเขียน tool เองทุกอย่าง คุณสามารถเชื่อมต่อ MCP servers ที่มีอยู่แล้วหลายร้อยตัว เช่น GitHub, PostgreSQL, Slack, Google Drive และอื่นๆ

```
adkcode Agent
    ├── Built-in tools (read_file, shell, grep, ...)
    └── MCP tools (จาก mcp.json)
         ├── GitHub server → create_issue, list_prs, ...
         ├── PostgreSQL server → query, list_tables, ...
         └── Custom server → your_custom_tools, ...
```

## Quick Start

### 1. สร้าง mcp.json

สร้างไฟล์ `mcp.json` ไว้ที่ root ของ project:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
    }
  }
}
```

### 2. รัน adkcode

```bash
adk web --port 8000
# หรือ
adk run adkcode
```

adkcode จะโหลด MCP servers จาก `mcp.json` อัตโนมัติ

## Connection Types

### Stdio (Local Server)

รัน MCP server เป็น child process สื่อสารผ่าน stdin/stdout เหมาะสำหรับ tools ที่รันบนเครื่องเดียวกัน

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "package-name", "arg1", "arg2"],
      "env": {
        "API_KEY": "xxx"
      }
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `command` | Yes | คำสั่งที่จะรัน |
| `args` | No | arguments ของคำสั่ง |
| `env` | No | environment variables เพิ่มเติม |
| `tool_filter` | No | เลือกเฉพาะบาง tools (array of names) |

### SSE (Remote Server)

เชื่อมต่อ MCP server ที่รันอยู่ที่อื่นผ่าน HTTP Server-Sent Events เหมาะสำหรับ shared servers หรือ cloud services

```json
{
  "mcpServers": {
    "remote-server": {
      "url": "https://my-mcp-server.com/sse",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | SSE endpoint URL |
| `headers` | No | HTTP headers (เช่น auth token) |
| `tool_filter` | No | เลือกเฉพาะบาง tools (array of names) |

## Popular MCP Servers

### Filesystem

อ่าน/เขียนไฟล์ผ่าน MCP (ปลอดภัยกว่า built-in tools เพราะจำกัด directory ได้)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### GitHub

จัดการ repos, issues, PRs บน GitHub

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

Tools ที่ได้: `create_repository`, `search_repositories`, `create_issue`, `list_issues`, `create_pull_request`, `search_code` และอื่นๆ

### PostgreSQL

Query database โดยตรง

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost:5432/mydb"]
    }
  }
}
```

### Slack

ส่ง/อ่านข้อความใน Slack

```json
{
  "mcpServers": {
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-xxxxxxxxxxxx"
      }
    }
  }
}
```

### Google Drive

อ่าน/ค้นหาไฟล์ใน Google Drive

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

### Brave Search

ค้นหาเว็บผ่าน Brave Search API

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "BSA_xxxxxxxxxxxx"
      }
    }
  }
}
```

## Google MCP Servers

Google มี MCP servers อย่างเป็นทางการหลายตัว ทั้งแบบ open-source และ managed service:

### Google Maps Platform

Code assist toolkit สำหรับ Maps API — ช่วยเขียนโค้ดที่ใช้ Google Maps ได้ถูกต้องตาม docs ล่าสุด

```json
{
  "mcpServers": {
    "google-maps": {
      "command": "npx",
      "args": ["-y", "@googlemaps/code-assist-mcp@latest"]
    }
  }
}
```

Tools ที่ได้: code assistance สำหรับ Maps JavaScript API, Places API, Geocoding API, Routes API และอื่นๆ

### Google Drive (by Anthropic)

อ่าน/ค้นหาไฟล์ใน Google Drive ผ่าน OAuth

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"]
    }
  }
}
```

Tools ที่ได้: `search`, `read_file` — ต้อง OAuth2 authentication ตอนรันครั้งแรก

### Google Workspace (Community)

ครอบคลุม Gmail, Calendar, Docs, Sheets, Slides, Chat, Tasks, Drive ในตัวเดียว

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "uvx",
      "args": ["google-workspace-mcp"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/path/to/client_secret.json"
      }
    }
  }
}
```

Tools ที่ได้: `gmail_send`, `calendar_create_event`, `docs_create`, `sheets_read`, `drive_search` และอื่นๆ

> ที่มา: [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp)

### MCP Toolbox for Databases (by Google)

รองรับ BigQuery, Cloud SQL, AlloyDB, Spanner, Firestore — เชื่อมต่อ Google Cloud databases

```json
{
  "mcpServers": {
    "toolbox-db": {
      "command": "toolbox",
      "args": ["--tools-file", "tools.yaml", "--mcp"]
    }
  }
}
```

ติดตั้ง:
```bash
# macOS / Linux
brew install mcp-toolbox

# หรือ Docker
docker run -p 5000:5000 us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest

# Python SDK (สำหรับ ADK)
pip install toolbox-adk
```

> ที่มา: [googleapis/genai-toolbox](https://github.com/googleapis/genai-toolbox)

### gcloud CLI MCP

ใช้ Google Cloud CLI ผ่าน MCP — จัดการ Cloud resources ทุกอย่าง

```json
{
  "mcpServers": {
    "gcloud": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/gcloud-mcp"]
    }
  }
}
```

> ที่มา: [googleapis/gcloud-mcp](https://github.com/googleapis/gcloud-mcp)

### Chrome DevTools

Debug เว็บไซต์ผ่าน Chrome DevTools Protocol

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/chrome-devtools-mcp"]
    }
  }
}
```

Tools ที่ได้: inspect DOM, network requests, console logs, screenshots, performance profiling

> ที่มา: [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)

### Google Cloud Managed MCP Servers (Remote)

Google Cloud ให้บริการ managed MCP servers แบบ remote (SSE) สำหรับ enterprise:

| Service | Description |
|---------|-------------|
| BigQuery | Query และจัดการ data warehouse |
| Maps Grounding Lite | Geospatial data สำหรับ AI agents |
| GKE (Kubernetes Engine) | จัดการ Kubernetes clusters |
| GCE (Compute Engine) | จัดการ VMs |
| Cloud Storage | จัดการ object storage |
| Cloud Run | Deploy และจัดการ serverless containers |
| Security Operations | Chronicle + Security Command Center |

ใช้งานผ่าน Google Cloud Console โดยไม่ต้องติดตั้งอะไรเพิ่ม — ต้องมี Google Cloud account และ IAM permissions

> ดูรายละเอียด: [Google Cloud MCP Overview](https://docs.google.com/mcp/overview)

## Tool Filtering

ใช้ `tool_filter` เพื่อเลือกเฉพาะ tools ที่ต้องการจาก MCP server:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"
      },
      "tool_filter": ["search_repositories", "list_issues", "create_issue"]
    }
  }
}
```

ข้อดี:
- ลดจำนวน tools ที่ LLM ต้องเลือก (เร็วขึ้น, แม่นยำขึ้น)
- จำกัด permissions (เช่น อ่านได้อย่างเดียว ไม่ให้ delete)

## Multiple Servers

ใช้หลาย MCP servers พร้อมกันได้:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx" }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": { "SLACK_BOT_TOKEN": "xoxb-xxx" }
    }
  }
}
```

## Config File Location

adkcode จะค้นหา `mcp.json` ตามลำดับ:

1. Working directory (current directory)
2. Project root (ข้างๆ `adkcode/` folder)

## Security

- `mcp.json` อยู่ใน `.gitignore` — จะไม่ถูก commit ขึ้น git (อาจมี tokens/passwords)
- ใช้ `tool_filter` จำกัดสิทธิ์ tools ที่ agent เข้าถึงได้
- ใช้ environment variables สำหรับ secrets แทนการใส่ตรงใน config
- ตรวจสอบ MCP server ที่ใช้ว่าเชื่อถือได้

## Troubleshooting

### MCP tools ไม่โหลด

1. ตรวจสอบว่ามี `mcp.json` ใน directory ที่ถูกต้อง
2. ตรวจสอบ format JSON ถูกต้อง
3. ดู logs: `docker compose logs` หรือ terminal output

### npx command not found

ต้องติดตั้ง Node.js ก่อน:

```bash
# ใน Dockerfile เพิ่ม
RUN apt-get install -y nodejs npm
```

### Connection refused (SSE)

ตรวจสอบว่า remote MCP server กำลังรันอยู่และ URL ถูกต้อง

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Servers Directory](https://github.com/modelcontextprotocol/servers)
- [Google ADK MCP Docs](https://google.github.io/adk-docs/tools-custom/mcp-tools/)
- [MCP GitHub](https://github.com/modelcontextprotocol/modelcontextprotocol)
- [Google MCP Servers](https://github.com/google/mcp) — รวม MCP servers จาก Google ทั้งหมด
- [Google Cloud MCP Overview](https://docs.cloud.google.com/mcp/overview) — Managed MCP servers
- [MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox) — BigQuery, Cloud SQL, AlloyDB, Spanner
- [Google Workspace MCP](https://github.com/taylorwilsdon/google_workspace_mcp) — Gmail, Calendar, Docs, Sheets
