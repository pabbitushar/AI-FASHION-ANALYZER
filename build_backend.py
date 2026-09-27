import os

base_dir = r"c:\Users\HP\AI Fashion analyzer\backend"
os.makedirs(base_dir, exist_ok=True)

files = {}

files["requirements.txt"] = """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pillow>=10.0.0
opencv-python-headless>=4.8.0
numpy>=1.24.0
scikit-learn>=1.3.0
pydantic>=2.0.0
python-dotenv>=1.0.0
"""

files[".env.example"] = """# StyleSense AI Environment Variables
DEMO_MODE=true
MAX_IMAGE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
CORS_ORIGINS=http://localhost:5173
YOLO_MODEL_PATH=models/weights/yolov8n.pt
"""

files["config.py"] = """import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", str(10 * 1024 * 1024)))
    ALLOWED_EXTENSIONS: list[str] = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,webp").split(",")
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "models/weights/yolov8n.pt")

settings = Settings()
"""

files["models/__init__.py"] = ""

files["models/schemas.py"] = """from pydantic import BaseModel
from typing import Optional

class ClothingItem(BaseModel):
    category: str
    display_name: str
    color: str
    color_hex: str
    confidence: float
    bbox: list[float]
    icon: str

class PaletteColor(BaseModel):
    name: str
    hex: str
    percentage: float
    is_dominant: bool

class StyleClassification(BaseModel):
    label: str
    secondary_label: Optional[str] = None
    confidence: float
    insight: str

class AnalysisResult(BaseModel):
    items: list[ClothingItem]
    palette: list[PaletteColor]
    style: StyleClassification
    item_count: int
    is_demo: bool

class AnalysisResponse(BaseModel):
    success: bool
    data: Optional[AnalysisResult] = None
    error: Optional[str] = None
    message: Optional[str] = None
"""

files["ml/__init__.py"] = ""

files["ml/base.py"] = """from abc import ABC, abstractmethod

class FashionAnalyzer(ABC):
    @abstractmethod
    def analyze(self, image) -> dict:
        \"\"\"Analyze an image and return structured fashion data.\"\"\"
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        \"\"\"Check if this analyzer is ready.\"\"\"
        pass
"""

