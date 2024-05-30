Our system mainly uses Python, thanks to its readability and wide range of packages in the field of data science, embedded and communication.

Our project implements some utilities that makes the workflow simple and efficient. In this page you will get to know about it each utility.

!!! note
    We are planning to publish these utilities as a python package to make it easy to develop the main dashboard. Once, all the code seems stable, it will be released as a package on GitHub. However, the documentation for that package remain the same.


## Constants

All the constant values are defined in the `constants.py`, it also contains some data structures. You can import these constants and use the values. It helps in maintaining code quality and prevents repetition.

### Action
These are defined actions that are used in mainly used with VizDoom game.

| Name          | Value         | Type |
|---------------|---------------|------|
| MOVE_FORWARD  | MOVE_FORWARD  | str  |
| MOVE_BACKWARD | MOVE_BACKWARD | str  |
| TURN_LEFT     | TURN_LEFT     | str  |
| TURN RIGHT    | TURN RIGHT    | str  |
| USE           | USE           | str  |
| ATTACK        | ATTACK        | str  |

This class also has a classmethod **to_dict()**. This method returns this constant data structure as a dictionary, this allows flexibility to system where it is being used.

Example usage:
```py

from constants import Action

actions = Action()
print(actions.MOVE_FORWARD)
print(actions.to_dict())
```

You might think that why we would just define constants and create a classmethod to convert it to dictionary. Well, our system used these constants very often and at some point they were also required as a dictionary.

### ActionMap
When we decode features into `Actions` i.e move forward, backward or turn left or right etc. The actions are returned with some properties. This ActionMap class holds the same properties.

| Name                      | Value                            | Type  |
|---------------------------|----------------------------------|-------|
| rms                       | (Actions.MOVE_FORWARD, 3.96e-07) | tuple |
| variance                  | (Actions.TURN_LEFT, 1.074e-26)   | tuple |
| spectral_entropy          | (Actions.USE, 0.7)               | tuple |
| peak_counts               | (Actions.ATTACK, 3)              | tuple |
| higuchi_fractal_dimension | (Actions.TURN_RIGHT, 1.35e-15)   | tuple |
| zero_crossing_rate        | (Actions.MOVE_FORWARD, 0.1)      | tuple |
| delta_band_power          | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| theta_band_power          | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| alpha_band_power          | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| beta_band_power           | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| peak_heights              | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| std_dev                   | (Actions.MOVE_FORWARD, 7.5e-14)  | tuple |
| centroids                 | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| spectral_edge_density     | (Actions.MOVE_FORWARD, 0.5)      | tuple |
| evolution_rate            | (Actions.MOVE_FORWARD, 0.5)      | tuple |

You can learn about the terms used in this project from the page `Frequent Terms`

This data structure contains all data to be tuple, this class also has a `to_dict()` method wich converts they keys and the values set by the user to a dictionary.

Example Usage:
```py
from constants import ActionMap

action_map = ActionMap()
actions_default = action_map.to_dict()  # Action map with default values
print(action_default)
```
**Output:**
``` py
{'rms': ('MOVE_FORWARD', 3.96e-07), 'variance': ('TURN_LEFT', 1.074e-26), 'spectral_entropy': ('USE', 0.7), 'peak_counts': ('ATTACK', 3), 'higuchi_fractal_dimension': ('TURN_RIGHT', 1.35e-15), 'zero_crossing_rate': ('MOVE_FORWARD', 0.1), 'delta_band_power': ('MOVE_FORWARD', 0.5), 'theta_band_power': ('MOVE_FORWARD', 0.5), 'alpha_band_power': ('MOVE_FORWARD', 0.5), 'beta_band_power': ('MOVE_FORWARD', 0.5), 'peak_heights': ('MOVE_FORWARD', 0.5), 'std_dev': ('MOVE_FORWARD', 7.5e-14), 'centroids': ('MOVE_FORWARD', 0.5), 'spectral_edge_density': ('MOVE_FORWARD', 0.5), 'evolution_rate': ('MOVE_FORWARD', 0.5)}

```

### AnalyzeSignalsResult

The signals received from MEAs are analysed to understand the nature of incoming data and the data we will be working further with. Many mathematical formulas are used to determine the features of signals.

You can find these mathematical formulas in `Mathematical Formulas` section. 

| Name                      | Value | Type  |
|---------------------------|-------|-------|
| peak_height               |   -   | Any   |
| peak_counts               |   -   | int   |
| variance                  |   -   | float |
| std_dev                   |   -   | float |
| rms                       |   -   | float |
| band_features             |   -   | Any   |
| delta_band_power          |   -   | Any   |
| theta_band_power          |   -   | Any   |
| alpha_band_power          |   -   | Any   |
| beta_band_power           |   -   | Any   |
| centroids                 |   -   | Any   |
| spectral_edge_densities   |   -   | Any   |
| higuchi_fractal_dimension |   -   | Any   |
| zero_crossing_rate        |   -   | Any   |
| evolution_rate            | -     | Any   |


This method also contains `to_dict()` method but it also contains a `to_python_float()` method. The `to_python_float()` convert **numpy.float64** to a python float if there is any.


