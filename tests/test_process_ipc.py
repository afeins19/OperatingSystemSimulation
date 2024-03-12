# testing ipc for processes
import unittest
from process_manager import ProcessManager
import time

def ipc_shared_value_test(shared_value):
    for _ in range(1000):  # Simulate many short messages
        with shared_value.get_lock():
            shared_value.value += 1

def ipc_message_queue_test(queue):
    for _ in range(1000):  # Simulate many short messages
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

    def wait_for_process_completion(self, pid):
        process = self.pm.active_processes.get(pid, {}).get('process')
        if process:
            process.join()

    def test_ipc_shared_value_performance(self):
        shared_val = self.pm.create_shared_value('i', 0)
        start_time = time.time()
        self.pm.start_process("IPC_Test_Shared_Memory", ipc_shared_value_test, shared_val)
        # Wait for process to complete and measure time
        # ...

    def test_ipc_message_queue_performance(self):
        message_queue = self.pm.create_shared_queue(1000)
        start_time = time.time()
        self.pm.start_process("IPC_Test_Message_Queue", ipc_message_queue_test, message_queue)
        # Wait for process to complete and measure time
        # ...

    # Additional tests for longer messages
    # ...
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
        long_messages = ["long" * 1000 for _ in range(10)]  # A few long messages

        start_time = time.time()
        p = self.pm.start_process("Producer", self.producer_ps, message_queue, long_messages)
        c = self.pm.start_process("Consumer", self.consumer_ps, message_queue, len(long_messages))
        self.wait_for_process_completion(p)
        self.wait_for_process_completion(c)
        end_time = time.time()
        self.assertEqual(message_queue.empty(), True)
        print(f"Time for long messages: {end_time - start_time}")