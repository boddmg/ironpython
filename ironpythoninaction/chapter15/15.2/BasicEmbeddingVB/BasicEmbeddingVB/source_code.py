import __main__
print "Inside", __name__, type(__main__)

# Use and change the 'variable' which is injected
print variable
variable = "Goodbye world!"

import Example
print Example.HelloWorld
print "The answer is", Example.answer

from ClassLibrary import Klass
Klass.Method1()
Klass.Method2()
