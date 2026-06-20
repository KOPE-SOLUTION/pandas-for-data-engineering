# EP9 — Pivot Table

## เป้าหมายของตอนนี้

หลังจากเรียน `GroupBy` ไปแล้ว ตอนนี้เราจะเรียนรู้ `Pivot Table`

แนวคิดสำคัญคือ:

```text
GroupBy = สรุปข้อมูลแบบกลุ่ม
Pivot Table = สรุปข้อมูลเป็นตาราง 2 มิติ อ่านง่ายกว่า
```

Pivot Table ถูกใช้บ่อยในงานจริง เช่น:
- Data Analysis
- Data Engineering
- Business Intelligence (BI)
- Dashboard
- IoT Monitoring
- Energy Monitoring
- Solar / Factory / Building Analytics

> หมายเหตุสำคัญ: ตัวอย่างใน EP นี้จะหลีกเลี่ยงการเอาค่าคนละหน่วย เช่น kW กับ °C มาเฉลี่ยรวมกัน เพราะในโลกจริงไม่สมเหตุสมผล

---

# 1. Import Library

```python
import pandas as pd
import numpy as np
```

---

# 2. Pivot Table คืออะไร

Pivot Table คือการสรุปข้อมูลให้อยู่ในรูปตาราง โดยกำหนดว่า:

- `values` = ค่าที่ต้องการคำนวณ
- `index` = ให้ข้อมูลเรียงเป็นแถวตามอะไร
- `columns` = ให้ข้อมูลแตกเป็นคอลัมน์ตามอะไร
- `aggfunc` = ใช้ฟังก์ชันอะไรในการสรุป เช่น mean, sum, count

โครงสร้างจำง่าย:

```python
pd.pivot_table(
    data,
    values="ค่าที่จะคำนวณ",
    index="แถว",
    columns="คอลัมน์",
    aggfunc="วิธีสรุป"
)
```

---

# 3. ตัวอย่างที่ 1 — Temperature Monitoring

ตัวอย่างนี้ใช้หน่วยเดียวกันทั้งหมด คือ °C

```python
temperature_logs = pd.DataFrame({
    "site": [
        "site_a", "site_a",
        "site_b", "site_b",
        "site_c", "site_c"
    ],
    "device_id": [
        "temp_01", "temp_02",
        "temp_03", "temp_04",
        "temp_05", "temp_06"
    ],
    "temperature_c": [
        28.5, 29.1,
        30.2, 30.8,
        27.9, 28.3
    ]
})

print(temperature_logs)
```

---

# 4. Pivot Table พื้นฐาน

หาค่าเฉลี่ยอุณหภูมิของแต่ละ Site

```python
result = pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc="mean"
)

print(result)
```

ผลลัพธ์ที่ควรได้:

```text
        temperature_c
site
site_a          28.8
site_b          30.5
site_c          28.1
```

คำนวณจาก:

```text
site_a = (28.5 + 29.1) / 2 = 28.8
site_b = (30.2 + 30.8) / 2 = 30.5
site_c = (27.9 + 28.3) / 2 = 28.1
```

---

# 5. เปรียบเทียบกับ GroupBy

## GroupBy

```python
temperature_logs.groupby("site")["temperature_c"].mean()
```

## Pivot Table

```python
pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc="mean"
)
```

ทั้งสองแบบได้แนวคิดเดียวกัน แต่ Pivot Table เหมาะเมื่ออยากสร้างตารางสรุปที่อ่านง่ายขึ้น

---

# 6. ตัวอย่างที่ 2 — Energy Monitoring รายเดือน

ตัวอย่างนี้ใช้หน่วยเดียวกันทั้งหมด คือ kWh

```python
energy_logs = pd.DataFrame({
    "building": [
        "A", "A", "A",
        "B", "B", "B"
    ],
    "month": [
        "Jan", "Feb", "Mar",
        "Jan", "Feb", "Mar"
    ],
    "energy_kwh": [
        1200, 1300, 1400,
        1500, 1450, 1600
    ]
})

print(energy_logs)
```

