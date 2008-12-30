from System.Windows import Application, Thickness
from System.Windows.Controls import (
	Button, Orientation, TextBlock,
	StackPanel, TextBox
)
from System.Windows.Input import Key

root = StackPanel()	
textblock = TextBlock()
textblock.Margin = Thickness(20)
textblock.FontSize = 18
textblock.Text = 'Stuff goes here'
root.Children.Add(textblock)

panel = StackPanel()
panel.Margin = Thickness(20)
panel.Orientation = Orientation.Horizontal

button = Button()
button.Content = 'Push Me'
button.FontSize = 18
button.Margin = Thickness(10)

textbox = TextBox()
textbox.Text = "Type stuff here..."
textbox.FontSize = 18
textbox.Margin = Thickness(10)
textbox.Width = 200
#textbox.Watermark = 'Type Something Here'

def onClick(s, e):
    textblock.Text = textbox.Text
    textbox.Text = ""
	
def onKeyDown(sender, e):
    if e.Key == Key.Enter:
        e.Handled = True
        onClick(None, None)
	
button.Click += onClick
textbox.KeyDown += onKeyDown

panel.Children.Add(button)
panel.Children.Add(textbox)

root.Children.Add(panel)
Application.Current.RootVisual = root
