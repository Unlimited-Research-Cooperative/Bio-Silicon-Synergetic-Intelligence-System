import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt
import time
import pyaudio
import threading
from scipy.signal import butter, lfilter

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
AMPLITUDE = 32767  # Max value for 16-bit audio
OUTPUT_SAMPLE_RATE = 48000  # Common sample rate for audio playback
BUFFER_SIZE = int(OUTPUT_SAMPLE_RATE * PACKET_DURATION)  # Number of samples per packet
RING_BUFFER_SIZE = BUFFER_SIZE * 8  # Larger buffer for more continuous playback

# PyAudio device indices for the output channels
pyaudio_devices = [18, 19, 20, 21]  # Replace with actual indices if needed

# Global variable to store the latest digital waveform for visualization
latest_waveform = None

# Ring buffers for audio playback
ring_buffers = [np.zeros(RING_BUFFER_SIZE, dtype=np.float32) for _ in range(NUM_CHANNELS)]
ring_buffer_write_positions = [0 for _ in range(NUM_CHANNELS)]
lock = threading.Lock()

# Low-pass filter parameters
CUTOFF_FREQ = 1000  # Cutoff frequency in Hz
NYQUIST_RATE = OUTPUT_SAMPLE_RATE / 2.0
NORMAL_CUTOFF = CUTOFF_FREQ / NYQUIST_RATE
b, a = butter(5, NORMAL_CUTOFF, btype='low', analog=False)

# Function to apply low-pass filter
def low_pass_filter(data, b, a):
    return lfilter(b, a, data)

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
        
        # Check the incoming digital data length
        print(f"Incoming digital data length: {len(digital_data)}")
        
        # Convert digital data (list of lists) to a NumPy array for each channel
        digital_waveform = [np.array([1 if bit == 150 else -1 for bit in signal], dtype=np.float32) for signal in digital_data]
        
        # Store the latest waveform for visualization
        with lock:
            latest_waveform = np.array(digital_waveform)
        
        # Apply low-pass filter to waveform data
        for i in range(NUM_CHANNELS):
            digital_waveform[i] = low_pass_filter(digital_waveform[i], b, a)
        
        # Debug print for the converted digital waveform
        print(f"Converted digital waveform (first 5 points for each channel):")
        for i, waveform in enumerate(digital_waveform):
            print(f"Channel {i} first 5 data points: {waveform[:5]}")
            print(f"Channel {i} - Min: {waveform.min()}, Max: {waveform.max()}")
        
        # Update ring buffers
        with lock:
            for i in range(NUM_CHANNELS):
                write_pos = ring_buffer_write_positions[i]
                to_write = np.tile(digital_waveform[i], BUFFER_SIZE // len(digital_waveform[i]))
                available_space = RING_BUFFER_SIZE - write_pos
                if len(to_write) > available_space:
                    ring_buffers[i][write_pos:] = to_write[:available_space]
                    ring_buffers[i][:len(to_write) - available_space] = to_write[available_space:]
                else:
                    ring_buffers[i][write_pos:write_pos + len(to_write)] = to_write
                ring_buffer_write_positions[i] = (write_pos + len(to_write)) % RING_BUFFER_SIZE

    except Exception as e:
        print(f"Error processing message: {e}")

def audio_callback_factory(channel):
    def audio_callback(in_data, frame_count, time_info, status):
        global ring_buffers, ring_buffer_write_positions, lock
        
        with lock:
            start_pos = ring_buffer_write_positions[channel]
            end_pos = start_pos + frame_count
            
            if end_pos <= RING_BUFFER_SIZE:
                chunk = ring_buffers[channel][start_pos:end_pos]
            else:
                chunk = np.concatenate((ring_buffers[channel][start_pos:], ring_buffers[channel][:end_pos % RING_BUFFER_SIZE]))

            ring_buffer_write_positions[channel] = end_pos % RING_BUFFER_SIZE
        
        int_waveform = (chunk * AMPLITUDE).astype(np.int16)
        
        # Logging to confirm each device is playing the respective channel signal
        print(f"Device {pyaudio_devices[channel]} playing channel {channel} data: {int_waveform[:10]}")

        return (int_waveform.tobytes(), pyaudio.paContinue)
    return audio_callback

class DigitalSignalVisualizer(QWidget):
    def __init__(self, num_channels, mqtt_client):
        super().__init__()
        self.num_channels = num_channels
        self.data = [np.zeros(500) for _ in range(num_channels)]  # Initialize with zeros for 500 samples per channel
        self.ptr = 0
        self.mqtt_client = mqtt_client
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('DIGITAL SIGNAL VISUALIZER')
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
            with lock:
                for i in range(self.num_channels):
                    self.data[i] = np.roll(self.data[i], -len(latest_waveform[i]))
                    self.data[i][-len(latest_waveform[i]):] = latest_waveform[i]
                    self.curves[i].setData(self.data[i])

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    # Set up audio streams with callback
    p = pyaudio.PyAudio()
    streams = []
    
    for i, device_index in enumerate(pyaudio_devices):
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=OUTPUT_SAMPLE_RATE,
                            output=True,
                            output_device_index=device_index,
                            stream_callback=audio_callback_factory(i))
            streams.append(stream)
            stream.start_stream()
        except IOError as e:
            print(f"Could not open audio stream for device {device_index}: {e}")

    app = QApplication(sys.argv)
    visualizer = DigitalSignalVisualizer(NUM_CHANNELS, mqtt_client)
    app.exec_()
    
    for stream in streams:
        stream.stop_stream()
        stream.close()
    p.terminate()

if __name__ == "__main__":
    main()
