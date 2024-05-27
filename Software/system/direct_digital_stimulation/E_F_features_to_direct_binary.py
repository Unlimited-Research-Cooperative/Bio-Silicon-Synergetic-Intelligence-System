import zmq
import time
import json
import numpy as np

def generate_digital_data(features, total_bits=16):
    digital_data_combined = []
    for feature_value in features:
        # Convert each feature value directly to binary strings
        binary_feature = format(int(feature_value), f'0{total_bits}b')
        # Convert binary strings to list of integers (0 or 1) for digital signal representation
        digital_data_feature = [int(bit) for bit in binary_feature]
        # Append the binary data to the combined list
        digital_data_combined.extend(digital_data_feature)
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
            
            # Assume game_state is a list of numerical features
            features = game_state.get('features', [])
            
            # Generate the digital data for all features in the game state
            digital_data = generate_digital_data(features)
            
            # Publish the digital data
            publisher.send_pyobj(digital_data)
            
        except zmq.Again:
            # No message received yet
            pass

        # Sleep for 0.25 seconds to maintain a 4Hz update rate
        time.sleep(0.25)

if __name__ == "__main__":
    main()
