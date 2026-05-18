# EP6 — Combining Datasets: Concat and Append

## เป้าหมายของตอนนี้

ในโลกจริง ข้อมูลมักไม่ได้มาเป็นไฟล์เดียวจบ แต่จะมาจากหลายแหล่ง เช่น หลาย CSV, หลายวัน, หลาย Sensor, หลาย Site หรือหลายระบบ Monitoring

ใน EP นี้เราจะเรียนรู้วิธีรวมข้อมูลด้วย Pandas โดยเน้นตัวอย่างที่สมเหตุสมผลกับงาน Sensor / IoT / Data Engineering

หัวข้อหลัก:
- `pd.concat()`
- `axis=0`
- `axis=1`
- `ignore_index=True`
- `join="outer"`
- `join="inner"`
- `keys=`
- `verify_integrity=True`
- ทำไม `append()` ถูกลบออกแล้ว

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. pd.concat() คืออะไร

`pd.concat()` ใช้สำหรับรวมข้อมูลหลายชุดเข้าด้วยกัน

ใช้ได้กับ:
- Series
- DataFrame
- ข้อมูลหลายวัน
- ข้อมูลหลายไฟล์
- ข้อมูลหลาย site
- ข้อมูลหลาย device

แนวคิด:

```text
day1 + day2 + day3 = all_logs
```

---

# 3. รวม Series

```python
ser1 = pd.Series([1.2, 1.4, 1.5])
ser2 = pd.Series([1.8, 1.9])

result = pd.concat([ser1, ser2])

print(result)
```

ตัวอย่างนี้เป็นการรวมข้อมูลแบบง่ายที่สุด

---

# 4. รวม DataFrame แบบแนวตั้ง

ตัวอย่างนี้สมมุติว่าเรามี Sensor Logs จาก 2 วัน

## Day 1

```python
day1 = pd.DataFrame({
    "date": ["2026-01-01", "2026-01-01"],
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "power_kw": [1.2, 1.4]
})
```

## Day 2

```python
day2 = pd.DataFrame({
    "date": ["2026-01-02", "2026-01-02"],
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "power_kw": [1.5, 1.6]
})
```

## รวมข้อมูล

```python
result = pd.concat([day1, day2])

print(result)
```

---

## axis=0

ถึงแม้เราไม่ได้เขียน `axis=0` แต่ `pd.concat()` ใช้ `axis=0` เป็นค่าเริ่มต้น

```python
result = pd.concat([day1, day2], axis=0)
```

ความหมายคือ:

```text
ต่อแนวตั้ง
เพิ่ม row
```

เหมาะกับกรณี:
- รวมข้อมูลหลายวัน
- รวม CSV หลายไฟล์
- รวม sensor logs ที่มี column เหมือนกัน

---

# 5. ignore_index=True

เมื่อรวม DataFrame หลายไฟล์ index เดิมอาจซ้ำกัน เพราะแต่ละไฟล์มักเริ่มจาก 0 เหมือนกัน

```python
result = pd.concat([day1, day2])

print(result)
```

อาจได้ index แบบนี้:

```text
0
1
0
1
```

ถ้า index เดิมไม่ได้มีความหมายทางธุรกิจ ให้ใช้:

```python
result = pd.concat(
    [day1, day2],
    ignore_index=True
)

print(result)
```

Pandas จะสร้าง index ใหม่:

```text
0
1
2
3
```

## จุดสำคัญ

`ignore_index=True` ไม่ได้บอกว่าข้อมูลมาจากวันไหน

ข้อมูลวันควรถูกเก็บใน column จริง เช่น:

```text
date
timestamp
device_id
```

ดังนั้นในงาน Data Engineering เรามักใช้ `ignore_index=True` เพื่อให้ index สะอาด แต่ยังเก็บข้อมูลสำคัญไว้ใน column

---

# 6. รวมแบบแนวนอน axis=1

ตัวอย่างนี้สมมุติว่าเรามีข้อมูลจาก Sensor คนละชนิด แต่เป็นเวลาเดียวกันและเรียง row ตรงกัน

## Temperature Data

```python
temp_df = pd.DataFrame({
    "timestamp": ["08:00", "09:00"],
    "temperature_c": [28.5, 29.1]
})
```

