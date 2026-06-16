import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    from tests.test_student import TestStudent
    from tests.test_student_list import TestStudentList
    from tests.test_validator import TestValidator
    from tests.test_api import TestAPI
    from tests.test_json_storage import TestJSONStorage

    suite.addTests(loader.loadTestsFromTestCase(TestStudent))
    suite.addTests(loader.loadTestsFromTestCase(TestStudentList))
    suite.addTests(loader.loadTestsFromTestCase(TestValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONStorage))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"{'='*50}")

    sys.exit(0 if result.wasSuccessful() else 1)
