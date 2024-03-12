# testing the process manager class
import time
import unittest
import sys
sys.path.append(r'/Users/aaronfeinberg/Projects/classWork/CMPSC472/OperatingSystemSimulation')

from multiprocessing import Array, Process, Value

from process_manager import ProcessManager


def sample_process():
    time.sleep(2)

def increment_shared_value(process_control, name, shared_value):
    if shared_value:
        with shared_value.get_lock():
            shared_value.value += 1
            print(shared_value.value)


class TestProcessManager(unittest.TestCase):

    def setUp(self):
        self.pm = ProcessManager()
        self.p_name = "test_process"
        self.invalid_pid = -123

    def test_start_stop_process(self):
        # Start the process
        self.pm.start_process(name=self.p_name, target_function=sample_process)

        # Let it actually startup
        time.sleep(0.5)

        # Check if it's in the actives
        active_names = [data['name'] for pid, data in self.pm.active_processes.items()]
        self.assertIn(self.p_name, active_names)

        # Cleanup
        pid = next(iter(self.pm.active_processes))
        self.pm.kill_process(pid)

    def test_parallel_start_and_stop(self):

        for i in range(10):
            pid = self.pm.start_process(name=self.p_name + str(i), target_function=sample_process)
            self.assertEqual(pid, self.pm.active_processes[pid]['process'].pid)

    def test_inactive_process_lookup(self):
        return self.assertEqual(self.pm.get_process(-1), None)

    def test_shared_value_creation(self):
        shared_val = self.pm.create_shared_value('i', 0)
        self.assertEqual(shared_val.value, 0)

    def test_increment_shared_value(self):
        # Create shared value using ProcessManager's method
        shared_val: Value = self.pm.create_shared_value('i', 0)

        # Create some processes to increment the shared value
        for i in range(5):
            self.pm.start_process(f"test_{i}", increment_shared_value, shared_val)

        # Wait for all processes to complete
        for pid, data in self.pm.active_processes.items():
            data['process'].join()

        # Assert that the shared value has been incremented correctly
        self.assertEqual(shared_val.value, 5)


if __name__ == '__main__':
    unittest.main()