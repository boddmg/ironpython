from System.Diagnostics import Stopwatch

timer = Stopwatch()
times = {}

def profiler(function):
    def wrapped(*args, **keywargs):
        if not timer.IsRunning:
            timer.Start()
            
        start = timer.ElapsedMilliseconds
        retVal = function(*args, **keywargs)
        timeTaken = timer.ElapsedMilliseconds - start
        
        name = function.__name__
        function_times = times.setdefault(name, [])
        function_times.append(timeTaken)
        return retVal
    return wrapped


from types import FunctionType

class ProfilingMetaclass(type):
    
    def  __new__(meta, classname, baseClasses, classDict):
        for name, item in classDict.items():
            if isinstance(item, FunctionType):
                classDict[name] = profiler(item)
        return type.__new__(meta, classname, baseClasses, classDict)
    
    
from System.Threading import Thread


class Test(object):
    
    __metaclass__ = ProfilingMetaclass

    def __init__(self):
        counter = 0
        while counter < 100:
            counter += 1
            self.method()
        
        
    def method(self):
        Thread.CurrentThread.Join(20)


if __name__ == '__main__':
    t = Test()
    
    for name, calls in times.items():
        print 'Function: %s' % name
        print 'Called: %s times' % len(calls)
        print 'Total time taken: %s seconds' % (sum(calls) / 1000.0)
        avg = (sum(calls) / float(len(calls)))
        print 'Max: %sms, Min: %sms, Avg: %sms\r\n' % (max(calls), min(calls), avg)