---

# 7. Pivot Table แบบมี index และ columns

สรุปพลังงานรายอาคาร แยกตามเดือน

```python
result = pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum"
)

print(result)
```

ผลลัพธ์:

```text
month      Feb   Jan   Mar
building
A         1300  1200  1400
B         1450  1500  1600
```

---

# 8. จัดลำดับเดือนให้อ่านง่าย

บางครั้ง Pivot Table จะเรียง column ตามตัวอักษร เช่น Feb, Jan, Mar

ถ้าต้องการเรียง Jan, Feb, Mar ให้ใช้:

```python
result = result[["Jan", "Feb", "Mar"]]

print(result)
```

---

# 9. aggfunc คืออะไร

`aggfunc` คือวิธีสรุปข้อมูล

| aggfunc | ความหมาย |
|---|---|
| mean | ค่าเฉลี่ย |
| sum | ผลรวม |
| count | จำนวนข้อมูล |
| min | ค่าต่ำสุด |
| max | ค่าสูงสุด |

ค่าเริ่มต้นของ `pivot_table()` คือ:

```python
aggfunc="mean"
```

---

# 10. ใช้ sum

```python
pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    aggfunc="sum"
)
```

ใช้เมื่อค่ามีความหมายแบบรวมได้ เช่น:

- energy_kwh
- production_count
- alarm_count
- runtime_hours

---

# 11. ใช้ mean

```python
pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc="mean"
)
```

ใช้เมื่ออยากดูค่าเฉลี่ย เช่น:

- temperature_c
- humidity_percent
- power_kw เฉลี่ย
- vibration เฉลี่ย

---

# 12. ใช้ count

```python
pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc="count"
)
```

ใช้ตรวจสอบจำนวนข้อมูลต่อกลุ่ม

---

# 13. หลาย Aggregation พร้อมกัน

```python
pd.pivot_table(
    temperature_logs,
    values="temperature_c",
    index="site",
    aggfunc=[
        "mean",
        "min",
        "max",
        "count"
    ]
)
```

เหมาะสำหรับทำ Summary Report

---

# 14. margins=True

`margins=True` ใช้เพิ่มแถวหรือคอลัมน์รวมทั้งหมด

```python
pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum",
    margins=True
)
```

ผลลัพธ์จะมี `All`

ใช้ในรายงานเพื่อดูผลรวมทั้งหมด

---

# 15. margins_name

ตั้งชื่อแถวรวมเองได้

```python
pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum",
    margins=True,
    margins_name="Total"
)
```

---

# 16. fill_value

ถ้าบางอาคารไม่มีข้อมูลบางเดือน จะเกิด `NaN`

```python
energy_missing = pd.DataFrame({
    "building": [
        "A", "A",
        "B", "B"
    ],
    "month": [
        "Jan", "Feb",
        "Jan", "Mar"
    ],
    "energy_kwh": [
        1200, 1300,
        1500, 1600
    ]
})

result = pd.pivot_table(
    energy_missing,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum"
)

print(result)
```

แทน NaN ด้วย 0:

```python
result = pd.pivot_table(
    energy_missing,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum",
    fill_value=0
)

print(result)
```

---

# 17. ตัวอย่างที่ 3 — Alarm Summary

```python
alarm_logs = pd.DataFrame({
    "site": [
        "site_a", "site_a", "site_a",
        "site_b", "site_b",
        "site_c"
    ],
    "alarm_type": [
        "Offline",
        "Over Temp",
        "Offline",
        "Low Power",
        "Offline",
        "Over Temp"
    ],
    "alarm_count": [
        1, 1, 1,
        1, 1,
        1
    ]
})

print(alarm_logs)
```

Pivot Alarm Count:

```python
alarm_summary = pd.pivot_table(
    alarm_logs,
    values="alarm_count",
    index="site",
    columns="alarm_type",
    aggfunc="sum",
    fill_value=0
)

print(alarm_summary)
```

