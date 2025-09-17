from flask import Flask, render_template, request, send_file
import os
from utils import process_syllabus

app = Flask(__name__)

# Configure upload & output folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Make sure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["syllabus"]
        paper_type = request.form["paper_type"]

        if file.filename != "":
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Process syllabus & generate question paper
            output_file = process_syllabus(file_path, paper_type, OUTPUT_FOLDER)

            return send_file(output_file, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)