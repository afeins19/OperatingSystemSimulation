# this is the entry point to the operating system. This file dispatches all other necessary resources and libraries
import argparse # module used for interpreting user commands
from command_handler import CommandHandler

def main():
    """initializing application resources here"""
    OS_LOGO = (f"\n      _.-;;-._ "
               f"\n-..-'|   ||   |"
               f"\n-..-'|_.-;;-._|"
               f"\n-..-'|   ||   |"
               f"\n-..-'|_.-''-._|")

    OS_HELP_MSG = f"Welcome to Michaelsoft Binbows { OS_LOGO }"

    parser = argparse.ArgumentParser(description='Task Manger') # setting up the main parser
    subparsers = parser.add_subparsers(dest='command', required=True)  # defining sub parsers for each command and thier args

        # PARSER FOR OS COMMANDS

    os_parser = subparsers.add_parser('os', help='Invoke general CLI commands')
    os_cmds = os_parser.add_subparsers(dest="os_command", required=True)

    # listing processes
    os_list = os_cmds.add_parser('list', help='Displays a list of all currently running processes')

    # help
    os_help = os_cmds.add_parser('help', help='Displays a list of all commands')

        # PARSERS FOR PROCESSES

    process_parser = subparsers.add_parser('process', help='Manage Processes')
    process_subparsers = process_parser.add_subparsers(dest='process_command', required=True)

    # starting processes
    process_start = process_subparsers.add_parser('start', help='Start a new process')
    process_start.add_argument('process_name', help='Name of the process')

    # killing processes
    process_kill = process_subparsers.add_parser('kill', help='Terminate a process that is currently running')
    process_kill.add_argument('process_name', help='Name of the process')
    process_kill.add_argument('--f', action='store_true', help='Force kill the process')

    # suspending processes
    process_suspend = process_subparsers.add_parser('suspend', help='Pause the execution of a process')
    process_suspend.add_argument('process_name', help='Name of the process')

    # resuming processes
    process_resume = process_subparsers.add_parser('resume', help='Resume a currently running process')
    process_resume.add_argument('process_name', help='Name of the process')

       # PARSERS FOR THREADS

    thread_parser = subparsers.add_parser('thread', help='Manage threads')
    thread_subparsers = thread_parser.add_subparsers(dest='thread_command', required=True)

    # starting processes
    thread_start = thread_subparsers.add_parser('start', help='Start a new thread')
    thread_start.add_argument('thread_name', help='Name of the thread')

    # killing processes
    thread_kill = thread_subparsers.add_parser('kill', help='Terminate a thread that is currently running')
    thread_kill.add_argument('thread_name', help='Name of the thread')

    # suspending processes
    thread_suspend = thread_subparsers.add_parser('suspend', help='Pause the execution of a thread')
    thread_suspend.add_argument('thread_name', help='Name of the thread')

    # resuming processes
    thread_resume = thread_subparsers.add_parser('resume', help='Resume a currently running thread')
    thread_resume.add_argument('thread_name', help='Name of the thread')


    # -- welcome page --
    print(OS_HELP_MSG, end='\n\n')

    # << program loop >>
    while True:
        try:
            user_cmd = input(">> ")

            if user_cmd == 'exit':
                break

            # give the parser the arguments
            args = parser.parse_args(user_cmd.split())

            # handler will execute the commands
            #   ... code here plz

        except SystemExit:
            # exceptions from external libraries
            pass

if __name__ == "__main__":
    main()