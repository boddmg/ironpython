import unittest

class Value(object):
    def __init__(self, value):
        self.value = value
        
    def add(self, number):
        return self.value + number
    
    def isEven(self):
        return (self.value % 2) == 0


class ValueTest(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.value = Value(6)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.value = None
    
    def testConstructorShouldStoreValue(self):
        self.assertEquals(self.value.value, 6, 
                          "value attribute not set correctly")
        
    def testAddShouldReturnArgumentAddedToValue(self):
        self.assertEquals(self.value.add(3), 9, 
                          "add returned the wrong answer")
        
    def testIsEvenShouldReturnTrueForEvenNumbers(self):
        self.assertTrue(self.value.isEven(), 
                        "Wrong answer for isEven with an even number")
        
    def testIsEvenShouldReturnFalseForOddNumbers(self):
        value = Value(7)
        self.assertFalse(value.isEven(), 
                         "Wrong answer for isEven with an odd number")
    

if __name__ == '__main__':
    unittest.main()