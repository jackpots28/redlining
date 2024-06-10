from pathlib import Path

import unittest
import docx
import os, sys, string

# Root directory to repo prep - addition to os path for python
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

# Sourcing internal packages
from src.file_transactions import file_handler

class TestFileHandler(unittest.TestCase):

    #
    def test_allowed_file(self):
        allowed_test_file_name = "/test/path/example.docx"
        unpermitted_test_file_name = "/test/path/example.pdf"
        allowed_result = file_handler.allowed_file(allowed_test_file_name)
        unpermitted_result = file_handler.allowed_file(unpermitted_test_file_name)
        self.assertTrue(allowed_result)
        self.assertFalse(unpermitted_result)



if __name__ == '__main__':
    unittest.main()