import numpy as np
import zmq
import json
from scipy.signal import find_peaks, hilbert, welch
from scipy.fft import fft, fftfreq
import itertools
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import logging

# Constants
NUM_CHANNELS = 32
FS = 500  # Sampling rate in Hz
UPDATE_RATE = 1  # Update rate in Hz
BUFFER_SIZE = int(FS // UPDATE_RATE)  # Size of buffer corresponding to update rate

def receive_neural_data(socket):
    try:
        message = socket.recv()  # Receive the message
        ecog_data = json.loads(message.decode('utf-8'))  # Decode and load the JSON data
        neural_data = np.array(ecog_data, dtype=np.float32)  # Convert the list to a NumPy array
        return neural_data
    except zmq.ZMQError as e:
        print(f"Error receiving data: {e}")
        return None

def buffer_data(data, buffer):
    buffer = np.roll(buffer, -data.shape[0], axis=1)
    buffer[:, -data.shape[0]:] = data
    return buffer

def scale_data(data, fs=FS, factor=2):
    # Simple subsampling by taking every 'factor'-th sample
    subsampled_data = data[:, ::factor]

    # Scaling to range [0, 1]
    data_min = np.min(subsampled_data, axis=1, keepdims=True)
    data_max = np.max(subsampled_data, axis=1, keepdims=True)

    # Avoid division by zero in case data_max equals data_min
    scaled_data = (subsampled_data - data_min) / np.where(data_max > data_min, data_max - data_min, 1)

    return scaled_data

def detect_peaks(signals):
        # Dynamically setting parameters based on signal characteristics
        median_height = np.median(signal)
        std_height = np.std(signal)
        height = median_height + std_height  # Setting height to be above median + 1 std deviation
        distance = len(signal) * 0.05  # Example to set distance to 5% of signal length
        prominence = std_height * 0.5  # Setting prominence to be half of std deviation
        
        # Detecting peaks
        peaks, properties = find_peaks(signal, height=height, distance=distance, prominence=prominence)
        
        # Calculating properties if peaks were found
        if peaks.size > 0:
            peak_count = len(peaks)
            average_peak_height = np.mean(properties["peak_heights"])
            average_distance = np.mean(np.diff(peaks)) if len(peaks) > 1 else 0
            average_prominence = np.mean(properties["prominences"])
        else:
            peak_count = 0
            average_peak_height = 0
            average_distance = 0
            average_prominence = 0
            
        # Appending results for each channel
        peaks_results.append({
            "peak_count": peak_count,
            "average_peak_height": average_peak_height,
            "average_distance": average_distance,
            "average_prominence": average_prominence,
        })
    
    return peaks_results

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
    band_features = np.zeros((signals.shape[0], 4))

    for i, signal in enumerate(signals):
        
        nperseg = min(32, len(downsampled_signal))
        
        frequencies, psd = welch(downsampled_signal, fs=FS, nperseg=nperseg)
        
        print("Frequencies:", frequencies)
        print("PSD:", psd)
        
        bands = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30)}
        for j, (name, (low, high)) in enumerate(bands.items()):
            idx = np.logical_and(frequencies >= low, frequencies <= high)
            if np.any(idx):
                band_features[i, j] = np.nanmean(psd[idx])
            else:
                band_features[i, j] = 0.0
    
    return band_features


def calculate_spectral_entropy(neural_data_array, fs):  
    # Initialize an array to hold spectral entropy values for each channel
    spectral_entropy_values = np.zeros(neural_data_array.shape[0])
    
    for i, signal in enumerate(neural_data_array):
        # Determine nperseg based on the length of the signal
        nperseg = min(len(signal), fs * 2)
        # Calculate the power spectral density (PSD) using Welch's method
        frequencies, psd = welch(signal, fs=fs, nperseg=nperseg)
        
        # Check if the sum of psd is zero
        if np.sum(psd) == 0:
            spectral_entropy_values[i] = 0.0  # Set spectral entropy to 0
        else:
            # Normalize the PSD to get a probability distribution for entropy calculation
            normalized_psd = psd / np.sum(psd)
            # Calculate the spectral entropy
            spectral_entropy = -np.sum(normalized_psd * np.log2(normalized_psd))
            # Store the spectral entropy value in the array
            spectral_entropy_values[i] = spectral_entropy
    
    return spectral_entropy_values

def spectral_centroids(signals, fs): 
    # Calculate the spectral centroids for each signal
    centroids = []
    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0/fs)
        magnitude = np.abs(fft_result)
        centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
        centroids.append(centroid)
    return centroids

