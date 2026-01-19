
# 🌿 Plant Disease Detection

A beginner-friendly web application that detects plant diseases from leaf images using Flask.

## ✨ Features

- 🖼️ Easy image upload (drag & drop)
- 🤖 AI-powered disease detection
- 📊 Visual confidence scores
- 🎨 Beautiful, modern UI

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If TensorFlow installation fails (Python 3.14), that's OK! The app works without it using mock predictions.

### 2. Run the App

```bash
python app.py
```

### 3. Open Browser

Go to: **http://localhost:5000**

That's it! 🎉

**Note:** The app uses mock predictions for demonstration. To use a real model, train one and save it as `models/plant_disease_model.h5`

## 🚀 Running the Application

### Start the Flask Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

### Open in Browser

Open your web browser and go to:
```
http://localhost:5000
```

## 📁 Project Structure

```
plant_Diease/
├── app.py              # Flask application
├── wsgi.py             # Production WSGI entry
├── requirements.txt    # Dependencies
├── Procfile           # Heroku deployment
├── runtime.txt        # Python version
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── models/            # ML models (auto-created)
└── uploads/           # Uploads (auto-created)
```

## 🎯 How to Use

1. **Upload an Image**
   - Click the upload box or drag & drop an image
   - Supported formats: PNG, JPG, JPEG, GIF, BMP
   - Max file size: 16MB

2. **Get Prediction**
   - Click "🔍 Detect Disease" button
   - Wait for the AI to analyze the image
   - View the results with confidence score

3. **Try Another**
   - Click "🔄 Analyze Another Image" to reset

## 🔧 Configuration

**Change Port:**
```bash
# Set environment variable
$env:PORT=8080  # Windows PowerShell
python app.py
```

**Production Mode:**
The app uses `gunicorn` for production. See `Procfile` for configuration.

## 🐛 Troubleshooting

**Port in use?** Use a different port: `$env:PORT=8080`

**TensorFlow error?** That's OK! The app works without TensorFlow.

**Import errors?** Make sure dependencies are installed: `pip install -r requirements.txt`

## 🚢 Deployment

Ready to deploy! The project includes:
- `Procfile` for Heroku
- `wsgi.py` for production servers
- `runtime.txt` for Python version

Deploy to Heroku, Railway, Render, or any WSGI-compatible platform.

---

**Made with ❤️ for beginners**
#
