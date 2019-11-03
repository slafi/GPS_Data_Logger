from threading import Event, Thread
from multiprocessing import Queue
from datetime import datetime

import os, time, random
import logging


# Initialize logger for the module
logger = logging.getLogger(__name__)


class Worker(Thread):
 

    def __init__(self, event, q, interval=5):
        super(Worker, self).__init__()
        self.event = event
        self.q = q
        self.interval = interval
        self.enabled = False

    def run(self):

        while(self.enabled):
            self.event.wait()            
            self.task()
            time.sleep(self.interval)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def task(self, *args, **kwargs):
        print("Worker task is a placeholder. This method is meant to be overridden!")

