### Break on '.' then iterate over a variable 'n' for breaking sentence into sub-phrases

"""
Assumptions:

.) list of len(n) "phrases"
.) break "paragraph" on sentence - e.g. '.'
    - the idea is, the known phrases won't overlap sentence length - thus will only be found per sentence
.) based on len(list(sentences)[x]) iter over broken paragraphs in contexts windows of len(list(sentences)[x]) +/- [0..3]
    - create embeddings per each permutation of above
"""

import os, sys, tempfile, pathlib

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, os.path.abspath(project_root))


list_of_sentence = ["Sample sentence 1 plus some padding",
                    "Sample sentence 2 less padding",
                    "Sample sentence 3 all the padding you want",
                    "Sample sentence 3 nothing"]





def main():
    return None



if __name__ == '__main__':
    main()