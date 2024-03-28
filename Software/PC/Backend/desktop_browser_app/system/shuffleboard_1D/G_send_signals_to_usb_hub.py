import zmq
import jack
import numpy as np
import threading
import time
import json

def send_data_to_audio_hubs():
    # ZeroMQ Subscriber Setup for receiving digital data
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")  # Connect to the modified publisher port
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    # Set up the JACK client
    client = jack.Client("DigitalDataSender")
    outports = []

    # Create only one output port as we are dealing with a single channel now
    outports.append(client.outports.register("output_0"))

    # Activating the client
    with client:
        # Ensure the JACK server is running and the ports are connected appropriately
        # This step assumes manual connection or using jack.connect in the script

        while True:
            try:
                # Receive digital data from ZeroMQ publisher
                digital_data = subscriber.recv_pyobj()

                # Convert the digital data (list of 0s and 1s) to a NumPy array
                # Here, we're assuming the need to map these binary values to a waveform
                # For simplicity, let's map 0 to -1 and 1 to 1 in the waveform
                digital_waveform = np.array([1 if bit else -1 for bit in digital_data])

                # Send this digital waveform to the output port
                # Ensure the waveform length does not exceed the port buffer size
                buffer_size = outports[0].get_buffer_size()
                outports[0].get_buffer()[:len(digital_waveform)] = digital_waveform[:buffer_size]

                # Wait briefly before processing the next packet
                time.sleep(0.1)
            except zmq.Again:
                # No digital data received yet, wait briefly to try again
                time.sleep(0.1)

# Create and start the thread for sending data
send_thread = threading.Thread(target=send_data_to_audio_hubs)
send_thread.start()

# Main execution
if __name__ == "__main__":
    send_thread.join()
