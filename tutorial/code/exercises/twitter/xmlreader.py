import clr
clr.AddReference('System.Xml')
from System.Xml import XmlException, XmlNodeType, XmlReader, XmlReaderSettings

class XmlDocumentReader(object):

    def read(self, textreader):
        settings = XmlReaderSettings()
        settings.IgnoreWhitespace = True
        reader = XmlReader.Create(textreader, settings)
        
        self._currentElement = None

        nodeTypeHandlers = {
            XmlNodeType.Element    : self.onStartElement,
            XmlNodeType.EndElement : self.onEndElement,
            XmlNodeType.Text       : self.onText,
            XmlNodeType.XmlDeclaration: lambda *_: None
            }

        while reader.Read():
            handler = nodeTypeHandlers.get(reader.NodeType)
            if handler:
                handler(reader)
            else:
                raise XmlException("invalid data at line %d" % reader.LineNumber)


    def onStartElement(self, reader):
        name = reader.Name
        self._currentElement = name

        attributes = {}
        while reader.MoveToNextAttribute():
            attributes[reader.Name] = reader.Value

        startHandler = self._findHandler('Start', name)
        if startHandler:
            startHandler(reader.LineNumber, attributes)


    def onText(self, reader):
        textHandler = self._findHandler('Text', self._currentElement)
        if textHandler:
            textHandler(reader.LineNumber, reader.Value)


    def onEndElement(self, reader):
        endHandler = self._findHandler('End', reader.Name)
        if endHandler:
            endHandler(reader.LineNumber)
       

    def _findHandler(self, prefix, nodeName):
        methodName = 'on%s_%s' % (prefix, nodeName.lower())
        return getattr(self, methodName, None)

        

