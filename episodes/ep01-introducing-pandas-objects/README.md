# EP1 — แนะนำโครงสร้างข้อมูลใน Pandas

## เป้าหมายของตอนนี้

ในตอนนี้เราจะทำความเข้าใจ Object หลัก 3 ตัวของ Pandas:

1. `Series`
2. `DataFrame`
3. `Index`

ทั้ง 3 ตัวนี้คือพื้นฐานสำคัญก่อนเรียนเรื่องการเลือกข้อมูล การทำความสะอาดข้อมูล การรวมตาราง การทำกราฟ และการวิเคราะห์ Time-Series

---

## ทำไมต้องใช้ Pandas?

ในงานจริง ข้อมูลมักมาในรูปแบบตาราง เช่น:

- ข้อมูลจาก Sensor
- Log เครื่องจักร
- ข้อมูลพลังงานรายวัน
- ข้อมูลสภาพอากาศ
- ข้อมูลคำสั่งซื้อ
- ไฟล์ CSV จากระบบต่าง ๆ

Pandas ช่วยให้เราทำงานกับข้อมูลแบบตารางใน Python ได้ง่ายขึ้น เพราะสามารถอ้างอิงข้อมูลด้วยชื่อคอลัมน์ได้ เช่น:

```python
row["temperature_c"]
```

แทนการจำตำแหน่งแบบตัวเลข เช่น:

```python
row[2]
```

---

## การติดตั้ง

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

python3 -m venv .venv
source .venv/bin/activate

pip install pandas numpy matplotlib
```

---

## Import Library พื้นฐาน

```python
import numpy as np
import pandas as pd
```

โดยทั่วไปเราจะใช้:

- `pd` แทน Pandas
- `np` แทน NumPy

---

# 1. Pandas Series

`Series` คือข้อมูลแบบ 1 มิติที่มี Label กำกับ

มองง่าย ๆ ได้ว่า Series คือ:

- ข้อมูลหนึ่งคอลัมน์
- Array ที่มีชื่อกำกับแต่ละตำแหน่ง
- โครงสร้างคล้าย Dictionary แต่เหมาะกับงาน Data มากกว่า

## สร้าง Series จาก List

```python
import pandas as pd

power_kw = pd.Series([1.2, 1.5, 1.7, 1.4])
print(power_kw)
```

ผลลัพธ์:

```text
0    1.2
1    1.5
2    1.7
3    1.4
dtype: float64
```

Pandas จะสร้าง Index เริ่มจาก `0` ให้อัตโนมัติ

---

## ดู Values และ Index

```python
print(power_kw.values)
print(power_kw.index)
```

- `values` คือค่าข้อมูลจริง
- `index` คือ Label ที่ใช้ระบุตำแหน่งของข้อมูล

---

## เข้าถึงข้อมูลด้วย Index

```python
print(power_kw[1])
```

ผลลัพธ์:

```text
1.5
```

สามารถเลือกข้อมูลเป็นช่วงได้:

```python
print(power_kw[1:3])
```

---

## กำหนด Index เอง

```python
power_kw = pd.Series(
    [1.2, 1.5, 1.7, 1.4],
    index=["08:00", "09:00", "10:00", "11:00"]
)

print(power_kw)
```

เลือกข้อมูลจาก Label ได้:

```python
print(power_kw["09:00"])
```

เหมาะกับข้อมูลที่เกี่ยวข้องกับเวลา เช่น Sensor Logs หรือ Energy Monitoring

---

## สร้าง Series จาก Dictionary

```python
device_status = {
    "sensor_01": "online",
    "sensor_02": "offline",
    "sensor_03": "online",
    "sensor_04": "warning"
}

status_series = pd.Series(device_status)
print(status_series)
```

ในกรณีนี้:

- Key ของ Dictionary จะกลายเป็น Index
- Value ของ Dictionary จะกลายเป็นข้อมูล

---

# 2. Pandas DataFrame

`DataFrame` คือข้อมูลแบบ 2 มิติที่มี Label ทั้งแถวและคอลัมน์

มองง่าย ๆ ได้ว่า DataFrame คือ:

- ตารางข้อมูล
- Spreadsheet
- ชุดของ Series หลายคอลัมน์
- Dictionary ที่แต่ละ Key คือชื่อคอลัมน์

---

## สร้าง DataFrame จาก Dictionary

```python
import pandas as pd

data = {
    "device_id": ["sensor_01", "sensor_02", "sensor_03"],
    "temperature_c": [28.5, 29.1, 27.8],
    "humidity_percent": [65, 70, 68]
}

df = pd.DataFrame(data)
print(df)
```

ผลลัพธ์:

```text
   device_id  temperature_c  humidity_percent
0  sensor_01           28.5                65
1  sensor_02           29.1                70
2  sensor_03           27.8                68
```

---

## ดู Index และ Columns

```python
print(df.index)
print(df.columns)
```

- `df.index` แสดง Label ของแถว
- `df.columns` แสดงชื่อคอลัมน์

---

## เลือกข้อมูล 1 คอลัมน์

```python
print(df["temperature_c"])
```

ผลลัพธ์ที่ได้จะเป็น `Series`

แนวคิดสำคัญ:

> DataFrame คือโครงสร้างแบบตารางที่แต่ละคอลัมน์เป็น Series

---

## สร้าง DataFrame จาก List of Dictionaries

รูปแบบนี้พบบ่อยในข้อมูล JSON, API Response หรือ Sensor Message

```python
records = [
    {"device_id": "sensor_01", "power_kw": 1.2},
    {"device_id": "sensor_02", "power_kw": 1.5},
    {"device_id": "sensor_03", "power_kw": 1.7}
]

