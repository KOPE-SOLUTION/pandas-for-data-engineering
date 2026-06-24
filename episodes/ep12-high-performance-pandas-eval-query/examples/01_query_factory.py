import pandas as pd

factory = pd.DataFrame({
    "machine_id": ["M01", "M02", "M03", "M04", "M05"],
    "line": ["line_1", "line_1", "line_2", "line_2", "line_3"],
    "temperature_c": [32.5, 28.2, 35.1, 30.8, 33.9],
    "vibration_mm_s": [1.2, 0.8, 2.5, 1.0, 1.8],
    "power_kw": [12.5, 8.2, 15.4, 10.1, 13.2],
    "status": ["running", "idle", "running", "running", "alarm"]
})

result = factory.query("temperature_c > 30 and power_kw > 10")

print(result)
