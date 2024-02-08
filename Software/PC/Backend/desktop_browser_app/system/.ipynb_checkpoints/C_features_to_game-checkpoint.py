import zmq
import time
from pynput.keyboard import Key, Controller as KeyboardController
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class GameActionEncoder:
    def __init__(self):
        self.keyboard = KeyboardController()
        # Map neural signal decoded actions to keyboard actions
        self.key_map = {
            'forward': Key.up,
            'left': Key.left,
            'right': Key.right,
            'stop': None,  # No key for stop
            'shoot': 'space',  # Space for shooting
            'open_door': 'e'   # 'e' for opening doors
        }

    def execute_actions(self, actions):
        """
        Simulates the necessary keyboard inputs to execute the game actions.
        """
        keys_pressed = set()
        for action, active in actions.items():
            if action in self.key_map and active:
                key = self.key_map[action]
                if key:
                    keys_pressed.add(key)
        for key in self.key_map.values():
            if key and key not in keys_pressed:
                self.keyboard.release(key)
        for key in keys_pressed:
            self.keyboard.press(key)

class SignalDecoder:
    """
    Decodes the analyzed signal features into specific game actions.
    """
    def __init__(self):
        # Fuzzy logic system setup
        self.input_var = ctrl.Antecedent(np.arange(0, 256, 1), 'input_var')
        self.output_action = ctrl.Consequent(np.arange(0, 256, 1), 'output_action')

        # Define membership functions for input and output variables
        self.input_var['low'] = fuzz.trimf(self.input_var.universe, [0, 0, 128])
        self.input_var['medium'] = fuzz.trimf(self.input_var.universe, [64, 128, 192])
        self.input_var['high'] = fuzz.trimf(self.input_var.universe, [128, 255, 255])

        self.output_action['forward'] = fuzz.trimf(self.output_action.universe, [0, 0, 128])
        self.output_action['stop'] = fuzz.trimf(self.output_action.universe, [64, 128, 192])
        self.output_action['back'] = fuzz.trimf(self.output_action.universe, [128, 255, 255])

        # Define fuzzy rules
        rule1 = ctrl.Rule(self.input_var['low'], self.output_action['forward'])
        rule2 = ctrl.Rule(self.input_var['medium'], self.output_action['stop'])
        rule3 = ctrl.Rule(self.input_var['high'], self.output_action['back'])

        # Create fuzzy control system
        self.system = ctrl.ControlSystem([rule1, rule2, rule3])
        self.controller = ctrl.ControlSystemSimulation(self.system)

        # Mapping of features to actions with ranges and change from the last packet
        self.feature_to_action_map = {
            'rms': ('forward', (0, 0.5), (-0.1, 0.1)),  # Example range for 'rms' feature and change
            'variance': ('left', (0, 0.2), (-0.05, 0.05)),  # Example range for 'variance' feature and change
            'spectral_entropy': ('open_door', (0.7, 1.0), (-0.05, 0.05)),  # Example range for 'spectral_entropy' feature and change
            'peak_counts': ('shoot', (3, float('inf')), (0, float('inf'))),  # Example range for 'peak_counts' feature and change
            'higuchi_fractal_dimension': ('right', (1.2, float('inf')), (0, float('inf'))),  # Example range for 'higuchi_fractal_dimension' feature and change
            'zero_crossing_rate': ('stop', (0, 0.1), (-0.05, 0.05)),  # Example range for 'zero_crossing_rate' feature and change
            'phase_synchronization': ('forward', (0.8, 1.0), (-0.05, 0.05)),  # Example range for 'phase_synchronization' feature and change
            'band_features_delta': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'band_features_delta' feature and change
            'band_features_theta': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'band_features_theta' feature and change
            'band_features_alpha': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'band_features_alpha' feature and change
            'band_features_beta': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'band_features_beta' feature and change
            'peak_heights': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'peak_heights' feature and change
            'std_dev': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'std_dev' feature and change
            'centroids': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'centroids' feature and change
            'spectral_edge_densities': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'spectral_edge_densities' feature and change
            'empirical_mode_decomposition': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'empirical_mode_decomposition' feature and change
            'time_warping_factor': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'time_warping_factor' feature and change
            'evolution_rate': ('stop', (0, 0.5), (-0.05, 0.05)),  # Example range for 'evolution_rate' feature and change
        }

    def decode_features_to_actions(self, analyzed_features):
        """
        Decodes the analyzed signal features into game actions based on fuzzy logic inference.
        """
        # Prepare input signal for fuzzy inference
        input_signal = analyzed_features.get('rms', 0)  # Example feature 'rms'
    
        # Perform fuzzy inference
        self.controller.input['input_var'] = input_signal
        self.controller.compute()
    
        # Get fuzzy output values
        fuzzy_output_values = {
            'forward': self.controller.output['output_action']['forward'],
            'stop': self.controller.output['output_action']['stop'],
            'back': self.controller.output['output_action']['back']
        }
    
        # Initialize actions based on fuzzy output
        actions = {
            'forward': fuzzy_output_values['forward'] > 0.5,  # Example threshold
            'stop': fuzzy_output_values['stop'] > 0.5,  # Example threshold
            'back': fuzzy_output_values['back'] > 0.5  # Example threshold
        }
    
        # Override actions based on direct feature ranges and changes from the last packet
        for feature, (action, range_, change_range) in self.feature_to_action_map.items():
            value = analyzed_features.get(feature, 0)
            if range_[0] <= value <= range_[1] and change_range[0] <= value <= change_range[1]:
                actions[action] = True
    
        return actions


def main():
    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5446")  # Bind to port 5556 for publishing

    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5445")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    decoder = SignalDecoder()
    encoder = GameActionEncoder()

    while True:
        try:
            # Receive analyzed signal features as a custom string
            message = sub_socket.recv_string()
            analyzed_features = eval(message)
            
            # Decode features to game actions using fuzzy logic
            actions = decoder.decode_features_to_actions(analyzed_features)
            
            # Execute decoded actions in the game
            encoder.execute_actions(actions)

            # Publish the extracted features and actions as a string
            encoded_features = " ".join([f"{key}:{value}" for key, value in analyzed_features.items()])
            encoded_actions = " ".join([f"{key}:{value}" for key, value in actions.items() if key in encoder.key_map])
            encoded_data = f"Features: {encoded_features}, Actions: {encoded_actions}"
            publisher.send_string(encoded_data)

            # Introduce a 100ms delay for 10 Hz frequency
            time.sleep(0.1)

        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()