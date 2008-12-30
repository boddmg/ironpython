from System.Windows.Threading import DispatcherTimer
from System import TimeSpan, Uri

from System.Windows import (
    Thickness, CornerRadius,
    HorizontalAlignment,
    VerticalAlignment,
    TextWrapping,
    FontWeights,
    GridLength,
    TextWrapping
)

from System.Windows.Controls import (
    Border, Button, ScrollViewer,  
    ScrollBarVisibility,
    PasswordBox,
    Orientation, StackPanel, TextBlock, 
    TextBox, Grid,
    ColumnDefinition, RowDefinition,
    HyperlinkButton, CheckBox
) 

from System.Windows.Input import Key
from System.Windows.Media import Colors, SolidColorBrush
from System.Windows.Threading import DispatcherTimer

from dispatcher import GetDispatchFunction
#from password_textbox import PasswordTextBox
from storage import (
    CheckStored, DeleteStored, 
    GetStored, PutStored
)
from twitter_proxy import Fetcher, Poster
from twitter import TwitterStatusReader


REFRESH_RATE = 60  # Fetch new tweets every 60 seconds


class MainPanel(StackPanel):

    def __init__(self):
        self.Margin = Thickness(5)
        self.Background = SolidColorBrush(Colors.Green)
        self.create_headline()

        top_panel = ScrollViewer()
        top_panel.Height = 475
        top_panel.Background = SolidColorBrush(Colors.White)
        top_panel.VerticalScrollBarVisibility = ScrollBarVisibility.Auto
        self.top_panel = top_panel

        border = Border()
        border.BorderThickness = Thickness(5)
        border.CornerRadius = CornerRadius(10)
        border.BorderBrush = SolidColorBrush(Colors.Blue)
        border.Background = SolidColorBrush(Colors.Yellow)
        border.Padding = Thickness(5)
        
        bottom_panel = StackPanel()
        bottom_panel.VerticalAlignment = VerticalAlignment.Stretch
        bottom_panel.HorizontalAlignment = HorizontalAlignment.Stretch
        bottom_panel.Background = SolidColorBrush(Colors.Red)
        bottom_panel.Orientation = Orientation.Horizontal
        
        border.Child = bottom_panel
        self.Children.Add(top_panel)
        self.Children.Add(border)
        
        self.bottom_panel = bottom_panel
        self.populate_login_panel()
        
        
    def create_headline(self):
        headline = TextBlock()
        headline.Margin = Thickness(5, 5, 5, 5)
        headline.FontSize = 16
        headline.Text = 'Twitter on Silverlight for IronPython in Action'
        headline.Foreground = SolidColorBrush(Colors.White)
        self.Children.Add(headline)
        
        self.headline = headline


    def populate_login_panel(self):
        button = Button()
        button.Content = '  Login  '
        button.FontSize = 16
        button.Margin = Thickness(5, 5, 5, 5)
        button.HorizontalAlignment = HorizontalAlignment.Stretch
        
        remember_me = CheckBox()
        remember_me.IsChecked = True
        remember_me.Margin = Thickness(5, 5, 5, 5)
        remember_me.Content = 'Remember'
        
        button_pane = StackPanel()
        button_pane.Children.Add(button)
        button_pane.Children.Add(remember_me)

        username = TextBox()
        username.FontSize = 16
        username.Width = 200
        username.Margin = Thickness(5, 5, 5, 5)

        password = PasswordBox()
        password.FontSize = 16
        password.Width = 200
        password.Margin = Thickness(5, 5, 5, 5)
        
        def HandleEnterKey(s, event):
            if event.Key == Key.Enter:
                event.Handled = True
                self.onLogin(None, None)
        
        password.KeyDown += HandleEnterKey
        if CheckStored():
            stored_username, stored_password = GetStored()
            username.Text = stored_username
            password.Password = stored_password

        entry_panel = StackPanel()
        entry_panel.HorizontalAlignment = HorizontalAlignment.Stretch
        entry_panel.Children.Add(username)
        entry_panel.Children.Add(password)

        self.bottom_panel.Children.Add(entry_panel)
        self.bottom_panel.Children.Add(button_pane)

        self.button = button
        self.remember_me = remember_me
        self.username_box = username
        self.password_box = password
        button.Click += self.onLogin
        
        self.msg = TextBlock()
        self.msg.Text = '      Login       '
        self.msg.FontSize = 16
        self.msg.HorizontalAlignment = HorizontalAlignment.Center
        self.msg.VerticalAlignment = VerticalAlignment.Center
        self.bottom_panel.Children.Add(self.msg)
        
        
    def onLogin(self, sender, event):
        username = self.username_box.Text
        password = self.password_box.Password

        if not username or not password:
            return
        
        if self.remember_me.IsChecked:
            PutStored(username, password)
        elif CheckStored():
            DeleteStored()
        
        self._username = username
        self._password = password
        self.msg.Text = ' Verifying Login '
        verify = GetDispatchFunction(self.verify)
        Fetcher('verify', username, password, verify)


    def verify(self, data):
        if data != '<authorized>true</authorized>':
            self.msg.Text = '  Login Failed  '
            print 'Verify failed'
            return
            
        print 'Verify successful'
        self.msg.Text = ' Success\r\n Fetching tweets'
        
        fetch_tweets = GetDispatchFunction(self.fetch_tweets)
        Fetcher('fetch', self._username, self._password, fetch_tweets)
        
            
    def fetch_tweets(self, data):
        if not data:
            return

        print 'Tweet fetch complete'
        self.setup_post_panel()
        self.populate_tweets(data)
        
        print 'Creating timer'
        self.setup_timer()
                
        
    def populate_tweets(self, data):
        statuses = TwitterStatusReader().read(data)
        if not statuses:
            self.msg.Text = 'No tweets found!'
            return
            
        grid = Grid()
        grid.ShowGridLines = True
        self.top_panel.Content = grid

        first_column = ColumnDefinition()
        first_column.Width = GridLength(115.0)
        grid.ColumnDefinitions.Add(first_column)
        grid.ColumnDefinitions.Add(ColumnDefinition())
        
        for i in range(len(statuses)):
            grid.RowDefinitions.Add(RowDefinition())

        def configure_block(block, col, row):
            block.FontSize = 14
            block.Margin = Thickness(5)
    
            block.HorizontalAlignment = HorizontalAlignment.Left
            block.VerticalAlignment = VerticalAlignment.Center
            grid.SetRow(block, row)
            grid.SetColumn(block, col)

        for row, status in enumerate(statuses):
            name = status['name']
            text = status['text']
            
            block1 = HyperlinkButton()
            block1.Content = name
            block1.NavigateUri = Uri('http://twitter.com/%s' % name)
            
            # this should open the link in a new window 
            # but causes link to not function at all on Safari
            # It works for IE though
            #block1.TargetName = '_blank' 
            
            block1.FontWeight = FontWeights.Bold
            configure_block(block1, 0, row)
            
            block2 = TextBlock()
            block2.Text = text
            block2.TextWrapping = TextWrapping.Wrap
            configure_block(block2, 1, row)
            
            grid.Children.Add(block1)
            grid.Children.Add(block2)


    def setup_post_panel(self):
        self.bottom_panel.Children.Clear()
                
        entry_pane = TextBox()
        entry_pane.AcceptsReturn = True
        entry_pane.Width = 275
        entry_pane.Height = 75
        entry_pane.FontSize = 14
        entry_pane.Margin = Thickness(2)
        entry_pane.TextChanged += self.setCharsMsg
        entry_pane.TextWrapping = TextWrapping.Wrap
        
        self.entry_pane = entry_pane
        
        button = Button()
        button.Content = ' Post '
        self.bottom_panel.Children.Add(entry_pane)
        self.bottom_panel.Children.Add(button)

        self.button = button
        button.Click += self.onPost
        button.Margin = Thickness(2)

        self.msg = TextBlock()
        self.msg.FontSize = 14
        self.msg.HorizontalAlignment = HorizontalAlignment.Center
        self.msg.VerticalAlignment = VerticalAlignment.Center
        self.bottom_panel.Children.Add(self.msg)
        self.setCharsMsg(None, None)


    def setCharsMsg(self, sender, event):
        self.msg.Text = ' %s chars left' % (140 - len(self.entry_pane.Text))


    def onPost(self, sender, event):
        print 'Post clicked'
        tweet = self.entry_pane.Text
        if not tweet.strip():
            return
        
        self.entry_pane.IsReadOnly = True
        self.entry_pane.Background = SolidColorBrush(Colors.LightGray)
        self.msg.Text = ' Tweeting '
        self.button.IsEnabled = False
        
        tweet_complete = GetDispatchFunction(self.tweet_complete)
        Poster(tweet, self._username, self._password, tweet_complete)
        
    
    def tweet_complete(self, result):
        self.entry_pane.IsReadOnly = False
        self.entry_pane.Background = SolidColorBrush(Colors.White)
        self.button.IsEnabled = True

        print result
        if not result:
            self.msg.Text = 'Tweeting failed'
            return   
        
        self.entry_pane.Text = ''        
        self.setCharsMsg(None, None)
        
        # Fetch tweets so that we can see the new message
        # Although it may not be ready yet!
        populate_tweets = GetDispatchFunction(self.populate_tweets)
        Fetcher('fetch', self._username, self._password, populate_tweets)
        
    
    def setup_timer(self):
        def callback(s, e):
            print 'Timed tweet fetch'
            populate_tweets = GetDispatchFunction(self.populate_tweets)
            Fetcher('fetch', self._username, self._password, populate_tweets)
        
        self._timer = DispatcherTimer()
        self._timer.Tick += callback
        self._timer.Interval = TimeSpan.FromSeconds(REFRESH_RATE)
        self._timer.Start()
    