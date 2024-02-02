import numpy as np
import zmq
import json
from scipy.signal import find_peaks, hilbert, welch
from scipy.fft import fft, fftfreq
import itertools

# Constants
NUM_CHANNELS = 32
FS = 500  # Sampling rate in Hz
UPDATE_RATE = 10  # Update rate in Hz
BUFFER_SIZE = FS // UPDATE_RATE  # Size of buffer corresponding to update rate

def receive_neural_data(socket):
    try:
        raw_data = socket.recv()
        neural_data = np.frombuffer(raw_data, dtype=np.float32)  # Assuming float32 for simplicity
        neural_data = neural_data.reshape(-1, NUM_CHANNELS)
        return neural_data
    except zmq.ZMQError as e:
        print(f"Error receiving data: {e}")
        return np.array([])  # Return empty array on error

def buffer_data(data, buffer):
    buffer = np.roll(buffer, -data.shape[0], axis=1)
    buffer[:, -data.shape[0]:] = data
    return buffer

def scale_data(data):
    return data / 255.0

def detect_peak_heights(signals):
    # Detecting peaks and their heights
    peak_heights = []
    for signal in signals:
        peaks, properties = find_peaks(signal, height=None)  # height=None means all peaks are considered
        heights = properties["peak_heights"]  # Get the heights of the peaks
        average_height = np.mean(heights) if len(heights) > 0 else 0
        peak_heights.append(average_height)
    return np.array(peak_heights)

def detect_peaks(signals): 
    # Detecting peaks
    peak_counts = np.array([len(find_peaks(signal)[0]) for signal in signals])
    return peak_counts

def calculate_variance_std_dev(signals):
    # Calculating variance and standard deviation
    variance = np.var(signals, axis=1) 
    std_dev = np.std(signals, axis=1)
    return variance, std_dev

def calculate_rms(signals): 
    # Calculating RMS value
    rms = np.sqrt(np.mean(signals**2, axis=1))
    return rms

def freq_bands(signals, fs=FS):
    # Assuming signals is a 2D array: channels x samples
    band_features = np.zeros((signals.shape[0], 4))  # 4 frequency bands
    for i, signal in enumerate(signals):
        frequencies, psd = welch(signal, fs, nperseg=1024)
        # Frequency bands
        bands = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30)}
        for j, (name, (low, high)) in enumerate(bands.items()):
            idx = np.logical_and(frequencies >= low, frequencies <= high)
            band_features[i, j] = np.nanmean(psd[idx])
    return band_features
    
def calculate_spectral_entropy(neural_data_array, neural_channels, fs=FS):  
    spectral_entropy_dict = {}
    for channel, signal in zip(neural_channels, neural_data_array):
        # Calculate the power spectral density (PSD) using Welch's method
        frequencies, psd = welch(signal, fs=fs, nperseg=fs*2)
        # Normalize the PSD to get a probability distribution for entropy calculation
        normalized_psd = psd / np.sum(psd)
        # Calculate the spectral entropy
        spectral_entropy = -np.sum(normalized_psd * np.log2(normalized_psd))
        # Store the spectral entropy in the dictionary with the channel name as the key
        spectral_entropy_dict[channel] = spectral_entropy
    return spectral_entropy_dict

def spectral_centroids(signals, fs=FS): 
    # Calculate the spectral centroids for each signal
    centroids = []
    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0/fs)
        magnitude = np.abs(fft_result)
        centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
        centroids.append(centroid)
    return np.array(centroids)

def spectral_edge_density(signals, fs=FS, percentage=95):
    # Loop through each channel and calculate spectral edge density
    spectral_edge_densities = []
    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0/fs)
        positive_frequencies = frequencies[frequencies >= 0]
        positive_fft_result = fft_result[frequencies >= 0]
        magnitude = np.abs(positive_fft_result)
        sorted_magnitude = np.sort(magnitude)[::-1]
        cumulative_sum = np.cumsum(sorted_magnitude)
        total_power = np.sum(magnitude)
        threshold = total_power * (percentage / 100)
        spectral_edge = positive_frequencies[np.argmax(cumulative_sum >= threshold)]
        spectral_edge_densities.append(spectral_edge)
    return np.array(spectral_edge_densities)

