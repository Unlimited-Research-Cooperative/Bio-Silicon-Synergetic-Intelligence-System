import paho.mqtt.client as mqtt
import json
import struct
import time

# Constants for digital signal
ON_SIGNAL = 150  # microvolts
OFF_SIGNAL = 0  # microvolts
BITS_PER_FEATURE = 16
BIT_DURATION = 0.003  # 3 ms per bit
STIM_DURATION = 0.192  # 192 ms (64 bits * 3 ms)
UPDATE_INTERVAL = 0.25  # 250 ms
NUM_CHANNELS = 4

def float_to_binary(value, bits=BITS_PER_FEATURE):
    """Converts a floating point number to a binary string of specified length."""
    max_val = (1 << bits) - 1
    scaled_value = int((value / max(value, 1.0)) * max_val)
    return f'{scaled_value:0{bits}b}'

def generate_digital_signals(features):
    """Generates digital signals for each feature value."""
    digital_signals_per_channel = []
    for feature_value in features:
        # Convert each feature value to binary string with the specified number of bits
        binary_feature = float_to_binary(feature_value)
        # Convert binary strings to list of signals (ON_SIGNAL or OFF_SIGNAL)
        digital_signals_feature = [ON_SIGNAL if bit == '1' else OFF_SIGNAL for bit in binary_feature]
        digital_signals_per_channel.append(digital_signals_feature)
    return digital_signals_per_channel

def calculate_packet_length(features):
    """Calculates the packet length in seconds based on the metadata."""
    total_bits = len(features) * BITS_PER_FEATURE
    total_duration = total_bits * BIT_DURATION
    return total_duration

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("game_metadata")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        game_state = json.loads(payload)
        
        # Assume game_state contains relevant numerical features
        features = [
            game_state.get('score', 0),
            game_state.get('round', 0),
            game_state.get('distance_to_target', 0.0),
            game_state.get('player_force', 0.0)
        ]
        
        # Calculate packet length in seconds
        packet_length = calculate_packet_length(features)
        print(f"Packet length: {packet_length} seconds")
        
        # Generate the digital signals for each feature
        digital_signals_per_channel = generate_digital_signals(features)
        
        # Create a list of 192 ms long signals for each channel
        stim_signals = []
        for channel_signals in digital_signals_per_channel:
            stim_channel = [channel_signals[i % len(channel_signals)] for i in range(int(STIM_DURATION / BIT_DURATION))]
            stim_signals.append(stim_channel)
        
        # Ensure we have exactly NUM_CHANNELS (pad with OFF_SIGNAL if necessary)
        while len(stim_signals) < NUM_CHANNELS:
            stim_signals.append([OFF_SIGNAL] * int(STIM_DURATION / BIT_DURATION))
        
        # Publish the stimulation signals to the MQTT topic "digital_signals"
        stim_signals_data = json.dumps({"stim_signals": stim_signals})
        client.publish("digital_signals", stim_signals_data)
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Set up MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)
    
    # Start MQTT loop
    mqtt_client.loop_start()
    
    try:
        while True:
            # Sleep to maintain a 4Hz update rate (250 ms interval)
            time.sleep(UPDATE_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
