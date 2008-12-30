import clr
clr.AddReference("System.Xml")

class Note(object):

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body


    @staticmethod
    def fromXml(element):
        id = element.Attributes.GetNamedItem('id').Value
        title = element.Attributes.GetNamedItem('title').Value
        body = element.InnerText.strip()
        return Note(id, title, body)


    def makeAttr(self, document, name, value):
        attr = document.CreateAttribute(name)
        attr.Value = value
        return attr


    # needs the document in order to create elements within it
    def toXml(self, document):
        element = document.CreateElement('note')
        element.Attributes.Append(self.makeAttr(document, 'id', self.id))
        element.Attributes.Append(self.makeAttr(document, 'title', self.title))
        element.InnerText = self.body
        return element


    def toSummaryXml(self, document, linkTemplate):
        element = document.CreateElement('notelink')
        element.Attributes.Append(self.makeAttr(document, 'title', self.title))
        element.Attributes.Append(self.makeAttr(document, 'href', linkTemplate % self.id))
        return element
