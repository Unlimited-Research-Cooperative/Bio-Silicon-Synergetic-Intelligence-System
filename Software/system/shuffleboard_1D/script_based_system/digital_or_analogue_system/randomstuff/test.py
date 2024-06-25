import numpy as np
import soundfile as sf
import subprocess

# ALSA device IDs for the output channels
alsa_devices = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

# Parameters for sine wave
duration = 1.0  # seconds
samplerate = 44100  # Hz
frequency = 440.0  # Hz (A4 note)
amplitude = 0.5  # max amplitude

# Generate a sine wave
t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
sine_wave = np.int16(sine_wave * 32767)

# Save the sine wave to a file
sine_wave_file = '/tmp/sine_wave.wav'
sf.write(sine_wave_file, sine_wave, samplerate)

def play_sine_wave():
    for device_index in alsa_devices:
        print(f"Playing sine wave on device plughw:{device_index},0")
        result = subprocess.call(['aplay', '-D', f'plughw:{device_index},0', sine_wave_file])
        print(f"Sine wave play result for device {device_index}: {result}")

if __name__ == "__main__":
    play_sine_wave()
