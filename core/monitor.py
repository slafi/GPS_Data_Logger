from helpers import worker


from datetime import datetime
import os, random, time

class OBD_Monitor(worker.Worker):

    def __init__(self, event, q, interval=5):
        super(OBD_Monitor, self).__init__(event, q, interval)

    def task(self, *args, **kwargs):
        #print("Worker task is a placeholder!")
        print(f'{datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")} => ID: {self.ident} (Overridden task)')
        self.q.put(random.random())