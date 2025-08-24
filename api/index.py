from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
from tensorflow.keras.models import load_model
import os
import requests # We need this library to download the file

app = Flask(__name__)

# --- NEW CODE TO DOWNLOAD THE MODEL ---
def load_model_from_url():
    """
    Downloads the model from a URL if it's not already in the /tmp directory.
    Vercel provides a temporary writable /tmp directory.
    """
    model_path = '/tmp/brain_tumor_model.h5'
    
    # Check if the model file already exists
    if not os.path.exists(model_path):
        print("Model not found locally. Downloading from URL...")
        # Get the URL you copied from GitHub LFS
        model_url = 'https://github.com/srini526/brain-tumor-detector/raw/refs/heads/main/brain_tumor_model.h5?download=' 
        
        try:
            response = requests.get(model_url, stream=True)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Model downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading model: {e}")
            return None
    
    # Load the model from the local path
    try:
        model = load_model(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Load the model when the application starts
model = load_model_from_url()
# --- END OF NEW CODE ---


# Function to preprocess the image
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0  # Normalize to [0, 1]
    return image

# Define the home page route
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model is not loaded, please check the server logs.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file:
        try:
            image = Image.open(io.BytesIO(file.read()))
            processed_image = preprocess_image(image, target_size=(150, 150))
            
            prediction = model.predict(processed_image)
            
            result = "Tumor Detected" if prediction[0][0] > 0.5 else "No Tumor Detected"
            
            return jsonify({'prediction': result})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500