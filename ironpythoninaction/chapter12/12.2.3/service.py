import clr
clr.AddReference("System.Web")

from note import Note

from System.IO import MemoryStream
from System.Net import HttpListener
from System.Text import Encoding
from System.Web import HttpUtility
from System.Xml import XmlDocument, XmlWriter


class ServiceError(Exception):
    def __init__(self, statusCode, reason):
        self.statusCode = statusCode
        self.reason = reason


LINK = 'http://localhost:8080/notes/%s'

class NotesService(object):

    def __init__(self):
        self.listener = HttpListener()
        self.listener.Prefixes.Add('http://localhost:8080/notes/')
        self.notes = {
            'example': Note('example', 
                            'An example note', 
                            'Note content here')}


    def run(self):
        self.listener.Start()
        print "Notes service started"
        while True:
            context = self.listener.GetContext()
            self.handle(context)


    def pathComponents(self, context):
        url = context.Request.RawUrl.strip('/')
        return url.split('/')


    def handle(self, context):
        path = self.pathComponents(context)
        method = context.Request.HttpMethod
        print method, path
        handlers = {}
        if path == ['notes']:
            handlers = dict(GET=self.getNotes, POST=self.addNote)
        elif len(path) == 2:
            handlers = dict(GET=self.getNote, 
                            PUT=self.updateNote, 
                            DELETE=self.deleteNote)
        handler = handlers.get(method, self.error)
        try:
            handler(context)
        except ServiceError, e:
            self.error(context, e.statusCode, e.reason)


    def error(self, context, statusCode=400, 
              reason='invalid path/method combination'):
        doc = self.makeResponse()
        doc.DocumentElement.Attributes.GetNamedItem('status').Value = 'error'
        doc.DocumentElement.InnerText = reason
        self.writeDocument(context, doc, statusCode)


    def makeResponse(self):
        doc = XmlDocument()
        doc.AppendChild(doc.CreateXmlDeclaration('1.0', 'utf-8', 'yes'))
        response = doc.CreateElement('response')
        status = doc.CreateAttribute('status')
        status.Value = 'ok'
        response.Attributes.Append(status)
        doc.AppendChild(response)
        return doc


    def getNotes(self, context):
        doc = self.makeResponse()
        for note in self.notes.values():
            link = note.toSummaryXml(
                doc, LINK)
            doc.DocumentElement.AppendChild(link)
        self.writeDocument(context, doc)


    def getNoteFromRequest(self, request):
        message = XmlDocument()
        message.Load(request.InputStream)
        request.InputStream.Close()
        return Note.fromXml(message.DocumentElement)


    def addNote(self, context):
        note = self.getNoteFromRequest(context.Request)
        if note.id in self.notes:
            raise ServiceError(400, 'note id already used')

        self.notes[note.id] = note
        doc = self.makeResponse()
        doc.DocumentElement.AppendChild(note.toSummaryXml(doc, LINK))
        self.writeDocument(context, doc)


    def getNoteForCurrentPath(self, context):
        lastChunk = self.pathComponents(context)[-1]
        noteId = HttpUtility.UrlDecode(lastChunk)
        note = self.notes.get(noteId)
        if note is None:
            raise ServiceError(404, 'no such note')
        return note


    def getNote(self, context):
        note = self.getNoteForCurrentPath(context)
        doc = self.makeResponse()
        doc.DocumentElement.AppendChild(note.toXml(doc))
        self.writeDocument(context, doc)


    def updateNote(self, context):
        note = self.getNoteForCurrentPath(context)
        updatedNote = self.getNoteFromRequest(context.Request)
        if note.id != updatedNote.id:
            raise ServiceError(400, "can't change note id")
        self.notes[note.id] = updatedNote
        self.writeDocument(context, self.makeResponse())


    def deleteNote(self, context):
        note = self.getNoteForCurrentPath(context)
        del self.notes[note.id]
        self.writeDocument(context, self.makeResponse())


    def writeDocument(self, context, document, statusCode=200):
        response = context.Response
        response.StatusCode = statusCode
        response.ContentType = 'text/xml'
        response.ContentEncoding = Encoding.UTF8
        # Write the document to a temporary stream so we can tell
        # client its length. 
        stream = MemoryStream()
        writer = XmlWriter.Create(stream)
        document.WriteTo(writer)
        writer.Flush()
        response.ContentLength64 = stream.Length
        stream.WriteTo(response.OutputStream)
        response.OutputStream.Close()


if __name__ == '__main__':
    service = NotesService()
    service.run()
