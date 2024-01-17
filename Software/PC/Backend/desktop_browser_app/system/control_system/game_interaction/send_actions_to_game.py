from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

class GameActionEncoder:
    def __init__(self):
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.key_map = {
            'forward': Key.up,  # Example key mapping
            'left': Key.left,
            'right': Key.right,
            'stop': Key.down,
            'shoot': 'space',   # Assuming space bar for shoot
            'open_door': 'e'    # Example key for opening doors
        }

    def send_actions_to_game(self, actions):
        for action, is_active in actions.items():
            if is_active:
                if action in ['forward', 'left', 'right', 'stop', 'shoot', 'open_door']:
                    self.keyboard.press(self.key_map[action])
                elif action == 'look_around':  # Example for mouse movement
                    # Implement mouse movement logic
                    pass
            else:
                if action in ['forward', 'left', 'right', 'stop', 'shoot', 'open_door']:
                    self.keyboard.release(self.key_map[action])
