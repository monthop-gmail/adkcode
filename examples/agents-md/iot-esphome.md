# AGENTS.md — ESPHome / Home Assistant

## Stack
- ESPHome (YAML-based firmware)
- Home Assistant
- ESP32 / ESP8266
- MQTT / Native API
- Sensors, Relays, LED strips, Displays

## Rules
- ตอบเป็นภาษาไทยเสมอ
- เขียน config เป็น YAML เท่านั้น — ESPHome ไม่ใช้ C++
- ระบุ board type ให้ชัดเจน (esp32dev, nodemcu-32s, d1_mini)
- ใส่ comment อธิบาย pin และ sensor ที่ใช้
- ใช้ substitutions สำหรับค่าที่ใช้ซ้ำ (ชื่อ device, WiFi)
- ใช้ secrets.yaml สำหรับ password / API key — ห้าม hardcode

## Project Structure
```
esphome/
├── secrets.yaml              # WiFi password, API keys
├── common/
│   ├── base.yaml             # WiFi, OTA, API, logger
│   ├── sensors.yaml          # Shared sensor configs
│   └── switches.yaml         # Shared switch configs
├── living-room-climate.yaml
├── bedroom-light.yaml
├── garden-irrigation.yaml
└── garage-door.yaml
```

## Config Template
```yaml
substitutions:
  device_name: living-room-climate
  friendly_name: "ห้องนั่งเล่น - สภาพอากาศ"

esphome:
  name: ${device_name}

esp32:
  board: esp32dev

# WiFi + Fallback AP
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
    ssid: "${device_name}-fallback"
    password: !secret fallback_password

captive_portal:
api:
  encryption:
    key: !secret api_key
ota:
  platform: esphome
  password: !secret ota_password
logger:
```

## Common Components

### Sensors
```yaml
# DHT22 อุณหภูมิ + ความชื้น
sensor:
  - platform: dht
    model: DHT22
    pin: GPIO4
    temperature:
      name: "${friendly_name} อุณหภูมิ"
    humidity:
      name: "${friendly_name} ความชื้น"
    update_interval: 30s

# Soil Moisture (Analog)
  - platform: adc
    pin: GPIO34
    name: "${friendly_name} ความชื้นดิน"
    unit_of_measurement: "%"
    filters:
      - calibrate_linear:
          - 3.3 -> 0.0    # แห้ง
          - 1.4 -> 100.0  # เปียก
    update_interval: 60s
```

### Switches
```yaml
# Relay ควบคุมปั๊มน้ำ
switch:
  - platform: gpio
    pin: GPIO26
    name: "${friendly_name} ปั๊มน้ำ"
    id: water_pump
    icon: "mdi:water-pump"
    restore_mode: ALWAYS_OFF
```

### Automations
```yaml
# ปิดปั๊มน้ำอัตโนมัติหลัง 10 นาที
  on_turn_on:
    - delay: 10min
    - switch.turn_off: water_pump
    - logger.log: "ปิดปั๊มน้ำอัตโนมัติ (timeout 10 นาที)"
```

### Binary Sensors
```yaml
# PIR Motion Sensor
binary_sensor:
  - platform: gpio
    pin: GPIO27
    name: "${friendly_name} ตรวจจับการเคลื่อนไหว"
    device_class: motion
    filters:
      - delayed_off: 30s
```

### Displays
```yaml
# OLED SSD1306
i2c:
  sda: GPIO21
  scl: GPIO22

display:
  - platform: ssd1306_i2c
    model: "SSD1306 128x64"
    address: 0x3C
    lambda: |-
      it.printf(0, 0, id(font1), "อุณหภูมิ: %.1f°C", id(temp).state);
      it.printf(0, 20, id(font1), "ความชื้น: %.1f%%", id(humidity).state);
```

## Home Assistant Integration
- ใช้ Native API (ไม่ต้อง MQTT) สำหรับ HA integration
- ตั้งชื่อ entity ภาษาไทยได้ผ่าน friendly_name
- จัด area ใน HA ตาม location จริง
- สร้าง automation ใน HA สำหรับ logic ที่ซับซ้อน

## Tips
- `esphome run <file>.yaml` — compile + upload
- `esphome logs <file>.yaml` — ดู serial log
- ใช้ `!include` แยก config ที่ใช้ซ้ำ
- ใช้ `on_boot` สำหรับ initial state
- ตั้ง `update_interval` ตามความจำเป็น — ไม่ต้องถี่เกินไป
- ใช้ `filters` สำหรับ smoothing / calibration ค่า sensor
