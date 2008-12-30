from System import Uri, UriKind
from System.Windows import Application
from System.Windows.Controls import Canvas, MediaElement

canv = Canvas()
xaml = Application.Current.RootVisual = canv

video = MediaElement()
source = Uri('../SomeVideo.wmv', UriKind.Relative)
video.Volume = 1
video.Source = source  
video.Width = 450

canv.Children.Add(video)
