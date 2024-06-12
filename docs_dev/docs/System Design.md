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

!!! warning ""
    We are now dropping the support of Scripts Monitor tool because it will be intergrated within the first version of Unified Software.

