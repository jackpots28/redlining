# Using python-docx for editing
import docx
from docx import Document
from docx.enum.text import WD_COLOR_INDEX

from pathlib import Path
import os

test_doc_path = Path("./word_doc_test.docx")
output_doc_path = Path("./uploads/output_doc.docx")


print(f"Is the test file path correct: {test_doc_path.is_file()}", end="\n")
print(f"docx version: {docx.__version__}", end="\n\n")


doc = Document(test_doc_path)

old_list = list()
new_list = list()

# Can Highlight text
# for par in doc.paragraphs:
#     for run in par.runs:
#         if 'ultricies' in run.text:
#             x = run.text.split('ultricies')
#             run.clear()
#             for i in range(len(x)):
#                 print(x[i])
#                 print("CHANGED")
#                 # run.add_text(x[i])
#                 # run.add_text('ultricies')
#                 # run.font.highlight_color = WD_COLOR_INDEX.YELLOW
#                 # run.font.strike = True

# Remove full paragraphs
# def delete_paragraph(paragraph):
#     p = paragraph._element
#     p.getparent().remove(p)
#     p._p = p._element = None

# Create list with single word changed
for paragraph in doc.paragraphs:
    if 'lorem' in paragraph.text:
        for run in paragraph.runs:
            if 'lorem' in run.text:
                x = run.text.split('lorem')
                run.clear()
                print(x)
                for i in range(len(x)-1):
                    run.add_text(x[i])
                    run.add_text('lorem')
                    run.font.highlight_color = WD_COLOR_INDEX.YELLOW

    # new_list.append((par.text).replace("ultricies", "CHANGED"))

for item in new_list:
    print(item)

# Clear out working doc
# for par in doc.paragraphs:
#     delete_paragraph(par)

# Fill it with new list of paragraphs with the modifications
# for item in new_list:
#     doc.add_paragraph().add_run(str(item))

# Save it to a new file
doc.save(output_doc_path)
