from System.Windows import Application, Thickness, CornerRadius
from System.Windows.Controls import Border
from System.Windows.Media import Colors, SolidColorBrush

from dispatcher import Dispatch, SetDispatcher
from main import MainPanel

import sys
from System.Windows.Browser import HtmlPage


class Writer(object):
    def __init__(self):
        self.stdout = ''
        
    def write(self, text):
        Dispatch(self.do_write, text)
        
    def do_write(self, text):
        self.stdout += text
        HtmlPage.Document.debugging.value = self.stdout


output_writer = Writer()
sys.stdout = output_writer

border = Border()
border.BorderThickness = Thickness(5)
border.CornerRadius = CornerRadius(10)
border.BorderBrush = SolidColorBrush(Colors.Blue)
border.Background = SolidColorBrush(Colors.Yellow)
border.Padding = Thickness(5)

border.Child = MainPanel()


Application.Current.RootVisual = border

SetDispatcher(border)
print 'App started'
