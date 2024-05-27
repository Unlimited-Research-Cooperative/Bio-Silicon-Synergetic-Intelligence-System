import constants
from json import loads, dumps
from data_manager import DataManager
from constants import ActionMap, Actions


class ActionEncoder:
    def __init__(self):
        self.action_map = Actions().to_dict()

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
        self.action_map = {}
        self.feature_to_action_map = ActionMap().to_dict()  # Dictionary with default values

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

        # numeric_actions = [action_dict[action] for action in self.action_map.keys()]
        return action_dict


class Executor:
    def __init__(self):
        self.encoder = ActionEncoder()
        self.decoder = SignalDecoder()
        self.data_m = DataManager("feature to game sub", constants.DECODED_FEATURES, constants.GAME_INPUTS,
                                  self.helper_func)

    def helper_func(self, payload: str):
        encoder = ActionEncoder()
        decoder = SignalDecoder()
        analyzed_features = loads(payload)
        decoded_actions = decoder.decode_features_to_actions(analyzed_features)
        action = encoder.execute_actions(decoded_actions)
        action_msg = dumps(action)
        self.set_game_input(action_msg)
        self.data_m.set_data(action_msg)
        self.data_m.publish(1)
#
# if __name__ == "__main__":
#     executor = Executor()
