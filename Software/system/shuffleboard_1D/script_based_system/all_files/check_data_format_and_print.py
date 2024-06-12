import paho.mqtt.client as mqtt
import json

# MQTT configuration
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "neural_data"

# Callback function when a message is received
def on_message(client, userdata, message):
    try:
        # Decode the message payload
        payload = message.payload.decode('utf-8')
        
        # Try to parse the JSON data
        try:
            neural_data = json.loads(payload)
            print("Received JSON neural data:")
            print(json.dumps(neural_data, indent=4))  # Pretty print JSON data
        except json.JSONDecodeError:
            print("Received raw neural data:")
            print(payload)
    except Exception as e:
        print(f"Error processing message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the neural data topic
client.subscribe(MQTT_TOPIC)

# Start the MQTT client loop
print(f"Listening for messages on topic '{MQTT_TOPIC}'...")
client.loop_forever()
