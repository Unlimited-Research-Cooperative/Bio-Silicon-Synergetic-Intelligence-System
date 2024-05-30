Event monitor tools monitors the event. The signals sent on the topic **SIGNALS** are received by other scripts that extract features from it. These features are then translated into game commands that VizDoom can understand. With this tools you just need to start a local MQTT broker and then you can look on the events. This tool is helpful in keeping records for observation purposes.


<p align="center">
  <img src="https://raw.githubusercontent.com/Raghav67816/Bio-Silicon-Synergetic-Intelligence-System/main/images/Signals%20Monitor.png" />
  <img src="https://raw.githubusercontent.com/Raghav67816/Bio-Silicon-Synergetic-Intelligence-System/main/images/Signals%20Monitor%202.png" />
</p>

You need to enter the host and port of your MQTT broker, topics are already defined as constants in constanst.py file. After, setting them up just click `Start` button under `Settings` tab.

You will now recieve the inputs for the game that are extracted from the signals. Also, you can export the data with timestamp by clicking `Export` button under `Settings` tab.

!!! note
    You must create a file in which you want to write data the data. The tools does not create a new file.
