# คู่มือทดสอบ Data Plugin

Plugin นี้เพิ่ม **7 skills** และ **6 commands** สำหรับงาน data analysis, SQL, visualization

## สิ่งที่ต้องเตรียม

- adkcode รันอยู่ที่ http://localhost:8000
- เลือก agent `adkcode` จาก dropdown
- (Optional) ไฟล์ CSV หรือ JSON ใน workspace สำหรับทดสอบ

---

## ทดสอบ Skills (ทำงานอัตโนมัติ)

### 1. SQL Queries Skill

```
เขียน SQL query หา top 10 ลูกค้าที่ซื้อสินค้ามากที่สุดในเดือนนี้
ใช้ PostgreSQL, ตาราง orders (id, customer_id, amount, created_at) และ customers (id, name, email)
```

**ผลที่คาดหวัง:** agent เขียน SQL ที่ถูกต้อง ใช้ CTE, JOIN, date filter, ORDER BY + LIMIT พร้อมอธิบาย

### 2. Data Validation Skill

```
ช่วยตรวจสอบ analysis นี้หน่อย:
- ยอดขายเฉลี่ยต่อเดือน = 500,000 บาท
- คำนวณจาก AVG(monthly_total) จาก 12 เดือน
- แต่มี 2 เดือนที่ไม่มีข้อมูล (null)
ผลลัพธ์ถูกต้องไหม?
```

**ผลที่คาดหวัง:** agent ชี้ปัญหา average of incomplete data, แนะนำ COALESCE หรือ exclude null months

### 3. Statistical Analysis Skill

```
มีข้อมูล A/B test:
- Control: 1000 users, 50 conversions (5%)
- Treatment: 1000 users, 65 conversions (6.5%)
ผลลัพธ์ significant ไหม?
```

**ผลที่คาดหวัง:** agent คำนวณ statistical significance (chi-square หรือ z-test), p-value, confidence interval

---

## ทดสอบ Commands

### 4. /write-query — เขียน SQL

```
/write-query หา revenue per product category รายเดือน ย้อนหลัง 6 เดือน
ตาราง: orders(id, product_id, amount, created_at), products(id, name, category)
ใช้ PostgreSQL
```

**ผลที่คาดหวัง:**
- SQL query ใน code block
- ใช้ CTE, date_trunc, JOIN
- อธิบายแต่ละ CTE
- Performance notes
- Modification suggestions

### 5. /analyze — วิเคราะห์ข้อมูล

```
/analyze ช่วยวิเคราะห์ข้อมูลนี้:

เดือน,ยอดขาย,จำนวนลูกค้า
ม.ค.,500000,120
ก.พ.,480000,115
มี.ค.,620000,145
เม.ย.,550000,130
พ.ค.,700000,160
มิ.ย.,680000,155
```

**ผลที่คาดหวัง:**
- สรุป trend (ยอดขายเพิ่มขึ้น)
- คำนวณ growth rate
- หา correlation ระหว่างยอดขายกับจำนวนลูกค้า
- แนะนำ follow-up analysis

### 6. /explore-data — สำรวจข้อมูล

```
/explore-data ช่วยสำรวจโครงสร้างข้อมูลนี้:

id,name,email,age,salary,department,join_date
1,สมชาย,somchai@test.com,28,35000,Engineering,2024-01-15
2,สมหญิง,somying@test.com,35,55000,Marketing,2023-06-01
3,สมศักดิ์,,42,null,Engineering,2022-03-10
4,สมศรี,somsri@test.com,25,30000,,2024-08-20
5,สมบัติ,sombat@test.com,38,48000,Engineering,2023-01-05
```

**ผลที่คาดหวัง:**
- Data Profile: row count, column types
- Null analysis (email, salary, department มี null)
- Data quality issues flagged
- Recommended explorations

### 7. /create-viz — สร้าง Visualization

```
/create-viz สร้าง bar chart เปรียบเทียบยอดขายรายเดือน:

เดือน: ม.ค. ก.พ. มี.ค. เม.ย. พ.ค. มิ.ย.
ยอดขาย: 500000 480000 620000 550000 700000 680000
```

**ผลที่คาดหวัง:**
- Python code ใช้ matplotlib/seaborn
- ตั้งค่า colorblind-friendly palette
- Labels, title ชัดเจน
- Save เป็น PNG

### 8. /build-dashboard — สร้าง Dashboard

```
/build-dashboard สร้าง sales dashboard แสดง:
- KPI: ยอดขายรวม, จำนวนลูกค้า, average order value
- Line chart: ยอดขายรายเดือน
- Bar chart: ยอดขายตาม category
ข้อมูล: ใช้ sample data
```

**ผลที่คาดหวัง:**
- ไฟล์ HTML เดียว (self-contained)
- KPI cards ด้านบน
- Charts ใช้ Chart.js
- Filter dropdowns
- Responsive design
- เปิดใน browser ได้เลย

### 9. /validate — ตรวจสอบ Analysis

```
/validate ช่วยตรวจสอบ analysis นี้:

สรุป: ยอดขายเพิ่มขึ้น 40% (จาก 500K เป็น 700K)
วิธีคำนวณ: เปรียบเทียบเดือนแรก vs เดือนสุดท้าย
ข้อสรุป: ธุรกิจเติบโตดีมาก ควรเพิ่มงบ marketing
```

**ผลที่คาดหวัง:**
- Overall Assessment: Share with caveats / Needs revision
- ชี้ปัญหา: เปรียบเทียบแค่ 2 เดือนไม่เพียงพอ, ไม่มี seasonality analysis
- Calculation spot-check
- Suggested improvements
- Required caveats

---

## Checklist สรุป

| # | ทดสอบ | ผ่าน |
|---|-------|:----:|
| 1 | SQL Queries Skill — เขียน SQL ถูกต้อง | ☐ |
| 2 | Data Validation Skill — ตรวจจับ data issues | ☐ |
| 3 | Statistical Analysis Skill — คำนวณ significance | ☐ |
| 4 | /write-query — SQL + explanation + performance notes | ☐ |
| 5 | /analyze — trend analysis + follow-up suggestions | ☐ |
| 6 | /explore-data — data profile + quality issues | ☐ |
| 7 | /create-viz — Python chart code + best practices | ☐ |
| 8 | /build-dashboard — self-contained HTML dashboard | ☐ |
| 9 | /validate — methodology review + caveats | ☐ |
