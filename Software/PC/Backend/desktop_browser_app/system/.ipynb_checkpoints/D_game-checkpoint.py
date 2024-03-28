import zmq
import vizdoom as vzd
import time
from time import sleep
import json

# scenarios: https://vizdoom.farama.org/environments/default/
# custom scenario: https://vizdoom.farama.org/environments/creatingCustom/
# Initialize the game environment using the given configuration and scenario paths
def initialize_vizdoom(config_path, scenario_path):
    # Create a new DoomGame instance
    game = vzd.DoomGame()
    # Overwrite the default config path with a specific path
    config_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.cfg"
    # Overwrite the default scenario path with a specific path
    scenario_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.wad"
    # Make the game window visible
    game.set_window_visible(True)
    # Set the game mode to PLAYER (as opposed to SPECTATOR)
    game.set_mode(vzd.Mode.PLAYER)
    # Enable detailed objects information
    game.set_objects_info_enabled(True)

    game.set_sectors_info_enabled(True)

    # Set the screen resolution
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    # Enable rendering of the HUD
    game.set_render_hud(True)

    game.set_automap_render_textures(True)

    game.set_render_weapon(True)

    game.set_render_decals(True)

    game.set_render_particles(True)

    game.set_render_effects_sprites(True)

    game.set_render_messages(True)

    game.set_render_corpses(True)

    game.set_render_all_frames(True)

    game.set_sound_enabled(True)

    
    
    # Clear any previously available buttons and specify new ones for this game instance
    game.clear_available_buttons()
    game.add_available_button(vzd.Button.ATTACK)
    game.add_available_button(vzd.Button.USE)
    game.add_available_button(vzd.Button.MOVE_BACKWARD)
    game.add_available_button(vzd.Button.MOVE_FORWARD)
    game.add_available_button(vzd.Button.TURN_RIGHT)
    game.add_available_button(vzd.Button.TURN_LEFT)
    # set_button_max_value(self: vizdoom.DoomGame, button: vizdoom.Button, max_value: float) → None
    # Sets the maximum allowed absolute value for the specified Button. Setting the maximum value to 0 results in no constraint at all (infinity). This method makes sense only for delta buttons. The constraints limit applies in all Modes.
    # Has no effect when the game is running.

    # Initialize the game with the specified settings
    game.init()
    return game
    # The following lines are unreachable due to the preceding return statement
    # and should be removed or corrected for proper execution.


# buttons for actions: 
#    https://vizdoom.farama.org/api/python/doomGame/#vizdoom.DoomGame.set_available_buttons
#    https://github.com/Farama-Foundation/ViZDoom/blob/master/examples/python/delta_buttons.py

# Decode action strings into boolean arrays indicating which actions are active
def decode_actions(action_str):
    # Convert the comma-separated string into a list of integers
    action_codes = [int(code) for code in action_str.split(',') if code.isdigit()]
    # Initialize a boolean list to represent the activation state of each action
    action = [False] * len(vzd.Button)
    # Set the corresponding action to True based on the action codes
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

# Extract and return game state information as a dictionary
def extract_game_state(game):
    # Retrieve various game variables
    hitcount = game.get_game_variable(vzd.GameVariable.HITCOUNT)
    hits_taken = game.get_game_variable(vzd.GameVariable.HITS_TAKEN)
    dead = game.get_game_variable(vzd.GameVariable.DEAD) > 0
    health = game.get_game_variable(vzd.GameVariable.HEALTH)
    attack_ready = game.get_game_variable(vzd.GameVariable.ATTACK_READY) > 0
    
    # Player position for distance calculation
    player_x = game.get_game_variable(vzd.GameVariable.POSITION_X)
    player_y = game.get_game_variable(vzd.GameVariable.POSITION_Y)
    player_z = game.get_game_variable(vzd.GameVariable.POSITION_Z)

    def detect_doors(labels):
    # Example logic; you'll need to adjust based on how doors are labeled in your scenario
    doors_detected = any(label.object_name.lower().contains("door") for label in labels)
    return doors_detected

    def categorize_enemy_type(labels):
    enemy_types_detected = {"weak": 0, "strong": 0, "boss": 0}
    for label in labels:
        if "Imp" in label.object_name:  # Example: assuming 'Imp' as a weak enemy
            enemy_types_detected["weak"] += 1
        elif "Demon" in label.object_name:  # Example: a stronger enemy
            enemy_types_detected["strong"] += 1
        # Add more conditions based on known enemy types in ViZDoom
    return enemy_types_detected

    # This requires keeping track of past actions and outcomes
    action_states = {"moving": False, "shooting": False, "escaping_enemy": False}

    def determine_exploring_state(depth_buffer):
    # Example heuristic: a narrower field in the depth buffer might indicate a corridor
    # This will require custom logic based on your game's design and scenarios
    return "corridor" if is_corridor(depth_buffer) else "open room"

    # Example logic for tracking if a key has been picked up
    level_states = {"looking_for_door_key": True, "have_door_key": False}

    def detect_wall_states(depth_buffer):
    # Example logic to process the depth buffer and determine wall proximity and orientation
    wall_states_detected = {"wall_to_the_left": False, "wall_to_the_right": False, "wall_in_front": False}
    # Fill in the logic based on depth buffer analysis
    return wall_states_detected

    # Initialize variables for enemy information
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

    visible_objects = []
    if state and state.labels:
        for obj in state.labels:  # Using labels for visible objects
            obj_distance = np.sqrt((obj.object_position_x - player_x) ** 2 + (obj.object_position_y - player_y) ** 2 + (obj.object_position_z - player_z) ** 2)
            visible_objects.append({
                "label": obj.value,
                "name": obj.object_name,
                "distance": obj_distance,
                "position": {
                    "x": obj.object_position_x,
                    "y": obj.object_position_y,
                    "z": obj.object_position_z,
                }
            })
     
    # Check if the game state has labels for identifying objects
    state = game.get_state()
    if state and state.labels:
        for label in state.labels:
            if label.object_name == "DoomPlayer" and label.object_id != 0:
                # Update enemy information based on the first encountered enemy
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
                break  # Exit loop after finding the first enemy
    # https://vizdoom.farama.org/main/api/python/gameState/#data-types-used-in-gamestate
    
    # add_available_game_variable(self: vizdoom.DoomGame, variable: vizdoom.GameVariable) → None
    # Adds the specified GameVariable to the list of available game variables (e.g. HEALTH, AMMO1, ATTACK_READY) in the GameState returned by get_state() method.
    # Has no effect when the game is running.
    # Config key: availableGameVariables/available_game_variables (list of values)
    # Attempt to extract the screen buffer, if available
    
    screen_buffer = None
    if game.get_screen_format() != vzd.ScreenFormat.CRCGCB:
        screen_buffer = state.screen_buffer

    # Compile extracted information into a dictionary and return it
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

