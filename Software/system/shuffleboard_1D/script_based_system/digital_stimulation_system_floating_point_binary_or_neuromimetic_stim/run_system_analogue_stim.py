import multiprocessing
import subprocess
import time
import os

def run_script(script_path):
    if script_path.endswith('.py'):
        subprocess.run(["python3", script_path])
    elif script_path.endswith('.yaml'):
        subprocess.run(["timeflux", script_path])
    else:
        raise ValueError(f"Unsupported script type: {script_path}")

if __name__ == "__main__":
    # Define the directory containing the scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List of scripts to run with relative paths
    scripts = [
        "A1_mqtt_client.py",
        "A2_brainflow_data_receiver.py",
        "B_signals_to_features.py",
        "B1_features_visualiser.py",
        "C_features_to_game.py",
        "D_shuffleboard_1D.py",
        "D1_session_history.py",
        "Neuromimetic_E_game_to_features.py",
        "Neuromimetic_F_signals_generator.py",
        "Neuromimetic_F1_Signals_Visualiser.py",
        "Neuromimetic_G_send_signals_to_usb_hub.py",
        "I_rewards_and_mappings.py"
    ]

    # Get the user-specified amount of time in minutes
    duration_minutes = float(input("Enter the duration to run the scripts (in minutes): "))
    duration_seconds = duration_minutes * 60

    processes = []
    for script in scripts:
        script_path = os.path.join(script_dir, script)
        p = multiprocessing.Process(target=run_script, args=(script_path,))
        p.start()
        processes.append(p)
        time.sleep(1)  # Wait for 1 second before starting the next script

    # Keep the scripts running for the specified duration
    time.sleep(duration_seconds)

    # Terminate all processes after the specified duration
    for p in processes:
        p.terminate()
        p.join()

    print("All scripts have been terminated after the specified duration.")
