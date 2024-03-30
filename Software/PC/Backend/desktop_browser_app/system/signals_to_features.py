import constants
import numpy as np
from PyEMD import EMD
from fastdtw import fastdtw
from json import loads, dumps
from scipy.fft import fft, fftfreq
from data_manager import DataManager
from scipy.spatial.distance import euclidean
from scipy.signal import find_peaks, welch, hilbert

BUFFER_SIZE = int(constants.SAMPLING_RATE // constants.UPDATE_RATE)


def buffer_data(data, buffer):
    buffer = np.roll(buffer, -data.shape[0], axis=1)
    buffer[:, -data.shape[0]:] = data
    return buffer


def scale_data(data, factor=2):
    if data.ndim != 2 or data.shape[0] != 32:
        raise ValueError(f"Unexpected data shape: {data.shape}. Expected (32, number_of_samples).")
    # Simple subsampling by taking every 'factor'-th sample
    subsampled_data = data[:, ::factor]

    # Scaling to range [0, 1]
    data_min = np.min(subsampled_data, axis=1, keepdims=True)
    data_max = np.max(subsampled_data, axis=1, keepdims=True)

    # Avoid division by zero in case data_max equals data_min
    scaled_data = (subsampled_data - data_min) / np.where(data_max > data_min, data_max - data_min, 1)

    return scaled_data


def detect_peaks(signals):
    peaks_results = []
    # Dynamically setting parameters based on signal characteristics
    median_height = np.median(signals)
    std_height = np.std(signals)
    height = median_height + std_height  # Setting height to be above median + 1 std deviation
    distance = len(signals) * 0.05  # Example to set distance to 5% of signal length
    prominence = std_height * 0.5  # Setting prominence to be half of std deviation

    # Detecting peaks
    peaks, properties = find_peaks(signals, height=height, distance=distance, prominence=prominence)

    # Calculating properties if peaks were found
    if peaks.size > 0:
        peak_count = len(peaks)
        average_peak_height = np.mean(properties["peak_heights"])
        average_distance = np.mean(np.diff(peaks)) if len(peaks) > 1 else 0
        average_prominence = np.mean(properties["prominences"])

        # Appending results for each channel
        peaks_results.append({
            "peak_count": peak_count,
            "average_peak_height": average_peak_height,
            "average_distance": average_distance,
            "average_prominence": average_prominence,
        })

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
    rms = np.sqrt(np.mean(signals ** 2, axis=1))
    return rms


def freq_bands(signals, fs=constants.SAMPLING_RATE):
    downsampled_signal = []
    band_features = np.zeros((signals.shape[0], 4))

    for i, signal in enumerate(signals):

        nperseg = min(32, len(downsampled_signal))

        frequencies, psd = welch(downsampled_signal, fs, nperseg=nperseg)

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
        frequencies = fftfreq(len(signal), 1.0 / fs)
        magnitude = np.abs(fft_result)
        centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
        centroids.append(centroid)
    return centroids


def spectral_edge_density(signals, fs, percentage=95):
    spectral_edge_densities = []

    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0 / fs)
        positive_frequencies = frequencies[frequencies >= 0]
        positive_fft_result = fft_result[frequencies >= 0]
        magnitude = np.abs(positive_fft_result)
        cumulative_sum = np.cumsum(np.sort(magnitude)[::-1])
        total_power = np.sum(magnitude)
        threshold = total_power * (percentage / 100)
        spectral_edge = positive_frequencies[np.argmax(cumulative_sum >= threshold)]
        spectral_edge_densities.append(spectral_edge)

    return spectral_edge_densities


def phase_locking_values(signals):
    # Compute the analytical signal for each input signal
    num_signals = signals.shape[0]
    plv_matrix = np.zeros((num_signals, num_signals))

    for i in range(num_signals):
        for j in range(i + 1, num_signals):  # Only compute for unique pairs
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
                    Lkm_sum += abs(x[m + i * k] - x[m + (i - 1) * k])
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
    imfs = None

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
    analyze_signals_results = constants.AnalyzeSignalsResult()
    signals = buffer.T  # Assuming signals are organized as channels x samples in the buffer
    analyze_signals_results.peak_heights = 0
    # peak_heights = detect_peak_heights(signals)
    analyze_signals_results.peak_counts = detect_peaks(signals)
    analyze_signals_results.variance, analyze_signals_results.std_dev = calculate_variance_std_dev(signals)
    analyze_signals_results.rms = calculate_rms(signals)

    band_features = freq_bands(signals, constants.SAMPLING_RATE)  # Assuming this returns an array of shape (

    analyze_signals_results.band_features = band_features
    # num_signals, num_bands)
    # Assuming band_features order: delta, theta, alpha, beta
    analyze_signals_results.delta_band_power = band_features[:, 0]  # Delta band powers for all signals
    analyze_signals_results.theta_band_power = band_features[:, 1]  # Theta band powers for all signals
    analyze_signals_results.alpha_band_power = band_features[:, 2]  # Alpha band powers for all signals
    analyze_signals_results.beta_band_power = band_features[:, 3]  # Beta band powers for all signals
    # spectral_entropy_values = spectral_entropy_values(signals, FS)
    analyze_signals_results.centroids = spectral_centroids(signals, constants.SAMPLING_RATE)
    analyze_signals_results.spectral_edge_densities = spectral_edge_density(signals, constants.SAMPLING_RATE, 95)
    # plv = phase_locking_values(signals)
    analyze_signals_results.hfd_values = calculate_higuchi_fractal_dimension(signals, k_max=10)
    analyze_signals_results.zero_crossing_rate = calculate_zero_crossing_rate(signals)
    # imfs = perform_empirical_mode_decomposition(signals)
    # warping_factors = time_warping_factor(signals)
    analyze_signals_results.rates = evolution_rate(signals)

    results = analyze_signals_results.to_dict()
    results = analyze_signals_results.to_python_float(results)

    # Print the results
    print("Analysis Results:")
    for key, value in results.items():
        print(f"{key}: {value}")
    return results


class SignalConverter:
    def __init__(self):
        self.data_m = DataManager("simulated signals sub", "simulated signals", "decoded features", self.receive_neural_data,
                                  True)

    def receive_neural_data(self, ecog_data):
        # ecog_data = ecog_data_str.replace("[", "").replace("]", "").split(",")
        ecog_data = loads(ecog_data)
        neural_data = np.array(ecog_data, dtype=np.float32)  # Convert the list to a NumPy array
        if neural_data.ndim == 1:
            neural_data = neural_data.reshape(-1,
                                              1)  # Reshape from (32) to (32, 1) for a single sample across 32 channels
        print(f"Received neural data shape: {neural_data.shape}")  # Debugging: Print shape

        if neural_data is not None and neural_data.size > 0:
            buffer = np.zeros((constants.NUM_CHANNELS, BUFFER_SIZE), dtype=np.float32)
            scaled_data = scale_data(neural_data)
            buffer = buffer_data(scaled_data, buffer)

            if np.all(buffer != 0):
                analysis_results = analyze_signals(buffer)
                serialized_results = dumps(analysis_results)
                self.data_m.set_data(serialized_results)
                self.data_m.publish(0)

        else:
            print("No data")
        return neural_data


if __name__ == "__main__":
    converter = SignalConverter()
    converter.data_m.listen()
