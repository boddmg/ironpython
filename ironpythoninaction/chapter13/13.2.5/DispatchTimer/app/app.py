from System.Windows import Application
from System.Windows.Controls import Canvas, TextBlock
from System.Windows.Threading import DispatcherTimer
from System import TimeSpan


root = Canvas()
Application.Current.RootVisual = root

text = TextBlock()
text.Text = "Nothing yet"
text.FontSize = 24
root.Children.Add(text)

counter = 0
def callback(sender, event):
    global counter
    counter += 1
    text.Text = 'Tick %s' % counter
    
timer = DispatcherTimer()
timer.Tick += callback
timer.Interval = TimeSpan.FromSeconds(2)
timer.Start()