def phase_synchronization(signals):
    num_channels = signals.shape[0]
    plv_matrix = np.zeros((num_channels, num_channels))
    for i, j in itertools.combinations(range(num_channels), 2):
        plv_matrix[i, j] = compute_phase_locking_value(signals[i], signals[j])
        plv_matrix[j, i] = plv_matrix[i, j]
    return plv_matrix
    
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
for channel_data in neural_data.T:  # .T because we need to iterate over channels
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

def time_warping_factor(signals): 
    # Calculate the average signal (mean across all signals for each time point)
    average_signal = np.mean(np.array(signals), axis=0)
    warping_factors = []
    for signal in signals:
        # Calculate the DTW distance between the signal and the average signal
        distance, _ = fastdtw(signal, average_signal, dist=euclidean)
        # Append the distance as the warping factor for this signal
        warping_factors.append(distance)
    return warping_factors

def evolution_rate(signals): 
    rates = np.zeros(signals.shape[0])
    for i, signal in enumerate(signals):
        # Compute the analytic signal
        analytic_signal = hilbert(signal)
        # Calculate the envelope
        envelope = np.abs(analytic_signal)
        # Calculate the derivative of the envelope
        derivative = np.diff(envelope)
        # Compute the evolution rate as the average absolute derivative of the envelope
        rates[i] = np.mean(np.abs(derivative))
    return rates

def analyze_signals(signals):
    # Define `k_max` for Higuchi's fractal dimension calculation
    k_max = 5  # Example value; adjust based on your signal analysis needs
    
    # Analysis results
    peak_heights = detect_peak_heights(signals)
    peak_counts = detect_peaks(signals)
    variance, std_dev = calculate_variance_std_dev(signals)
    rms = calculate_rms(signals)
    band_features = freq_bands(signals, FS)
    spectral_entropy = calculate_spectral_entropy(signals, FS)
    centroids = spectral_centroids(signals, FS)
    spectral_edge_densities = spectral_edge_density(signals, FS, 95)
    plv_matrix = phase_synchronization(signals)
    hfd_values = calculate_higuchi_fractal_dimension(signals, k_max)
    zero_crossing_rate = calculate_zero_crossing_rate(signals)
    imfs = perform_empirical_mode_decomposition(signals)
    warping_factors = time_warping_factor(signals)
    rates = evolution_rate(signals)

    results = {
        'variance': variance.tolist(),
        'std_dev': std_dev.tolist(),
        'rms': rms.tolist(),
        'peak_counts': peak_counts.tolist(),
        'band_features': band_features.tolist(),
        'spectral_entropy': list(spectral_entropy.values()),
        'centroids': centroids.tolist(),
        'spectral_edge_densities': spectral_edge_densities.tolist(),
        'phase_synchronization': plv_matrix.tolist(),
        'higuchi_fractal_dimension': hfd_values,
        'zero_crossing_rate': zero_crossing_rate.tolist(),
        'empirical_mode_decomposition': [imf.tolist() for imf in imfs],  # Assuming `imfs` is an array of IMFs
        'time_warping_factor': warping_factors.tolist(),
        'evolution_rate': rates.tolist(),
    }
    return results

def main():
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://localhost:5444")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:5445")
    
    buffer = np.zeros((NUM_CHANNELS, BUFFER_SIZE), dtype=np.float32)

    while True:
        neural_data = receive_neural_data(sub_socket)
        if neural_data.size > 0:
            scaled_data = scale_data(neural_data)  # If scaling is necessary
            buffer = buffer_data(scaled_data, buffer)
            if np.all(buffer != 0):  # Assuming buffer is correctly filled
                analysis_results = analyze_signals(buffer.T)  # Ensure signals are rows in buffer
                serialized_results = json.dumps(analysis_results)
                pub_socket.send_string(serialized_results)

if __name__ == "__main__":
    main()