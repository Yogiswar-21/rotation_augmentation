# Dark Circles Detection API

A FastAPI-based REST API for detecting dark circles in images using YOLO model.

## Features

- Accepts image uploads via POST request
- Captures images from webcam using OpenCV
- Uses YOLO model to predict dark circle severity
- Returns prediction with causes and remedies
- Automatic model file detection

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python main.py
```
or
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. API Documentation:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Endpoints

### GET `/`
Root endpoint with API information

### GET `/health`
Health check endpoint

### POST `/predict`
Upload an image to detect dark circles

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "success": true,
  "prediction": "High",
  "class_name": "High",
  "causes": "Lack of sleep, dehydration, genetics, stress.",
  "remedies": "• Sleep at least 7-8 hours\n• Stay hydrated\n• Use under-eye creams\n• Manage stress\n• Reduce screen time",
  "confidence": 0.85
}
```

### POST `/predict/camera`
Capture an image from webcam and detect dark circles

**Request:**
- Method: POST
- Query Parameter: `camera_index` (optional, default: 0) - Camera device index

**Response:**
```json
{
  "success": true,
  "prediction": "Moderate",
  "class_name": "Moderate",
  "causes": "Mild sleep issues, stress, slight dehydration.",
  "remedies": "• Improve sleep routine\n• Drink more water\n• Gentle eye massage\n• Cold compress therapy",
  "confidence": 0.72
}
```

## Example Usage

### Using curl:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

### Using Python requests:
```python
import requests

# Upload image
url = "http://localhost:8000/predict"
with open("image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    print(response.json())

# Capture from camera
url = "http://localhost:8000/predict/camera"
response = requests.post(url, params={"camera_index": 0})
print(response.json())
```

### Using curl for camera:
```bash
curl -X POST "http://localhost:8000/predict/camera?camera_index=0" \
  -H "accept: application/json"
```

## Model

The API automatically detects and loads the `best*.pt` model file from the current directory.

