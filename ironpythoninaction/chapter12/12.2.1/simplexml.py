import clr
clr.AddReference("System.Xml")

from System.Xml import XmlDocument, XmlElement, XmlText


singularToPlural = {
    'entry': 'entries',
    'child': 'children',
}

pluralToSingular = dict((value, key)
    for (key, value) in singularToPlural.iteritems())


def isPluralOf(maybePlural, noun):
    '''whether maybePlural is the plural of the specified noun

    This should be replaced with a real plural detection system'''
    if pluralToSingular.get(maybePlural) == noun:
        return True
    return maybePlural == noun + 's'


def elementOnlyContainsText(element):
    return (element.Attributes.Count == 0
        and element.HasChildNodes
        and element.FirstChild == element.LastChild
        and isinstance(element.FirstChild, XmlText))


class NotFound(Exception):
    pass


class SimpleXml(object):
    def __init__(self, element):
        self.element = element


    def _childElements(self):
        'just the elements that are children of the current node'
        for node in self.element.ChildNodes:
            if isinstance(node, XmlElement):
                yield node


    def _getAttribute(self, name):
        attr = self.element.Attributes.GetNamedItem(name)
        if attr:
            return attr.Value
        raise NotFound()


    def _getChild(self, name):
        for node in self._childElements():
            if node.Name == name:
                if elementOnlyContainsText(node):
                    return node.InnerText
                else:
                    # make sure we return another SimpleXml
                    return SimpleXml(node)
        raise NotFound()


    def _getChildren(self, name):
        matchingChildren = []
        singularName = None
        for node in self._childElements():
            if singularName is None and isPluralOf(name, node.Name):
                singularName = node.Name
                matchingChildren.append(node)
            elif singularName == node.Name:
                matchingChildren.append(node)

        if matchingChildren:
            return map(SimpleXml, matchingChildren)
        raise NotFound()


    def _find(self, name):
        # the requested attribute could be an XML attribute
        try:
            return self._getAttribute(name)
        except NotFound:
            pass

        # it could be a child element
        try:
            return self._getChild(name)
        except NotFound:
            pass

        # or it could be a pluralised version of a child element's name
        try:
            return self._getChildren(name)
        except NotFound:
            raise AttributeError('element has no attribute %r' % name)


    def __getattr__(self, name):
        try:
            return getattr(self.element, name)
        except AttributeError:
            return self._find(name)


    @staticmethod
    def fromString(value):
        document = XmlDocument()
        document.LoadXml(value)
        return SimpleXml(document.DocumentElement)


    @staticmethod
    def fromStream(stream):
        document = XmlDocument()
        document.Load(stream)
        return SimpleXml(document.DocumentElement)
