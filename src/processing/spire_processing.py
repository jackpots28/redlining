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
from src.logger import logger
from src.logger.logger import func_log

# Setup Logging
log_path = Path(f"{project_root}/logs/spire_document_processing.log")
document_processing_logger = logger.setup_logger("spire_document_processing_logger", log_path)

'''
spire.doc based functions 
'''

# Note - Not sure if I wanna return the document itself or how it is currently as a path object
@func_log
def spire_replace_phrase(ingest_document_path: Path, output_dir: Path, search_phrase: str, repl_text: str,) -> Path:
    document = Document()
    document.LoadFromFile(f"{ingest_document_path}")

    ### Produce temp-file that includes the original filename as a prefix
    output_file_name = tempfile.NamedTemporaryFile(prefix=f"{ingest_document_path.stem}_",
                                                   suffix=".docx",
                                                   dir=f"{output_dir}",
                                                   delete=False,)

    text_selections = document.FindAllString(search_phrase, caseSensitive=False, wholeWord=True,)
    regex = Regex(f"{search_phrase}")
    document.Replace(regex, f"{search_phrase} {repl_text}")

    ### Apply strikethrough and highlighting to regex'd phrase
    for selection in text_selections:
        text_range = selection.GetAsOneRange()
        text_range.CharacterFormat.HighlightColor = Color.get_Red()
        text_range.CharacterFormat.IsStrikeout = True


    document.SaveToFile(output_file_name.name, FileFormat.Docx2016)
    document.Close()

    return Path(output_file_name.name)