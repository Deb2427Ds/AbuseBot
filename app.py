# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Dummy logic — replace with your model
            if "abuse" in file.filename.lower():
                result = "Abusive content detected"
            else:
                result = "No abuse detected"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
