import zmq
import time
import json

class ShuffleboardGame:
    def __init__(self, target_distance):
        self.target_distance = target_distance
        self.player_force = 10  # Initial force
        self.score = 0
        self.round = 1
        self.history = []
        self.start_time = time.time()

        # ZeroMQ setup for receiving actions and publishing metadata
        self.context = zmq.Context()
        self.sub_socket = self.context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://localhost:5446")
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.pub_socket = self.context.socket(zmq.PUB)  # Publisher socket for metadata
        self.pub_socket.bind("tcp://*:5556")  # Binding to a port to publish metadata

    def receive_action(self):
        try:
            action_message = self.sub_socket.recv_string(zmq.NOBLOCK)  # Non-blocking
            action = json.loads(action_message).get("action")  # Assuming action is wrapped in JSON
            return action
        except zmq.Again:
            # No action received yet
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
        self.history.append({
            'round': self.round,
            'action': 'execute_shot',
            'result': result,
            'timestamp': current_time,
            'distance_to_target': abs(self.target_distance - actual_distance),
            'player_force': self.player_force
        })
        self.score += self.calculate_score(actual_distance)
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

    def generate_metadata(self):
        duration = time.time() - self.start_time
        return {
            'score': self.score,
            'round': self.round,
            'game_duration': duration,
            'history': self.history
        }

    def publish_metadata(self):
        if self.history:
            last_action = self.history[-1]
            distance_to_target = last_action['distance_to_target']
            player_force = last_action['player_force']
        else:
            distance_to_target = self.target_distance
            player_force = 0

        metadata_string = f"score:{self.score},round:{self.round},duration:{time.time() - self.start_time},distance_to_target:{distance_to_target},player_force:{player_force}"
        self.pub_socket.send_string(metadata_string)

    def play_round(self):
        action = self.receive_action()
        if action:
            result = self.apply_action(action)
            if result is not None:
                print(f"Shot executed with distance {result} and force {self.player_force}")
            self.publish_metadata()  # Publish metadata after processing the action
            metadata = self.generate_metadata()
            print(f"Metadata: {metadata}")

def main():
    target_distance = 50
    game = ShuffleboardGame(target_distance)

    while True:
        game.play_round()
        time.sleep(0.1)  # Control the pace of game rounds

if __name__ == "__main__":
    main()
