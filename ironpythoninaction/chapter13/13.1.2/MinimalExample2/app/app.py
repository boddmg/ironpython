from System.Windows import Application
from System.Windows.Controls import Canvas

canv = Canvas()
xaml = Application.Current.LoadRootVisual(canv, "app.xaml")
xaml.textblock.Text = 'Hello World from IronPython'
