import cv2
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
    """Extract dominant colors from image or bounding box region using KMeans."""
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
