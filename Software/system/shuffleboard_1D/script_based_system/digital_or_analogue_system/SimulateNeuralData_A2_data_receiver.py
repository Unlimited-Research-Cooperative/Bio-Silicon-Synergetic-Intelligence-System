import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import mne

logging.basicConfig(level=logging.DEBUG)

# Path to your EDF file
file_path = '/home/vincent/datasets/bio-silicon/sub-01_ses-task_task-game_run-01_ieeg.edf'

# Load the EDF file
raw = mne.io.read_raw_edf(file_path, preload=True, stim_channel=None)

# Electrode names matched to centroids (retrieved from your earlier analysis)
matched_names = ['B21', 'A48', 'B56', 'A5', 'B57', 'B55', 'B4', 'B17', 'B18', 'A46', 'A9', 'A16', 'A18', 'A12', 'A39', 'A43', 'A13', 'B51', 'A38', 'B25', 'B37', 'B36', 'B44', 'B54', 'A34', 'A3', 'A24', 'A31', 'B48', 'B33', 'B40', 'B22']

# Function to generate the corresponding channel names with the "POL" prefix
def generate_pol_channel_name(name):
    if name.startswith('POL'):
        return name
    elif name.startswith('EEG'):
        return f'POL {name[4:]}'
    else:
        return f'POL {name}'  # Assuming other prefixes can be safely prefixed with "POL"

# Adjusted matched names with "POL" prefix
adjusted_matched_names = [generate_pol_channel_name(name) for name in matched_names]

print("Adjusted matched names:", adjusted_matched_names)

# Filter to keep only the indices of channels that are in adjusted_matched_names
indices = [raw.ch_names.index(name) for name in adjusted_matched_names if name in raw.ch_names]

print("Number of channels selected:", len(indices))  # Print the number of selected channels

# Downsample the data to 500 Hz if the original sampling rate is 1000 Hz
if raw.info['sfreq'] == 1000:
    raw.resample(500)

# Extract the downsampled data
selected_data, times = raw[indices, :]

class NEURALVisualiser(QWidget):
    def __init__(self, num_channels, mqtt_client):
        super().__init__()
        self.num_channels = num_channels
        self.data = np.zeros((num_channels, 500))  # Initialize with zeros for 500 samples
        self.ptr = 0
        self.mqtt_client = mqtt_client
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('NEURAL SIGNALS')
        self.setStyleSheet("background-color: black;")
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.plots = []
        self.curves = []  # To store PlotDataItem objects for each curve
        
        num_plots_per_row = 4
        num_rows = int(np.ceil(self.num_channels / num_plots_per_row))
        
        for i in range(num_rows):
            row_layout = QHBoxLayout()
            main_layout.addLayout(row_layout)
            
            for j in range(num_plots_per_row):
                channel_index = i * num_plots_per_row + j
                if channel_index < self.num_channels:
                    plot = pg.PlotWidget()
                    plot.setBackground('k')  # Set plot background to black
                    plot.setTitle(f'{channel_index + 1}', color='#00D8D8')  # Bright turquoise color
                    plot.setMinimumHeight(100)  # Halve plot height
                    plot.setMinimumWidth(200)   # Halve plot width
                    
                    plot.getAxis('left').setPen(pg.mkPen(color='#00D8D8'))  # Set left axis pen color
                    plot.getAxis('bottom').setPen(pg.mkPen(color='#00D8D8'))  # Set bottom axis pen color
                    plot.getAxis('left').setTextPen(pg.mkPen(color='#00D8D8'))  # Set left axis text color
                    plot.getAxis('bottom').setTextPen(pg.mkPen(color='#00D8D8'))  # Set bottom axis text color
                    
                    row_layout.addWidget(plot)
                    self.plots.append(plot)
                    
                    # Initialize PlotDataItem and add to the plot
                    curve = plot.plot(pen=pg.mkPen(color='#00D8D8', width=1))  # Bright turquoise color
                    self.curves.append(curve)
        
        # Adding a window to display live data numerically
        self.data_window = QWidget()
        self.data_window.setWindowTitle('NUMERICAL INCOMING SIGNAL DATA')
        self.data_window.setStyleSheet("background-color: black; color: #00D8D8;")  # Set background to black and text to bright turquoise
        self.data_layout = QGridLayout()
        self.data_labels = []
        
        for i in range(self.num_channels):
            label = QLabel(f'{i+1}: 0.0 uV')
            label.setStyleSheet("color: #00D8D8;")  # Bright turquoise color
            self.data_labels.append(label)
            self.data_layout.addWidget(label, i // 8, i % 8)
        
        self.data_window.setLayout(self.data_layout)
        self.data_window.show()
        
        self.show()

    def update_plot(self, data):
        num_samples = data.shape[1]
        
        if num_samples > 500:
            data = data[:, -500:]  # Ensure data does not exceed 500 samples

        self.data = np.roll(self.data, -num_samples, axis=1)
        self.data[:, -num_samples:] = data
        
        for i in range(self.num_channels):
            self.curves[i].setData(self.data[i])
            self.data_labels[i].setText(f'{i+1}: {data[i, -1]:.2f} uV')

            # Adjust y-axis range dynamically based on the last 500 points for each channel
            min_value = np.min(self.data[i])
            max_value = np.max(self.data[i])
            margin = 0.1 * (max_value - min_value)  # Add 10% margin
            self.plots[i].setYRange(min_value - margin, max_value + margin)
        
        self.ptr += num_samples
        if self.ptr >= self.data.shape[1]:
            self.ptr = self.data.shape[1] - 1

        # Send data over MQTT
        self.send_data_over_mqtt(data)
        
    def send_data_over_mqtt(self, data):
        payload = json.dumps(data.tolist())  # Convert the numpy array to a list and then to a JSON string
        self.mqtt_client.publish("INCOMING NEURAL SIGNALS", payload)
        
    def closeEvent(self, event):
        self.timer.stop()  # Stop the QTimer
        event.accept()

class DataReader:
    def __init__(self, visualizer):
        self.visualizer = visualizer
        self.data = selected_data
        self.sampling_rate = raw.info['sfreq']
        self.chunk_size = int(self.sampling_rate * 0.25)  # 250ms of data
        self.current_idx = 0
    
    def start(self):
        logging.debug("Starting simulated data stream")
        
        self.visualizer.timer = QTimer()
        self.visualizer.timer.timeout.connect(self.update_data)
        self.visualizer.timer.start(250)  # Update data every 250 milliseconds (4Hz)
        
    def update_data(self):
        logging.debug(f"Updating data: current_idx = {self.current_idx}, chunk_size = {self.chunk_size}")
        start_idx = self.current_idx
        end_idx = start_idx + self.chunk_size
        if end_idx > self.data.shape[1]:
            end_idx = self.data.shape[1]
            self.current_idx = 0  # Loop back to start for continuous simulation
        data_chunk = self.data[:, start_idx:end_idx]
        self.visualizer.update_plot(data_chunk)
        self.current_idx += self.chunk_size

    def stop(self):
        logging.debug("Stopping simulated data stream")
        self.visualizer.timer.stop()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

if __name__ == '__main__':
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect("localhost", 1883, 60)  # Update with your MQTT broker address if necessary
    mqtt_client.loop_start()
    
    app = QApplication(sys.argv)  # Initialize QApplication instance

    visualizer = NEURALVisualiser(num_channels=32, mqtt_client=mqtt_client)
    
    data_reader = DataReader(visualizer)
    data_reader.start()
    
    # Ensure we stop streaming and release session when closing the application
    app.aboutToQuit.connect(data_reader.stop)
    
    sys.exit(app.exec_())
