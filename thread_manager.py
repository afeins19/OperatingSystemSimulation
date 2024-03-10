# manager for individual threads in the OS
import multiprocessing
import threading
class ThreadManager:
    def __init__(self):
        self.active_threads = {}

    def start_thread(self, target, *args):
        # starting a thread
        thread = threading.Thread(target=target, args=args)
        thread.start()
        self.active_threads[thread.ident] = thread # saving thread by its TID

    def get_thread(self, tid):
        return self.active_threads[tid]

    def get_active_thread_stats(self):
        thread_info = []

        for thread in self.active_threads:
            thread: threading.Thread
            t_stat = {'TID' : thread.ident,
                      'is alive?' : thread.isAlive()
                      }
            thread_info.append(t_stat)

        return threading
    def kill_thread(self, tid):
        if tid in self.active_threads.keys():
            # stop the thread logic
            pass
        else:
            print(f"\t** Thread with [TID={ tid }] not found")


