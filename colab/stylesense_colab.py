# -----------------------------------------------------------
# StyleSense AI — Fashion Detection Backend (Google Colab)
# -----------------------------------------------------------
# HOW TO USE:
# 1. Open Google Colab (colab.research.google.com)
# 2. File → Upload notebook → upload this file
#    (Colab treats .py files with # %% markers as notebooks)
# 3. Runtime → Change runtime type → GPU (T4 is fine)
# 4. Run All (Ctrl+F9)
# 5. Copy the ngrok URL printed at the bottom
# 6. Paste it in your backend .env: COLAB_API_URL=https://xxxx.ngrok-free.app
# 7. Restart your local backend
# -----------------------------------------------------------

# %% [markdown]
# # 🧠 StyleSense AI — Fashion Detection
# This notebook runs the real fashion detection model.
# It exposes an API that your local app calls.

# %% Install dependencies
!pip install -q transformers torch torchvision pillow fastapi uvicorn pyngrok python-multipart scikit-learn opencv-python-headless nest-asyncio

# %% Imports and setup
import io
import base64
import numpy as np
import cv2
import torch
from PIL import Image
from sklearn.cluster import KMeans
from transformers import AutoImageProcessor, AutoModelForObjectDetection

print("✅ Imports loaded")

# %% Load the fashion detection model
MODEL_NAME = "valentinafeve/yolos-fashionpedia"

print("⏳ Loading fashion detection model... (first time may take ~2 min)")
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForObjectDetection.from_pretrained(MODEL_NAME)
model.eval()

# Move to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
print(f"✅ Model loaded on {device}")

# %% Category definitions
# Fashionpedia 27 categories
FASHIONPEDIA_CATEGORIES = {
    0: {"name": "shirt", "display": "Shirt / Blouse", "icon": "👔", "group": "top"},
    1: {"name": "top", "display": "Top / T-Shirt", "icon": "👕", "group": "top"},
    2: {"name": "sweater", "display": "Sweater", "icon": "🧶", "group": "top"},
    3: {"name": "cardigan", "display": "Cardigan", "icon": "🧥", "group": "top"},
    4: {"name": "jacket", "display": "Jacket", "icon": "🧥", "group": "outerwear"},
    5: {"name": "vest", "display": "Vest", "icon": "🦺", "group": "top"},
    6: {"name": "pants", "display": "Pants", "icon": "👖", "group": "bottom"},
    7: {"name": "shorts", "display": "Shorts", "icon": "🩳", "group": "bottom"},
    8: {"name": "skirt", "display": "Skirt", "icon": "👗", "group": "bottom"},
    9: {"name": "coat", "display": "Coat", "icon": "🧥", "group": "outerwear"},
    10: {"name": "dress", "display": "Dress", "icon": "👗", "group": "full-body"},
    11: {"name": "jumpsuit", "display": "Jumpsuit", "icon": "👗", "group": "full-body"},
    12: {"name": "cape", "display": "Cape", "icon": "🧥", "group": "outerwear"},
    13: {"name": "glasses", "display": "Glasses", "icon": "👓", "group": "accessory"},
    14: {"name": "hat", "display": "Hat", "icon": "🎩", "group": "accessory"},
    15: {"name": "headband", "display": "Headband / Hair Accessory", "icon": "💇", "group": "accessory"},
    16: {"name": "tie", "display": "Tie", "icon": "👔", "group": "accessory"},
    17: {"name": "glove", "display": "Gloves", "icon": "🧤", "group": "accessory"},
    18: {"name": "watch", "display": "Watch", "icon": "⌚", "group": "accessory"},
    19: {"name": "belt", "display": "Belt", "icon": "🪢", "group": "accessory"},
    20: {"name": "leg_warmer", "display": "Leg Warmer", "icon": "🧦", "group": "bottom"},
    21: {"name": "tights", "display": "Tights / Stockings", "icon": "🧦", "group": "bottom"},
    22: {"name": "sock", "display": "Socks", "icon": "🧦", "group": "footwear"},
    23: {"name": "shoe", "display": "Shoes", "icon": "👟", "group": "footwear"},
    24: {"name": "bag", "display": "Bag / Wallet", "icon": "👜", "group": "accessory"},
    25: {"name": "scarf", "display": "Scarf", "icon": "🧣", "group": "accessory"},
    26: {"name": "umbrella", "display": "Umbrella", "icon": "☂️", "group": "accessory"},
}

