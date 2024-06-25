import paho.mqtt.client as mqtt
import json
import time
import numpy as np

# Constants for digital signal
ON_SIGNAL = 150  # microvolts
OFF_SIGNAL = 0  # microvolts
BITS_PER_FEATURE = 16
BIT_DURATION = 0.001875  # 1.875 ms per bit (16 bits * 1.875 ms = 0.03s per feature, 4 features * 0.03s = 0.12s)
STIM_DURATION = 0.12  # 120 ms (16 bits * 1.875 ms * 4 features)
SIN_CHAOS_DURATION = 0.13  # 130 ms
UPDATE_INTERVAL = 0.25  # 250 ms
NUM_CHANNELS = 4
FREQUENCY = 10  # 10 Hz for the sine wave

# Global variable to store the latest outcome
latest_outcome = "neutral"

def float_to_binary(value, bits=BITS_PER_FEATURE):
    """Converts a floating point number to a binary string of specified length."""
    if value is None:
        value = 0.0
    max_val = (1 << bits) - 1
    scaled_value = int((value / 100.0) * max_val)  # Assuming the value is between 0 and 100
    return f'{scaled_value:0{bits}b}'

def generate_digital_signals(features):
    """Generates digital signals for each feature value."""
    digital_signals_per_channel = []
    for feature_value in features:
        # Convert each feature value to binary string with the specified number of bits
        binary_feature = float_to_binary(feature_value)
        print(f"Feature value: {feature_value}, Binary: {binary_feature}")  # Debug statement
        # Convert binary strings to list of signals (ON_SIGNAL or OFF_SIGNAL)
        digital_signals_feature = [ON_SIGNAL if bit == '1' else OFF_SIGNAL for bit in binary_feature]
        digital_signals_per_channel.append(digital_signals_feature)
    return digital_signals_per_channel

def calculate_packet_length(features):
    """Calculates the packet length in seconds based on the metadata."""
    total_bits = len(features) * BITS_PER_FEATURE
    total_duration = total_bits * BIT_DURATION
    return total_duration

def generate_waveform(outcome):
    """Generates a waveform based on the outcome."""
    num_samples = int(SIN_CHAOS_DURATION / BIT_DURATION)
    if outcome == "reward":
        t = np.linspace(0, SIN_CHAOS_DURATION, num_samples, endpoint=False)
        waveform = 75 * (np.sin(2 * np.pi * FREQUENCY * t) + 1)  # Clean sine wave between 0 and 150
    elif outcome == "distress":
        waveform = np.random.uniform(0, 150, num_samples)  # Chaotic wave between 0 and 150
    else:
        waveform = [OFF_SIGNAL] * num_samples  # No signal
    return waveform.tolist()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("metadata")
    client.subscribe("outcome")

def on_message(client, userdata, message):
    global latest_outcome

    try:
        payload = message.payload.decode('utf-8')
        if message.topic == "metadata":
            game_state = json.loads(payload)
            
            # Assume game_state contains relevant numerical features
            features = [
                game_state.get('score', 0),
                game_state.get('round', 0),
                game_state.get('distance_to_target', 0.0),
                game_state.get('player_force', 0.0)
            ]
            
            # Print received features for debugging
            print(f"Received features: {features}")
            
            # Calculate packet length in seconds
            packet_length = calculate_packet_length(features)
            print(f"Packet length: {packet_length} seconds")
            
            # Generate the digital signals for each feature
            digital_signals_per_channel = generate_digital_signals(features)
            print(f"Digital signals: {digital_signals_per_channel}")  # Debug statement
            
            # Create a list of 120 ms long signals for each channel
            stim_signals = []
            for channel_signals in digital_signals_per_channel:
                stim_channel = [channel_signals[i % len(channel_signals)] for i in range(int(STIM_DURATION / BIT_DURATION))]
                stim_signals.append(stim_channel)
            
            # Ensure we have exactly NUM_CHANNELS (pad with OFF_SIGNAL if necessary)
            while len(stim_signals) < NUM_CHANNELS:
                stim_signals.append([OFF_SIGNAL] * int(STIM_DURATION / BIT_DURATION))
            
            # Generate waveform based on the latest outcome
            waveform = generate_waveform(latest_outcome)
            print(f"Generated waveform based on outcome '{latest_outcome}': {waveform}")  # Debug statement
            
            # Append the waveform to the stimulation signals
            for i in range(NUM_CHANNELS):
                stim_signals[i].extend(waveform)
            
            # Publish the stimulation signals to the MQTT topic "DIGITAL SIGNALS"
            stim_signals_data = json.dumps({"stim_signals": stim_signals})
            client.publish("DIGITAL SIGNALS", stim_signals_data)
            print(f"Published digital signals: {stim_signals_data}")  # Debug statement
        
        elif message.topic == "outcome":
            latest_outcome = payload
            print(f"Received outcome: {latest_outcome}")

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