def spectral_edge_density(signals, fs, percentage=95):
    spectral_edge_densities = []

    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0/fs)
        positive_frequencies = frequencies[frequencies >= 0]
        positive_fft_result = fft_result[frequencies >= 0]
        magnitude = np.abs(positive_fft_result)
        cumulative_sum = np.cumsum(np.sort(magnitude)[::-1])
        total_power = np.sum(magnitude)
        threshold = total_power * (percentage / 100)
        spectral_edge = positive_frequencies[np.argmax(cumulative_sum >= threshold)]
        spectral_edge_densities.append(spectral_edge)  

    return spectral_edge_densities

def phase_locking_values(signal1, signal2):
    # Compute the analytical signal for each input signal
    num_signals = signals.shape[0]
    plv_matrix = np.zeros((num_signals, num_signals))

    for i in range(num_signals):
        for j in range(i+1, num_signals):  # Only compute for unique pairs
            signal1 = signals[i]
            signal2 = signals[j]
            
            # Compute the analytical signal for each input signal
            analytic_signal1 = hilbert(signal1)
            analytic_signal2 = hilbert(signal2)
            
            # Compute the instantaneous phase for each analytical signal
            phase1 = np.angle(analytic_signal1)
            phase2 = np.angle(analytic_signal2)
            
            # Compute the phase difference
            phase_diff = phase1 - phase2
            
            # Compute the PLV
            plv = np.abs(np.sum(np.exp(1j * phase_diff)) / len(signal1))
            
            # Store the PLV in the matrix
            plv_matrix[i, j] = plv
            plv_matrix[j, i] = plv  # PLV is symmetric

    return plv_matrix

def calculate_higuchi_fractal_dimension(signals, k_max):
    hfd_values = []  # To store HFD for each channel
    
    for signal in signals:
        N = len(signal)
        L = []
        x = np.asarray(signal)
        for k in range(1, k_max + 1):
            Lk = []
            for m in range(k):
                Lkm_sum = 0
                max_index = int((N - m - 1) / k) + 1  # Ensures valid indexing
                for i in range(1, max_index):
                    Lkm_sum += abs(x[m + i*k] - x[m + (i-1)*k])
                if max_index - 1 > 0:  # Check to avoid division by zero
                    Lkm = Lkm_sum * (N - 1) / (k * (max_index - 1))
                    Lk.append(Lkm)
                else:
                    Lk.append(0)  # Or handle appropriately
                
            # Check if Lk contains non-zero values before taking log
            if np.mean(Lk) > 0:
                L.append(np.log(np.mean(Lk)))
            else:
                # Handle the case where np.mean(Lk) results in 0 or a negative number
                # For example, append a very small positive value or handle as an error
                L.append(np.log(np.finfo(float).eps))  # Using machine epsilon for a small positive number

        # Proceed with polyfit only if L contains valid log values
        if len(L) > 0 and np.all(np.isfinite(L)):
            hfd = np.polyfit(np.log(range(1, k_max + 1)), L, 1)[0]  # Linear fit to log-log plot
            hfd_values.append(hfd)
        else:
            # Handle the case where HFD cannot be computed due to invalid L values
            hfd_values.append(np.nan)  # Append NaN or another placeholder to indicate failure
    
    return hfd_values

def calculate_zero_crossing_rate(signals):
    sign_changes = np.diff(np.sign(signals), axis=1)
    zero_crossings = np.count_nonzero(sign_changes, axis=1)
    zero_crossing_rates = zero_crossings / (signals.shape[1] - 1)
    
    print("Sign Changes:", sign_changes)
    print("Zero Crossings:", zero_crossings)
    
    return zero_crossing_rates

def perform_empirical_mode_decomposition(signals):
    # Initialize EMD
    emd = EMD()
    
    # Initialize an empty list to store IMFs for each signal
    imfs_all_signals = []
    
    # Loop through each signal
    for signal in signals:
        # Perform EMD decomposition for the current signal
        imfs = emd(signal)
        
        # Append the IMFs of the current signal to the list
        imfs_all_signals.append(imfs)
    
    # Convert the list of IMFs into a NumPy array
    imfs_all_signals = np.array(imfs_all_signals)
    
    return imfs

def time_warping_factor(signals): 
    # Calculate the average signal (mean across all signals for each time point)
    average_signal = np.mean(np.array(signals), axis=0)
    warping_factors = []
    for signal in signals:
        # Ensure that the signals are 1-D
        signal = np.atleast_1d(signal)
        average_signal = np.atleast_1d(average_signal)
        
        print("Signal shape:", signal.shape)
        print("Average signal shape:", average_signal.shape)
        distance, _ = fastdtw(np.squeeze(signal), np.squeeze(average_signal), dist=euclidean)
        

        
        # Calculate the DTW distance between the signal and the average signal
        distance, _ = fastdtw(np.squeeze(signal), np.squeeze(average_signal), dist=euclidean)

        # Append the distance as the warping factor for this signal
        warping_factors.append(distance)
    return warping_factors

