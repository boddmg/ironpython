# Copyright (c) 2007-8 Michael Foord.
# All Rights Reserved
#

from System.Windows.Controls import UserControl
from System.Windows.Media import Color, Colors, SolidColorBrush

from System.Windows.Markup import XamlReader

xaml = """\
<Canvas xmlns="http://schemas.microsoft.com/client/2007" 
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" 
    Width="450"
    Height="40"
    Background="DarkBlue"
    >
    <TextBlock x:Name="buttonTextBlock" Cursor="Hand" Foreground="White" FontWeight="ExtraBold" FontSize="28"  Canvas.Left="10"></TextBlock>
</Canvas>"""


class EventHook(object):
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        self.handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.handlers.remove(handler)
        return self

    def __call__(self, *args, **keywargs):
        for handler in self.handlers:
            handler(*args, **keywargs)


class Button(UserControl):

    def __init__(self, Text='Click Me'):
        self.Content = root = XamlReader.Load(xaml)
        self.buttonTextBlock = root.FindName("buttonTextBlock")
        
        self.buttonTextBlock.MouseEnter += self.onMouseEnter
        self.buttonTextBlock.MouseLeave += self.onMouseLeave
        self.buttonTextBlock.MouseLeftButtonDown += self.onMouseLeftButtonDown
        self.buttonTextBlock.MouseLeftButtonUp += self.onMouseLeftButtonUp
        root.MouseLeave += self.onRootMouseLeave
        
        self.Text = Text
        self.root = root
        self._mouseOver = False
        self._mouseDown = False
        
        self.Click = EventHook()

        
    def getText(self):
        return self.buttonTextBlock.Text
        
    def setText(self, text):
        self.buttonTextBlock.Text = text
        
    Text = property(getText, setText)
    
    
    def onMouseEnter(self, sender, event):
        self._mouseOver = True
        self.root.Background = SolidColorBrush(Color.FromArgb(255, 255, 215, 0))
        self.buttonTextBlock.Foreground = SolidColorBrush(Color.FromArgb(255, 0, 0, 139))
        
    def onMouseLeave(self, sender, event):
        self._mouseOver = False
        self.root.Background = SolidColorBrush(Color.FromArgb(255, 0, 0, 139))
        self.buttonTextBlock.Foreground = SolidColorBrush(Colors.White)
        
    def onMouseLeftButtonDown(self, sender, event):
        self._mouseDown = True
        
    def onMouseLeftButtonUp(self, sender, event):
        if self._mouseOver and self._mouseDown:
            self.Click()
        self._mouseDown = False
    
    def onRootMouseLeave(self, sender, event):
        if self._mouseOver or self._mouseDown:
            self._mouseOver = False
            self._mouseDown = False
            self.ReleaseMouseCapture()


