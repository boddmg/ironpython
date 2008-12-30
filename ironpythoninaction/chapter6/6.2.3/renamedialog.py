if __name__ == '__main__':
    import clr
    clr.AddReference('RenameTabDialog')
    clr.AddReference('System.Windows.Forms')

from RenameTabDialog import RenameTabDialogBase
from System.Windows.Forms import DialogResult


class RenameTabDialog(RenameTabDialogBase):
    
    def __init__(self, name, rename):
        RenameTabDialogBase.__init__(self)

        title = "Name Tab"
        if rename:
            title = "Rename Tab"
        self.Text = title
        
        self.textBox.Text = name
        
        
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
    