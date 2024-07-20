import paho.mqtt.client as mqtt
import json
import time
import numpy as np

# Buffers for distance to target and adjusted force
distance_buffer = []
adjusted_force_buffer = []

# Define min and max values for normalization
distance_min, distance_max = float('inf'), float('-inf')
force_min, force_max = float('inf'), float('-inf')
adjusted_force_min, adjusted_force_max = float('inf'), float('-inf')
improvement_rate_min, improvement_rate_max = float('inf'), float('-inf')

# Normalize value between 0 and 1 based on observed min and max
def normalize_value(value, min_value, max_value):
    if max_value - min_value == 0:
        return 0  # Avoid division by zero
    return (value - min_value) / (max_value - min_value)

# Define the function to determine the state based on distance_to_target
def determine_state(distance_to_target):
    challenging_shot_threshold = 0.05  # Define the threshold below which the state is considered 'challenging'
    
    # Check if the distance_to_target is below the challenging shot threshold
    if distance_to_target < challenging_shot_threshold:
        state = "challenging"  # If true, set the state to 'challenging'
    else:
        state = "resting"  # Otherwise, set the state to 'resting'
    
    return state

# Other feature encoding functions
def encode_variability_factor(normalized_value):
    return 0.7 if 0.3 <= normalized_value <= 0.7 else 0.5

