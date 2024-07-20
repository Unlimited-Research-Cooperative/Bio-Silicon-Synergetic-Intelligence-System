import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from datetime import datetime
import pyqtgraph.exporters

logging.basicConfig(level=logging.DEBUG)

# Directory to save the historic data files
output_dir = "/home/vincent/MySSD/JupyterProjects/AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/Bio-Silicon-Synergetic-Intelligence-System/Software/system/shuffleboard_1D/script_based_system/digital_or_analogue_system/sessions"

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

rounds = []
distances_to_target = []
player_forces = []
improvement_rates = []
extracted_features_list = []

closer_plays = 0
further_plays = 0

def calculate_improvement_rate():
    if len(distances_to_target) < 2:
        return 0
    return (distances_to_target[-2] - distances_to_target[-1]) / distances_to_target[-2]

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("historic_data")
    client.subscribe("EXTRACTED FEATURES")

def on_message(client, userdata, msg):
    global closer_plays, further_plays

    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic

        if topic == "historic_data":
            historic_data = json.loads(payload)

            print(f"Processing {len(historic_data['history'])} historic data entries.")

            for entry in historic_data['history']:
                rounds.append(entry['round'])
                distances_to_target.append(entry['distance_to_target'])
                player_forces.append(entry['player_force'])
                improvement_rates.append(calculate_improvement_rate())

                if entry['distance_to_target'] < entry['player_force']:
                    closer_plays += 1
                else:
                    further_plays += 1

            print(f"Total rounds: {len(rounds)}")
            print(f"Total distances: {len(distances_to_target)}")
            print(f"Total player forces: {len(player_forces)}")
            print(f"Total improvement rates: {len(improvement_rates)}")
            print(f"Total closer plays: {closer_plays}")
            print(f"Total further plays: {further_plays}")

        elif topic == "EXTRACTED FEATURES":
            extracted_features = json.loads(payload)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extracted_features_with_timestamp = {
                "timestamp": timestamp,
                "features": extracted_features
            }
            extracted_features_list.append(extracted_features_with_timestamp)
            print(f"Total extracted features: {len(extracted_features_list)}")

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

        self.distance_force_plot = self.plot_widget.addPlot(title="Distance to Target and Player Force over Time")
        self.distance_force_plot.setLabel('left', 'Values')
        self.distance_force_plot.setLabel('bottom', 'Round')
        self.distance_force_plot.addLegend()

        self.distance_curve = self.distance_force_plot.plot(pen=pg.mkPen(color='#00D8D8', width=2), name="Distance to Target")
        self.force_curve = self.distance_force_plot.plot(pen=pg.mkPen(color='r', width=2), name="Player Force")

        self.plot_widget.nextRow()

        self.improvement_plot = self.plot_widget.addPlot(title="Improvement Rate over Time")
        self.improvement_plot.setLabel('left', 'Improvement Rate')
        self.improvement_plot.setLabel('bottom', 'Round')
        self.improvement_plot.addLegend()

        self.improvement_curve = self.improvement_plot.plot(pen=pg.mkPen(color='g', width=2), name="Improvement Rate")

        self.plot_widget.nextRow()

        self.play_count_plot = self.plot_widget.addPlot(title="Closer vs Further Plays")
        self.play_count_plot.setLabel('left', 'Count')
        self.play_count_plot.setLabel('bottom', 'Type')
        self.play_count_plot.addLegend()

        x_ticks = [(1, "Closer"), (2, "Further")]
        self.play_count_plot.getAxis('bottom').setTicks([x_ticks])

        self.play_count_bar = pg.BarGraphItem(x=[1, 2], height=[closer_plays, further_plays], width=0.6, brush='b')
        self.play_count_plot.addItem(self.play_count_bar)

        self.show()

    def update_plots(self):
        self.distance_curve.setData(rounds, distances_to_target)
        self.force_curve.setData(rounds, player_forces)
        self.improvement_curve.setData(rounds, improvement_rates)

        self.play_count_bar.setOpts(height=[closer_plays, further_plays])

    def closeEvent(self, event):
        timestamp = datetime.now().strftime("experiment_date_%d_%m_%Y_time_%H_%M_%S")
        data_filename = os.path.join(output_dir, f"{timestamp}_data.npz")
        plot_filename = os.path.join(output_dir, f"{timestamp}_plots.png")

        try:
            print(f"Saving data with {len(rounds)} rounds, {len(distances_to_target)} distances, and {len(player_forces)} forces.")
            # Save the data
            np.savez(data_filename, rounds=rounds, distances_to_target=distances_to_target, 
                     player_forces=player_forces, improvement_rates=improvement_rates, 
                     closer_plays=closer_plays, further_plays=further_plays, 
                     extracted_features_list=extracted_features_list)

            # Save the plot
            exporter = pg.exporters.ImageExporter(self.plot_widget.scene())
            exporter.export(plot_filename)
            print(f"Saved final plot to {plot_filename}")
            print(f"Saved session data to {data_filename}")
        except Exception as e:
            print(f"Error saving files: {e}")

        super().closeEvent(event)

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
