import sys
import json
import time
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel

class FeaturesToGameAction(QWidget):
    def __init__(self, mqtt_client, selected_channels=None):
        super().__init__()
        self.mqtt_client = mqtt_client  # MQTT client for publishing actions
        self.selected_channels = selected_channels if selected_channels else list(range(32))  # Default to all 32 channels

        # To store previous values for comparison
        self.previous_values = {
            'variance': None, 'std_dev': None, 'rms': None, 'peak_count': None,
            'average_peak_height': None, 'average_distance': None, 'average_prominence': None,
            'beta_band_power': None, 'centroids': None, 'spectral_edge_densities': None,
            'higuchi_fractal_dimension': None, 'zero_crossing_rate': None,
            'magnitudes_diff_mean': None, 'magnitudes_diff_std': None,
            'cumulative_sums_diff_mean': None, 'cumulative_sums_diff_std': None,
            'log_means_diff_mean': None, 'log_means_diff_std': None,
            'analytic_signals_diff_mean': None, 'analytic_signals_diff_std': None,
            'envelopes_diff_mean': None, 'envelopes_diff_std': None,
            'derivatives_diff_mean': None, 'derivatives_diff_std': None
        }

        # Setup UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Features to Actions')
        self.setStyleSheet("background-color: black; color: #00D8D8;")

        self.results_table = QTableWidget()
        self.results_table.setRowCount(len(self.previous_values))
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(['Feature', 'Value', 'Action'])
        self.results_table.setStyleSheet("background-color: black; color: #00D8D8;")

        # Adjust column widths
        self.results_table.setColumnWidth(0, 200)  # Feature column
        self.results_table.setColumnWidth(1, 300)  # Value column
        self.results_table.setColumnWidth(2, 300)  # Action column, increased the width

        self.total_force_label = QLabel("Total Force Adjustment: 0")
        self.total_force_label.setStyleSheet("color: #00D8D8; font-size: 16px;")

        layout = QVBoxLayout()
        layout.addWidget(self.results_table)
        layout.addWidget(self.total_force_label)
        self.setLayout(layout)

        self.show()

    def decode_signal_features(self, feature, value):
        """
        Translate the decoded signal feature into a game action
        based on whether the feature value has increased or decreased.
        """
        previous_value = self.previous_values.get(feature)
        if previous_value is None:
            self.previous_values[feature] = value
            return 'maintain_force', 0
        
        force_adjustment = 0
        adjustment_map = {
            'variance': -1, 'std_dev': -1, 'rms': -1, 'peak_count': -1,
            'average_peak_height': 1, 'average_distance': -1, 'average_prominence': -1,
            'beta_band_power': -1, 'centroids': 1, 'spectral_edge_densities': -1,
            'higuchi_fractal_dimension': 1, 'zero_crossing_rate': -1,
            'magnitudes_diff_mean': -1, 'magnitudes_diff_std': -1,
            'cumulative_sums_diff_mean': 1, 'cumulative_sums_diff_std': 1,
            'log_means_diff_mean': 1, 'log_means_diff_std': -1,
            'analytic_signals_diff_mean': 1, 'analytic_signals_diff_std': 1,
            'envelopes_diff_mean': 1, 'envelopes_diff_std': -1,
            'derivatives_diff_mean': 1, 'derivatives_diff_std': 1
        }

        adjustment_factor = adjustment_map.get(feature, 0)
        if value > previous_value:
            force_adjustment += adjustment_factor
        elif value < previous_value:
            force_adjustment -= adjustment_factor

        self.previous_values[feature] = value
        return 'adjust_force', force_adjustment

    def normalize_force_adjustment(self, total_force_adjustment, num_features):
        # Scale to the range of -5 to 5
        max_force_adjustment = num_features
        scaled_adjustment = (total_force_adjustment / max_force_adjustment) * 5



        return scaled_adjustment

    def process_actions(self, total_force_adjustment):
        normalized_adjustment = self.normalize_force_adjustment(total_force_adjustment, len(self.previous_values))
        print(f"Total force adjustment: {normalized_adjustment}")
        # Convert action to a JSON string and publish via MQTT
        action_message = json.dumps({"action": "adjust_force", "force_adjustment": normalized_adjustment})
        self.mqtt_client.publish("GAME ACTIONS", action_message)
        self.total_force_label.setText(f"Total Force Adjustment: {normalized_adjustment:.2f}")

    def update_results(self, feature, value, action, force_adjustment):
        row = list(self.previous_values.keys()).index(feature)
        display_value = f"{value:.4f}"  # Format the value to 4 decimal places
        self.results_table.setItem(row, 0, QTableWidgetItem(feature))
        self.results_table.setItem(row, 1, QTableWidgetItem(display_value))
        self.results_table.setItem(row, 2, QTableWidgetItem(f"{action} ({force_adjustment})"))

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("EXTRACTED FEATURES")

def on_message(client, userdata, message):
    try:
        payload = message.payload.decode('utf-8')
        analyzed_data = json.loads(payload)

        # List of features to process
        features_of_interest = [
            'variance', 'std_dev', 'rms', 'peak_count', 'average_peak_height',
            'average_distance', 'average_prominence', 'beta_band_power', 'centroids', 'spectral_edge_densities',
            'higuchi_fractal_dimension', 'zero_crossing_rate', 'magnitudes_diff_mean',
            'magnitudes_diff_std', 'cumulative_sums_diff_mean', 'cumulative_sums_diff_std',
            'log_means_diff_mean', 'log_means_diff_std', 'analytic_signals_diff_mean',
            'analytic_signals_diff_std', 'envelopes_diff_mean', 'envelopes_diff_std',
            'derivatives_diff_mean', 'derivatives_diff_std'
        ]
        filtered_data = {feature: analyzed_data[feature] for feature in features_of_interest if feature in analyzed_data}

        # Process each feature for the selected channels
        total_force_adjustment = 0
        for feature, values in filtered_data.items():
            for channel in userdata.selected_channels:
                value = values[channel]
                action, force_adjustment = userdata.decode_signal_features(feature, value)
                total_force_adjustment += force_adjustment
                userdata.update_results(feature, value, action, force_adjustment)

        # Perform the action with the total force adjustment
        if total_force_adjustment != 0:
            userdata.process_actions(total_force_adjustment)
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
