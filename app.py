from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import json
import uuid
import os
import base64

app = Flask(__name__)
CORS(app)

# Create directories
os.makedirs('uploadimages', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Load model and labels
model = None
label = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
         'Background_without_leaves', 'Blueberry___healthy', 'Cherry___Powdery_mildew', 'Cherry___healthy',
         'Corn___Cercospora_leaf_spot Gray_leaf_spot', 'Corn___Common_rust', 'Corn___Northern_Leaf_Blight', 'Corn___healthy',
         'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
         'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
         'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
         'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy',
         'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
         'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
         'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Load disease info
try:
    with open("plant_disease.json", 'r') as f:
        plant_disease = json.load(f)
except:
    plant_disease = []

# Load TensorFlow model
try:
    import tensorflow as tf
    model = tf.keras.models.load_model("models/plant_disease_recog_model_pwp.keras")
    print("✅ Model loaded!")
except:
    print("⚠️ Model not found. Install TensorFlow to use real predictions.")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'model': 'loaded' if model else 'mock'})

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Save file
    filename = f"uploadimages/temp_{uuid.uuid4().hex}_{file.filename}"
    file.save(filename)
    
    # Predict
    try:
        if model is None:
            return jsonify({'success': False, 'error': 'Model not loaded. Please install TensorFlow.'}), 500
        
        # Process image
        img = tf.keras.utils.load_img(filename, target_size=(160, 160))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.array([img_array])
        
        # Predict
        prediction = model.predict(img_array, verbose=0)
        class_idx = prediction.argmax()
        confidence = float(prediction[0][class_idx] * 100)
        disease_name = label[class_idx]
        
        # Check if valid leaf (not background)
        if 'Background_without_leaves' in disease_name or confidence < 30:
            os.remove(filename)
            return jsonify({'success': False, 'error': 'Please upload a clear image of a plant leaf'}), 400
        
        # Get disease info
        disease_info = next((item for item in plant_disease if item["name"] == disease_name), {})
        
        # Read image for response
        file.seek(0)
        image_base64 = base64.b64encode(file.read()).decode('utf-8')
        
        # Format disease name
        disease_display = disease_name.replace("___", " - ").replace("_", " ")
        
        # Clean up
        os.remove(filename)
        
        return jsonify({
            'success': True,
            'disease': disease_display,
            'confidence': round(confidence, 2),
            'image': f'data:image/jpeg;base64,{image_base64}'
        })
        
    except Exception as e:
        try:
            os.remove(filename)
        except:
            pass
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
