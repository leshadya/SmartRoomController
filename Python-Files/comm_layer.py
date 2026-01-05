import json
import threading
import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self, broker, port):
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.client.connect(broker, port, 60)
        threading.Thread(target=self.client.loop_forever, daemon=True).start()

    def publish(self, topic_to_send, payload: dict):
        self.client.publish(topic_to_send, json.dumps(payload))

    def listen(self, topic_to_listen, callback):
        self.client.subscribe(topic_to_listen)
        self.client.on_message = lambda c, u, m: callback(m.payload.decode())
