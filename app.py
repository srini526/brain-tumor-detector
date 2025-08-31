# app.py
from flask import Flask, request, jsonify, render_template
import numpy as np
from PIL import Image
import io
from tensorflow.keras.models import load_model

# --- CORRECTED CLASS NAMES (MUST BE ALPHABETICAL) ---
CLASS_NAMES = ['glioma', 'meningioma', 'notumor', 'pituitary']

CONFIDENCE_THRESHOLD = 0.5

app = Flask(__name__)

try:
    model = load_model('multiclass_brain_tumor_model_v2.h5')
    print("Multiclass model loaded successfully!")
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
        return jsonify({'error': 'Model could not be loaded.'}), 500
    
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file part in the request'}), 400
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400
    
    try:
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image, target_size=(150, 150))
        
        prediction = model.predict(processed_image)
        
        predicted_class_index = np.argmax(prediction)
        confidence = np.max(prediction)

        # This print statement is your best friend for debugging.
        # It shows the raw probabilities for each class.
        print(f"DEBUG: Raw Prediction Array: {prediction}")
        print(f"DEBUG: Predicted Index: {predicted_class_index}, Confidence: {confidence:.4f}")

        if confidence < CONFIDENCE_THRESHOLD:
            result = "Invalid Input File: Please upload a brain MRI scan."
        else:
            predicted_class_name = CLASS_NAMES[predicted_class_index]
            
            if predicted_class_name == 'notumor':
                result = "No Tumor Detected"
            else:
                tumor_type = predicted_class_name.capitalize()
                result = f"Tumor Detected. Type: {tumor_type}"
        
        return jsonify({'prediction': result})
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'prediction': 'Invalid Input File: Not a valid image.'})

if __name__ == '__main__':
    print("Starting Flask server... Go to http://127.0.0.1:5000/")
    app.run(debug=True)
    # to run venv\Scripts\activate
    # python app.py