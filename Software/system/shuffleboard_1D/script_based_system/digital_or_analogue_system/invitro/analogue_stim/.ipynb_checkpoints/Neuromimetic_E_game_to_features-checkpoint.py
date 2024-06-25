import paho.mqtt.client as mqtt
import json
import time
import numpy as np

# Define all the feature encoding functions
def determine_state(normalized_distance):
    easy_shot_threshold = 0.1
    challenging_shot_threshold = 0.9
    
    if normalized_distance < easy_shot_threshold or normalized_distance > challenging_shot_threshold:
        state = "resting"
    else:
        state = "active"
    
    return state

def encode_variability_factor(normalized_distance, normalized_force):
    if 0.3 <= normalized_distance <= 0.7 and 0.2 <= normalized_force <= 0.8:
        variability_factor = 0.7
    else:
        variability_factor = 0.5    
        
    return variability_factor

def encode_variance(normalized_distance, normalized_force):
    variance = normalized_distance + normalized_force
    return variance

def encode_standard_deviation(normalized_distance, normalized_force):
    std_dev = normalized_distance * 0.5 + normalized_force * 0.5
    return std_dev

def encode_rms_value(normalized_distance, normalized_force):
    rms_value = normalized_distance * 0.3 + normalized_force * 0.7
    return rms_value

def encode_fractal_dimension(normalized_distance, normalized_force):
    fractal_dimension = normalized_distance * 0.2 + normalized_force * 0.5
    return fractal_dimension

def encode_num_peaks(normalized_distance, normalized_force):
    num_peaks = int(normalized_distance * normalized_force * 10)
    return num_peaks

def encode_peak_height(normalized_distance, normalized_force):
    peak_height = normalized_distance * normalized_force
    return peak_height

def encode_target_rate(normalized_distance):
    target_rate = 1 if normalized_distance <= 0.5 else 0
    return target_rate

def encode_min_freq(normalized_distance, normalized_force):
    min_freq = 0.2 + 0.3 * normalized_distance + 0.2 * normalized_force
    return min_freq

def encode_max_freq(normalized_distance, normalized_force):
    max_freq = 0.4 + 0.3 * normalized_distance + 0.2 * normalized_force
    return max_freq

def encode_blend_factor(normalized_distance, normalized_force):
    blend_factor = 0.5 - 0.3 * normalized_distance + 0.2 * normalized_force
    return blend_factor

def encode_global_sync_level(normalized_distance, normalized_force):
    global_sync_level = 0.2 + 0.3 * normalized_distance + 0.2 * normalized_force
    return global_sync_level

def encode_pairwise_sync_level(normalized_distance, normalized_force):
    pairwise_sync_level = 0.4 + 0.2 * normalized_distance + 0.3 * normalized_force
    return pairwise_sync_level

def encode_sync_factor(normalized_distance, normalized_force):
    sync_factor = 0.05 + 0.1 * normalized_distance - 0.1 * normalized_force
    return sync_factor

def encode_influence_factor(normalized_distance, normalized_force):
    influence_factor = 0.3 + 0.3 * normalized_distance + 0.2 * normalized_force
    return influence_factor

def encode_max_influence(normalized_distance, normalized_force):
    max_influence = 0.5 + 0.3 * normalized_distance + 0.2 * normalized_force
    return max_influence

def encode_centroid_factor(normalized_distance, normalized_force):
    centroid_factor = 0.4 + 0.3 * normalized_distance + 0.3 * normalized_force
    return centroid_factor

def encode_edge_density_factor(normalized_distance, normalized_force):
    edge_density_factor = 0.3 + 0.2 * normalized_distance + 0.5 * normalized_force
    return edge_density_factor

def encode_warping_factor(normalized_distance, normalized_force):
    warping_factor = 0.2 + 0.6 * normalized_distance + 0.2 * normalized_force
    return warping_factor

def encode_complexity_factor(normalized_distance, normalized_force):
    complexity_factor = 0.1 + 0.4 * normalized_distance + 0.5 * normalized_force
    return complexity_factor

def encode_evolution_rate(normalized_distance, normalized_force):
    evolution_rate = 0.05 + 0.1 * normalized_distance + 0.2 * normalized_force
    return evolution_rate

