#iot_simlator.py -Valencia Walker's

import random
import time
from datetime import datetime



def simulate_temperature():
    temp = round(random.uniform(22.0, 30.0), 2)
    return {
        "sensor": "arduino_temp",
        "timestamp": datetime.utcnow().isoformat(),
        "value": temp,
        "unit": "C"
    }




def stream_sensor_data():
    while True:
        temp = round(random.uniform(20, 35), 2)
        print(f"Temperature: {temp}°C")
        time.sleep(1)
