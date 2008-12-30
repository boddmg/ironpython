import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

from System.IO import File
from System.Windows.Markup import XamlReader

from System.Windows import (
   Application, Window
)

from System.Windows.Controls import Label


class HelloWorld(object):
   def __init__(self):
      stream = File.OpenRead("HelloWorld.xaml")
      self.Root = XamlReader.Load(stream)
      self.button = self.Root.FindName('button')
      self.stackPanel = self.Root.FindName('stackPanel')
      self.button.Click += self.onClick
      
   def onClick(self, sender, event):
      message = Label()
      message.FontSize = 36
      message.Content = 'Welcome to IronPython!'
      self.stackPanel.Children.Add(message)
      
      
hello = HelloWorld()

app = Application()
app.Run(hello.Root)
