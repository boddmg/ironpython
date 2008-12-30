import clr
clr.AddReference('System.Management.Automation')
from System.Management.Automation import PSMethod, RunspaceInvoke

runspace = RunspaceInvoke()
psobjects = runspace.Invoke("Get-WmiObject Win32_VideoController")
video = psobjects[0]

print
print 'Video controller properties'
for prop in video.Properties:
    print prop.Name, prop.Value

psobjects = runspace.Invoke("Get-WmiObject Win32_Processor")
cpu = psobjects[0]

print
print 'CPU properties'
for prop in cpu.Properties:
    print prop.Name, prop.Value

psobjects = runspace.Invoke('Get-WmiObject Win32_Process -filter \'Name = "ipy.exe"\'')
ipy = psobjects[0]

print
print 'WMI process methods'
for member in ipy.Members:
    if not isinstance(member, PSMethod):
        continue
    print member
