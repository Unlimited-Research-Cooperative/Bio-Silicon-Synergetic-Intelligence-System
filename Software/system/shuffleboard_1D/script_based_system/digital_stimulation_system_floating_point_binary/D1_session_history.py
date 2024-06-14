import paho.mqtt.client as mqtt
import json
import time
import os
from datetime import datetime

# Directory to save the historic data files
output_dir = "/home/vincent/MySSD/JupyterProjects/AAA_projects/UnlimitedResearchCooperative/Synthetic_Intelligence_Labs/Bio-Silicon-Synergetic-Intelligence-System/Software/system/shuffleboard_1D/script_based_system/digital_stimulation_system_floating_point_binary/sessions"

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Callback when the client receives a connection acknowledgment from the server
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe("historic_data")

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    try:
        # Decode the message payload
        payload = msg.payload.decode('utf-8')
        historic_data = json.loads(payload)

        # Generate a filename with the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{output_dir}/historic_data_{timestamp}.txt"

        # Save the historic data to the file in an intuitive format
        with open(filename, 'w') as f:
            f.write(f"Game Duration: {historic_data['game_duration']} seconds\n")
            f.write("History:\n")
            for entry in historic_data['history']:
                f.write(f"Round: {entry['round']}\n")
                f.write(f"  Action: {entry['action']}\n")
                f.write(f"  Result: Distance - {entry['result']['distance']}, Force - {entry['result']['force']}\n")
                f.write(f"  Timestamp: {datetime.fromtimestamp(entry['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  Distance to Target: {entry['distance_to_target']}\n")
                f.write(f"  Player Force: {entry['player_force']}\n")
                f.write("\n")

        print(f"Saved historic data to {filename}")

    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    # Set up MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)
    
    # Start MQTT loop
    mqtt_client.loop_start()

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
