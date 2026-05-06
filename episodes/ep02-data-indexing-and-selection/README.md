# EP2 — Data Indexing and Selection

## เป้าหมายของตอนนี้

ใน EP นี้ เราจะเรียนรู้การเลือกและเข้าถึงข้อมูลใน Pandas ซึ่งเป็นพื้นฐานสำคัญของงาน Data Analysis และ Data Engineering

หัวข้อหลักที่จะเรียน:
- การเลือกข้อมูลใน Series
- การเลือกข้อมูลใน DataFrame
- การใช้งาน `loc`
- การใช้งาน `iloc`
- Filtering และ Masking
- การเลือกข้อมูลแบบหลายเงื่อนไข

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. สร้าง Series เบื้องต้น

```python
import pandas as pd

temperature = pd.Series(
    [28.5, 29.1, 30.0, 29.4],
    index=["08:00", "09:00", "10:00", "11:00"]
)

print(temperature)
```

---

# 3. การเลือกข้อมูลจาก Series

## เลือกด้วย Label

```python
print(temperature["09:00"])
```

---

## เลือกหลายค่า

```python
print(temperature[["08:00", "10:00"]])
```

---

## Slicing

```python
print(temperature["08:00":"10:00"])
```

---

# 4. Filtering และ Masking

```python
print(temperature[temperature > 29])
```

---

## หลายเงื่อนไข

```python
print(
    temperature[
        (temperature > 28.8) & (temperature < 30)
    ]
)
```

---

# 5. การเพิ่มข้อมูลใหม่ใน Series

```python
temperature["12:00"] = 31.2

print(temperature)
```

---

# 6. การสร้าง DataFrame

```python
sensor_data = {
    "device_id": ["sensor_01", "sensor_02", "sensor_03"],
    "temperature_c": [28.5, 29.1, 30.0],
    "humidity_percent": [65, 66, 64],
    "power_kw": [1.2, 1.4, 1.3]
}

df = pd.DataFrame(sensor_data)

print(df)
```

---

# 7. เลือก Column

```python
print(df["temperature_c"])
```

---

## เลือกหลาย Column

```python
print(df[["temperature_c", "power_kw"]])
```

---

# 8. การใช้งาน loc

```python
print(df.loc[0])
```

---

## เลือก Row และ Column

```python
print(df.loc[0:1, ["device_id", "power_kw"]])
```

---

# 9. การใช้งาน iloc

```python
print(df.iloc[0])
```

---

## เลือกหลาย Row และ Column

```python
print(df.iloc[0:2, 1:3])
```

---

# 10. เปรียบเทียบ loc และ iloc

| คำสั่ง | ใช้อะไรอ้างอิง |
|---|---|
| loc | Label |
| iloc | Position |

---

# 11. Filtering DataFrame

```python
print(df[df["power_kw"] > 1.25])
```

---

## หลายเงื่อนไข

```python
print(
    df[
        (df["temperature_c"] > 28.8) &
        (df["humidity_percent"] < 66)
    ]
)
```

---

# 12. การแก้ไขข้อมูล

```python
df.loc[0, "power_kw"] = 1.5

print(df)
```

---

# 13. Mini Lab — Sensor Monitoring

```python
sensor_logs = {
    "timestamp": [
        "2026-01-01 08:00",
        "2026-01-01 09:00",
        "2026-01-01 10:00",
        "2026-01-01 11:00"
    ],
    "device_id": [
        "sensor_01",
        "sensor_01",
        "sensor_01",
        "sensor_01"
    ],
    "temperature_c": [28.5, 29.1, 30.0, 31.2],
    "power_kw": [1.2, 1.3, 1.4, 1.6]
}

df_logs = pd.DataFrame(sensor_logs)

print(df_logs)
```

---

## Filter ข้อมูล

```python
high_power = df_logs[df_logs["power_kw"] > 1.3]

print(high_power)
```

---

## เลือกเฉพาะ Column สำคัญ

```python
print(
    high_power[
        ["timestamp", "power_kw"]
    ]
)
```

---

# 14. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. การเลือกข้อมูลจาก Series
2. การเลือกข้อมูลจาก DataFrame
3. ความแตกต่างระหว่าง `loc` และ `iloc`
4. การ Filtering ข้อมูล
5. การเลือกข้อมูลด้วยหลายเงื่อนไข
6. การแก้ไขข้อมูลใน DataFrame

---

# 15. ตอนถัดไป

EP3 — Operating on Data in Pandas
