# this class will handle processes and their interactions
import multiprocessing
import time
from multiprocessing import Array, Process, Value, Queue
import psutil
import os
import signal
import threading

# Value - shared variable
# Queue - message passing

class ProcessManager:
    def __init__(self):
        self.active_processes = {}

        # shared variable space for processes to share memory
        self.shared_memory_locations = []
        self.log = []

        # create a thread to check for completed processses and drop em from active_processes
        self.monitoring_thread = threading.Thread(target=self.start_monitoring_processes)
        self.monitoring_thread.start()
    def start_monitoring_processes(self): # call processs is_active check function repeatedly
        while True:
            self.remove_completed_processes()
            time.sleep(1)

    def remove_completed_processes(self):
        to_pop = []

        for pid, ps_tuple in self.active_processes.items():
            ps: Process = ps_tuple[1]

            if not ps.is_alive():
                to_pop.append(pid)

        for pid in to_pop:
            del self.active_processes[pid]
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

    def start_process(self, name, function, *args):
        process = Process(target=function, args=args)

        process.start() # start the process
        process.join()
        self.active_processes[process.pid] = (name, process)  # save this to the list of active processes
        print(f"Started process '{ name }' | PID: { process.pid }")


        return process.pid

    def get_process(self, pid):
        if pid in self.active_processes:
            return self.active_processes[pid]
        else:
            return None

    def get_process_threads(self, pid):
        ps = psutil.Process(pid)
        return ps.threads() # list of threads?

    def process_stats(self, pid):
        # returns a dict with statistics about the process
        try:
            ps = psutil.Process(pid)

            stats = {
                'PID' : ps.pid,
                'Name' : ps.name(),
                'Status' : ps.status(),
                'Number of threads' : len(ps.threads())
            }

            return stats

        except psutil.NoSuchProcess:
            print(f"\t** Process [PID={pid}] Not Found **")

        return None

    def get_active_process_stats(self):
        p_stats = []

        for process in self.active_processes:
            p_stats.append(process)

        return p_stats

    def kill_process(self, pid, force=False):
        pid = int(pid) # store pid as int since thats how the keys in the dict are

        if pid in self.active_processes.keys():
            process: Process = self.active_processes[pid][1] # retrieve process
            process.terminate() # end the process

            if not force:
                print(f"\t** Terminating process [PID={ pid }]  ** ")
                process.join()

            else:
                print(f"\t** Terminating process [PID={pid}] forcefully ** ")

            del self.active_processes[pid] # drop the process from active list

        else:
            print(f"\t** Process [PID={ pid }] not found ** ")

    def suspend_proccess(self, pid):
        os.kill(pid, signal.SIGSTOP) # sends a stop signal to the process

    def resume_process(self, pid):
        os.kill(pid, signal.SIGCONT) # sends a signal to continue the process


