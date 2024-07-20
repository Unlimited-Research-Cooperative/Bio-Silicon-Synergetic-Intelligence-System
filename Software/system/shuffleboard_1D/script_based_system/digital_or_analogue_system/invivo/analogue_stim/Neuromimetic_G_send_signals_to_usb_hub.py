import numpy as np
import paho.mqtt.client as mqtt
import json
import pyaudio
import threading
import time
from scipy.signal import resample_poly

# Constants
PACKET_DURATION = 0.25  # 250 ms packets
NUM_CHANNELS = 4
AMPLITUDE = 32767  # Max value for 16-bit audio
INPUT_SAMPLE_RATE = 500
OUTPUT_SAMPLE_RATE = 48000  # Common sample rate for audio playback
BUFFER_SIZE = int(OUTPUT_SAMPLE_RATE * PACKET_DURATION)  # Number of samples per packet
RING_BUFFER_SIZE = BUFFER_SIZE  # Larger buffer for more continuous playback

# PyAudio device indices for the output channels
pyaudio_devices = [18, 19, 20, 21]  # Replace with actual indices if needed

# Global variables
latest_waveform = None
ring_buffers = [np.zeros(RING_BUFFER_SIZE, dtype=np.float32) for _ in range(NUM_CHANNELS)]
ring_buffer_write_positions = [0 for _ in range(NUM_CHANNELS)]
lock = threading.Lock()

# Callback when the client receives a connection acknowledgment from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("ANALOGUE SIGNALS")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    global latest_waveform
    try:
        # Decode the message payload
        payload = msg.payload.decode('utf-8')
        
        # Parse the JSON data
        analogue_data = json.loads(payload)["signals"]
        
        # Convert analogue data (list of lists) to a NumPy array for each channel
        analogue_waveform = [np.array(signal) for signal in analogue_data]
        
        # Scale the signals to the appropriate range
        scaled_waveform = [signal * 4000 for signal in analogue_waveform]  # Adjust scaling as needed
        
        with lock:
            latest_waveform = np.array(scaled_waveform)
        
        print(f"Received waveform (1 data point per channel): {[waveform[0] for waveform in latest_waveform]}")
        for i, waveform in enumerate(latest_waveform):
            print(f"Received Channel {i} first 5 data points: {waveform[:5]}")
            print(f"Channel {i} - Min: {waveform.min()}, Max: {waveform.max()}")
        
    except Exception as e:
        print(f"Error processing message: {e}")

def audio_callback_factory(channel):
    def audio_callback(in_data, frame_count, time_info, status):
        global ring_buffers, ring_buffer_write_positions, lock
        
        with lock:
            start_pos = ring_buffer_write_positions[channel]
            end_pos = start_pos + frame_count
            
            if end_pos <= RING_BUFFER_SIZE:
                chunk = ring_buffers[channel][start_pos:end_pos]
            else:
                chunk = np.concatenate((ring_buffers[channel][start_pos:], ring_buffers[channel][:end_pos % RING_BUFFER_SIZE]))

            ring_buffer_write_positions[channel] = end_pos % RING_BUFFER_SIZE
        
        int_waveform = (chunk * AMPLITUDE).astype(np.int16)
        
        # Logging to confirm each device is playing the respective channel signal
        print(f"Device {pyaudio_devices[channel]} playing channel {channel} data: {int_waveform[:10]}...")

        return (int_waveform.tobytes(), pyaudio.paContinue)
    return audio_callback

def main():
    global latest_waveform, ring_buffers, ring_buffer_write_positions

    # Set up MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("127.0.0.1", 1883, 60)
    client.loop_start()

    # Set up audio streams with callback
    p = pyaudio.PyAudio()
    streams = []
    
    for i, device_index in enumerate(pyaudio_devices):
        try:
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=OUTPUT_SAMPLE_RATE,
                            output=True,
                            output_device_index=device_index,
                            stream_callback=audio_callback_factory(i))
            streams.append(stream)
            stream.start_stream()
        except Exception as e:
            print(f"Error opening stream for device {device_index}: {e}")

    try:
        while True:
            if latest_waveform is not None:
                with lock:
                    # Resample the waveform for each channel and update the ring buffer
                    resampled_waveform = [resample_poly(channel, OUTPUT_SAMPLE_RATE, INPUT_SAMPLE_RATE) for channel in latest_waveform]
                    for i in range(NUM_CHANNELS):
                        print(f"Original length: {len(latest_waveform[i])}, Resampled length: {len(resampled_waveform[i])}")  # Verification line
                        write_pos = ring_buffer_write_positions[i]
                        to_write = resampled_waveform[i]
                        available_space = RING_BUFFER_SIZE - write_pos
                        if len(to_write) > available_space:
                            ring_buffers[i][write_pos:] = to_write[:available_space]
                            ring_buffers[i][:len(to_write) - available_space] = to_write[available_space:]
                        else:
                            ring_buffers[i][write_pos:write_pos + len(to_write)] = to_write
                        ring_buffer_write_positions[i] = (write_pos + len(to_write)) % RING_BUFFER_SIZE
                        print(f"Updated ring buffer for channel {i} with first 5 data points: {ring_buffers[i][:5]}")
                latest_waveform = None  # Clear the latest_waveform after processing
            
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()
        for stream in streams:
            stream.stop_stream()
            stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