def encode_frequency_parameters(normalized_distance, normalized_force):
    low_freq = 0.1 + 0.3 * normalized_distance
    high_freq = 0.5 + 0.3 * normalized_force
    return low_freq, high_freq

def encode_causality_strength(normalized_distance, normalized_force):
    causality_strength = 0.1 + 0.5 * normalized_distance + 0.2 * normalized_force
    return causality_strength

def encode_num_imfs(normalized_distance, normalized_force):
    num_imfs = int(2 + 5 * normalized_distance + 2 * normalized_force)
    return num_imfs

def encode_metadata_to_params(normalized_distance, normalized_force):
    modification_factor = 0.5 + 0.3 * normalized_distance - 0.1 * normalized_force
    matrix_size = int(5 + 20 * normalized_distance)
    value_range = (0.1 + 0.3 * normalized_force, 0.7 + 0.2 * normalized_distance)
    num_matrices = int(2 + 8 * normalized_distance)
    eigenvalue_subset = np.arange(0, matrix_size, step=int(1 + normalized_force * 10))
    return modification_factor, matrix_size, value_range, num_matrices, eigenvalue_subset

def metadata_to_features(distance_to_target, player_force):
    normalized_distance = distance_to_target / 100.0
    normalized_force = player_force / 100.0

    features = {}
    for channel in range(1, 5):
        features[f'channel_{channel}'] = {
            "state": determine_state(normalized_distance),
            "variability_factor": encode_variability_factor(normalized_distance, normalized_force),
            "variance": encode_variance(normalized_distance, normalized_force),
            "std_dev": encode_standard_deviation(normalized_distance, normalized_force),
            "rms_value": encode_rms_value(normalized_distance, normalized_force),
            "num_peaks": encode_num_peaks(normalized_distance, normalized_force),
            "peak_height": encode_peak_height(normalized_distance, normalized_force),
            "fractal_dimension": encode_fractal_dimension(normalized_distance, normalized_force),
            "target_rate": encode_target_rate(normalized_distance),
            "min_freq": encode_min_freq(normalized_distance, normalized_force),
            "max_freq": encode_max_freq(normalized_distance, normalized_force),
            "blend_factor": encode_blend_factor(normalized_distance, normalized_force),
            "global_sync_level": encode_global_sync_level(normalized_distance, normalized_force),
            "pairwise_sync_level": encode_pairwise_sync_level(normalized_distance, normalized_force),
            "sync_factor": encode_sync_factor(normalized_distance, normalized_force),
            "influence_factor": encode_influence_factor(normalized_distance, normalized_force),
            "max_influence": encode_max_influence(normalized_distance, normalized_force),
            "centroid_factor": encode_centroid_factor(normalized_distance, normalized_force),
            "edge_density_factor": encode_edge_density_factor(normalized_distance, normalized_force),
            "warping_factor": encode_warping_factor(normalized_distance, normalized_force),
            "complexity_factor": encode_complexity_factor(normalized_distance, normalized_force),
            "evolution_rate": encode_evolution_rate(normalized_distance, normalized_force),
            "low_freq": encode_frequency_parameters(normalized_distance, normalized_force)[0],
            "high_freq": encode_frequency_parameters(normalized_distance, normalized_force)[1],
            "causality_strength": encode_causality_strength(normalized_distance, normalized_force),
            "num_imfs": encode_num_imfs(normalized_distance, normalized_force),
            "metadata_to_params": encode_metadata_to_params(normalized_distance, normalized_force)
        }

    return features

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("metadata")

metadata_buffer = None
last_publish_time = time.time()

def on_message(client, userdata, msg):
    global metadata_buffer
    try:
        game_state = json.loads(msg.payload.decode('utf-8'))
        distance_to_target = game_state.get('distance_to_target')
        player_force = game_state.get('player_force')

        # Ensure we have valid data
        if distance_to_target is None or player_force is None:
            print(f"Received invalid data: {game_state}")
            return

        metadata_buffer = (distance_to_target, player_force)
    except Exception as e:
        print(f"Error processing message: {e}")

def publish_features(client):
    global metadata_buffer, last_publish_time
    current_time = time.time()
    
    if metadata_buffer and (current_time - last_publish_time) >= 0.25:  # 4 Hz
        distance_to_target, player_force = metadata_buffer
        features = metadata_to_features(distance_to_target, player_force)
        
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
