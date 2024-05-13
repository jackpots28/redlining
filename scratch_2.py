import docx
from docx.document import Document
from docx.shared import RGBColor, Pt
from docx.enum.text import WD_COLOR_INDEX

import os, sys
from pathlib import Path


def highlight_word_in_paragraphs(doc: Document, output_docx_path, word_to_highlight, highlight_color=RGBColor(255, 255, 0)):
    """
    Highlight a specific word in individual paragraphs found in a DOCX document.

    Args:
    - input_docx_path: The path to the input DOCX document.
    - output_docx_path: The path to the output DOCX document with highlighted word.
    - word_to_highlight: The word to highlight in the document.
    - highlight_color: The color to use for highlighting. Default is yellow.
    """

    # Loop through all paragraphs in the document
    for paragraph in doc.paragraphs:
        # Check if the word to highlight is present in the paragraph
        if word_to_highlight in paragraph.text:
            # Loop through each run in the paragraph

            for run in paragraph.runs:
                # Find the position of the word to highlight in the run's text
                start_index = run.text.find(word_to_highlight)
                if start_index != -1:
                    print(start_index)
                    # Add highlighting to the run's text containing the word
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW

    # Save the modified document
    doc.save(output_docx_path)

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(project_root))

test_doc_path = Path("./word_doc_test.docx")
output_doc_path = Path("./output_files/test_doc.docx")

word_to_highlight = "ipsum"
test_doc = docx.Document(test_doc_path)

highlight_word_in_paragraphs(test_doc, output_doc_path, word_to_highlight)



