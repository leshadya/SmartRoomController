import subprocess
import time
from data_layer import store_data
from device_layer import SensorState, ActuatorState, EnvironmentModel
from control_layer import RoomController
from comm_layer import MQTTClient

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC_TO_PUBLISH = "2025_proje_x9z/house/data"
TOPIC_TO_SUBSCRIBE = "2025_proje_x9z/house/status"

sensors = SensorState()
actuators = ActuatorState()

env = EnvironmentModel(sensors, actuators)
controller = RoomController()

data = {
    "fan_on": False,
    "window_on": False,
    "alarm_on": False,
}

def on_unity_message(msg):
    print(f"[UNITY EVENT] {msg}")

    if msg == "fan_on":
        actuators.fan = True
        data["fan_on"] = True
    elif msg == "fan_off":
        actuators.fan = False
        data["fan_on"] = False

    elif msg == "window_open":
        actuators.window = True
        data["window_on"] = True
    elif msg == "window_close":
        actuators.window = False
        data["window_on"] = False

    elif msg == "alarm_on":
        actuators.fire_alarm = True
        data["alarm_on"] = True


mqtt_client = MQTTClient(BROKER, PORT)
subprocess.Popen(["streamlit", "run", "dashboard.py"])

mqtt_client.listen(TOPIC_TO_SUBSCRIBE, on_unity_message)

while True:

    state = controller.step(sensors)
    env.update(state)

    if state == "recovery":
        if data["alarm_on"]:
            actuators.fire_alarm = False
            data["alarm_on"] = False
            sensors.smoke = 0

    payload = {
        "temperature": round(sensors.temperature, 2),
        "co2": round(sensors.co2, 2),
        "humidity": round(sensors.humidity, 1),
        "smoke": sensors.smoke
    }

    mqtt_client.publish(TOPIC_TO_PUBLISH, payload)

    final_data = {**payload, **data}
    print(final_data)
    store_data(final_data)

    time.sleep(1)