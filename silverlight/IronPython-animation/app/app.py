from System import TimeSpan
from System.Windows import Application, Duration, PropertyPath
from System.Windows.Controls import Canvas, TextBlock
from System.Windows.Media.Animation import (
    DoubleAnimation, Storyboard
)

root = Canvas()

Application.Current.RootVisual = root

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