def encode_variance(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_standard_deviation(normalized_value):
    return normalized_value * 0.5  # Range: 0 to 0.5

def encode_rms_value(normalized_value):
    return normalized_value * 0.3  # Range: 0 to 0.3

def encode_fractal_dimension(normalized_value):
    return normalized_value * 0.5 + 1.0  # Range: 1.0 to 1.5

def encode_num_peaks(normalized_value):
    return int(normalized_value * 50)  # Range: 0 to 50

def encode_peak_height(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_target_rate(normalized_value):
    return 1 if normalized_value <= 0.5 else 0  # Binary value

def encode_base_freq(normalized_value):
    return 9 + normalized_value * 11  # Range: 9 to 11 Hz

def encode_harmonics(normalized_value):
    return 2 + normalized_value * 4  # Range: 2 to 4 Hz

def encode_blend_factor(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_global_sync_level(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_pairwise_sync_level(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_sync_factor(normalized_value):
    return normalized_value * 0.1  # Range: 0 to 0.1

def encode_influence_factor(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_max_influence(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_centroid_factor(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_edge_density_factor(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_warping_factor(normalized_value):
    return normalized_value * 0.3 + 0.2  # Range: 0.2 to 0.5

def encode_complexity_factor(normalized_value):
    return normalized_value * 0.3 + 0.1  # Range: 0.1 to 0.4

def encode_evolution_rate(normalized_value):
    return normalized_value * 0.05 + 0.05  # Range: 0.05 to 0.1

def encode_frequency_parameters(normalized_value):
    low_freq = 0.5 + normalized_value * 3.5  # Range: 0.5 to 4 Hz
    high_freq = 30 + normalized_value * 70  # Range: 30 to 100 Hz
    return low_freq, high_freq

def encode_causality_strength(normalized_value):
    return normalized_value  # Range: 0 to 1

def encode_num_imfs(normalized_value):
    return int(normalized_value * 8) + 2  # Range: 2 to 10

def encode_metadata_to_params(normalized_value):
    modification_factor = 0.5 + 0.3 * normalized_value
    matrix_size = int(5 + 20 * normalized_value)
    value_range = (0.1 + 0.3 * normalized_value, 0.7 + 0.2 * normalized_value)
    num_matrices = int(2 + 8 * normalized_value)
    step_value = max(1, int(1 + normalized_value * 10))  # Ensure step is at least 1
    eigenvalue_subset = np.arange(0, matrix_size, step=step_value)
    return modification_factor, matrix_size, value_range, num_matrices, eigenvalue_subset

def metadata_to_features(distance_to_target, player_force, adjusted_force, improvement_rate):
    features = {}
    
    normalized_distance = normalize_value(distance_to_target, distance_min, distance_max)
    normalized_force = normalize_value(player_force, force_min, force_max)
    normalized_adjusted_force = normalize_value(adjusted_force, adjusted_force_min, adjusted_force_max)
    normalized_improvement_rate = normalize_value(improvement_rate, improvement_rate_min, improvement_rate_max)
    
    features['channel_1'] = calculate_features(normalized_distance, is_distance=True)
    features['channel_2'] = calculate_features(normalized_force)
    features['channel_3'] = calculate_features(normalized_adjusted_force)
    features['channel_4'] = calculate_features(normalized_improvement_rate)
    
    return features

def calculate_features(normalized_value, is_distance=False):
    features = {
        "variability_factor": encode_variability_factor(normalized_value),
        "variance": encode_variance(normalized_value),
        "std_dev": encode_standard_deviation(normalized_value),
        "rms_value": encode_rms_value(normalized_value),
        "num_peaks": encode_num_peaks(normalized_value),
        "peak_height": encode_peak_height(normalized_value),
        "fractal_dimension": encode_fractal_dimension(normalized_value),
        "target_rate": encode_target_rate(normalized_value),
        "base_freq": encode_base_freq(normalized_value),
        "harmonics": encode_harmonics(normalized_value),
        "blend_factor": encode_blend_factor(normalized_value),
        "global_sync_level": encode_global_sync_level(normalized_value),
        "pairwise_sync_level": encode_pairwise_sync_level(normalized_value),
        "sync_factor": encode_sync_factor(normalized_value),
        "influence_factor": encode_influence_factor(normalized_value),
        "max_influence": encode_max_influence(normalized_value),
        "centroid_factor": encode_centroid_factor(normalized_value),
        "edge_density_factor": encode_edge_density_factor(normalized_value),
        "warping_factor": encode_warping_factor(normalized_value),
        "complexity_factor": encode_complexity_factor(normalized_value),
        "evolution_rate": encode_evolution_rate(normalized_value),
        "low_freq": encode_frequency_parameters(normalized_value)[0],
        "high_freq": encode_frequency_parameters(normalized_value)[1],
        "causality_strength": encode_causality_strength(normalized_value),
        "num_imfs": encode_num_imfs(normalized_value),
        "metadata_to_params": encode_metadata_to_params(normalized_value)
    }

    if is_distance:
        features["state"] = determine_state(normalized_value)
    
    return features

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("metadata")

metadata_buffer = None
last_publish_time = time.time()

def on_message(client, userdata, msg):
    global metadata_buffer, distance_min, distance_max, force_min, force_max, adjusted_force_min, adjusted_force_max, improvement_rate_min, improvement_rate_max
    try:
        game_state = json.loads(msg.payload.decode('utf-8'))
        distance_to_target = game_state.get('distance_to_target')
        player_force = game_state.get('player_force')
        adjusted_force = game_state.get('adjusted_force')

        # Ensure we have valid data
        if distance_to_target is None or player_force is None or adjusted_force is None:
            print(f"Received invalid data: {game_state}")
            return

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

        # Update min and max values
        distance_min = min(distance_min, distance_to_target)
        distance_max = max(distance_max, distance_to_target)
        force_min = min(force_min, player_force)
        force_max = max(force_max, player_force)
        adjusted_force_min = min(adjusted_force_min, adjusted_force)
        adjusted_force_max = max(adjusted_force_max, adjusted_force)
        improvement_rate_min = min(improvement_rate_min, improvement_rate)
        improvement_rate_max = max(improvement_rate_max, improvement_rate)

        metadata_buffer = (distance_to_target, player_force, adjusted_force, improvement_rate)
    except Exception as e:
        print(f"Error processing message: {e}")

def calculate_improvement_rate():
    if len(distance_buffer) < 2:
        return 0.0

    distance_improvement = np.diff(distance_buffer)
    force_adjustments = np.diff(adjusted_force_buffer)
    improvement_rate = np.mean(distance_improvement / (force_adjustments + 1e-6))  # Avoid division by zero

    return improvement_rate

def publish_features(client):
    global metadata_buffer, last_publish_time
    current_time = time.time()
    
    if metadata_buffer and (current_time - last_publish_time) >= 0.25:  # 4 Hz
        distance_to_target, player_force, adjusted_force, improvement_rate = metadata_buffer
        features = metadata_to_features(distance_to_target, player_force, adjusted_force, improvement_rate)
        
        # Convert numpy arrays to lists in the features
        for channel in features:
            metadata_to_params = features[channel]['metadata_to_params']
            features[channel]['metadata_to_params'] = [
                metadata_to_params[0],
                metadata_to_params[1],
                metadata_to_params[2],
                metadata_to_params[3],
                metadata_to_params[4].tolist() if isinstance(metadata_to_params[4], np.ndarray) else metadata_to_params[4]  # Convert ndarray to list if necessary
            ]

        encoded_features = json.dumps(features)
        client.publish("GAME FEATURES", encoded_features)
        print(f"Published GAME FEATURES: {encoded_features}")
        last_publish_time = current_time

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("127.0.0.1", 1883, 60)
    
    client.loop_start()
    
    try:
        while True:
            publish_features(client)
            time.sleep(0.01)  # Small sleep to avoid busy-waiting
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
