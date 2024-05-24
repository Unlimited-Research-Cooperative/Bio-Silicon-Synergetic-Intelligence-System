import time
import arcade
import arcade.color
from data_manager import DataManager


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600)

        self.set_caption("Shuffleboard 2D")
        self.window_width = 800
        self.window_height = 600

        self.score_blue = 0
        self.score_red = 0
        self.set_score = True

        self.first_region_blue = 640
        self.second_region_blue = 580
        self.third_region_blue = 500

        self.first_region_red = 150
        self.second_region_red = 230
        self.third_region_red = 310

        self.blue_weights = []
        self.red_weights = []
        self.weight_mass = 4  # 400 grams
        self.target_weight = None

        self.physics_engine = None
        self.physics_sprites = None

        self.data_m = DataManager("./config.ini", self.execute_input)
        self.data_m.listen()

    def setup(self):
        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.create_weights()

    # Create weights (sprites)
    def create_weights(self):
        default_height = self.window_height - 200
        for i in range(4):
            red_weight_sprite = arcade.SpriteCircle(10, arcade.color.RED)
            red_weight_sprite.center_x = self.window_width / 8
            red_weight_sprite.center_y = default_height - (i * 50)
            self.red_weights.append(red_weight_sprite)
            self.physics_engine.add_sprite(red_weight_sprite, mass=self.weight_mass)

        for i in range(4):
            blue_weight_sprite = arcade.SpriteCircle(10, arcade.color.BLUE)
            blue_weight_sprite.center_x = self.window_width * 7 / 8
            blue_weight_sprite.center_y = default_height - (i * 50)
            self.blue_weights.append(blue_weight_sprite)
            self.physics_engine.add_sprite(blue_weight_sprite, mass=self.weight_mass)

    def on_draw(self):
        self.clear()

        # Draw the table
        arcade.draw_rectangle_filled(
            self.window_width / 2,
            self.window_height / 2,
            self.window_width - 100,
            self.window_height - 200,
            arcade.color.WHITE
        )

        # Draw the weights
        for red_weight_sprite in self.red_weights:
            red_weight_sprite.draw()

        for blue_weight_sprite in self.blue_weights:
            blue_weight_sprite.draw()

    def on_update(self, delta_time):
        self.physics_engine.step()
        if self.physics_sprites != None and self.target_weight != None:
            if self.physics_sprites[self.target_weight].center_x >= 150:
                if self.set_score:
                    self.score_red += 1
                    self.set_score = False
                    self.target_weight = 0 
                    self.set_score = True

                else:
                    pass
            print(self.physics_sprites[self.target_weight].center_x)

        else:
            pass

    def execute_input(self, input_recv: str):
        self.physics_sprites = list(self.physics_engine.sprites.keys())
        inputs = input_recv.split(",")
        self.target_weight = int(inputs[0])
        force_x = int(inputs[1])
        force_y = int(inputs[2])
        self.physics_engine.apply_force(self.physics_sprites[self.target_weight], (force_x, force_y))


game = GameWindow()
game.setup()
arcade.run()
