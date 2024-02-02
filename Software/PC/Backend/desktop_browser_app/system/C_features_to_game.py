import zmq
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

class GameActionEncoder:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        # Map neural signal decoded actions to keyboard/mouse actions
        self.key_map = {
            'forward': Key.up,
            'left': Key.left,
            'right': Key.right,
            'stop': Key.down,  # Assuming you have a specific key for stop
            'shoot': 'space',  # Space for shooting
            'open_door': 'e'   # 'e' for opening doors
        }

    class SignalDecoder:
    """
    Decodes the analyzed signal features into specific game actions, utilizing insights from
    BCI research which often relates specific neural signal patterns to intended actions or
    mental states.
    """
    def __init__(self):
        # Configuration for mapping signal features to game actions, incorporating BCI research findings.
        # Each feature can trigger different actions based on its value exceeding a certain threshold.
        self.feature_to_action_map = {
            'rms': ('move_forward', 0.5),
            'variance': ('turn_left', 0.2),
            'spectral_entropy': ('open_door', 0.7),  # Higher entropy might indicate a decision-making state.
            'peak_counts': ('shoot', 3),  # Number of peaks could be linked to excitement or intention to shoot.
            'higuchi_fractal_dimension': ('turn_right', 1.2),  # Complexity of the signal might indicate directional intention.
            'zero_crossing_rate': ('stop', 0.1),  # Low activity could indicate a stop command.
            'phase_synchronization': ('synchronize_team', 0.8),  # High phase locking value might indicate team coordination.
            # Frequency bands can indicate different types of cognitive activity or focus:
            'band_features_delta': ('rest', 0.5),  # High delta power might indicate rest or low engagement.
            'band_features_theta': ('strategic_think', 0.5),  # Theta might be linked to strategic thinking or navigation.
            'band_features_alpha': ('calm', 0.5),  # Alpha increases can indicate relaxation or calm.
            'band_features_beta': ('alert', 0.5),  # Beta might indicate alertness and readiness.
        }

    def decode_features_to_actions(self, analyzed_features):
        """
        Decodes the analyzed signal features into game actions based on predefined thresholds.
        """
        actions = {}
        for feature, (action, threshold) in self.feature_to_action_map.items():
            value = analyzed_features.get(feature, 0)
            # Trigger action if the feature's value crosses its specified threshold.
            actions[action] = value > threshold
        return actions


    def decode_features_to_actions(self, analyzed_features):
        """
        Decodes the analyzed signal features into game actions based on predefined thresholds.
        """
        actions = {}
        for feature, (action, threshold) in self.feature_to_action_map.items():
            value = analyzed_features.get(feature, 0)
            actions[action] = value > threshold
        return actions

        def execute_actions(self, actions):
        """
        Simulates the necessary keyboard and mouse inputs to execute the game actions.
        """
        for action, active in actions.items():
            key = self.action_to_key_map.get(action)
            if key:
                if active:
                    self.keyboard.press(key)
                else:
                    self.keyboard.release(key)
            # Add mouse action execution if needed

def main():
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5445")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    decoder = SignalDecoder()
    executor = GameActionExecutor()

    while True:
        try:
            # Receive analyzed signal features as a custom string
            message = sub_socket.recv_string()
            analyzed_features = d.loads(message)
            
            # Decode features to game actions
            actions = decoder.decode_features_to_actions(analyzed_features)
            
            # Execute decoded actions in the game
            executor.execute_actions(actions)

        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except DecodeError:
            print("Error d from received message")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()