# Functions to invoke functions on the UI threads
# or create callbacks that will be invoked on the UI thread.
# SetDispatcher must be called with a UI element before
# the other functions are used.

dispatcher = None

def SetDispatcher(ui_element):
    global dispatcher
    dispatcher = ui_element.Dispatcher
    

def Dispatch(function, *args):
    dispatcher.BeginInvoke(lambda *_: function(*args))
    
    
def GetDispatchFunction(function):
    return lambda *args: Dispatch(function, *args)
