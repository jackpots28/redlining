from pathlib import Path

import unittest
import os, sys

# Root directory to repo prep - addition to os path for python
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

from src.logger import logger
from src.processing import spire_processing

ingest_file = Path(f"../word_doc_test.docx")
output_files_dest = Path(f"../output_files/")


class TestSpireProcessing(unittest.TestCase):
    def test_redlining(self):
        test_file = spire_processing.spire_replace_phrase(ingest_file, output_files_dest, "ipsum", "TEST_TEST_TEST")

        self.assertIsNotNone(test_file, Path())
        self.assertTrue(Path(test_file).exists())

        # Cleanup output file
        os.remove(test_file)


if __name__ == '__main__':
    unittest.main()
