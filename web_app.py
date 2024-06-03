# Using flask as a frontend for uploading file from localhost chosen directory
# Sourcing global packages
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pathlib import Path

import os, sys
import docx

# Setup root_path for referencing files/dirs consistently
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), './'))
sys.path.insert(0, os.path.abspath(project_root))

# Sourcing internal packages
from src.processing import document_processor
from src.logger import logger
from src.logger.logger import func_log
from src.file_transactions import file_handler

from src.processing.spire_processing import spire_replace_phrase

# Setup Logging
log_path = Path(f"{project_root}/logs/web_app.log")
web_app_logger = logger.setup_logger("web_app_logger", log_path)

UPLOAD_FOLDER = Path(f"{project_root}/output_files")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("upload.html")


# TODO - replace all references to a string filename to a Pathlib filename

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        web_app_logger.debug(f"Contents of request.files: {request.files}")
        if "file" not in request.files:
            return "No file in the form."
        f = request.files["file"]
        if f.filename == "":
            return "No file selected."

        web_app_logger.debug(f"Paths in request.file array: {f}")
        if f and file_handler.allowed_file(f.filename):
            filename = secure_filename(str(f.filename))
            ingest_file = Path(filename)
            web_app_logger.debug(f"secure_filename contents: {filename}")
            # TODO - Redo this to utilize an external class object to create documents, parse, and update/save them
            # doc = docx.Document(filename)

            word = request.form['text']
            replacement_text = f"WEBAPP TEST PHRASE REPLACEMENT"

            # doc = document_processor.split_runs(doc, word)
            # doc = document_processor.style_token(doc, word, True)

            formated_output_doc = spire_replace_phrase(ingest_file, app.config["UPLOAD_FOLDER"], word, replacement_text)

            # Live testing doc_to_dict function
            # test_dict = document_processor.doc_to_dict(doc)
            # web_app_logger.debug(f"{ {k: v for (k, v) in test_dict.items()} }")

            var_app_config = app.config["UPLOAD_FOLDER"]
            web_app_logger.debug(f"Output file location: {os.path.join(var_app_config, filename)}")
            # doc.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "file successfully upload"
        return "File not allowed."
    return "Upload file route"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
