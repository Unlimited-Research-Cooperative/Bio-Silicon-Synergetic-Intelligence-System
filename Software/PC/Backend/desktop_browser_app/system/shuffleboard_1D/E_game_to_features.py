import zmq
import time
import json

def determine_state(normalized_distance):
    # Define thresholds for determining resting vs. active states
    easy_shot_threshold = 0.1  # Threshold for easy shot
    challenging_shot_threshold = 0.9  # Threshold for challenging shot
    
    # Determine the state based on the normalized distance
    if normalized_distance < easy_shot_threshold or normalized_distance > challenging_shot_threshold:
        state = "resting"
    else:
        state = "active"
    
    return state

def calculate_variability_factor(normalized_distance, normalized_force):
    # Define the mapping of game metadata to variability factor
    # Adjust these mappings based on the desired behavior in response to game metadata
    if 0.3 <= normalized_distance <= 0.7 and 0.2 <= normalized_force <= 0.8:
        # Both distance and force within optimal ranges
        variability_factor = 0.7  # High variability to encourage flexibility
    else:
        # Either distance or force outside optimal ranges
        variability_factor = 0.5  # Moderate variability as a default    
        
    return variability_factor

def calculate_variance(normalized_distance, normalized_force):
    # Encode metadata into the variance value
    variance = normalized_distance + normalized_force
    
    return variance

def calculate_standard_deviation(normalized_distance, normalized_force):
    # Initial value for standard deviation
    std_dev = normalized_distance * 0.5 + normalized_force * 0.5
    
    return std_dev

def encode_rms_value(normalized_distance, normalized_force):
    # Initial value for RMS value
    rms_value = normalized_distance * 0.3 + normalized_force * 0.7
    
    return rms_value

def encode_fractal_dimension(normalized_distance, normalized_force):
    # Calculate fractal dimension based on normalized metadata
    fractal_dimension = normalized_distance * 0.2 + normalized_force * 0.5

    return fractal_dimension

def encode_num_peaks(normalized_distance, normalized_force):
    # Assuming the number of peaks is determined by the product of normalized_distance and normalized_force
    num_peaks = int(normalized_distance * normalized_force * 10)  # Multiplying by 10 for scale

    return num_peaks

def encode_peak_height(normalized_distance, normalized_force):
    # Assuming the peak height is determined by the product of normalized_distance and normalized_force
    peak_height = normalized_distance * normalized_force  # Multiplying the two factors

    return peak_height

def encode_target_rate(normalized_distance):
    # Assuming target_rate decreases linearly with distance, and is 1 for distance <= 50 and 0 otherwise
    target_rate = 1 if normalized_distance <= 0.5 else 0

    return target_rate

