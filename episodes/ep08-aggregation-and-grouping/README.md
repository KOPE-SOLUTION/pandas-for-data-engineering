# EP08 — aggregation and grouping

## เป้าหมายของตอนนี้

หลังจากที่เราเรียนการรวมข้อมูลด้วย Merge และ Join ไปแล้ว ขั้นตอนถัดไปในงาน Data Engineering คือการสรุปข้อมูล (Aggregation)

ตัวอย่างงานจริง:
- ค่าเฉลี่ยอุณหภูมิราย Site
- พลังงานรวมรายวัน
- จำนวน Alarm ต่อ Device
- ค่า Max/Min ของ Sensor
- จำนวนข้อมูลที่เก็บได้ในแต่ละ Site

Pandas ใช้ `groupby()` ในการทำสิ่งเหล่านี้

---

## 1. Import Library

```py
import pandas as pd 
import numpy as np
```

---

## 2. สร้างข้อมูล Sensor

```py
sensor_data = pd.DataFrame({
    "site": [
        "site_a", "site_a",
        "site_b", "site_b",
        "site_c", "site_c"
    ],
    "device_id": [
        "sensor_01", "sensor_02",
        "sensor_03", "sensor_04",
        "sensor_05", "sensor_06"
    ],
    "temperature_c": [
        28.5, 29.1,
        30.2, 30.8,
        27.9, 28.3
    ],
    "power_kw": [
        1.2, 1.4,
        1.8, 2.0,
        1.1, 1.3
    ]
})

print(sensor_data)
```

---

## 3. Aggregation พื้นฐาน

### ค่าเฉลี่ย

```py
print(
    sensor_data["temperature_c"].mean()
)
```

### ค่าสูงสุด

```py
print(
    sensor_data["temperature_c"].max()
)
```

### ค่าต่ำสุด

```py
print(
    sensor_data["temperature_c"].min()
)
```

### ผลรวม

```py
print(
    sensor_data["power_kw"].sum()
)
```

### จำนวนข้อมูล

```py
print(
    sensor_data["device_id"].count()
)
```

---

## 4. describe()

ดูสถิติทั้งหมดพร้อมกัน

```py
print(
    sensor_data.describe()
)
```

ได้ผลลัพธ์เช่น:
- count
- mean
- std
- min
- max
- quartile

---

## 5. GroupBy

ค่าเฉลี่ยราย Site

```py
print(
    sensor_data.groupby("site").mean(
        numeric_only=True
    )
)
```

ผลลัพธ์:
```sh
site_a
site_b
site_c
```

Pandas จะทำให้ดังนี้
- Split : แยกตาม site
- Apply : คำนวณ mean
- Combine : รวมผลลัพธ์

---

## 6. GroupBy หลายคอลัมน์

```py
print(
    sensor_data.groupby(
        ["site", "device_id"]
    ).mean(
        numeric_only=True
    )
)
```

จะได้ MultiIndex อัตโนมัติ

---

## 7. เลือกเฉพาะคอลัมน์ก่อน Aggregate

```py
print(
    sensor_data
    .groupby("site")["power_kw"]
    .sum()
)
```

คำนวณเฉพาะ power_kw

---

## 8. Aggregate หลายฟังก์ชันพร้อมกัน

```py
print(
    sensor_data.groupby("site")
    .agg({
        "temperature_c": [
            "mean",
            "max",
            "min"
        ],
        "power_kw": [
            "sum",
            "mean"
        ]
    })
)
```

ตัวอย่างงานจริง:
- อุณหภูมิเฉลี่ย
- อุณหภูมิสูงสุด
- พลังงานรวม

---

## 9. GroupBy + Count Alarm

```py
alarm_data = pd.DataFrame({
    "site": [
        "site_a",
        "site_a",
        "site_b",
        "site_b",
        "site_b"
    ],
    "alarm": [
        "Over Temp",
        "Offline",
        "Offline",
        "Low Power",
        "Offline"
    ]
})

print(
    alarm_data.groupby("site")
    .size()
)
```

นับจำนวน Alarm ต่อ Site

## 10. value_counts()

```py
print(
    alarm_data["alarm"]
    .value_counts()
)
```

ใช้บ่อยมากในงาน Data Analysis

## 11. Mini Lab

หาพลังงานรวมของแต่ละ Site

```py
result = (
    sensor_data
    .groupby("site")["power_kw"]
    .sum()
)

print(result)
```

---

## 12. 12. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. mean()
2. max()
3. min()
4. sum()
5. count()
6. describe()
7. groupby()
8. agg()
9. size()
10. value_counts()

---

## ตอนถัดไป

`EP9 — Pivot Table`