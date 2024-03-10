# this file will define the CLI for the user. This is where the avialable commands for the user are stored

import argparse # argument parsing library
# import task_manager

class CommandHandler:


    def dispatch_command(self, command_name, *args):
        cmd = self.commands.get(command_name)

        if cmd:
            cmd['methods'](*args) # dispatch the command to the correct method
        else:
            print(f"Invalid Command: { command_name }")

    def list_threads(self):
        # logic for showing threads to the user
        pass
    def create_thread(self):
        # logic for creating threads
        pass
    def kill_thread(self, thread_id):
        # logic for killing a thread
        pass
    def show_help_menu(self):
        print("\n\t- Commands -\n")

        for name, info, args in self.commands.items():
            print(f"\n{name}\t{info}", end="")

            if args:
                print(f"\t | args: { args }\n")

