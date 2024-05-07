# Using flask as a frontend for uploading file from localhost chosen directory
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pathlib import Path

import os, sys
import docx

# Setup for logging and root_path for referencing files/dirs consistently
project_root = os.path.realpath(os.path.join(os.path.dirname(__file__), './'))
sys.path.insert(0, os.path.abspath(project_root))

from src.processing import document_processor
from src.logger import logger
from src.logger.logger import func_log

log_path = Path(f"{project_root}/logs/web_app.log")
web_app_logger = logger.setup_logger("web_app_logger", log_path)

UPLOAD_FOLDER = Path(f"{project_root}/output_files")
ALLOWED_EXTENSIONS = {"txt", "text", "docx", "pdf"}

@func_log
def allowed_file(filename: str) -> bool:
    allowed_file_output = "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    web_app_logger.debug(f"Input allow_file filename var type: {type(filename)}")
    web_app_logger.debug(f"{allowed_file_output} - Type: {type(allowed_file_output)}")
    return allowed_file_output


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("upload.html")

# TODO - replace all references to a string filename to a Pathlib filename

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return "No file part in the form."
        f = request.files["file"]
        if f.filename == "":
            return "No file selected."
        if f and allowed_file(f.filename):
            filename = secure_filename(str(f.filename))
            # TODO - Redo this to utilize an external class object to create documents, parse, and update/save them
            doc = docx.Document(filename)
            word = request.form['text']
            doc = document_processor.split_runs(doc, word)
            doc = document_processor.style_token(doc, word, True)

            # Live testing doc_to_dict function
            test_dict = document_processor.doc_to_dict(doc)
            web_app_logger.debug(f"{ {k:v for (k,v) in test_dict.items()} }")

            var_app_config = app.config["UPLOAD_FOLDER"]
            web_app_logger.debug(f"Output file location: {os.path.join(var_app_config, filename)}")
            doc.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "file successfully upload"
        return "File not allowed."
    return "Upload file route"


if __name__ == "__main__":
    app.run(debug=True)
