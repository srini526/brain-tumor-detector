# app.py

from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
from tensorflow.keras.models import load_model

# --- NEW, SMARTER THRESHOLDS ---
# We will only consider an image invalid if the prediction is in a very tight
# "total confusion" zone around 0.5. This is much more reliable.
UNCERTAINTY_ZONE_LOWER = 0.40
UNCERTAINTY_ZONE_UPPER = 0.60

app = Flask(__name__)

try:
    model = load_model('brain_tumor_model.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = np.array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    return image

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model could not be loaded. Check server logs.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file:
        try:
            image = Image.open(io.BytesIO(file.read()))
            processed_image = preprocess_image(image, target_size=(150, 150))
            
            prediction_probability = model.predict(processed_image)[0][0]
            
            # --- IMPORTANT: DEBUGGING PRINTOUT ---
            # This will show you the model's raw output in the terminal.
            print(f"DEBUG: Raw prediction probability is: {prediction_probability}")
            
            # --- NEW, IMPROVED LOGIC ---
            if UNCERTAINTY_ZONE_LOWER < prediction_probability < UNCERTAINTY_ZONE_UPPER:
                # If the prediction is in the "total confusion" zone.
                result = "Invalid Input File: Please upload a brain MRI scan."
            else:
                # Otherwise, the model is confident enough that it's an MRI.
                # Now we can classify it.
                result = "Tumor Detected" if prediction_probability > 0.5 else "No Tumor Detected"
            
            return jsonify({'prediction': result})
        
        except Exception as e:
            return jsonify({'prediction': 'Invalid Input File: Not a valid image.'})

if __name__ == '__main__':
    print("Starting Flask server... Go to http://127.0.0.1:5000/")
    app.run(debug=True)
    # to run venv\Scripts\activate
    # python app.py