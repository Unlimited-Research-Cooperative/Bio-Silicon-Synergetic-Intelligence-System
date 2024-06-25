import paho.mqtt.client as mqtt
import time
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen

class GameWindow(QWidget):
    def __init__(self, target_distance):
        super().__init__()
        self.target_distance = target_distance
        self.actual_distance = 0
        self.setWindowTitle('Shuffleboard Game')
        self.setGeometry(100, 100, 800, 200)
        self.setStyleSheet("background-color: black; color: #00D8D8;")
        self.distance_label = QLabel(self)
        self.distance_label.setAlignment(Qt.AlignCenter)
        self.distance_label.setStyleSheet("font-size: 18px; color: #00D8D8;")

        layout = QVBoxLayout()
        layout.addWidget(self.distance_label)
        self.setLayout(layout)

    def update_game_state(self, target_distance, actual_distance):
        self.target_distance = target_distance
        self.actual_distance = actual_distance
        self.distance_label.setText(f'Shufflepuck Stopped at: {actual_distance}')
        print(f"Update game state: target_distance={self.target_distance}, actual_distance={self.actual_distance}")  # Debug statement
        self.update()  # Ensures that the paint event is triggered
        self.show()

    def paintEvent(self, event):
        print("Paint event triggered")  # Debug statement
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor('#00D8D8'), 2))

        # Draw horizontal line
        width = self.width()
        height = self.height()
        print(f"Widget dimensions: width={width}, height={height}")  # Debug statement
        painter.drawLine(50, height // 2, width - 50, height // 2)

        # Calculate target and puck positions
        target_x = 50 + int((self.target_distance / 100) * (width - 100))
        puck_x = 50 + int((self.actual_distance / 100) * (width - 100))

        print(f"Target position: {target_x}, Puck position: {puck_x}")  # Debug statement

        # Draw target line
        painter.drawLine(target_x, height // 2 - 10, target_x, height // 2 + 10)

        # Draw shufflepuck position
        painter.drawRect(puck_x - 5, height // 2 - 5, 10, 10)

        # Draw ticks and numbers
        for i in range(11):
            tick_x = 50 + int((i / 10) * (width - 100))
            painter.drawLine(tick_x, height // 2 - 5, tick_x, height // 2 + 5)
            painter.drawText(tick_x - 10, height // 2 + 20, str(i * 10))

class ShuffleboardGame:
    def __init__(self, target_distance, max_rounds=10, performance_threshold=80):
        self.target_distance = target_distance
        self.max_rounds = max_rounds
        self.performance_threshold = performance_threshold
        self.reset_game()

        # MQTT setup for subscribing to actions and publishing metadata and outcomes
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        self.metadata_topic = "metadata"
        self.outcome_topic = "outcome"
        self.historic_data_topic = "historic_data"

        # Initialize game window
        self.game_window = GameWindow(self.target_distance)

    def reset_game(self):
        self.player_force = 10  # Initial force
        self.score = 0
        self.round = 1
        self.history = []
        self.start_time = time.time()
        self.previous_distance_to_target = None  # Initialize previous distance

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("GAME ACTIONS")

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode('utf-8')
            action = json.loads(payload).get("action")
            print(f"Received action: {action}")  # Debug statement
            self.process_action(action)
        except Exception as e:
            print(f"Error processing message: {e}")

    def process_action(self, action):
        if action:
            result = self.apply_action(action)
            if result is not None:
                print(f"Shot executed with distance {result} and force {self.player_force}")
                self.game_window.update_game_state(self.target_distance, result)
            self.publish_metadata()
            metadata = self.generate_metadata()
            print(f"Metadata: {metadata}")  # Debug statement

        if self.round > self.max_rounds or self.score >= self.performance_threshold:
            self.end_game()

    def apply_action(self, action):
        if action == 'adjust_force':
            self.player_force += 5
        elif action == 'fine_tune_force':
            self.player_force += 2
        elif action == 'execute_shot':
            return self.execute_shot()
        elif action == 'retry_shot':
            self.player_force -= 5
        else:
            pass
        return None

    def execute_shot(self):
        actual_distance = self.player_force
        self.update_state(actual_distance)
        return actual_distance

    def update_state(self, actual_distance):
        current_time = time.time()
        result = {"distance": actual_distance, "force": self.player_force}
        distance_to_target = abs(self.target_distance - actual_distance)

        # Determine outcome based on distance change
        if self.previous_distance_to_target is not None:
            if distance_to_target < self.previous_distance_to_target:
                outcome = "reward"
            else:
                outcome = "distress"
        else:
            outcome = "neutral"  # Initial outcome if there's no previous distance to compare

        self.previous_distance_to_target = distance_to_target  # Update previous distance

        self.history.append({
            'round': self.round,
            'action': 'execute_shot',
            'result': result,
            'timestamp': current_time,
            'distance_to_target': distance_to_target,
            'player_force': self.player_force
        })
        self.score += self.calculate_score(actual_distance)
        self.publish_outcome(distance_to_target, outcome)
        self.round += 1

    def calculate_score(self, actual_distance):
        distance_to_target = abs(self.target_distance - actual_distance)
        if distance_to_target == 0:
            return 10
        elif distance_to_target <= 5:
            return 5
        elif distance_to_target <= 10:
            return 3
        else:
            return 1

    def publish_outcome(self, distance_to_target, outcome):
        outcome_message = json.dumps({
            "round": self.round,
            "distance_to_target": distance_to_target,
            "outcome": outcome
        })
        self.mqtt_client.publish(self.outcome_topic, outcome_message)
        print(f"Published outcome: {outcome_message}")

    def generate_metadata(self):
        return {
            'score': self.score,
            'round': self.round,
            'distance_to_target': self.history[-1]['distance_to_target'] if self.history else 0,
            'player_force': self.history[-1]['player_force'] if self.history else self.player_force
        }

    def publish_metadata(self):
        metadata = self.generate_metadata()
        metadata_json = json.dumps(metadata)
        self.mqtt_client.publish(self.metadata_topic, metadata_json)
        print(f"Published metadata: {metadata_json}")  # Debug statement

    def publish_historic_data(self):
        duration = time.time() - self.start_time
        historic_data = {
            'game_duration': duration,
            'history': self.history
        }
        historic_data_json = json.dumps(historic_data)
        self.mqtt_client.publish(self.historic_data_topic, historic_data_json)

    def play_round(self):
        pass  # No need to do anything here since actions are processed via MQTT

    def end_game(self):
        duration = time.time() - self.start_time
        print(f"Game over. Duration: {duration} seconds")
        self.publish_historic_data()
        self.reset_game()

def main():
    app = QApplication(sys.argv)
    target_distance = 50  # Preset target distance from player
    game = ShuffleboardGame(target_distance, max_rounds=20, performance_threshold=80)

    game.mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1)  # Control the pace of game rounds
    except KeyboardInterrupt:
        print("Stopping...")
        game.mqtt_client.loop_stop()
        game.mqtt_client.disconnect()

if __name__ == "__main__":
    main()
