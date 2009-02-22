import clr
clr.AddReference('System')
from System.IO import StreamReader, StreamWriter
from System.Net import NetworkCredential, WebRequest, ServicePointManager

import urllib

from StatusReader import StatusReader

# See: http://groups.google.com/group/twitter-development-talk/browse_thread/thread/7c67ff1a2407dee7
# This setting needed for working with the Twitter API and .NET
ServicePointManager.Expect100Continue = False


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


    def update(self, text):
        request = WebRequest.Create(self.url_base + '/statuses/update.xml')
        request.Credentials = self.credentials
        request.Method = 'POST'

        writer = StreamWriter(request.GetRequestStream())
        postData = urllib.urlencode(dict(status=text))
        writer.WriteLine(postData)
        writer.Close()

        response = request.GetResponse()
        reader = StatusReader()
        tweets = reader.read(StreamReader(response.GetResponseStream()))
        assert len(tweets) == 1, "expecting just one update response"
        return tweets[0]
    

def demo():
    import sys
    client = Client(sys.argv[1], sys.argv[2])
    print client.getFriendsTimeline()

if __name__ == '__main__':
    demo()

