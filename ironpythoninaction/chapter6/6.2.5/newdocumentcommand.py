from System.Windows.Forms import (
    DialogResult, MessageBox,
    MessageBoxButtons, MessageBoxIcon
)

from model import Document


class NewDocumentCommand(object):
    def __init__(self, tabController):
        self.tabController = tabController
        
    def execute(self):
        result = MessageBox.Show("Are you sure?",
                                 "New Document",
                                 MessageBoxButtons.OKCancel,
                                 MessageBoxIcon.Question)
        if result == DialogResult.OK:
            self.tabController.document = Document()
        