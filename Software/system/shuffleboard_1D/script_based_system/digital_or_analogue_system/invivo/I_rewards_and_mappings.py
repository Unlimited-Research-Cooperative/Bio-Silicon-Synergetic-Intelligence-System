import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import subprocess  # To control the USB power
import serial  # To communicate with the USB relay
import pyaudio
import wave
import os
from collections import defaultdict  # Ensure defaultdict is imported

class USBRelay:
    def __init__(self, port):
        self.port = port
        try:
            self.ser = serial.Serial(self.port, 9600, timeout=1)
            self.relay_on = bytes.fromhex('A0 01 01 A2')
            self.relay_off = bytes.fromhex('A0 01 00 A1')
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def turn_on(self):
        if self.ser:
            try:
                self.ser.write(self.relay_on)
                print("Relay is turned ON")
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")

    def turn_off(self):
        if self.ser:
            try:
                self.ser.write(self.relay_off)
                print("Relay is turned OFF")
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")

    def close(self):
        if self.ser:
            try:
                self.ser.close()
            except serial.SerialException as e:
                print(f"Error closing serial port: {e}")

class FeedbackSystem:
    def __init__(self, hub, port, usb_relay, sound_file, audio_device_index):
        self.hub = hub
        self.port = port
        self.usb_relay = usb_relay
        self.last_distance_to_target = None

        # Initialize PyAudio for audio output
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.sound_file = sound_file
        self.audio_device_index = audio_device_index
        self.load_sound()

    def load_sound(self):
        # Open the sound file
        self.wf = wave.open(self.sound_file, 'rb')
        # Open a stream with the specified audio device
        try:
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                      channels=self.wf.getnchannels(),
                                      rate=self.wf.getframerate(),
                                      output=True,
                                      output_device_index=self.audio_device_index)
            print("Sound loaded and stream opened.")
        except Exception as e:
            print(f"Error opening audio stream: {e}")

    def play_sound(self):
        if self.stream:
            # Rewind the wave file
            self.wf.rewind()
            data = self.wf.readframes(1024)
            start_time = time.time()
            while data and (time.time() - start_time) < 0.03:
                self.stream.write(data)
                data = self.wf.readframes(1024)
            print("Sound played.")

    # def turn_repeller_on(self):
    #     # Turn on the USB power to the repeller
    #     subprocess.run(['uhubctl', '-l', self.hub, '-p', self.port, '-a', 'on'])

    # def turn_repeller_off(self):
    #     # Turn off the USB power to the repeller
    #     subprocess.run(['uhubctl', '-l', self.hub, '-p', self.port, '-a', 'off'])

    def activate_feeder(self):
        # Activate the feeder to dispense the reward mix using the USB relay
        self.usb_relay.turn_on()  # Turn on the USB relay to activate the feeder
        time.sleep(0.1)  # Keep the feeder active for 0.1 seconds
        self.usb_relay.turn_off()  # Turn off the USB relay to deactivate the feeder

    def provide_feedback(self, distance_to_target):
        # Provide feedback based on the change in distance to the target
        if self.last_distance_to_target is not None:
            if distance_to_target < self.last_distance_to_target:
                print(f"Distance decreased from {self.last_distance_to_target} to {distance_to_target}, playing sound and activating feeder...")
                self.play_sound()
                self.activate_feeder()  # Also activate the feeder for positive reinforcement
            # elif distance_to_target > self.last_distance_to_target:
            #     print(f"Distance increased from {self.last_distance_to_target} to {distance_to_target}, activating repeller...")
            #     self.turn_repeller_on()
            #     time.sleep(0.03)  # Keep the repeller on for 0.03 seconds
            #     self.turn_repeller_off()
        else:
            print(f"Initial distance to target: {distance_to_target}")

        self.last_distance_to_target = distance_to_target

        