def encode_min_freq(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    min_freq = 0.2 + 0.3 * normalized_distance + 0.2 * normalized_force

    return min_freq

def encode_max_freq(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    max_freq = 0.4 + 0.3 * normalized_distance + 0.2 * normalized_force

    return max_freq

def encode_blend_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    blend_factor = 0.5 - 0.3 * normalized_distance + 0.2 * normalized_force

    return blend_factor

def encode_global_sync_level(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    global_sync_level = 0.2 + 0.3 * normalized_distance + 0.2 * normalized_force

    return global_sync_level

def encode_pairwise_sync_level(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    pairwise_sync_level = 0.4 + 0.2 * normalized_distance + 0.3 * normalized_force

    return pairwise_sync_level

def encode_sync_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    sync_factor = 0.05 + 0.1 * normalized_distance - 0.1 * normalized_force

    return sync_factor

def encode_influence_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    influence_factor = 0.3 + 0.3 * normalized_distance + 0.2 * normalized_force

    return influence_factor

def encode_max_influence(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    max_influence = 0.5 + 0.3 * normalized_distance + 0.2 * normalized_force

    return max_influence

def encode_centroid_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    centroid_factor = 0.4 + 0.3 * normalized_distance + 0.3 * normalized_force

    return centroid_factor

def encode_edge_density_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    edge_density_factor = 0.3 + 0.2 * normalized_distance + 0.5 * normalized_force

    return edge_density_factor

def encode_warping_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    warping_factor = 0.2 + 0.6 * normalized_distance + 0.2 * normalized_force

    return warping_factor

def encode_complexity_factor(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    complexity_factor = 0.1 + 0.4 * normalized_distance + 0.5 * normalized_force

    return complexity_factor

def encode_evolution_rate(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    evolution_rate = 0.05 + 0.1 * normalized_distance + 0.2 * normalized_force

    return evolution_rate

def encode_frequency_parameters(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    low_freq = 0.1 + 0.3 * normalized_distance
    high_freq = 0.5 + 0.3 * normalized_force

    return low_freq, high_freq

def encode_causality_strength(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    causality_strength = 0.1 + 0.5 * normalized_distance + 0.2 * normalized_force

    return causality_strength

def encode_num_imfs(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    num_imfs = int(2 + 5 * normalized_distance + 2 * normalized_force)

    return num_imfs

def encode_metadata_to_params(normalized_distance, normalized_force):
    # Encoding logic based on normalized_distance and normalized_force
    modification_factor = 0.5 + 0.3 * normalized_distance - 0.1 * normalized_force
    matrix_size = int(5 + 20 * normalized_distance)
    value_range = (0.1 + 0.3 * normalized_force, 0.7 + 0.2 * normalized_distance)
    num_matrices = int(2 + 8 * normalized_distance)
    eigenvalue_subset = np.arange(0, matrix_size, step=int(1 + normalized_force * 10))

    return modification_factor, matrix_size, value_range, num_matrices, eigenvalue_subset

def metadata_to_features(distance_to_target, player_force):
    # Normalize once per update
    normalized_distance = distance_to_target / 100.0  # Assuming max distance of 100 units
    normalized_force = player_force / 100.0  # Assuming max force of 100 units
    
    state = determine_state(normalized_distance)
    variability_factor = calculate_variability_factor(normalized_distance, normalized_force)
    variance = calculate_variance(normalized_distance, normalized_force)
    std_dev = calculate_standard_deviation(normalized_distance, normalized_force)
    rms_value = encode_rms_value(normalized_distance, normalized_force)
    num_peaks = encode_num_peaks(normalized_distance, normalized_force)
    peak_height = encode_peak_height(normalized_distance, normalized_force)
    fractal_dimension = encode_fractal_dimension(normalized_distance, normalized_force)
    target_rate = encode_target_rate(normalized_distance)
    min_freq = encode_min_freq(normalized_distance, normalized_force)
    max_freq = encode_max_freq(normalized_distance, normalized_force)
    blend_factor = encode_blend_factor(normalized_distance, normalized_force)
    global_sync_level = encode_global_sync_level(normalized_distance, normalized_force)
    pairwise_sync_level = encode_pairwise_sync_level(normalized_distance, normalized_force)
    sync_factor = encode_sync_factor(normalized_distance, normalized_force)
    influence_factor = encode_influence_factor(normalized_distance, normalized_force)
    max_influence = encode_max_influence(normalized_distance, normalized_force)
    centroid_factor = encode_centroid_factor(normalized_distance, normalized_force)
    edge_density_factor = encode_edge_density_factor(normalized_distance, normalized_force)
    warping_factor = encode_warping_factor(normalized_distance, normalized_force)
    complexity_factor = encode_complexity_factor(normalized_distance, normalized_force)
    evolution_rate = encode_evolution_rate(normalized_distance, normalized_force)
    low_freq, high_freq = encode_frequency_parameters(normalized_distance, normalized_force)
    causality_strength = encode_causality_strength(normalized_distance, normalized_force)
    num_imfs = encode_num_imfs(normalized_distance, normalized_force)
    metadata_to_params = encode_metadata_to_params(normalized_distance, normalized_force)

    features = {
        "state": state,
        "variability_factor": variability_factor,
        "variance": variance,
        "std_dev": std_dev,
        "rms_value": rms_value,
        "num_peaks": num_peaks,
        "peak_height": peak_height,
        "window_size": 0.5,  # Static value as a placeholder
        "fractal_dimension": fractal_dimension,
        "target_rate": target_rate,
        "min_freq": min_freq,
        "max_freq": max_freq,
        "blend_factor": blend_factor,
        "global_sync_level": global_sync_level,
        "pairwise_sync_level": pairwise_sync_level,
        "sync_factor": sync_factor,
        "influence_factor": influence_factor,
        "max_influence": max_influence,
        "centroid_factor": centroid_factor,
        "edge_density_factor": edge_density_factor,
        "warping_factor": warping_factor,
        "complexity_factor": complexity_factor,
        "evolution_rate": evolution_rate,
        "low_freq": low_freq,
        "high_freq": high_freq,
        "causality_strength": causality_strength,
        "num_imfs": num_imfs,
        "metadata_to_params": metadata_to_params
    }
    
    return features


def main():
    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5556")
    
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    
    while True:
        try:
            # Wait for an incoming message containing game state
            message = subscriber.recv_string(zmq.NOBLOCK)
            game_state = json.loads(message)  # Assuming game_state is a dict with 'distance_to_target' and 'player_force'
            
            features = metadata_to_features(game_state['distance_to_target'], game_state['player_force'])
            
            # Convert the features dictionary to a string for publishing
            encoded_features = json.dumps(features)
            publisher.send_string(encoded_features)
            
        except zmq.Again:
            # No message received yet
            time.sleep(0.1)  # Sleep briefly to maintain a 10Hz update rate
            continue

if __name__ == "__main__":
    main()