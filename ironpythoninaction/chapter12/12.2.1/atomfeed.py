from System.Net import WebClient
from simplexml import SimpleXmlWrapper

feedUrl = "http://www.voidspace.org.uk/ironpython/planet/atom.xml"
feedContent = WebClient().DownloadString(feedUrl)
feed = SimpleXmlWrapper.fromString(feedContent)

for entry in feed.entries:
    print 'Title:', entry.title
    print 'Url:', entry.link.href
    print 'Author:', entry.author.name
    print

