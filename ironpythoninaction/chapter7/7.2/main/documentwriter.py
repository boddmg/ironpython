from System.Xml import XmlWriter, XmlWriterSettings

class DocumentWriter(object):
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def write(self, document):
        settings = XmlWriterSettings()
        settings.Indent = True
        settings.IndentChars = '    '
        
        settings.OmitXmlDeclaration = True
        writer = XmlWriter.Create(self.fileName, settings)
        
        writer.WriteStartDocument()
        writer.WriteStartElement("document")
        
        def WritePage(page):
            writer.WriteStartElement("page")
            writer.WriteAttributeString("title", page.title)
            writer.WriteString(page.text)
            writer.WriteEndElement()
    
        for page in document:
            WritePage(page)
        
        writer.WriteEndElement()
        writer.WriteEndDocument()
        writer.Flush()
        writer.Close()

