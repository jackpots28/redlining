import os
import pathlib
import sys

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

from src.processing.spire_processing import spire_replace_phrase


test_doc = pathlib.Path(f"{project_root}/word_doc_test.docx")
output_dir = pathlib.Path(f"{project_root}/output_files/")

test_output = spire_replace_phrase(test_doc, output_dir, "ipsum", "TEST_TEST_TEST")
