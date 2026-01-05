import random
from enum import Enum

class RoomState(Enum):
    NORMAL = "normal"
    FIRE = "fire"
    RECOVERY = "recovery"


class RoomController:

    def __init__(self):
        self.state = RoomState.NORMAL
        self.time = 0

        self.fire_timer = 0
        self.fire_triggered = False
        self.fire_time = random.randint(30, 40)

        print(f"[CONTROL] Fire scheduled at t={self.fire_time}s")

    def step(self, sensors):
        if not self.fire_triggered and self.time >= self.fire_time:
            self.state = RoomState.FIRE
            self.fire_triggered = True
            self.fire_timer = 0
            print("[CONTROL] Fire started")

        if self.state == RoomState.FIRE:
            self.fire_timer += 1
            if self.fire_timer >= 20:
                self.state = RoomState.RECOVERY
                print("[CONTROL] Fire extinguished")

        elif self.state == RoomState.RECOVERY:
            if sensors.temperature < 26 and sensors.co2 < 450:
                self.state = RoomState.NORMAL
                print("[CONTROL] Back to normal")

        self.time += 1
        return self.state.value
