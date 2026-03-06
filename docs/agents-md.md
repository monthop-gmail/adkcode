# AGENTS.md Guide

## AGENTS.md คืออะไร?

AGENTS.md คือไฟล์ที่คุณวางไว้ใน project เพื่อบอก adkcode ว่า **project นี้ทำงานอย่างไร** เช่น:
- ใช้ภาษา/framework อะไร
- โครงสร้าง project เป็นอย่างไร
- กฎ/conventions ที่ต้องปฏิบัติตาม
- คำสั่งที่ใช้รัน test, build, deploy

เปรียบเหมือน **คู่มือที่ให้ AI อ่านก่อนเริ่มงาน** — ยิ่งให้ข้อมูลดี ยิ่งได้ผลลัพธ์ที่ตรงใจ

## Quick Start

### 1. สร้างไฟล์ AGENTS.md ไว้ที่ root ของ project

```bash
# copy template ที่ใกล้เคียง
cp examples/agents-md/python-fastapi.md /path/to/your/project/AGENTS.md

# หรือเขียนเอง
nano /path/to/your/project/AGENTS.md
```

### 2. รัน adkcode จาก directory ที่มี AGENTS.md

```bash
cd /path/to/your/project
adk run adkcode
# หรือ
adk web --port 8000
```

adkcode จะโหลด AGENTS.md อัตโนมัติ — ไม่ต้อง config อะไรเพิ่ม

## AGENTS.md กับ Multi-Agent ทำงานร่วมกันอย่างไร?

adkcode มี 4 agents ที่ทำงานร่วมกัน **ทุก agent ได้รับ AGENTS.md เหมือนกันหมด**:

```
┌─────────────────────────────────────────────┐
│                 AGENTS.md                    │
│  "ใช้ Python, ตอบเป็นภาษาไทย, ..."          │
└──────────┬──────────┬──────────┬────────────┘
           │          │          │
     ┌─────▼──┐ ┌─────▼──┐ ┌────▼───┐
     │ coder  │ │reviewer│ │ tester │
     └────────┘ └────────┘ └────────┘
```

### แต่ละ agent ใช้ AGENTS.md ต่างกัน

| Agent | อ่าน AGENTS.md แล้วทำอะไร |
|-------|--------------------------|
| **orchestrator** | ใช้ข้อมูล project เพื่อ route งานให้ถูก agent |
| **coder** | เขียนโค้ดตาม stack, conventions, structure ที่กำหนด |
| **reviewer** | review โค้ดตามกฎของ project (เช่น ห้าม `*` imports) |
| **tester** | รู้คำสั่งรัน test ที่ถูกต้อง (pytest, jest, go test) |

### ตัวอย่างจริง

สมมุติ AGENTS.md ของคุณเขียนว่า:

```markdown
# AGENTS.md
## Stack
- Python 3.12 + FastAPI
- Test: `pytest -v`
- ห้ามใช้ `*` imports

## Rules
- ตอบเป็นภาษาไทย
- เขียน test ทุกครั้งที่สร้าง endpoint ใหม่
```

ผลลัพธ์:

| คุณถาม | Agent | ทำอะไร |
|--------|-------|--------|
| *"สร้าง API endpoint /users"* | coder | เขียน FastAPI endpoint + สร้าง test ด้วย (เพราะกฎบอกไว้) |
| *"review โค้ด"* | reviewer | ตรวจว่ามี `*` imports ไหม + ตอบเป็นภาษาไทย |
| *"รัน test"* | tester | รัน `pytest -v` (รู้คำสั่งจาก AGENTS.md) |
| *"project นี้ใช้อะไร?"* | orchestrator | ตอบว่า Python 3.12 + FastAPI (อ่านจาก AGENTS.md) |

## เขียน AGENTS.md ยังไงให้ได้ผลดี

### โครงสร้างแนะนำ

```markdown
# AGENTS.md

## Stack
- ภาษา/framework ที่ใช้
- database, ORM, package manager

## Project Structure
- โครงสร้าง folder หลักๆ

## Commands
- คำสั่งรัน dev, test, build, deploy

## Code Style
- conventions, linting rules

## Rules
- กฎที่ต้องปฏิบัติตามเสมอ
```

### Tips

- **บอก Stack ชัดเจน** — "Python 3.12 + FastAPI" ดีกว่า "Python backend"
- **ใส่ Project Structure** — agent จะเข้าใจว่าไฟล์อยู่ตรงไหน ไม่ต้องถามซ้ำ
- **ใส่ Commands** — agent จะรัน test/build ได้ถูกคำสั่งเลย
- **กฎสั้นๆ ชัดๆ** — "ห้ามใช้ `*` imports" ดีกว่า "ควรระวังการ import"
- **ภาษาไทยหรืออังกฤษก็ได้** — Gemini เข้าใจทั้งสองภาษา

