from pathlib import Path
from werkzeug.utils import secure_filename

import os, sys

'''
TODO - need to start writing this file handler for sanitization 
and verification of file paths / data ingestion typing
'''

ALLOWED_EXTENSIONS = {"doc", "docx"}

# Setup root_path for referencing files/dirs consistently
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, os.path.abspath(project_root))

# Sourcing internal packages
from src.logger import logger
from src.logger.logger import func_log

# Setup Logging
log_path = Path(f"{project_root}/logs/file_handler.log")
file_handler_logger = logger.setup_logger("file_handler_logger", log_path)


@func_log
def allowed_file(filename: str) -> bool:
    allowed_file_output = "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    file_handler_logger.debug(f"Input allow_file filename var type: {type(filename)}")
    file_handler_logger.debug(f"{allowed_file_output} - Type: {type(allowed_file_output)}")
    return allowed_file_output