# Place your YOLO fashion model here
# 
# For V1, the application runs in DEMO_MODE by default.
# When you're ready to use a real model:
#
# 1. Download or train a YOLO model for fashion detection
#    - Option A: Use a pretrained YOLOv8 model (yolov8n.pt, yolov8s.pt, etc.)
#    - Option B: Fine-tune on a fashion dataset like DeepFashion2
#
# 2. Place the .pt file in this directory
#    Example: models/yolo_fashion.pt
#
# 3. Update .env:
#    DEMO_MODE=false
#    YOLO_MODEL_PATH=models/yolo_fashion.pt
#
# 4. Install ultralytics: pip install ultralytics
#
# 5. Restart the backend server
#
# Recommended fashion datasets for fine-tuning:
# - DeepFashion2: https://github.com/switchablenorms/DeepFashion2
# - ModaNet: https://github.com/eBay/modanet
# - Fashionpedia: https://fashionpedia.github.io/home/