# Color name mapping (RGB → nearest named color)
COLOR_MAP = {
    "black": (0, 0, 0), "white": (255, 255, 255), "navy": (0, 0, 128),
    "blue": (0, 0, 255), "light blue": (135, 206, 235), "red": (255, 0, 0),
    "dark red": (139, 0, 0), "green": (0, 128, 0), "dark green": (0, 100, 0),
    "gray": (128, 128, 128), "light gray": (192, 192, 192), "dark gray": (64, 64, 64),
    "beige": (245, 245, 220), "brown": (139, 90, 43), "tan": (210, 180, 140),
    "pink": (255, 182, 193), "hot pink": (255, 105, 180), "purple": (128, 0, 128),
    "lavender": (186, 147, 216), "orange": (255, 165, 0), "yellow": (255, 255, 0),
    "olive": (128, 128, 0), "burgundy": (128, 0, 32), "teal": (0, 128, 128),
    "cream": (255, 253, 208), "coral": (255, 127, 80), "maroon": (128, 0, 0),
    "khaki": (195, 176, 145), "denim blue": (80, 102, 140),
}

print(f"✅ {len(FASHIONPEDIA_CATEGORIES)} clothing categories loaded")

# %% Color extraction functions
def closest_color_name(rgb):
    """Find the nearest named color for an RGB tuple."""
    min_dist = float("inf")
    name = "unknown"
    for cname, crgb in COLOR_MAP.items():
        dist = sum((a - b) ** 2 for a, b in zip(rgb, crgb))
        if dist < min_dist:
            min_dist = dist
            name = cname
    return name

def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_region_color(image_np, bbox, n_colors=3):
    """Extract dominant color from a bounding box region."""
    h, w = image_np.shape[:2]
    x1 = max(0, int(bbox[0]))
    y1 = max(0, int(bbox[1]))
    x2 = min(w, int(bbox[2]))
    y2 = min(h, int(bbox[3]))

    region = image_np[y1:y2, x1:x2]
    if region.size == 0 or region.shape[0] < 5 or region.shape[1] < 5:
        return "unknown", "#808080"

    # Resize region for speed
    region_small = cv2.resize(region, (50, 50))
    pixels = region_small.reshape(-1, 3).astype(float)

    # Remove near-skin tones (rough filter to avoid skin being the "color")
    # Skin typically: R > 100, G > 50, B > 30, R > G > B
    mask = ~((pixels[:, 0] > 140) & (pixels[:, 1] > 80) & (pixels[:, 1] < pixels[:, 0]) & (pixels[:, 2] < pixels[:, 1]))
    filtered = pixels[mask]
    if len(filtered) < 20:
        filtered = pixels  # Not enough non-skin pixels, use all

    k = min(n_colors, len(filtered))
    if k < 1:
        return "unknown", "#808080"

    kmeans = KMeans(n_clusters=k, n_init=5, random_state=42)
    kmeans.fit(filtered)

    # Get the most frequent cluster
    counts = np.bincount(kmeans.labels_)
    dominant_idx = np.argmax(counts)
    dominant_rgb = kmeans.cluster_centers_[dominant_idx]

    name = closest_color_name(dominant_rgb)
    hex_val = rgb_to_hex(dominant_rgb)
    return name, hex_val

def extract_palette(image_np, items_bboxes, n_colors=5):
    """Extract overall color palette from all clothing regions combined."""
    all_pixels = []

    for bbox in items_bboxes:
        h, w = image_np.shape[:2]
        x1, y1, x2, y2 = max(0, int(bbox[0])), max(0, int(bbox[1])), min(w, int(bbox[2])), min(h, int(bbox[3]))
        region = image_np[y1:y2, x1:x2]
        if region.size == 0:
            continue
        region_small = cv2.resize(region, (40, 40))
        all_pixels.append(region_small.reshape(-1, 3))

    if not all_pixels:
        return []

    combined = np.vstack(all_pixels).astype(float)
    k = min(n_colors, len(combined))
    if k < 1:
        return []

    kmeans = KMeans(n_clusters=k, n_init=5, random_state=42)
    kmeans.fit(combined)

    counts = np.bincount(kmeans.labels_)
    total = len(kmeans.labels_)
    dominant_idx = int(np.argmax(counts))

    palette = []
    for i in range(k):
        rgb = kmeans.cluster_centers_[i]
        palette.append({
            "name": closest_color_name(rgb),
            "hex": rgb_to_hex(rgb),
            "percentage": round(float(counts[i] / total) * 100, 1),
            "is_dominant": i == dominant_idx,
        })

    # Sort by percentage descending
    palette.sort(key=lambda x: x["percentage"], reverse=True)
    return palette

print("✅ Color extraction ready")

