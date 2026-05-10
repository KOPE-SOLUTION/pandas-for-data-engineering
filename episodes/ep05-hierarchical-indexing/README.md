# EP5 — Hierarchical Indexing

## เป้าหมายของตอนนี้

ใน EP นี้ เราจะเรียนรู้การจัดข้อมูลแบบหลายระดับใน Pandas หรือที่เรียกว่า MultiIndex

แนวคิดนี้สำคัญมากเมื่อต้องทำงานกับข้อมูลจริง เช่น:

- หลาย Site
- หลาย Device
- หลาย Timestamp
- หลาย Sensor Type
- ข้อมูล IoT / Sensor / Monitoring

ตัวอย่างข้อมูลจริงมักไม่ได้มีแค่ 1 มิติหรือ 2 มิติ แต่มีหลายมิติ เช่น:

```text
site / device / timestamp / measurement
```

Pandas จึงมี MultiIndex เพื่อช่วยจัดโครงสร้างข้อมูลแบบนี้ให้เป็นระบบ

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. Hierarchical Indexing คืออะไร

Hierarchical Indexing คือการมี Index มากกว่า 1 ระดับในข้อมูลชุดเดียว

ตัวอย่างปกติ:

```text
timestamp
```

<br>

ตัวอย่างแบบหลายระดับ:

```text
site / device
```

หรือ:

```text
site / device / timestamp
```

---

# 3. ทำไมต้องใช้ MultiIndex

ถ้าข้อมูลมีหลายมิติ เช่น ข้อมูล Sensor จากหลายจุด การใช้ Index ชั้นเดียวอาจไม่พอ

ตัวอย่าง:

| site | device_id | temperature_c |
|---|---|---|
| site_a | sensor_01 | 28.5 |
| site_a | sensor_02 | 29.1 |
| site_b | sensor_01 | 30.0 |
| site_b | sensor_02 | 27.8 |

ถ้าเราตั้ง `site` และ `device_id` เป็น Index พร้อมกัน จะทำให้เลือกข้อมูลได้ง่ายขึ้นมาก

---

# 4. สร้าง DataFrame เบื้องต้น

```python
df = pd.DataFrame({
    "site": [
        "site_a", "site_a",
        "site_b", "site_b"
    ],
    "device_id": [
        "sensor_01", "sensor_02",
        "sensor_01", "sensor_02"
    ],
    "temperature_c": [
        28.5, 29.1,
        30.0, 27.8
    ],
    "power_kw": [
        1.2, 1.4,
        1.6, 1.1
    ]
})

print(df)
```

---

# 5. สร้าง MultiIndex ด้วย set_index()

```python
df_multi = df.set_index(["site", "device_id"])

print(df_multi)
```

ผลลัพธ์จะเป็น DataFrame ที่มี Index 2 ระดับ:

```text
site    device_id
site_a  sensor_01
        sensor_02
site_b  sensor_01
        sensor_02
```

---

# 6. ดูชื่อระดับของ Index

```python
print(df_multi.index.names)
```

ผลลัพธ์:

```text
['site', 'device_id']
```

---

# 7. เลือกข้อมูลจาก Index ระดับแรก

เลือกข้อมูลทั้งหมดของ `site_a`

```python
print(df_multi.loc["site_a"])
```

---

# 8. เลือกข้อมูลจาก Index หลายระดับ

เลือกข้อมูลของ `site_a` และ `sensor_01`

```python
print(df_multi.loc[("site_a", "sensor_01")])
```

---

# 9. เลือกเฉพาะบาง Column

```python
print(
    df_multi.loc[
        ("site_a", "sensor_01"),
        "temperature_c"
    ]
)
```

---

# 10. reset_index()

ถ้าต้องการเปลี่ยน MultiIndex กลับมาเป็น Column ปกติ ใช้:

```python
df_reset = df_multi.reset_index()

print(df_reset)
```

ใช้บ่อยมากเมื่อต้อง Export เป็น CSV หรือเตรียมข้อมูลสำหรับ Visualization

---

# 11. MultiIndex จาก from_product()

ใช้สร้างชุด Index จากการจับคู่ค่าหลายชุดเข้าด้วยกัน

```python
index = pd.MultiIndex.from_product(
    [
        ["site_a", "site_b"],
        ["sensor_01", "sensor_02"]
    ],
    names=["site", "device_id"]
)

print(index)
```

---

# 12. สร้าง DataFrame จาก MultiIndex

```python
df2 = pd.DataFrame(
    {
        "temperature_c": [28.5, 29.1, 30.0, 27.8],
        "power_kw": [1.2, 1.4, 1.6, 1.1]
    },
    index=index
)

print(df2)
```

---

# 13. MultiIndex กับ Time-Series

ตัวอย่างข้อมูล Sensor ที่มี site, device และ timestamp

```python
df_time = pd.DataFrame({
    "site": [
        "site_a", "site_a", "site_a", "site_a",
        "site_b", "site_b", "site_b", "site_b"
    ],
    "device_id": [
        "sensor_01", "sensor_01", "sensor_02", "sensor_02",
        "sensor_01", "sensor_01", "sensor_02", "sensor_02"
    ],
    "timestamp": [
        "08:00", "09:00", "08:00", "09:00",
        "08:00", "09:00", "08:00", "09:00"
    ],
    "temperature_c": [
        28.5, 29.0, 27.8, 28.2,
        30.1, 30.3, 29.5, 29.7
    ]
})

print(df_time)
```

---

