import numpy as np
import zmq
import time
from metadata_encoder import MetadataToSignalEncoder

class SymbolicStates:
    PLAYER_POSITIONS = {"unknown": 0, "center": 1, "left": 2, "right": 3, "forward": 4, "backward": 5}
    DOOR_STATES = {"unknown": 0, "closed": 1, "open": 2}
    ENEMY_TYPES = {"none": 0, "weak": 1, "strong": 2, "boss": 3}
    HEALTH_STATES = {"critical": 0, "low": 1, "medium": 2, "high": 3, "full": 4}
    ACTION_STATES = {"none": 0, "moving": 1, "shooting": 2, "jumping": 3, "interacting": 4}

class MetadataToSignalEncoder:
    def __init__(self):
        pass

    def encode_to_packet(self, metadata_packet):
        packet = 0
        # Encode player position
        position_code = SymbolicStates.PLAYER_POSITIONS.get(metadata_packet['player_position'], 0)
        packet |= position_code << 26  # 6 bits for player position

        # Encode door state
        door_code = SymbolicStates.DOOR_STATES.get(metadata_packet['door_state'], 0)
        packet |= door_code << 24  # 2 bits for door state

        # Encode enemy type
        enemy_code = SymbolicStates.ENEMY_TYPES.get(metadata_packet['enemy_type'], 0)
        packet |= enemy_code << 22  # 2 bits for enemy type

        # Encode player health
        health_code = SymbolicStates.HEALTH_STATES.get(metadata_packet['player_health'], 0)
        packet |= health_code << 19  # 3 bits for player health

        # Encode player actions
        action_code = SymbolicStates.ACTION_STATES.get(metadata_packet['player_action'], 0)
        packet |= action_code << 15  # 4 bits for player action

        # Encode remaining game states (example)
        # Additional game states can be encoded similarly

        return packet

    def extract_parameters(self, packet):
        # Extract specific bits and convert them to parameters for signal processing
        encoded_values = {}
        encoded_values["variability_factor"] = (packet >> 26) & 0x3F  # 6 bits
        encoded_values["variance"] = (packet >> 24) & 0x03  # 2 bits
        encoded_values["std_dev"] = (packet >> 22) & 0x03  # 2 bits
        encoded_values["rms_value"] = (packet >> 19) & 0x07  # 3 bits
        encoded_values["fractal_dimension"] = (packet >> 15) & 0x0F  # 4 bits
        encoded_values["num_peaks"] = (packet >> 12) & 0x07  # 3 bits
        encoded_values["peak_height"] = (packet >> 9) & 0x07  # 3 bits
        encoded_values["window_size"] = (packet >> 6) & 0x07  # 3 bits
        encoded_values["target_rate"] = (packet >> 3) & 0x07  # 3 bits
        encoded_values["arnold_parameter"] = packet & 0x07  # 3 bits
        # Adjust the bit positions and lengths as needed.
        return encoded_values

    def encode_position(self, position):
        # Encode the player's position
        # Assuming position is a string like "center", "left", etc.
        return SymbolicStates.PLAYER_POSITIONS.get(position, 0)

    def encode_walls(self, walls):
        # Encode the number of walls
        # Assuming walls is a list of wall objects or positions
        return min(len(walls), 3)  # Example: Limit to a maximum of 3

    def encode_doors(self, doors):
        # Encode the door state
        # Assuming doors is a list with states like "open" or "closed"
        if not doors:
            return 0  # No doors
        open_doors = sum(door == "open" for door in doors)
        return min(open_doors, 3)  # Example: Limit to a maximum of 3 open doors

    def encode_health(self, health):
        # Encode the player's health
        # Assuming health is a string like "critical", "low", etc.
        return SymbolicStates.HEALTH_STATES.get(health, 0)

    def encode_enemies(self, enemies):
        # Encode the enemy presence/type
        # Assuming enemies is a list of enemy types
        if not enemies:
            return 0  # No enemies
        strongest_enemy = max(enemies, key=lambda e: SymbolicStates.ENEMY_TYPES[e])
        return SymbolicStates.ENEMY_TYPES.get(strongest_enemy, 0)

    def encode_player_actions(self, actions):
        # Encode the player's actions
        # Assuming actions is a dictionary with boolean values for each action
        action_sum = sum(actions.values())
        return min(action_sum, 15)  # Example: Limit to a maximum sum of 15


# Example usage
metadata_packet = {
    "player_position": "center",
    "door_state": "open",
    "enemy_type": "boss",
    "player_health": "medium",
    "player_action": "shooting"
}

encoder = MetadataToSignalEncoder()
packet = encoder.encode_to_packet(metadata_packet)
encoded_values = encoder.extract_parameters(packet)
print(encoded_values)  # Dictionary of parameters for signal processing

# ZeroMQ setup
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5555")  # Publisher binds to port 5555

encoder = MetadataToSignalEncoder()

while True:
    # Generate and encode metadata
    metadata_packet = {
        "player_position": "center",
        "door_state": "open",
        "enemy_type": "boss",
        "player_health": "medium",
        "player_action": "shooting"
    }
    packet = encoder.encode_to_packet(metadata_packet)
    encoded_packet = str(packet)  # Convert packet to string for sending

    publisher.send_string(encoded_packet)
    time.sleep(0.1)  # Publish at 10 Hz (every 100 milliseconds)