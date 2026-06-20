# EP10 — Vectorized String Operations

## เป้าหมายของตอนนี้

ในงานจริง ข้อมูลที่ได้จาก Sensor, IoT Platform, CSV, MQTT, Excel หรือระบบ Monitoring มักไม่ได้สะอาดเสมอไป

ตัวอย่างปัญหาที่เจอบ่อย:

- `device_id` เขียนไม่เหมือนกัน
- มีช่องว่างเกิน
- ตัวพิมพ์เล็ก / ใหญ่ปนกัน
- ชื่อ Site ไม่เป็นมาตรฐาน
- Status มีหลายรูปแบบ เช่น `online`, `ONLINE`, ` Online `
- Topic MQTT ต้องแยกเป็นส่วน ๆ
- ข้อความ Alarm ต้องค้นหา keyword

Pandas มีเครื่องมือชื่อว่า `.str` สำหรับจัดการข้อความแบบ Vectorized

```text
Vectorized String Operations = จัดการข้อความทั้งคอลัมน์ในคำสั่งเดียว
```

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. ทำไมต้องใช้ .str

สมมุติเรามีข้อมูลชื่ออุปกรณ์แบบไม่สะอาด

```python
devices = pd.Series([
    " sensor_01 ",
    "SENSOR_02",
    None,
    "Sensor_03",
    " sensor_04"
])

print(devices)
```

ถ้าใช้ Python loop ปกติ แล้วเจอ `None` อาจ error ได้

แต่ Pandas `.str` จะจัดการข้อความทั้ง Series และข้าม missing value ให้โดยอัตโนมัติในหลายกรณี

---

# 3. แปลงตัวพิมพ์เล็ก

```python
clean_devices = devices.str.lower()

print(clean_devices)
```

ใช้เมื่อต้องการให้ `device_id` เป็นรูปแบบเดียวกัน

```text
SENSOR_02
Sensor_03
sensor_04
```

กลายเป็น

```text
sensor_02
sensor_03
sensor_04
```

---

# 4. ลบช่องว่างหัวท้าย

```python
clean_devices = devices.str.strip()

print(clean_devices)
```

ใช้เมื่อข้อมูลมาจาก CSV หรือ Excel แล้วมีช่องว่างแฝง

ตัวอย่าง: `" sensor_01 "`

กลายเป็น `"sensor_01"`

---

# 5. ทำความสะอาด device_id แบบรวมหลายขั้นตอน

```python
clean_devices = (
    devices
    .str.strip()
    .str.lower()
)

print(clean_devices)
```

รูปแบบนี้ใช้บ่อยมากในงาน Data Cleaning

---

# 6. สร้าง DataFrame ตัวอย่าง

```python
iot_logs = pd.DataFrame({
    "raw_device_id": [
        " Sensor_01 ",
        "sensor_02",
        "SENSOR_03",
        " sensor_04 "
    ],
    "site": [
        " SITE_A ",
        "site_a",
        "Site_B",
        " site_b "
    ],
    "status": [
        " ONLINE ",
        "offline",
        "Warning",
        " online"
    ]
})

print(iot_logs)
```

---

# 7. Cleaning หลายคอลัมน์

```python
iot_logs["device_id"] = (
    iot_logs["raw_device_id"]
    .str.strip()
    .str.lower()
)

iot_logs["site_clean"] = (
    iot_logs["site"]
    .str.strip()
    .str.lower()
)

iot_logs["status_clean"] = (
    iot_logs["status"]
    .str.strip()
    .str.lower()
)

print(iot_logs)
```

---

# 8. ตรวจสอบความยาวข้อความด้วย str.len()

```python
print(
    iot_logs["device_id"].str.len()
)
```

ใช้เช็คความผิดปกติ เช่น device_id สั้นหรือยาวเกินไป

---

# 9. ค้นหาข้อความด้วย str.contains()

```python
print(
    iot_logs["status_clean"].str.contains("online")
)
```

ผลลัพธ์จะเป็น Boolean

```text
True
False
False
True
```

---

## ใช้ filter เฉพาะ online

```python
online_devices = iot_logs[
    iot_logs["status_clean"].str.contains("online", na=False)
]

print(online_devices)
```

`na=False` ใช้บอกว่า ถ้าเจอค่า missing ให้ถือว่าไม่ match

---

# 10. startswith() และ endswith()

## device_id ที่ขึ้นต้นด้วย sensor

```python
print(
    iot_logs["device_id"].str.startswith("sensor")
)
```

## site ที่ลงท้ายด้วย _a

