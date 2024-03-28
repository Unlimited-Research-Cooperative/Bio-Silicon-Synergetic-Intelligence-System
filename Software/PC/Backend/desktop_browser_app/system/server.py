"""
The Server class is a subscriber which listens for incoming signals
Usage:
The files which need data to READ from a topic
"""
from threading import Thread
from paho.mqtt.client import Client


class Server:
    def __init__(self, client_id: str, topic: str, processing_func):
        super().__init__()

        self.host = "127.0.0.1"  # localhost
        self.port = 3000

        self.client = Client(client_id)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        self.client.connect(self.host, self.port)

        self.client.subscribe(topic)

        self.helper_func = processing_func

    def server_loop(self):
        self.client.loop_forever()

    def run_server(self):
        thread = Thread(target=self.server_loop)
        thread.start()

    # Callbacks
    def on_connect(self, client, userdata, flags, rc):
        print("connected to host")

    def on_message(self, client, userdata, message):
        self.helper_func(message.payload)

    def on_disconnect(self, client, userdata, flags, rc):
        print(f"{client.client_id} disconnected from {self.host}")

