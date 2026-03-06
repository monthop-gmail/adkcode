# Roadmap

## Phase 1 — Core (Done)

- [x] Google ADK agent with Gemini model
- [x] 8 coding tools: read_file, write_file, edit_file, list_files, grep, shell, web_search, web_fetch
- [x] AGENTS.md support — project-specific instructions
- [x] MCP support — stdio + SSE connections
- [x] Docker Compose setup
- [x] .env configuration
- [x] Documentation (README, docs/mcp.md)

## Phase 2 — Multi-Agent

ADK รองรับ sub-agents — ใช้ประโยชน์จากจุดแข็งนี้:

- [ ] Orchestrator pattern — root agent สั่งงาน sub-agents
- [ ] Coder agent — เขียน/แก้โค้ดโดยเฉพาะ
- [ ] Reviewer agent — review โค้ดก่อน commit
- [ ] Test agent — รัน test + วิเคราะห์ผลอัตโนมัติ
- [ ] Agent routing — เลือก agent ที่เหมาะกับงานอัตโนมัติ

```
adkcode (orchestrator)
    ├── coder-agent    → เขียน/แก้โค้ด
    ├── reviewer-agent → review โค้ด
    └── test-agent     → รัน test + แก้ bug
```

## Phase 3 — Multi-Model & Intelligence

- [ ] Multi-model — Gemini 2.5 Pro สำหรับงานยาก + Flash สำหรับงานเบา
- [ ] Auto model selection — เลือก model ตามความซับซ้อนของงาน
- [ ] Image understanding — ใช้ Gemini vision อ่านรูป/screenshot แล้วเขียนโค้ด
- [ ] Context management — summarize/compress เมื่อ token ใกล้ limit
- [ ] Cost tracking — ประมาณ token usage ต่อ session

## Phase 4 — Safety & Guardrails

- [ ] Callbacks — safety check ก่อนรัน shell command อันตราย (rm -rf, drop table)
- [ ] File access whitelist — จำกัด directory ที่ agent เข้าถึงได้
- [ ] Rate limiting — จำกัดจำนวน requests / token budget
- [ ] Audit log — บันทึก tool calls ทั้งหมด

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

- [ ] RAG — index codebase สำหรับ search ที่แม่นยำขึ้น
- [ ] Voice input/output
- [ ] Custom slash commands (/commit, /test, /review, /deploy)
- [ ] Agent marketplace — share/install custom agents
- [ ] Git-aware context — auto-include changed files
- [ ] Self-improving — agent เรียนรู้จาก feedback

---

Want to contribute? Pick any unchecked item and open a PR!
