import paho.mqtt.client as mqtt
import json
import time
import numpy as np
from scipy.signal import resample

# Constants
BUFFER_SIZE = 500  # Target buffer size for 500 Hz resolution
TARGET_SAMPLING_RATE = 500  # Target sampling rate
UPDATE_RATE = 25  # Update rate in Hz
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_INPUT_TOPIC = "neural_data"
MQTT_OUTPUT_TOPIC = "processed_neural_data"

# Global buffer to hold data
data_buffer = []

def downsample(data, original_rate, target_rate):
    num_samples = int(len(data) * target_rate / original_rate)
    return resample(data, num_samples)

def process_and_send_data(client):
    global data_buffer
    if len(data_buffer) >= BUFFER_SIZE:
        # Process the data in the buffer
        data_block = data_buffer[:BUFFER_SIZE]
        data_buffer = data_buffer[BUFFER_SIZE:]

        # Downsample the data to the target rate
        data_block = downsample(data_block, len(data_block), TARGET_SAMPLING_RATE)

        # Convert data block to JSON
        data_json = json.dumps({"data": data_block.tolist()})

        # Publish the processed data to MQTT
        client.publish(MQTT_OUTPUT_TOPIC, data_json)
        print(f"Published data block of size {len(data_block)} at {TARGET_SAMPLING_RATE} Hz")

# Callback function when a message is received
def on_message(client, userdata, message):
    global data_buffer
    try:
        # Decode the message payload
        payload = message.payload.decode('utf-8')
        
        # Parse the JSON data
        neural_data = json.loads(payload)
        
        # Assuming neural_data['data'] is a list of lists with samples from multiple channels
        # For simplicity, flattening the list (this depends on your actual data structure)
        flat_data = [item for sublist in neural_data['data'] for item in sublist]
        
        # Append data to buffer
        data_buffer.extend(flat_data)
        
    except Exception as e:
        print(f"Error processing message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_message callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the neural data topic
client.subscribe(MQTT_INPUT_TOPIC)

# Start the MQTT client loop
client.loop_start()

try:
    # Run at 25 Hz
    while True:
        time.sleep(1 / UPDATE_RATE)
        process_and_send_data(client)
except KeyboardInterrupt:
    print("Stopping...")
    client.loop_stop()
    client.disconnect()
