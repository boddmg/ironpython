#! /usr/bin/python

import cgi
import urllib
import urllib2
import BaseHTTPServer
import SimpleHTTPServer
from StringIO import StringIO
from threading import Thread


clientaccesspolicy = """<?xml version="1.0" encoding="utf-8"?>
<access-policy>
    <cross-domain-access>
        <policy>
            <allow-from http-request-headers="*">
                <domain uri="*"/>
            </allow-from>
            <grant-to>
                <resource path="/" include-subpaths="true"/>
            </grant-to>
        </policy>
    </cross-domain-access>
</access-policy>"""

crossdomain = """<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
  <allow-access-from domain="*" />
</cross-domain-policy>"""


def read_with_authentication(url, username, password, data=None):
    protocol = 'http://'
    base_url = 'twitter.com'
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, base_url, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)

    urllib2.install_opener(opener)
    return urllib2.urlopen(protocol + url, data)


class TwitterProxy(SimpleHTTPServer.SimpleHTTPRequestHandler):

    server_version = "TwitterProxy/0.1.0"
    
 
    def do_HEAD(self):
        f = self.send_head()
        self.end_headers()
        if f:
            f.close()
            
            
    def do_GET(self):
        f = self.send_head()
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

            
    def send_head(self):
        print 'Serving:', self.path
        if len(self.path) <= 1:
            self.send_response(404)
            return
           
        path = self.path[1:]
        
        if path == 'clientaccesspolicy.xml':
            self.send_response(200)
            self.send_header("Content-type", 'application/xml')
            return StringIO(clientaccesspolicy)
        
        if path == 'crossdomain.xml':
            self.send_response(200)
            self.send_header("Content-type", 'application/xml')
            return StringIO(crossdomain)
        
        if not path.startswith('?'):
            self.send_response(404)
            return
            
        values = cgi.parse_qs(path[1:])
        username = values['username'][0]
        password = values['password'][0]
        action = values['action'][0]
        
        
        print 'Parsed:', username, 'password', action
        self.send_response(200)
        self.send_header("Content-type", 'application/xml')
        
        if action == 'verify':
            url = 'twitter.com/account/verify_credentials.xml'

        elif action == 'fetch':
            url = 'twitter.com/statuses/friends_timeline.xml'
        
        else:
            self.send_response(404)
            return
        
        return self.safe_get(url, username, password, action)
        
    
    def do_POST(self):
        print 'Post received...'
        length = self.headers.getheader('content-length')
        if not length:
            print 'No post data - exiting'
            self.send_response(404)
            return

        try:
            nbytes = int(length)
        except (TypeError, ValueError):
            nbytes = 0
        if self.command.lower() != "post" or nbytes == 0:
            print 'not a post!'
            self.send_response(404)
            return
            
        data = self.rfile.read(nbytes)
        values = cgi.parse_qs(data)
        if ('username' not in values or 'password' not in values
            or 'tweet' not in values):
            print 'missing values'
            self.send_response(404)
            return
        
        username = values['username'][0]
        password = values['password'][0]
        tweet = values['tweet'][0]
        print 'Username', username, 'Password', password[:3] + '...', 'Tweet', tweet[:10] + '...'

        url = 'twitter.com/statuses/update.xml'
        data = urllib.urlencode({'status': tweet})
        
        # make post from another thread because a slow response breaks Silverlight...
        t = Thread(target=self.safe_get, args=(url, username, password, 'post', data))
        t.start()
        
        self.send_response(200)
        self.send_header("Content-type", 'text/plain')
        self.end_headers()
        self.copyfile(StringIO('posted'), self.wfile)
        
        
    def safe_get(self, url, username, password, action, data=None):
        if data is not None:
            print 'POST started'
        try:
            return read_with_authentication(url, username, password, data)
        except Exception, e:
            msg = 'Error in %s' % action
            print msg, e
            return StringIO('error')
   

port = 9981

def run(port=port):
    ServerAddress = ('', port)
    print 'Serving on port:', port
    httpd = BaseHTTPServer.HTTPServer(ServerAddress, TwitterProxy)
    httpd.serve_forever()

if __name__ == '__main__':
    run()