''' Testing entry point '''
import unittest
import sys
import os


sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
)
# pylint: disable=wrong-import-position
import test_utils
import test_auth
import test_cache
import test_storage
import test_storage_errors
import test_bot
import test_bot_errors


loader = unittest.TestLoader()
suite  = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_utils))
suite.addTests(loader.loadTestsFromModule(test_auth))
suite.addTests(loader.loadTestsFromModule(test_cache))
suite.addTests(loader.loadTestsFromModule(test_storage))
suite.addTests(loader.loadTestsFromModule(test_storage_errors))
suite.addTests(loader.loadTestsFromModule(test_bot))
suite.addTests(loader.loadTestsFromModule(test_bot_errors))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
