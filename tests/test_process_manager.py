# testing the process manager class
import time
import unittest
import sys
sys.path.append(r'/Users/aaronfeinberg/Projects/classWork/CMPSC472/OperatingSystemSimulation')
import multiprocessing
from multiprocessing import Array, Process, Value

from process_manager import ProcessManager

def sample_process():
    time.sleep(2)

def increment_shared_value(shared_value: multiprocessing.Value):
    if shared_value:
        with shared_value.get_lock():
            shared_value.value += 1

class TestProcessManager(unittest.TestCase):

    def setUp(self):
        self.pm = ProcessManager()
        self.p_name = "TEST_PROCESS"
        self.invalid_pid = -123

    def test_start_stop_process(self):
        # start the process
        self.pm.start_process(name=self.p_name, function=sample_process)

        # let it actually startup
        time.sleep(0.5)

        # check if its in the actives
        self.assertIn("TEST_PROCESS", [name for name, _ in self.pm.active_processes.values()])

        # cleanup
        pid = next(iter(self.pm.active_processes))
        self.pm.kill_process(pid)

    def test_parallel_start_and_stop(self):

        for i in range(10):
            pid = self.pm.start_process(name=self.p_name + str(i), function=sample_process)
            self.assertEqual(pid, self.pm.active_processes[pid][1].pid)

    def test_inactive_process_lookup(self):
        return self.assertEqual(self.pm.get_process(-1), None)

    def test_shared_value_creation(self):
        shared_val = self.pm.create_shared_value('i', 0)
        self.assertEqual(shared_val.value, 0)

    def test_increment_shared_value(self):
        # testing incrementing the shared value via multiple processes
        shared_val = self.pm.create_shared_value('i', 0)

        # create some processes
        pids = []

        for i in range(5):
            ps = self.pm.start_process(f"test_{i}", increment_shared_value, shared_val)
            time.sleep(.1)
            pids.append(ps)

        for pid in pids:
            print(pid)
            self.pm.active_processes[pid][1].join() # wait until each process finishes before checking value

        self.assertEqual(shared_val.value, 5)

if __name__ == '__main__':
    unittest.main()