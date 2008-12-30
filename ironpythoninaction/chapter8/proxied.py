
def GetProxy(thing, readlist=None, writelist=None, dellist=None):
    
    class Proxy(object):
        def __getattr__(self, name):
            if readlist and name in readlist:
                return getattr(thing, name)
            else:
                raise AttributeError("Attribute %s not found" % name)
            
        def __setattr__(self, name, value):
            if writelist and name in writelist:
                setattr(thing, name, value)
            else:
                raise AttributeError("Attribute %s not found" % name)

        def __delattr__(self, name):
            if dellist and name in dellist:
                delattr(thing, name)
            else:
                raise AttributeError("Attribute %s not found" % name)

    return Proxy()


if __name__ == '__main__':
    all = ['a', 'b', 'c', 'd', 'e']
    read = ['b', 'c', 'd']
    write = ['a', 'c', 'd']
    delete = ['a', 'b', 'd']
    
    class Test(object):
        def __init__(self):
            for name, value in zip(all, range(5)):
                setattr(self, name, value)

    test = Test()
    proxy = GetProxy(test, read, write, delete)
    
    def AssertRaisesAttributeError(callable):
        try:
            callable()
        except AttributeError:
            return
        else:
            raise AssertionError("AttributeError %s not raised" % exceptionType)
        
    for name, value in zip(all, range(5)):
        if name in read:
            assert getattr(proxy, name) == value        
        else:
            AssertRaisesAttributeError(lambda: getattr(proxy, name))
            
        if name in write:
            setattr(proxy, name, value + 1)
            assert getattr(test, name) == value + 1
        else:
            AssertRaisesAttributeError(lambda: setattr(proxy, name, value + 1))
            
        if name in delete:
            delattr(proxy, name)
            assert not hasattr(test, name)
        else:
            AssertRaisesAttributeError(lambda: delattr(proxy, name))
        