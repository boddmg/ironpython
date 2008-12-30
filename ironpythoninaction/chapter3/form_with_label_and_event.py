import clr
clr.AddReference('System.Windows.Forms') 
clr.AddReference('System.Drawing')
from System.Windows.Forms import (
    Application, Form,
    FormBorderStyle, Label
)
from System.Drawing import (
    Color, Font, FontStyle, Point
)
from System import Random

random = Random()

form = Form()
form.Text = "Hello World"
form.FormBorderStyle = FormBorderStyle.Fixed3D
form.Height = 150

newFont = Font("Verdana", 16, 
    FontStyle.Bold | FontStyle.Italic)

label = Label()
label.AutoSize = True
label.Text = "My Hello World Label"
label.Font = newFont
label.BackColor = Color.Aquamarine
label.ForeColor = Color.DarkMagenta
label.Location = Point(10, 50)

form.Controls.Add(label)

def GetNewColor():
    red = random.Next(255)
    blue = random.Next(255)
    green = random.Next(255)
    return Color.FromArgb(red, blue, green)

def ChangeColor(sender, event):
    print ' X:', event.X, 'Y:', event.Y
    sender.BackColor = GetNewColor()
    sender.ForeColor = GetNewColor()

label.MouseMove += ChangeColor

Application.Run(form)