ผลลัพธ์จะเป็นตารางจำนวน Alarm ตาม Site และ Alarm Type

---

# 18. ใช้ Pivot Table เพื่อเตรียม Dashboard

Pivot Table เหมาะมากกับการทำตารางก่อนส่งต่อไป:

- Excel
- CSV
- Grafana
- Power BI
- Web Dashboard
- Machine Learning Feature Table

```python
dashboard_table = pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum",
    fill_value=0
)

print(dashboard_table)
```

---

# 19. Pivot Table กับข้อมูลคนละหน่วย

หลีกเลี่ยงการเอาค่าคนละหน่วยมารวมกันใน column เดียว เช่น:

```text
120 kWh
28.5 °C
```

แล้วนำไปหาค่าเฉลี่ยรวมกัน

เพราะผลลัพธ์ไม่มีความหมายทางวิศวกรรม

วิธีที่เหมาะสมคือ:

1. แยก column ตามชนิดข้อมูล เช่น `temperature_c`, `energy_kwh`
2. หรือใช้ `columns="device_type"` เพื่อแยกประเภทก่อน
3. หรือแยก DataFrame ก่อนวิเคราะห์

---

# 20. Mini Lab — Realistic Energy Pivot

สร้างข้อมูลพลังงาน 2 อาคาร 3 เดือน

```python
energy_logs = pd.DataFrame({
    "building": [
        "A", "A", "A",
        "B", "B", "B"
    ],
    "month": [
        "Jan", "Feb", "Mar",
        "Jan", "Feb", "Mar"
    ],
    "energy_kwh": [
        1200, 1300, 1400,
        1500, 1450, 1600
    ]
})
```

ทำ Pivot Table:

```python
energy_pivot = pd.pivot_table(
    energy_logs,
    values="energy_kwh",
    index="building",
    columns="month",
    aggfunc="sum",
    margins=True,
    fill_value=0
)

energy_pivot = energy_pivot[["Jan", "Feb", "Mar", "All"]]

print(energy_pivot)
```

---

# 21. สิ่งที่ควรเข้าใจหลังเรียนจบ

1. `pivot_table()` คืออะไร
2. `values` คือค่าที่นำไปคำนวณ
3. `index` คือแถวของตารางสรุป
4. `columns` คือคอลัมน์ของตารางสรุป
5. `aggfunc` คือวิธีสรุปข้อมูล
6. `fill_value` ใช้แทนค่า NaN
7. `margins=True` ใช้เพิ่ม Total
8. Pivot Table ช่วยจัดผลลัพธ์ให้อ่านง่ายกว่า GroupBy
9. ควรระวังการรวมข้อมูลคนละหน่วย
10. Pivot Table เหมาะมากกับงาน Dashboard และ Reporting

---

# 22. คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---|---|
| Pivot Table | ตารางสรุปข้อมูลหลายมิติ |
| values | ค่าที่ต้องการคำนวณ |
| index | แถวของตารางสรุป |
| columns | คอลัมน์ของตารางสรุป |
| aggfunc | วิธีสรุปข้อมูล |
| margins | เพิ่มแถวหรือคอลัมน์รวม |
| fill_value | แทนค่า NaN |
| mean | ค่าเฉลี่ย |
| sum | ผลรวม |
| count | จำนวนข้อมูล |



---

# การบ้าน

ให้สร้าง DataFrame ชื่อ `power_logs` โดยมี column:
- building
- floor
- month
- energy_kwh

<br>

จากนั้นให้ทำ:
1. Pivot Table สรุป `energy_kwh` ตาม building และ month
2. ใช้ `aggfunc="sum"`
3. ใช้ `fill_value=0`
4. ใช้ `margins=True`
5. ทดลองเปลี่ยน `index` เป็น `floor`

---

# ตอนถัดไป

EP10 — Working with Time Series

เราจะเรียนรู้:
- Datetime
- DateTimeIndex
- Resampling
- Rolling Window
- Shift
- Time-based Sensor Data