# %% Clothing detection function
CONFIDENCE_THRESHOLD = 0.4

def detect_clothing(image_pil):
    """Detect clothing items in a PIL image. Returns list of detections."""
    inputs = processor(images=image_pil, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    target_sizes = torch.tensor([image_pil.size[::-1]], device=device)
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=CONFIDENCE_THRESHOLD)

    if not results:
        return []

    result = results[0]
    boxes = result["boxes"].cpu().numpy()
    scores = result["scores"].cpu().numpy()
    labels = result["labels"].cpu().numpy()

    image_np = np.array(image_pil)
    h, w = image_np.shape[:2]

    detections = []
    for box, score, label in zip(boxes, scores, labels):
        label_int = int(label)
        if label_int not in FASHIONPEDIA_CATEGORIES:
            continue

        cat = FASHIONPEDIA_CATEGORIES[label_int]
        x1, y1, x2, y2 = box

        # Extract color from this region
        color_name, color_hex = extract_region_color(image_np, [x1, y1, x2, y2])

        detections.append({
            "category": cat["name"],
            "display_name": cat["display"],
            "color": color_name,
            "color_hex": color_hex,
            "confidence": round(float(score), 3),
            "bbox": [
                round(float(x1) / w, 4),
                round(float(y1) / h, 4),
                round(float(x2) / w, 4),
                round(float(y2) / h, 4),
            ],
            "icon": cat["icon"],
            "group": cat["group"],
        })

    # Sort by confidence descending
    detections.sort(key=lambda x: x["confidence"], reverse=True)

    # Deduplicate: if two detections of the same category overlap heavily, keep the best
    final = []
    for det in detections:
        is_dup = False
        for existing in final:
            if existing["category"] == det["category"]:
                # Check IoU
                iou = compute_iou(det["bbox"], existing["bbox"])
                if iou > 0.5:
                    is_dup = True
                    break
        if not is_dup:
            final.append(det)

    return final

def compute_iou(box1, box2):
    """Compute IoU between two normalized boxes [x1,y1,x2,y2]."""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = area1 + area2 - inter
    return inter / union if union > 0 else 0

print("✅ Clothing detection ready")

# %% Style classification
STYLE_RULES = {
    "formal": {
        "requires_any": ["shirt", "tie", "coat", "dress"],
        "boost_items": ["belt", "watch", "glasses"],
        "penalize": ["shorts", "sock", "hat", "cap"],
    },
    "casual": {
        "requires_any": ["top", "pants", "shoe", "shorts"],
        "boost_items": ["bag", "scarf"],
        "penalize": ["tie", "coat"],
    },
    "sporty": {
        "requires_any": ["shorts", "top", "shoe", "sock"],
        "boost_items": ["hat", "watch"],
        "penalize": ["tie", "dress", "coat", "shirt"],
    },
    "streetwear": {
        "requires_any": ["jacket", "pants", "shoe", "hat"],
        "boost_items": ["bag", "scarf", "glasses"],
        "penalize": ["tie", "dress"],
    },
    "smart casual": {
        "requires_any": ["shirt", "pants", "shoe", "sweater", "cardigan"],
        "boost_items": ["belt", "watch", "bag"],
        "penalize": ["shorts", "sock"],
    },
    "bohemian": {
        "requires_any": ["dress", "skirt", "scarf"],
        "boost_items": ["hat", "bag", "headband"],
        "penalize": ["tie", "coat"],
    },
}

def classify_style(items):
    """Rule-based style classification from detected items."""
    if not items:
        return {"label": "unknown", "secondary_label": None, "confidence": 0.0,
                "insight": "We couldn't determine a style direction from this image."}

    item_names = {item["category"] for item in items}
    item_groups = {item.get("group", "") for item in items}
    colors = [item["color"] for item in items]

    scores = {}
    for style, rules in STYLE_RULES.items():
        score = 0.0
        matches = item_names & set(rules["requires_any"])
        score += len(matches) * 0.3
        boosts = item_names & set(rules["boost_items"])
        score += len(boosts) * 0.1
        penalties = item_names & set(rules["penalize"])
        score -= len(penalties) * 0.15
        scores[style] = max(0.0, score)

    if not any(scores.values()):
        # Default to casual
        scores["casual"] = 0.3

    sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = sorted_styles[0]
    second = sorted_styles[1] if len(sorted_styles) > 1 else None

    # Build insight
    item_list = [item["display_name"] for item in items[:4]]
    color_list = list(dict.fromkeys(colors))[:3]  # unique, first 3

    if len(item_list) == 1:
        items_text = item_list[0]
    elif len(item_list) == 2:
        items_text = f"{item_list[0]} and {item_list[1]}"
    else:
        items_text = ", ".join(item_list[:-1]) + f", and {item_list[-1]}"

    color_text = " and ".join(color_list[:2]) if color_list else "mixed"
    style_label = best[0]

    insight_templates = [
        f"Your outfit features {items_text} with a {color_text} color direction — reading as {style_label}.",
        f"A {style_label} look built around {items_text} in {color_text} tones.",
        f"We see {items_text} creating a {style_label} silhouette with {color_text} as the dominant palette.",
    ]

    import random
    insight = random.choice(insight_templates)

    return {
        "label": best[0],
        "secondary_label": second[0] if second and second[1] > 0.15 else None,
        "confidence": round(min(best[1] / 0.9, 1.0), 2),
        "insight": insight,
    }

