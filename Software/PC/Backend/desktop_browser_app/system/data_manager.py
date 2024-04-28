"""
The DataManager class is a data transmitter and receiver
Usage:
The files which need data to SEND & READ data simultaneously
"""
import time
from os import getenv, path
from threading import Thread
from dotenv import load_dotenv
from paho.mqtt import MQTTException
from paho.mqtt.client import Client
from typing import Any


class DataManager:
    def __init__(self, client_id: str, config_file_path: str, topic_sub: str | None, topic_pub: str | None,
                 processing_func: Any = None, close_after_first_list: bool = False):
        super().__init__()

        if topic_pub == None and topic_sub == None:
            raise Exception("Must provide either topic_sub or topic_pub")

        if not path.exists(config_file_path):
            raise FileExistsError("Config file does not exists.")
        else:
            load_dotenv(config_file_path)

        self.host = getenv("host")
        self.port = int(getenv("port"))

        self.client = Client(client_id)
        self.close_after_first_list = close_after_first_list

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.data = None

        try:
            self.client.connect(self.host, self.port)

        except MQTTException:
            raise MQTTException

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

    def set_data(self, data: Any):
        self.data = data

    def get_data(self):
        return self.data

    def publish(self, sleep_time: float):
        if self.topic_pub is None:
            raise Exception("Instance cannot publish data. Provide topic_pub parameter.")
        thread = Thread(target=self.publish_data, args=[sleep_time])
        thread.start()

    def publish_data(self, sleep_time: float = 0):
        data = self.get_data()
        if data is None:
            self.client.publish(topic=self.topic_pub, payload="NaN")
        elif data is not None:
            self.client.publish(topic=self.topic_pub, payload=data)
        time.sleep(sleep_time)

    # Callbacks
    def on_connect(self, client, userdata, flags, rc):
        print("connected to host")

    def on_message(self, client, userdata, message):
        self.helper_func(message.payload.decode("utf-8"))
        if self.close_after_first_list:
            self.client.unsubscribe(self.topic_sub)
        else:
            pass

    def on_disconnect(self, client, userdata, flags, rc):
        raise Exception("Disconnected from host")
