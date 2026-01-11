"""
Script to re-export the YOLO model to fix version compatibility issues.
This will load the old model and save it in a format compatible with the current ultralytics version.
"""
from ultralytics import YOLO
import os

def re_export_model():
    """Re-export the model to fix version compatibility"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find the model file
    model_file = "best (7).pt"
    model_path = os.path.join(current_dir, model_file)
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return
    
    print(f"📦 Found model: {model_path}")
    print("🔄 Attempting to load and re-export the model...")
    
    try:
        # Try to load with weights_only=False to handle old format
        import torch
        
        # Load checkpoint directly
        print("Loading checkpoint...")
        checkpoint = torch.load(model_path, map_location='cpu', weights_only=False)
        
        # Try to extract model architecture info
        if 'model' in checkpoint:
            print("✅ Checkpoint loaded successfully")
            print("Model keys:", list(checkpoint.keys())[:10])
            
            # Try to create a new model and load weights
            print("\n🔄 Attempting to create new model...")
            
            # Get model architecture from checkpoint if available
            if 'model_yaml' in checkpoint:
                # Create model from YAML
                from ultralytics import YOLO
                model = YOLO(checkpoint['model_yaml'])
                model.load(model_path)
            else:
                # Try loading directly - this might still fail
                model = YOLO(model_path)
            
            # Export to new format
            output_path = os.path.join(current_dir, "best_reexported.pt")
            print(f"\n💾 Saving re-exported model to: {output_path}")
            
            # Save the model
            model.save(output_path)
            print(f"✅ Model re-exported successfully to: {output_path}")
            print("\n📝 Update main.py to use 'best_reexported.pt' instead of 'best (7).pt'")
            
        else:
            print("❌ Could not find model in checkpoint")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔧 Alternative approach: Try installing a compatible ultralytics version")
        print("The model might have been trained with ultralytics < 8.0.0")
        print("\nTry:")
        print("  pip install ultralytics==7.0.0")
        print("  # or")
        print("  pip install ultralytics==6.0.0")

if __name__ == "__main__":
    re_export_model()

