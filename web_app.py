# Using flask as a frontend for uploading file from localhost chosen directory
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from src.processing import document_processor

import os
import logging
import docx

logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = os.path.abspath("./output_files/")
ALLOWED_EXTENSIONS = {"txt", "text", "docx", "pdf"}


def allowed_file(filename: str) -> bool:
    allowed_file_output = "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    logging.debug(f"Input allow_file filename var type: {type(filename)}")
    logging.debug(f"{allowed_file_output} - Type: {type(allowed_file_output)}")
    return allowed_file_output


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("upload.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if not "file" in request.files:
            return "No file part in the form."
        f = request.files["file"]
        if f.filename == "":
            return "No file selected."
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            # TODO - Redo this to utilize an external class object to create documents, parse, and update/save them
            doc = docx.Document(filename)
            word = request.form['text']
            doc = document_processor.split_runs(doc, word)
            doc = document_processor.style_token(doc, word, True)

            var_app_config = app.config["UPLOAD_FOLDER"]
            logging.debug(f"Output file location: {os.path.join(var_app_config, filename)}")
            doc.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return "file successfully upload"
        return "File not allowed."
    return "Upload file route"


if __name__ == "__main__":
    app.run(debug=True)
