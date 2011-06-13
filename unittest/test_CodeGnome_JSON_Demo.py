#!/usr/bin/env python
# vim: tw=80 sw=4 et

import os
import sys
import unittest
from CodeGnome_JSON_Demo.CodeGnome_JSON_Demo import *

__author__    = 'Todd A. Jacobs'
__copyright__ = 'Copyright 2011, Todd A. Jacobs'
__license__   = "GPLv3"

class CodeGnome_JSON_Demo(unittest.TestCase):
    def setUp(self):
        filename = os.path.join('..', 'fixtures', 'example_data.json')
        assert os.path.isfile(filename), ( 'File missing: %s\n'
                                           'Try running this test from the the '
                                           'package\'s unittest directory.'
					   % filename )
        self.filename = filename
        self.programmer = Programmer(self.filename)

    def tearDown(self):
        pass

    """
    @unittest.expectedFailure
    def test_fail(self):
        self.assertFail()
    """

    def test_instantiate_programmer_object(self):
        programmer = Programmer()
        self.assertIsInstance(programmer, Programmer)

    def test_loading_non_json_files(self):
        with self.assertRaises(ValueError):
            programmer = Programmer('/etc/passwd')

    def test_loading_json_from_file(self):
        self.programmer = Programmer(self.filename)

    def test_load_file_returns_dictionary(self):
        self.assertIsInstance(self.programmer.attributes, dict)

    def test_output_of_present_method(self):
        """
        This test is particularly brittle, but also the most important
        behavioral test. In short, are we getting the expected output from the
        program's fixture data?
        """
        expected_result = \
"""Todd Jacobs currently works at CodeGnome Consulting, LTD. You should consider
hiring Todd because of his many sterling qualities. These include being bright,
friendly, outgoing, knowledgeable, personable, experienced, and reliable."""
        # Temporarily send standard output to the null device to avoid
        # cluttering the test results.
        sys.stdout = open(os.devnull, 'w')
        # Provide a diff in the test results between expected output and the
        # actual results. This is probably more useful than a general failure
        # message or a manual diff.
        self.assertMultiLineEqual(self.programmer.present(), expected_result)
        # This is a foolproof way to restore standard out without having to save
        # it away first. Resetting standard output is essential if one expects
        # to add more tests.
        sys.stdout = sys.__stdout__

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run individual tests with:
        #     python test_foo.py SomeTestClass.test_Something
        unittest.main()
    else:
        # Run all tests verbosely.
        suite = unittest.TestLoader().loadTestsFromTestCase(CodeGnome_JSON_Demo)
        unittest.TextTestRunner(verbosity=2).run(suite)
