from System import TimeSpan, Uri, UriKind
from System.Windows import Application
from System.Windows.Controls import Canvas, TextBlock, MediaElement
from System.Windows.Media import VideoBrush, Stretch

root = Canvas()
video = MediaElement() 
source = Uri('../SomeVideo.wmv', UriKind.Relative)
video.Source = source
video.Opacity = 0.0
video.IsMuted = True

def restart(s, e):
    video.Position = TimeSpan(0)
    video.Play()

video.MediaEnded += restart

brush = VideoBrush()
brush.Stretch = Stretch.UniformToFill
brush.SetSource(video)

t = TextBlock()
t.Text = 'Video'
t.FontSize = 120
t.Foreground = brush

root.Children.Add(t)
root.Children.Add(video)

Application.Current.RootVisual = root
