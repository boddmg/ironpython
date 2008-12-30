import clr
clr.AddReference('System.Xml')
from System.Xml import XmlException, XmlNodeType, XmlReader, XmlReaderSettings


MISSING_HANDLERS = (None, None, None)
ignore = lambda *_: None

class XmlDocumentReader(object):

    def __init__(self, elementHandlers):
        self._elementHandlers = elementHandlers


    def read(self, textreader):
        settings = XmlReaderSettings()
        settings.IgnoreWhitespace = True
        reader = XmlReader.Create(textreader, settings)
        
        self._currentElement = None

        nodeTypeHandlers = {
            XmlNodeType.Element    : self.onStartElement,
            XmlNodeType.EndElement : self.onEndElement,
            XmlNodeType.Text      : self.onText,
            XmlNodeType.XmlDeclaration: ignore
        }

        try:
            while reader.Read():
                handler = nodeTypeHandlers.get(reader.NodeType)
                if handler:
                    handler(reader)
                else:
                    print reader.NodeType
                    raise XmlException("invalid data at line %d" % 
                                       reader.LineNumber)
        finally:
            reader.Close()
            

    def onStartElement(self, reader):
        name = reader.Name
        self._currentElement = name

        attributes = {}
        while reader.MoveToNextAttribute():
            attributes[reader.Name] = reader.Value

        startHandler = self._elementHandlers.get(name, MISSING_HANDLERS)[0]
        if startHandler:
            startHandler(reader.LineNumber, attributes)
        else:
            raise XmlException("invalid data at line %d" % 
                               reader.LineNumber)


    def onText(self, reader):
        textHandler = self._elementHandlers.get(self._currentElement, MISSING_HANDLERS)[1]
        if textHandler:
            textHandler(reader.LineNumber, reader.Value)


    def onEndElement(self, reader):
        endHandler = self._elementHandlers.get(reader.Name, MISSING_HANDLERS)[2]
        if endHandler:
            endHandler(reader.LineNumber)
        
