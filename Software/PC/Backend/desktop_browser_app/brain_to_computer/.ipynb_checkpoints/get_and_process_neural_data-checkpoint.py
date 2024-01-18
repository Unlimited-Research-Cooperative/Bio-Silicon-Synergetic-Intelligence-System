import zmq
import numpy as np
from data_processing.scaling import scale_signals_to_16bit

def receive_neural_data(socket):
    """
    Receive neural data from a ZeroMQ socket.
    """
    raw_data = socket.recv()
    neural_data = np.frombuffer(raw_data, dtype=np.float32)
    neural_data = neural_data.reshape(-1, 8)  # Assuming 8 channels
    return neural_data

def scale_data(data, bit_depth=16):
    """
    Scale data to the specified bit depth.
    """
    # Example scaling for unsigned 16-bit integers
    scaled_data = ((data - data.min()) / (data.max() - data.min())) * (2**bit_depth - 1)
    return scaled_data.astype(np.uint16)

def main():
    context = zmq.Context()

    # Subscriber socket to receive neural data
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://neural_data_publisher:5555")
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    # Publisher socket to send scaled data to modules
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:5556")

    # Subscriber socket to collect results from modules
    results_sub_socket = context.socket(zmq.SUB)
    results_sub_socket.bind("tcp://*:5557")
    results_sub_socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        # Receive data
        neural_data = receive_neural_data(sub_socket)

        # Scale data to 16-bit
        scaled_data = scale_data(neural_data, 16)

        # Send scaled data to analysis modules
        pub_socket.send(scaled_data.tobytes())

        # Collect and combine results from all modules
        combined_results = {}
        for _ in range(number_of_modules):  # Replace with actual number of modules
            topic, result = results_sub_socket.recv_multipart()
            combined_results[topic.decode()] = np.frombuffer(result, dtype=np.float32)

        # Process combined results further or send to next stage
        process_and_forward_results(combined_results)

if __name__ == "__main__":
    main()
