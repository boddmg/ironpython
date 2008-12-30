from System import Uri
from System.Net import WebClient
from System.Windows.Browser import HttpUtility

token = 0
def get_next():
    """
    WebClient caches the results of downloading from URIs.
    So to get round this we attach a new number for each fetch
    to make a unique URI.
    """
    global token
    token += 1
    return str(token)

get_url = 'http://localhost:9981/'
post_url = 'http://localhost:9981/'

def MakeGet(action, username, password):
    values = '?action=%s&username=%s&password=%s&nocache=%s'
    username = HttpUtility.UrlEncode(username)
    password = HttpUtility.UrlEncode(password)
    get_string = values % (action, username, password, get_next())
    return get_url + get_string 


class Fetcher(object):

    def __init__(self, action, username, password, callback):
        uri = Uri(MakeGet(action, username, password))
        
        self.callback = callback
        
        try:
            web = WebClient()
            
            web.DownloadStringCompleted += self.completed
            web.DownloadStringAsync(uri)
        except Exception, e:
            print 'Error beginning request'


    def completed(self, sender, event):
        if not event.Error or event.Cancelled:
            self.callback(event.Result)
        else:
            print 'Error', event.Error, event.Cancelled
            self.callback('')


class Poster(object):

    def __init__(self, tweet, username, password, callback):
        uri = Uri(post_url)
        self.callback = callback
        
        print 'Tweeting:', tweet[:10]
        tweet = tweet[:140]
    
        url_encoded_tweet = HttpUtility.UrlEncode(tweet)
        while len(url_encoded_tweet) > 160:
            # Twitter API states that encoded post data MUST NOT
            # exceed 160 characters
            tweet = tweet[:-1]
            url_encoded_tweet = HttpUtility.UrlEncode(tweet)
        
        username = HttpUtility.UrlEncode(username)
        password = HttpUtility.UrlEncode(password)
        
        data = '%s=%s&%s=%s&%s=%s' % ('username', username,
            'password', password, 'tweet', url_encoded_tweet)
                
        web = WebClient()
        web.UploadStringCompleted += self.completed
        web.UploadStringAsync(uri, "Post", data)


    def completed(self, sender, event):
        if event.Cancelled or event.Error:
            # Post failed
            print 'POST failed'
            return self.callback('')
        return self.callback(event.Result)
        
        