from model import Document, Page
from xmldocumentreader import XmlDocumentReader, XmlException

class DocumentReader(object):
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.document = None
        self.currentPage = None
        self.pages = []
        
    def read(self):
        handlers = {
            'document': (self.onStartDocument, None, self.onEndDocument),
            'page': (self.onStartPage, self.onPageText, self.onEndPage)
        }
        self.reader = XmlDocumentReader(handlers)
        self.reader.read(self.fileName)
        return self.document
    
    
    def onStartPage(self, lineNumber, attributes):
        title = attributes.get('title')
        if title is None:
            raise XmlException('Invalid data at line %d' %
                               lineNumber)
        self.currentPage = Page(title)
        
        
    def onEndPage(self, lineNumber):
        self.pages.append(self.currentPage)
    
    
    def onPageText(self, lineNumber, value):
        self.currentPage.text = value.replace('\n', '\r\n')
        
        
    def onStartDocument(self, lineNumber, attributes):
        self.document = Document(self.fileName)
        
        
    def onEndDocument(self, lineNumber):
        self.document.pages = self.pages
        