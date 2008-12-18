# Copyright (c) 2007-8 Michael Foord.
# All Rights Reserved
#

browserDOM = """\
from System.Windows.Browser import HtmlPage

def SetExperimental(html):
    HtmlPage.Document.experimental.innerHTML = html

def ChangeBorder():
    experimental = HtmlPage.Document.GetElementById('experimental')
    experimental.SetStyleAttribute('border', 'solid black 2px')
    
html = '<strong>Set from IronPython</strong>'

print 'Setting innerHTML'
SetExperimental(html)

print 'Changing Border'
ChangeBorder()

print 'Done'

# Call a javascript function "writesomestuff"
HtmlPage.Window.CreateInstance("writesomestuff", 'One last thing...\\n')
"""


inputEvents = """\
from System import EventHandler
from System.Windows.Browser.HtmlPage import Document
from System.Windows.Controls import TextBlock

root.Children.Clear()
t = TextBlock()
t.FontSize = 24
t.Text = 'Nothing yet...'
root.Children.Add(t)

def OnClick(sender, event):
    text = Document.input_field.value
    if text.isdigit():
        t.FontSize = int(text)
    else:
        t.Text = text

handler = EventHandler(OnClick)
Document.OkButton.AttachEvent("onclick", handler)
"""


videoExample = """\
from System.Windows.Controls import MediaElement
from System import TimeSpan, Uri, UriKind

m = MediaElement()
root.Children.Clear()
root.Children.Add(m)

def OnClick(s, e):
    global playing
    if not playing:
        print 'Playing.'
        m.Play()
    else:
        position = m.Position.TotalSeconds
        print 'Pausing. At position: %s Seconds' % position
        m.Pause()

    playing = not playing

def OnMediaEnded(s, e):
    # Make the video player loop
    m.Position = TimeSpan(0)
    m.Play()

u = Uri('SomeVideo.wmv', UriKind.Relative)
t = TimeSpan(0)
m.Volume = 1
m.Source = u
m.Position = t
m.Width = 450
m.Height = 340

m.MouseLeftButtonUp += OnClick
m.MediaEnded += OnMediaEnded
playing = True
"""


openFileDialog = """\
from System.Windows.Controls import (
    OpenFileDialog
)

dialog = OpenFileDialog()
dialog.Filter = "Python files (*.py)|*.py|All files (*.*)|*.*"
dialog.Multiselect = True

if dialog.ShowDialog() == True:
    data = dialog.File.OpenText().ReadToEnd()
    print data
    
else:
    print 'The user cancelled'
"""


isolatedStorageFile = """\
from System.IO.IsolatedStorage import (
    IsolatedStorageFile, IsolatedStorageFileStream
)

from System.IO import (
    FileMode, StreamReader, StreamWriter
)

def ListFiles():
    store = IsolatedStorageFile.GetUserStoreForApplication()
    files = store.GetFileNames('.')
    if not files.Length:
        print 'No Files.'
    else:
        print 'Files:\\n' + '\\n    '.join(files) + '\\n'

def DeleteFile(name):
    store = IsolatedStorageFile.GetUserStoreForApplication()
    store.DeleteFile(name)

def SaveFile(name, data):
    store = IsolatedStorageFile.GetUserStoreForApplication()
    isolatedStream = IsolatedStorageFileStream(name, FileMode.OpenOrCreate, store)

    writer = StreamWriter(isolatedStream)
    writer.Write(data)

    writer.Close()
    isolatedStream.Close()

def LoadFile(name):
    store = IsolatedStorageFile.GetUserStoreForApplication()
    isolatedStream = IsolatedStorageFileStream(name, FileMode.Open, store)

    reader = StreamReader(isolatedStream)
    data = reader.ReadToEnd()

    reader.Close()
    isolatedStream.Close()

    return data

data = 'a long string of text'

store = IsolatedStorageFile.GetUserStoreForApplication()
print 'Free space:', store.AvailableFreeSpace
print 'Quota:', store.Quota
print

ListFiles()
print 'Saving file.'
SaveFile('test.txt', data)
ListFiles()
print 'Free space:', store.AvailableFreeSpace

print 'Loading "test.txt".'
print LoadFile('test.txt')

print 'Deleting File.'
DeleteFile('test.txt')

ListFiles()
"""


