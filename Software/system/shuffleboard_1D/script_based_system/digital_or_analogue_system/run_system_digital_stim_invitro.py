import sys
import multiprocessing
import subprocess
import time
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox

def run_script(script_path):
    if script_path.endswith('.py'):
        subprocess.run(["python3", script_path])
    elif script_path.endswith('.yaml'):
        subprocess.run(["timeflux", script_path])
    else:
        raise ValueError(f"Unsupported script type: {script_path}")

def start_scripts(real, duration_minutes):
    # Define the directory containing the scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List of scripts to run with relative paths
    scripts = [
        "A1_mqtt_client.py",
        "B_signals_to_features.py",
        "invitro/C_features_to_game.py",
        "shuffleboard1d/D_shuffleboard_1D.py",
        "shuffleboard1d/D1_session_history.py",
        "invitro/digital_stim/E_F_features_to_floating_point_binary.py",
        "invitro/digital_stim/G_send_signals_to_usb_hub.py",
        "I_rewards_and_mappings.py"
    ]

    # Add the appropriate data receiver script based on user input
    if real:
        scripts.insert(0, "A2_brainflow_data_receiver.py")
    else:
        scripts.insert(0, "SimulateNeuralData_A2_data_receiver.py")

    duration_seconds = duration_minutes * 60

    processes = []
    for i, script in enumerate(scripts):
        script_path = os.path.join(script_dir, script)
        p = multiprocessing.Process(target=run_script, args=(script_path,))
        p.start()
        processes.append(p)
        
        if i == 0:
            # Wait for 10 seconds after running the first script
            time.sleep(10)
        else:
            time.sleep(1)  # Wait for 1 second before starting the next script

    # Keep the scripts running for the specified duration
    time.sleep(duration_seconds)

    # Terminate all processes after the specified duration
    for p in processes:
        p.terminate()
        p.join()

    QMessageBox.information(None, "Info", "All scripts have been terminated after the specified duration.")

class ScriptRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Script Runner')
        self.setStyleSheet("background-color: black; color: #00D8D8;")

        main_layout = QVBoxLayout()

        duration_layout = QHBoxLayout()
        duration_label = QLabel('Duration of Experiment (in minutes):')
        self.duration_entry = QLineEdit()
        duration_label.setStyleSheet("color: #00D8D8;")
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.duration_entry)

        button_layout = QHBoxLayout()
        real_button = QPushButton('Run Real')
        simulation_button = QPushButton('Run Simulation')
        real_button.setStyleSheet("background-color: #00D8D8; color: black;")
        simulation_button.setStyleSheet("background-color: #00D8D8; color: black;")
        real_button.clicked.connect(self.run_real)
        simulation_button.clicked.connect(self.run_simulation)
        button_layout.addWidget(real_button)
        button_layout.addWidget(simulation_button)

        main_layout.addLayout(duration_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
    
    def run_real(self):
        self.start_scripts_wrapper(True)
    
    def run_simulation(self):
        self.start_scripts_wrapper(False)
    
    def start_scripts_wrapper(self, real):
        try:
            duration_minutes = float(self.duration_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number for the duration.")
            return
        
        start_scripts(real, duration_minutes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    runner = ScriptRunner()
    runner.show()
    sys.exit(app.exec_())
