from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from time import sleep

class ThreadInfo:
    thread_object: Thread
    service_name: str
    thread_id: int

class ThreadManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=20)
        self.services = {}

    """
        start_new

        start new thread store it's pid and corresponding service name

        args:
        target - target function
        isDaemon - set true if you want to start a deamon thread
        target_args - arguments to pass to the target function
        service_name - provide a service name to make it more convinient
	"""

    def start_new(self, target: callable, target_args: list, service_name: str, isDaemon: bool = True):
        try:
            thread = Thread(target=target, args=target_args)
            thread.isDaemon = isDaemon
            thread_id = id(thread)
            thread_data = ThreadInfo()
            thread_data.thread_object = thread
            thread_data.service_name = service_name
            thread_data.thread_id = thread_id

            self.services[service_name] = thread_data

            self.executor.submit(thread.start)
            return thread_id

        except Exception as threading_error: 
            print(str(threading_error))

    """
	kill_thread

	kill running thread and exit safely
	args: 
	    service_name - id of thread to terminate
	"""
    def kill_thread(self, service_name: str):
        try:
            thread_obj = self.services[service_name].thread_object
            del self.services[service_name]
            future = self.executor.submit(thread_obj.join, timeout=0)
            future.cancel()

        except Exception as error:
            print(str(error))

