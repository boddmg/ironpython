import sys
from testutils import MakeSuite, RunTests

import testing

suite = MakeSuite(testing)
results = RunTests(suite, verbosity=2)

if results.failures or results.errors:
    sys.exit(1)
