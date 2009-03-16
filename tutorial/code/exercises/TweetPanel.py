import AddReferences

from System.Drawing import Bitmap, Color, ContentAlignment, Font, FontStyle
from System.IO import MemoryStream
from System.Net import WebClient
from System.Windows.Forms import (
    AnchorStyles, BorderStyle, DockStyle, Panel, Label, PictureBox
)

import os

def getImage(tweet):
    cacheLocation = os.path.join('imagecache', tweet['screen_name'] + '.jpg')
    if os.path.isfile(cacheLocation):
        return Bitmap.FromFile(cacheLocation)

	# Exercise E: download and save the image in the cache
	# replace the line below with something appropriate
    return Bitmap.FromFile(os.path.join('imagecache', '__fallback__.png'))
    

HEIGHT = 49

class TweetPanel(Panel):

    def __init__(self, tweet):
        Panel.__init__(self)
        self.tweet = tweet
        self.Height = HEIGHT

        self.imageBox = imageBox = PictureBox(Height=HEIGHT, Width=HEIGHT)
        imageBox.Image = getImage(tweet)
        imageBox.Anchor = AnchorStyles.Left
        imageBox.Parent = self

        halfway = (self.ClientSize.Width - imageBox.Width) / 2
        
        self.friendLabel = friendLabel = Label(Text=tweet['screen_name'],
                                               TextAlign=ContentAlignment.MiddleLeft)
        friendLabel.Font = Font(friendLabel.Font,
                                friendLabel.Font.Style | FontStyle.Bold)
        friendLabel.Left = imageBox.Width
        friendLabel.Anchor = AnchorStyles.Left | AnchorStyles.Right
        friendLabel.Width = halfway
        friendLabel.Parent = self

        self.dateLabel = dateLabel = Label(Text=str(tweet['created']),
                                           TextAlign=ContentAlignment.MiddleRight)
        dateLabel.Width = halfway
        dateLabel.Left = self.Width - dateLabel.Width - 10 # scrollbar
        dateLabel.Anchor = AnchorStyles.Left | AnchorStyles.Right
        dateLabel.Parent = self
        dateLabel.BringToFront()

        self.tweetLabel = tweetLabel = Label(Text=tweet['text'])
        tweetLabel.Left = self.imageBox.Width
        tweetLabel.Top = friendLabel.Height
        tweetLabel.Width = self.Width - self.imageBox.Width
        tweetLabel.Height = self.Height - friendLabel.Height
        tweetLabel.Anchor = (AnchorStyles.Left
                                  | AnchorStyles.Top
                                  | AnchorStyles.Right
                                  | AnchorStyles.Bottom)
        tweetLabel.Parent = self


    def Dispose(self, disposing=None):
        if self.imageBox.Image is not None:
            self.imageBox.Image.Dispose()
            self.imageBox.Image = None
        if disposing is None:
            Panel.Dispose(self)
            
