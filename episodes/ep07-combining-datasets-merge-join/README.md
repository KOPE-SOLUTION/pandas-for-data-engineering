# EP7 — Combining Datasets: Merge and Join

## เป้าหมายของตอนนี้

ในโลกจริง ข้อมูลมักไม่ได้อยู่ในไฟล์เดียว

ตัวอย่างเช่น

- Sensor ส่งค่ามาไฟล์หนึ่ง
- รายละเอียด Sensor อยู่ไฟล์หนึ่ง
- Site อยู่ไฟล์หนึ่ง
- Asset อยู่ไฟล์หนึ่ง
- PLC Tag อยู่อีกไฟล์หนึ่ง

ดังนั้นเราจึงต้อง "เชื่อมข้อมูล" เข้าด้วยกัน

Pandas ใช้ `pd.merge()` ในการเชื่อมข้อมูลแบบเดียวกับ SQL JOIN

---

## 1. Import Library

```py
import pandas as pd
```

---

## 2. Sensor Data

ข้อมูลที่อ่านจาก MQTT หรือ CSV

```py
sensor_data = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02",
        "sensor_03"
    ],
    "temperature_c": [
        28.5,
        29.1,
        30.2
    ]
})

print(sensor_data)
```

<br>

ผลลัพธ์

```sh
   device_id  temperature_c
0  sensor_01           28.5
1  sensor_02           29.1
2  sensor_03           30.2
```

---

## 3. Metadata

รายละเอียดอุปกรณ์

```py
sensor_info = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02",
        "sensor_03"
    ],
    "site": [
        "Site_A",
        "Site_A",
        "Site_B"
    ]
})

print(sensor_info)
```

---

## 4. Merge เบื้องต้น

```py
result = pd.merge(
    sensor_data,
    sensor_info,
    on="device_id"
)

print(result)
```

<br>

ผลลัพธ์

```sh
   device_id  temperature_c    site
0  sensor_01           28.5  Site_A
1  sensor_02           29.1  Site_A
2  sensor_03           30.2  Site_B
```

---

## 5. Merge คืออะไร

ก่อน Merge

```sh
sensor_data

device_id
temperature
```

```sh
sensor_info

device_id
site
```

<br>

หลัง Merge

```sh
device_id
temperature
site
```

---

## 6. One-to-One Join

1 Key = 1 Record

```py
device_status = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02"
    ],
    "status": [
        "online",
        "offline"
    ]
})

pd.merge(
    sensor_info,
    device_status,
    on="device_id"
)
```

<br>

ใช้เมื่อ `1 Sensor ↔ 1 สถานะ`

---

## 7. Many-to-One Join

Sensor หลายตัว อยู่ Site เดียวกัน

```py
site_info = pd.DataFrame({
    "site": [
        "Site_A",
        "Site_B"
    ],
    "province": [
        "Chiang Mai",
        "Bangkok"
    ]
})
```

```py
result = pd.merge(
    sensor_info,
    site_info,
    on="site"
)

print(result)
```

<br>

ใช้เมื่อ `หลาย Sensor ↔ 1 Site`

---

## 8. Many-to-Many Join

Sensor หลายตัว มี Sensor Type หลายประเภท

```py
sensor_type = pd.DataFrame({
    "site": [
        "Site_A",
        "Site_A",
        "Site_B"
    ],
    "measurement": [
        "Temperature",
        "Humidity",
        "Temperature"
    ]
})
```

```py
pd.merge(
    sensor_info,
    sensor_type,
    on="site"
)
```

<br>

ใช้เมื่อ `หลาย Record ↔ หลาย Record`

---

## 9. on=

กำหนด Key ที่ใช้เชื่อม

```py
pd.merge(
    sensor_data,
    sensor_info,
    on="device_id"
)
```

---

## 10. left_on และ right_on

กรณีชื่อ Column ไม่เหมือนกัน

```py
sensor_data = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02"
    ]
})

asset_data = pd.DataFrame({
    "asset_id": [
        "sensor_01",
        "sensor_02"
    ],
    "owner": [
        "ฝ่ายผลิต",
        "ฝ่ายซ่อมบำรุง"
    ]
})
```

```py
pd.merge(
    sensor_data,
    asset_data,
    left_on="device_id",
    right_on="asset_id"
)
```

---

## 11. Inner Join

เอาเฉพาะข้อมูลที่ Match กัน

```py
pd.merge(
    sensor_data,
    asset_data,
    left_on="device_id",
    right_on="asset_id",
    how="inner"
)
```

ภาพจำ `A ∩ B`

---

## 12. Left Join

เก็บข้อมูลฝั่งซ้ายทั้งหมด

```py
pd.merge(
    sensor_data,
    asset_data,
    left_on="device_id",
    right_on="asset_id",
    how="left"
)
```

ภาพจำ `เอาฝั่งซ้ายทั้งหมด`

---

## 13. Right Join

เก็บข้อมูลฝั่งขวาทั้งหมด

```py
pd.merge(
    sensor_data,
    asset_data,
    left_on="device_id",
    right_on="asset_id",
    how="right"
)
```

ภาพจำ `เอาฝั่งขวาทั้งหมด`

---

## 14. Outer Join

เก็บทุก Record

```py
pd.merge(
    sensor_data,
    asset_data,
    left_on="device_id",
    right_on="asset_id",
    how="outer"
)
```

ภาพจำ `A ∪ B`

---

## 15. Join ด้วย Index

```py
sensor_data = sensor_data.set_index(
    "device_id"
)

sensor_info = sensor_info.set_index(
    "device_id"
)
```

```py
pd.merge(
    sensor_data,
    sensor_info,
    left_index=True,
    right_index=True
)
```

---

## 16. DataFrame.join()

เขียนสั้นกว่า

```py
sensor_data.join(
    sensor_info
)
```

---

## 17. suffixes

กรณีชื่อ Column ซ้ำ

```py
pd.merge(
    left_df,
    right_df,
    on="device_id",
    suffixes=(
        "_old",
        "_new"
    )
)
```

---

## 18. Mini Lab — IoT Monitoring

ข้อมูล Telemetry

```py
telemetry = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02"
    ],
    "temperature_c": [
        28.5,
        29.1
    ]
})
```

<br>

Metadata

```py
devices = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02"
    ],
    "site": [
        "Site_A",
        "Site_B"
    ],
    "device_type": [
        "Weather",
        "Power Meter"
    ]
})
```

<br>

Merge

```py
result = pd.merge(
    telemetry,
    devices,
    on="device_id"
)

print(result)
```

---

## สิ่งที่ควรเข้าใจหลังเรียนจบ
- pd.merge()
- One-to-One
- Many-to-One
- Many-to-Many
- on
- left_on
- right_on
- inner
- left
- right
- outer
- left_index
- right_index
- join()
- suffixes

---

ตอนถัดไป `EP8 — Aggregation and Grouping`