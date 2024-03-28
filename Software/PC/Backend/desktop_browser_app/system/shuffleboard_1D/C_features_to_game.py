import zmq
import time
import json  # Import JSON for encoding messages

class FeaturesToGameAction:
    def __init__(self, pub_socket):
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:5445")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.retry_interval = 1 / 10  # Retry interval to attempt receiving at 10Hz update rate
        self.pub_socket = pub_socket  # Publisher socket

        # Adjusted feature-to-action mappings for 1D shuffleboard
        self.feature_to_action_map = {
            'variance': ('adjust_force', 0.2),
            'std_dev': ('fine_tune_force', 0.1),
            'rms': ('execute_shot', 0.5),
            'peak_counts': ('retry_shot', 3),
        }

    def decode_signal_features(self):
        while True:
            try:
                message = self.sub_socket.recv_string(flags=zmq.NOBLOCK)
                feature, value = message.split(':')  # Assuming message format "feature:value"
                value = float(value)
                return self.translate_features_to_action(feature, value)
            except zmq.Again:
                time.sleep(self.retry_interval)  # Wait before retrying
                continue
            except ValueError:
                print("Error decoding feature value")
                return None

    def translate_features_to_action(self, feature, value):
        """
        Translate the decoded signal feature into a game action,
        using the feature_to_action_map.
        """
        if feature in self.feature_to_action_map:
            action, threshold = self.feature_to_action_map[feature]
            if value > threshold:
                return action
        return 'maintain_force'

    def process_actions(self, action):
        print(f"Action to perform: {action}")
        # Convert action to a JSON string and publish
        action_message = json.dumps({"action": action})
        self.pub_socket.send_string(action_message)

def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5446")

    features_to_action = FeaturesToGameAction(publisher)
    
    while True:
        action = features_to_action.decode_signal_features()
        if action:
            features_to_action.process_actions(action)
            time.sleep(1 / 10)  # Ensure consistent processing rate

if __name__ == "__main__":
    main()