print("✅ Style classification ready")

# %% Full analysis pipeline
def analyze_image(image_pil):
    """Run the complete analysis pipeline on a PIL image."""
    # 1. Detect clothing
    items = detect_clothing(image_pil)

    # 2. Extract overall palette from clothing regions
    image_np = np.array(image_pil)
    bboxes_abs = []
    h, w = image_np.shape[:2]
    for item in items:
        b = item["bbox"]
        bboxes_abs.append([b[0]*w, b[1]*h, b[2]*w, b[3]*h])

    palette = extract_palette(image_np, bboxes_abs, n_colors=5) if bboxes_abs else []

    # 3. Classify style
    style = classify_style(items)

    # 4. Clean items (remove 'group' field before returning)
    clean_items = []
    for item in items:
        clean_item = {k: v for k, v in item.items() if k != "group"}
        clean_items.append(clean_item)

    return {
        "success": True,
        "data": {
            "items": clean_items,
            "palette": palette,
            "style": style,
            "item_count": len(clean_items),
            "is_demo": False,
        },
        "error": None,
        "message": f"Detected {len(clean_items)} clothing item(s)",
    }

# Quick self-test with a blank image
test_result = analyze_image(Image.new("RGB", (200, 200), color=(100, 100, 200)))
print(f"✅ Pipeline self-test OK (detected {test_result['data']['item_count']} items in blank test)")

# %% FastAPI server
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(title="StyleSense AI - Colab Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": False, "device": str(device), "model": MODEL_NAME}

@app.get("/api/config")
def config():
    return {"demo_mode": False, "max_image_size": 10 * 1024 * 1024, "allowed_extensions": ["jpg", "jpeg", "png", "webp"]}

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if len(contents) > 10 * 1024 * 1024:
            return JSONResponse(status_code=400, content={
                "success": False, "data": None,
                "error": "Image too large. Please upload under 10MB.", "message": None
            })

        image = Image.open(io.BytesIO(contents)).convert("RGB")

        # Resize if very large (keep under 1024px for speed)
        max_dim = 1024
        if max(image.size) > max_dim:
            ratio = max_dim / max(image.size)
            new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
            image = image.resize(new_size, Image.LANCZOS)

        result = analyze_image(image)
        return JSONResponse(content=result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={
            "success": False, "data": None,
            "error": f"Analysis failed: {str(e)}", "message": None
        })

print("✅ FastAPI app created")

# %% Start server with ngrok
# -----------------------------------------------------------
# IMPORTANT: Set your ngrok auth token below
# Get a free token at: https://dashboard.ngrok.com/signup
# -----------------------------------------------------------
NGROK_AUTH_TOKEN = ""  # <-- PASTE YOUR TOKEN HERE

import nest_asyncio
nest_asyncio.apply()

if NGROK_AUTH_TOKEN:
    from pyngrok import ngrok, conf
    conf.get_default().auth_token = NGROK_AUTH_TOKEN
    tunnel = ngrok.connect(8000)
    public_url = tunnel.public_url
else:
    # Try without auth (might work on some Colab setups)
    try:
        from pyngrok import ngrok
        tunnel = ngrok.connect(8000)
        public_url = tunnel.public_url
    except Exception:
        public_url = "http://localhost:8000"
        print("⚠️  ngrok not configured. Set NGROK_AUTH_TOKEN above.")
        print("   Get a free token: https://dashboard.ngrok.com/signup")

print("\n" + "="*60)
print("🚀 StyleSense AI Backend is LIVE!")
print("="*60)
print(f"\n   📡 Public URL: {public_url}")
print(f"\n   Paste this in your .env file:")
print(f"   COLAB_API_URL={public_url}")
print(f"\n   Test it: {public_url}/api/health")
print("="*60 + "\n")

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)
