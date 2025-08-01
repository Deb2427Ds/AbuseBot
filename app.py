from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data_url = request.json['image']
    header, encoded = data_url.split(",", 1)
    image_data = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_data))
    image = np.array(image.convert('RGB'))

    try:
        result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except Exception as e:
        emotion = "Error"

    return jsonify({'emotion': emotion})

if __name__ == '__main__':
    app.run(debug=True)
