if __name__ == '__main__':
    import clr
    clr.AddReference("System.Windows.Forms")
    clr.AddReference("System.Drawing")

from System.Drawing import Size
from System.Windows.Forms import (
    Button, DialogResult, 
    DockStyle, Panel, Form,  
    FormBorderStyle, Padding, TextBox
)

class RenameTabDialog(Form):
    
    def __init__(self, name, rename):
        Form.__init__(self)

        title = "Name Tab"
        if rename:
            title = "Rename Tab"
        self.Text = title
        self.Size = Size(170, 85)
        self.FormBorderStyle = FormBorderStyle.FixedDialog
        self.ShowInTaskbar = False
        self.Padding = Padding(5)
        
        self.initialiseTextBox(name)
        self.initialiseButtons()
        
        
    def initialiseTextBox(self, name):
        self.textBox = TextBox()
        self.textBox.Text = name
        self.textBox.Width = 160
        self.Dock = DockStyle.Top
        
        self.Controls.Add(self.textBox)
        
        
    def initialiseButtons(self):
        buttonPanel = Panel()
        buttonPanel.Height = 23
        buttonPanel.Dock = DockStyle.Bottom
        buttonPanel.Width = 170
        
        acceptButton = Button()
        acceptButton.Text = "OK"
        acceptButton.DialogResult = DialogResult.OK
        acceptButton.Width = 75
        acceptButton.Dock = DockStyle.Left
        self.AcceptButton = acceptButton
        buttonPanel.Controls.Add(acceptButton)
        
        cancelButton = Button()
        cancelButton.Text = "Cancel"
        cancelButton.DialogResult = DialogResult.Cancel
        cancelButton.Width = 75
        cancelButton.Dock = DockStyle.Right
        self.CancelButton = cancelButton
        buttonPanel.Controls.Add(cancelButton)
        
        self.Controls.Add(buttonPanel)
        
        
def ShowDialog(name, rename):
    dialog = RenameTabDialog(name, rename)
    result = dialog.ShowDialog()
    dialog.Close()
    if result == DialogResult.OK:
        return dialog.textBox.Text
    return None


if __name__ == '__main__':
    print ShowDialog("Something", False)
    print ShowDialog("Something Else", True)
    