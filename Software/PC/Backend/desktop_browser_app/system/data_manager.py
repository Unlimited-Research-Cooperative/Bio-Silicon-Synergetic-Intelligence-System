"""
The DataManager class is a data transmitter and receiver
Usage:
The files which need data to SEND & READ data simultaneously
"""
import time
from threading import Thread
from paho.mqtt.client import Client
from typing import Any


class DataManager:
    def __init__(self, client_id: str, topic_sub: str | None, topic_pub: str | None, processing_func: Any = None):
        super().__init__()

        self.host = "127.0.0.1"  # localhost
        self.port = 3000

        self.client = Client(client_id)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.client.connect(self.host, self.port)

        if topic_sub is None:
            pass
        else:
            self.client.subscribe(topic_sub)

        self.helper_func = processing_func
        self.topic_pub = topic_pub
        self.topic_sub = topic_sub

    def server_loop(self):
        self.client.loop_forever()

    def listen(self):
        if self.topic_sub is None:
            raise Exception("Instance cannot subscribe to topic. Set topic_sub parameter to subscribe")
        else:
            thread = Thread(target=self.server_loop)
            thread.start()

    def publish(self, timeout: int, data: Any, sleep_time: float):
        if self.topic_pub is None:
            raise Exception("Instance cannot publish data. Provide topic_pub parameter.")
        thread = Thread(target=self.publish_data, args=[timeout, data, sleep_time])
        thread.start()

    def publish_data(self, timeout: int, data: Any, sleep_time: float = 0):
        c_time = 0
        while c_time != timeout:
            if data is None:
                self.client.publish(topic=self.topic_pub, payload="NaN")
            elif data is not None:
                self.client.publish(topic=self.topic_pub, payload=data)
            c_time += 1
            time.sleep(sleep_time)

    # Callbacks
    def on_connect(self, client, userdata, flags, rc):
        print("connected to host")

    def on_message(self, client, userdata, message):
        self.helper_func(message.payload.decode("utf-8"))

    def on_disconnect(self, client, userdata, flags, rc):
        print(f"{client.client_id} disconnected from {self.host}")
