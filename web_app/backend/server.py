import time
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from flask import Flask, request, jsonify
from flask.helpers import send_from_directory
from PIL import Image
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'real_vs_fake_v3_final.pth')

app = Flask(__name__, static_folder='../frontend', static_url_path='')

device = torch.device('cpu')
model = models.resnet18()
model.fc = nn.Linear(512, 1)
state_dict = torch.load(MODEL_PATH, map_location=device)
if 'model_state_dict' in state_dict:
    state_dict = state_dict['model_state_dict']
model.load_state_dict(state_dict)
model.eval()

transform = T.Compose([
    T.Resize((128, 128)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    try:
        img = Image.open(file.stream).convert('RGB')
    except Exception:
        return jsonify({'error': 'Invalid image'}), 400

    t0 = time.time()
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        logit = model(tensor)
        prob = torch.sigmoid(logit).item()

    elapsed_ms = round((time.time() - t0) * 1000)
    is_real = prob > 0.5
    confidence = prob if is_real else 1 - prob

    return jsonify({
        'prediction': 'REAL' if is_real else 'FAKE',
        'confidence': round(confidence, 4),
        'model': 'CIFake ResNet-18',
        'processing_time_ms': elapsed_ms,
    })

if __name__ == '__main__':
    app.run(port=8080, debug=False)
