import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
import pyqtgraph as pg

logging.basicConfig(level=logging.DEBUG)

class SignalGeneratorVisualiser(QWidget):
    def __init__(self, num_channels, mqtt_client):
        super().__init__()
        self.num_channels = num_channels
        self.sample_size = 1000  # Display 1000 samples at a time
        self.data = [np.zeros(self.sample_size) for _ in range(num_channels)]  # Initialize with zeros
        self.mqtt_client = mqtt_client
        
        self.init_ui()
        self.subscribe_mqtt()
        
    def init_ui(self):
        self.setWindowTitle('GENERATED NEUROMIMETIC SIGNALS')
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
                    plot.setTitle(f'Channel {channel_index + 1}', color='#00D8D8')  # Bright turquoise color
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
        
        self.show()
    
    def subscribe_mqtt(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("localhost", 1883, 60)  # Update with your MQTT broker address if necessary
        self.mqtt_client.subscribe("ANALOGUE DATA")  # Subscribe to the ANALOGUE DATA topic
        self.mqtt_client.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        logging.debug(f"Connected with result code {str(rc)}")
    
    def on_message(self, client, userdata, msg):
        try:
            decoded_payload = msg.payload.decode()
            logging.debug(f"Received MQTT message: {decoded_payload}")
            
            data = json.loads(decoded_payload).get('signals')
            
            if not isinstance(data, list):
                logging.warning("Received non-list data. Ignoring message.")
                return
            
            for i, channel_data in enumerate(data):
                if not isinstance(channel_data, list):
                    logging.warning(f"Received non-list data for channel {i+1}. Ignoring channel.")
                    continue
                
                num_samples = len(channel_data)
                
                # Update plot and numerical display for the channel
                self.update_plot(i, channel_data)
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {str(e)}")
        except Exception as e:
            logging.error(f"Error processing message: {str(e)}")
    
    def update_plot(self, channel_index, channel_data):
        self.data[channel_index] = np.roll(self.data[channel_index], -len(channel_data))
        self.data[channel_index][-len(channel_data):] = channel_data
        self.curves[channel_index].setData(self.data[channel_index])
        
        # Adjust y-axis range dynamically based on the data range
        min_value = np.min(self.data[channel_index])
        max_value = np.max(self.data[channel_index])
        margin = 0.1 * (max_value - min_value)  # Add 10% margin
        self.plots[channel_index].setYRange(min_value - margin, max_value + margin)

    def closeEvent(self, event):
        self.mqtt_client.disconnect()
        event.accept()

if __name__ == '__main__':
    mqtt_client = mqtt.Client()
    
    app = QApplication(sys.argv)  # Initialize QApplication instance

    visualizer = SignalGeneratorVisualiser(num_channels=4, mqtt_client=mqtt_client)
    
    sys.exit(app.exec_())