def evolution_rate(signals):
    rates = np.zeros(signals.shape[0])

    for i, signal in enumerate(signals):
        analytic_signal = hilbert(signal)
        envelope = np.abs(analytic_signal)
        derivative = np.diff(envelope)
        rates[i] = np.mean(np.abs(derivative))
        
        print("Analytic Signal:", analytic_signal)
        print("Envelope:", envelope)
        print("Derivative:", derivative)
    
    return rates

def analyze_signals(buffer):
    signals = buffer.T  # Assuming signals are organized as channels x samples in the buffer
    
    peak_heights = detect_peak_heights(signals)
    peak_counts = detect_peaks(signals)
    variance, std_dev = calculate_variance_std_dev(signals)
    rms = calculate_rms(signals)
    band_features = freq_bands(signals, FS)  # Assuming this returns an array of shape (num_signals, num_bands)
    # Assuming band_features order: delta, theta, alpha, beta
    delta_band_power = band_features[:, 0]  # Delta band powers for all signals
    theta_band_power = band_features[:, 1]  # Theta band powers for all signals
    alpha_band_power = band_features[:, 2]  # Alpha band powers for all signals
    beta_band_power = band_features[:, 3]  # Beta band powers for all signals
    #spectral_entropy_values = spectral_entropy_values(signals, FS)
    centroids = spectral_centroids(signals, FS)
    spectral_edge_densities = spectral_edge_density(signals, FS, 95)
    #plv = phase_locking_values(signals) 
    hfd_values = calculate_higuchi_fractal_dimension(signals, k_max=10)
    zero_crossing_rate = calculate_zero_crossing_rate(signals)
    #imfs = perform_empirical_mode_decomposition(signals) 
    #warping_factors = time_warping_factor(signals)
    rates = evolution_rate(signals)

    # Convert float32 values to Python floats in the results dictionary
    results = {
        'peak_heights': peak_heights.tolist() if isinstance(peak_heights, np.ndarray) else peak_heights,
        'peaks': peak_counts.tolist() if isinstance(peak_counts, np.ndarray) else peak_counts,
        'variance': variance.tolist() if isinstance(variance, np.ndarray) else variance,
        'std_dev': std_dev.tolist() if isinstance(std_dev, np.ndarray) else std_dev,
        'rms': rms.tolist() if isinstance(rms, np.ndarray) else rms,
        'delta_band_power': delta_band_power.tolist() if isinstance(delta_band_power, np.ndarray) else delta_band_power,
        'theta_band_power': theta_band_power.tolist() if isinstance(theta_band_power, np.ndarray) else theta_band_power,
        'alpha_band_power': alpha_band_power.tolist() if isinstance(alpha_band_power, np.ndarray) else alpha_band_power,
        'beta_band_power': beta_band_power.tolist() if isinstance(beta_band_power, np.ndarray) else beta_band_power,
        #'spectral_entropy...
        'centroids': centroids.tolist() if isinstance(centroids, np.ndarray) else centroids,
        'spectral_edge_densities': spectral_edge_densities.tolist() if isinstance(spectral_edge_densities, np.ndarray) else spectral_edge_densities,
        #'phase_synchronization': plv.tolist(),
        'higuchi_fractal_dimension': hfd_values if isinstance(hfd_values, list) else hfd_values.tolist(),
        'zero_crossing_rate': zero_crossing_rate.tolist() if isinstance(zero_crossing_rate, np.ndarray) else zero_crossing_rate,
        #'empirical_mode_decomposition': [imf.tolist() for imf in imfs],
        #'time_warping_factor': warping_factors.tolist(),
        'evolution_rate': rates.tolist() if isinstance(rates, np.ndarray) else rates,
    }

        # Print the results
    print("Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
        
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
        # Inside main(), after receiving and checking neural_data
        if neural_data is not None and neural_data.size > 0:
            scaled_data = scale_data(neural_data)  # Scale the received data
            buffer = buffer_data(scaled_data, buffer)  # Buffer the scaled data
            
            # Once the buffer is ready for analysis
            if np.all(buffer != 0):  # Assuming buffer is filled to a point where analysis is meaningful
                analysis_results = analyze_signals(buffer)  # Analyze the buffered signals
                serialized_results = json.dumps(analysis_results)  # Serialize analysis results
                pub_socket.send_string(serialized_results)  # Send the results

        else:
            print("No neural data received or neural_data is empty.")
        # Inside the while loop of the main function
        message = sub_socket.recv_string()
        analyzed_features = json.loads(message)

if __name__ == "__main__":
    main()