## Humidity Data

```python
humidity_df = pd.DataFrame({
    "humidity_percent": [65, 66]
})
```

## รวมแนวนอน

```python
result = pd.concat(
    [temp_df, humidity_df],
    axis=1
)

print(result)
```

## axis=1

```text
ต่อแนวนอน
เพิ่ม column
```

## ข้อควรระวัง

ถ้า row ไม่ตรงกัน การใช้ `axis=1` อาจทำให้ข้อมูลผิดตำแหน่งได้

งานจริงควรมี key เช่น:

```text
timestamp
device_id
```

แล้วใช้ `merge()` ใน EP7 จะปลอดภัยกว่า

---

# 7. outer join

สมมุติว่าไฟล์จากคนละระบบมี column ไม่เหมือนกัน

## Power Log

```python
power_log = pd.DataFrame({
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "power_kw": [1.2, 1.4]
})
```

## Temperature Log

```python
temp_log = pd.DataFrame({
    "timestamp": ["10:00", "11:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "temperature_c": [30.1, 30.5]
})
```

## concat แบบ default

```python
result = pd.concat(
    [power_log, temp_log],
    ignore_index=True
)

print(result)
```

ค่า default คือ:

```python
join="outer"
```

ความหมายคือ:

```text
เอาทุก column มารวมกัน
column ไหนไม่มีข้อมูล ให้เป็น NaN
```

ผลลัพธ์จะมี column:

```text
timestamp
device_id
power_kw
temperature_c
```

## outer join ใช้เมื่อไหร่

ใช้เมื่อเราต้องการเก็บข้อมูลทุกอย่างไว้ก่อน แม้บาง column จะว่าง

เหมาะกับ:
- รวม log จากหลายระบบ
- รวมข้อมูลที่ schema ยังไม่เหมือนกัน
- exploratory data analysis
- data lake staging

---

# 8. inner join

ถ้าต้องการเอาเฉพาะ column ที่มีร่วมกันทุก DataFrame ให้ใช้:

```python
result = pd.concat(
    [power_log, temp_log],
    join="inner",
    ignore_index=True
)

print(result)
```

ผลลัพธ์จะเหลือเฉพาะ column ที่ทั้งสอง DataFrame มีเหมือนกัน เช่น:

```text
timestamp
device_id
```

## inner join ใช้เมื่อไหร่

ใช้เมื่อเราต้องการเฉพาะข้อมูลที่โครงสร้างตรงกันจริง ๆ

เหมาะกับ:
- ตรวจสอบ schema กลาง
- รวมเฉพาะ column ที่มั่นใจว่าใช้ร่วมกันได้
- ลด NaN จาก column ที่ไม่ตรงกัน

---

# 9. keys=

`keys=` ใช้สำหรับแปะป้ายชื่อแหล่งข้อมูลตอน concat

ตัวอย่าง: รวมข้อมูล 2 วัน แต่ยังอยากรู้ว่าแต่ละแถวมาจากวันไหน

```python
logs_with_keys = pd.concat(
    [day1, day2],
    keys=["2026-01-01", "2026-01-02"]
)

print(logs_with_keys)
```

ผลลัพธ์จะกลายเป็น MultiIndex

```text
2026-01-01  0
            1
2026-01-02  0
            1
```

## keys เรียนเพื่ออะไร

ใช้เพื่อจำแหล่งที่มาของข้อมูล เช่น:
- วันที่
- site
- ไฟล์ต้นทาง
- batch
- sensor group

ตัวอย่างรวมหลาย site:

```python
site_a = pd.DataFrame({
    "device_id": ["sensor_01", "sensor_02"],
    "power_kw": [1.2, 1.4]
})

site_b = pd.DataFrame({
    "device_id": ["sensor_03", "sensor_04"],
    "power_kw": [1.6, 1.8]
})

all_sites = pd.concat(
    [site_a, site_b],
    keys=["site_a", "site_b"]
)

print(all_sites)
```

`keys=` เหมือนการแปะป้ายว่า:

```text
ข้อมูลก้อนนี้มาจาก source ไหน
```

---

# 10. verify_integrity=True