files["ml/demo_analyzer.py"] = """import random
from models.schemas import AnalysisResult, ClothingItem, PaletteColor, StyleClassification
from ml.base import FashionAnalyzer

class DemoAnalyzer(FashionAnalyzer):
    def is_available(self) -> bool:
        return True

    def analyze(self, image) -> dict:
        presets = [
            {
                "items": [
                    ClothingItem(category="t-shirt", display_name="T-Shirt", color="black", color_hex="#1a1a1a", confidence=0.95, bbox=[0.2, 0.1, 0.8, 0.5], icon="👕"),
                    ClothingItem(category="jeans", display_name="Jeans", color="blue", color_hex="#2a52be", confidence=0.92, bbox=[0.2, 0.5, 0.8, 0.9], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="black", hex="#1a1a1a", percentage=55.0, is_dominant=True),
                    PaletteColor(name="blue", hex="#2a52be", percentage=45.0, is_dominant=False)
                ],
                "style": StyleClassification(label="casual", secondary_label="everyday", confidence=0.88, insight="A classic, effortless everyday look combining basic staples.")
            },
            {
                "items": [
                    ClothingItem(category="blazer", display_name="Blazer", color="navy", color_hex="#000080", confidence=0.98, bbox=[0.1, 0.1, 0.9, 0.6], icon="🧥"),
                    ClothingItem(category="trousers", display_name="Trousers", color="navy", color_hex="#000080", confidence=0.91, bbox=[0.2, 0.6, 0.8, 1.0], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="navy", hex="#000080", percentage=80.0, is_dominant=True),
                    PaletteColor(name="white", hex="#ffffff", percentage=20.0, is_dominant=False)
                ],
                "style": StyleClassification(label="formal", secondary_label="business", confidence=0.94, insight="Sharp and professional monochromatic tailoring.")
            },
            {
                "items": [
                    ClothingItem(category="hoodie", display_name="Hoodie", color="gray", color_hex="#808080", confidence=0.89, bbox=[0.15, 0.1, 0.85, 0.55], icon="🧥"),
                    ClothingItem(category="sweatpants", display_name="Sweatpants", color="black", color_hex="#000000", confidence=0.85, bbox=[0.2, 0.55, 0.8, 0.95], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="gray", hex="#808080", percentage=60.0, is_dominant=True),
                    PaletteColor(name="black", hex="#000000", percentage=40.0, is_dominant=False)
                ],
                "style": StyleClassification(label="sporty", secondary_label="athleisure", confidence=0.91, insight="Comfort-first athleisure perfect for on-the-go days.")
            },
            {
                "items": [
                    ClothingItem(category="jacket", display_name="Oversized Jacket", color="olive", color_hex="#808000", confidence=0.88, bbox=[0.1, 0.1, 0.9, 0.6], icon="🧥"),
                    ClothingItem(category="cargo", display_name="Cargo Pants", color="beige", color_hex="#f5f5dc", confidence=0.87, bbox=[0.15, 0.6, 0.85, 1.0], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="olive", hex="#808000", percentage=50.0, is_dominant=True),
                    PaletteColor(name="beige", hex="#f5f5dc", percentage=50.0, is_dominant=False)
                ],
                "style": StyleClassification(label="streetwear", secondary_label="utilitarian", confidence=0.85, insight="A trendy streetwear fit with utilitarian elements.")
            },
            {
                "items": [
                    ClothingItem(category="shirt", display_name="Button-up", color="white", color_hex="#ffffff", confidence=0.93, bbox=[0.2, 0.1, 0.8, 0.5], icon="👔"),
                    ClothingItem(category="chinos", display_name="Chinos", color="tan", color_hex="#d2b48c", confidence=0.90, bbox=[0.2, 0.5, 0.8, 0.9], icon="👖")
                ],
                "palette": [
                    PaletteColor(name="white", hex="#ffffff", percentage=45.0, is_dominant=False),
                    PaletteColor(name="tan", hex="#d2b48c", percentage=55.0, is_dominant=True)
                ],
                "style": StyleClassification(label="smart casual", secondary_label="preppy", confidence=0.92, insight="A polished smart casual combination blending comfort and sophistication.")
            },
            {
                "items": [
                    ClothingItem(category="dress", display_name="Maxi Dress", color="floral", color_hex="#ffb6c1", confidence=0.96, bbox=[0.2, 0.1, 0.8, 0.9], icon="👗")
                ],
                "palette": [
                    PaletteColor(name="pink", hex="#ffb6c1", percentage=70.0, is_dominant=True),
                    PaletteColor(name="green", hex="#008000", percentage=30.0, is_dominant=False)
                ],
                "style": StyleClassification(label="boho", secondary_label="summer", confidence=0.89, insight="A breezy, free-spirited bohemian dress with floral accents.")
            }
        ]
        
        selected = random.choice(presets)
        
        result = AnalysisResult(
            items=selected["items"],
            palette=selected["palette"],
            style=selected["style"],
            item_count=len(selected["items"]),
            is_demo=True
        )
        return result.model_dump()
"""

files["ml/yolo_analyzer.py"] = """import os
from ml.base import FashionAnalyzer

class YOLOAnalyzer(FashionAnalyzer):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None

    def is_available(self) -> bool:
        # Check if the YOLO model exists. Place your model in models/weights/yolov8n.pt
        return os.path.exists(self.model_path)

    def analyze(self, image) -> dict:
        \"\"\"
        Real analyzer stub that would use ultralytics YOLO model.
        To implement:
        1. import ultralytics
        2. self.model = ultralytics.YOLO(self.model_path)
        3. results = self.model(image)
        4. map results to schema
        \"\"\"
        if not self.is_available():
            raise RuntimeError("YOLO model not found.")
        
        # Stub implementation
        return {}
"""

