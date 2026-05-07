
# EP4 — Handling Missing Data

## เป้าหมายของตอนนี้

ในโลกจริง ข้อมูลมักไม่สมบูรณ์เสมอไป

ตัวอย่าง:
- Sensor ส่งข้อมูลไม่ครบ
- API ส่งค่า null
- CSV บางช่องว่าง
- Device Offline
- ข้อมูลบางช่วงหายไป

ใน EP นี้ เราจะเรียนรู้วิธีจัดการ Missing Data ใน Pandas

หัวข้อสำคัญ:
- NaN และ None
- Missing Values
- isnull()
- notnull()
- dropna()
- fillna()
- Forward Fill / Backward Fill

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. Missing Data คืออะไร

Missing Data คือข้อมูลที่หายไป หรือไม่มีค่า

ตัวอย่าง:

| device_id | temperature_c |
|---|---|
| sensor_01 | 28.5 |
| sensor_02 | NaN |
| sensor_03 | 30.1 |

ค่า NaN หมายถึง:

```text
Not a Number
```

Pandas ใช้ NaN เพื่อแทนข้อมูลที่หายไป

---

# 3. None และ NaN

## None

```python
data = [1, None, 3]
print(data)
```

None คือ object ของ Python

---

## NaN

```python
data = [1, np.nan, 3]
print(data)
```

NaN เป็นค่าพิเศษของ NumPy/Pandas

---

# 4. Series ที่มี Missing Data

```python
sensor_data = pd.Series(
    [28.5, np.nan, 30.1, None]
)

print(sensor_data)
```

---

# 5. ตรวจสอบ Missing Value

## isnull()

```python
print(sensor_data.isnull())
```

---

## notnull()

```python
print(sensor_data.notnull())
```

---

# 6. Filter เฉพาะข้อมูลที่ไม่หาย

```python
print(
    sensor_data[
        sensor_data.notnull()
    ]
)
```

---

# 7. dropna()

```python
print(sensor_data.dropna())
```

---

# 8. DataFrame ที่มี Missing Data

```python
df = pd.DataFrame({
    "device_id": [
        "sensor_01",
        "sensor_02",
        "sensor_03"
    ],
    "temperature_c": [
        28.5,
        np.nan,
        30.1
    ],
    "humidity_percent": [
        65,
        66,
        np.nan
    ]
})

print(df)
```

---

# 9. ลบ Row ที่มี Missing Data

```python
print(df.dropna())
```

---

# 10. ลบ Column ที่มี Missing Data

```python
print(
    df.dropna(axis=1)
)
```

---

# 11. fillna()

```python
print(
    df.fillna(0)
)
```

---

# 12. Fill ด้วยค่าเฉลี่ย

```python
mean_temp = df["temperature_c"].mean()

df["temperature_c"] = df["temperature_c"].fillna(mean_temp)

print(df)
```

---

# 13. Forward Fill (ffill)

```python
power_data = pd.Series(
    [1.2, np.nan, np.nan, 1.5]
)

print(
    power_data.fillna(method="ffill")
)
```

---

# 14. Backward Fill (bfill)

```python
print(
    power_data.fillna(method="bfill")
)
```

---

# 15. Mini Lab — IoT Sensor Data

```python
iot_df = pd.DataFrame({
    "timestamp": [
        "08:00",
        "09:00",
        "10:00",
        "11:00"
    ],
    "temperature_c": [
        28.5,
        np.nan,
        30.1,
        np.nan
    ],
    "power_kw": [
        1.2,
        1.3,
        np.nan,
        1.5
    ]
})

print(iot_df)
```

---

## ตรวจสอบ Missing Data

```python
print(iot_df.isnull())
```

---

## เติม Missing Value

```python
iot_df = iot_df.fillna(method="ffill")

print(iot_df)
```

---

# 16. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. Missing Data คืออะไร
2. NaN และ None
3. isnull() และ notnull()
4. dropna()
5. fillna()
6. Forward Fill / Backward Fill
7. การจัดการข้อมูลจริงที่ไม่สมบูรณ์

---

# 17. คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---|---|
| Missing Data | ข้อมูลหาย |
| NaN | Not a Number |
| Null Value | ค่าว่าง |
| fillna() | เติมค่าที่หาย |
| dropna() | ลบข้อมูลที่หาย |
| ffill | ใช้ค่าก่อนหน้า |
| bfill | ใช้ค่าถัดไป |

---

# 18. ตอนถัดไป

EP5 — Hierarchical Indexing