```python
print(
    iot_logs["site_clean"].str.endswith("_a")
)
```

---

# 11. replace() แทนข้อความ

สมมุติอยากเปลี่ยนชื่อ Site

```python
iot_logs["site_clean"] = (
    iot_logs["site_clean"]
    .str.replace("site_", "factory_", regex=False)
)

print(iot_logs)
```

---

# 12. split() แยกข้อความ

ตัวอย่าง MQTT Topic

```python
mqtt_logs = pd.DataFrame({
    "topic": [
        "factory_a/line_1/meter_01/power",
        "factory_a/line_1/meter_02/power",
        "factory_b/line_2/meter_03/temperature"
    ],
    "value": [
        120.5,
        118.2,
        30.1
    ]
})

print(mqtt_logs)
```

---

## split topic

```python
topic_parts = mqtt_logs["topic"].str.split("/")

print(topic_parts)
```

ผลลัพธ์แต่ละแถวจะเป็น list

---

# 13. ดึงตำแหน่งจาก split ด้วย str.get()

```python
mqtt_logs["factory"] = mqtt_logs["topic"].str.split("/").str.get(0)
mqtt_logs["line"] = mqtt_logs["topic"].str.split("/").str.get(1)
mqtt_logs["device_id"] = mqtt_logs["topic"].str.split("/").str.get(2)
mqtt_logs["metric"] = mqtt_logs["topic"].str.split("/").str.get(3)

print(mqtt_logs)
```

---

# 14. slice() และการตัดข้อความ

สมมุติ `device_id` เป็น `meter_01`

ต้องการเอาเฉพาะเลขท้าย

```python
mqtt_logs["device_number"] = (
    mqtt_logs["device_id"]
    .str.slice(-2)
)

print(mqtt_logs)
```

หรือเขียนแบบสั้น:

```python
mqtt_logs["device_number"] = mqtt_logs["device_id"].str[-2:]
```

---

# 15. extract() ด้วย Regular Expression

ต้องการดึงตัวเลขออกจาก device_id เช่น `meter_01`

```python
mqtt_logs["device_no"] = (
    mqtt_logs["device_id"]
    .str.extract(r"(\d+)")
)

print(mqtt_logs)
```

---

# 16. contains() กับ Alarm Message

```python
alarm_logs = pd.DataFrame({
    "message": [
        "Meter_01 Over Temperature",
        "meter_02 offline",
        "Sensor_03 Low Battery",
        "METER_04 normal"
    ]
})

alarm_logs["message_clean"] = (
    alarm_logs["message"]
    .str.strip()
    .str.lower()
)

print(alarm_logs)
```

---

## หา alarm ที่เกี่ยวกับ offline

```python
offline_alarm = alarm_logs[
    alarm_logs["message_clean"].str.contains("offline", na=False)
]

print(offline_alarm)
```

---

# 17. get_dummies() แยก Tag หรือ Flag

สมมุติข้อมูลอุปกรณ์มี Tag หลายค่าในช่องเดียว

```python
device_tags = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02",
        "sensor_03"
    ],
    "tags": [
        "temperature|critical|indoor",
        "power|outdoor",
        "temperature|outdoor"
    ]
})

print(device_tags)
```

---

## แปลง tags เป็น column

```python
tag_matrix = device_tags["tags"].str.get_dummies("|")

print(tag_matrix)
```

ผลลัพธ์จะได้ column เช่น:

```text
critical
indoor
outdoor
power
temperature
```

เหมาะกับการเตรียมข้อมูลสำหรับ Dashboard หรือ Machine Learning

---

# 18. cat() รวมข้อความ

สร้างชื่อเต็มของอุปกรณ์จาก site + device_id

```python
mqtt_logs["full_device_name"] = (
    mqtt_logs["factory"]
    .str.cat(mqtt_logs["device_id"], sep="_")
)

print(mqtt_logs)
```

---

# 19. ตารางคำสั่ง .str ที่ใช้บ่อย

| คำสั่ง | ใช้ทำอะไร |
|---|---|
| `.str.lower()` | แปลงเป็นตัวพิมพ์เล็ก |
| `.str.upper()` | แปลงเป็นตัวพิมพ์ใหญ่ |
| `.str.strip()` | ลบช่องว่างหัวท้าย |
| `.str.len()` | นับความยาวข้อความ |
| `.str.contains()` | ตรวจว่ามีคำที่ต้องการหรือไม่ |
| `.str.startswith()` | ตรวจว่าขึ้นต้นด้วยคำใด |
| `.str.endswith()` | ตรวจว่าลงท้ายด้วยคำใด |
| `.str.replace()` | แทนข้อความ |
| `.str.split()` | แยกข้อความ |
| `.str.get()` | ดึงค่าจาก list หรือ string |
| `.str.slice()` | ตัดข้อความ |
| `.str.extract()` | ดึงข้อความด้วย Regular Expression |
| `.str.get_dummies()` | แยก tag เป็น column |
| `.str.cat()` | รวมข้อความ |