'''        
class NeuralMappingVisualizer:
    def __init__(self, processor):
        self.processor = processor
        self.fig, self.ax = plt.subplots()
        self.quality_scores = np.zeros(32)

    def update_plot(self, frame):
        # Update the plot with new data
        neural_data = self.fetch_neural_data()  # Placeholder for actual neural data fetching
        actions = self.processor.process_signals(neural_data)
        self.quality_scores = self.processor.assess_mapping_quality(neural_data, actions)
        self.ax.clear()
        self.ax.bar(range(32), self.quality_scores)
        self.ax.set_ylim(0, 1)
        self.ax.set_title('Mapping Quality Scores')
        self.ax.set_xlabel('Channel')
        self.ax.set_ylabel('Quality Score')

    def fetch_neural_data(self):
        # Placeholder method to fetch neural data
        return np.random.rand(32, 500)  # Dummy neural data

    def animate(self):
        animation = FuncAnimation(self.fig, self.update_plot, interval=100)
        plt.show()

class DynamicSignalDecoder(SignalDecoder):
    def adjust_mappings_based_on_feedback(self, feedback_log):
        for feature, outcomes in feedback_log.items():
            success_rate = self.calculate_success_rate(outcomes)
            if success_rate < desired_threshold:
                self.adjust_thresholds(feature)
            elif success_rate > high_performance_threshold:
                self.refine_action_mappings(feature)

    def calculate_success_rate(self, outcomes):
        # Calculate the success rate for actions triggered by specific features
        return sum(outcomes) / len(outcomes)

    def adjust_thresholds(self, feature):
        # Adjust thresholds to optimize performance based on feedback
        pass

    def refine_action_mappings(self, feature):
        # Potentially re-map features to different actions based on success rates
        pass
    def __init__(self, action_logger):
        self.action_logger = action_logger

    def adjust_mappings_based_on_feedback(self):
        for action in self.action_logger.action_log.keys():
            success_rate = self.action_logger.get_action_success_rate(action)
            # Implement logic for adjusting thresholds and mappings based on success_rate 
'''


class ActionSuccessLogger:
    def __init__(self):
        self.action_log = defaultdict(list)

    def log_action(self, action, success, context=None, feedback=None):
        self.action_log[action].append({
            'success': success,
            'context': context,
            'user_feedback': feedback
        })

    def get_action_success_rate(self, action):
        if action not in self.action_log or not self.action_log[action]:
            return 0
        successes = [entry['success'] for entry in self.action_log[action]]
        return sum(successes) / len(successes)

class GameController:
    def __init__(self, feedback_system, action_logger):
        self.feedback_system = feedback_system
        self.action_logger = action_logger

        # Set up MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        self.metadata_topic = "metadata"
        self.distance_buffer = []

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.metadata_topic)

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode('utf-8')
            metadata = json.loads(payload)
            distance_to_target = metadata.get("distance_to_target")
            
            if distance_to_target is not None:
                self.distance_buffer.append(distance_to_target)
                if len(self.distance_buffer) > 1:
                    last_distance = self.distance_buffer[-2]
                    self.feedback_system.provide_feedback(distance_to_target)
                    self.log_action(metadata, distance_to_target, last_distance)
                else:
                    print(f"Initial distance to target: {distance_to_target}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def log_action(self, metadata, distance_to_target, last_distance):
        # Log the action outcome
        adjusted_force = metadata.get('adjusted_force')
        player_force = metadata.get('player_force')
        context = {
            'adjusted_force': adjusted_force,
            'player_force': player_force,
            'last_distance_to_target': last_distance,
            'current_distance_to_target': distance_to_target
        }
        success = distance_to_target < last_distance
        self.action_logger.log_action("distance_change", success, context=context, feedback="reward" if success else "distress")

    def run(self):
        self.mqtt_client.loop_start()
        try:
            while True:
                time.sleep(0.25)  # Adjust the sleep interval to 0.25 seconds
        except KeyboardInterrupt:
            print("Stopping...")
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()

if __name__ == "__main__":
    hub = "1-1"  # Example hub identifier, replace with your actual hub
    port = "2"   # Example port number, replace with your actual port
    usb_relay = USBRelay("/dev/ttyUSB0")  # Initialize with the correct USB port
    script_path = os.path.dirname(os.path.abspath(__file__))
    sound_file = os.path.join(script_path, "3khz_beep.wav")
    audio_device_index = 9  # Replace with the correct device index that supports audio output
    feedback_system = FeedbackSystem(hub=hub, port=port, usb_relay=usb_relay, sound_file=sound_file, audio_device_index=audio_device_index)
    action_logger = ActionSuccessLogger()
    controller = GameController(feedback_system, action_logger)
    controller.run()
