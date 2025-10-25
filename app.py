from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import base64
import uuid
from werkzeug.utils import secure_filename
from model import predict_sign

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'file' not in request.files:
            return "Không có file"
        file = request.files['file']
        if file.filename == '':
            return "Chưa chọn file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Nhận diện biển báo
            result = predict_sign(filepath)

            return render_template("Result.html", filename=filename, result=result)
    return render_template("index.html")

# New endpoint to receive webcam snapshot (base64) and process it
@app.route("/upload_snapshot", methods=["POST"])
def upload_snapshot():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400

    image_data = data['image']
    # image_data expected like "data:image/png;base64,...."
    header, encoded = image_data.split(",", 1) if "," in image_data else (None, image_data)
    try:
        decoded = base64.b64decode(encoded)
    except Exception:
        return jsonify({"error": "Invalid image data"}), 400

    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, "wb") as f:
        f.write(decoded)

    result = predict_sign(filepath)
    return render_template("Result.html", filename=filename, result=result)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)
