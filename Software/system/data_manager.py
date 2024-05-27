"""
The DataManager class is a data transmitter and receiver
Usage:
The files which need data to SEND & READ data simultaneously
"""

# Import dependencies
from os import path
from time import sleep
from typing import Any
from threading import Thread
from paho.mqtt import MQTTException
from paho.mqtt.client import Client
from configparser import ConfigParser


class DataManager:
    def __init__(self, profile: str, func: Any = None):
        super().__init__()

        # Default variables
        self.host = "127.0.0.1"
        self.port = 8000
        self.topic_sub = None
        self.topic_pub = None
        self.client = None
        self.func = func

        self.data = None

        # Check path existence
        if path.exists(profile):
            config_obj = ConfigParser()
            config_obj.read(profile)
            self.host = config_obj['General']['host']
            self.port = int(config_obj['General']['port'])
            self.client = Client(config_obj["General"]['client_id'])

            if config_obj["General"]['topic_sub'] == None:
                self.topic_sub = None

            else:
                self.topic_sub = config_obj["General"]['topic_sub']

            if config_obj['General']['topic_pub'] == None:
                self.topic_pub = None
            else:
                self.topic_pub = config_obj["General"]['topic_pub']

            print(self.host, self.port)

        else:
            raise FileNotFoundError("Profile not found.")
        

        # Connect to broker
        try:
            self.client.connect(self.host, self.port)

        except MQTTException:
            raise MQTTException

        if self.topic_sub is None:
            pass
        else:
            self.client.subscribe(self.topic_sub)
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def stop_loop(self):
        self.client.loop_stop()
        
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
        sleep(sleep_time)

    def server_loop(self):
        self.client.loop_forever()

    # Callbacks
    def on_connect(self, client, userdata, flags, rc):
        print("connected to host")

    def on_message(self, client, userdata, message):
        if self.func == None:
            pass
        else:
            self.func(message.payload.decode("utf-8"))

    def on_disconnect(self, client, userdata, flags, rc):
        raise Exception("Disconnected from host")

