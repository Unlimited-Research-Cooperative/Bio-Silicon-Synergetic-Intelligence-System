import sys
import json
import numpy as np
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

# Constants
NUM_CHANNELS = 32
UPDATE_RATE = 250  # Update rate in milliseconds (4 Hz)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_OUTPUT_TOPIC = "EXTRACTED FEATURES"

# Global variable to store received features
features_data = {}

# MQTT callback when a message is received
def on_message(client, userdata, msg):
    global features_data
    try:
        decoded_payload = msg.payload.decode()
        data = json.loads(decoded_payload)
        features_data = data
        print(f"Received data: {data}")  # Debugging: Print received data
    except Exception as e:
        print(f"Error processing message: {e}")

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_OUTPUT_TOPIC)
mqtt_client.loop_start()

class FeatureVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EEG Data Visualization')

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Create a plot for the spectrogram
        self.spectrogram_plot = pg.PlotWidget(title="Composite Spectrogram")
        self.layout.addWidget(self.spectrogram_plot)
        self.spectrogram_img = pg.ImageItem()
        self.spectrogram_plot.addItem(self.spectrogram_img)
        self.spectrogram_plot.getAxis('left').setLabel('Frequency (Hz)')
        self.spectrogram_plot.getAxis('bottom').setLabel('Time (s)')
        self.spectrogram_plot.setXRange(0, NUM_CHANNELS)
        self.spectrogram_plot.setYRange(0, 3)  # Adjusted for 3 feature types

        # Setup a timer to update the plots
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(UPDATE_RATE)

    def update_plots(self):
        global features_data
        if not features_data:
            print("No features data available")
            return

        try:
            # Check for required feature data
            if 'rms' in features_data and 'centroids' in features_data and 'std_dev' in features_data:
                rms_data = np.array(features_data['rms'])
                centroids_data = np.array(features_data['centroids'])
                std_dev_data = np.array(features_data['std_dev'])

                # Check that data is the correct shape
                if rms_data.shape[0] == NUM_CHANNELS and centroids_data.shape[0] == NUM_CHANNELS and std_dev_data.shape[0] == NUM_CHANNELS:
                    # Create a composite data array
                    composite_data = np.vstack((rms_data, centroids_data, std_dev_data))

                    # Normalize data to the range [0, 1]
                    composite_data -= np.min(composite_data)
                    composite_data /= np.max(composite_data)

                    # Print for debugging
                    print(f"Composite data shape: {composite_data.shape}")
                    print(f"Composite data: {composite_data}")

                    # Use a color map for the spectrogram
                    lut = pg.colormap.get('inferno').getLookupTable()
                    self.spectrogram_img.setImage(composite_data, autoLevels=False, lut=lut, levels=(0, 1))

                    # Set the correct shape for the spectrogram image
                    self.spectrogram_img.setRect(0, 0, composite_data.shape[1], composite_data.shape[0])

        except Exception as e:
            print(f"Error updating plots: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = FeatureVisualizer()
    visualizer.show()
    sys.exit(app.exec_())
