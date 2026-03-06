# AGENTS.md — IoT Platform / Backend

## Stack
- MQTT Broker (Mosquitto / EMQX)
- Node-RED สำหรับ flow automation
- InfluxDB / TimescaleDB สำหรับ time-series data
- Grafana สำหรับ dashboard
- Docker Compose สำหรับ deployment

## Rules
- ตอบเป็นภาษาไทยเสมอ
- ออกแบบ topic structure ให้เป็นระบบ
- คำนึงถึง scalability — รองรับอุปกรณ์หลายร้อยตัว
- ข้อมูล sensor ต้องมี timestamp เสมอ
- ใช้ JSON format สำหรับ payload

## MQTT Topic Design
```
{project}/{location}/{device_type}/{device_id}/{data_type}

ตัวอย่าง:
factory/building-a/temperature/sensor-001/data
factory/building-a/temperature/sensor-001/status
farm/greenhouse-1/soil-moisture/node-003/data
home/living-room/ac/unit-01/command
```

## Data Format
```json
{
  "device_id": "sensor-001",
  "type": "temperature",
  "value": 28.5,
  "unit": "°C",
  "timestamp": "2026-03-06T10:30:00Z",
  "battery": 85
}
```

## Common Tasks
- ออกแบบ MQTT topic structure
- สร้าง Node-RED flow สำหรับ automation
- ตั้งค่า InfluxDB retention policy
- สร้าง Grafana dashboard
- ตั้ง alert เมื่อค่า sensor ผิดปกติ
- จัดการ device provisioning

## Architecture
```
[Devices] → MQTT Broker → Node-RED → InfluxDB → Grafana
                ↓
          Rule Engine
                ↓
         Alerts / Actions
```

## Docker Compose Services
- `mosquitto` — MQTT broker (port 1883, 9001)
- `nodered` — Flow automation (port 1880)
- `influxdb` — Time-series DB (port 8086)
- `grafana` — Dashboard (port 3000)

## Monitoring
- Device online/offline status via LWT (Last Will and Testament)
- ตรวจสอบ battery level ของ sensor nodes
- Alert เมื่อ device ไม่ส่งข้อมูลเกิน 5 นาที
- ดู throughput ของ MQTT broker
