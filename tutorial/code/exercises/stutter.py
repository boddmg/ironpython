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

		# Practical 4: Use the 'onRefresh' function to handle events from the
        # 'Refresh' menu item.
		# Write an 'onQuit' function and use it to handle 'Quit' menu item
        # events.

		# Exercise H: Add a handler for the friendListBox.SelectedIndexChanged
		# event.

		# Exercuse I: Add a handler for the 'Post' Button

        self.refreshFriends()


    def refreshFriends(self):
        prevSelection = self.form.friendsListBox.SelectedItem
        self.form.showFriends(['All'] + stutterdb.getFriends())
        # fires the onSelectFriend event handler that displays tweets
        self.form.friendsListBox.SelectedItem = prevSelection


    def run(self):
        self.form.Show()
        Application.Run(self.form)


    def onRefresh(self, source, args):
        def refresh():
            for tweet in self.client.getFriendsTimeline():
                stutterdb.saveTweet(tweet)
        DoBackgroundWithInvoke(refresh, self.refreshFriends, self.form)


def main():
    app = Stutter()
    app.run()

if __name__ == '__main__':
    main()
