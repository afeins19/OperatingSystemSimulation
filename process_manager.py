# this class will handle processes and their interactions
import time
from multiprocessing import Process
import psutil

class ProcessManager:
    def __init__(self):
        self.active_processes = {}

    def start_process(self, name, function, *args):
        process = Process(target=function, args=args)
        process.start() # start the process
        print(f"Starting process '{name}' | PID: {process.pid}")
        self.active_processes[process.pid] = (name, process) # save this to the list of active processes

        return process.pid

    def get_process(self, pid):
        if pid in self.active_processes:
            return self.active_processes[pid]
        else:
            print(f"\t** Process [PID={pid}] not found **")

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

    def kill_process(self, pid, force=False):
        if pid in self.active_processes:
            process = self.active_processes[pid][1] # retrieve process
            process.terminate() # end the process

            if force:
                print(f"\t** Terminating process [PID={ pid }] forcefully ** ")
            else:
                process.join()

            del self.active_processes[pid]

        else:
            print(f"\t** Process [PID={ pid }] not found ** ")



