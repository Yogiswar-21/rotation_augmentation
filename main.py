from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import os
import cv2
import numpy as np
import torch

app = FastAPI(title="Dark Circles Detection API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global variables for model
model = None
model_path = None

# Find the best.pt file in the current directory
def find_best_model():
    """Find the best.pt model file in the current directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Look for files matching best*.pt pattern
    pt_files = [f for f in os.listdir(current_dir) if f.endswith('.pt') and 'best' in f.lower()]
    
    if not pt_files:
        raise FileNotFoundError("No best.pt file found in the current directory")
    
    # Use the first found file (or you can sort to get the latest)
    model_path = os.path.join(current_dir, pt_files[0])
    return model_path

@app.on_event("startup")
async def load_model():
    """Load the YOLO model on application startup"""
    global model, model_path
    try:
        model_path = find_best_model()
        print(f"Attempting to load model from: {model_path}")
        
        # Try loading with YOLO - handle PyTorch 2.6+ security restrictions
        try:
            # Add safe globals for ultralytics classes to handle PyTorch 2.6+ security
            torch.serialization.add_safe_globals([
                'ultralytics.nn.tasks.DetectionModel',
                'ultralytics.nn.modules.head.Detect',
                'ultralytics.nn.modules.conv.Conv',
                'ultralytics.nn.modules.block.C2f',
                'ultralytics.nn.modules.block.SPPF',
                'torch.nn.modules.upsampling.Upsample',
                'torch.nn.modules.pooling.AdaptiveAvgPool2d',
                'torch.nn.modules.activation.SiLU'
            ])
            
            model = YOLO(model_path)
            print(f"✅ Model loaded successfully from: {model_path}")
        except (ModuleNotFoundError, AttributeError) as e:
            error_msg = str(e)
            print(f"\n❌ Version compatibility error: {error_msg}")
            print("\nPossible solutions:")
            print("1. The model was saved with a different ultralytics version")
            print("2. Try reinstalling ultralytics: pip install --upgrade --force-reinstall ultralytics")
            print("3. Or re-export the model with the current ultralytics version")
            print("4. Check if you need to use a specific ultralytics version")
            model = None  # Set to None so endpoints can handle gracefully
        except Exception as e:
            # If the safe globals approach doesn't work, try with weights_only=False
            error_msg = str(e)
            if "weights_only" in error_msg or "WeightsUnpickler" in error_msg:
                print(f"⚠️  PyTorch security restriction detected. Attempting alternative loading...")
                try:
                    # This is less secure but may be necessary for older model files
                    import warnings
                    warnings.filterwarnings("ignore", category=UserWarning, message=".*weights_only.*")
                    
                    # Try to load with weights_only=False (less secure but may work)
                    # Note: This requires modifying how YOLO loads the model internally
                    # For now, we'll provide clear instructions to the user
                    print(f"❌ Model loading failed due to PyTorch 2.6+ security restrictions")
                    print(f"Error: {error_msg}")
                    print("\n🔧 Solutions:")
                    print("1. Re-train/export your model with the current ultralytics version")
                    print("2. Or downgrade PyTorch: pip install 'torch<2.6'")
                    print("3. Or use an older ultralytics version compatible with your model")
                    model = None
                except Exception as e2:
                    print(f"❌ Alternative loading also failed: {str(e2)}")
                    model = None
            else:
                print(f"❌ Unexpected error loading model: {error_msg}")
                model = None
    except FileNotFoundError as e:
        print(f"❌ Model file not found: {str(e)}")
        model = None
    except Exception as e:
        print(f"❌ Unexpected error loading model: {str(e)}")
        model = None

# Define advice based on prediction
advice_dict = {
    'High': {
        'causes': 'Lack of sleep, dehydration, genetics, stress.',
        'remedies': '• Sleep at least 7-8 hours\n• Stay hydrated\n• Use under-eye creams\n• Manage stress\n• Reduce screen time'
    },
    'Moderate': {
        'causes': 'Mild sleep issues, stress, slight dehydration.',
        'remedies': '• Improve sleep routine\n• Drink more water\n• Gentle eye massage\n• Cold compress therapy'
    },
    'Low': {
        'causes': 'Minor tiredness or long screen exposure.',
        'remedies': '• Take regular screen breaks\n• Maintain hydration\n• Relax eyes frequently'
    },
    'No': {
        'causes': 'No significant dark circles detected! 👏',
        'remedies': '• Maintain healthy habits\n• Keep good sleep and hydration routine'
    }
}

def process_prediction(image):
    """
    Process an image through the model and return prediction results
    
    Args:
        image: PIL Image object
    
    Returns:
        dict: Prediction response with class_name, causes, remedies, and confidence
    """
    # Check if model is loaded
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check server logs.")
    
    # Convert PIL Image to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Run prediction
    results = model.predict(image, conf=0.25)
    names = model.names
    
    # Get predictions
    predictions = results[0].boxes.cls.tolist()
    
    if predictions:
        class_id = int(predictions[0])  # Taking the first detection
        class_name = names[class_id]
        confidence = float(results[0].boxes.conf[0])
    else:
        class_name = 'No'
        confidence = None
    
    # Get advice
    advice = advice_dict.get(class_name, {
        'causes': 'Unknown',
        'remedies': 'No advice available.'
    })
    
    # Format response
    response = {
        "success": True,
        "prediction": class_name.replace('_', ' ').capitalize(),
        "class_name": class_name,
        "causes": advice['causes'],
        "remedies": advice['remedies'],
        "confidence": confidence
    }
    
    return response

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Dark Circles Detection API",
        "version": "1.0.0",
        "model_path": model_path if model_path else "Not loaded",
        "endpoints": {
            "/predict": "POST - Upload an image to detect dark circles",
            "/predict/camera": "POST - Capture image from webcam and detect dark circles",
            "/health": "GET - Check API health status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": model_path
    }

@app.post("/predict")
async def predict_dark_circles(file: UploadFile = File(...)):
    """
    Predict dark circles severity from an uploaded image
    
    Args:
        file: Image file (jpg, png, etc.)
    
    Returns:
        JSON response with prediction class, causes, and remedies
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Process prediction
        response = process_prediction(image)
        return JSONResponse(content=response)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/predict/camera")
async def predict_from_camera(camera_index: int = Query(default=0, description="Camera device index (0 for default camera)")):
    """
    Capture an image from webcam and predict dark circles severity
    
    Args:
        camera_index: Camera device index (default: 0 for default camera)
    
    Returns:
        JSON response with prediction class, causes, and remedies
    """
    try:
        # Check if model is loaded
        if model is None:
            raise HTTPException(status_code=503, detail="Model not loaded. Please check server logs.")
        
        # Open camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            raise HTTPException(
                status_code=500, 
                detail=f"Could not open camera at index {camera_index}. Make sure the camera is connected and not being used by another application."
            )
        
        # Capture frame
        ret, frame = cap.read()
        cap.release()  # Release camera immediately after capture
        
        if not ret or frame is None:
            raise HTTPException(status_code=500, detail="Failed to capture image from camera")
        
        # Convert BGR (OpenCV format) to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert numpy array to PIL Image
        image = Image.fromarray(frame_rgb)
        
        # Process prediction
        response = process_prediction(image)
        return JSONResponse(content=response)
    
    except HTTPException:
        raise
    except cv2.error as e:
        raise HTTPException(status_code=500, detail=f"OpenCV error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error capturing from camera: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

