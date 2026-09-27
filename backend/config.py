import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "true").lower() == "true"
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", str(10 * 1024 * 1024)))
    ALLOWED_EXTENSIONS: list[str] = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,webp").split(",")
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "models/weights/yolov8n.pt")
    COLAB_API_URL: str = os.getenv("COLAB_API_URL", "")

settings = Settings()
