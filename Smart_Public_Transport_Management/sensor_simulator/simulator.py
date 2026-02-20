import firebase_admin
from firebase_admin import credentials, firestore
import random
import time
from datetime import datetime

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
buses = [
    {"bus_id": "bus_01", "passenger_count": 0},
    {"bus_id": "bus_02", "passenger_count": 0},
    {"bus_id": "bus_03", "passenger_count": 0}
]

def generate_sensor_event():
    bus = random.choice(buses)

    entry = 1 if random.random() > 0.5 else 0
    exit = 0 if entry == 1 else 1

    current_count = bus.get("passenger_count", 0)
    new_count = current_count + (1 if entry else -1)
    bus["passenger_count"] = max(0, new_count)

    weight_change = (50 + random.random()*30) if entry else -(50 + random.random()*30)
    timestamp = datetime.now().isoformat()
    event = {
        "bus_id": bus["bus_id"],
        "entry": entry,
        "exit": exit,
        "passenger_count": bus["passenger_count"],
        "weight_change": weight_change,
        "timestamp": timestamp
    }
    return event

while True:
    event = generate_sensor_event()
    try:
        db.collection("sensor_events").add(event)
        print("Sent to Firebase:", event)
    except Exception as e:
        print("Error sending to Firebase:", e)
    time.sleep(2)
