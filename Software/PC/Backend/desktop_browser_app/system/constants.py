from typing import Any
from numpy import ndarray

NUM_CHANNELS = 32
SAMPLING_RATE = 500
UPDATE_RATE = 1

SIGNALS = "SIGNALS"
DECODED_FEATURES = "DECODED FEATURES"
GAME_INPUTS = "GAME INPUTS"


class Actions:
    MOVE_FORWARD = "MOVE_FORWARD"
    MOVE_BACKWARD = "MOVE_BACKWARD"
    TURN_LEFT = "TURN_LEFT"
    TURN_RIGHT = "TURN_RIGHT"
    USE = "USE"
    ATTACK = "ATTACK"

    @classmethod
    def to_dict(cls):
        pre_dict = {attr: value for attr, value in cls.__dict__.items() if
                    not attr.startswith('__')}
        pre_dict.pop("to_dict")
        return pre_dict


class ActionMap:
    rms: tuple = (Actions.MOVE_FORWARD, 3.96e-07)
    variance: tuple = (Actions.TURN_LEFT, 1.074e-26)
    spectral_entropy: tuple = (Actions.USE, 0.7)
    peak_counts: tuple = (Actions.ATTACK, 3)
    higuchi_fractal_dimension: tuple = (Actions.TURN_RIGHT, 1.35e-15)
    zero_crossing_rate: tuple = (Actions.MOVE_FORWARD, 0.1)
    delta_band_power: tuple = (Actions.MOVE_FORWARD, 0.5)
    theta_band_power: tuple = (Actions.MOVE_FORWARD, 0.5)
    alpha_band_power: tuple = (Actions.MOVE_FORWARD, 0.5)
    beta_band_power: tuple = (Actions.MOVE_FORWARD, 0.5)
    peak_heights: tuple = (Actions.MOVE_FORWARD, 0.5)
    std_dev: tuple = (Actions.MOVE_FORWARD, 7.5e-14)
    centroids: tuple = (Actions.MOVE_FORWARD, 0.5)
    spectral_edge_density: tuple = (Actions.MOVE_FORWARD, 0.5)
    evolution_rate: tuple = (Actions.MOVE_FORWARD, 0.5)

    @classmethod
    def to_dict(cls):
        pre_dict = {attr: value for attr, value in cls.__dict__.items() if
                    not attr.startswith('__')}
        pre_dict.pop("to_dict")
        return pre_dict


class AnalyzeSignalsResult:
    peak_height: Any
    peak_counts: int
    variance: float
    std_dev: float
    rms: float
    band_features: Any
    delta_band_power: Any
    theta_band_power: Any
    alpha_band_power: Any
    beta_band_power: Any
    centroids: Any
    spectral_edge_densities: Any
    higuchi_fractal_dimension: Any
    zero_crossing_rate: Any
    evolution_rate: Any

    @classmethod
    def to_dict(cls):
        pre_dict = {attr: value for attr, value in cls.__dict__.items() if
                    not attr.startswith('__')}
        pre_dict.pop("to_dict")
        return pre_dict

    @classmethod
    def to_python_float(cls, pre_dict: dict):
        keys = pre_dict.keys()
        vals = pre_dict.values()
        for i in range(0, len(keys)):
            if isinstance(keys[i], ndarray):
                pre_dict[str(keys[i])] = vals[i].tolist()
        return pre_dict
