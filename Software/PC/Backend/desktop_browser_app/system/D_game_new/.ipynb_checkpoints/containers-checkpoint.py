"""
Data structures for game state, enemy info and player info
"""
# Import dependencies
from json import dumps
from typing import Any


class Actions:
    ATTACK: str = "ATTACK"
    USE: str = "USE"
    MOVE_BACKWARD: str = "MOVE_BACKWARD"
    MOVE_FORWARD: str = "MOVE_FORWARD"
    TURN_RIGHT: str = "TURN_RIGHT"
    TURN_LEFT: str = "TURN_LEFT"


class EnemyState:
    enemy_in_view: float
    enemy_angle: float
    enemy_pitch: float
    enemy_roll: float
    pos_x: float
    pos_y: float
    pos_z: float
    vel_x: float
    vel_y: float
    vel_z: float


class GameState:
    hit_count: int
    hits_taken: int
    dead: int
    health: int
    attack_ready: int
    screen_buffer: Any
    enemy_state: EnemyState

    """
    toJson
    Args: hit_count, hits_taken, dead, health, attack_ready
    No need to pass any arguments manually
    """
    def to_json(self):
        json_data = dumps({
            "hit_count": self.hit_count,
            "hits_taken": self.hits_taken,
            "dead": self.dead,
            "health": self.health,
            "attack_ready": self.attack_ready,
            "enemy": {
                "position": {
                    "x": self.enemy_state.pos_x,
                    "y": self.enemy_state.pos_y,
                    "z": self.enemy_state.pos_z
                },
                "velocity": {
                    "x": self.enemy_state.vel_x,
                    "y": self.enemy_state.vel_y,
                    "z": self.enemy_state.vel_z,
                },
                "transform": {
                    "angle": self.enemy_state.enemy_angle,
                    "pitch": self.enemy_state.enemy_pitch,
                    "roll": self.enemy_state.enemy_roll
                }
            }
        })
        return json_data
