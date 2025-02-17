import io
import json
import base64
from functools import lru_cache
import numpy as np
from PIL import Image
import onnxruntime as ort
from flask import Flask, request, jsonify

app = Flask(__name__)
MODEL = ort.InferenceSession('./emotion-ferplus.onnx')
EMOTIONS = ['neutral', 'happiness', 'surprise', 'sadness', 'anger', 'disgust', 'fear', 'contempt']

@lru_cache
def get_image_str(file):
    img_bytes = io.BytesIO()
    img = Image.open(file)
    img.save(img_bytes, 'PNG')
    base64_string = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return base64_string

@lru_cache
def get_image_arr(file):
    input_shape = (1, 1, 64, 64) 
    img = Image.open(file).convert('L') 
    img = img.resize((64, 64), Image.Resampling.LANCZOS)
    img_data = np.array(img)
    img_data = img_data.astype(np.float32) / 255.0
    img_data = np.reshape(img_data, input_shape)
    return img_data
  
def predict(model, processed_image):
    input_name = model.get_inputs()[0].name
    result = model.run(None, {input_name: processed_image})
    return result

def softmax(scores):
    arr = np.array(scores)
    C = np.max(arr)
    exp_values = np.exp(arr - C)
    d = np.sum(exp_values)
    return exp_values / d

def analyze(session, preprocessed_img):
    inference = predict(session, preprocessed_img)
    prob = softmax(inference)
    prob = np.squeeze(prob)
    classes = np.argsort(prob)[::-1]
    return {'principal_emotion':EMOTIONS[classes[0]]}

@app.route('/classify', methods=['POST'])
def classify():
    file = request.files['image']
    try:
        preprocessed_img = get_image_arr(file)
        base64_img = get_image_str(file)
        analysis = analyze(MODEL, preprocessed_img)
        return json.dumps({'inference': analysis, 'src_png': base64_img}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
