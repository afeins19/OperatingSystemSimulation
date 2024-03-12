# testing ipc for processes
import unittest
import sys
sys.path.append(r'/Users/aaronfeinberg/Projects/classWork/CMPSC472/OperatingSystemSimulation')
from process_manager import ProcessManager
import time
from multiprocessing import Value, Queue

def ipc_shared_value_test(shared_value):
    for _ in range(1000):  # many short messages
        with shared_value.get_lock():
            shared_value.value += 1

def increment_shared_value(process_control, name, shared_value):
    if shared_value:
        with shared_value.get_lock():
            shared_value.value += 1
            print(shared_value.value)

def decrement_shared_value(process_control, name, shared_value):
    if shared_value:
        with shared_value.get_lock():
            shared_value.value -= 1
            print(shared_value.value)

def ipc_message_queue_test(queue):
    for _ in range(100):  #  many short messages
        queue.put("message")

def producer(queue, messages):
    for m in messages:
        queue.put(m)

def consumer(queue, num_messages):
    for i in range(num_messages):
        queue.get()

class TestProcessManagerIPC(unittest.TestCase):
    def setUp(self):
        self.pm = ProcessManager()
        self.producer_ps = producer
        self.consumer_ps = consumer

        # setting up shared value
        self.shared_value = Value('i', 0)
        self.message_queue = Queue()
    def wait_for_process_completion(self, pid):
        process = self.pm.active_processes.get(pid, {}).get('process')
        if process:
            process.join()

    def test_ipc_shared_value_performance(self):
        shared_val = self.pm.create_shared_value('i', 0)
        start_time = time.time()
        pid = self.pm.start_process("ipc_shared_value_test", ipc_shared_value_test, shared_val)
        if pid:
            process = self.pm.active_processes[pid]['process']
            process.join() # wait for it to join

    def test_ipc_message_queue_performance(self):
        message_queue = self.pm.create_shared_queue(1000)
        start_time = time.time()
        pid = self.pm.start_process("ipc_message_queue_test", ipc_message_queue_test, 1000)
        if pid:
            process = self.pm.active_processes[pid]['process']
            process.join()  # wait for it to join


    def test_message_passing_short_messages(self):
        message_queue = self.pm.create_shared_queue(10000)
        short_messages = ["TEST" for _ in range(1000)]  # Many short messages

        start_time = time.time()
        p = self.pm.start_process("Producer", self.producer_ps, message_queue, short_messages)
        c = self.pm.start_process("Consumer", self.consumer_ps, message_queue, len(short_messages))

        self.wait_for_process_completion(p)
        self.wait_for_process_completion(c)
        end_time = time.time()
        self.assertEqual(message_queue.empty(), True)
        print(f"Time for short messages: {end_time - start_time}")

    def test_message_passing_long_messages(self):
        message_queue = self.pm.create_shared_queue(10)
        msg_str = """"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
        incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
         ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in 
         voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
        long_messages = [msg_str * 100 for _ in range(10)]  # a few long messages

        start_time = time.time()
        p = self.pm.start_process("Producer", self.producer_ps, message_queue, long_messages)
        c = self.pm.start_process("Consumer", self.consumer_ps, message_queue, len(long_messages))
        self.wait_for_process_completion(p)
        self.wait_for_process_completion(c)
        end_time = time.time()
        self.assertEqual(message_queue.empty(), True)
        print(f"Time for long messages: {end_time - start_time}")

    def test_shared_value_message_passing(self):
        increment_process = self.pm.start_process("increment", increment_shared_value, self.shared_value, "increment")
        decrement_process = self.pm.start_process("decrement", decrement_shared_value, self.shared_value, "decrement")

        increment_process.start()
        decrement_process.start()

        increment_process.join()
        decrement_process.join()

        # check if the shared value is 0
        self.assertEqual(self.shared_value.value, 0)

        # check if all messages were received
        messages_received = {"incremented": 0, "decremented": 0}
        while not self.message_queue.empty():
            message = self.message_queue.get()
            messages_received[message] += 1

        self.assertEqual(messages_received["incremented"], 100)
        self.assertEqual(messages_received["decremented"], 100)

if __name__ == '__main__':
    unittest.main()