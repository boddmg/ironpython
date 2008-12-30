from System.IO import Directory, Path
from System.Windows.Forms import (
    DialogResult, SaveFileDialog,
    MessageBox, MessageBoxButtons, 
    MessageBoxIcon,
)

from documentwriter import DocumentWriter

filter = 'Text files (*.txt)|*.txt|All files (*.*)|*.*'

class SaveCommand(object):
    
    title = "Save Document"
    
    def __init__(self, document, tabController):
        self.document = document
        self.tabController = tabController
        self.saveDialog = SaveFileDialog()
        self.saveDialog.Filter = filter
        self.saveDialog.Title = self.title
    
    
    def execute(self):
        fileName = self.document.fileName
        document = self.getUpdatedDocument()
        
        directory = Path.GetDirectoryName(fileName)
        directoryExists = Directory.Exists(directory)
        if fileName is None or not directoryExists:
            self.promptAndSave(document)
        else:
            self.saveFile(fileName, document)


    def getUpdatedDocument(self):
        self.tabController.updateDocument()
        return self.document
        
        
    def promptAndSave(self, document):
        saveDialog = self.saveDialog
        if saveDialog.ShowDialog() == DialogResult.OK:
            fileName = saveDialog.FileName
            if self.saveFile(fileName, document):
                self.document.fileName = fileName
        
        
    def saveFile(self, fileName, document):
            try:
                writer = DocumentWriter(fileName)
                writer.write(document)
                return True
            except IOError, e:
                name = Path.GetFileName(fileName)
                MessageBox.Show(
                    'Could not write file "%s"\r\nThe error was:\r\n%s' %
                        (name, str(e)),
                    "Error Saving File",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                )
                return False


class SaveAsCommand(SaveCommand):
    
    title = "Save Document As"

    def execute(self):
        fileName = self.document.fileName
        document = self.getUpdatedDocument()
        if fileName is not None:    
            name = Path.GetFileName(fileName)
            directory = Path.GetDirectoryName(fileName) 
            self.saveDialog.FileName = name
            if Directory.Exists(directory):
                self.saveDialog.InitialDirectory = directory
        
        self.promptAndSave(document)

