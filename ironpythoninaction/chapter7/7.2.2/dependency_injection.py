import time

class Scheduler(object):
    def __init__(self, tm=time.time, sl=time.sleep):
        self.time = tm
        self.sleep = sl
        
    def schedule(self, when, function):
        self.sleep(when - self.time())
        return function()