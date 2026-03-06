# AGENTS.md — IoT Embedded (Arduino / ESP32 / Raspberry Pi)

## Stack
- ESP32 / ESP8266 (Arduino Framework)
- Raspberry Pi (Python / C++)
- Arduino IDE / PlatformIO
- MQTT (Mosquitto broker)
- Sensors: DHT22, BME280, HC-SR04, PIR, LDR, Relay Module

## Rules
- ตอบเป็นภาษาไทยเสมอ
- ระบุขา GPIO / Pin ที่ใช้ให้ชัดเจนทุกครั้ง
- เขียน comment อธิบายการต่อวงจรในโค้ด
- ใส่ delay / debounce เสมอเมื่ออ่าน sensor
- ห้ามใช้ delay() ใน production — ใช้ millis() แทน

## Coding Conventions
- ตั้งชื่อ pin เป็น constant: `const int LED_PIN = 2;`
- แยก function: setup, loop, readSensor, sendData
- ใช้ Serial.println() สำหรับ debug
- WiFi credentials เก็บใน config.h แยกจากโค้ดหลัก

## MQTT Topics
```
home/{room}/{device}/status     → สถานะ (online/offline)
home/{room}/{device}/sensor     → ค่า sensor (JSON)
home/{room}/{device}/command    → สั่งงาน (on/off/set)
```

## Common Tasks
- อ่านค่า sensor แล้วส่งผ่าน MQTT
- ควบคุม relay / LED / motor ผ่าน MQTT
- แสดงผลบน OLED / LCD
- OTA update firmware
- Deep sleep เพื่อประหยัดพลังงาน
- เชื่อมต่อ WiFi พร้อม reconnect อัตโนมัติ

## Safety
- ตรวจสอบ voltage ก่อนต่อวงจร (3.3V vs 5V)
- ใช้ resistor กับ LED เสมอ
- ระวัง relay — แยก power supply สำหรับ high voltage
- ห้ามต่อ motor ตรงกับ GPIO — ใช้ driver module
