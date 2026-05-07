
# EP3 — Operating on Data in Pandas

## เป้าหมายของตอนนี้

ใน EP นี้ เราจะเรียนรู้การคำนวณข้อมูลใน Pandas ทั้งระดับ Series และ DataFrame

หัวข้อสำคัญ:
- Arithmetic Operations
- NumPy Functions กับ Pandas
- Index Alignment
- Operations ระหว่าง DataFrame และ Series
- Broadcasting
- การจัดการข้อมูลที่ Index ไม่ตรงกัน

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. Arithmetic Operations บน Series

```python
power = pd.Series([1.2, 1.5, 1.7])

print(power * 100)
```

---

## การบวกข้อมูล

```python
print(power + 10)
```

---

## การคำนวณหลายแบบ

```python
print((power * 1000) / 2)
```

---

# 3. NumPy Functions กับ Pandas

```python
print(np.sqrt(power))
```

---

## ตัวอย่างเพิ่มเติม

```python
print(np.exp(power))
```

---

# 4. DataFrame Operations

```python
sensor_data = {
    "temperature_c": [28.5, 29.1, 30.0],
    "humidity_percent": [65, 66, 64],
    "power_kw": [1.2, 1.4, 1.3]
}

df = pd.DataFrame(sensor_data)

print(df)
```

---

## คูณทุกค่าใน DataFrame

```python
print(df * 2)
```

---

## คำนวณเฉพาะ Column

```python
df["power_w"] = df["power_kw"] * 1000

print(df)
```

---

# 5. Index Alignment ใน Series

> Pandas พยายาม “จับคู่ข้อมูลตามชื่อ Index” ก่อนคำนวณ

```python
A = pd.Series(
    [10, 20, 30],
    index=["sensor_01", "sensor_02", "sensor_03"]
)

B = pd.Series(
    [1, 2, 3],
    index=["sensor_02", "sensor_03", "sensor_04"]
)

print(A + B)
```

---

# 6. การจัดการ Missing Value ระหว่าง Operation

```python
print(A.add(B, fill_value=0))
```

---

# 7. Operations บน DataFrame

```python
df_a = pd.DataFrame(
    [[1, 2], [3, 4]],
    columns=["A", "B"]
)

df_b = pd.DataFrame(
    [[10, 20], [30, 40]],
    columns=["B", "A"]
)

print(df_a + df_b)
```

---

# 8. DataFrame กับ Series

```python
df = pd.DataFrame(
    [[3, 8, 2],
     [4, 6, 5],
     [7, 1, 9]],
    columns=["A", "B", "C"]
)

print(df)
```

---

## ลบด้วย Row แรก

<details>
<summary>💡 Check data Type!</summary>

```py
type(df)
type(df.iloc[0])
```

</details>

```python
print(df - df.iloc[0])
```

---

# 9. Column-wise Operations

```python
print(
    df.subtract(df["B"], axis=0)
)
```

---

# 10. Mini Lab — Energy Monitoring

```python
energy_data = {
    "device_id": ["meter_01", "meter_02", "meter_03"],
    "power_kw": [1.2, 1.5, 1.3],
    "voltage_v": [220, 221, 219]
}

df_energy = pd.DataFrame(energy_data)

print(df_energy)
```

---

## คำนวณ Power เป็น Watt

```python
df_energy["power_w"] = df_energy["power_kw"] * 1000

print(df_energy)
```

---

# 11. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. Arithmetic Operations ใน Pandas
2. NumPy Functions ใช้กับ Pandas ได้
3. Pandas Align Index อัตโนมัติ
4. DataFrame Operations
5. Broadcasting
6. การจัดการ Missing Value ระหว่าง Operation

---

# 12. ตอนถัดไป

EP4 — Handling Missing Data