## ตั้ง MultiIndex 3 ระดับ

```python
df_time_multi = df_time.set_index(
    ["site", "device_id", "timestamp"]
)

print(df_time_multi)
```

---

# 14. เลือกข้อมูลจาก MultiIndex 3 ระดับ

เลือกข้อมูลทั้งหมดของ site_a

```python
print(df_time_multi.loc["site_a"])
```

เลือกข้อมูลของ site_a / sensor_01

```python
print(df_time_multi.loc[("site_a", "sensor_01")])
```

เลือกข้อมูลของ site_a / sensor_01 / 08:00

```python
print(df_time_multi.loc[("site_a", "sensor_01", "08:00")])
```

---

# 15. unstack()

`unstack()` ใช้เปลี่ยน Index บางระดับให้กลายเป็น Column

```python
print(df_time_multi.unstack())
```

เหมาะสำหรับการทำตารางเปรียบเทียบ หรือเตรียมข้อมูลสำหรับ Dashboard

---

# 16. stack()

`stack()` ใช้เปลี่ยน Column กลับไปเป็น Index

```python
unstacked = df_time_multi.unstack()

print(unstacked.stack())
```

---

# 17. sort_index()

MultiIndex ควรถูก sort ก่อนใช้งาน slicing บางรูปแบบ

```python
df_time_multi = df_time_multi.sort_index()

print(df_time_multi)
```

---

# 18. Group และ Aggregation กับ MultiIndex

หาค่าเฉลี่ยอุณหภูมิตาม site

```python
print(
    df_time_multi.groupby(level="site").mean()
)
```

หาค่าเฉลี่ยตาม device_id

```python
print(
    df_time_multi.groupby(level="device_id").mean()
)
```

---

# 19. Mini Lab — Monitoring Data

สร้างข้อมูล Monitoring แบบหลายระดับ

```python
monitoring_df = pd.DataFrame({
    "site": [
        "factory_a", "factory_a", "factory_a",
        "factory_b", "factory_b", "factory_b"
    ],
    "device_id": [
        "meter_01", "meter_01", "meter_02",
        "meter_01", "meter_02", "meter_02"
    ],
    "timestamp": [
        "08:00", "09:00", "08:00",
        "08:00", "08:00", "09:00"
    ],
    "power_kw": [
        1.2, 1.4, 1.1,
        1.8, 1.5, 1.6
    ]
})

monitoring_multi = monitoring_df.set_index(
    ["site", "device_id", "timestamp"]
)

print(monitoring_multi)
```

---

## เลือกข้อมูลของ factory_a

```python
print(monitoring_multi.loc["factory_a"])
```

---

## เลือกข้อมูลของ meter_02 ทุก site

```python
print(
    monitoring_multi[
        monitoring_multi.index.get_level_values("device_id") == "meter_02"
    ]
)
```

---

## หาค่าเฉลี่ย power_kw ตาม site

```python
print(
    monitoring_multi.groupby(level="site")["power_kw"].mean()
)
```

---

# 20. สิ่งที่ควรเข้าใจหลังเรียนจบ

หลังจาก EP นี้ คุณควรเข้าใจ:

1. Hierarchical Indexing คืออะไร
2. MultiIndex ใช้ทำอะไร
3. set_index() สำหรับสร้าง MultiIndex
4. reset_index() สำหรับแปลง Index กลับเป็น Column
5. เลือกข้อมูลจาก Index หลายระดับด้วย loc
6. stack() และ unstack()
7. sort_index()
8. groupby(level=...) สำหรับสรุปข้อมูลตาม Index Level

---

# 21. คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---|---|
| Hierarchical Indexing | การทำ Index หลายระดับ |
| MultiIndex | Index หลายชั้นใน Pandas |
| Level | ระดับของ Index |
| set_index() | ตั้ง Column ให้เป็น Index |
| reset_index() | เปลี่ยน Index กลับเป็น Column |
| stack() | ย้าย Column ลงมาเป็น Index |
| unstack() | ย้าย Index ขึ้นไปเป็น Column |
| sort_index() | เรียง Index |
| groupby(level=...) | จัดกลุ่มตามระดับของ Index |

---

# 22. ลำดับการสอนแนะนำ

1. อธิบายปัญหาของข้อมูลหลายระดับ
2. ยกตัวอย่าง site / device / timestamp
3. สร้าง DataFrame ปกติ
4. ใช้ set_index()
5. เลือกข้อมูลด้วย loc
6. ใช้ reset_index()
7. สร้าง MultiIndex 3 ระดับ
8. ทดลอง stack() / unstack()
9. ทำ Mini Lab
10. สรุปว่าทำไม MultiIndex สำคัญกับ Data Engineering

---

# 23. การบ้าน

สร้าง DataFrame ที่มี Column:

- site
- device_id
- timestamp
- voltage_v
- current_a

จากนั้นให้ทำ:

1. ตั้ง MultiIndex ด้วย site, device_id, timestamp
2. เลือกข้อมูลของ site ใด site หนึ่ง
3. เลือกข้อมูลของ device_id ใด device_id หนึ่ง
4. คำนวณค่าเฉลี่ย voltage_v ตาม site
5. reset_index() กลับมาเป็น DataFrame ปกติ

---

# 24. ตอนถัดไป

EP6 — Combining Datasets: Concat and Append

เราจะเรียนรู้:
- การรวมข้อมูลหลายไฟล์
- การต่อข้อมูลหลายวัน
- การรวม Sensor Logs
- concat()
