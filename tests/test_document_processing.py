from pathlib import Path
from docx.document import Document
from docx.enum.text import WD_COLOR_INDEX

import unittest
import docx
import os, sys, string

# Root directory to repo prep - addition to os path for python
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

# Sourcing internal packages
from src.logger import logger
from src.processing import document_processor

class TestDocumentProcessor(unittest.TestCase):
    # 
    def test_splitting_sentences_to_list(self):
        test_sentence = "This is a test sentence."
        result = document_processor.split_sentence_to_list(test_sentence)
        self.assertEqual(result, ["This", "is", "a", "test", "sentence."])

    # 
    def test_doc_to_dict(self):
        test_doc_path = Path(f"{project_root}/word_doc_test.docx")
        test_doc = docx.Document(str(test_doc_path))
        test_dict = document_processor.doc_to_dict(test_doc)
        self.assertIsInstance(test_dict, dict)

if __name__ == '__main__':
    unittest.main()
