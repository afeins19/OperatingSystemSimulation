# this file will hold the user programs that the os will execute
import time
import logging as lg
from log_config import setup_logger
from multiprocessing import Queue, Value, Array, Process
from threading import Thread

from process_manager import ProcessManager

lgr = setup_logger(__name__)
class AppManager:
    def __init__(self):

        self.name_table = {
            'test_process' : AppManager.test_process,
            'test_thread' : AppManager.test_thread_kill, # args = stop_event that we have to pass in
            'count' : AppManager.process_file
        } # maps names to the actual functions for users


    def get_app(self, app_name):
        if app_name in self.name_table.keys():
            return self.name_table[app_name]
        else:
            return None

    # -- processes go here (MUST BE STATIC) --
    @staticmethod
    def test_process(process_control):
        while True:
            # check the pause
            if process_control.pause_event.is_set():
                print(f">>>MSG FROM PROCESS : Process paused.")
                # wait for resume
                process_control.resume_event.wait()
                # Clear pause
                process_control.pause_event.clear()
                print(f">>>MSG FROM PROCESS : Process resumed.")
            # Check stop
            if process_control.stop_event.is_set():
                print(f">>>MSG FROM PROCESS : Process stopped.")
                return

            time.sleep(1)

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


    # -- STRING HANDLING FUNCTIONS --

    @staticmethod
    def process_file(process_control):
        num_ps = 4
        file_name = "shrek.txt"

        # read the entire file and split into lines
        with open(file_name, 'r') as file:
            text_lines = file.readlines()

        # shared queue to hold the count
        char_queue = Queue()

        # partition the text and count the chars using workers
        partioned_text = AppManager.divide_file(process_control, text_lines, num_ps)

        # start worker processes
        pm = ProcessManager()

        processes = []
        for i, text_chunk in enumerate(partioned_text):
            process_name = f'worker_{i}'
            args = (char_queue, text_chunk)
            pm.start_process(process_name, AppManager.count_chars, *args)
            processes.append(process_name)

        print(f"Running Processes: {processes}")

        chars=char_queue.get()
        lgr.info(chars)

    @staticmethod
    def divide_file(process_control, text_lines, num_ps):
        chunk_len = len(text_lines) // num_ps
        partioned_text = []

        # divide the work among multiple processes
        for i in range(num_ps):
            start = i * chunk_len
            end = start + chunk_len if i < num_ps - 1 else len(text_lines)
            partioned_text.append(text_lines[start:end])

        return partioned_text

    @staticmethod
    def count_chars(process_control, char_queue, text_chunk):
        # count the occurrences of each character in a text chunk
        char_counts = {}
        for line in text_chunk:
            for char in line:
                char_counts[char] = char_counts.get(char, 0) + 1

        # put the character counts into the shared queue
        char_queue.put(char_counts)





