import paho.mqtt.client as mqtt
import json
import time
import numpy as np

# Function to generate base ECoG-like signals within the specified range, continuing from last values
def generate_ecog_like_base_signals(length, num_signals, initial_values=None):
    if initial_values is None:
        signals = np.random.uniform(min_volt, max_volt, (num_signals, length))
    else:
        signals = np.zeros((num_signals, length))
        for i in range(num_signals):
            signals[i, 0] = initial_values[i]
            signals[i, 1:] = np.random.uniform(min_volt, max_volt, (length - 1))
    return signals

# Function to scale signals to a specific bit depth
def scale_signals_to_bit_depth(modified_signals, bit_depth):
    min_val, max_val = min_volt, max_volt
    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_val - min_val) + min_val
    return modified_signals

# Function to apply oscillations to the signals
def apply_oscillations_to_signals(modified_signals, state, fs, min_volt, max_volt):
    scaled_amplitude_factors = {
        'alpha': (0.1, 1),
        'beta': (0.2, 1),
        'gamma': (0.1, 0.5)
    }

    num_signals, length = modified_signals.shape
    t = np.arange(length) / fs
    
    frequency_bands = {
        'resting': [
            ('alpha', (8, 12)),
        ],
        'active': [
            ('beta', (12, 30)),
            ('gamma', (30, 100))
        ]
    }

    selected_bands = frequency_bands.get(state, frequency_bands['resting'])

    for band, freq_range in selected_bands:
        scaled_min, scaled_max = scaled_amplitude_factors[band]
        min_amp = min_volt + (max_volt - min_volt) * scaled_min
        max_amp = min_volt + (max_volt - min_volt) * scaled_max

        frequency = np.random.uniform(freq_range[0], freq_range[1])
        phase_offset = np.random.uniform(0, 2 * np.pi)

        amplitude = np.random.uniform(min_amp, max_amp)
        oscillation = amplitude * np.sin(2 * np.pi * frequency * t + phase_offset)
        modified_signals += oscillation[np.newaxis, :]

    return modified_signals

# Function to apply amplitude variability while keeping the signals within the specified range
def apply_amplitude_variability(modified_signals, variability_factor):
    for i in range(modified_signals.shape[0]):
        current_std = np.std(modified_signals[i])
        if current_std == 0:
            continue
        scaling_factor = np.sqrt(variability_factor) / current_std
        scaled_noise = np.random.normal(0, scaling_factor, modified_signals.shape[1])
        modified_signals[i] += scaled_noise

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return modified_signals

# Function to apply variance while keeping the signals within the specified range
def apply_variance(modified_signals, variance):
    for i in range(modified_signals.shape[0]):
        noise = np.random.normal(0, np.sqrt(variance), modified_signals.shape[1])
        modified_signals[i] += noise

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return modified_signals

# Function to apply signal with standard deviation while keeping the signals within the specified range
def apply_signal_with_std(modified_signals, std_dev):
    for i in range(modified_signals.shape[0]):
        current_std = np.std(modified_signals[i])
        if current_std == 0:
            continue
        scaling_factor = std_dev / current_std
        modified_signals[i] += np.random.normal(0, scaling_factor * std_dev, modified_signals.shape[1])

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return modified_signals

# Function to apply signal with RMS value
def apply_signal_with_rms(modified_signals, rms_value):
    current_rms = np.sqrt(np.mean(modified_signals**2, axis=1, keepdims=True))
    scaling_factor = np.minimum(1.0, rms_value / current_rms)
    modified_signals *= scaling_factor
    return modified_signals

# Function to add peaks
def add_peaks(modified_signals, num_peaks, peak_height):
    num_signals, signal_length = modified_signals.shape
    scaling_factor = np.maximum(min_volt / np.min(modified_signals), max_volt / np.max(modified_signals))
    
    for i in range(num_signals):
        for _ in range(num_peaks):
            peak_position = np.random.randint(0, signal_length)
            modified_signals[i, peak_position] += peak_height * scaling_factor
            modified_signals[i, peak_position] = np.clip(modified_signals[i, peak_position], min_volt, max_volt)
            
    return modified_signals

