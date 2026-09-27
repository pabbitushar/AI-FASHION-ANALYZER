import os
import io
import cv2
import numpy as np
from PIL import Image
from config import settings

def validate_image(file_bytes: bytes, filename: str) -> tuple[bool, str]:
    if len(file_bytes) > settings.MAX_IMAGE_SIZE:
        return False, "This image is too large. Please upload an image under 10MB."
    
    ext = filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        return False, "This image format isn't supported. Please upload a JPG, PNG, or WebP image."
        
    return True, ""

def load_image(file_bytes: bytes) -> np.ndarray:
    """Convert bytes to numpy array for OpenCV processing."""
    # Process images in memory (No temp files)
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    # Resize max 640px
    max_size = 640
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))
    return np.array(image)

def cleanup_temp_file(path: str):
    """Delete temp file if it exists."""
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
