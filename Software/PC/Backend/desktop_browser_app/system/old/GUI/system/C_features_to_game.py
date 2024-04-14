import zmq
import time
import numpy as np
#import skfuzzy as fuzz
#from skfuzzy import control as ctrl

class GameActionEncoder:
    def __init__(self):
        # Map decoded actions to environment's numeric actions
        self.action_map = {
            'MOVE_FORWARD': 0,
            'TURN_LEFT': 1,
            'TURN_RIGHT': 2,
            'ATTACK': 3,
            'USE': 4,
            'MOVE_BACKWARD': 5
        }

    def execute_actions(self, decoded_actions):
        # This example assumes a discrete action space where only one action is performed at a time
        action = [False] * len(self.action_map)  # Initialize a list of False actions
        for decoded_action, active in decoded_actions.items():
            if active and decoded_action in self.action_map:
                action_index = self.action_map[decoded_action]  # Get the index of the action
                action[action_index] = True  # Set the action to True
        return action

class SignalDecoder:
    """
    Decodes analyzed signal features into specific game actions, supporting combinations of actions
    based on combinations of features.
    """
    def __init__(self):
        self.feature_to_action_map = {
            'rms': ('MOVE_FORWARD', 3.96e-07),
            'variance': ('TURN_LEFT', 1.074e-26),
            'spectral_entropy': ('USE', 0.7),
            'peak_counts': ('ATTACK', 3),
            'higuchi_fractal_dimension': ('TURN_RIGHT', 1.35e-15),
            'zero_crossing_rate': ('MOVE_FORWARD', 0.1),
            #'phase_synchronization': ('forward', 0.8),
            'delta_band_power': ('MOVE_FORWARD', 0.5),
            'theta_band_power': ('MOVE_FORWARD', 0.5),
            'alpha_band_power': ('MOVE_FORWARD', 0.5),
            'beta_band_power': ('MOVE_FORWARD', 0.5),
            'peak_heights': ('MOVE_FORWARD', 0.5),
            'std_dev': ('MOVE_FORWARD', 7.5e-14),
            'centroids': ('MOVE_FORWARD', 0.5),
            'spectral_edge_densities': ('MOVE_FORWARD', 0.5),
            #'empirical_mode_decomposition': ('stop', 0.5),
            #'time_warping_factor': ('stop', 0.5),
            'evolution_rate': ('MOVE_FORWARD', 0.5),
        }


    def decode_features_to_actions(self, analyzed_features):
        actions = {}
        # Define a minimum proportion of signals that must meet the threshold for an action
        min_proportion = 0.5  # Example: at least 50% of signals must exceed the threshold
    
        for feature, (action, threshold) in self.feature_to_action_map.items():
            values = analyzed_features.get(feature, None)
            if values is not None and isinstance(values, list):
                # Calculate the proportion of values exceeding the threshold
                exceeding_threshold = sum(val > threshold for val in values) / len(values)
                if exceeding_threshold >= min_proportion:
                    actions[action] = True
                else:
                    print(f"Feature '{feature}' did not meet the threshold proportion {min_proportion}.")
            else:
                print(f"Feature '{feature}' is missing or not a list.")
        
        # Convert actions into numeric format for game input, ensuring actions are correctly mapped
        action_dict = {action: False for action in self.action_map}  # Initialize action dictionary
        for action in actions:
            if actions[action]:
                action_dict[action] = True  # Update action dictionary based on decoded actions
        
        numeric_actions = [action_dict[action] for action in self.action_map.keys()]
        return numeric_actions
        
'''
class SignalDecoder:
        
    Decodes the analyzed signal features into specific game actions.
    
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
        
        Decodes the analyzed signal features into game actions based on fuzzy logic inference.
        
        # Example feature 'rms'
        input_signal = analyzed_features.get('rms', 0)  
        
        # Perform fuzzy inference
        self.controller.input['input_var'] = input_signal
        self.controller.compute()
        
        # Initialize actions based on fuzzy output, corrected to use .defuzzify method
        actions = {}
        actions['forward'] = self.controller.output['forward'] > 0.5  # Correctly access output
        actions['stop'] = self.controller.output['stop'] > 0.5
        actions['back'] = self.controller.output['back'] > 0.5
        
        # Override actions based on direct feature ranges and changes from the last packet
        for feature, (action, range_, change_range) in self.feature_to_action_map.items():
            value = analyzed_features.get(feature, 0)
            if value >= range_[0] and value <= range_[1]:  # Adjusted to avoid ambiguous truth value
                actions[action] = True
        
        # Convert boolean actions to numerical format expected by the game environment
        numeric_actions = [self.action_map[action] for action, active in actions.items() if active]
        
        return numeric_actions
'''

def main():
    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5446")

    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5445")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')  # Subscribe to all incoming messages

    decoder = SignalDecoder()
    encoder = GameActionEncoder()

    while True:
        try:
            message = sub_socket.recv_string()  # Receive the message as a string
            analyzed_features = json.loads(message)  # Safely deserialize the JSON string to a dictionary
            
            decoded_actions = decoder.decode_features_to_actions(analyzed_features)
            actions = encoder.execute_actions(decoded_actions)
                 
            # Convert dictionary to JSON string
            action_message = json.dumps(action_dict)
            publisher.send_string(action_message)
            
            time.sleep(1)

        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()