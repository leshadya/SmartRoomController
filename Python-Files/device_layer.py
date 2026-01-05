import random
from dataclasses import dataclass


@dataclass
class SensorState:
    temperature: float = 23.0
    co2: float = 500.0
    humidity: float = 45.0
    smoke: int = 0


@dataclass
class ActuatorState:
    fan: bool = False
    window: bool = False
    fire_alarm: bool = False


class EnvironmentModel:

    def __init__(self, sensors: SensorState, actuators: ActuatorState):
        self.sensors = sensors
        self.actuators = actuators

    def update(self, state: str):
        if state == "normal":
            heat = 0.02
            co2_gen = random.uniform(1, 3)
            humidity_gen = random.uniform(-0.05, 0.05)
            self.sensors.smoke = 0

        elif state == "fire":
            heat = 1.3
            co2_gen = 25
            humidity_gen = 0.3
            self.sensors.smoke = 1

        elif state == "recovery":
            heat = -0.4
            co2_gen = -20
            humidity_gen = -0.4
            self.sensors.smoke = 0

        ventilation = 0.0
        humidity_vent = 0.0

        if self.actuators.fan:
            ventilation += 1.0
            humidity_vent += 0.6
        if self.actuators.window:
            ventilation += 0.4
            humidity_vent += 0.3

        self.sensors.temperature += heat - ventilation + random.gauss(0, 0.05)
        self.sensors.co2 += co2_gen - ventilation * 30 + random.gauss(0, 5)
        self.sensors.humidity += humidity_gen - humidity_vent + random.gauss(0, 0.1)

        self.sensors.temperature = max(15, self.sensors.temperature)
        self.sensors.co2 = max(350, self.sensors.co2)
        self.sensors.humidity = max(20, min(80, self.sensors.humidity))
