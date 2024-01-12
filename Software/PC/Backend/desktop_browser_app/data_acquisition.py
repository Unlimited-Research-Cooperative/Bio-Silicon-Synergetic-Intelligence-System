import numpy as np
import time

class SimulatedBoard:
    def __init__(self, file_path, sample_rate_hz=250):
        self.neural_signals = np.load(file_path)
        self.sample_rate_hz = sample_rate_hz
        self.sample_interval = 1.0 / sample_rate_hz
        self.current_sample_index = 0

    def get_current_data(self, num_samples):
        """
        Get the current data from the simulated board.

        :param num_samples: Number of samples to retrieve.
        :return: The current data as a numpy array.
        """
        end_index = self.current_sample_index + num_samples
        if end_index > self.neural_signals.shape[1]:
            end_index -= self.neural_signals.shape[1]
            self.current_sample_index = 0

        data = self.neural_signals[:, self.current_sample_index:end_index]
        self.current_sample_index = end_index
        time.sleep(self.sample_interval * num_samples)  # Simulate delay for real-time acquisition
        return data

# Initialize the simulated board when the module is imported
file_path = '/home/vincent/AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/EEG_Chaos_Kuramoto_Neural_Net/eeg_data_with_channels.npy'  # Replace with your actual file path
simulated_board = SimulatedBoard(file_path)

def start_board():
    # Placeholder for starting the board, if needed
    pass

def stop_board():
    # Placeholder for stopping the board, if needed
    pass

def get_live_data(num_samples=250):
    """
    Get 'live' data for the current time window.

    :param num_samples: Number of samples to retrieve.
    :return: 'Live' data as a numpy array.
    """
    return simulated_board.get_current_data(num_samples)
