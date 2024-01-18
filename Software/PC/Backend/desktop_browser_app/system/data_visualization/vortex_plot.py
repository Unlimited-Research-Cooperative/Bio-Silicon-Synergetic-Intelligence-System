import numpy as np
import matplotlib.pyplot as plt

def plot_signals_on_circle(signals, radii_increment, sampling_rate):
    num_signals = signals.shape[0]
    duration = signals.shape[1] / sampling_rate
    theta = np.linspace(0, -2 * np.pi, signals.shape[1])  # Change theta direction to clockwise

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 8))

    # Hide the radial grid lines
    ax.yaxis.grid(False)

    # Set the axis background color to transparent
    ax.patch.set_visible(False)
    
    # Hide the axis line
    ax.spines['polar'].set_visible(False)

    # Set the thetagrids to match 0.25 second increments
    ax.set_thetagrids(np.arange(0, 360, 90), labels=[f'{duration - x * duration / 4:.2f}s' for x in range(4)])  # Adjust labels for clockwise direction

    for i in range(num_signals):
        radius = (i + 1) * radii_increment + signals[i]
        ax.plot(theta, radius, linewidth=1, color='red')  # Make all signal lines red

    plt.show()

# Example usage:
num_signals = 8  # Number of signals
sampling_rate = 1000  # Sampling rate in Hz
signal_length = 1000  # Number of samples
radii_increment = 1  # Distance between each signal

# Generate some example signals, replace this with your actual signals
signals = np.random.rand(num_signals, signal_length)

plot_signals_on_circle(signals, radii_increment, sampling_rate)