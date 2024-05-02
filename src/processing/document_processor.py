from pathlib import Path
from docx.enum.text import WD_COLOR_INDEX
from src.logger import logger
from pathlib import Path

import docx
import re
import os

log_path = Path("./logs/document_processing.log")
document_processing_logger = logger.setup_logger("document_processing_logger", log_path)


def split_sentence_to_list(text: str) -> list:
    output_list = list()
    output_list = text.split(" ")
    document_processing_logger.debug(f"Split sentence buffer: {output_list}")
    return output_list


# Creates a set of "virtual" runs that the "style_token" func loops through
# to apply formatting based on if keyword is found in list of runs
def split_runs(doc: docx.Document, word: str) -> docx.Document:
    for p in doc.paragraphs:
        document_processing_logger.debug(f"Boolean value if word is found: {p.text.find(word)}")
        if p.text.find(word) != -1:
            DEBUGGING_OUTPUT_TEXT = p.text
            document_processing_logger.debug(f"Text buffer as of found: {word}:\n{DEBUGGING_OUTPUT_TEXT}")
            virtual_runs = p.runs
            p.text = ""
            for r in virtual_runs:
                if r.text.find(word) != -1:
                    broken_sentence = split_sentence_to_list(r.text)
                    for word in broken_sentence:
                        p.add_run(word)
                        p.add_run(" ")
    return doc


# Loops over doc "runs" and applies text formatting only to "keywords" that are found
def style_token(doc: docx.Document, word: str, comment=True) -> docx.Document:
    for p in doc.paragraphs:
        for i, r in enumerate(p.runs):
            if p.runs[i].text.find(word) != -1:
                p.runs[i].font.highlight_color = WD_COLOR_INDEX.RED
                p.runs[i].font.strike = True
    return doc

# words = ['ipsum']

# for word in words:
#     doc = split_Runs(doc, word)

# for word in words:
#     doc = style_Token(doc,word,True)

#nums is the list of tokens that is going to be highlighted and comment
# nums=['vulputate ']
# for num in nums:
#     doc=split_Runs(doc,num)
# for num in nums:
#     doc=style_Token(doc,num,True)

# doc.save(output_doc_path)