## Data Manager

The system involves transmitting and receiving data alot. Currently, we are using **Paho MQTT** for this purpose. The scripts in themselves need to send data from one to another. To facilitate this complex movement of data we implemented a `DataManager` class which handles these tasks seamlessly.

It has the following features:

- Multi-threaded / Non-Blocking
- Transmit & Receive Concurrently
- Flexible
- Easy to Setup

The `DataManager` needs to be instantiated directly with the following parameters:

| Name                   | Default Value | Type          | Description                                                                                    |
|------------------------|---------------|---------------|------------------------------------------------------------------------------------------------|
| client_id              |      None     |      str      | A client name to be used as an identifier for the client                                       |
| topic_sub              | None          | str           | A topic to subscribe, let it be None if client is only for receiving messages                  |
| topic_pub              | None          | str           | A topic to publish message on, let it be None if client is only for sending messages           |
| processing_func        | None          | function: Any | A function you want to execute when message is received                                        |
| close_after_first_list | False         | bool          | Set to True if you want to destroy client after receiving single message, else let it be False |

### Constructing client
```py
from data_manager import DataManager

data_m = DataManager("example_client")
```
For now lets keep all the parameters to default i.e None, in this way create a client that does nothing. DataManager needs a `config.env` file which consist two variable `host` and `port`.

!!! note
    Make sure that you are running a local or cloud MQTT broker at the defined host and port else, this will raise a **Connection Refused** error.

### Receiving data
For only recieving messages you need to specify `topic_sub` and leave `topic_pub` to None.

```py
from data_manager import DataManager

data_m = DataManager("example_client", topic_sub="test_topic")
data_m.listen()
```

**Just 2 lines**, yeah just 2 lines to start receiving messages. This starts the server loop on a new thread which prevents blocking main thread. You can also pass a function that you want to execute when you receive any data, this also helps you to utilise data that you will be receving. 

For example, lets say we will be receving a string on **test_topic** and to that we string we want to append **foo** and print it.

```py

def foo(msg):
    print(f"{msg} foo")

data_m = DataManager("example_client", topic_sub="test_topic", processing_func=foo)
data_m.listen()

```

Now this will print a string that will have **foo** in it. You can pass your own function but make sure you take the incoming message as the first argument of your custom function.

### Sending data
Sending data is simple, you need to specify `topic_pub` for the client. For such case you don't need to specify `processing_func`.

```py

from data_manager import DataManager

data_m = DataManager("example_client", topic_pub="test_pub_topic")
data_m.set_data("This is the message I want to send.")
data_m.publish()

```

In this way you send data in just 3 lines. But, you need to be carefull while sending data. Firstly, you need to specify data through `set_data()` function, `self.data` is the property of DataManager class which is set by the user through this function. Then you need to call the function `publish(sleep_time: float)`

Data Manager also has a `publish_data()` function, but the function `publish()` executes publish_data() function on a new thread so that main thread is not blocked.

### Sending & Receving Data Concurrently

We are not done yet, you can also receive and set data **concurrently** through **same class**. You just need to specify both `topic_sub` and `topic_pub`

```py

def foo(msg):
    print(f"{msg} foo")

data_m = DataManager("example_client", topic_sub="test_topic", topic_pub="test_pub_topic" ,processing_func=foo)
data_m.listen()

data_m.set_data("I am sending this message")
data_m.publish()

# Your code ......
# And it will not be blocked
```

## Logging Service
Our system is wide and complex so it becomes really important to keep records of events being fired behind the scene. So, to save logs we implemented a `LoggingService` class that uses `DataManager` and listens for logging data on topic **logs**. This includes a `RotatingFileHandler` that means if the size of log file reaches the limit a new file will be created and data will be written to it. The limit set is 200 MB for each file.

### Formats
The format in which we want to save our logs is an important parameter, we have provided a class containing string of all formats available with python's built-in package `logging`

```py
class Formats:
    BASIC_FMT = "%(asctime)s %(levelname)s %(message)s"
    FUNC_FMT = "%(asctime)s: %(levelname)s - %(funcName)s - %(message)s"
    LINE_NO_FMT = "%(asctime)s: %(levelname)s -%(lineno)d - %(message)s"
    
```

### Logging data
To log data you need to send a dictionary converted into json as string on topic **logs**. The logger will automatically log the data whenever you send a json on the topic. Make sure to follow the given format for dictionary.

```json
{
    'level': "LEVEL_INT",
    'msg': "YOUR_MESSAGE_OR_EVENT",
    'funcName' : 'NAME_OF_THE_FUNCTION'  # put as 'NA' if you dont want to use it.
    'lineno' : 'LINE_NUMBER' # put as 'NA' if you dont want to use it.
}
```

The parameters `level`, `msg` are important and cannot be set NA.

### Convert to database
If you have a lot of logs then it might be difficul to read that through the file itself, to make analysing the logs easy we provide a function `convert_to_database()` which takes no argument and converts the log file into a sqlite3 database file. Also make sure to follow the given template for .db file. You can download the template.db file from <a href="https://github.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System/raw/main/docs/assets/template.db">here</a>.
