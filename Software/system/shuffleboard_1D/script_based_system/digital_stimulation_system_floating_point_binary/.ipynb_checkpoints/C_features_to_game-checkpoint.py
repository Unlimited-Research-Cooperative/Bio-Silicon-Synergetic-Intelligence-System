import paho.mqtt.client as mqtt
import json
import time
import zmq

class FeaturesToGameAction:
    def __init__(self, pub_socket):
        self.pub_socket = pub_socket  # Publisher socket for ZMQ

        # Adjusted feature-to-action mappings for 1D shuffleboard
        self.feature_to_action_map = {
            'variance': ('adjust_force', 0.2),
            'std_dev': ('fine_tune_force', 0.1),
            'rms': ('execute_shot', 0.5),
            'peak_counts': ('retry_shot', 3),
        }

    def decode_signal_features(self, feature, value):
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
        # Convert action to a JSON string and publish via ZMQ
        action_message = json.dumps({"action": action})
        self.pub_socket.send_string(action_message)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("analyzed_neural_data")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        analyzed_data = json.loads(payload)
        # Process each feature in the analyzed data
        for feature, value in analyzed_data.items():
            action = userdata.decode_signal_features(feature, value)
            if action:
                userdata.process_actions(action)
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5446")

    features_to_action = FeaturesToGameAction(publisher)

    # Set up MQTT client
    mqtt_client = mqtt.Client(userdata=features_to_action)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1 / 10)  # Ensure consistent processing rate
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
