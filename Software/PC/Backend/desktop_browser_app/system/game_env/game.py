"""
Vizdoom game environment
"""
# Import dependencies
import vizdoom as vzd
from time import sleep
from containers import EnemyState, GameState


class Game:
    def __init__(self):
        self.game_ctx = vzd.DoomGame()
        self.config_path = "./config.cfg"
        self.scenario = "./basic.wad"
        self.state = None

        # Initial setting
        self.game_ctx.set_render_hud(True)
        self.game_ctx.set_window_visible(True)
        self.game_ctx.set_mode(vzd.Mode.PLAYER)
        self.game_ctx.set_objects_info_enabled(True)
        self.game_ctx.set_screen_resolution(vzd.ScreenResolution.RES_1024X576)

        self.game_ctx.load_config(self.config_path)
        self.game_ = self.init_game()

    def init_game(self):
        return self.game_ctx.init()

    def run(self):
        self.state = self.game_ctx.get_state()
        while not self.game_ctx.is_episode_finished():
            state = self.game_ctx.get_state()
            print("Frame number:", state.number)
            action = [False] * vzd.BINARY_BUTTON_COUNT
            self.game_ctx.make_action(action, 1)
            sleep(0.02)

    def decode_actions(self, action_str: str):
        action_codes = [int(code) for code in action_str.split(',') if code.isdigit()]
        # Initialize an action array with all elements set to False
        action = [False] * len(vzd.BINARY_BUTTON_COUNT)
        for code in action_codes:
            if code < len(action):
                action[code] = True
        return action

    def get_game_state(self):
        hit_count = self.game_.get_game_variable(vzd.GameVariable.HITCOUNT)
        hits_taken = self.game_.get_game_variable(vzd.GameVariable.HITS_TAKEN)
        dead = self.game_.get_game_variable(vzd.GameVariable.DEAD) > 0
        health = self.game_.get_game_variable(vzd.GameVariable.HEALTH)
        attack_ready = self.game_.get_game_variable(vzd.GameVariable.ATTACK_READY) > 0

        enemy_state = EnemyState()

        state = self.game_.get_state()
        if state and state.labels:
            for label in state.labels:
                if label.object_name == "DoomPlayer" and label.object_id != 0:
                    enemy_state.enemy_in_view = 1.0
                    enemy_state.pos_x = label.object_position_x
                    enemy_state.pos_y = label.object_position_y
                    enemy_state.pos_z = label.object_position_z
                    enemy_state.enemy_angle = label.object_angle
                    enemy_state.enemy_pitch = label.object_pitch
                    enemy_state.enemy_roll = label.object_roll
                    enemy_state.vel_x = label.object_velocity_x
                    enemy_state.vel_y = label.object_velocity_y
                    enemy_state.vel_z = label.object_velocity_z
                    break

        screen_buff = None
        if self.game_.get_screen_format() != vzd.ScreenFormat.CRCGCB:
            screen_buff = state.screen_buffer
        else:
            print("Screen buffer format not supported or not enabled.")

        game_state = GameState()
        game_state.hit_count = hit_count
        game_state.hits_taken = hits_taken
        game_state.enemy_state = enemy_state
        game_state.screen_buffer = screen_buff
        game_state.attack_ready = attack_ready
        game_state.dead = dead
        game_state.health = health

        game_state_json = game_state.to_json()
        print(game_state_json)


game_obj = Game()
game_obj.run()
