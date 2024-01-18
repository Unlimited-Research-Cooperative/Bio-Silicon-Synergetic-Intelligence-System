import numpy as np
from scipy.signal import find_peaks, hilbert
from scipy.fft import fft

def calculate_variance_std_dev(signals):
    # Calculating variance and standard deviation
    variance = np.var(signals, axis=1)
    std_dev = np.std(signals, axis=1)
    return variance, std_dev

def calculate_rms(signals):
    # Calculating RMS value
    rms = np.sqrt(np.mean(signals**2, axis=1))
    return rms
    
def detect_peaks(signals):
    # Detecting peaks
    peak_counts = np.array([len(find_peaks(signal)[0]) for signal in signals])
    return peak_counts
    
def freq_bands(signals):
    # Use Welch's method to estimate the power spectral density
frequencies, psd = signal.welch(eeg_data, fs, nperseg=1024)

# Define frequency bands of interest (you can adjust these according to your requirements)
delta_band = (1, 4)    # Delta band (1-4 Hz)
theta_band = (4, 8)    # Theta band (4-8 Hz)
alpha_band = (8, 13)   # Alpha band (8-13 Hz)
beta_band = (13, 30)   # Beta band (13-30 Hz)

# Find indices corresponding to each frequency band
delta_indices = np.where((frequencies >= delta_band[0]) & (frequencies <= delta_band[1]))[0]
theta_indices = np.where((frequencies >= theta_band[0]) & (frequencies <= theta_band[1]))[0]
alpha_indices = np.where((frequencies >= alpha_band[0]) & (frequencies <= alpha_band[1]))[0]
beta_indices = np.where((frequencies >= beta_band[0]) & (frequencies <= beta_band[1]))[0]

# Extract power values for each frequency band
delta_power = np.nanmean(psd[delta_indices])
theta_power = np.nanmean(psd[theta_indices])
alpha_power = np.nanmean(psd[alpha_indices])
beta_power = np.nanmean(psd[beta_indices])

# Create a feature array from the power values
features = np.array([delta_power, theta_power, alpha_power, beta_power])

# Save the features as a numpy array
save_path = '/home/vincent/AAA_projects/MVCS/Neuroscience/Analysis/Spectral Analysis/welchs_x.npy'
np.save(save_path, features)

def spectral_entropy(signals):
    # Initialize a dictionary to store the spectral entropy for each channel
spectral_entropy_dict = {}

# Loop through each EEG channel
for channel in eeg_channels:
    # Select EEG data from the current channel
    eeg_data = eeg_data_array[:, eeg_channels.index(channel)]
    
    # Calculate the power spectral density using Welch's method
    f, Pxx = welch(eeg_data, fs=fs, nperseg=fs*2)
    
    # Normalize the power spectrum
    normalized_Pxx = Pxx / np.sum(Pxx)
    
    # Calculate the spectral entropy
    spectral_entropy = -np.sum(normalized_Pxx * np.log2(normalized_Pxx))
    
    # Store the spectral entropy in the dictionary
    spectral_entropy_dict[channel] = spectral_entropy

# Save the spectral entropy values as a numpy array
results_file = "SpectralEntropy_x.npy"
np.save(results_folder_path + results_file, spectral_entropy_dict)

# Extract channel names and corresponding spectral entropy values
channels = list(spectral_entropy_dict.keys())
entropy_values = list(spectral_entropy_dict.values())



def spectral_centroids(signals):
    # Initialize a dictionary to store the spectral centroids for each channel
spectral_centroids = {}

# Loop through each channel and calculate spectral centroid
for channel in eeg_channels:
    eeg_data = eeg_data_array[:, eeg_channels.index(channel)]  # Get the data from the array
    
    # Perform Fourier transform on the data
    fft_result = scipy.fft.fft(eeg_data)
    
    # Generate frequencies associated with the Fourier transform values
    frequencies = scipy.fft.fftfreq(len(eeg_data), 1.0/fs)

    # Calculate the absolute values of the Fourier transform results
    magnitude = np.abs(fft_result)
    
    # Compute the spectral centroid
    spectral_centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
    
    # Add the spectral centroid to the dictionary
    spectral_centroids[channel] = spectral_centroid



