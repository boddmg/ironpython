from System.Windows import Application
from System.Windows.Controls import Canvas, TextBlock
from System.Threading import Thread, ThreadStart

root = Canvas()
Application.Current.RootVisual = root

text = TextBlock()
thread_id = Thread.CurrentThread.ManagedThreadId
text.Text = "Created on thread %s" % thread_id
text.FontSize = 24
root.Children.Add(text)

def wait():
    Thread.Sleep(3000)
    thread_id = Thread.CurrentThread.ManagedThreadId
    def SetText():
        text.Text = 'Hello from thread %s' % thread_id
    text.Dispatcher.BeginInvoke(SetText)
    
t = Thread(ThreadStart(wait))
t.Start()
