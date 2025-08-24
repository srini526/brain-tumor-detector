# app.py

from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
from tensorflow.keras.models import load_model

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = load_model('brain_tumor_model.h5')
print("Model loaded. Check http://127.0.0.1:5000/")

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
    # Render the HTML file for the frontend
    return render_template('index.html')

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    if file:
        try:
            # Open and preprocess the image
            image = Image.open(io.BytesIO(file.read()))
            processed_image = preprocess_image(image, target_size=(150, 150))
            
            # Make a prediction
            prediction = model.predict(processed_image)
            
            # Interpret the prediction
            # The output is a probability. > 0.5 means 'yes', <= 0.5 means 'no'.
            if prediction[0][0] > 0.5:
                result = "Tumor Detected"
            else:
                result = "No Tumor Detected"
            
            return jsonify({'prediction': result})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Run the app
# if __name__ == '__main__':
#     app.run(debug=True)