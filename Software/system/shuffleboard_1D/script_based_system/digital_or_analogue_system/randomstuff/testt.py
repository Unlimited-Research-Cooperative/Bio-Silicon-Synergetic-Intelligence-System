import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']} - {device_info['maxOutputChannels']} channels")
    p.terminate()

if __name__ == "__main__":
    list_audio_devices()
