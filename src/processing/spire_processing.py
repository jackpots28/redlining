import os
import string
import sys
from pathlib import Path
from typing import Any

import tempfile

from spire.doc import *
from spire.doc.common import *

# Setup root_path for referencing files/dirs consistently
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(project_root))

# Sourcing internal packages
# from src.logger import logger
# from src.logger.logger import func_log

# from src.file_transactions.file_handler import create_temp_file

# Setup Logging
# log_path = Path(f"{project_root}/logs/spire_document_processing.log")
# spire_processing_logger = logger.setup_logger("spire_document_processing_logger", log_path)

'''
spire.doc based functions 
'''


# Note - Not sure if I wanna return the document itself or how it is currently as a path object
def spire_replace_phrase(ingest_document_path: Path, output_dir: Path, search_phrase: str, repl_text: str, ) -> Path:
    output_file = tempfile.NamedTemporaryFile(prefix=f"{ingest_document_path.stem}_",
                                                   suffix=".docx",
                                                   dir=f"{output_dir}",
                                                   delete=False, )

    # This was buggy and creating a duplicate output file in scratches dir
    # output_file = create_temp_file(output_dir, ingest_document_path, )

    document = Document()
    document.LoadFromFile(f"{ingest_document_path}")

    # Produce temp-file that includes the original filename as a prefix

    regex = Regex(f"{search_phrase}")
    document.Replace(regex, f"{search_phrase} {repl_text}")

    # Apply strikethrough and highlighting to regex'd phrase
    text_selections = document.FindAllString(search_phrase, caseSensitive=False, wholeWord=True, )
    for selection in text_selections:
        text_range = selection.GetAsOneRange()
        text_range.CharacterFormat.HighlightColor = Color.get_Red()
        text_range.CharacterFormat.IsStrikeout = True

    # spire_processing_logger.debug(f"{output_file}\n{output_file.name}")
    document.SaveToFile(output_file.name, FileFormat.Docx2016)
    document.Close()

    return Path(output_file.name)


'''
Note - scratch_6 is testing the functionality of using file-handler.py creating the temp file used for output
func_log was duplicating output temp file creation and currently scratch_6 is buggy with creating an output file in:
output_files dir and scratches dir
'''
