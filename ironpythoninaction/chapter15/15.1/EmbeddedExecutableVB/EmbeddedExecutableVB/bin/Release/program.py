import sys

print "Running!"
print 'Command line arguments', sys.argv
print 'Path', sys.path

def boom():
    raise Exception('boom!')
boom()

