import zmq
import serial
import threading
import time

def send_data_to_fpga():
    # Set up the serial connection
    ser = serial.Serial('COM1', baudrate=128000)

    # ZeroMQ Subscriber Setup for receiving data
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        # Receive data from ZeroMQ publisher
        data_to_send = subscriber.recv()

        # Send data to the FPGA via UART
        ser.write(data_to_send)

        # Delay to match the 500 Hz signal rate (2 ms interval)
        time.sleep(0.01)

# Create and start the thread for sending data
send_thread = threading.Thread(target=send_data_to_fpga)
send_thread.start()
send_thread.join()

# Main execution
if __name__ == "__main__":