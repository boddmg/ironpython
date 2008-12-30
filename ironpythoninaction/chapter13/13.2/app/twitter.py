from System.IO import StringReader

from xmlreader import XmlDocumentReader, ignore


ignored = (
    'created_at',
    'source',
    'truncated',
    'in_reply_to_status_id',
    'in_reply_to_user_id',
    'favorited',
    'user',
    'location',
    'description',
    'name',
    'profile_image_url',
    'url',
    'protected',
    'followers_count',
    'id'
)


class TwitterStatusReader(object):
    
    def read(self, data):
        self.statuses = []
        handlers = {
            'statuses': (self.onStartStatuses, None, self.onEndStatuses),
            'status': (self.onStartStatus, None, ignore),
            'text': (ignore, self.handleText, ignore),
            'screen_name': (ignore, self.handleScreenName, ignore)
        }
        for entry in ignored:
            handlers[entry] = (ignore, ignore, ignore)
            
        self.reader = XmlDocumentReader(handlers)
        self.reader.read(StringReader(data))
        return self.statuses

        
    def onStartStatuses(self, lineNumber, attributes):
        print 'Start statuses'
        
    def onEndStatuses(self, lineNumber):
        print 'End statuses'
        
    
    def onStartStatus(self, lineNumber, attributes):
        print 'New status:',
        self.statuses.append({})
        
    def handleText(self, lineNumber, value):
        print 'Value', value[:10] + '...',
        self.statuses[-1]['text'] = value
        
    def handleScreenName(self, lineNumber, value):
        print 'Name:', value
        self.statuses[-1]['name'] = value


