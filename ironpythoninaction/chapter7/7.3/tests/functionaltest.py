from tests.testcase import TestCase

from main.mainform import MainForm

from System.IO import Directory, Path
from System.Windows.Forms import Application
from System.Threading import (
    ApartmentState, ManualResetEvent,
    Thread, ThreadStart, Timeout
)

try:
    from IronPython.Runtime.Calls import CallTarget0
except ImportError:
    import clr
    clr.AddReference('IronPython')
    try:
        from IronPython.Compiler import CallTarget0
    except ImportError:
        # IronPython 2.0a5 (FePy on Mono)
        clr.AddReference('Microsoft.Scripting')
        from Microsoft.Scripting import CallTarget0
    
    
class AsyncExecutor(object):

    def __init__(self, function):
        self.result = None
        startEvent = ManualResetEvent(False)
        
        def StartFunction():        
            startEvent.Set()
            self.result = function()
            
        self._thread = Thread(ThreadStart(StartFunction))
        self._thread.Start()
        startEvent.WaitOne()


    def join(self, timeout=Timeout.Infinite):
        return self._thread.Join(timeout)


class TimeoutError(Exception):
    pass
    

class FunctionalTest(TestCase):

    def setUp(self):
        self.mainForm = None
        self._thread = Thread(ThreadStart(self.startMultiDoc))
        self._thread.SetApartmentState(ApartmentState.STA)
        self._thread.Start()
        while self.mainForm is None:
            Thread.CurrentThread.Join(100)
    
    
    def startMultiDoc(self):
        fileDirectory = Path.GetDirectoryName(__file__)
        executableDirectory = Directory.GetParent(fileDirectory).FullName
        
        self.mainForm = MainForm(executableDirectory)
        Application.Run(self.mainForm)
        
    
    def tearDown(self):
        self.invokeOnGUIThread(lambda: self.mainForm.Close())
        
        
    def invokeOnGUIThread(self, function):
        return self.mainForm.Invoke(CallTarget0(function))


    def executeAsynchronously(self, function):
        def AsyncFunction():
            return self.invokeOnGUIThread(function)
        executor = AsyncExecutor(AsyncFunction)
        return executor
            