# Function to apply moving average
def apply_moving_average(modified_signals, window_size):  
    for i in range(len(modified_signals)):
        length = len(modified_signals[i])
        if length >= window_size:
            cumsum_vec = np.cumsum(np.insert(modified_signals[i], 0, 0))
            moving_average = (cumsum_vec[window_size:] - cumsum_vec[:-window_size]) / window_size
            modified_signals[i, window_size//2:-window_size//2+1] = moving_average
    return modified_signals

# Function to apply fractal structure
def apply_fractal_structure(modified_signals, fractal_dimension):
    length = modified_signals.shape[1]
    fBm_signal = np.zeros_like(modified_signals)
    hurst_exponent = 2 - fractal_dimension

    for i in range(1, length):
        scale = (i ** (2 * hurst_exponent)) - ((i-1) ** (2 * hurst_exponent))
        fBm_signal[:, i] = fBm_signal[:, i-1] + np.random.normal(0, np.sqrt(scale), modified_signals.shape[0])

    max_signal = np.max(fBm_signal, axis=1, keepdims=True)
    min_signal = np.min(fBm_signal, axis=1, keepdims=True)
    fBm_signal = (fBm_signal - min_signal) / (max_signal - min_signal)
    fBm_signal *= (max_volt - min_volt)
    fBm_signal += min_volt

    return modified_signals

# Function to apply zero-crossing rate
def apply_zero_crossing_rate(modified_signals, target_rate):
    def calculate_zero_crossing_rate(sig):
        zero_crossings = np.where(np.diff(np.sign(sig)))[0]
        return len(zero_crossings) / len(sig)

    for i in range(len(modified_signals)):
        current_rate = calculate_zero_crossing_rate(modified_signals[i])
        factor = target_rate / current_rate if current_rate > 0 else 1.0
        modified_signals[i] *= factor
    return modified_signals

# Function to apply Arnold tongues
def apply_arnold_tongues(modified_signals, min_freq, max_freq, blend_factor):
    num_signals, signal_length = modified_signals.shape

    for i in range(num_signals):
        K = np.random.uniform(0.1 * max_volt, 0.5 * max_volt)
        omega = np.random.uniform(min_freq, max_freq)
        t = np.linspace(0, 2 * np.pi, signal_length)
        arnold_tongue_pattern = np.sin(t * omega) * K
        harmonics = np.random.choice([2, 3, 4], size=1)
        noise = np.random.uniform(-0.1 * K, 0.1 * K, size=signal_length)
        arnold_tongue_pattern += (np.sin(t * omega * harmonics) + noise) * K * 0.5
        modified_signals[i, :] = (1 - blend_factor) * modified_signals[i, :] + blend_factor * arnold_tongue_pattern

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    normalized_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return normalized_signals

def apply_phase_synchronization(modified_signals, global_sync_level, pairwise_sync_level, sync_factor=0.05):
    num_signals, length = modified_signals.shape
    common_phase = np.linspace(0, 2 * np.pi * global_sync_level, length)

    for i in range(num_signals):
        signal_fft = np.fft.fft(modified_signals[i])
        amplitude = np.abs(signal_fft)
        phase = np.angle(signal_fft)
        global_phase_shift = sync_factor * np.interp(common_phase, (common_phase.min(), common_phase.max()), (-np.pi, np.pi))
        adjusted_phase = phase + global_phase_shift
        modified_signals[i] = np.fft.ifft(amplitude * np.exp(1j * adjusted_phase)).real

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            phase_diff = np.angle(np.fft.fft(modified_signals[i])) - np.angle(np.fft.fft(modified_signals[j]))
            phase_diff_adjustment = np.interp(phase_diff, (-np.pi, np.pi), (-pairwise_sync_level, pairwise_sync_level))
            signal_fft_i = np.fft.fft(modified_signals[i])
            signal_fft_j = np.fft.fft(modified_signals[j])
            adjusted_phase_i = np.angle(signal_fft_i) + phase_diff_adjustment * sync_factor
            adjusted_phase_j = np.angle(signal_fft_j) - phase_diff_adjustment * sync_factor
            modified_signals[i] = np.fft.ifft(np.abs(signal_fft_i) * np.exp(1j * adjusted_phase_i)).real
            modified_signals[j] = np.fft.ifft(np.abs(signal_fft_j) * np.exp(1j * adjusted_phase_j)).real

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return modified_signals

def apply_transfer_entropy(modified_signals, influence_factor, max_influence):
    num_signals = len(modified_signals)
    max_length = max(len(signal) for signal in modified_signals)
    interaction_weights = np.random.uniform(0, 1, (num_signals, num_signals))
    interaction_weights /= interaction_weights.sum(axis=1, keepdims=True)
    interaction_weights *= influence_factor
    
    for i in range(1, max_length):
        influenced_signals = np.dot(interaction_weights, [signal[i - 1] if i < len(signal) else signal[-1] for signal in modified_signals])
        max_possible_influence = (max_volt - min_volt) / max_length
        
        if np.max(np.abs(influenced_signals)) > max_possible_influence:
            scaling_factor = max_possible_influence / np.max(np.abs(influenced_signals))
            influenced_signals *= scaling_factor
        
        for j in range(num_signals):
            if i < len(modified_signals[j]):
                modified_signals[j][i] += influenced_signals[j]

    return modified_signals

# Function to apply Hilbert-Huang transform
def apply_hilbert_huang(modified_signals):
    for i in range(len(modified_signals)):
        signal = modified_signals[i]
        low_freq_amplitude = 0.05 * (max_volt - min_volt)
        low_freq_signal = low_freq_amplitude * np.sin(2 * np.pi * 0.1 * np.arange(len(signal)))
        high_freq_amplitude = 0.05 * (max_volt - min_volt)
        high_freq_noise = high_freq_amplitude * np.random.randn(len(signal))
        modulated_signal = signal + low_freq_signal + high_freq_noise
        modulated_signal = np.clip(modulated_signal, min_volt, max_volt)
        modified_signals[i] = modulated_signal

    return modified_signals

# Function to apply spectral centroids
def apply_spectral_centroids(modified_signals, centroid_factor, edge_density_factor):
    for i in range(modified_signals.shape[0]):
        fft_spectrum = np.fft.fft(modified_signals[i])
        freq = np.fft.fftfreq(len(modified_signals[i]))
        centroid = np.sum(freq * np.abs(fft_spectrum)) / np.sum(np.abs(fft_spectrum))
        edge_density = np.sum(np.abs(np.diff(fft_spectrum))) / np.sum(np.abs(fft_spectrum))
        adjusted_spectrum = fft_spectrum * (centroid_factor * centroid + edge_density_factor * edge_density)
        modified_signals[i] = np.fft.ifft(adjusted_spectrum).real
    return modified_signals

# Function to apply dynamic time warping
def apply_dynamic_time_warping(modified_signals, reference_signal, warping_factor, min_volt, max_volt):
    modified_signals_aligned = []
    reference_signal = np.array(reference_signal)

    for signal in modified_signals:
        signal = np.array(signal)
        signal_length = len(signal)
        time_vector = np.linspace(0, 1, signal_length)
        reference_time_vector = np.linspace(0, 1, len(reference_signal)) * warping_factor
        modified_signal = np.interp(time_vector, reference_time_vector, reference_signal)
        current_min = np.min(modified_signal)
        current_max = np.max(modified_signal)
        scaling_factor = (max_volt - min_volt) / (current_max - current_min)
        modified_signal = (modified_signal - current_min) * scaling_factor + min_volt
        modified_signals_aligned.append(modified_signal)

    return np.array(modified_signals)

def apply_fft(modified_signals, complexity_factor):
    modified_signals_complexity = []

    for signal in modified_signals:
        spectrum = np.fft.fft(signal)
        freq = np.fft.fftfreq(len(signal))
        current_max = np.max(signal)
        current_min = np.min(signal)
        scaling_factor = max_volt / (current_max - current_min)
        modified_spectrum = spectrum * (1 + np.random.randn(len(spectrum)) * complexity_factor)
        modified_signal = np.fft.ifft(modified_spectrum).real
        modified_signal = (modified_signal - current_min) * scaling_factor + min_volt
        modified_signals_complexity.append(modified_signal)

    return np.array(modified_signals)

def apply_signal_evolution(modified_signals, evolution_rate):
    modified_signals_evolution = np.zeros_like(modified_signals)
    for i in range(modified_signals.shape[0]):
        modified_signals_evolution[i, 0] = np.random.randn()
        for t in range(1, modified_signals.shape[1]):
            modified_signals_evolution[i, t] = modified_signals_evolution[i, t - 1] + evolution_rate * np.random.randn()
    return modified_signals

def apply_phase_amplitude_coupling(modified_signals, low_freq, high_freq):
    modified_signals_pac = np.zeros_like(modified_signals)
    time = np.linspace(0, 1, modified_signals.shape[1])
    for i in range(modified_signals.shape[0]):
        low_freq_signal = np.sin(2 * np.pi * low_freq * time)
        high_freq_signal = np.sin(2 * np.pi * high_freq * time)
        modified_signals_pac[i] = (1 + low_freq_signal) * high_freq_signal
    return modified_signals

def apply_granger_causality(modified_signals, causality_strength):
    modified_signals_granger = np.copy(modified_signals)
    num_signals, signal_length = modified_signals.shape
    for i in range(1, num_signals):
        for j in range(num_signals):
            if i != j:
                causal_effect = modified_signals[j, :-i] * causality_strength
                modified_signals_granger[i, i:] += causal_effect
    return modified_signals

def apply_multivariate_empirical_mode_decomposition(modified_signals, num_imfs):
    num_channels, signal_length = modified_signals.shape
    memd_signals = np.zeros((num_channels, num_imfs, signal_length))
    for channel in range(num_channels):
        for imf_idx in range(num_imfs):
            imf = np.sin(2 * np.pi * (imf_idx + 1) * np.linspace(0, 1, signal_length))
            amplitude_scaling = np.random.uniform(0.5, 2.0)
            memd_signals[channel, imf_idx, :] = amplitude_scaling * imf
    modified_signals_memd = modified_signals + np.sum(memd_signals, axis=1)
    return modified_signals

def apply_normalized_states(modified_signals, modification_factor, matrix_size, value_range, num_matrices, eigenvalue_subset):
    num_signals, signal_length = modified_signals.shape
    modified_signals = modified_signals.copy()

    def generate_parameterized_hermitian_matrix(size, value_range):
        A = np.random.uniform(value_range[0], value_range[1], (size, size)) + 1j * np.random.uniform(value_range[0], value_range[1], (size, size))
        return A + A.conj().T

    density_diagonals = []
    for _ in range(num_matrices):
        hermitian_matrix = generate_parameterized_hermitian_matrix(matrix_size, value_range)
        eigenvalues, eigenvectors = np.linalg.eigh(hermitian_matrix)
        eigenvalues = eigenvalues[eigenvalue_subset]
        eigenvectors = eigenvectors[:, eigenvalue_subset]
        density_matrix = np.dot(eigenvectors, np.dot(np.diag(eigenvalues), eigenvectors.T.conj()))
        density_diagonal = np.diag(density_matrix).real
        density_diagonals.append(density_diagonal)

    for i, signal in enumerate(modified_signals):
        density_diagonal = density_diagonals[i % len(density_diagonals)]
        signal_modification = np.interp(signal, (np.min(signal), np.max(signal)), (np.min(density_diagonal), np.max(density_diagonal)))
        modified_signals[i] = (1 - modification_factor) * signal + modification_factor * signal_modification

    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    modified_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_volt - min_volt) + min_volt

    return modified_signals

