# this file will define the CLI for the user. This is where the avialable commands for the user are stored

import argparse # argument parsing library
# import task_manager
from process_manager import ProcessManager
class CommandHandler:
    def __init__(self):
        self.process_manager = ProcessManager()


    def handle_command(self, args):
        # sends command and args to their respective handler functions
        if args.command == 'os':
            if args.os_command == 'list':
                self.os_list()

        elif args.command == 'process':
            if args.process_command == 'start':
                self.start_process(name=args.process_name)

            elif args.process_command == 'kill':
                self.kill_processs(pid=args.proccess_name)

            elif args.process_command == 'suspend':
                self.suspend_proces(pid=args.proccess_name)

            elif args.process_command == 'resume':
                self.resume_proces(pid=args.proccess_name)

        elif args.command == 'thread':
            if args.thread_command == 'start':
                self.start_process()

            elif args.thread_command == 'kill':
                self.kill_processs(pid=args.proccess_name)

            elif args.thread_command == 'suspend':
                self.suspend_proces(pid=args.proccess_name)

            elif args.thread_command == 'resume':
                self.resume_proces(pid=args.proccess_name)

                    # -- OS COMMANDS --
    def os_list(self):
        # logic for showing processes to the user
        pass

        # -- PROCESS COMMANDS --

    def start_process(self, name, function_to_execute, args=None):
        # logic for starting the process
        if args:
            pid = self.process_manager.start_process(name, function_to_execute, args=args)
        else:
            pid = self.process_manager.start_process(name, function_to_execute)
        print(f"Starting process '{name}' | PID: {pid}")
        pass

    def kill_processs(self, pid):
        # logic for killing a process
        pass

    def suspend_process(self, pid):
        # logic for suspending a processs
        pass

    def resume_proces(self, pid):
        # logic for resuming a process
        pass

        # -- THREAD COMMANDS --

    def start_thread(self):
        # logic for starting a thread
        pass

    def suspend_thread(self, tid):
        # logic for suspending a thread
        pass

    def resume_thread(self, tid):
        # logic for resuming a thread
        pass

    def kill_thread(self, tid):
        # logic for killing a thread
        pass



