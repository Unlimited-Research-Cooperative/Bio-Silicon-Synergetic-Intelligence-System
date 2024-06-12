import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

def create_mqtt_client(client_id):
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)  # Assuming Mosquitto is running locally
    client.loop_start()
    
    return client