def final_modified_scale_signals_to_bit_depth(modified_signals, bit_depth):
    min_val, max_val = min_volt, max_volt
    max_signal = np.max(modified_signals)
    min_signal = np.min(modified_signals)
    scaled_signals = ((modified_signals - min_signal) / (max_signal - min_signal)) * (max_val - min_val) + min_val
    return scaled_signals

def generate_transformed_signals(signal_length, num_signals, fs, min_volt, max_volt, features, initial_values=None):
    modified_signals = generate_ecog_like_base_signals(signal_length, num_signals, initial_values)
    
    for channel in range(num_signals):
        channel_features = features[f"channel_{channel + 1}"]
        transformations = [
            lambda x: scale_signals_to_bit_depth(x[np.newaxis, :], bit_depth)[0],
            lambda x: apply_oscillations_to_signals(x[np.newaxis, :], channel_features["state"], fs, min_volt, max_volt)[0],
            lambda x: apply_amplitude_variability(x[np.newaxis, :], channel_features["variability_factor"])[0],
            lambda x: apply_variance(x[np.newaxis, :], channel_features["variance"])[0],
            lambda x: apply_signal_with_std(x[np.newaxis, :], channel_features["std_dev"])[0],
            lambda x: apply_signal_with_rms(x[np.newaxis, :], channel_features["rms_value"])[0],
            lambda x: add_peaks(x[np.newaxis, :], channel_features["num_peaks"], channel_features["peak_height"])[0],
            lambda x: apply_fractal_structure(x[np.newaxis, :], channel_features["fractal_dimension"])[0],
            lambda x: apply_zero_crossing_rate(x[np.newaxis, :], channel_features["target_rate"])[0],
            lambda x: apply_arnold_tongues(x[np.newaxis, :], channel_features["min_freq"], channel_features["max_freq"], channel_features["blend_factor"])[0],
            lambda x: apply_phase_synchronization(x[np.newaxis, :], channel_features["global_sync_level"], channel_features["pairwise_sync_level"], channel_features["sync_factor"])[0],
            lambda x: apply_transfer_entropy(x[np.newaxis, :], channel_features["influence_factor"], channel_features["max_influence"])[0],
            lambda x: apply_spectral_centroids(x[np.newaxis, :], channel_features["centroid_factor"], channel_features["edge_density_factor"])[0],
            lambda x: apply_dynamic_time_warping(x[np.newaxis, :], reference_signal=np.mean(x[np.newaxis, :], axis=0), warping_factor=channel_features["warping_factor"], min_volt=min_volt, max_volt=max_volt)[0],
            lambda x: apply_fft(x[np.newaxis, :], channel_features["complexity_factor"])[0],
            lambda x: apply_signal_evolution(x[np.newaxis, :], channel_features["evolution_rate"])[0],
            lambda x: apply_phase_amplitude_coupling(x[np.newaxis, :], channel_features["low_freq"], channel_features["high_freq"])[0],
            lambda x: apply_granger_causality(x[np.newaxis, :], channel_features["causality_strength"])[0],
            lambda x: apply_multivariate_empirical_mode_decomposition(x[np.newaxis, :], channel_features["num_imfs"])[0],
            lambda x: apply_normalized_states(x[np.newaxis, :], channel_features["metadata_to_params"][0], channel_features["metadata_to_params"][1], channel_features["metadata_to_params"][2], channel_features["metadata_to_params"][3], channel_features["metadata_to_params"][4])[0]
        ]

        for transform in transformations:
            modified_signals[channel] = transform(modified_signals[channel])

    modified_signals = final_modified_scale_signals_to_bit_depth(modified_signals, bit_depth)
    return modified_signals


