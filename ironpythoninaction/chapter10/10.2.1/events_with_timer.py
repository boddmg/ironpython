import clr
clr.AddReference('System.Management')
from System.Management import (
    ManagementClass, WqlEventQuery, 
    ManagementEventWatcher
)
    
from System import TimeSpan
from System.Threading import Thread

TimerClass = ManagementClass("__IntervalTimerInstruction")
timer = TimerClass.CreateInstance()
timer["TimerId"] = "Timer1"
timer["IntervalBetweenEvents"] = 1000
timer.Put()

query = WqlEventQuery("__TimerEvent", "TimerId=\"Timer1\"")
watcher = ManagementEventWatcher()
watcher.Query = query
watcher.Options.Timeout = TimeSpan(0, 0, 5)

def arrived(sender, event):
    print 'Event arrived'
    real_event = event.NewEvent
    # No TargetInstance for this timer event
    for entry in real_event.Properties:
        print entry.Name, entry.Value

        
watcher.EventArrived += arrived
watcher.Start()

print 'started'
while True:
    Thread.CurrentThread.Join(1000)
