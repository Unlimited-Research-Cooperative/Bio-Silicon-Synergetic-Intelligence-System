import sys
import json
import logging
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

logging.basicConfig(level=logging.DEBUG)

# Initialize player force
player_force = 80
target_location = 100  # Define the target location

rounds = []
distances_to_target = []
adjusted_forces = []

# MQTT topic for publishing metadata
metadata_topic = "metadata"

def calculate_distance_to_target(player_force):
    """
    Calculate the distance from the puck location (player force) to the target location.
    """
    return abs(target_location - player_force)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("historic_data")
    client.subscribe("GAME ACTIONS")  # Subscribe to the GAME ACTIONS topic

def on_message(client, userdata, msg):
    global player_force

    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic

        if topic == "historic_data":
            historic_data = json.loads(payload)
            
            print(f"Processing {len(historic_data['history'])} historic data entries.")

            for entry in historic_data['history']:
                rounds.append(entry['round'])
                player_force = entry['player_force']
                distance_to_target = calculate_distance_to_target(player_force)
                distances_to_target.append(distance_to_target)
                adjusted_forces.append(entry['adjusted_force'])

                # Publish the metadata for each entry
                metadata = {
                    "distance_to_target": distance_to_target,
                    "adjusted_force": entry['adjusted_force'],
                    "player_force": player_force
                }
                client.publish(metadata_topic, json.dumps(metadata))
                print(f"Published metadata: {metadata}")
            
            print(f"Total rounds: {len(rounds)}")
            print(f"Total distances: {len(distances_to_target)}")
            print(f"Total adjusted forces: {len(adjusted_forces)}")

        elif topic == "GAME ACTIONS":
            action_data = json.loads(payload)
            if action_data.get("action") == "adjust_force":
                adjusted_force = action_data.get("force_adjustment", 0)
                player_force += adjusted_force
                distance_to_target = calculate_distance_to_target(player_force)
                distances_to_target.append(distance_to_target)
                adjusted_forces.append(adjusted_force)

                # Publish the metadata for each entry
                metadata = {
                    "distance_to_target": distance_to_target,
                    "adjusted_force": adjusted_force,
                    "player_force": player_force
                }
                client.publish(metadata_topic, json.dumps(metadata))
                print(f"Player force: {player_force}, Adjusted force: {adjusted_force}, Distance to target: {distance_to_target}")

    except Exception as e:
        print(f"Error processing message: {e}")

class ShuffleboardVisualizer(QWidget):
    def __init__(self, mqtt_client):
        super().__init__()
        self.mqtt_client = mqtt_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Shuffleboard Game Live Visualization')
        self.setStyleSheet("background-color: black; color: #00D8D8;")

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.plot_widget = pg.GraphicsLayoutWidget()
        layout.addWidget(self.plot_widget)

        self.distance_plot = self.plot_widget.addPlot(title="Distance to Target and Adjusted Force over Time")
        self.distance_plot.setLabel('left', 'Value', color='#00D8D8')
        self.distance_plot.setLabel('bottom', 'Time', color='#00D8D8')
        self.distance_plot.getAxis('left').setPen(pg.mkPen(color='#00D8D8'))
        self.distance_plot.getAxis('bottom').setPen(pg.mkPen(color='#00D8D8'))
        self.distance_plot.getAxis('left').setTextPen(pg.mkPen(color='#00D8D8'))
        self.distance_plot.getAxis('bottom').setTextPen(pg.mkPen(color='#00D8D8'))
        
        self.distance_curve = self.distance_plot.plot(pen=pg.mkPen(color='#00D8D8', width=2), name="Distance to Target")
        self.adjusted_force_curve = self.distance_plot.plot(pen=pg.mkPen(color='#D800D8', width=2), name="Adjusted Force")

        # Add legend
        self.legend = self.distance_plot.addLegend(labelTextColor='#00D8D8')
        self.legend.addItem(self.distance_curve, "Distance to Target")
        self.legend.addItem(self.adjusted_force_curve, "Adjusted Force")

        self.show()

    def update_plots(self):
        self.distance_curve.setData(list(range(len(distances_to_target))), distances_to_target)
        self.adjusted_force_curve.setData(list(range(len(adjusted_forces))), adjusted_forces)

def main():
    app = QApplication(sys.argv)
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)

    visualizer = ShuffleboardVisualizer(mqtt_client)

    timer = QTimer()
    timer.timeout.connect(visualizer.update_plots)
    timer.start(1000)  # Update plots every second

    mqtt_client.loop_start()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
