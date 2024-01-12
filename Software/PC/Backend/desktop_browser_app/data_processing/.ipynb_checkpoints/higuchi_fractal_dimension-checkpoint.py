import higuchi_fractal 

DEFAULT_K_MAX = 5
DEFAULT_SAMPLE_LENGTH = 256

def compute_hfd_for_live_data(data, sample_length=DEFAULT_SAMPLE_LENGTH, k_max=DEFAULT_K_MAX):
    """
    Compute Higuchi Fractal Dimension for multi-channel live data.
    
    :param data: 2D numpy array where each row represents a channel
    :param sample_length: Number of latest data points to consider for each channel
    :param k_max: Maximum k value for the Higuchi algorithm
    :return: List of Higuchi Fractal Dimensions for each channel
    """
    if data.ndim != 2 or data.shape[1] < sample_length:
        raise ValueError("Data must be a 2D array with sufficient length.")

    latest_data = data[:, -sample_length:]  # Use only the most recent data

    # Call the higuchi_fd_multichannel function from the higuchi_fractal package
    return higuchi_fractal.higuchi_fd_multichannel(latest_data, k_max)

# Example usage:
# live_data = np.random.rand(32, 1000)  # Example data
# hfd_live = compute_hfd_for_live_data(live_data)
