import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import pygame
from collections import defaultdict
import usbrelaymodule  # Assuming this is the correct module for USB relay

class FeedbackSystem:
    def __init__(self, usb_relay):
        # Initialize pygame for audio output
        pygame.mixer.init()
        self.reward_sound_path = "reward_sound.wav"  # Path to the reward sound file
        self.distress_sound_path = "distress_sound.wav"  # Path to the distress sound, inaudible to humans

        # USB relay for solenoid valve control
        self.usb_relay = usb_relay

    def play_sound(self, sound_path):
        # Play a sound from the specified path
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

    def activate_feeder(self):
        # Activate the feeder to dispense the reward mix using the USB relay
        self.usb_relay.turn_on()  # Turn on the USB relay to activate the feeder
        time.sleep(0.5)  # Keep the feeder active for 0.5 second
        self.usb_relay.turn_off()  # Turn off the USB relay to deactivate the feeder

    def provide_feedback(self, outcome):
        # Provide feedback based on whether the player is getting closer or further from the target
        if outcome == "reward":
            self.play_sound(self.reward_sound_path)
            self.activate_feeder()  # Also activate the feeder for positive reinforcement
        elif outcome == "distress":
            self.play_sound(self.distress_sound_path)

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
class GameController:
    def __init__(self, feedback_system, action_logger):
        self.feedback_system = feedback_system
        self.action_logger = action_logger

        # Set up MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("127.0.0.1", 1883, 60)
        self.outcome_topic = "game_outcome"

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.outcome_topic)

    def on_message(self, client, userdata, message):
        try:
            payload = message.payload.decode('utf-8')
            outcome_data = json.loads(payload)
            outcome = outcome_data.get("outcome")
            if outcome:
                self.feedback_system.provide_feedback(outcome)
                self.log_action(outcome_data, outcome)
        except Exception as e:
            print(f"Error processing message: {e}")

    def log_action(self, outcome_data, outcome):
        # Log the action outcome
        round_num = outcome_data.get('round')
        distance_to_target = outcome_data.get('distance_to_target')
        context = {
            'round': round_num,
            'distance_to_target': distance_to_target
        }
        success = outcome == "reward"
        self.action_logger.log_action("execute_shot", success, context=context, feedback=outcome)

    def run(self):
        self.mqtt_client.loop_start()
        try:
            while True:
                time.sleep(1)  # Keep the script running
        except KeyboardInterrupt:
            print("Stopping...")
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()

if __name__ == "__main__":
    usb_relay = usbrelaymodule.Relay("relay_device_identifier")  # Initialize with appropriate identifier
    feedback_system = FeedbackSystem(usb_relay=usb_relay)
    action_logger = ActionSuccessLogger()
    controller = GameController(feedback_system, action_logger)
    controller.run()