import clr
from System.Threading import Thread, ThreadStart

try:
    # IronPython 1.x
    from IronPython.Runtime.Calls import CallTarget0
except ImportError: 
    # IronPython 2.0b4
    clr.AddReference('IronPython')
    try:
        from IronPython.Compiler import CallTarget0
    except ImportError:
        # IronPython 2.0a5 (FePy on Mono)
        clr.AddReference('Microsoft.Scripting')
        from Microsoft.Scripting import CallTarget0

        
def DoBackgroundWithInvoke(function, callback, form):
    def op():
        function()
        form.Invoke(CallTarget0(callback))
    t = Thread(ThreadStart(op))
    t.Start()
