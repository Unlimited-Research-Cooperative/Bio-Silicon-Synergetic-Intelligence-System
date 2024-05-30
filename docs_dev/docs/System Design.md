This research involves complex software worflow. Therefore, it becomes essential to visualize the process. 

![Proccess](https://raw.githubusercontent.com/Unlimited-Research-Cooperative/Human-Brain-Rat/main/images/bidirectional_brain_computer_communication.jpg)

- Step 1: Raw EEG signals are fetched over 32 channels from the subject.
- Step 2: The recieved analog signals are then converted into digital signals.
- Step 3: In this step the digital signals are decoding into movements using features (e.g move forward or backward, turn left or right).
- Step 4: VizDoom has its own set of commands to perform defined action inside of the game environment. The movements are converted into VizDoom commands.

At each step some mathematical formulas are used to process data, these formulas can be found in papers from `References` section.

## Tools

Under application we provide main software and tools such as Signal Simulator & Script Monitor. These tools can be found on GitHub Repo releases.

Currently, we have two tools

- Signal Simulator - The actual signals are generated through MEA that are implanted into the subjects brain. But for testing the system software we simulate signals using this tools. It mimics the FreeEEG board.

- Scripts Monitor - The data is being published on different Mqtt topics by scripts and some scripts simultaneously. While development it becomes messy to open multiple terminal windows and look at each of them one by one. This tools lets you see what's being published on topics continously.

## Dashboard

The main software has a sci-fi user interface and delivers expectional performance. This is used to monitor everything including the subject's stress, reward, signals, data visualization, data logging etc. 

<figure markdown="span">
  ![User Inteface](https://raw.githubusercontent.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System/main/images/ui.png)
  <figcaption>UI under development</figcaption>
</figure>

The interface is built using [React JS](https://react.dev/) and CSS. To make it run out-of-browser we use [Electron JS](https://electronjs.org). The application communicates with the backend written in Python using WebSockets and the scripts communicates through `Mqtt` Pub-Sub system.

There are following files:

- **data_manager.py**: It has `DataManager` class which provides functions to publish data and listen to incoming messages concurrently. For more details refer to **Data Manager**.

- **constants.py**: This file in the root directory contains constants and data strcutures with appropraite class methods for their conversion.

- **signal_simulator.py**: It generates synthetic signals for testing purposes.

- **signals_to_features.py**: It receives the generated signals through topic **simulated signals**, upon receiving signals it extract features from it and send them to **features_to_game.py**

- **features_to_game.py**: VizDoom has its own set of commands. The features that are translated into actions are in raw form, which might not be understood by the Doom Engine. It converts these raw actions into game commands that are known by VizDoom.

