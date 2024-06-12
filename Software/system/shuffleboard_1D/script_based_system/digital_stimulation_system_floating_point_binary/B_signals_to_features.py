import numpy as np
import paho.mqtt.client as mqtt
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
UPDATE_RATE = 4  # Update rate in Hz
BUFFER_SIZE = int(FS // UPDATE_RATE)  # Size of buffer corresponding to update rate
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_INPUT_TOPIC = "processed_neural_data"
MQTT_OUTPUT_TOPIC = "analyzed_neural_data"

# Global buffer to hold data
buffer = np.zeros((NUM_CHANNELS, BUFFER_SIZE), dtype=np.float32)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_INPUT_TOPIC)

def on_message(client, userdata, message):
    global buffer
    try:
        payload = message.payload.decode('utf-8')
        neural_data = json.loads(payload)
        data = np.array(neural_data['data'], dtype=np.float32)
        if data.ndim == 1:
            data = data.reshape(-1, 1)
        scaled_data = scale_data(data)
        buffer = buffer_data(scaled_data, buffer)
        if np.all(buffer != 0):
            analysis_results = analyze_signals(buffer)
            client.publish(MQTT_OUTPUT_TOPIC, json.dumps(analysis_results))
    except Exception as e:
        print(f"Error processing message: {e}")

def buffer_data(data, buffer):
    buffer = np.roll(buffer, -data.shape[1], axis=1)
    buffer[:, -data.shape[1]:] = data
    return buffer

def scale_data(data, fs=FS, factor=2):
    if data.ndim != 2 or data.shape[0] != NUM_CHANNELS:
        raise ValueError(f"Unexpected data shape: {data.shape}. Expected ({NUM_CHANNELS}, number_of_samples).")
    subsampled_data = data[:, ::factor]
    data_min = np.min(subsampled_data, axis=1, keepdims=True)
    data_max = np.max(subsampled_data, axis=1, keepdims=True)
    scaled_data = (subsampled_data - data_min) / np.where(data_max > data_min, data_max - data_min, 1)
    return scaled_data

def detect_peaks(signals):
    peaks_results = []
    for signal in signals:
        median_height = np.median(signal)
        std_height = np.std(signal)
        height = median_height + std_height
        distance = len(signal) * 0.05
        prominence = std_height * 0.5
        peaks, properties = find_peaks(signal, height=height, distance=distance, prominence=prominence)
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
        peaks_results.append({
            "peak_count": peak_count,
            "average_peak_height": average_peak_height,
            "average_distance": average_distance,
            "average_prominence": average_prominence,
        })
    return peaks_results

def calculate_variance_std_dev(signals):
    variance = np.var(signals, axis=1)
    std_dev = np.std(signals, axis=1)
    return variance, std_dev

def calculate_rms(signals):
    rms = np.sqrt(np.mean(signals**2, axis=1))
    return rms

def freq_bands(signals, fs=FS):
    band_features = np.zeros((signals.shape[0], 4))
    for i, signal in enumerate(signals):
        nperseg = min(32, len(signal))
        frequencies, psd = welch(signal, fs=FS, nperseg=nperseg)
        bands = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30)}
        for j, (name, (low, high)) in enumerate(bands.items()):
            idx = np.logical_and(frequencies >= low, frequencies <= high)
            if np.any(idx):
                band_features[i, j] = np.nanmean(psd[idx])
            else:
                band_features[i, j] = 0.0
    return band_features

def spectral_centroids(signals, fs):
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

def calculate_higuchi_fractal_dimension(signals, k_max):
    hfd_values = []
    for signal in signals:
        N = len(signal)
        L = []
        x = np.asarray(signal)
        for k in range(1, k_max + 1):
            Lk = []
            for m in range(k):
                Lkm_sum = 0
                max_index = int((N - m - 1) / k) + 1
                for i in range(1, max_index):
                    Lkm_sum += abs(x[m + i*k] - x[m + (i-1)*k])
                if max_index - 1 > 0:
                    Lkm = Lkm_sum * (N - 1) / (k * (max_index - 1))
                    Lk.append(Lkm)
                else:
                    Lk.append(0)
            if np.mean(Lk) > 0:
                L.append(np.log(np.mean(Lk)))
            else:
                L.append(np.log(np.finfo(float).eps))
        if len(L) > 0 and np.all(np.isfinite(L)):
            hfd = np.polyfit(np.log(range(1, k_max + 1)), L, 1)[0]
            hfd_values.append(hfd)
        else:
            hfd_values.append(np.nan)
    return hfd_values

def calculate_zero_crossing_rate(signals):
    sign_changes = np.diff(np.sign(signals), axis=1)
    zero_crossings = np.count_nonzero(sign_changes, axis=1)
    zero_crossing_rates = zero_crossings / (signals.shape[1] - 1)
    return zero_crossing_rates

def evolution_rate(signals):
    rates = np.zeros(signals.shape[0])
    for i, signal in enumerate(signals):
        analytic_signal = hilbert(signal)
        envelope = np.abs(analytic_signal)
        derivative = np.diff(envelope)
        rates[i] = np.mean(np.abs(derivative))
    return rates

def analyze_signals(buffer):
    signals = buffer.T
    peaks = detect_peaks(signals)
    variance, std_dev = calculate_variance_std_dev(signals)
    rms = calculate_rms(signals)
    band_features = freq_bands(signals, FS)
    delta_band_power = band_features[:, 0]
    theta_band_power = band_features[:, 1]
    alpha_band_power = band_features[:, 2]
    beta_band_power = band_features[:, 3]
    centroids = spectral_centroids(signals, FS)
    spectral_edge_densities = spectral_edge_density(signals, FS, 95)
    hfd_values = calculate_higuchi_fractal_dimension(signals, k_max=10)
    zero_crossing_rate = calculate_zero_crossing_rate(signals)
    rates = evolution_rate(signals)
    results = {
        'peaks': peaks,
        'variance': variance.tolist(),
        'std_dev': std_dev.tolist(),
        'rms': rms.tolist(),
        'delta_band_power': delta_band_power.tolist(),
        'theta_band_power': theta_band_power.tolist(),
        'alpha_band_power': alpha_band_power.tolist(),
        'beta_band_power': beta_band_power.tolist(),
        'centroids': centroids,
        'spectral_edge_densities': spectral_edge_densities,
        'higuchi_fractal_dimension': hfd_values,
        'zero_crossing_rate': zero_crossing_rate.tolist(),
        'evolution_rate': rates.tolist(),
    }
    return results

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        while True:
            time.sleep(1 / UPDATE_RATE)
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