def serialize_transformed_signals(transformed_signals):
    return json.dumps({"signals": transformed_signals.tolist()})

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("GAME FEATURES")

def on_message(client, userdata, msg):
    global features_buffer, min_volt, max_volt
    try:
        features = json.loads(msg.payload.decode('utf-8'))
        features_buffer = features
        min_volt = 1e-6
        max_volt = 200e-6
    except Exception as e:
        print(f"Error processing message: {e}")

def publish_analogue_data(client, signals):
    encoded_signals = serialize_transformed_signals(signals)
    client.publish("ANALOGUE SIGNALS", encoded_signals)
    for i in range(len(signals)):
        print(f"Channel {i} first 5 data points: {signals[i][:5]}")

def main():
    global features_buffer, min_volt, max_volt, bit_depth

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()

    bit_depth = 16
    num_signals = 4
    fs = 500
    duration = 0.25
    signal_length = int(fs * duration)

    last_values = np.zeros(num_signals)
    features_buffer = None
    last_publish_time = time.time()

    try:
        while True:
            current_time = time.time()
            if features_buffer and (current_time - last_publish_time) >= 0.25:  # 4 Hz
                features = features_buffer
                transformed_signals = generate_transformed_signals(signal_length, num_signals, fs, min_volt, max_volt, features, initial_values=last_values)
                last_values = transformed_signals[:, -1]
                publish_analogue_data(client, transformed_signals)
                last_publish_time = current_time
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
