import sys
import json
import logging
import numpy as np
import paho.mqtt.client as mqtt
import time

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette
import pyqtgraph as pg
from scipy.signal import resample, find_peaks, hilbert, welch
from scipy.fft import fft, fftfreq

logging.basicConfig(level=logging.DEBUG)

# Constants
NUM_CHANNELS = 32
FS_ORIGINAL = 512  # Original sampling rate in Hz
FS_DOWNSAMPLED = 500  # Downsampled rate in Hz
UPDATE_RATE = 4  # Update rate in Hz
BUFFER_SIZE = int(FS_DOWNSAMPLED // UPDATE_RATE)  # Size of buffer corresponding to update rate
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_INPUT_TOPIC = "INCOMING NEURAL SIGNALS"
MQTT_OUTPUT_TOPIC = "EXTRACTED FEATURES"

# Global buffer to hold data
buffer = np.zeros((NUM_CHANNELS, BUFFER_SIZE), dtype=np.float32)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_INPUT_TOPIC)

def on_message(client, userdata, message):
    global buffer
    try:
        payload = message.payload.decode('utf-8')
        data = np.array(json.loads(payload), dtype=np.float32)
        if data.ndim == 1:
            data = data.reshape(NUM_CHANNELS, -1)
        downsampled_data = downsample(data, FS_ORIGINAL, FS_DOWNSAMPLED)
        buffer = buffer_data(downsampled_data, buffer)
        if np.all(buffer != 0):
            analysis_results = analyze_signals(buffer)
            client.publish(MQTT_OUTPUT_TOPIC, json.dumps(analysis_results))
            visualizer.update_results(analysis_results)
    except Exception as e:
        print(f"Error processing message: {e}")

def downsample(data, original_fs, target_fs):
    num_samples = int(data.shape[1] * target_fs / original_fs)
    downsampled_data = resample(data, num_samples, axis=1)
    return downsampled_data

def buffer_data(data, buffer):
    buffer = np.roll(buffer, -data.shape[1], axis=1)
    buffer[:, -data.shape[1]:] = data
    return buffer

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

def freq_bands(signals, fs=FS_DOWNSAMPLED):
    band_features = np.zeros((signals.shape[0], 4))
    for i, signal in enumerate(signals):
        nperseg = min(32, len(signal))
        frequencies, psd = welch(signal, fs=fs, nperseg=nperseg)
        bands = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (8, 13), 'beta': (13, 30)}
        for j, (name, (low, high)) in enumerate(bands.items()):
            idx = np.logical_and(frequencies >= low, frequencies <= high)
            if np.any(idx):
                band_features[i, j] = np.nanmean(psd[idx])
            else:
                band_features[i, j] = 0.0
    return band_features

def spectral_centroids(signals, fs=FS_DOWNSAMPLED):
    centroids = []
    for signal in signals:
        fft_result = fft(signal)
        frequencies = fftfreq(len(signal), 1.0/fs)
        magnitude = np.abs(fft_result)
        centroid = np.sum(frequencies * magnitude) / np.sum(magnitude)
        centroids.append(centroid)
    return centroids

def spectral_edge_density(signals, fs=FS_DOWNSAMPLED, percentage=95):
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
    band_features = freq_bands(signals, FS_DOWNSAMPLED)
    delta_band_power = band_features[:, 0]
    theta_band_power = band_features[:, 1]
    alpha_band_power = band_features[:, 2]
    beta_band_power = band_features[:, 3]
    centroids = spectral_centroids(signals, FS_DOWNSAMPLED)
    spectral_edge_densities = spectral_edge_density(signals, FS_DOWNSAMPLED, 95)
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

class ResultVisualizer(QWidget):
    def __init__(self, num_channels):
        super().__init__()
        self.num_channels = num_channels
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('EXTRACTED FEATURES')
        self.setStyleSheet("background-color: black; color: #00D8D8;")

        self.results_table = QTableWidget()
        self.results_table.setRowCount(self.num_channels)
        self.results_table.setColumnCount(12)
        self.results_table.setHorizontalHeaderLabels(['Peaks', 'Var', 'Std Dev', 'RMS', 'Delta', 'Theta', 'Alpha', 'Beta', 'Centroid', 'Spec Edge', 'HFD', 'ZCR'])
        self.results_table.setStyleSheet("background-color: black; color: #00D8D8;")

        layout = QVBoxLayout()
        layout.addWidget(self.results_table)
        self.setLayout(layout)

        self.show()

    def update_results(self, results):
        for i in range(self.num_channels):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(results['peaks'][i]['peak_count'])))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{results['variance'][i]:.2f}"))
            self.results_table.setItem(i, 2, QTableWidgetItem(f"{results['std_dev'][i]:.2f}"))
            self.results_table.setItem(i, 3, QTableWidgetItem(f"{results['rms'][i]:.2f}"))
            self.results_table.setItem(i, 4, QTableWidgetItem(f"{results['delta_band_power'][i]:.2f}"))
            self.results_table.setItem(i, 5, QTableWidgetItem(f"{results['theta_band_power'][i]:.2f}"))
            self.results_table.setItem(i, 6, QTableWidgetItem(f"{results['alpha_band_power'][i]:.2f}"))
            self.results_table.setItem(i, 7, QTableWidgetItem(f"{results['beta_band_power'][i]:.2f}"))
            self.results_table.setItem(i, 8, QTableWidgetItem(f"{results['centroids'][i]:.2f}"))
            self.results_table.setItem(i, 9, QTableWidgetItem(f"{results['spectral_edge_densities'][i]:.2f}"))
            self.results_table.setItem(i, 10, QTableWidgetItem(f"{results['higuchi_fractal_dimension'][i]:.2f}"))
            self.results_table.setItem(i, 11, QTableWidgetItem(f"{results['zero_crossing_rate'][i]:.2f}"))

def main():
    app = QApplication(sys.argv)

    global visualizer
    visualizer = ResultVisualizer(num_channels=32)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
