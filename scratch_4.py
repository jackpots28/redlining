### TESTING SPIRE.DOC by https://www.e-iceblue.com/

from spire.doc import *
from spire.doc.common import *


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
document.SaveToFile("./output_files/ReplaceTextUsingRegexPattern.docx", FileFormat.Docx2016)
document.Close()



