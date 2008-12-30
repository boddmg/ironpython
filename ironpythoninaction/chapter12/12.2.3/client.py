from simplexml import SimpleXml
from note import Note

from System.IO import MemoryStream
from System.Net import WebException, WebExceptionStatus, WebRequest
from System.Xml import XmlDocument, XmlWriter


def sendMessage(method, url, note=None):
    request = WebRequest.Create(url)
    request.Method = method
    if note is not None:
        writeNoteToRequest(note, request)
    try:
        response = request.GetResponse()
    except WebException, e:
        if e.Status == WebExceptionStatus.ProtocolError:
            # this is an error message from the service
            # look in the response for the problem
            response = e.Response
        else:
            raise
    stream = response.GetResponseStream()
    responseDoc = SimpleXml.fromStream(stream)
    stream.Close()
    checkResponse(responseDoc)
    return responseDoc


class ServiceError(Exception):
    pass


def checkResponse(response):
    if response.status != 'ok':
        raise ServiceError(response.InnerText)


def writeNoteToRequest(note, request):
    doc = XmlDocument()
    doc.AppendChild(doc.CreateXmlDeclaration('1.0', 'utf-8', 'yes'))
    doc.AppendChild(note.toXml(doc))

    request.ContentType = 'text/xml'
    stream = request.GetRequestStream()
    writer = XmlWriter.Create(stream)
    doc.WriteTo(writer)
    writer.Flush()
    stream.Close()


index = 'http://localhost:8080/notes'

def getAllNotes():
    response = sendMessage('GET', index)
    return [(n.title, n.href) for n in response.notelinks]


def getNote(link):
    response = sendMessage('GET', link)
    return Note.fromXml(response.note.element)


def addNote(note):
    response = sendMessage('POST', index, note)
    return response.notelink.href


def updateNote(link, note):
     sendMessage('PUT', link, note)


def deleteNote(link):
     sendMessage('DELETE', link)


if __name__ == '__main__':
    print getAllNotes()

    newNote = Note('thing 2', 'title', 'body')
    newLink = addNote(newNote)

    print getAllNotes()
    for title, link in getAllNotes():
        note = getNote(link)
        print note.id
        print note.title
        print note.body
        print

    newNote.title = 'this is the new title'
    updateNote(newLink, newNote)

    print getAllNotes()

    newNote.id = 'newid'
    try:
        updateNote(newLink, newNote)
    except ServiceError, e:
        print e

    print getAllNotes()

    deleteNote(newLink)

    print getAllNotes()
