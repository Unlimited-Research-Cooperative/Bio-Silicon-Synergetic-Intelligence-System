import zmq
import numpy as np
import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import usbrelaymodule 
import usb_audio_module  
import pygame

class NeuralSignalSubscriber:
    def __init__(self, context, address):
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def get_signals(self):
        try:
            message = self.socket.recv_string(zmq.NOBLOCK)
            return np.fromstring(message, sep=',')  # Assuming signals are sent as comma-separated values
        except zmq.Again:
            return np.zeros(32)  # Return zeros if no message is available

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

    def provide_feedback(self, event_type):
        # Provide feedback based on whether the player is getting closer or further from the target
        if event_type == "closer":
            self.play_sound(self.reward_sound_path)
            self.activate_feeder()  # Also activate the feeder for positive reinforcement
        elif event_type == "further":
            self.play_sound(self.distress_sound_path)

class ActionSuccessLogger:
    """
    Logs success metrics, contextual information, and user feedback for actions.
    """
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

class GameController:
    def __init__(self, feedback_system, event_monitor, action_logger, zmq_context):
        self.feedback_system = feedback_system
        self.event_monitor = event_monitor
        self.action_logger = action_logger
        self.dynamic_decoder = DynamicSignalDecoder(self.action_logger)
        self.incoming_signals_sub = NeuralSignalSubscriber(zmq_context, "tcp://localhost:5444")
        self.outgoing_signals_sub = NeuralSignalSubscriber(zmq_context, "tcp://localhost:5557")
        self.last_decoder_update = datetime.now()

    def run(self):
        while True:
            current_time = datetime.now()
            game_events = self.event_monitor.poll_events()
            for event in game_events:
                self.feedback_system.provide_feedback(event)
            
            # Refresh feedback system at 10Hz
            incoming_signals = self.incoming_signals_sub.get_signals()
            outgoing_signals = self.outgoing_signals_sub.get_signals()

            # Adjust dynamic mappings every 1 minute
            if current_time - self.last_decoder_update > timedelta(minutes=1):
                self.dynamic_decoder.adjust_mappings_based_on_feedback()
                self.last_decoder_update = current_time

            time.sleep(0.1)  # 10Hz refresh rate

if __name__ == "__main__":
    zmq_context = zmq.Context()
    visualizer = NeuralMappingVisualizer()
    usb_relay = usbrelaymodule.Relay("relay_device_identifier")  # Initialize with appropriate identifier
    feedback_system = FeedbackSystem(usb_relay=usb_relay)
    event_monitor = GameEventMonitor(zmq_context)
    action_logger = ActionSuccessLogger()
    controller = GameController(feedback_system, event_monitor, action_logger, zmq_context)
    controller.run()

    while True:
        event_monitor.poll_and_process_events(feedback_system)
        time.sleep(0.1)  # Poll every 0.1 seconds to reduce CPU usage