from pathlib import Path
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

import unittest
import docx
import os, sys

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

from src.logger import logger
from src.processing import document_processor

class TestDocumentProcessor(unittest.TestCase):
    def test_splitting_sentences_to_list(self):
        test_sentence = "This is a test sentence."
        result = document_processor.split_sentence_to_list(test_sentence)
        self.assertEqual(result, ["This", "is", "a", "test", "sentence."])


if __name__ == '__main__':
    unittest.main()
