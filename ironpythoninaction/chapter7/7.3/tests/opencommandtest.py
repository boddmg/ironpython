from tests.testcase import TestCase

from System.IO import Path
from System.Windows.Forms import DialogResult

from main.opencommand import OpenCommand


class Mock(object):
    pass


class MockDialog(object):
    def __init__(self):
        self.InitialDirectory = None
        self.FileName = None
        self.returnVal = DialogResult.Cancel
        
    def ShowDialog(self):
        return self.returnVal


class Listener(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.returnVal = None
        self.triggered = False
        self.triggerArgs = None
        self.triggerKeyWargs = None
        
    def __call__(self, *args, **keywargs):
        self.triggered = True
        self.triggerArgs = args
        self.triggerKeyWargs = keywargs
        return self.returnVal
        

class OpenCommandTest(TestCase):
    
    def setUp(self):        
        mainform = Mock()
        document = Mock()
        document.fileName = None
        mainform.document = document
                
        self.command = OpenCommand(mainform)
        self.command.openFileDialog = MockDialog()
        
        
    def testExecuteShouldSetFilenameAndInitialDirectoryOnDialog(self):
        self.command.execute()
        self.assertNone(self.command.openFileDialog.FileName, 
                        "FileName incorrectly set")
        
        self.command.mainForm.document.fileName = __file__        
        self.command.execute()
        self.assertEquals(self.command.openFileDialog.FileName, 
                          __file__, 
                          "FileName incorrectly set")
        self.assertEquals(self.command.openFileDialog.InitialDirectory, 
                          Path.GetDirectoryName(__file__), 
                          "InitialDirectory incorrectly set")


    def testExecuteShouldNotCallGetDocumentForCancelledDialog(self):
        listener = Listener()
        self.command.getDocument = listener
        
        self.command.execute()
        self.assertFalse(listener.triggered, "getDocument called incorrectly")
        
        
    def testExecuteWithAcceptedDialogShouldCallGetDocument(self):
        listener = Listener()
        self.command.getDocument = listener
        
        originalDocument = self.command.mainForm.document
        self.command.mainForm.document.fileName = __file__        
        self.command.openFileDialog.returnVal = DialogResult.OK
        self.command.execute()
        self.assertEquals(listener.triggerArgs, (__file__,), 
                          "getDocument not called with filename")
        self.assertEquals(self.command.openFileDialog.InitialDirectory, 
                          Path.GetDirectoryName(__file__), 
                          "FileName incorrectly set")
        self.assertEquals(self.command.mainForm.document, 
                          originalDocument, 
                          "document incorrectly changed")


    def testNewDocumentFromGetDocumentShouldBeSetOnMainForm(self):
        listener = Listener()
        self.command.getDocument = listener
        self.command.mainForm.document.fileName = __file__        
        self.command.openFileDialog.returnVal = DialogResult.OK
        
        newDocument = object()
        listener.returnVal = newDocument
        self.command.execute()
        self.assertEquals(self.command.mainForm.document, 
                          newDocument, 
                          "document not replaced")
