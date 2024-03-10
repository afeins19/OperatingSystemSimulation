# testing the process manager class
import time
import unittest
import sys
sys.path.append(r'C:\Users\aaron\Projects\classWork\CMPSC472\OperatingSystemSimulation')
import multiprocessing

from process_manager import ProcessManager

def sample_process():
    time.sleep(2)


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
        return self.assertEquals(self.pm.get_process(-1), None)



if __name__ == '__main__':
    unittest.main()