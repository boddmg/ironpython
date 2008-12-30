import unittest

"""
When creating my own TestCase class for a project, the first thing I do is
redefine the default 'assertEquals', 'assertTrue' and 'assertFalse'.

The default 'assertEquals' doesn't tell you what the actual and expected values
were in the failure message.

The default 'assertFalse' and 'assertTrue' will pass for any object which
evaluates to False or True.  I usually want them to actually check for
the values True and False.
"""

class TestCase(unittest.TestCase):
    
    def assertEquals(self, actual, expected, message=''):
        message += ':\nactual = "%s"\nexpected = "%s"\n' % (actual, expected)
        unittest.TestCase.assertEquals(self, actual, expected, message)
        
    def assertTrue(self, arg, message=''):
        unittest.TestCase.assertEquals(self, arg, True, message)
        
    def assertFalse(self, arg, message=''):
        unittest.TestCase.assertEquals(self, arg, False, message)
        
    def assertNone(self, arg, message=''):
        unittest.TestCase.assertEquals(self, arg, None, message)
        
    