
# EP6 — Combining Datasets: Concat and Append

## เป้าหมายของตอนนี้

ในโลกจริง ข้อมูลมักมาจากหลายแหล่ง เช่น:
- หลาย CSV
- หลาย Sensor
- หลายวัน
- หลาย Site
- หลาย Device

ดังนั้นเราจึงต้องเรียนรู้การรวมข้อมูลด้วย Pandas

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. pd.concat()

ใช้สำหรับรวม Series หรือ DataFrame

---

# 3. รวม Series

```python
ser1 = pd.Series([1.2, 1.4, 1.5])
ser2 = pd.Series([1.8, 1.9])

result = pd.concat([ser1, ser2])

print(result)
```

---

# 4. รวม DataFrame แบบแนวตั้ง

```python
df1 = pd.DataFrame({
    "device_id": ["sensor_01", "sensor_02"],
    "power_kw": [1.2, 1.4]
})

df2 = pd.DataFrame({
    "device_id": ["sensor_03", "sensor_04"],
    "power_kw": [1.6, 1.8]
})

result = pd.concat([df1, df2])

print(result)
```

---

## axis=0

```text
ต่อแนวตั้ง
เพิ่ม row
```

---

# 5. ignore_index=True

```python
result = pd.concat(
    [df1, df2],
    ignore_index=True
)

print(result)
```

Pandas จะสร้าง index ใหม่

---

# 6. รวมแบบแนวนอน

```python
df_left = pd.DataFrame({
    "temperature_c": [28.5, 29.1]
})

df_right = pd.DataFrame({
    "humidity_percent": [65, 66]
})

result = pd.concat(
    [df_left, df_right],
    axis=1
)

print(result)
```

---

## axis=1

```text
ต่อแนวนอน
เพิ่ม column
```

---

# 7. outer join

```python
df_a = pd.DataFrame({
    "A": [1, 2],
    "B": [3, 4]
})

df_b = pd.DataFrame({
    "B": [5, 6],
    "C": [7, 8]
})

result = pd.concat([df_a, df_b])

print(result)
```

Column ที่ไม่มีข้อมูลจะกลายเป็น NaN

---

# 8. inner join

```python
result = pd.concat(
    [df_a, df_b],
    join="inner"
)

print(result)
```

จะเหลือเฉพาะ column ที่เหมือนกัน

---

# 9. verify_integrity=True

```python
df_x = pd.DataFrame({
    "value": [1, 2]
}, index=[0, 1])

df_y = pd.DataFrame({
    "value": [3, 4]
}, index=[0, 1])

pd.concat(
    [df_x, df_y],
    verify_integrity=True
)
```

ใช้ตรวจสอบ index ซ้ำ

---

# 10. keys=

```python
result = pd.concat(
    [df1, df2],
    keys=["day_01", "day_02"]
)

print(result)
```

จะสร้าง MultiIndex

---

# 11. append()

```python
result = df1.append(df2)

print(result)
```

---

# 12. Mini Lab — Sensor Logs

```python
day1 = pd.DataFrame({
    "timestamp": ["08:00", "09:00"],
    "power_kw": [1.2, 1.4]
})

day2 = pd.DataFrame({
    "timestamp": ["10:00", "11:00"],
    "power_kw": [1.5, 1.6]
})

sensor_logs = pd.concat(
    [day1, day2],
    ignore_index=True
)

print(sensor_logs)
```

---

# 13. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. concat()
2. axis=0
3. axis=1
4. ignore_index
5. outer join
6. inner join
7. keys
8. append()

---

# 14. ตอนถัดไป

EP7 — Merge and Join
