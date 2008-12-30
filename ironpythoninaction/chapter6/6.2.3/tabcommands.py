from System.Windows.Forms import (
    DialogResult, MessageBox, 
    MessageBoxButtons, MessageBoxIcon
)

from renamedialog import ShowDialog

class RemoveCommand(object):
    
    def __init__(self, tabController):
        self.tabController = tabController
        
    
    def execute(self):
        if not self.tabController.hasPages:
            return
        result = MessageBox.Show("Are you sure?",
                                 "Delete Page",
                                 MessageBoxButtons.OKCancel,
                                 MessageBoxIcon.Question)
        if result == DialogResult.OK:
            self.tabController.deletePage()


class RenameCommand(object):
    
    def __init__(self, tabController):
        self.tabController = tabController
        
        
    def execute(self):
        if not self.tabController.hasPages:
            return
        currentTitle = self.tabController.currentPageTitle
        
        newTitle = ShowDialog(currentTitle, True)
        if newTitle is not None:
            self.tabController.currentPageTitle = newTitle
            
