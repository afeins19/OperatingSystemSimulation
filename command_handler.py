# this file will define the CLI for the user. This is where the avialable commands for the user are stored

import argparse # argument parsing library
import multiprocessing
from psutil import Process
from thread_manager import ThreadManager
from threading import Thread
# import task_manager
from process_manager import ProcessManager
from tabulate import tabulate

from appmanager import AppManager

class CommandHandler:
    def __init__(self):
        self.process_manager = ProcessManager()
        self.thread_manager = ThreadManager()

        # initiazlie the app library
        self.app_manger = AppManager()


    def handle_command(self, args):
        # sends command and args to their respective handler functions
        if args.command == 'os':
            if args.os_command == 'list':
                self.os_list()

            if args.os_command == 'apps': # shows a list of apps
                self.show_user_apps()


        elif args.command == 'process':
            if args.process_command == 'start':
                # lookup process in the app library
                app = self.app_manger.get_app(args.process_name)

                if app:
                    self.start_process(name=args.process_name,
                                       function_to_execute=app)
                else:
                    print(f"\t** Unknown App `{ args.process_name }` **")

            elif args.process_command == 'kill':
                self.kill_processs(pid=args.process_name)

            elif args.process_command == 'suspend':
                self.suspend_proces(pid=args.process_name)

            elif args.process_command == 'resume':
                self.resume_proces(pid=args.proccess_name)

        elif args.command == 'thread':
            if args.thread_command == 'start':
                self.start_thread()

            elif args.thread_command == 'kill':
                self.kill_thread(pid=args.proccess_name)

            elif args.thread_command == 'suspend':
                self.suspend_thread(pid=args.proccess_name)

            elif args.thread_command == 'resume':
                self.resume_proces(pid=args.proccess_name)

                    # -- OS COMMANDS --
    def os_list(self):
        # get processes and get threads then send them to main for tabulation and display
        ps_processes = [p[1] for p in self.process_manager.active_processes.values()]
        ps_names = [p[0] for p in self.process_manager.active_processes.values()]

        threads = self.thread_manager.active_threads

        process_headers = ['PID', 'Name', 'Status' ,'Number of Threads']
        thread_headers = ['TID', 'is alive?']

        #ps_names = [ps[0] for ps in processes] # list of all process names
        #ps_processes: [Process] = [ps[1] for ps in processes]

        ps_info = {
            'pid' : [ps.pid for ps in ps_processes], # the process component of tuple and its pid value
            'name' : [name for name in ps_names], # name component of tuple
            #'status' : [ps.status() for ps in ps_processes],
            #'num_threads' : [len(ps.threads()) for ps in ps_processes]
            }

        th_info = {
            'tid' : [th.ident for th in threads],
            'is_active' : [th.isAlive() for th in threads] }


        self.display_system_info(ps_info, th_info)

        # -- SHOW A LIST OF APPS --
    def show_user_apps(self):
        app_data = {'Name' : self.app_manger.name_table.keys(),
                    'Function' : [str(func.__name__ + "()") for func in self.app_manger.name_table.values()]}

        app_table = tabulate(app_data, headers='keys', showindex='True')
        print(app_table)

        # -- DISPLAYING TASK MANAGER TO USER --
    def display_system_info(self, process_info={}, thread_info={}):
        # display processes first

        if len(process_info['pid']) == 0:
            print("\t** No Running Processes **")

        else:
            print("\tProcesses:")
            print(self.tabulate_processes(process_info))

        if len(thread_info['tid']) == 0 :
            print("\t ** No Running Threads **")

        else:
            print("\tThreads:")
            print(self.tabulate_threads(thread_info))

    def tabulate_processes(self, process_info={}):
        # create panel showing running processes
        process_table = tabulate(process_info, headers="keys", tablefmt="simplegrid")
        return process_table

    def tabulate_threads(self, thread_info={}):
        # create panel showing running threads
        thread_table = tabulate(thread_info, headers="keys", tablefmt="simplegrid")
        return thread_table

        # -- PROCESS COMMANDS --

    def start_process(self, name, function_to_execute, args=None):
        # logic for starting the process
        if args:
            pid = self.process_manager.start_process(name, function_to_execute, args=args)
        else:
            pid = self.process_manager.start_process(name, function_to_execute)


    def kill_processs(self, pid, force=False):
        self.process_manager.kill_process(pid=pid, force=force)

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





