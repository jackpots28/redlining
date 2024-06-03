### TESTING SPIRE.DOC by https://www.e-iceblue.com/
### This example works

from spire.doc import *
from spire.doc.common import *

import os, sys, tempfile, pathlib

project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, os.path.abspath(project_root))


output_files_dest = pathlib.Path(f"../output_files/")
temp = tempfile.NamedTemporaryFile(prefix='test_',
                                   suffix='.docx',
                                   dir=f"{output_files_dest}",
                                   delete=False)

# Create a Document object
document = Document()
# Load a Word docx or doc document
document.LoadFromFile("word_doc_test.docx")

search_word="ipsum"
textSelections = document.FindAllString(search_word, False, True)
regex = Regex(f"{search_word}")

# Replace the matched text with another text
document.Replace(regex, f"{search_word} SOMETHING")

for selection in textSelections:
    # Get the current instance as a single text range
    textRange = selection.GetAsOneRange()
    # Highlight the text range with a color
    textRange.CharacterFormat.HighlightColor = Color.get_Red()
    textRange.CharacterFormat.IsStrikeout = True

# Save the resulting document
document.SaveToFile(temp.name, FileFormat.Docx2016)
document.Close()

# TODO - Move this to a function module to be used inside web_app.py for editing ingested documents



