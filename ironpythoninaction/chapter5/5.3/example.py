from xmldocumentreader import XmlDocumentReader

output = {}


def handleStartDocument(lineNumber, attributes):
    if attributes != {}:
        raise Exception("Document should have no attributes!")
    print "Document start tag encountered"
    output['document'] = {}
    
def handleEndDocument(parent):
    print "Document end tag encountered"

def handleElement1(lineNumber, attributes):
    print 'Element1 encountered, with the following attributes:', attributes
    element1Dict = output['document'].setdefault('element1', {})
    element1Dict.update(attributes)
                                                 
def handleElement2(lineNumber, attributes):
    print 'Element2 encountered, with the following attributes:', attributes
    element1Dict = output['document'].setdefault('element1', )
    element1Dict.update(attributes)

def handleElement2Text(lineNumber, text):
    print 'Text encountered:',
    print text

def handleChild(lineNumber, attributes):
    print 'Child element, with the following attributes:', attributes
    
    
def handleEnd(lineNumber):
    pass
    
    
handlers = {
    'document': (handleStartDocument, None, handleEndDocument),
    'element1': (handleElement1, None, handleEnd),
    'element2': (handleElement2, handleElement2Text, handleEnd),
    'child': (handleChild, None, handleEnd)
}


reader = XmlDocumentReader(handlers)
reader.read('example.xml')

print output


