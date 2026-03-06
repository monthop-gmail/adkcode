# Roadmap

## Phase 1 — Core ✅

- [x] Google ADK agent with Gemini model
- [x] 8 coding tools: read_file, write_file, edit_file, list_files, grep, shell, web_search, web_fetch
- [x] AGENTS.md support — project-specific instructions
- [x] MCP support — stdio + SSE connections, Google MCP servers documented
- [x] Docker Compose setup
- [x] .env configuration
- [x] Documentation (README, docs/mcp.md)

## Phase 2 — Multi-Agent ✅

ADK `sub_agents` parameter — LLM route request ไป agent ที่เหมาะสมอัตโนมัติ:

- [x] Orchestrator pattern — root agent สั่งงาน sub-agents
- [x] Coder agent — เขียน/แก้โค้ดโดยเฉพาะ
- [x] Reviewer agent — review โค้ด (read-only, ไม่แก้ไฟล์)
- [x] Test agent — รัน test + วิเคราะห์ผลอัตโนมัติ
- [x] Agent routing — LLM เลือก agent ตาม description อัตโนมัติ

```
adkcode (orchestrator) — web_search, web_fetch, MCP tools
    ├── coder    → เขียน/แก้โค้ด (read, write, edit, list, grep, shell)
    ├── reviewer → review โค้ด (read, list, grep — read-only)
    └── tester   → รัน test + แก้ bug (read, write, edit, list, grep, shell)
```

## Phase 3 — Multi-Model ✅

- [x] Multi-model — smart model (orchestrator, reviewer) + fast model (coder, tester)
- [x] Configurable via env vars — `ADKCODE_MODEL_SMART`, `ADKCODE_MODEL_FAST`
- [x] Default: `gemini-2.5-flash` (smart) + `gemini-2.0-flash` (fast)
- [x] Image understanding — `read_image` tool ใช้ Gemini vision อ่านรูป/screenshot แล้วเขียนโค้ด
- [ ] Context management — summarize/compress เมื่อ token ใกล้ limit
- [ ] Cost tracking — ประมาณ token usage ต่อ session

## Phase 4 — Safety & Guardrails ✅

- [x] Shell safety — block destructive commands (rm -rf /, mkfs, fork bomb), warn on dangerous ones (sudo, force push, DROP TABLE)
- [x] File access whitelist — `ADKCODE_ALLOWED_DIRS` จำกัด directory ที่ agent เข้าถึงได้
- [x] Sensitive file protection — block .env reads, /etc/shadow, /etc/passwd
- [x] Audit log — `ADKCODE_AUDIT_LOG` บันทึก tool calls ทั้งหมดเป็น JSON lines
- [ ] Rate limiting — จำกัดจำนวน requests / token budget

## Phase 5 — Better Tools

- [ ] Git tools — git status, diff, commit, log (ไม่ต้องผ่าน shell)
- [ ] Test runner — รัน test framework อัตโนมัติ (pytest, jest, go test)
- [ ] Code analysis — static analysis, linting
- [ ] File watcher — detect การเปลี่ยนแปลงไฟล์ภายนอก

## Phase 6 — Production Ready

- [ ] Authentication — API key / OAuth สำหรับ Web UI
- [ ] Session persistence — เก็บ history ข้ามวัน (database backend)
- [ ] Multi-user — แยก workspace ต่อ user
- [ ] Logging & monitoring — structured logs, metrics
- [ ] VS Code extension

## Ideas (Unscheduled)

- [x] RAG — semantic code search ด้วย Gemini embeddings (index_codebase + semantic_search)
- [x] Plugin system — โหลด knowledge-work plugins (skills, commands) จาก `plugins/` directory
- [x] Engineering plugin — code review, testing strategy, debugging, architecture, incident response
- [ ] Voice input/output
- [ ] More plugins — sales, data, productivity, etc.
- [ ] Agent marketplace — share/install custom agents
- [ ] Git-aware context — auto-include changed files
- [ ] Self-improving — agent เรียนรู้จาก feedback

---

Want to contribute? Pick any unchecked item and open a PR!