def spectral_edge_density(signals):
    # Define the percentage of the total power used to calculate the spectral edge density
percentage = 95

# Initialize a dictionary to store the spectral edge densities for each channel
spectral_edge_densities = {}

# Loop through each channel and calculate spectral edge density
for channel in eeg_channels:
    eeg_data = eeg_data_array[:, eeg_channels.index(channel)]  # Get the data from the array

    # Perform Fourier transform on the data
    fft_result = scipy.fft.fft(eeg_data)

    # Generate frequencies associated with the Fourier transform values
    frequencies = scipy.fft.fftfreq(len(eeg_data), 1.0/fs)

    # Keep only the positive frequencies (since the spectrum is symmetric)
    positive_frequencies = frequencies[frequencies >= 0]
    positive_fft_result = fft_result[frequencies >= 0]

    # Calculate the absolute values of the Fourier transform results
    magnitude = np.abs(positive_fft_result)

    # Sort the magnitude array in descending order
    sorted_magnitude = np.sort(magnitude)[::-1]

    # Calculate the cumulative sum of the sorted magnitude array
    cumulative_sum = np.cumsum(sorted_magnitude)

    # Calculate the threshold based on the specified percentage of total power
    total_power = np.sum(magnitude)
    threshold = total_power * percentage / 100

    # Find the frequency where the cumulative sum first exceeds the threshold
    spectral_edge = positive_frequencies[np.argmax(cumulative_sum >= threshold)]

    # Add the spectral edge density to the dictionary
    spectral_edge_densities[channel] = spectral_edge



def phase_synchronization(signals):
    num_channels = len(eeg_channel_names)
plv_matrix = np.zeros((num_channels, num_channels))

for i, j in itertools.combinations(range(num_channels), 2):
    plv_matrix[i, j] = compute_phase_locking_value(EEG_data[:, i], EEG_data[:, j])
    plv_matrix[j, i] = plv_matrix[i, j]


def transfer_entropy(signals):
    





def calculate_higuchi_fractal_dimension(signals, k_max):
    N = len(signals)
    L = []
    
    x = np.asarray(signals)
    
    for k in range(1, k_max):
        Lk = []
        
        for m in range(0, k):
            Lkm = 0
            for i in range(1, int((N-m)/k)):
                Lkm += abs(x[m+i*k] - x[m+i*k-k])
            Lkm = Lkm*(N - 1)/(((N - m)/k)*k)
            Lk.append(Lkm)
            
        L.append(np.log(np.mean(Lk)))
    
    hfd = np.polyfit(np.log(range(1, k_max)), L, 1)[0]
    
    return higuchi_fractal_dimensions

hfd_values = []

for channel_data in EEG_data.T:  # .T because we need to iterate over channels
    hfd_channel = higuchi_fd(channel_data, k_max=10)  # Adjust k_max as needed
    hfd_values.append(hfd_channel)





def calculate_zero_crossing_rate(signals):
    # Calculating zero-crossing rate
    zero_crossing_rates = np.array([((signal[:-1] * signal[1:]) < 0).sum() for signal in signals]) / len(signals[0])
    return zero_crossing_rates



def perform_empirical_mode_decomposition(signals):
    # EMD analysis (placeholder for actual implementation)
    imfs = np.array([compute_emd(signal) for signal in signals])
    return imfs

# Add other analysis functions as needed...

def analyze_signals(signals):
    # Main analysis function that calls all other functions
    results = {
        'variance': calculate_variance_std_dev(signals),
        'rms': calculate_rms(signals),
        'fractal_dimension': calculate_fractal_dimension(signals),
        'peak_counts': detect_peaks(signals),
        'spectral_content': perform_spectral_analysis(signals),
        'zero_crossing_rate': calculate_zero_crossing_rate(signals),
        'phase_synchronization': analyze_phase_synchronization(signals),
        'emd': perform_empirical_mode_decomposition(signals),
        # Add other analyses as needed...
    }
    return results

# Example usage
# neural_signals = np.random.rand(8, 1000)  # Example neural signals
# analysis_results = analyze_signals(neural_signals)
