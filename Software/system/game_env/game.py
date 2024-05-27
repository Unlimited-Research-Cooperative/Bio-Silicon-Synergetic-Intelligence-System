"""
Vizdoom game environment
"""
# Import dependencies
import vizdoom as vzd
from time import sleep
from threading import Thread


class Actions:
    MOVE_LEFT: list[int] = [1, 0, 0, 0, 0]
    MOVE_RIGHT: list[int] = [0, 1, 0, 0, 0]
    ATTACK: list[int] = [0, 0, 1, 0, 0]
    MOVE_FORWARD: list[int] = [0, 0, 0, 1, 0]
    MOVE_BACKWARD: list[int] = [0, 0, 0, 0, 1]


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
        self.game_ctx.set_screen_resolution(vzd.ScreenResolution.RES_800X600)

        self.game_ctx.load_config(self.config_path)

        # Add important buttons
        self.game_ctx.add_available_button(vzd.Button.MOVE_FORWARD)
        self.game_ctx.add_available_button(vzd.Button.MOVE_BACKWARD)

        self.game_ = self.init_game()

        print(self.game_ctx.get_available_buttons())

    def init_game(self):
        return self.game_ctx.init()

    def run(self):
        self.state = self.game_ctx.get_state()
        while not self.game_ctx.is_episode_finished():
            state = self.game_ctx.get_state()
            self.game_ctx.make_action(Actions.MOVE_FORWARD, 1)
            sleep(0.02)

    def run_game(self):
        thread = Thread(target=self.run)
        thread.start()


if __name__ == "__main__":
    game = Game()
    game.run_game()
