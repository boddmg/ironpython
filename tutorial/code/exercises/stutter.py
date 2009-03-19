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

        self.form.friendsListBox.SelectedIndexChanged += self.onSelectFriend

		# Practical 4: Use the 'onRefresh' function to handle events from the
        # 'Refresh' menu item.
		# Write an 'onQuit' function and use it to handle 'Quit' menu item
        # events.

		# Practical 5: Add 'onPost' method as a handler for the 'Post' button

        self.refreshFriends()


    def onSelectFriend(self, source, args):
        self.displayTweets()


    def displayTweets(self):
        selectedFriend = None
        if self.form.friendsListBox.SelectedIndex != 0:
            selectedFriend = self.form.friendsListBox.SelectedItem
        self.form.showTweets(stutterdb.getTweets(selectedFriend))


    def refreshFriends(self):
        prevSelection = self.form.friendsListBox.SelectedItem
        self.form.showFriends(['All'] + stutterdb.getFriends())
        # fires the onSelectFriend event handler that displays tweets
        self.form.friendsListBox.SelectedItem = prevSelection


    def onRefresh(self, source, args):
        def refresh():
            for tweet in self.client.getFriendsTimeline():
                stutterdb.saveTweet(tweet)
        DoBackgroundWithInvoke(refresh, self.refreshFriends, self.form)


    def onPost(self, source, args):
        tweet = self.client.update(self.form.postTextBox.Text)
        stutterdb.saveTweet(tweet)
        self.form.postTextBox.Text = ''
        self.displayTweets()


    def run(self):
        self.form.Show()
        Application.Run(self.form)


def main():
    app = Stutter()
    app.run()


if __name__ == '__main__':
    main()