files["ml/color_extractor.py"] = """import cv2
import numpy as np
from sklearn.cluster import KMeans
from models.schemas import PaletteColor

COLOR_MAPPING = {
    "black": (0, 0, 0), "white": (255, 255, 255), "navy": (0, 0, 128),
    "blue": (0, 0, 255), "red": (255, 0, 0), "green": (0, 128, 0),
    "gray": (128, 128, 128), "beige": (245, 245, 220), "brown": (165, 42, 42),
    "tan": (210, 180, 140), "pink": (255, 192, 203), "purple": (128, 0, 128),
    "orange": (255, 165, 0), "yellow": (255, 255, 0), "olive": (128, 128, 0),
    "burgundy": (128, 0, 32), "teal": (0, 128, 128), "cream": (255, 253, 208),
    "coral": (255, 127, 80), "maroon": (128, 0, 0)
}

def closest_color(requested_color: tuple) -> str:
    min_colors = {}
    for name, value in COLOR_MAPPING.items():
        r_c, g_c, b_c = value
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]

def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_colors(image: np.ndarray, bbox: list[float] = None, n_colors: int = 5) -> list[PaletteColor]:
    \"\"\"Extract dominant colors from image or bounding box region using KMeans.\"\"\"
    if bbox is not None:
        h, w = image.shape[:2]
        x1, y1, x2, y2 = [int(bbox[0]*w), int(bbox[1]*h), int(bbox[2]*w), int(bbox[3]*h)]
        image = image[y1:y2, x1:x2]
        if image.size == 0:
            return []
            
    # Resize to speed up
    image = cv2.resize(image, (100, 100))
    pixels = image.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=n_colors, n_init=10)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    counts = np.bincount(labels)
    total = sum(counts)
    
    palette = []
    for i in range(n_colors):
        color = colors[i]
        percentage = (counts[i] / total) * 100
        name = closest_color(color)
        hex_val = rgb_to_hex(color)
        is_dom = i == np.argmax(counts)
        palette.append(PaletteColor(name=name, hex=hex_val, percentage=float(percentage), is_dominant=bool(is_dom)))
        
    return palette

def get_dominant_color(image: np.ndarray, bbox: list[float] = None) -> tuple[str, str]:
    colors = extract_colors(image, bbox, n_colors=1)
    if colors:
        return colors[0].name, colors[0].hex
    return "unknown", "#000000"
"""

files["utils/__init__.py"] = ""

files["utils/image_utils.py"] = """import os
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
    \"\"\"Convert bytes to numpy array for OpenCV processing.\"\"\"
    # Process images in memory (No temp files)
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    # Resize max 640px
    max_size = 640
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))
    return np.array(image)

def cleanup_temp_file(path: str):
    \"\"\"Delete temp file if it exists.\"\"\"
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
"""

files["services/__init__.py"] = ""

files["services/analysis_service.py"] = """from config import settings
from ml.demo_analyzer import DemoAnalyzer
from ml.yolo_analyzer import YOLOAnalyzer
from models.schemas import AnalysisResult
import numpy as np

class AnalysisService:
    def __init__(self):
        self.demo_analyzer = DemoAnalyzer()
        self.real_analyzer = YOLOAnalyzer(settings.YOLO_MODEL_PATH)

    def analyze_image(self, image: np.ndarray) -> AnalysisResult:
        if settings.DEMO_MODE or not self.real_analyzer.is_available():
            data = self.demo_analyzer.analyze(image)
        else:
            data = self.real_analyzer.analyze(image)
            
        return AnalysisResult(**data)
"""

files["api/__init__.py"] = ""

files["api/routes.py"] = """from fastapi import APIRouter, UploadFile, File, HTTPException
from services.analysis_service import AnalysisService
from utils.image_utils import validate_image, load_image
from models.schemas import AnalysisResponse, AnalysisResult
from config import settings
import traceback

router = APIRouter()
service = AnalysisService()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_endpoint(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
        
    file_bytes = await file.read()
    
    is_valid, msg = validate_image(file_bytes, file.filename)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
        
    try:
        image = load_image(file_bytes)
    except Exception:
        raise HTTPException(status_code=422, detail="We couldn't get a clear read of the outfit. Try a photo where one person is clearly visible and most of the outfit is in frame.")
        
    try:
        result = service.analyze_image(image)
        return AnalysisResponse(success=True, data=result, message="Analysis complete")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Server error during analysis.")
    finally:
        # If we had temp files we would clean them up here
        pass

@router.get("/health")
def health_check():
    return {"status": "ok", "demo_mode": settings.DEMO_MODE}

@router.get("/config")
def get_config():
    return {
        "demo_mode": settings.DEMO_MODE,
        "max_image_size": settings.MAX_IMAGE_SIZE,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS
    }
"""

files["main.py"] = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from config import settings

app = FastAPI(title="StyleSense AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
"""

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
