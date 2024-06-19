import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt
import time
import subprocess

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

logging.basicConfig(level=logging.DEBUG)

# Constants
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "DIGITAL SIGNALS"
PACKET_DURATION = 0.25  # 250 ms packets
BIT_DURATION = 0.0125  # 12.5 ms per bit (for 16 bits in 200 ms)
NUM_CHANNELS = 4

# Global variable to store the latest digital waveform for visualization
latest_waveform = None

# Start the JACK server and connect to USB audio devices
def start_jack():
    # Start JACK server if not already running
    subprocess.Popen(['jackd', '-d', 'alsa', '-d', 'hw:0', '-r', '48000', '-p', '512', '-n', '3', '-S', '-P', '4', '-C', '4'])
    time.sleep(5)  # Wait for JACK to start

    # List of USB audio device symlinks
    usb_devices = ["/dev/USB16_usb2", "/dev/USB16_usb3", "/dev/USB16_usb4", "/dev/USB16_usb5"]

    # Connect JACK ports to USB audio devices
    for i, device in enumerate(usb_devices):
        subprocess.call(['jack_connect', f'system:playback_{i*2+1}', f'{device}:playback_1'])
        subprocess.call(['jack_connect', f'system:playback_{i*2+2}', f'{device}:playback_2'])

# Callback when the client receives a connection acknowledgment from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    global latest_waveform
    try:
        # Decode the message payload
        payload = msg.payload.decode('utf-8')
        
        # Parse the JSON data
        digital_data = json.loads(payload)["stim_signals"]
        
        # Convert digital data (list of lists) to a NumPy array for each channel
        digital_waveform = [np.array([1 if bit == 150 else -1 for bit in signal]) for signal in digital_data]
        
        # Store the latest waveform for visualization
        latest_waveform = digital_waveform
        print(f"Latest waveform: {latest_waveform}")  # Debug statement
        
    except Exception as e:
        print(f"Error processing message: {e}")

class DigitalSignalVisualizer(QWidget):
    def __init__(self, num_channels, mqtt_client):
        super().__init__()
        self.num_channels = num_channels
        self.data = [np.zeros(500) for _ in range(num_channels)]  # Initialize with zeros for 500 samples per channel
        self.ptr = 0
        self.mqtt_client = mqtt_client
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('ANALOGUE SIGNAL VISUALISER')
        self.setStyleSheet("background-color: black;")
        
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.plots = []
        self.curves = []  # To store PlotDataItem objects for each curve
        
        num_plots_per_row = 2
        num_rows = int(np.ceil(self.num_channels / num_plots_per_row))
        
        for i in range(num_rows):
            row_layout = QHBoxLayout()
            main_layout.addLayout(row_layout)
            
            for j in range(num_plots_per_row):
                channel_index = i * num_plots_per_row + j
                if channel_index < self.num_channels:
                    plot = pg.PlotWidget()
                    plot.setBackground('k')  # Set plot background to black
                    plot.setTitle(f'Channel {channel_index + 1}', color='#00D8D8')  # Bright turquoise color
                    plot.setLabel('left', 'Signal Value', color='#00D8D8')
                    plot.setLabel('bottom', 'Sample Index', color='#00D8D8')
                    plot.setMinimumHeight(200)  # Adjust plot height
                    plot.setMinimumWidth(400)   # Adjust plot width
                    
                    plot.getAxis('left').setPen(pg.mkPen(color='#00D8D8'))  # Set left axis pen color
                    plot.getAxis('bottom').setPen(pg.mkPen(color='#00D8D8'))  # Set bottom axis pen color
                    plot.getAxis('left').setTextPen(pg.mkPen(color='#00D8D8'))  # Set left axis text color
                    plot.getAxis('bottom').setTextPen(pg.mkPen(color='#00D8D8'))  # Set bottom axis text color
                    
                    row_layout.addWidget(plot)
                    self.plots.append(plot)
                    
                    # Initialize PlotDataItem and add to the plot
                    curve = plot.plot(pen=pg.mkPen(color='#00D8D8', width=1))  # Bright turquoise color
                    self.curves.append(curve)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        
        self.show()
        
    def update_plot(self):
        global latest_waveform
        if latest_waveform is not None:
            for i in range(self.num_channels):
                self.data[i] = np.roll(self.data[i], -len(latest_waveform[i]))
                self.data[i][-len(latest_waveform[i]):] = latest_waveform[i]
                self.curves[i].setData(self.data[i])
                # Send the data to JACK ports
                self.send_to_jack(i, self.data[i])

    def send_to_jack(self, channel_index, data):
        # Replace with your actual logic to send data to JACK
        # Example: Use subprocess to call an external script that handles JACK communication
        # This is a placeholder
        jack_client = subprocess.Popen(['jack_simple_client', str(channel_index)], stdin=subprocess.PIPE)
        jack_client.stdin.write(data.tobytes())
        jack_client.stdin.close()

def main():
    # Start the JACK server and set up connections
    start_jack()

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    
    app = QApplication(sys.argv)
    visualizer = DigitalSignalVisualizer(num_channels=NUM_CHANNELS, mqtt_client=mqtt_client)
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
