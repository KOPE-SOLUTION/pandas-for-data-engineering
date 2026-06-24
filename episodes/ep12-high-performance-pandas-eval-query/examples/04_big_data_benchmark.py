import pandas as pd
import numpy as np
import time

n = 1_000_000

big_df = pd.DataFrame({
    "temperature_c": np.random.uniform(20, 40, n),
    "power_kw": np.random.uniform(5, 20, n),
    "vibration_mm_s": np.random.uniform(0.5, 4.0, n)
})

start = time.time()
result = big_df.query("temperature_c > 30 and power_kw > 10 and vibration_mm_s < 2.5")
end = time.time()

print(result.head())
print(result.shape)
print("query time:", end - start)
print("memory bytes:", big_df.memory_usage(deep=True).sum())
