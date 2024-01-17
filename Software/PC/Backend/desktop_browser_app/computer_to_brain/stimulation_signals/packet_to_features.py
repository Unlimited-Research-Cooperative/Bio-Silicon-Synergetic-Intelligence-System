class PacketToFeatures:
    def __init__(self, packet):
        self.packet = packet

    def extract_features(self):
        features = {
            "variability_factor": self.scale_to_range(self.extract_bits(26, 6), 0, 1, 6),
            "variance": self.scale_to_range(self.extract_bits(24, 2), 0, 1, 2),
            "std_dev": self.scale_to_range(self.extract_bits(22, 2), 0, 1, 2),
            "rms_value": self.scale_to_range(self.extract_bits(19, 3), 0, 1, 3),
            "fractal_dimension": self.scale_to_range(self.extract_bits(15, 4), 0, 1, 4),
            "num_peaks": self.extract_bits(12, 3),
            "peak_height": self.scale_to_range(self.extract_bits(9, 3), 0, 1, 3),
            "window_size": self.extract_bits(6, 3),
            "target_rate": self.scale_to_range(self.extract_bits(3, 3), 0, 1, 3),
            "synchronization_level": self.scale_to_range(self.extract_bits(0, 3), 0, 1, 3),
            "influence_factor": self.scale_to_range(self.extract_bits(28, 4), 0, 1, 4),
            "warping_factor": self.scale_to_range(self.extract_bits(32, 4), 0, 1, 4),
            "complexity_factor": self.scale_to_range(self.extract_bits(36, 4), 0, 1, 4),
            "centroid_factor": self.scale_to_range(self.extract_bits(40, 4), 0, 1, 4),
            "edge_density_factor": self.scale_to_range(self.extract_bits(44, 4), 0, 1, 4),
            "evolution_rate": self.scale_to_range(self.extract_bits(48, 4), 0, 1, 4),
            "low_freq": self.scale_to_range(self.extract_bits(52, 4), 0, 50, 4),  
            "high_freq": self.scale_to_range(self.extract_bits(56, 4), 50, 100, 4),  
            "causality_strength": self.scale_to_range(self.extract_bits(60, 4), 0, 1, 4),
            "num_imfs": self.extract_bits(64, 4)
        }

        game_state_code = self.extract_bits_for_game_state()
        features["min_volt"], features["max_volt"] = self.determine_voltage_range(game_state_code)

        return features

    def extract_bits_for_game_state(self):
        return (self.packet >> 30) & 0x03

    def determine_voltage_range(self, game_state_code):
        if game_state_code == 1:
            return 0.5e-3, 3e-3
        elif game_state_code == 2:
            return 0.1e-3, 0.5e-3
        else:
            return 0.1e-3, 3e-3

    def extract_bits(self, start, length):
        mask = (1 << length) - 1
        return (self.packet >> start) & mask

    def scale_to_range(self, value, min_val, max_val, length):
        max_possible_value = (1 << length) - 1
        return min_val + (max_val - min_val) * (value / max_possible_value)

# Example usage
packet = 0b...  # Your 32-bit packet here
feature_extractor = PacketToFeatures(packet)
features = feature_extractor.extract_features()
print(features)
