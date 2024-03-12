# this is the entry point to the operating system. This file dispatches all other necessary resources and libraries
import argparse  # module used for interpreting user commands
from tabulate import tabulate
from command_handler import CommandHandler
import time
from log_config import setup_logger
lgr = setup_logger(__name__)

def debug(arg):
    print(f"\tARGS={arg}")

def process_user_input(parser, command_handler):
    # setup handler instance
    psr = parser
    cmd_handler = command_handler


    try:
        time.sleep(.1)
        user_cmd = input(">> ")

        # log the input
        # lgr.info(f"USER_INPUT: {user_cmd}")

        if user_cmd == 'exit':
            return None

        # give the parser the arguments
        args = psr.parse_args(user_cmd.split())
        lgr.info(f"[[ USER INPUT : {args}")

        # debug for some problems
        # debug(args)

        cmd_handler.handle_command(args)  # give commands with args to the cmd handler

    except SystemExit:
        # exceptions from external libraries won't cause crashes
        lgr.info(f"EXCEPTION: SystemExit")


    return 1
def main():
    """initializing application resources here"""
    OS_LOGO = (f"\n      _.-;;-._ "
               f"\n-..-'|   ||   |"
               f"\n-..-'|_.-;;-._|"
               f"\n-..-'|   ||   |"
               f"\n-..-'|_.-''-._|")

    OS_HELP_MSG = f"Welcome to psuOS {OS_LOGO}"

    parser = argparse.ArgumentParser(description='Task Manger')  # setting up the main parser
    subparsers = parser.add_subparsers(dest='command', required=True)  # defining sub parsers for each command and their args

    # PARSER FOR OS COMMANDS
    os_parser = subparsers.add_parser('os', help='Invoke general CLI commands')
    os_cmds = os_parser.add_subparsers(dest="os_command", required=True)

    # listing processes
    os_list = os_cmds.add_parser('list', help='Displays a list of all currently running processes')

    # help
    os_help = os_cmds.add_parser('help', help='Displays a list of all commands')

    # list all user apps
    os_apps = os_cmds.add_parser('apps', help='Displays a list of all available applications')

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

    # setup handler instance
    cmd_handler = CommandHandler()

    # setup the log to capture user input stuff
    lgr = setup_logger()
    lgr.info("[[ STARTUP SUCCESFUL ]]")
    # << program loop >>
    while process_user_input(parser, cmd_handler):
        continue


if __name__ == "__main__":
    main()
