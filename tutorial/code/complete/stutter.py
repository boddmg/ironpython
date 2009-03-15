#!/usr/bin/env ipy

import AddReferences
from System.Windows.Forms import Application

from MainForm import MainForm
from twitter.Client import Client
from config import config

import stutterdb

from threadhelper import DoBackgroundWithInvoke


class Stutter(object):

    def __init__(self):
        self.client = Client(config.username,
                             config.password,
                             config.url_base)

        self.form = MainForm()
        self.form.postButton.Click += self.onPost
        self.form.refreshMenuItem.Click += self.onRefresh
        self.form.friendsListBox.SelectedIndexChanged += self.onSelectFriend
        self.form.quitMenuItem.Click += self.onQuit
        self.refreshFriends()


    def refreshFriends(self):
        prevSelection = self.form.friendsListBox.SelectedItem
        self.form.showFriends(['All'] + stutterdb.getFriends())
        # fires the onSelectFriend event handler that displays tweets
        self.form.friendsListBox.SelectedItem = prevSelection


    def displayTweets(self):
        selectedFriend = None
        if self.form.friendsListBox.SelectedIndex != 0:
            selectedFriend = self.form.friendsListBox.SelectedItem
        self.form.showTweets(stutterdb.getTweets(selectedFriend))


    def run(self):
        self.form.Show()
        Application.Run(self.form)


    def onPost(self, source, args):
        tweet = self.client.update(self.form.postTextBox.Text)
        stutterdb.saveTweet(tweet)
        self.form.postTextBox.Text = ''
        self.displayTweets()


    def onRefresh(self, source, args):
        def refresh():
            for tweet in self.client.getFriendsTimeline():
                stutterdb.saveTweet(tweet)
        DoBackgroundWithInvoke(refresh, self.refreshFriends, self.form)


    def onSelectFriend(self, source, args):
        self.displayTweets()


    def onQuit(self, source, args):
        Application.Exit()


def main():
    app = Stutter()
    app.run()

if __name__ == '__main__':
    main()
