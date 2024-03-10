# this class will handle processes and their interactions

import multiprocessing

class ProcessManager:
    def __init__(self):
        self.active_processes = {}

    def start_process(self, name, function, *args):
        process = multiprocessing.process(target=function, args=args)
        print(f"Starting process'{ name }' | PID: { process.pid }")

        process.start() # start the process
        self.active_processes[process.pid] = (name, process) # save this to the list of active processes


    def get_process(self, pid):
        if pid in self.active_processes:
            return self.active_processes[pid]
        else:
            print(f"\t** Process [PID={pid}] not found **")

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
            print(f"\t** Process [PID={pid}] not found ** ")


