
class Value(object):
    def __init__(self, value):
        self.value = value
        
    def __eq__(self, other):
        if isinstance(other, Value):
            return self.value == other.value
        return False
        
    def __ne__(self, other):
        return not self.__eq__(other)
    
if __name__ == '__main__':
    v1 = Value(6)
    v2 = Value(3)
    v3 = Value(6)
    assert v1 == v3
    assert v1 != v2
    assert v1 != 6
    