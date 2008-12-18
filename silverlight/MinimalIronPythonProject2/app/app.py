from System.Windows import Application
from System.Windows.Controls import Canvas, TextBlock

canvas = Canvas()
textblock = TextBlock()
textblock.FontSize = 24
textblock.Text = 'Hello World from IronPython'
canvas.Children.Add(textblock)

Application.Current.RootVisual = canvas
