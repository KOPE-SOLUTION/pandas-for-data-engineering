# EP09 — Pivot Tables

## เป้าหมายของตอนนี้

หลังจากเรียน GroupBy ไปแล้ว ในตอนนี้เราจะเรียนรู้ Pivot Table ซึ่งช่วยให้สรุปข้อมูลหลายมิติได้ง่ายและอ่านผลลัพธ์ได้สวยกว่า GroupBy ในหลายกรณี

Pivot Table ถูกใช้งานบ่อยใน
- Data Analysis
- Data Engineering
- Business Intelligence (BI)
- Dashboard
- IoT Monitoring
- Energy Management

---

## 1. Import Library

```py
import pandas as pd
import numpy as np
```

## 2. สร้างข้อมูลตัวอย่าง

```py
monitoring = pd.DataFrame({
    "site": [
        "site_a",
        "site_a",
        "site_b",
        "site_b",
        "site_c",
        "site_c"
    ],
    "device_type": [
        "power_meter",
        "temperature_sensor",
        "power_meter",
        "temperature_sensor",
        "power_meter",
        "temperature_sensor"
    ],
    "value": [
        120,
        28.5,
        150,
        30.2,
        110,
        27.9
    ]
})

print(monitoring)
```

---

## 3. Pivot Table คืออะไร

Pivot Table คือ สรุปข้อมูล โดยจัดเป็นตาราง ตาม Row และ Column ที่ต้องการ

แนวคิด

`Raw Data --> Pivot Table --> Summary Table`

---

## 4. Pivot Table พื้นฐาน

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site"
)
```

<br>

ผลลัพธ์

```sh
site
site_a
site_b
site_c
```

สรุปค่าเฉลี่ยต่อ Site

---

## 5. กำหนด Columns

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    columns="device_type"
)
```

<br>

ผลลัพธ์

```sh
device_type
                power_meter
                temperature_sensor

site_a
site_b
site_c
```

## เปรียบเทียบกับ GroupBy

GroupBy

```py
monitoring.groupby(
    ["site", "device_type"]
).mean(
    numeric_only=True
)
```

<br>

Pivot Table

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    columns="device_type"
)
```

Pivot Table อ่านง่ายกว่า

---

## 7. aggfunc

ค่า Default คือ mean

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    aggfunc="mean"
)
```

---

## 8. ใช้ sum

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    aggfunc="sum"
)
```

---

## 9. ใช้ count

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    aggfunc="count"
)
```

---

## 10. หลาย Aggregation

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    aggfunc=[
        "mean",
        "min",
        "max",
        "count"
    ]
)
```

## 11. margins=True

เพิ่ม Grand Total

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    aggfunc="mean",
    margins=True
)
```

<br>

ผลลัพธ์

```sh
site_a
site_b
site_c
All
```

---

## 12. fill_value

แทนค่า NaN

```py
pd.pivot_table(
    monitoring,
    values="value",
    index="site",
    columns="device_type",
    fill_value=0
)
```

---

## 13. ตัวอย่างจริงในงาน Energy Monitoring

```py
energy = pd.DataFrame({
    "building": [
        "A","A","A",
        "B","B","B"
    ],
    "month": [
        "Jan","Feb","Mar",
        "Jan","Feb","Mar"
    ],
    "kwh": [
        1200,
        1300,
        1400,
        1500,
        1450,
        1600
    ]
})

pd.pivot_table(
    energy,
    values="kwh",
    index="building",
    columns="month",
    aggfunc="sum"
)
```

ผลลัพธ์

```sh
           Jan   Feb   Mar
A         1200  1300  1400
B         1500  1450  1600
```

---

## 14. Mini Lab

สรุปค่าเฉลี่ยอุณหภูมิ

```py
temperature_logs = pd.DataFrame({
    "site": [
        "A","A",
        "B","B",
        "C","C"
    ],
    "device_id": [
        "sensor_01",
        "sensor_02",
        "sensor_03",
        "sensor_04",
        "sensor_05",
        "sensor_06"
    ],
    "temperature_c": [
        28.5,
        29.1,
        30.2,
        30.8,
        27.9,
        28.3
    ]
})
```

```py
result = pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc="mean"
)

print(result)
```

---

## 15. สิ่งที่ควรเข้าใจหลังเรียนจบ
1. pivot_table()
2. values
3. index
4. columns
5. aggfunc
6. mean
7. sum
8. count
9. margins
10. fill_value

---

## ตอนถัดไป

`EP10 — Working with Time Series`