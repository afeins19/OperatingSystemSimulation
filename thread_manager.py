# manager for individual threads in the OS
import multiprocessing
import threading
from log_config import setup_logger

lgr = setup_logger(__name__) # logging for threads
class ThreadManager:
    def __init__(self):
        self.active_threads = {}

    def start_thread(self, target, *args):
        # starting a thread
        thread = threading.Thread(target=target, args=args)
        stop_event = threading.Event()
        self.active_threads[thread.ident] = (thread, stop_event) # saving thread by its TID
        thread.start()

        lgr.info(f"Thread with [TID={thread.ident}] has started")
        print((f"Thread with [TID={thread.ident}] has started"))
        return thread.ident

    def get_thread(self, tid):
        return self.active_threads[tid]

    def get_active_thread_stats(self):
        thread_info = []

        for thread_body, stop_event in self.active_threads.values():
            thread_actual: threading.Thread =  thread_actual
            thread_tid = thread_actual.ident
            thread_status = thread_actual.is_alive()
            stop_event: threading.Event = stop_event

            t_stat = {'TID' : thread_tid,
                      'is_alive' : thread_status,
                      'stop_event_set' : stop_event.isSet()
                      }

            thread_info.append(t_stat)

        return threading

    def kill_thread(self, tid, force=False):
        tid = int(tid)
        print(tid)
        if tid in self.active_threads.keys():
            # get the thread
            print(tid)
            thread_actual, stop_event = self.active_threads[tid][0]
            stop_event.set() # stop the thread


            #if not force:
                #thread_actual.join()


            del self.active_threads[tid] # remove the thread after a stopping

            lgr.info(f"Thread { tid } has been stopped")

        else:
            lgr.info(f"** Thread with [TID={ tid }] not found **")


