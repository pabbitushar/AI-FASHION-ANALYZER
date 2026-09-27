"""
ColabAnalyzer — Bridges the local backend to the Google Colab ML server.

Sends the uploaded image to the Colab ngrok endpoint for real fashion detection.
Falls back gracefully if Colab is unreachable.
"""

import io
import requests
from PIL import Image
import numpy as np
from ml.base import FashionAnalyzer
from config import settings


class ColabAnalyzer(FashionAnalyzer):
    """Sends images to a remote Colab-hosted fashion detection API."""

    def __init__(self, colab_url: str = ""):
        self.colab_url = colab_url.rstrip("/") if colab_url else ""
        self._available = False
        if self.colab_url:
            self._check_connection()

    def _check_connection(self):
        """Ping the Colab health endpoint."""
        try:
            resp = requests.get(f"{self.colab_url}/api/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                self._available = True
                print(f"[ColabAnalyzer] Connected to Colab: {data}")
            else:
                self._available = False
                print(f"[ColabAnalyzer] Colab returned status {resp.status_code}")
        except Exception as e:
            self._available = False
            print(f"[ColabAnalyzer] Colab not reachable: {e}")

    def is_available(self) -> bool:
        """Check if Colab backend is reachable. Re-checks on each call."""
        if self.colab_url:
            self._check_connection()
        return self._available

    def analyze(self, image: np.ndarray) -> dict:
        """Send image to Colab for analysis. Returns structured result dict."""
        if not self.colab_url:
            raise RuntimeError("Colab URL not configured")

        # Convert numpy array to JPEG bytes
        pil_image = Image.fromarray(image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)

        try:
            resp = requests.post(
                f"{self.colab_url}/api/analyze",
                files={"file": ("outfit.jpg", buffer, "image/jpeg")},
                timeout=60,  # ML inference can take a while
            )

            if resp.status_code != 200:
                error_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                raise RuntimeError(error_data.get("error", f"Colab returned {resp.status_code}"))

            result = resp.json()

            if not result.get("success"):
                raise RuntimeError(result.get("error", "Colab analysis failed"))

            return result["data"]

        except requests.exceptions.Timeout:
            raise RuntimeError("Colab took too long to respond. The model may still be loading.")
        except requests.exceptions.ConnectionError:
            self._available = False
            raise RuntimeError("Lost connection to Colab. Check if the notebook is still running.")
