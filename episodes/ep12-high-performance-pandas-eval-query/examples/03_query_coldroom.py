import pandas as pd

coldroom = pd.DataFrame({
    "room_id": ["room_a", "room_a", "room_b", "room_b"],
    "temperature_c": [4.1, 8.5, 3.8, 9.2],
    "door_open": [False, True, False, True],
    "compressor_running": [True, True, True, False]
})

abnormal = coldroom.query("temperature_c > 8 and door_open == True")

print(abnormal)
