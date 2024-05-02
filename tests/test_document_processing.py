from src.processing import document_processor
from pathlib import Path
from src.logger import logger

from docx import Document
from docx.enum.text import WD_COLOR_INDEX

import unittest
import docx


class TestDocumentProcessor(unittest.TestCase):
    def test_splitting_sentences_to_list(self):
        test_sentence = "This is a test sentence."
        result = document_processor.split_sentence_to_list(test_sentence)
        self.assertEqual(result, ["This", "is", "a", "test", "sentence."])


if __name__ == '__main__':
    unittest.main()
