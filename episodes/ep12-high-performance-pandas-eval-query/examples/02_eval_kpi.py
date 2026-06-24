import pandas as pd

factory = pd.DataFrame({
    "machine_id": ["M01", "M02", "M03", "M04", "M05"],
    "temperature_c": [32.5, 28.2, 35.1, 30.8, 33.9],
    "vibration_mm_s": [1.2, 0.8, 2.5, 1.0, 1.8],
    "power_kw": [12.5, 8.2, 15.4, 10.1, 13.2],
})

factory.eval("risk_score = temperature_c * vibration_mm_s / power_kw", inplace=True)

print(factory)
