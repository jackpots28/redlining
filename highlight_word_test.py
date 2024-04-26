import docx
import re
from docx.enum.text import WD_COLOR_INDEX

from pathlib import Path
import os

test_doc_path = Path("./word_doc_test.docx")
output_doc_path = Path("./uploads/output_doc.docx")

doc=docx.Document(test_doc_path)

def split_text(text, word):
    pattern = re.compile(r'([\S\s]*)(\b{})([\S\s]*)'.format(word))
    match = pattern.search(text)
    if match:
        return match.groups()
    return None
def split_Runs(doc,word):
    for p in doc.paragraphs:
        if p.text.find(word) != -1:
            virtualRuns=p.runs
            p.text = ""
            for r in virtualRuns:
                if r.text.find(word) != -1:
                    before, word, after = split_text(r.text, word)
                    p.add_run(before)
                    p.add_run()
                    p.add_run(word)
                    p.add_run(after)
                else:
                    p.add_run(r.text)
    return doc
    
def style_Token(doc,word,comment=True):
    for p in doc.paragraphs:
        for i,r in enumerate(p.runs):
            if p.runs[i].text.find(word) != -1:
                p.runs[i].font.highlight_color = WD_COLOR_INDEX.RED
                p.runs[i].font.strike=True
    return doc

#nums is the list of tokens that is going to be highlighted and comment
nums=['Lorem']
for num in nums:
    doc=split_Runs(doc,num)
for num in nums:
    doc=style_Token(doc,num,True)

doc.save(output_doc_path)