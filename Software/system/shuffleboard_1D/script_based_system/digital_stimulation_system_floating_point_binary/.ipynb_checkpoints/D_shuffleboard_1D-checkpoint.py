import paho.mqtt.client as mqtt
import zmq
import time
import json

class ShuffleboardGame:
    def __init__(self, target_distance, max_rounds=10, performance_threshold=80):
        self.target_distance = target_distance
        self.max_rounds = max_rounds
        self.performance_threshold = performance_threshold
        self.reset_game()

        # ZeroMQ setup for receiving actions
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:5446")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

        # MQTT setup for publishing metadata and outcomes
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        self.metadata_topic = "game_metadata"
        self.outcome_topic = "game_outcome"
        self.historic_data_topic = "historic_data"

    def reset_game(self):
        self.player_force = 10  # Initial force
        self.score = 0
        self.round = 1
        self.history = []
        self.start_time = time.time()

    def receive_action(self):
        try:
            action_message = self.sub_socket.recv_string(zmq.NOBLOCK)
            action = json.loads(action_message).get("action")
            return action
        except zmq.Again:
            return None

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
        self.history.append({
            'round': self.round,
            'action': 'execute_shot',
            'result': result,
            'timestamp': current_time,
            'distance_to_target': distance_to_target,
            'player_force': self.player_force
        })
        self.score += self.calculate_score(actual_distance)
        self.publish_outcome(distance_to_target)
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

    def publish_outcome(self, distance_to_target):
        if distance_to_target == 0:
            outcome = "reward"
        elif distance_to_target <= 5:
            outcome = "reward"
        elif distance_to_target <= 10:
            outcome = "neutral"
        else:
            outcome = "distress"
        
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
            'distance_to_target': self.history[-1]['distance_to_target'] if self.history else None,
            'player_force': self.history[-1]['player_force'] if self.history else self.player_force
        }

    def publish_metadata(self):
        metadata = self.generate_metadata()
        metadata_json = json.dumps(metadata)
        self.mqtt_client.publish(self.metadata_topic, metadata_json)

    def publish_historic_data(self):
        duration = time.time() - self.start_time
        historic_data = {
            'game_duration': duration,
            'history': self.history
        }
        historic_data_json = json.dumps(historic_data)
        self.mqtt_client.publish(self.historic_data_topic, historic_data_json)

    def play_round(self):
        action = self.receive_action()
        if action:
            result = self.apply_action(action)
            if result is not None:
                print(f"Shot executed with distance {result} and force {self.player_force}")
            self.publish_metadata()
            metadata = self.generate_metadata()
            print(f"Metadata: {metadata}")

        if self.round > self.max_rounds or self.score >= self.performance_threshold:
            self.end_game()

    def end_game(self):
        duration = time.time() - self.start_time
        print(f"Game over. Duration: {duration} seconds")
        self.publish_historic_data()
        self.reset_game()

def main():
    target_distance = 50  # Preset target distance from player
    game = ShuffleboardGame(target_distance, max_rounds=10, performance_threshold=80)

    while True:
        game.play_round()
        time.sleep(1)  # Control the pace of game rounds

if __name__ == "__main__":
    main()
