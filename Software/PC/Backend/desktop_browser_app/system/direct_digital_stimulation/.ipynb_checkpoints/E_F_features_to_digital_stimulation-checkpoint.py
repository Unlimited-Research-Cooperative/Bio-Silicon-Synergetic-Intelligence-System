import zmq
import time
import json
import numpy as np

def generate_digital_data(target_distance, target_force):
    # Convert the raw values directly to binary strings.
    binary_distance = format(target_distance, '016b')  # Using 16 bits as an example
    binary_force = format(target_force, '016b')  # Using 16 bits as an example
    
    # Convert binary strings to list of integers (0 or 1) for digital signal representation
    digital_data_distance = [int(bit) for bit in binary_distance]
    digital_data_force = [int(bit) for bit in binary_force]
    
    # Combining the digital data for distance and force into one signal if necessary
    digital_data_combined = digital_data_distance + digital_data_force
    
    return digital_data_combined

def main():
    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5557")
    
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5555")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")
    
    while True:
        try:
            # Wait for an incoming message containing game state
            message = subscriber.recv_string(zmq.NOBLOCK)
            game_state = json.loads(message)
            
            # Extracting 'distance_to_target' and 'player_force' from the game state
            target_distance = game_state.get('distance_to_target', 0)  # Providing default values in case keys are missing
            target_force = game_state.get('player_force', 0)
            
            # Generate the digital data
            digital_data = generate_digital_data(target_distance, target_force)
            
            # Publish the digital data
            publisher.send_pyobj(digital_data)
            
        except zmq.Again:
            # No message received yet
            time.sleep(0.1)  # Sleep briefly to maintain a 10Hz update rate
            continue

if __name__ == "__main__":
    main()
