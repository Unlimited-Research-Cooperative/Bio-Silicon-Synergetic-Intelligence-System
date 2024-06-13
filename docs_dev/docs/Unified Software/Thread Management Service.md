
# Thread Management Service

The software will run many process in the background and we need to keep track of them in order to make user experience seamless.

This services includes a Python file with a `Thread Manager` class and an app to see running tasks and to terminate threads.

## Thread Manager API Reference

It has only two methods to work with, first is `start_new` and `terminate_thread`

### Starting a new thread
To start a new thread you need to use the `start_new` method and provide a `function: callable` to run, `target_args` the arguments for the target function and `service_name` an service identifier which will make it easier for users to understand which thread belong to which task.

```py
from time import sleep
from thread_manager import ThreadManager

manager = ThreadManager()

def example_func():
    while True:
        print("Hello World")
        sleep(2)

# pass an empty list if your function needs no arguments
manager.start_new(example_func, [], "example_service")
```

### Terminating a thread
It's very simple to terminate a thread. You just need to pass the `service_name`
```py
"""
Assuming that you already have starteda new thread
"""

manager.kill_thread("example_service")
```

As discussed above it aslo has a GUI app.

<div align="center" style="display: flex">
    <img src="https://raw.githubusercontent.com/Unlimited-Research-Cooperative/Bio-Silicon-Synergetic-Intelligence-System/main/images/thread%20app.png" />
</div>

!!! note
    UI will be changed in future, this is a very basic version of the UI and the app.

