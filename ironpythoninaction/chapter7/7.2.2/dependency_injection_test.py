import unittest

import time

from dependency_injection import Scheduler

class FakeTime(object):
    calls = []
    
    def time(self):
        self.calls.append('time')
        return 100
    
    def sleep(self, howLong):
        self.calls.append(('sleep', howLong))


class DependencyInjectionTest(unittest.TestCase):
    
    def testConstructor(self):
        scheduler = Scheduler()
        self.assertEquals(scheduler.time, time.time, "time not initialised correctly")
        self.assertEquals(scheduler.sleep, time.sleep, "sleep not initialised correctly")


    def testSchedule(self):
        faketime = FakeTime()
        scheduler = Scheduler(faketime.time, faketime.sleep)
        
        expectedResult = object()
        def function():
            faketime.calls.append('function')
            return expectedResult
            
        actualResult = scheduler.schedule(300, function)
        
        self.assertEquals(actualResult, expectedResult, 
                          "schedule did not return result of calling function")
        
        self.assertEquals(faketime.calls,
                          ['time', ('sleep', 200), 'function'],
                          "time module and functions called incorrectly")
            
        
if __name__ == '__main__':
    unittest.main()