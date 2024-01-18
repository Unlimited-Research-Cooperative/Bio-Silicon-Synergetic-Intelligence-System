import zmq
import serial
import threading
import time

# Function to send data to the FPGA via UART
def send_data_to_fpga():
    # Configure the serial port (adjust port name and baud rate)
    ser = serial.Serial('COM1', baudrate=9600)

    while True:
        # Prepare the data to send to the FPGA (adjust as needed)
        data_to_send = b'Hello FPGA'  # Replace with your data

        # Send data to the FPGA via UART
        ser.write(data_to_send)
        
        # You can add delays or other logic as needed
        time.sleep(0.1)  # Add a 100 ms delay between sending data

# Function to receive data from the ZeroMQ publisher
def receive_data_from_publisher():
    # ZeroMQ Subscriber Setup
    context_sub = zmq.Context()
    subscriber = context_sub.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5557")  # Connect to the publisher at port 5557
    subscriber.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all incoming messages

    while True:
        message = subscriber.recv_string()
        print("Received message from ZeroMQ publisher:", message)
        
        # Process the received data as needed
        # Add your logic here to handle and process the data
        
        # You can add delays or other logic as needed
        time.sleep(0.1)  # Add a 100 ms delay between processing received data

# Create two threads for sending and receiving data
send_thread = threading.Thread(target=send_data_to_fpga)
receive_thread = threading.Thread(target=receive_data_from_publisher)

# Start both threads
send_thread.start()
receive_thread.start()

# Wait for both threads to finish
send_thread.join()
receive_thread.join()
