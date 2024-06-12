import paho.mqtt.client as mqtt
import jack
import numpy as np
import threading
import time
import json
import matplotlib.pyplot as plt

# Constants
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "digital_signals"
PACKET_DURATION = 0.25  # 250 ms packets
BIT_DURATION = 0.0125  # 12.5 ms per bit (for 16 bits in 200 ms)

# Global variable to store the latest digital waveform for visualization
latest_waveform = None

# Callback when the client receives a connection acknowledgment from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC)

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    global latest_waveform
    try:
        # Decode the message payload
        payload = msg.payload.decode('utf-8')
        
        # Parse the JSON data
        digital_data = json.loads(payload)["stim_signals"]
        
        # Convert digital data (list of lists) to a NumPy array
        digital_waveform = np.array([1 if bit == 150 else -1 for signal in digital_data for bit in signal])
        
        # Store the latest waveform for visualization
        latest_waveform = digital_waveform
        
        # Send the digital waveform to the USB hub via JACK
        send_data_to_audio_hub(digital_waveform)
    except Exception as e:
        print(f"Error processing message: {e}")

# Function to send data to the USB hub via JACK
def send_data_to_audio_hub(digital_waveform):
    # Set up the JACK client
    client = jack.Client("DigitalDataSender")
    outport = client.outports.register("output_0")

    # Activating the client
    with client:
        # Send the digital waveform to the output port
        buffer_size = outport.get_buffer_size()
        start_index = 0
        
        while start_index < len(digital_waveform):
            end_index = start_index + buffer_size
            packet = digital_waveform[start_index:end_index]
            
            # Ensure the waveform length does not exceed the port buffer size
            outport.get_buffer()[:len(packet)] = packet
            start_index += buffer_size

            # Wait for the duration of the packet
            time.sleep(PACKET_DURATION)

# Function to visualize the signals
def visualize_signals():
    global latest_waveform
    
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    
    ax.set_xlim(0, 16 * len(latest_waveform) // 4)
    ax.set_ylim(-1.5, 1.5)
    
    while True:
        if latest_waveform is not None:
            # Update the plot with the latest waveform
            line.set_xdata(np.arange(len(latest_waveform)))
            line.set_ydata(latest_waveform)
            ax.set_xlim(0, len(latest_waveform))
            fig.canvas.draw()
            fig.canvas.flush_events()
        time.sleep(0.1)

# Main function to set up MQTT client and start the loop
def main():
    # Set up MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start MQTT loop
    mqtt_client.loop_start()
    
    # Start the visualization in a separate thread
    vis_thread = threading.Thread(target=visualize_signals)
    vis_thread.start()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        vis_thread.join()

# Run the main function in a thread
send_thread = threading.Thread(target=main)
send_thread.start()

# Main execution
if __name__ == "__main__":
    send_thread.join()
