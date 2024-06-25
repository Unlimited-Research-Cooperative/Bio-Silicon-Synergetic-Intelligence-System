import subprocess

# List of ALSA hardware device names corresponding to the symlinks
alsa_devices = ["hw:21,0", "hw:20,0", "hw:19,0", "hw:18,0", 
                "hw:17,0", "hw:7,0", "hw:16,0", "hw:15,0", 
                "hw:14,0", "hw:13,0", "hw:12,0", "hw:11,0", 
                "hw:9,0", "hw:8,0"]

# Function to check device capabilities using aplay for playback
def check_playback_device_capabilities(device):
    try:
        result = subprocess.run(['aplay', '-D', device, '--dump-hw-params'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Checking playback device {device}")
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'FORMAT' in line or 'RATE' in line or 'CHANNELS' in line:
                    print(line)
        else:
            print(f"No output for device {device}. Possible error: {result.stderr}")
    except Exception as e:
        print(f"Error checking playback device {device}: {e}")

# Function to check device capabilities using arecord for capture
def check_capture_device_capabilities(device):
    try:
        result = subprocess.run(['arecord', '-D', device, '--dump-hw-params'], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Checking capture device {device}")
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'FORMAT' in line or 'RATE' in line or 'CHANNELS' in line:
                    print(line)
        else:
            print(f"No output for device {device}. Possible error: {result.stderr}")
    except Exception as e:
        print(f"Error checking capture device {device}: {e}")

# Check capabilities for each device
for device in alsa_devices:
    check_playback_device_capabilities(device)
    check_capture_device_capabilities(device)