---

# 20. Mini Lab — Clean IoT Device Data

สร้างข้อมูลดิบ:

```python
raw_devices = pd.DataFrame({
    "device_id": [
        " Meter_01 ",
        "meter_02",
        "METER_03",
        None
    ],
    "site": [
        " Site_A ",
        "site_a",
        "SITE_B",
        "site_b"
    ],
    "status": [
        " Online ",
        "offline",
        "WARNING",
        None
    ]
})
```

ทำความสะอาด:

```python
raw_devices["device_id_clean"] = (
    raw_devices["device_id"]
    .str.strip()
    .str.lower()
)

raw_devices["site_clean"] = (
    raw_devices["site"]
    .str.strip()
    .str.lower()
)

raw_devices["status_clean"] = (
    raw_devices["status"]
    .str.strip()
    .str.lower()
)

print(raw_devices)
```

กรองเฉพาะอุปกรณ์ online:

```python
online_devices = raw_devices[
    raw_devices["status_clean"].str.contains("online", na=False)
]

print(online_devices)
```

---

# 21. Mini Lab — Parse MQTT Topic

```python
mqtt_logs = pd.DataFrame({
    "topic": [
        "factory_a/line_1/meter_01/power",
        "factory_a/line_1/meter_02/power",
        "factory_b/line_2/meter_03/temperature"
    ],
    "value": [
        120.5,
        118.2,
        30.1
    ]
})
```

แยก Topic:

```python
parts = mqtt_logs["topic"].str.split("/")

mqtt_logs["factory"] = parts.str.get(0)
mqtt_logs["line"] = parts.str.get(1)
mqtt_logs["device_id"] = parts.str.get(2)
mqtt_logs["metric"] = parts.str.get(3)

print(mqtt_logs)
```

---

# 22. สิ่งที่ควรเข้าใจหลังเรียนจบ

หลังจาก EP นี้ คุณควรเข้าใจ:

1. `.str` ใช้จัดการข้อความทั้ง Series
2. `.str.lower()` และ `.str.upper()` ใช้ปรับตัวพิมพ์
3. `.str.strip()` ใช้ลบช่องว่าง
4. `.str.contains()` ใช้ค้นหาคำ
5. `.str.split()` ใช้แยกข้อความ
6. `.str.get()` ใช้ดึงส่วนที่ต้องการ
7. `.str.extract()` ใช้ดึงข้อมูลด้วย Regular Expression
8. `.str.get_dummies()` ใช้แยก Tag เป็น column
9. Pandas จัดการ missing value ได้ดีกว่า loop ปกติในหลายกรณี
10. String Operations สำคัญมากในงาน Data Cleaning

---

# 23. คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---|---|
| Vectorized | ทำงานกับข้อมูลหลายค่าในคำสั่งเดียว |
| String Operation | การจัดการข้อความ |
| `.str` | ตัวเข้าถึงเมธอดข้อความของ Pandas |
| lower | แปลงเป็นตัวพิมพ์เล็ก |
| strip | ลบช่องว่างหัวท้าย |
| contains | ตรวจว่ามีคำที่ต้องการหรือไม่ |
| split | แยกข้อความ |
| extract | ดึงข้อความด้วย pattern |
| regex | รูปแบบสำหรับค้นหาข้อความ |
| get_dummies | แปลง tag เป็น column 0/1 |

---

# การบ้าน

สร้าง DataFrame ชื่อ `raw_logs` โดยมี column:

- raw_topic
- raw_device_id
- raw_status
- message

จากนั้นให้ทำ:

1. ทำความสะอาด device_id ด้วย strip + lower
2. ทำความสะอาด status ด้วย strip + lower
3. แยก raw_topic เป็น factory, line, device_id, metric
4. filter เฉพาะ message ที่มีคำว่า offline
5. ดึงตัวเลขจาก device_id ด้วย extract
6. สร้าง tag column ด้วย get_dummies

---

# ตอนถัดไป

`EP11 — Working with Time Series`

เราจะเรียนรู้:
- Datetime
- DateTimeIndex
- resample()
- rolling()
- shift()
- Time-based IoT Sensor Data
