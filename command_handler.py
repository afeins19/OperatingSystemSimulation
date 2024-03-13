# this file will define the CLI for the user. This is where the avialable commands for the user are stored

import argparse # argument parsing library
import multiprocessing

import psutil
from psutil import Process
from thread_manager import ThreadManager
from threading import Thread
# import task_manager
from process_manager import ProcessManager
from tabulate import tabulate

from app_manager import AppManager
from log_config import setup_logger

lgr = setup_logger(__name__)

class CommandHandler:
    def __init__(self):
        self.process_manager = ProcessManager()
        self.thread_manager = ThreadManager()
        self.app_manager = AppManager()

    def handle_command(self, args):
        if args.command == 'os':
            if args.os_command == 'list':
                self.os_list()

            if args.os_command == 'apps':
                self.show_user_apps()

        elif args.command == 'process':
            if args.process_command == 'start':
                app = self.app_manager.get_app(args.process_name)
                if app is not None:
                    self.start_process(name=args.process_name, function_to_execute=app)
                else:
                    print(f"\t** Unknown App `{args.process_name}` **")

            elif args.process_command == 'kill':
                self.kill_process(pid=args.pid)

            elif args.process_command == 'suspend':
                self.suspend_process(pid=args.pid)

            elif args.process_command == 'resume':
                self.resume_process(pid=args.pid)

        elif args.command == 'thread':
            if args.thread_command == 'start':
                app = self.app_manager.get_app(args.thread_name)
                if app is not None:
                    self.start_thread(app)
                else:
                    print(f"\t** Unknown App `{args.thread_name}` **")

            elif args.thread_command == 'kill':
                self.kill_thread(tid=args.tid)

            elif args.thread_command == 'suspend':
                self.suspend_thread(tid=args.tid)

            elif args.thread_command == 'resume':
                self.resume_thread(tid=args.tid)


    def os_list(self):
        ps_processes = [p['process'] for p in self.process_manager.active_processes.values()]
        ps_names = [p['name'] for p in self.process_manager.active_processes.values()]
        ps_suspended = [p['pause_event'].is_set() for p in self.process_manager.active_processes.values()]

        threads = self.thread_manager.active_threads.values()

        th_tids = [t[0].ident for t in self.thread_manager.active_threads.values()]
        th_statuses = [t[0].is_alive() for t in self.thread_manager.active_threads.values()]
        th_stop_events = [t[1].is_set() for t in self.thread_manager.active_threads.values()]

        process_headers = ['PID', 'Name', 'Status' ,'Number of Threads']
        thread_headers = ['TID', 'is_alive', 'is_suspended']

        ps_info = {'pid': [ps.pid for ps in ps_processes],
                   'name': [name for name in ps_names],
                   'is_suspended' : [status for status in ps_suspended],
                   }

        th_info = {'tid': [tid for tid in th_tids],
                   'is_active': [ia for ia in th_statuses],
                   'is_suspended': [se for se in th_stop_events]}
        self.display_system_info(ps_info, th_info)

    def show_user_apps(self):
        app_data = {'Name': self.app_manager.name_table.keys(),
                    'Function': [str(func.__name__ + "()") for func in self.app_manager.name_table.values()]}
        app_table = tabulate(app_data, headers='keys', showindex='True')
        print(app_table)

    def display_system_info(self, process_info={}, thread_info={}):
        if len(process_info['pid']) == 0:
            print("\t** No Running Processes **")
        else:
            print("\n\t\t- Processes -")
            print(self.tabulate_processes(process_info))

        if len(thread_info['tid']) == 0:
            print("\n\t ** No Running Threads **")
        else:
            print("\n\t\t - Threads -")
            print(self.tabulate_threads(thread_info))

    def tabulate_processes(self, process_info={}):
        process_table = tabulate(process_info, headers="keys", tablefmt="simplegrid")
        return process_table

    def tabulate_threads(self, thread_info={}):
        thread_table = tabulate(thread_info, headers="keys", tablefmt="simplegrid")
        return thread_table

    def start_process(self, name, function_to_execute, args=None):
        if args:
            pid = self.process_manager.start_process(name, function_to_execute, args=args)
        else:
            pid = self.process_manager.start_process(name, function_to_execute)

    def kill_process(self, pid, force=False):
        self.process_manager.kill_process(pid=pid)

    def suspend_process(self, pid):
        self.process_manager.suspend_process(pid=pid)

    def resume_process(self, pid):
        self.process_manager.resume_process(pid=pid)

    def start_thread(self, function_to_execute, args=None):
        if args:
            self.thread_manager.start_thread(function_to_execute, args)
        else:
            self.thread_manager.start_thread(function_to_execute, args)

    def suspend_thread(self, tid):
        self.thread_manager.suspend_thread(tid=tid)

    def resume_thread(self, tid):
        self.thread_manager.resume_thread(tid=tid)

    def kill_thread(self, tid):
        self.thread_manager.kill_thread(tid=tid)