loadingXaml = '''\
from System.Windows.Media import SolidColorBrush, Colors
from System.Windows.Markup import XamlReader


# This XAML is copied and pasted from Expression Blend!
xaml = """\
<Canvas
    xmlns="http://schemas.microsoft.com/client/2007"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Width="400" Height="400"
    Background="White"
    x:Name="Page"
    >
    <Canvas.Triggers>
        <EventTrigger>
            <BeginStoryboard>               
                <Storyboard x:Name="Example">
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="image" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[3].(TranslateTransform.X)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="-124.018"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="-93"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="image" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[3].(TranslateTransform.Y)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="-21.536"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="-58"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="image" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[0].(ScaleTransform.ScaleX)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="3.444"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="1"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="image" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[0].(ScaleTransform.ScaleY)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="3.444"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="1"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="image" Storyboard.TargetProperty="(UIElement.RenderTransform).(TransformGroup.Children)[2].(RotateTransform.Angle)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="-179.915"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="0"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="Page" Storyboard.TargetProperty="(FrameworkElement.Width)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="375"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="482"/>
                    </DoubleAnimationUsingKeyFrames>
                    <DoubleAnimationUsingKeyFrames BeginTime="00:00:00" Storyboard.TargetName="Page" Storyboard.TargetProperty="(FrameworkElement.Height)">
                        <SplineDoubleKeyFrame KeyTime="00:00:00" Value="414"/>
                        <SplineDoubleKeyFrame KeyTime="00:00:2" Value="364"/>
                    </DoubleAnimationUsingKeyFrames>
                </Storyboard>
            </BeginStoryboard>
        </EventTrigger>
    </Canvas.Triggers>
    <Path Width="1" Height="1" Fill="#FFFFFFFF" Stretch="Fill" Stroke="#FF000000" Canvas.Left="534.5" Canvas.Top="297.5" Data="M535,298"/>
    <Path Width="1" Height="1" Fill="#FFFFFFFF" Stretch="Fill" Stroke="#FF000000" Canvas.Left="356.5" Canvas.Top="104.5" Data="M357,105"/>
    <Image RenderTransformOrigin="0.5,0.5" x:Name="image" Width="70.4" Height="70.4" Canvas.Left="270" Canvas.Top="179" Source="simpsons.jpg" Stretch="Fill">
        <Image.RenderTransform>
            <TransformGroup>
                <ScaleTransform ScaleX="1" ScaleY="1"/>
                <SkewTransform AngleX="0" AngleY="0"/>
                <RotateTransform Angle="0"/>
                <TranslateTransform X="0" Y="0"/>
            </TransformGroup>
        </Image.RenderTransform>
    </Image>
</Canvas>
"""

canvas = XamlReader.Load(xaml)
storyboard = canvas.FindName('Example')
storyboard.AutoReverse = True

def OnClick(sender, event):
    storyboard.Begin()
    
canvas.MouseLeftButtonDown += OnClick

root.Background = SolidColorBrush(Colors.White)
root.Children.Clear()
root.Children.Add(canvas)
'''


controls = '''\
from System.Windows import Thickness
from System.Windows.Controls import (
    Button, Orientation, StackPanel, 
    TextBlock, TextBox
)

from System.Windows.Input import Key

root.Children.Clear()

firstPanel = StackPanel()
textblock = TextBlock()
textblock.FontSize = 24
textblock.Text = 'Stuff goes here...'
textblock.Margin = Thickness(10)
firstPanel.Children.Add(textblock)

panel = StackPanel()
panel.Orientation = Orientation.Horizontal

button = Button()
button.Content = 'Push Me'
button.FontSize = 18
button.Margin = Thickness(10)

textbox = TextBox()
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
firstPanel.Children.Add(panel)

root.Children.Add(firstPanel)
'''


