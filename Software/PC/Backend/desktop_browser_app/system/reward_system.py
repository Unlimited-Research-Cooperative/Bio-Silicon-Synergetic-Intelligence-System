import serial
import sqlite3
import numpy as np
from threading import Thread
from playsound import playsound
from data_manager import DataManager
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class FeedBackSystem:
    def __init__(self, port: str):
        self.reward_sound = "./sounds/reward.mp3"
        self.distress_sound = "./sounds/distress.mp3"

        self.serial_port = serial.Serial(port)

    def process_feedback(self, game_event):
        if game_event in ['killed_enemy', 'found_item', 'won']:
            playsound(self.reward_sound)
            self.serial_port.write(b'1')  # 1 for open and 0 for close

        elif game_event in ["wrong_direction", "got_shot", "died", "stuck_in_loop"]:
            playsound(self.distress_sound)
            playsound(self.distress_sound)
            self.serial_port.write(b'0')

        self.serial_port.close()


class ActionLogger:
    def __init__(self):
        self.connection = sqlite3.connect('action logs.db')
        self.cursor = self.connection.cursor()

    def log_action(self, context: str, action: str, success: str):
        data = (success, context, action)  # Tuple for a single insert
        self.cursor.execute('INSERT INTO ACTIONS VALUES (?, ?, ?)', data)
        self.connection.commit()

    # def get_action_success_rate(self, action):
    #     if action not in self.action_log or not self.action_log[action]:
    #         return 0
    #     successes = [entry['success'] for entry in self.action_log[action]]
    #     return sum(successes) / len(successes)


class NeuralMappingVisualizer:
    def __init__(self, signal_listener: DataManager):
        self.fig, self.ax = plt.subplots()
        self.quality_scores = np.zeros(32)
        self.signal_listener = signal_listener

        self.set_labels()

    def set_labels(self):
        self.ax.set_ylim(0, 1)
        self.ax.set_title('Mapping Quality Scores')
        self.ax.set_xlabel('Channel')
        self.ax.set_ylabel('Quality Score')

    def update_plot(self):
        # Update the plot with new data
        neural_data = self.signal_listener.listen()
        # actions = self.processor.process_signals(neural_data)
        # self.quality_scores = self.processor.assess_mapping_quality(neural_data, actions)
        self.ax.clear()
        self.ax.bar(range(32), self.quality_scores)
        self.set_labels()

    def animate(self):
        animation = FuncAnimation(self.fig, func=self.update_plot, interval=100)
        plt.show()

    def visualize(self):  # Run on new thread. This will not block the main thread
        thread = Thread(target=self.animate)
        thread.start()
