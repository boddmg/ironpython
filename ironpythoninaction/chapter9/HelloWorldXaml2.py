import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")

from System.IO import File
from System.Windows.Markup import XamlReader

from System.Windows import Application

# XAML created from Expression blend
class HelloWorld2(object):
   def __init__(self):
      stream = File.OpenRead("HelloWorld2.xaml")
      self.Root = XamlReader.Load(stream)
      
      
hello = HelloWorld2()

app = Application()
app.Run(hello.Root)
