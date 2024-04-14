import zmq
import jack
import numpy as np
import threading
import time
import json

def send_data_to_audio_hubs():
    # ZeroMQ Subscriber Setup for receiving transformed signal data
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")  # Connect to the publisher port
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    # Set up the JACK client
    client = jack.Client("SignalSender")
    outports = []

    # Create output ports. Assuming 32 channels are split across two 16-port hubs.
    for i in range(32):  # For 32 channels
        port_name = f"output_{i}"
        outports.append(client.outports.register(port_name))

    # Activating the client
    with client:
        # Ensure the JACK server is running and the ports are connected appropriately
        # This step assumes manual connection or using jack.connect in the script

        while True:
            # Receive transformed signal data from ZeroMQ publisher
            encoded_packet = subscriber.recv_string()
            # Deserialize the JSON string to a Python object
            transformed_signals_dict = json.loads(encoded_packet)
            # Convert the list back into a NumPy array
            transformed_signals = np.array(transformed_signals_dict["signals"])

            # Assuming the data length matches the port buffer size and each channel maps to a port
            for port, signal_channel in zip(outports, transformed_signals):
                buffer_size = port.get_buffer_size()
                # Fill the port buffer with the signal data
                port.get_buffer()[:] = signal_channel[:buffer_size]

            # Wait 1 second before processing the next packet
            time.sleep(1)

# Create and start the thread for sending data
send_thread = threading.Thread(target=send_data_to_audio_hubs)
send_thread.start()

# Main execution
if __name__ == "__main__":
    send_thread.join()
