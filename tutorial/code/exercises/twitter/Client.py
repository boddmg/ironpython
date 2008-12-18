import clr
clr.AddReference('System')
from System.IO import StreamReader, StreamWriter
from System.Net import NetworkCredential, WebRequest

import urllib

from StatusReader import StatusReader


class Client(object):

    def __init__(self, username, password, url_base='http://twitter.com'):
        self.credentials = NetworkCredential(username, password)
        self.url_base = url_base


    def getFriendsTimeline(self):
        request = WebRequest.Create(self.url_base + '/statuses/friends_timeline.xml')
        request.Credentials = self.credentials
        response = request.GetResponse()
        reader = StatusReader()
        return reader.read(StreamReader(response.GetResponseStream()))


def demo():
    import sys
    client = Client(sys.argv[1], sys.argv[2])
    print client.getFriendsTimeline()

if __name__ == '__main__':
    demo()

