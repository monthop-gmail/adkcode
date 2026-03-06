# คู่มือทดสอบ Engineering Plugin

Plugin นี้เพิ่ม **6 skills** และ **6 commands** สำหรับงาน software engineering

## สิ่งที่ต้องเตรียม

- adkcode รันอยู่ที่ http://localhost:8000
- เลือก agent `adkcode` จาก dropdown
- มีไฟล์โค้ดใน workspace สำหรับทดสอบ (หรือให้ agent สร้างให้)

---

## ทดสอบ Skills (ทำงานอัตโนมัติ)

Skills จะถูก inject เข้า agent prompts อัตโนมัติ ไม่ต้องเรียกตรง — แค่ถามในหัวข้อที่เกี่ยวข้อง

### 1. Code Review Skill → reviewer agent

ส่งโค้ดให้ review แล้วดูว่า agent ตอบตาม structured format หรือไม่

```
ช่วย review โค้ดนี้หน่อย:

def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    if result:
        session['user'] = username
        return redirect('/dashboard')
    return 'Login failed'
```

**ผลที่คาดหวัง:** agent ต้องชี้ปัญหา SQL injection, plain text password, XSS ฯลฯ พร้อมแยก severity (Critical/Warning/Suggestion)

### 2. Testing Strategy Skill → tester agent

```
ช่วยวาง test strategy สำหรับ REST API ที่มี CRUD operations ให้หน่อย
```

**ผลที่คาดหวัง:** agent ควรแนะนำ testing pyramid (unit/integration/e2e), test cases, coverage guidance

### 3. System Design Skill → orchestrator

```
ช่วยออกแบบระบบ URL shortener ที่รองรับ 1 ล้าน requests/วัน
```

**ผลที่คาดหวัง:** agent ควรถาม requirements, วาด high-level design, วิเคราะห์ trade-offs

---

## ทดสอบ Commands

### 4. /review — Code Review

```
/review agent.py
```

**ผลที่คาดหวัง:**
- Summary ของ code changes
- ตาราง Critical Issues (File, Line, Issue, Severity)
- ตาราง Suggestions
- What Looks Good
- Verdict: Approve / Request Changes / Needs Discussion

### 5. /debug — Structured Debugging

```
/debug TypeError: 'NoneType' object is not subscriptable ใน tools.py
```

**ผลที่คาดหวัง:**
- **Reproduce:** อธิบาย expected vs actual behavior
- **Isolate:** หา component/code path ที่เกี่ยวข้อง
- **Diagnose:** ตั้ง hypothesis, trace code, หา root cause
- **Fix:** เสนอ fix + regression test

### 6. /standup — Daily Standup

```
/standup

เมื่อวาน: เพิ่ม plugin system, copy engineering plugin
วันนี้: ทดสอบ plugin commands, เขียน docs
blockers: ไม่มี
```

**ผลที่คาดหวัง:**
- จัดรูปแบบเป็น Yesterday / Today / Blockers
- สรุปกระชับ ชัดเจน

### 7. /architecture — Architecture Decision Record

```
/architecture เลือกระหว่าง PostgreSQL กับ MongoDB สำหรับ e-commerce platform
```

**ผลที่คาดหวัง:**
- ADR format: Context, Decision, Options Considered
- Trade-off Analysis (complexity, cost, scalability)
- Consequences + Action Items

### 8. /incident — Incident Response

```
/incident new API response time เพิ่มจาก 200ms เป็น 5s ตั้งแต่ deploy ล่าสุด
```

**ผลที่คาดหวัง:**
- Severity classification (SEV1-4)
- Status update: Impact, Actions taken, Timeline
- แนะนำ mitigation steps

### 9. /deploy-checklist — Pre-deployment Checklist

```
/deploy-checklist adkcode v2.0
```

**ผลที่คาดหวัง:**
- Checklist แบ่ง: Pre-Deploy, Deploy, Post-Deploy
- รายการ: tests, migrations, feature flags, rollback plan
- Rollback triggers

---

## Checklist สรุป

| # | ทดสอบ | ผ่าน |
|---|-------|:----:|
| 1 | Code Review Skill — ตรวจจับ security issues | ☐ |
| 2 | Testing Strategy Skill — แนะนำ test pyramid | ☐ |
| 3 | System Design Skill — วิเคราะห์ trade-offs | ☐ |
| 4 | /review — structured code review output | ☐ |
| 5 | /debug — 4-step debugging workflow | ☐ |
| 6 | /standup — Yesterday/Today/Blockers format | ☐ |
| 7 | /architecture — ADR format | ☐ |
| 8 | /incident — severity classification + response | ☐ |
| 9 | /deploy-checklist — pre/deploy/post checklist | ☐ |
