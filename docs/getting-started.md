# คู่มือใช้งาน adkcode เบื้องต้น

## เปิดใช้งาน

1. เปิด browser ไปที่ **http://localhost:8000**
2. เลือก agent **adkcode** จาก dropdown ด้านบนซ้าย
3. คลิก **New Session** เพื่อเริ่ม session ใหม่
4. พิมพ์คำสั่งในช่อง chat แล้วกด Enter

---

## สิ่งที่ adkcode ทำได้

### เขียนโค้ด

```
สร้างไฟล์ hello.py ที่พิมพ์ Hello World
```

```
สร้าง REST API ด้วย FastAPI มี endpoint GET /users และ POST /users
```

```
แก้ไฟล์ main.py เพิ่ม error handling ใน function login()
```

### Review โค้ด

```
review โค้ดใน agent.py ให้หน่อย
```

```
ดู tools.py แล้วหา bugs หรือ security issues
```

### รัน Test

```
รัน pytest แล้วสรุปผลให้หน่อย
```

```
เขียน unit test สำหรับ utils.py
```

### ค้นหาข้อมูล

```
ค้นหาข่าว AI ล่าสุด
```

```
เปิด https://example.com แล้วสรุปเนื้อหาให้หน่อย
```

### วิเคราะห์รูป / Screenshot

```
ดู screenshot.png แล้วเขียน HTML ตามนี้
```

### ค้นหาโค้ดด้วย RAG

```
index โปรเจคนี้
```

```
หาโค้ดที่เกี่ยวกับ authentication
```

---

## Plugin Commands

adkcode มี plugin commands สำเร็จรูป พิมพ์ได้เลย:

### Engineering

| Command | ใช้ทำอะไร | ตัวอย่าง |
|---------|----------|---------|
| `/review` | Review โค้ด | `/review agent.py` |
| `/debug` | Debug ปัญหา | `/debug TypeError: NoneType object` |
| `/standup` | สรุปงานประจำวัน | `/standup` |
| `/architecture` | ออกแบบ architecture | `/architecture เลือก DB สำหรับ e-commerce` |
| `/incident` | จัดการ incident | `/incident new API ช้ามาก` |
| `/deploy-checklist` | Checklist ก่อน deploy | `/deploy-checklist v2.0` |

### Data

| Command | ใช้ทำอะไร | ตัวอย่าง |
|---------|----------|---------|
| `/write-query` | เขียน SQL | `/write-query หา top 10 ลูกค้า` |
| `/analyze` | วิเคราะห์ข้อมูล | `/analyze ยอดขายรายเดือน` |
| `/explore-data` | สำรวจ dataset | `/explore-data users.csv` |
| `/create-viz` | สร้าง chart | `/create-viz bar chart ยอดขาย` |
| `/build-dashboard` | สร้าง dashboard | `/build-dashboard sales dashboard` |
| `/validate` | ตรวจสอบ analysis | `/validate ยอดขายเพิ่ม 40%` |

### Productivity

| Command | ใช้ทำอะไร | ตัวอย่าง |
|---------|----------|---------|
| `/start` | เริ่มระบบ task | `/start` |
| `/update` | Sync tasks | `/update` |

---

## ตัวอย่างการใช้งานจริง

### สร้างโปรเจคใหม่

```
สร้างโปรเจค Python Flask API สำหรับ Todo App มี:
- GET /todos — list ทั้งหมด
- POST /todos — สร้างใหม่
- PUT /todos/:id — แก้ไข
- DELETE /todos/:id — ลบ
ใช้ SQLite เก็บข้อมูล
```

### แก้ Bug

```
รัน python main.py แล้วเจอ error:
ImportError: cannot import name 'app' from 'server'
ช่วยแก้ให้หน่อย
```

### Review + แก้ไข

```
review ไฟล์ทั้งหมดใน src/ แล้วแก้ issues ที่เจอให้ด้วย
```

### วิเคราะห์ข้อมูล

```
/analyze
มีข้อมูลยอดขาย 6 เดือน:
ม.ค. 500K, ก.พ. 480K, มี.ค. 620K, เม.ย. 550K, พ.ค. 700K, มิ.ย. 680K
สรุป trend และแนะนำ action
```

---

## Tips

- **ภาษา** — พิมพ์ไทยหรืออังกฤษก็ได้ agent เข้าใจทั้งสองภาษา
- **ไฟล์** — agent ทำงานกับไฟล์ใน `/workspace` directory
- **Session** — แต่ละ session แยกกัน คลิก New Session เพื่อเริ่มใหม่
- **Multi-agent** — ไม่ต้องเลือก agent เอง ระบบ route อัตโนมัติ (coding → coder, review → reviewer, test → tester)
- **Context** — ยิ่งให้ข้อมูลเยอะ ผลลัพธ์ยิ่งดี เช่น บอก framework, ภาษา, ข้อจำกัด

## Troubleshooting

| ปัญหา | วิธีแก้ |
|-------|--------|
| Agent ไม่ตอบ | สร้าง session ใหม่ |
| ตอบช้า | ปกติสำหรับคำถามซับซ้อน รอสักครู่ |
| Error ใน chat | ดู Docker logs: `docker compose logs --tail 50` |
| เปิดเว็บไม่ได้ | ตรวจว่า container รัน: `docker compose ps` |