### สิ่งที่ไม่ควรใส่

- Secrets, API keys, passwords
- ข้อมูลที่เปลี่ยนบ่อย (เช่น version เฉพาะที่อัพเดททุกวัน)
- คำอธิบายยาวเกินไป — สั้นกระชับได้ผลดีกว่า

## Templates พร้อมใช้ (21 แบบ)

เลือก template ที่ใกล้เคียงแล้ว copy ไปแก้ได้เลย:

### Coding

| Template | สำหรับ |
|----------|-------|
| [minimal.md](../examples/agents-md/minimal.md) | เริ่มต้นเร็ว ใช้ได้ทุก project |
| [go-project.md](../examples/agents-md/go-project.md) | Go backend |
| [nextjs-project.md](../examples/agents-md/nextjs-project.md) | Next.js + TypeScript |
| [python-fastapi.md](../examples/agents-md/python-fastapi.md) | Python FastAPI |
| [rust-project.md](../examples/agents-md/rust-project.md) | Rust + Axum |
| [flutter-project.md](../examples/agents-md/flutter-project.md) | Flutter mobile |

### Tech

| Template | สำหรับ |
|----------|-------|
| [devops.md](../examples/agents-md/devops.md) | DevOps / Infrastructure |
| [sysadmin.md](../examples/agents-md/sysadmin.md) | System Administration |
| [data-analysis.md](../examples/agents-md/data-analysis.md) | Data Analysis |
| [writing-docs.md](../examples/agents-md/writing-docs.md) | Technical Writing |
| [research-assistant.md](../examples/agents-md/research-assistant.md) | Research & Analysis |

### IoT

| Template | สำหรับ |
|----------|-------|
| [iot-embedded.md](../examples/agents-md/iot-embedded.md) | Arduino / ESP32 |
| [iot-platform.md](../examples/agents-md/iot-platform.md) | IoT Backend (MQTT, InfluxDB) |
| [iot-smart-farm.md](../examples/agents-md/iot-smart-farm.md) | Smart Farm |
| [iot-esphome.md](../examples/agents-md/iot-esphome.md) | ESPHome + Home Assistant |

### ERP / Business

| Template | สำหรับ |
|----------|-------|
| [odoo.md](../examples/agents-md/odoo.md) | Odoo ERP |
| [hr.md](../examples/agents-md/hr.md) | HR ทรัพยากรบุคคล |
| [crm.md](../examples/agents-md/crm.md) | CRM จัดการลูกค้า |
| [sales.md](../examples/agents-md/sales.md) | Sales ทีมขาย |
| [marketing.md](../examples/agents-md/marketing.md) | Marketing การตลาด |
| [accounting.md](../examples/agents-md/accounting.md) | Accounting บัญชี/การเงิน |

## วิธีใช้ Template

```bash
# 1. เลือก template
cp examples/agents-md/python-fastapi.md /your/project/AGENTS.md

# 2. แก้ไขให้ตรงกับ project
nano /your/project/AGENTS.md

# 3. รัน adkcode จาก project directory
cd /your/project
adk run adkcode
```

## ใช้ไม่ใช้ AGENTS.md ต่างกันยังไง?

| | ไม่มี AGENTS.md | มี AGENTS.md |
|---|----------------|--------------|
| **เขียนโค้ด** | เขียนได้ แต่ไม่รู้ style ของ project | เขียนตาม conventions ของ project |
| **รัน test** | ต้องถามคำสั่ง | รู้คำสั่งเลย (`pytest -v`, `npm test`) |
| **review** | review ทั่วไป | review ตามกฎเฉพาะของ project |
| **ภาษา** | ตอบภาษาอังกฤษ | ตอบภาษาที่กำหนด |
| **โครงสร้าง** | ต้องสำรวจก่อน | รู้โครงสร้างทันที |

## FAQ

### AGENTS.md ต้องชื่อนี้เท่านั้นหรือเปล่า?

รองรับ 3 ชื่อ: `AGENTS.md`, `agents.md`, `Agents.md`

### วางไว้ตรงไหน?

ต้องวางที่ **working directory** (directory ที่คุณรัน `adk` command)

### แก้ AGENTS.md ระหว่างใช้งานได้ไหม?

ได้ แต่ต้อง restart adkcode ใหม่เพื่อโหลดไฟล์ใหม่

### ใช้ร่วมกับ MCP ได้ไหม?

ได้! AGENTS.md กำหนด instructions ส่วน MCP กำหนด tools — ทำงานแยกกันไม่ขัดกัน

### ถ้ามีหลาย project ใช้ AGENTS.md คนละไฟล์ได้ไหม?

ได้! แต่ละ project มี AGENTS.md ของตัวเอง adkcode จะโหลดจาก directory ที่คุณรัน