df_records = pd.DataFrame(records)
print(df_records)
```

---

## กรณีข้อมูลบางช่องหายไป

ถ้าข้อมูลบางแถวมี Key ไม่ครบ Pandas จะเติม `NaN` ให้อัตโนมัติ

```python
records = [
    {"device_id": "sensor_01", "power_kw": 1.2},
    {"device_id": "sensor_02", "temperature_c": 29.1},
    {"device_id": "sensor_03", "power_kw": 1.7}
]

df_missing = pd.DataFrame(records)
print(df_missing)
```

ข้อมูลจริงมักไม่สมบูรณ์เสมอ เรื่อง Missing Data จะเรียนต่อใน EP4

---

# 3. Pandas Index

`Index` คือระบบ Label ของ Pandas ใช้กับทั้ง:

- Series
- DataFrame

Index ช่วยให้ Pandas เลือกข้อมูล รวมข้อมูล และคำนวณข้อมูลได้แม่นยำขึ้น

---

## สร้าง Index

```python
idx = pd.Index(["sensor_01", "sensor_02", "sensor_03"])
print(idx)
```

---

## Index ใช้งานคล้าย Array

```python
print(idx[0])
print(idx[1:])
```

อ่านค่าได้ แต่ไม่ควรแก้ไขค่าภายใน Index โดยตรง

---

## Index แก้ไขตรง ๆ ไม่ได้

```python
# ตัวอย่างนี้จะ Error
# idx[0] = "sensor_99"
```

เหตุผลคือ Index ถูกออกแบบให้เป็น Label ที่เสถียร เพื่อช่วยให้ Pandas จัดตำแหน่งข้อมูลได้ปลอดภัยขึ้น

---

## Index ใช้เปรียบเทียบแบบ Set ได้

```python
idx_a = pd.Index(["sensor_01", "sensor_02", "sensor_03"])
idx_b = pd.Index(["sensor_02", "sensor_03", "sensor_04"])

print(idx_a.intersection(idx_b))
print(idx_a.union(idx_b))
print(idx_a.difference(idx_b))
```

เหมาะกับงาน เช่น:

- หา Sensor ที่หายไป
- เทียบข้อมูลของเมื่อวานกับวันนี้
- ตรวจสอบ Device List ก่อน Merge ข้อมูล

---

# 4. Mini Lab: ตารางข้อมูล Sensor

```python
import pandas as pd

sensor_data = {
    "timestamp": ["2026-01-01 08:00", "2026-01-01 09:00", "2026-01-01 10:00"],
    "device_id": ["sensor_01", "sensor_01", "sensor_01"],
    "temperature_c": [28.5, 29.1, 30.0],
    "humidity_percent": [65, 66, 64],
    "power_kw": [1.2, 1.4, 1.3]
}

df = pd.DataFrame(sensor_data)
print(df)
```

---

## ตรวจสอบข้อมูลเบื้องต้น

```python
print(df.head())
print(df.info())
print(df.describe())
```

คำสั่งที่ควรรู้:

- `head()` ดูข้อมูลแถวแรก ๆ
- `info()` ดูชนิดข้อมูลและค่าว่าง
- `describe()` ดูสถิติพื้นฐานของคอลัมน์ตัวเลข

---

## เลือก 1 คอลัมน์

```python
print(df["power_kw"])
```

---

## เพิ่มคอลัมน์ใหม่

```python
df["energy_score"] = df["power_kw"] * 100
print(df)
```

การสร้างคอลัมน์ใหม่เป็นพื้นฐานของ Feature Engineering สำหรับงาน Visualization และ Machine Learning

---

# 5. สรุป

1. `Series` คือข้อมูล 1 คอลัมน์ที่มี Label
2. `DataFrame` คือตารางที่ประกอบจาก Series หลายคอลัมน์
3. `Index` คือระบบ Label ของแถว
4. Pandas เหมาะกับข้อมูลแบบตารางและข้อมูลจริง
5. ข้อมูลจริงมักมาในรูปแบบ CSV, Logs, Records หรือ JSON

---

# 6. การบ้าน

ลองสร้าง DataFrame ที่มีคอลัมน์ดังนี้:

- `timestamp`
- `device_id`
- `voltage_v`
- `current_a`
- `status`

แล้วตอบคำถาม:

1. คอลัมน์ไหนเป็นตัวเลข?
2. คอลัมน์ไหนเป็นข้อความ?
3. `df.index` แสดงอะไร?
4. `df.columns` แสดงอะไร?
5. เมื่อเลือก 1 คอลัมน์ ผลลัพธ์เป็นชนิดใด?

---

# 7. ตอนถัดไป

EP2 จะเรียนเรื่อง **Data Indexing and Selection**

หัวข้อที่จะเจอ:

- การเลือกแถว
- การเลือกคอลัมน์
- ความต่างของ `loc` และ `iloc`
- การกรองข้อมูลด้วยเงื่อนไข
