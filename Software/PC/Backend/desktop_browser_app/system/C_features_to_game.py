import zmq
import time
import numpy as np
#import skfuzzy as fuzz
#from skfuzzy import control as ctrl

class GameActionEncoder:
    def __init__(self):
        # Map decoded actions to environment's numeric actions
        self.action_map = {
            'forward': 0,
            'left': 1,
            'right': 2,
            'shoot': 3,
            'open_door': 4,
            'back': 5
        }

    def execute_actions(self, decoded_actions):
        # This example assumes a discrete action space where only one action is performed at a time
        action = None
        for decoded_action, active in decoded_actions.items():
            if active and decoded_action in self.action_map:
                action = self.action_map[decoded_action]
        return action

class SignalDecoder:
    """
    Decodes analyzed signal features into specific game actions, supporting combinations of actions
    based on combinations of features.
    """
    def __init__(self):
        self.feature_to_action_map = {
            'rms': ('forward', 3.96e-07),
            'variance': ('left', 1.074e-26),
            'spectral_entropy': ('open_door', 0.7),
            'peak_counts': ('shoot', 3),
            'higuchi_fractal_dimension': ('right', 1.35e-15),
            'zero_crossing_rate': ('stop', 0.1),
            #'phase_synchronization': ('forward', 0.8),
            'band_features_delta': ('stop', 0.5),
            'band_features_theta': ('stop', 0.5),
            'band_features_alpha': ('stop', 0.5),
            'band_features_beta': ('stop', 0.5),
            'peak_heights': ('stop', 0.5),
            'std_dev': ('stop', 7.5e-14),
            'centroids': ('stop', 0.5),
            'spectral_edge_densities': ('stop', 0.5),
            #'empirical_mode_decomposition': ('stop', 0.5),
            #'time_warping_factor': ('stop', 0.5),
            'evolution_rate': ('stop', 0.5),
        }


    def decode_features_to_actions(self, analyzed_features):
        actions = {}
        for feature, (action, threshold) in self.feature_to_action_map.items():
            value = analyzed_features.get(feature, None)
            if value is not None:
                if isinstance(value, list):  # Handle list values by averaging
                    value = sum(value) / len(value)
                # Perform the comparison if value is an appropriate type
                if isinstance(value, (float, int)):
                    if value > threshold:
                        actions[action] = True
                    else:
                        print(f"Feature '{feature}' value {value} did not meet the threshold {threshold}.")
                else:
                    print(f"Skipping comparison for feature: {feature} with unsupported type: {type(value)}")
    
        # Convert actions into numeric format for game input, ensuring actions are correctly mapped
        numeric_actions = [self.action_map[action] for action in actions if actions[action]]
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
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    decoder = SignalDecoder()
    encoder = GameActionEncoder()

    while True:
        try:
            message = sub_socket.recv_string()
            analyzed_features = eval(message)
            
            actions = decoder.decode_features_to_actions(analyzed_features)
            numeric_action = encoder.execute_actions(actions)
            
            if numeric_action is not None:
                # Assuming numeric_action needs to be published
                publisher.send_string(f"Action: {numeric_action}")
            
            time.sleep(1)

        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()