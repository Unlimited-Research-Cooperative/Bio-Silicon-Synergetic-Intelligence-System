# import client
from os import getcwd
from time import time
from threading import Thread
from PySide6.QtCore import QSettings

settings_obj = QSettings("config/config.ini", QSettings.Format.IniFormat)
settings_obj.setValue("export_path", str(getcwd()))


def get_features():
    with open("signals_simulator/config/features.txt", "r") as features_file:
        features = [feature.rstrip("\n") for feature in features_file.readlines()]
        features_file.close()
        return features


def get_val(key: str, return_type: str):
    val = settings_obj.value(key)
    if return_type == "str":
        return str(val)

    elif return_type == "int":
        return int(val)

    elif return_type == "float":
        return float(val)


def get_all_vals() -> list:
    vals = []
    keys = settings_obj.allKeys()
    for i in range(0, len(keys)):
        vals.append(settings_obj.value(keys[i]))
    return vals


def update_vals(features: list, vals: list):
    for i in range(0, len(features)):
        settings_obj.setValue(f"features/{features[i]}", vals[i])


def create_features_dict(features: list, vals: list) -> dict:
    # Dummy list
    # Define the features dictionary with the required values
    features_dict = {
        "min_volt": 1e-6,  # 1 micro volt
        "max_volt": 8e-5,  # 8 micro-volts
        "variability_factor": 0.1,  # Direct mapping of player movement to variability factor, normalized to a 0-1 scale
        "variance": 0.01,  # Mapping door state to variance feature
        "std_dev": 0.05,  # Mapping enemy type to standard deviation feature
        "rms_value": 0.02,  # Player health state affects the RMS value feature
        "num_peaks": 5,  # Number of peaks determined by exploring states
        "peak_height": 0.05,  # Peak height influenced by level state
        "fractal_dimension": 0.2,  # Action states influence the fractal dimension
        "window_size": 10,  # Window size feature influenced by wall states
        "target_rate": 0.1,  # Target rate is determined by the presence of any enemy type
        "min_freq": 0.5,
        # Minimum frequency affected by player movement, demonstrating a range for frequency based on movement
        "max_freq": 1.5,
        # Maximum frequency influenced by player health state, indicating a dynamic range based on health
        "blend_factor": 0.2,  # Static blend factor as a static state
        "global_sync_level": 0.1,  # Global sync level determined by action state, reflecting synchronization needs
        "pairwise_sync_level": 0.2,
        # Pairwise sync level affected by door state, indicating sync adjustments based on environmental factors
        "sync_factor": 0.05,  # Sync factor as a static value for simplicity
        "influence_factor": 0.1,  # Influence factor derived from enemy type, representing external influence levels
        "max_influence": 0.02,  # Maximum influence as a static maximum for the presence of any enemy
        "centroid_factor": 0.1,  # Centroid factor and edge density factor as placeholders for sensory data encoding
        "edge_density_factor": 0.2,  # Centroid factor and edge density factor as placeholders for sensory data encoding
        "complexity_factor": 0.1,  # Example value for complexity factor in FFT
        "evolution_rate": 0.05,  # Evolution rate as a static value for dynamic environmental changes
        "low_freq": 0.5,  # Low frequency ranges influenced by exploring states
        "high_freq": 2.0,  # High frequency ranges influenced by level states
        "causality_strength": 0.1,  # Causality strength as a static value for interaction effects
        "num_imfs": 5,  # Number of intrinsic mode functions (IMFs) as a static value for interaction effects
    }
    vals.pop(0)
    for i in range(0, len(vals)):
        features_dict[features[i]] = float(vals[i])
        print(f"{features_dict[features[i]]} = {vals[i]}")

    return features_dict


# def publish_data(topic: str, ecog_data: list):
#     start_time = time()
#     client.client.publish("ecog_data", ecog_data)
#     elapsed_time = time() - start_time
#
#     print("--------------------")
#     print("ECoG data for all channels:")
#     for channel, data in enumerate(ecog_data, start=1):
#         print(f"Channel {channel}: {data}")
#     print("--------------------")
#
#     return start_time, elapsed_time
#
#
# def start_new_thread(func, args: list):
#     publish_thread = Thread(target=func, args=args)
#     publish_thread.start()