`verify_integrity=True` ใช้ตรวจสอบว่า index หลัง concat ห้ามซ้ำ

เหมาะกับกรณีที่ index เป็นข้อมูลที่ควร unique จริง ๆ เช่น:
- device_id
- asset_id
- meter_id
- invoice_id
- transaction_id

## ตัวอย่างที่สมเหตุสมผล: Device Registry

สมมุติว่าเรามี device registry จาก 2 site

## Registry จาก Factory A

```python
factory_a_devices = pd.DataFrame({
    "site": ["factory_a", "factory_a"],
    "device_type": ["temperature", "power_meter"]
}, index=["sensor_01", "meter_01"])
```

## Registry จาก Factory B

```python
factory_b_devices = pd.DataFrame({
    "site": ["factory_b", "factory_b"],
    "device_type": ["temperature", "power_meter"]
}, index=["sensor_02", "meter_01"])
```

ในที่นี้ index คือ device_id

```text
meter_01 ซ้ำ
```

ถ้า device_id ควร unique ทั้งระบบ การซ้ำแบบนี้คือปัญหา

## ตรวจสอบด้วย verify_integrity

```python
pd.concat(
    [factory_a_devices, factory_b_devices],
    verify_integrity=True
)
```

Pandas จะ error เพราะ index ซ้ำ

## ทำไมต้องเรียน verify_integrity

เพราะบางครั้ง index ซ้ำไม่ควรถูกปล่อยผ่าน

เช่น:

```text
meter_01 อยู่ทั้ง factory_a และ factory_b
```

เราต้องถามต่อว่า:
- เป็น meter ตัวเดียวกันจริงหรือไม่
- ตั้งชื่อซ้ำโดยบังเอิญหรือไม่
- ต้องเพิ่ม site เข้าไปใน key หรือไม่
- ควรใช้ MultiIndex เช่น site + device_id หรือไม่

## วิธีแก้ที่ดีกว่าในกรณี device_id ซ้ำข้าม site

ถ้า device_id ซ้ำได้ในแต่ละ site ให้ใช้ MultiIndex แทน

```python
factory_a_devices = factory_a_devices.reset_index().rename(columns={"index": "device_id"})
factory_b_devices = factory_b_devices.reset_index().rename(columns={"index": "device_id"})

all_devices = pd.concat(
    [factory_a_devices, factory_b_devices],
    ignore_index=True
)

all_devices = all_devices.set_index(["site", "device_id"])

print(all_devices)
```

ตอนนี้ key จะเป็น:

```text
site + device_id
```

ซึ่งสมเหตุสมผลกว่า

---

# 11. append() ถูกลบออกแล้ว

ใน Pandas รุ่นเก่าเคยใช้:

```python
df1.append(df2)
```

แต่ใน Pandas รุ่นใหม่ `append()` ถูกลบออกแล้ว

ให้ใช้:

```python
result = pd.concat([df1, df2])
```

แทนทั้งหมด

## ทำไม append() ถูกลบ

เพราะ `append()` ข้างในก็ใช้แนวคิดเดียวกับ `concat()` และทำให้หลายคนเข้าใจผิดว่าเหมือน `list.append()`

แต่จริง ๆ แล้ว Pandas ไม่ได้แก้ DataFrame เดิม

มันสร้าง DataFrame ใหม่

## วิธีที่ถูกต้องในปัจจุบัน

```python
result = pd.concat(
    [day1, day2],
    ignore_index=True
)

print(result)
```

## ถ้าต้อง concat หลายรอบใน loop

ไม่ควร concat ทีละรอบแบบนี้:

```python
result = pd.DataFrame()

for frame in [day1, day2]:
    result = pd.concat([result, frame])
```

เพราะจะ copy ข้อมูลใหม่ซ้ำหลายรอบ

ควรเก็บไว้ใน list แล้ว concat ครั้งเดียว:

```python
frames = [day1, day2]

result = pd.concat(
    frames,
    ignore_index=True
)

print(result)
```

---

# 12. Mini Lab — รวม Sensor Logs หลายวัน

