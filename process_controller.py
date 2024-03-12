# creates signals for the process to listen to
from multiprocessing import Event

class ProcessControl:
    def __init__(self, pause_event, resume_event, stop_event):
        self.pause_event = pause_event
        self.resume_event = resume_event
        self.stop_event = stop_event
