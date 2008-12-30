import clr
clr.AddReference('System.Management')
from System.Management import (
    ConnectionOptions, ManagementScope,
    WqlEventQuery, ManagementEventWatcher
)
from System import TimeSpan
from System.Threading import Thread

options = ConnectionOptions()
options.Username = "administrator"
options.Password = "******"

# For impersonation rather than authentication:
# from System.Management import AuthenticationLevel, ImpersonationLevel
# options.Impersonation = ImpersonationLevel.Impersonate
# options.Authentication = AuthenticationLevel.Default

options.EnablePrivileges = True
scope =  ManagementScope(r"\\FullComputerName\root\cimv2", options)

# Available Physical Memory dropping below 10Mb 
wql = ('TargetInstance ISA "Win32_OperatingSystem" AND '
       'TargetInstance.FreePhysicalMemory < 10000 ')

timeout = TimeSpan(0, 0, 5)
query = WqlEventQuery("__InstanceModificationEvent", timeout, wql)

watcher = ManagementEventWatcher()
watcher.Query = query
watcher.Scope = scope

interesting_properties = (
    'FreePhysicalMemory',
    'FreeSpaceInPagingFiles',
    'FreeVirtualMemory',
    'NumberOfProcesses',
    'NumberOfUsers',
    'OSArchitecture',
    'ServicePackMajorVersion',
    'ServicePackMinorVersion',
    'SizeStoredInPagingFiles',
    'Status',
    'TotalVirtualMemorySize',
    'TotalVisibleMemorySize',
    'LocalDateTime'
)

def arrived(sender, event):
    print 'Event arrived'
    real_event = event.NewEvent
    instance = real_event['TargetInstance']
    
    for prop in interesting_properties:
        entry = instance.Properties[prop]
        print entry.Name, entry.Value

        
watcher.EventArrived += arrived
watcher.Start()

print 'started'
while True:
    Thread.CurrentThread.Join(1000)
