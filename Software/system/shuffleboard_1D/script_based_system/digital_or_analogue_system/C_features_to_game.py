import sys
import json
import time
import paho.mqtt.client as mqtt

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem

class FeaturesToGameAction(QWidget):
    def __init__(self, mqtt_client, selected_channels=None):
        super().__init__()
        self.mqtt_client = mqtt_client  # MQTT client for publishing actions
        self.selected_channels = selected_channels if selected_channels else list(range(32))  # Default to all 32 channels

        # Adjusted feature-to-action mappings for 1D shuffleboard
        self.feature_to_action_map = {
            'variance': ('adjust_force', 0.2),
            'std_dev': ('fine_tune_force', 0.1),
            'rms': ('execute_shot', 0.5),
            'peak_count': ('retry_shot', 3),
        }

        # Setup UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Features to Actions')
        self.setStyleSheet("background-color: black; color: #00D8D8;")

        self.results_table = QTableWidget()
        self.results_table.setRowCount(len(self.feature_to_action_map))
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Feature', 'Value', 'Action'])
        self.results_table.setStyleSheet("background-color: black; color: #00D8D8;")

        # Adjust column widths
        self.results_table.setColumnWidth(0, 150)  # Feature column
        self.results_table.setColumnWidth(1, 150)  # Value column
        self.results_table.setColumnWidth(2, 300)  # Action column, doubled the width

        layout = QVBoxLayout()
        layout.addWidget(self.results_table)
        self.setLayout(layout)

        self.show()

    def decode_signal_features(self, feature, value):
        """
        Translate the decoded signal feature into a game action,
        using the feature_to_action_map.
        """
        if feature in self.feature_to_action_map:
            action, threshold = self.feature_to_action_map[feature]
            if isinstance(value, dict):  # Special handling for peaks
                peak_count = value['peak_count']
                if peak_count > threshold:
                    return action
            else:
                # Handle list or single value comparison
                if isinstance(value, list):
                    avg_value = sum(value) / len(value)
                    if avg_value > threshold:
                        return action
                else:
                    if value > threshold:
                        return action
        return 'maintain_force'

    def process_actions(self, action):
        print(f"Action to perform: {action}")
        # Convert action to a JSON string and publish via MQTT
        action_message = json.dumps({"action": action})
        self.mqtt_client.publish("GAME ACTIONS", action_message)

    def update_results(self, feature, value, action):
        row = list(self.feature_to_action_map.keys()).index(feature)
        display_value = str(value['peak_count']) if isinstance(value, dict) else str(value)
        self.results_table.setItem(row, 0, QTableWidgetItem(feature))
        self.results_table.setItem(row, 1, QTableWidgetItem(display_value))
        self.results_table.setItem(row, 2, QTableWidgetItem(action))

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("EXTRACTED FEATURES")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        analyzed_data = json.loads(payload)

        # Filter out unnecessary features
        features_of_interest = ['variance', 'std_dev', 'rms', 'peaks']
        filtered_data = {feature: analyzed_data[feature] for feature in features_of_interest if feature in analyzed_data}

        # Aggregate feature values for the selected channels
        aggregated_data = {}
        for feature, values in filtered_data.items():
            if feature == 'peaks':
                peak_counts = [values[i]['peak_count'] for i in userdata.selected_channels]
                aggregated_data['peak_count'] = sum(peak_counts) / len(peak_counts)
            else:
                selected_values = [values[i] for i in userdata.selected_channels]
                aggregated_data[feature] = sum(selected_values) / len(selected_values)

        # Process each feature in the aggregated data
        for feature, value in aggregated_data.items():
            action = userdata.decode_signal_features(feature, value)
            if action:
                userdata.process_actions(action)
                userdata.update_results(feature, value, action)
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    app = QApplication(sys.argv)

    features_to_action = FeaturesToGameAction(None)

    # Set up MQTT client
    mqtt_client = mqtt.Client(userdata=features_to_action)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.loop_start()

    features_to_action.mqtt_client = mqtt_client  # Set the mqtt_client after initialization

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
