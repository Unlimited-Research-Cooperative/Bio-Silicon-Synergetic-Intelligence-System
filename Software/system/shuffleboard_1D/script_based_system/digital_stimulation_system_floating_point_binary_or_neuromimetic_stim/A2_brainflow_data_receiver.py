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
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError

logging.basicConfig(level=logging.DEBUG)

def get_serial_port():
    try:
        for device in os.listdir('/dev'):
            if 'ttyUSB' in device or 'ttyACM' in device or 'stm32-virtual-comport' in device:
                device_path = f'/dev/{device}'
                return device_path
        raise Exception("No STM32 Virtual ComPort tty devices found. Please connect your neural device.")
    except Exception as e:
        logging.error(f"Error finding serial port: {e}")
        sys.exit(1)

params = BrainFlowInputParams()
params.serial_port = get_serial_port()  # Automatically find the correct device node

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
        self.board = None
    
    def start(self):
        try:
            logging.debug("Initializing BoardShim")
            self.board = BoardShim(BoardIds.FREEEEG32_BOARD.value, params)
            logging.debug("Preparing session")
            self.board.prepare_session()
            logging.debug("Starting stream")
            self.board.start_stream()
            
            logging.debug("Streaming data...")
            self.visualizer.timer = QTimer()
            self.visualizer.timer.timeout.connect(self.update_data)
            self.visualizer.timer.start(250)  # Update data every 250 milliseconds (4Hz)
            
        except BrainFlowError as e:
            logging.error(f'BrainFlow error: {e}')

    def update_data(self):
        try:
            data = self.board.get_board_data()  # Get the latest data
            self.visualizer.update_plot(data[:self.visualizer.num_channels])
        except BrainFlowError as e:
            logging.error(f'BrainFlow error: {e}')

    def stop(self):
        if self.board:
            logging.debug("Stopping stream")
            self.board.stop_stream()
            logging.debug("Releasing session")
            self.board.release_session()

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
