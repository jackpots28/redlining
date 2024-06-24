import os
import sys
import unittest

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(project_root))

from src.embeddings_engine import gen_and_insert_embed


class TestEmbeddingGeneration(unittest.TestCase):
    def test_something(self):
        print()
