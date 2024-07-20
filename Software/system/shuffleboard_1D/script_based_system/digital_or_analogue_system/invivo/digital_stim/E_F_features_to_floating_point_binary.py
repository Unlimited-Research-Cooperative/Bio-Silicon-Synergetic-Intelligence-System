import paho.mqtt.client as mqtt
import json
import time
import numpy as np

# Constants for digital signal
ON_SIGNAL = 150  # microvolts
OFF_SIGNAL = 0  # microvolts
BITS_PER_FEATURE = 16
NUM_CHANNELS = 4
PACKET_DURATION = 0.25  # 250 ms packets
STIM_DURATION = .25
BIT_DURATION = PACKET_DURATION / (BITS_PER_FEATURE * NUM_CHANNELS)  # New bit duration based on total packet duration
UPDATE_INTERVAL = 0.25  # 250 ms

# Buffers for distance to target and adjusted force
distance_buffer = []
adjusted_force_buffer = []

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

def calculate_improvement_rate():
    """Calculates the improvement rate based on the distance to target and adjusted force over time."""
    if len(distance_buffer) < 2:
        return 0.0

    distance_improvement = np.diff(distance_buffer)
    force_adjustments = np.diff(adjusted_force_buffer)
    improvement_rate = np.mean(distance_improvement / (force_adjustments + 1e-6))  # Avoid division by zero

    return improvement_rate

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("metadata")

def on_message(client, userdata, message):
    global latest_outcome

    try:
        payload = message.payload.decode('utf-8')
        if message.topic == "metadata":
            game_state = json.loads(payload)
            
            # Extract relevant features
            distance_to_target = game_state.get('distance_to_target', 0.0)
            adjusted_force = game_state.get('adjusted_force', 0.0)
            player_force = game_state.get('player_force', 0.0)

            # Update buffers
            distance_buffer.append(distance_to_target)
            adjusted_force_buffer.append(adjusted_force)

            # Ensure buffers do not grow indefinitely
            if len(distance_buffer) > 100:
                distance_buffer.pop(0)
            if len(adjusted_force_buffer) > 100:
                adjusted_force_buffer.pop(0)

            # Calculate improvement rate
            improvement_rate = calculate_improvement_rate()

            # Prepare features for digital signals
            features = [distance_to_target, adjusted_force, player_force, improvement_rate]
            
            # Print received features for debugging
            print(f"Received features: {features}")
            
            # Calculate packet length in seconds
            packet_length = calculate_packet_length(features)
            print(f"Packet length: {packet_length} seconds")
            
            # Generate the digital signals for each feature
            digital_signals_per_channel = generate_digital_signals(features)
            print(f"Digital signals: {digital_signals_per_channel}")  # Debug statement
            
            # Create a list of 250 ms long signals for each channel
            stim_signals = []
            for channel_signals in digital_signals_per_channel:
                stim_channel = [channel_signals[i % len(channel_signals)] for i in range(int(STIM_DURATION / BIT_DURATION))]
                stim_signals.append(stim_channel)
            
            # Ensure we have exactly NUM_CHANNELS (pad with OFF_SIGNAL if necessary)
            while len(stim_signals) < NUM_CHANNELS:
                stim_signals.append([OFF_SIGNAL] * int(STIM_DURATION / BIT_DURATION))
            
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
