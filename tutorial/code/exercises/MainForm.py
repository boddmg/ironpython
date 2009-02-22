import AddReferences
from itertools import cycle, izip
from System.Drawing import Color
from System.Windows.Forms import (AnchorStyles, BorderStyle, Button,
        DockStyle, Form, ListBox, MenuStrip, Panel, TextBox, ToolStripMenuItem)

from TweetPanel import TweetPanel

class MainForm(Form):

    INITIAL_WIDTH = 600
    INITIAL_HEIGHT = 600
    PADDING = 5

    def __init__(self):
        Form.__init__(self)
        self.Text = 'stutter'
        self.Height = self.INITIAL_HEIGHT
        self.Width = self.INITIAL_WIDTH

        self.postTextBox = TextBox()
        self.postTextBox.Multiline = True

        self.postButton = Button()
        self.postButton.Text = "Post"

        self.friendsListBox = ListBox()
      
        self._addMenu()
        self._layout()


    def _addMenu(self):
        self.menuStrip = MenuStrip()

        stutterMenu = ToolStripMenuItem("Stutter")
        stutterMenu.DropDown.ShowImageMargin = False
        stutterMenu.DropDown.ShowCheckMargin = False

        # TODO: Add menu items for 'Refresh' and 'Quit'
        # These need to be added to the menu 
        # 'stutterMenu' created above.


        self.menuStrip.Items.Add(stutterMenu)
        self.MainMenuStrip = self.menuStrip
        
        # TODO: The main menu (the MenuStrip) needs to
        #  be docked to the top of its parent
        # It doesn't have a parent yet


    def _layout(self):
        upperPanel = Panel()
        upperPanel.Top = self.menuStrip.Height + self.PADDING
        upperPanel.Left = self.PADDING
        upperPanel.Width = self.ClientSize.Width - (2 * self.PADDING)
        upperPanel.Anchor = (AnchorStyles.Left |
                             AnchorStyles.Top |
                             AnchorStyles.Right)

        upperPanel.Controls.Add(self.postTextBox)
        upperPanel.Controls.Add(self.postButton)

        self.postTextBox.Left = 0
        self.postTextBox.Top = 0
        self.postTextBox.Width = (upperPanel.ClientSize.Width -
                                  self.postButton.Width -
                                  self.PADDING)
        self.postTextBox.Height *= 2
        self.postTextBox.Anchor = (AnchorStyles.Top |
                                   AnchorStyles.Left |
                                   AnchorStyles.Right)

        self.postButton.Left = self.postTextBox.Width + self.PADDING
        self.postButton.Top = 0
        self.postButton.Anchor = (AnchorStyles.Top |
                                 AnchorStyles.Right)

        upperPanel.Height = self.postTextBox.Height

        self.Controls.Add(upperPanel)


        lowerPanel = Panel()
        lowerPanel.Width = upperPanel.Width
        lowerPanel.Top = upperPanel.Top + upperPanel.Height + self.PADDING
        lowerPanel.Left = self.PADDING
        lowerPanel.Height = (self.ClientSize.Height -
                             lowerPanel.Top -
                             self.PADDING)
        lowerPanel.Anchor = (AnchorStyles.Top |
                             AnchorStyles.Left |
                             AnchorStyles.Right |
                             AnchorStyles.Bottom)

        self.friendsListBox.Top = 0
        self.friendsListBox.Left = 0
        self.friendsListBox.Anchor = (AnchorStyles.Top |
                                      AnchorStyles.Left |
                                      AnchorStyles.Bottom)
        self.friendsListBox.Height = lowerPanel.ClientSize.Height
        lowerPanel.Controls.Add(self.friendsListBox)

        self.tweetsPanel = Panel()
        self.tweetsPanel.BorderStyle = BorderStyle.FixedSingle
        self.tweetsPanel.Anchor = (AnchorStyles.Top |
                                   AnchorStyles.Left |
                                   AnchorStyles.Right |
                                   AnchorStyles.Bottom)
        self.tweetsPanel.AutoScroll = True
        self.tweetsPanel.Top = 0
        self.tweetsPanel.Left = self.friendsListBox.Width + self.PADDING
        self.tweetsPanel.Width = (lowerPanel.ClientSize.Width -
                                  self.tweetsPanel.Left)
        self.tweetsPanel.Height = lowerPanel.ClientSize.Height
        lowerPanel.Controls.Add(self.tweetsPanel)

        self.Controls.Add(lowerPanel)
        

    def showFriends(self, friends):
        self.friendsListBox.DataSource = friends


    def showTweets(self, tweets):
        self.SuspendLayout()
        for oldPanel in self.tweetsPanel.Controls:
            oldPanel.Dispose()
        self.tweetsPanel.Controls.Clear()
        top = 0
        for tweet, color in izip(tweets, cycle([Color.LightBlue, Color.Cornsilk])):
            tweetPanel = TweetPanel(tweet)
            tweetPanel.BackColor = color
            tweetPanel.Width = self.tweetsPanel.Width
            tweetPanel.Top = top
            tweetPanel.Anchor = (AnchorStyles.Left
                                 | AnchorStyles.Right
                                 | AnchorStyles.Top)
            tweetPanel.Parent = self.tweetsPanel
            top += tweetPanel.Height

        self.ResumeLayout()
                                 