webClient = """\
from System import Uri, UriKind 
from System.IO import StreamReader
from System.Net import WebClient

#help(WebClient)

uri = Uri('/', UriKind.Relative)
web = WebClient()

def completed(s, e):
    print 'Completed'
    print 'Error?', e.Error
    print 'Cancelled?', e.Cancelled
    print e.Result

def changed(s, e):
    print 'Bytes Recieved', e.BytesReceived
    print 'Progress Percentage', e.ProgressPercentage

web.DownloadStringCompleted += completed
web.DownloadProgressChanged += changed
web.DownloadStringAsync(uri)

# Next do the same thing with a stream
# instead of a string
def completed2(s, e):
    print '\\nStream Read Completed'
    print e.Result
    reader = StreamReader(e.Result)
    print reader.ReadToEnd()
    
web2 = WebClient()
web2.OpenReadCompleted += completed2
web2.OpenReadAsync(uri)
"""


threading = '''\
from System.Windows.Controls import TextBlock
from System.Threading import Thread, ThreadStart

text = TextBlock()
text.Text = "Nothing yet"
text.FontSize = 24
root.Children.Clear()
root.Children.Add(text)

def wait():
    Thread.Sleep(3000)
    def SetText():
        text.Text = 'Hello from another thread'
    text.Dispatcher.BeginInvoke(SetText)
    
t = Thread(ThreadStart(wait))
t.Start()
'''


openFile = '''\
from System.Windows.Controls import TextBlock

# Read from a file in the 'xap'
handle = file('app.py')
data = handle.read()
handle.close()

t = TextBlock()
t.Text = data

root.Children.Clear()
root.Children.Add(t)
'''


position = """\
from System.Windows import DependencyObject
from System.Windows.Controls import TextBlock, Canvas
from System.Windows.Media import Colors, SolidColorBrush

def OnMouseLeftButtonDown(sender, event):
    position = event.GetPosition(newCanvas)
    t = TextBlock()
    t.Text = "Clicked"
    DependencyObject.SetValue(t, Canvas.TopProperty, position.Y)
    DependencyObject.SetValue(t, Canvas.LeftProperty, position.X)
    newCanvas.Children.Add(t)

newCanvas = Canvas()
newCanvas.Background = SolidColorBrush(Colors.Yellow)
newCanvas.Width = 450
newCanvas.Height = 600
newCanvas.MouseLeftButtonDown += OnMouseLeftButtonDown

t = TextBlock()
t.Text = 'Click the Canvas'
t.FontSize = 30
newCanvas.Children.Add(t)

root.Children.Clear()
root.Children.Add(newCanvas)
"""


animation = """\
from System import TimeSpan
from System.Windows import Application, Duration, PropertyPath
from System.Windows.Controls import Canvas, TextBlock
from System.Windows.Media.Animation import (
    DoubleAnimation, Storyboard
)

root.Children.Clear()
root.Resources.Clear()

t = TextBlock()
t.FontSize = 20
t.Text = 'Move the Mouse Over Me'
root.Children.Add(t)

sb = Storyboard()
duration = Duration(TimeSpan.FromSeconds(0.25))
a = DoubleAnimation()
a.Duration = duration
sb.Duration = duration
sb.AutoReverse = True
sb.Children.Add(a)

Storyboard.SetTarget(a, t)
Storyboard.SetTargetProperty(a, PropertyPath('FontSize'))
a.From = 20
a.To = 30

def anim(s, e):
    print 'Starting'
    sb.Begin()
    
t.MouseEnter += anim 

root.Resources.Add('StoryBoard', sb)
"""
