from System.IO import Directory, Path
from System.Windows.Forms import (
    DialogResult, MessageBox, 
    MessageBoxButtons, MessageBoxIcon,
    OpenFileDialog
)

from main.documentreader import DocumentReader, XmlException
from main.savecommands import filter

class OpenCommand(object):
    
    title = "Open Document"
    
    def __init__(self, mainForm):
        self.openFileDialog = OpenFileDialog()
        self.mainForm = mainForm
        self.document = None
        
        self.openFileDialog.Filter = filter
        self.openFileDialog.Title = self.title

    def execute(self):
        fileName = self.mainForm.document.fileName
        directory = Path.GetDirectoryName(fileName)
        directoryExists = Directory.Exists(directory)
        openFileDialog = self.openFileDialog
        
        if fileName is not None and directoryExists:
            openFileDialog.InitialDirectory = directory
            openFileDialog.FileName = fileName
        
        if openFileDialog.ShowDialog() == DialogResult.OK:
            document = self.getDocument(openFileDialog.FileName)
            if document:
                self.mainForm.document = document
            
    def getDocument(self, fileName):
            try:
                reader = DocumentReader(fileName)
                return reader.read()
            except (IOError, XmlException), e:
                name = Path.GetFileName(fileName)
                MessageBox.Show(
                    'Could not read file "%s"\r\nThe error was:\r\n%s' %
                        (name, str(e)),
                    "Error Saving File",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                )
                return None
            