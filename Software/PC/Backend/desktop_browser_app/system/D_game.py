import zmq
import vizdoom as vzd
import time
from time import sleep
import json

# scenarios: https://vizdoom.farama.org/environments/default/
# custom scenario: https://vizdoom.farama.org/environments/creatingCustom/
def initialize_vizdoom(config_path, scenario_path):
    game = vzd.DoomGame()
    config_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.cfg"
    scenario_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.wad"
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.PLAYER)
    game.set_objects_info_enabled(True)
    game.set_screen_resolution(vzd.ScreenResolution.RES_512X384)
    game.set_render_hud(True)
    
    # Specify available buttons
    game.clear_available_buttons()
    game.add_available_button(vzd.Button.ATTACK)
    game.add_available_button(vzd.Button.USE)
    game.add_available_button(vzd.Button.MOVE_BACKWARD)
    game.add_available_button(vzd.Button.MOVE_FORWARD)
    game.add_available_button(vzd.Button.TURN_RIGHT)
    game.add_available_button(vzd.Button.TURN_LEFT)

    game.init()
    return game
    # Enable detailed game variables
    game.set_objects_info_enabled(True)
    
    game.init()
    return game

# buttons for actions: 
#    https://vizdoom.farama.org/api/python/doomGame/#vizdoom.DoomGame.set_available_buttons
#    https://github.com/Farama-Foundation/ViZDoom/blob/master/examples/python/delta_buttons.py

def decode_actions(action_str):
    # Split the received action string into individual action codes
    action_codes = [int(code) for code in action_str.split(',') if code.isdigit()]
    # Initialize an action array with all elements set to False
    action = [False] * len(vzd.Button)
    for code in action_codes:
        if code < len(action):
            action[code] = True
    return action

# variables for game state: 
#    https://vizdoom.farama.org/main/api/python/gameState/#
#    https://vizdoom.farama.org/api/python/enums/
#    https://github.com/Farama-Foundation/ViZDoom/issues/361
#    https://github.com/Farama-Foundation/ViZDoom
#    https://github.com/Farama-Foundation/ViZDoom/blob/master/examples/python/buffers.py
#    https://github.com/Farama-Foundation/ViZDoom/blob/master/examples/python/labels_buffer.py
#    https://github.com/Farama-Foundation/ViZDoom/blob/master/examples/python/objects_and_sectors.py
#    https://vizdoom.farama.org/main/api/python/doomGame/#vizdoom.DoomGame.set_sectors_info_enabled
#    https://vizdoom.farama.org/main/api/python/gameState/#vizdoom.GameState.objects

def extract_game_state(game):
    # Extract required game variables
    hitcount = game.get_game_variable(vzd.GameVariable.HITCOUNT)
    hits_taken = game.get_game_variable(vzd.GameVariable.HITS_TAKEN)
    dead = game.get_game_variable(vzd.GameVariable.DEAD) > 0
    health = game.get_game_variable(vzd.GameVariable.HEALTH)
    attack_ready = game.get_game_variable(vzd.GameVariable.ATTACK_READY) > 0

    # Initialize enemy information
    enemy_in_view = 0.0
    enemy_position_x = 0.0
    enemy_position_y = 0.0
    enemy_position_z = 0.0
    enemy_angle = 0.0
    enemy_pitch = 0.0
    enemy_roll = 0.0
    enemy_velocity_x = 0.0
    enemy_velocity_y = 0.0
    enemy_velocity_z = 0.0

    # Check if there are labels (requires SCREEN_LABELS to be enabled in game config)
    state = game.get_state()
    if state and state.labels:
        for label in state.labels:
            if label.object_name == "DoomPlayer" and label.object_id != 0:
                enemy_in_view = 1.0
                enemy_position_x = label.object_position_x
                enemy_position_y = label.object_position_y
                enemy_position_z = label.object_position_z
                enemy_angle = label.object_angle
                enemy_pitch = label.object_pitch
                enemy_roll = label.object_roll
                enemy_velocity_x = label.object_velocity_x
                enemy_velocity_y = label.object_velocity_y
                enemy_velocity_z = label.object_velocity_z
                break  # Assuming you're only interested in the first enemy in view

    # Extract screen buffer if available
    screen_buffer = None
    if game.get_screen_format() != vzd.ScreenFormat.CRCGCB:
        screen_buffer = state.screen_buffer
    else:
        print("Screen buffer format not supported or not enabled.")

    game_state_info = {
        "hitcount": hitcount,
        "hits_taken": hits_taken,
        "dead": dead,
        "health": health,
        "attack_ready": attack_ready,
        "enemy_in_view": enemy_in_view,
        "enemy_position": {
            "x": enemy_position_x,
            "y": enemy_position_y,
            "z": enemy_position_z
        },
        "enemy_angle": enemy_angle,
        "enemy_pitch": enemy_pitch,
        "enemy_roll": enemy_roll,
        "enemy_velocity": {
            "x": enemy_velocity_x,
            "y": enemy_velocity_y,
            "z": enemy_velocity_z
        },
        "screen_buffer": screen_buffer
    }
    return game_state_info


def main():
    game = initialize_vizdoom("config_path", "scenario_path")

    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5447")

    context_sub = zmq.Context()
    sub_socket = context_sub.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5446")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        try:
            # Attempt to receive a message non-blockingly
            try:
                message = sub_socket.recv_string(zmq.NOBLOCK)
                actions_json = json.loads(message)
                actions_list = [actions_json.get("ATTACK", False), 
                                actions_json.get("USE", False),
                                actions_json.get("MOVE_BACKWARD", False),
                                actions_json.get("MOVE_FORWARD", False),
                                actions_json.get("TURN_RIGHT", False),
                                actions_json.get("TURN_LEFT", False)]
                game.make_action(actions_list)
                
                # Convert actions to JSON string and send
                action_message = json.dumps(actions_list)
                publisher.send_string(action_message)

            except zmq.Again:
                pass  # Expected behavior, no message to receive
                
        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            # Ensure some delay in the loop to prevent it from spinning too fast
            time.sleep(0.001)  # Adjust as needed

if __name__ == "__main__":
    main()

