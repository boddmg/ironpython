import unittest

class Value(object):
    def __init__(self, value):
        self.value = value
        
    def add(self, number):
        return self.value + number
    
    def isEven(self):
        return (self.value % 2) == 0


class ValueTest(unittest.TestCase):
    
    def testConstructorShouldStoreValue(self):
        value = Value(6)
        self.assertEquals(value.value, 6, 
                          "value attribute not set correctly")
        
    def testAddShouldReturnArgumentAddedToValue(self):
        value = Value(6)
        self.assertEquals(value.add(3), 9, 
                          "add returned the wrong answer")
        
    def testIsEvenShouldReturnTrueForEvenNumbers(self):
        value = Value(6)
        self.assertTrue(value.isEven(), 
                        "Wrong answer for isEven with an even number")
        
    def testIsEvenShouldReturnFalseForOddNumbers(self):
        value = Value(7)
        self.assertFalse(value.isEven(), 
                         "Wrong answer for isEven with an odd number")
    

if __name__ == '__main__':
    unittest.main()