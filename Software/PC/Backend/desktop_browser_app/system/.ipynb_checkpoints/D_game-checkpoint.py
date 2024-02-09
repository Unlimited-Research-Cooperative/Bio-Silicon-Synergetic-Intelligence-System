import zmq
import vizdoom as vzd
from time import sleep
import json

def initialize_vizdoom(config_path, scenario_path):
    game = vzd.DoomGame()
    config_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.cfg"
    scenario_path = "AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/ViZDoom/scenarios/my_way_home.wad"
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.PLAYER)
    
    # Enable detailed game variables
    game.set_objects_info_enabled(True)
    
    game.init()
    return game

def decode_actions(action_str):
    # Split the received action string into individual action codes
    action_codes = [int(code) for code in action_str.split(',') if code.isdigit()]
    # Initialize an action array with all elements set to False
    action = [False] * len(vzd.Button)
    for code in action_codes:
        if code < len(action):
            action[code] = True
    return action

def extract_game_state(game):
    state = game.get_state()
    objects = state.objects
    game_variables = state.game_variables
    
    # Extract detailed information
    enemies = [obj for obj in objects if "enemy" in obj.name]  # Adjust condition based on your scenario
    enemy_locations = [(enemy.x, enemy.y) for enemy in enemies]
    player_health = game.get_game_variable(vzd.GameVariable.HEALTH)
    
    # Assuming doors and walls are identified by specific names or types in your scenario
    # Adjust these according to the actual game objects present
    doors = [obj for obj in objects if "door" in obj.name]
    walls = [obj for obj in objects if "wall" in obj.name]
    
    game_state_info = {
        "player_health": player_health,
        "enemy_locations": enemy_locations,
        "doors": len(doors),
        "walls": len(walls),
        # Add more as needed
    }
    return game_state_info

def main():
    context_pub = zmq.Context()
    publisher = context_pub.socket(zmq.PUB)
    publisher.bind("tcp://*:5446")  # Assuming this is for sending actions to the game

    context_sub = zmq.Context()
    sub_socket = context_sub.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5445")  # Assuming this is for receiving features
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    decoder = SignalDecoder()

    while True:
        try:
            message = sub_socket.recv_string()
            analyzed_features = eval(message)  # Caution: eval can be dangerous; consider safer alternatives
            
            actions = decoder.decode_features_to_actions(analyzed_features)
            
            action_message = json.dumps(actions)  # Example conversion to JSON
            publisher.send_string(action_message)

            time.sleep(1)  # Adjust based on your needs

        except zmq.ZMQError as e:
            print(f"ZMQ Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()