```python
day1 = pd.DataFrame({
    "date": ["2026-01-01", "2026-01-01"],
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "power_kw": [1.2, 1.4]
})

day2 = pd.DataFrame({
    "date": ["2026-01-02", "2026-01-02"],
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_01"],
    "power_kw": [1.5, 1.6]
})

sensor_logs = pd.concat(
    [day1, day2],
    ignore_index=True
)

print(sensor_logs)
```

---

# 13. Mini Lab — รวมหลาย Site พร้อม keys

```python
site_a_logs = pd.DataFrame({
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_01", "sensor_02"],
    "temperature_c": [28.5, 29.1]
})

site_b_logs = pd.DataFrame({
    "timestamp": ["08:00", "09:00"],
    "device_id": ["sensor_03", "sensor_04"],
    "temperature_c": [30.2, 30.8]
})

site_logs = pd.concat(
    [site_a_logs, site_b_logs],
    keys=["site_a", "site_b"]
)

print(site_logs)
```

---

# 14. สิ่งที่ควรเข้าใจหลังเรียนจบ

หลังจาก EP นี้ คุณควรเข้าใจ:

1. `pd.concat()` ใช้รวมข้อมูลหลายชุด
2. `axis=0` คือการต่อแนวตั้ง เพิ่ม row
3. `axis=1` คือการต่อแนวนอน เพิ่ม column
4. `ignore_index=True` ใช้เมื่อ index เดิมไม่มีความหมายและต้องการสร้างใหม่
5. `join="outer"` เก็บทุก column และเติม NaN ในส่วนที่ไม่มีข้อมูล
6. `join="inner"` เอาเฉพาะ column ที่มีร่วมกัน
7. `keys=` ใช้แปะ label ให้ source และสร้าง MultiIndex
8. `verify_integrity=True` ใช้จับ index ซ้ำที่ไม่ควรเกิดขึ้น
9. `append()` ถูกลบออกแล้ว ควรใช้ `pd.concat()` แทน
10. ถ้ารวมหลายรอบ ให้เก็บ DataFrame ใน list แล้ว concat ครั้งเดียว

---

# 15. คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---|---|
| concat | รวมข้อมูลหลายชุด |
| axis=0 | ต่อแนวตั้ง เพิ่ม row |
| axis=1 | ต่อแนวนอน เพิ่ม column |
| ignore_index | ไม่ใช้ index เดิม และสร้าง index ใหม่ |
| outer join | รวมทุก column |
| inner join | เอาเฉพาะ column ที่เหมือนกัน |
| keys | แปะ label ให้แหล่งข้อมูล |
| MultiIndex | Index หลายระดับ |
| verify_integrity | ตรวจสอบ index ซ้ำ |
| append | วิธีเก่าที่ถูกลบแล้ว |

---

# 16. ลำดับการสอนแนะนำ

1. อธิบายว่าทำไมข้อมูลจริงมาจากหลายไฟล์
2. รวมข้อมูลหลายวันด้วย `concat()`
3. อธิบาย `axis=0`
4. อธิบาย `ignore_index=True`
5. รวมข้อมูลแนวนอนด้วย `axis=1`
6. อธิบายข้อควรระวังของ `axis=1`
7. อธิบาย `outer join`
8. อธิบาย `inner join`
9. สอน `keys=`
10. สอน `verify_integrity=True` ด้วย Device Registry
11. อธิบายว่า `append()` ถูกลบแล้ว
12. ทำ Mini Lab

---

# 17. การบ้าน

สร้างข้อมูล 3 วัน:

- day1
- day2
- day3

โดยมี column:
- date
- timestamp
- device_id
- voltage_v

จากนั้นให้ทำ:

1. concat ทั้ง 3 วัน
2. ใช้ `ignore_index=True`
3. ทดลองใช้ `keys=` เป็นวันที่
4. สร้าง device registry 2 ชุด แล้วทดลอง `verify_integrity=True`
5. อธิบายว่าเมื่อไหร่ควรใช้ `ignore_index` และเมื่อไหร่ควรใช้ `keys`

---

# 18. ตอนถัดไป

EP7 — Combining Datasets: Merge and Join

เราจะเรียนรู้:
- `pd.merge()`
- left join
- right join
- inner join
- outer join
- database-style join
- การเชื่อม sensor logs กับ device metadata
