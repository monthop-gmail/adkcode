# คู่มือทดสอบ Productivity Plugin

Plugin นี้เพิ่ม **2 skills** และ **2 commands** สำหรับจัดการ tasks และ memory

## สิ่งที่ต้องเตรียม

- adkcode รันอยู่ที่ http://localhost:8000
- เลือก agent `adkcode` จาก dropdown

---

## ทดสอบ Skills (ทำงานอัตโนมัติ)

### 1. Task Management Skill

ถามเกี่ยวกับจัดการ task แล้วดูว่า agent ใช้รูปแบบ TASKS.md หรือไม่

```
ช่วยสร้าง task list สำหรับ project ใหม่:
1. Setup project structure
2. เขียน API endpoints
3. เขียน tests
4. Deploy to staging
```

**ผลที่คาดหวัง:** agent สร้างไฟล์ TASKS.md ในรูปแบบ:
```markdown
## Active
- [ ] **Setup project structure** - สร้างโครงสร้าง project
- [ ] **เขียน API endpoints** - REST API
- [ ] **เขียน tests** - unit + integration tests
- [ ] **Deploy to staging** - deploy ขึ้น staging

## Waiting On

## Done
```

### 2. Memory Management Skill

```
ช่วยจำว่า project นี้ใช้ Python 3.12 + FastAPI, deploy บน Google Cloud Run,
ทีมมี 3 คน (สมชาย, สมหญิง, สมศักดิ์)
```

**ผลที่คาดหวัง:** agent บันทึกข้อมูลลง memory file หรือ context เพื่อใช้ในภายหลัง

---

## ทดสอบ Commands

### 3. /start — เริ่มระบบ Productivity

```
/start
```

**ผลที่คาดหวัง:**
- สร้าง TASKS.md (ถ้ายังไม่มี)
- สร้าง memory/ directory
- แสดงสถานะ: จำนวน tasks, memory details
- แนะนำให้รัน `/update` ต่อ

### 4. /start แล้วเพิ่ม Tasks

หลังจาก /start ให้ทดสอบเพิ่ม tasks:

```
เพิ่ม task: Review PR #42 ของสมชาย — deadline วันศุกร์
```

**ผลที่คาดหวัง:**
- เพิ่ม task ลง TASKS.md
- มี context (ใครทำ, deadline)

```
task "Setup project structure" เสร็จแล้ว
```

**ผลที่คาดหวัง:**
- ย้าย task ไป Done section
- เพิ่มวันที่ completed

### 5. /update — Sync Tasks

```
/update
```

**ผลที่คาดหวัง:**
- อ่าน TASKS.md ปัจจุบัน
- สรุปสถานะ: active tasks, completed, overdue
- ถามเกี่ยวกับ tasks ที่ค้างนาน
- แนะนำ next actions

### 6. /update --comprehensive

```
/update --comprehensive
```

**ผลที่คาดหวัง:**
- Deep scan ข้อมูลทั้งหมด
- Flag missed todos
- Suggest new memories
- Fill memory gaps

---

## ทดสอบ Workflow แบบต่อเนื่อง

ทดสอบ full workflow ตั้งแต่ต้น:

```
ขั้นตอนที่ 1: /start
ขั้นตอนที่ 2: เพิ่ม tasks 3-4 รายการ
ขั้นตอนที่ 3: mark task แรกว่าเสร็จ
ขั้นตอนที่ 4: /update ดูสถานะ
ขั้นตอนที่ 5: ถาม "สรุปงานวันนี้"
```

**ตัวอย่าง:**

```
/start
```

```
เพิ่ม tasks:
1. แก้ bug login page — urgent
2. เขียน unit test สำหรับ auth module
3. Review PR #15 ของสมหญิง
4. Update API docs
```

```
task "แก้ bug login page" เสร็จแล้ว
```

```
/update
```

```
สรุปงานวันนี้ให้หน่อย
```

**ผลที่คาดหวัง:**
- agent จัดการ TASKS.md ได้ถูกต้อง
- สรุปงานได้ (เสร็จ 1, เหลือ 3)
- แนะนำ priority ของงานที่เหลือ

---

## Checklist สรุป

| # | ทดสอบ | ผ่าน |
|---|-------|:----:|
| 1 | Task Management Skill — สร้าง TASKS.md format ถูกต้อง | ☐ |
| 2 | Memory Management Skill — บันทึก context ได้ | ☐ |
| 3 | /start — bootstrap ระบบ productivity | ☐ |
| 4 | เพิ่ม/จัดการ tasks — CRUD operations | ☐ |
| 5 | /update — sync + สรุปสถานะ | ☐ |
| 6 | /update --comprehensive — deep scan | ☐ |
| 7 | Full workflow ต่อเนื่อง | ☐ |
