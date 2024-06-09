import json
import time
import numpy as np
from scipy.signal import resample
from data_manager import DataManager


# Constants
BUFFER_SIZE = 500
TARGET_SAMPLING_RATE = 500
UPDATE_RATE = 25
DEFAULT_SAMPLING_RATE = 512


data_buffer = []

# Callback function when a message is received
def on_message_recv(client, userdata, message):
    global data_buffer
    try:
        # Decode the message payload
        payload = message.payload.decode('utf-8')
        
        # Parse the JSON data
        neural_data = json.loads(payload)
        
        # Extract original sampling rate if provided, else use default
        original_sampling_rate = neural_data.get('sampling_rate', DEFAULT_SAMPLING_RATE)
        
        # Assuming neural_data['data'] is a list of lists with samples from multiple channels
        # For simplicity, flattening the list (this depends on your actual data structure)
        flat_data = [item for sublist in neural_data['data'] for item in sublist]
        
        # Append data to buffer
        data_buffer.extend(flat_data)

        # Process and send data at the specified update rate
        process_and_send_data(client, original_sampling_rate)
        
    except Exception as e:
        print(f"Error processing message: {e}")

client = DataManager("./neural profile.ini", on_message_recv)
client.listen()

def downsample(data, original_rate, target_rate):
    num_samples = int(len(data) * target_rate / original_rate)
    return resample(data, num_samples)


def process_and_send_data(client, original_sampling_rate):
    global data_buffer
    if len(data_buffer) >= BUFFER_SIZE:
        # Process the data in the buffer
        data_block = data_buffer[:BUFFER_SIZE]
        data_buffer = data_buffer[BUFFER_SIZE:]

        # Downsample the data to the target rate
        data_block = downsample(data_block, original_sampling_rate, TARGET_SAMPLING_RATE)

        # Convert data block to JSON
        data_json = json.dumps({"data": data_block.tolist()})

        # Publish the processed data to MQTT
        client.set_data(data_json)
        client.publish()
        print(f"Published data block of size {len(data_block)} at {TARGET_SAMPLING_RATE} Hz")
