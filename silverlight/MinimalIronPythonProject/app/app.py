from System.Windows import Application
from System.Windows.Controls import Canvas


xaml = Application.Current.LoadRootVisual(Canvas(), "app.xaml")
xaml.textblock.Text = 'Hello IronPython'
