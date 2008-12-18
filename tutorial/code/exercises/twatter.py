import AddReferences
from System.Windows.Forms import Application

from MainForm import MainForm
from twitter.Client import Client
from config import config

import twatterdb

class Twatter(object):

    def __init__(self):
        self.client = Client(config.username, 
                             config.password,
                             config.url_base)

        self.form = MainForm()
        self.refreshFriends()


    def refreshFriends(self):
        prevSelection = self.form.friendsListBox.SelectedItem
        self.form.showFriends(['All'])
        # fires the onSelectFriend event handler that displays tweets
        self.form.friendsListBox.SelectedItem = prevSelection


    def run(self):
        self.form.Show()
        Application.Run(self.form)


def main():
    app = Twatter()
    app.run()

if __name__ == '__main__':
    main()
