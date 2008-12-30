class Iterator(object):
    def __init__(self, start, stop):
        self.stop = stop
        self.count = start
        
    def __iter__(self):
        return self
    
    def next(self):
        if self.count > self.stop:
            raise StopIteration
        count = self.count
        self.count += 1
        return count
    
if __name__ == '__main__':
    for entry in Iterator(17, 20):
        print entry
