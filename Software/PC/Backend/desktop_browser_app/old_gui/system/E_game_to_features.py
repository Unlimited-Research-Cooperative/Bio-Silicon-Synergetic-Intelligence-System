import numpy as np
import zmq
import time

class SymbolicStates: 
    PLAYER_MOVEMENT = {"forward": 1, "left": 2, "right": 2, "backward": 3, "none": 0}
    DOOR_STATES = {"no door": 0, "closed": 3, "open": 1, "door far ahead": 2}
    ENEMY_TYPES = {"none": 0, "weak": 1, "strong": 2, "boss": 3}
    PLAYER_HEALTH_STATES = {"critical": 4, "low": 3, "medium": 2, "high": 1, "full": 0}
    ACTION_STATES = {"moving": 1, "shooting": 2, "escaping enemy": 3}
    EXPLORING_STATES = {"corridor": 1, "open room": 2}
    LEVEL_STATES = {"looking for door key": 2, "have door key": 1}
    WALL_STATES = {"wall to the left": 1, "wall to the right": 1, "wall in front": 2, "wall to the left and right": 3, "dead end": 4}

def metadata_to_features(metadata):
    features = {

        # Mapping og action state to neural state
        "state": SymbolicStates.ACTION_STATES.get(metadata.get("player_action", "shooting"), 1) / 3.0,  # Max value for movement is 3
        
        # Direct mapping of player movement to variability factor, normalized to a 0-1 scale
        "variability_factor": SymbolicStates.PLAYER_MOVEMENT.get(metadata.get("player_movement", "none"), 0) / 3.0,  # Max value for movement is 3
        
        # Mapping door state to variance feature
        "variance": SymbolicStates.DOOR_STATES.get(metadata.get("door_state", "no door"), 0) / 3.0,  # Max value for door states is 3
        
        # Mapping enemy type to standard deviation feature
        "std_dev": SymbolicStates.ENEMY_TYPES.get(metadata.get("enemy_type", "none"), 0) / 3.0,  # Max value for enemy types is 3
        
        # Player health state affects the RMS value feature
        "rms_value": SymbolicStates.PLAYER_HEALTH_STATES.get(metadata.get("player_health", "full"), 0) / 4.0,  # Max value for health states is 4
        
        # Action states influence the fractal dimension
        "fractal_dimension": SymbolicStates.ACTION_STATES.get(metadata.get("player_action", "moving"), 0) / 3.0,  # Max value for action states is 3
        
        # Number of peaks determined by exploring states
        "num_peaks": SymbolicStates.EXPLORING_STATES.get(metadata.get("exploring_state", "corridor"), 1),  # Direct mapping
        
        # Peak height influenced by level state
        "peak_height": SymbolicStates.LEVEL_STATES.get(metadata.get("level_state", "looking for door key"), 1) / 2.0,  # Normalized
        
        # Window size feature influenced by wall states
        "window_size": SymbolicStates.WALL_STATES.get(metadata.get("wall_state", "no wall"), 0) / 4.0,  # Max value for wall states is 4
        
        # Target rate is determined by the presence of any enemy type
        "target_rate": 1.0 if SymbolicStates.ENEMY_TYPES.get(metadata.get("enemy_type", "none"), 0) != 0 else 0,
        
        # Minimum frequency affected by player movement, demonstrating a range for frequency based on movement
        "min_freq": 0.1 * SymbolicStates.PLAYER_MOVEMENT.get(metadata.get("player_movement", "none"), 0),
        
        # Maximum frequency influenced by player health state, indicating a dynamic range based on health
        "max_freq": 0.1 * SymbolicStates.PLAYER_HEALTH_STATES.get(metadata.get("player_health", "full"), 0),
        
        # Static blend factor as a static state
        "blend_factor": 0.5,
        
        # Global sync level determined by action state, reflecting synchronization needs
        "global_sync_level": SymbolicStates.ACTION_STATES.get(metadata.get("player_action", "moving"), 0) / 3.0,
        
        # Pairwise sync level affected by door state, indicating sync adjustments based on environmental factors
        "pairwise_sync_level": SymbolicStates.DOOR_STATES.get(metadata.get("door_state", "no door"), 0) / 3.0,
        
        # Sync factor as a static value for simplicity
        "sync_factor": 0.5,
        
        # Influence factor derived from enemy type, representing external influence levels
        "influence_factor": SymbolicStates.ENEMY_TYPES.get(metadata.get("enemy_type", "none"), 0) / 3.0,
        
        # Maximum influence as a static maximum for the presence of any enemy
        "max_influence": 1.0,
        
        # Centroid factor and edge density factor as placeholders for sensory data encoding
        "centroid_factor": 0.5,
        "edge_density_factor": SymbolicStates.WALL_STATES.get(metadata.get("wall_state", "no wall"), 0) / 4.0,
        
        # Evolution rate as a static value for dynamic environmental changes
        "evolution_rate": 0.5,
        
        # Low and high frequency ranges influenced by exploring and level states, respectively
        "low_freq": SymbolicStates.EXPLORING_STATES.get(metadata.get("exploring_state", "corridor"), 1) / 2.0,
        "high_freq": SymbolicStates.LEVEL_STATES.get(metadata.get("level_state", "looking for door key"), 1) / 2.0,
        
        # Causality strength and number of intrinsic mode functions (IMFs) as static values for interaction effects
        "causality_strength": 0.5,
        "num_imfs": 2
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
        metadata_packet = {
            "player_movement": "forward",
            "door_state": "open",
            "enemy_type": "boss",
            "player_health": "medium",
            "player_action": "shooting",
            "exploring_state": "corridor",
            "level_state": "looking for door key",
            "wall_state": "wall to the right"
        }

        features = metadata_to_features(metadata_packet)
        
        # Convert the features dictionary to a string for publishing
        encoded_features = " ".join([f"{key}:{value:.2f}" for key, value in features.items()])
        publisher.send_string(encoded_features)
    
        time.sleep(1)  # Delay to simulate time between data sends

if __name__ == "__main__":
    main()