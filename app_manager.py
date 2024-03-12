# this file will hold the user programs that the os will execute
import time
import logging as lg
from log_config import setup_logger

lgr = setup_logger(__name__)
class AppManager:
    def __init__(self):

        self.name_table = {
            'test_process' : AppManager.test_process,
            'test_thread' : AppManager.test_thread_kill # args = stop_event that we have to pass in
        } # maps names to the actual functions for users

    def get_app(self, app_name):
        if app_name in self.name_table.keys():
            return self.name_table[app_name]
        else:
            return None

    # -- processes go here (MUST BE STATIC) --
    @staticmethod
    def test_process(process_control, process_name):
        while True:
            # check the pause
            if process_control.pause_event.is_set():
                print(f">>>MSG FROM PROCESS `{ process_name }`: Process paused.")
                # wait for resume
                process_control.resume_event.wait()
                # Clear pause
                process_control.pause_event.clear()
                print(f">>>MSG FROM PROCESS `{ process_name }`: Process resumed.")
            # Check stop
            if process_control.stop_event.is_set():
                print(f">>>MSG FROM PROCESS `{ process_name }`: Process stopped.")
                return

            time.sleep(1)

    @staticmethod
    def spt(process_control):
        while not process_control.stop_event.is_set():
            if process_control.pause_event.is_set():
                print("Process paused.")
                process_control.resume_event.wait()  # Wait for the resume signal
                process_control.pause_event.clear()  # Clear pause_event after resuming
                print("Process resumed.")

            # Perform the main task here
            print("Running main task...")
            time.sleep(1)  # Sleep for a while to simulate work

    @staticmethod
    def test_thread_kill(stop_event, resume_event, suspend_event):
        while not stop_event.is_set():
            if suspend_event.is_set():
                # thread paused, wait for resume event
                lgr.info("[[ Thread paused ]]")
                resume_event.wait()  # waiting until resume event is set
                lgr.info("[[ Thread resumed ]]")

            # work
            lgr.info("[[ Thread Running... ]]")
            time.sleep(3)







