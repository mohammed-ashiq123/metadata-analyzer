from flask import Flask, render_template, request
from PIL import Image
from PIL.ExifTags import TAGS
import hashlib
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    metadata = {}
    sha256_hash = ""

    if request.method == "POST":
        file = request.files["image"]

        if file:
            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                file.filename
            )

            file.save(filepath)

            sha256 = hashlib.sha256()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)

            sha256_hash = sha256.hexdigest()

            image = Image.open(filepath)
            exif = image.getexif()

            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = value

    return render_template(
        "index.html",
        metadata=metadata,
        sha256_hash=sha256_hash
    )

if __name__ == "__main__":
    app.run(debug=True)
