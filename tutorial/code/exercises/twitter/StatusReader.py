from xmlreader import XmlDocumentReader
from System import DateTime
import rfc822

class StatusReader(XmlDocumentReader):
   
    def __init__(self):
        self.tweets = []
        self.currentTweet = None
        self.currentUser = None

    def read(self, *args):
        XmlDocumentReader.read(self, *args)
        return self.tweets

    def onStart_status(self, _, __):
        self.currentTweet = {}

    def onEnd_status(self, _):
        self.tweets.append(self.currentTweet)

    def onText_id(self, _, text):
        if self.currentUser is not None:
            updatee = self.currentUser
        else:
            updatee = self.currentTweet
        updatee['id'] = int(text)

    def onText_created_at(self, _, text):
        self.currentTweet['created_at'] = DateTime(*rfc822.parsedate(text)[:6])

    def onText_text(self, _, text):
        self.currentTweet['text'] = text

    def onStart_user(self, _, __):
        self.currentUser = {}

    def onEnd_user(self, _):
        self.currentTweet['user'] = self.currentUser
        self.currentUser = None

    def onText_screen_name(self, _, text):
        self.currentUser['screen_name'] = text

    def onText_name(self, _, text):
        self.currentUser['name'] = text

    def onText_url(self, _, text):
        self.currentUser['url'] = text

    def onText_profile_image_url(self, _, text):
        self.currentUser['profile_image_url'] = text

    def onText_location(self, _, text):
        self.currentUser['location'] = text

    def onText_description(self, _, text):
        self.currentUser['description'] = text


def demo():
    import sys
    from System.IO import StringReader
    
    reader = StatusReader()
    xml = file(sys.argv[1], 'rb').read()
    reader.read(StringReader(xml))
    print reader.tweets

if __name__ == '__main__':
    demo()
