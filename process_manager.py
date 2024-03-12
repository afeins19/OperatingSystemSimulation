from multiprocessing import Process, Event, Array, Queue, Value
import time
import signal
import os
import threading
from log_config import setup_logger
from process_controller import ProcessControl



lgr = setup_logger(__name__)

class ProcessManager:
    def __init__(self):
        self.active_processes = {}

        # shared variable space for processes to share memory
        self.shared_memory_locations = []

    def process_wrapper(self, target_function, pause_event, resume_event, stop_event, *args):
        # allows for handling of process signals
        try:
            while not stop_event.is_set():
                if not pause_event.is_set():
                    target_function(*args)
                else:
                    resume_event.wait()

                time.sleep(0.1)
        except:
            return

    def get_process(self, pid):
        pid = int(pid)
        if pid in self.active_processes.keys():
            return self.active_processes[pid]['process']
        else:
            return None

    def create_shared_array(self, dtype, size):
        shared_array = Array(dtype, size)
        self.shared_memory_locations.append(shared_array)
        return shared_array

    def create_shared_value(self, dtype, initial_value):
        shared_value = Value(dtype, initial_value)
        self.shared_memory_locations.append(shared_value)
        return shared_value

    def create_shared_queue(self, maxsize):
        # creating a queue for message passing
        shared_queue = Queue(maxsize=maxsize)
        self.shared_memory_locations.append(shared_queue)
        return shared_queue

    def start_process(self, name, target_function, *args):
        pause_event = Event()
        resume_event = Event()
        stop_event = Event()

        process_control = ProcessControl(pause_event, resume_event, stop_event)
        modified_args = (process_control, name,) + args
        process = Process(target=target_function, args=modified_args)
        process.start()

        # save process data to dict
        self.active_processes[process.pid] = {
            'name': name,
            'process': process,
            'pause_event': pause_event,
            'resume_event': resume_event,
            'stop_event': stop_event
        }

        print(f"[[ Started process '{name}' | PID: {process.pid} ]]")
        return process.pid


    def kill_process(self, pid):
        pid = int(pid)
        if pid in self.active_processes:
            self.active_processes[pid]['stop_event'].set()
            self.active_processes[pid]['process'].join()
            del self.active_processes[pid]
            lgr.info(f"Process with PID {pid} stopped.")
        else:
            print(f"[[ NO PROCESS WITH [PID={pid}] ]]")
            lgr.info(f"[[ NO PROCESS WITH [PID={pid}] ]]")

    def suspend_process(self, pid):
        pid = int(pid)
        if pid in self.active_processes:
            self.active_processes[pid]['pause_event'].set()
            print(f"[[ PROCESS [PID={ pid }] SUSPENDED ]]")
            lgr.info(f"[[ PROCESS [PID={ pid }] SUSPENDED ]]")
    def resume_process(self, pid):
        pid = int(pid)
        if pid in self.active_processes:
            self.active_processes[pid]['pause_event'].clear()
            print(f"[[ PROCESS [PID={pid}] RESUMED ]]")
            lgr.info(f"[[ PROCESS [PID={pid}] RESUMED ]]")


