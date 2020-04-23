import unittest

import TestExpressions
import TestParser
import TestRuleEvaluator
import TestSingletons

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()


# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(TestExpressions))
suite.addTests(loader.loadTestsFromModule(TestParser))
suite.addTests(loader.loadTestsFromModule(TestRuleEvaluator))
suite.addTests(loader.loadTestsFromModule(TestSingletons))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)