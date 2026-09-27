"""
AnalysisService — Orchestrates the fashion analysis pipeline.

Priority order:
  1. Colab backend (real ML, if COLAB_API_URL is set and reachable)
  2. Local YOLO model (if model file exists and DEMO_MODE=false)
  3. Demo analyzer (fallback, returns preset results)
"""

from config import settings
from ml.demo_analyzer import DemoAnalyzer
from ml.yolo_analyzer import YOLOAnalyzer
from ml.colab_analyzer import ColabAnalyzer
from models.schemas import AnalysisResult
import numpy as np


class AnalysisService:
    def __init__(self):
        self.demo_analyzer = DemoAnalyzer()
        self.real_analyzer = YOLOAnalyzer(settings.YOLO_MODEL_PATH)
        self.colab_analyzer = ColabAnalyzer(settings.COLAB_API_URL)

        # Log which analyzer will be used
        if settings.COLAB_API_URL:
            print(f"[AnalysisService] Colab URL configured: {settings.COLAB_API_URL}")
        if settings.DEMO_MODE:
            print("[AnalysisService] Demo mode is ON (fallback)")

    def analyze_image(self, image: np.ndarray) -> AnalysisResult:
        """Run analysis using the best available analyzer."""

        # Priority 1: Colab (real ML)
        if settings.COLAB_API_URL and self.colab_analyzer.is_available():
            try:
                print("[AnalysisService] Using Colab analyzer")
                data = self.colab_analyzer.analyze(image)
                return AnalysisResult(**data)
            except Exception as e:
                print(f"[AnalysisService] Colab failed: {e}, falling back...")

        # Priority 2: Local YOLO model
        if not settings.DEMO_MODE and self.real_analyzer.is_available():
            try:
                print("[AnalysisService] Using local YOLO analyzer")
                data = self.real_analyzer.analyze(image)
                return AnalysisResult(**data)
            except Exception as e:
                print(f"[AnalysisService] YOLO failed: {e}, falling back...")

        # Priority 3: Demo mode
        print("[AnalysisService] Using demo analyzer")
        data = self.demo_analyzer.analyze(image)
        return AnalysisResult(**data)
