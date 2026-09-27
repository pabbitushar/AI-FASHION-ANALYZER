# 🧠 StyleSense AI

AI-powered fashion analysis. Upload an outfit photo → get real clothing detection, color analysis, and style classification.

## Architecture

```
Browser (localhost:5173)
   ↓
React Frontend (Vite + Tailwind + Framer Motion)
   ↓
Python Backend (FastAPI, localhost:8000)
   ↓
Google Colab ML Backend (ngrok tunnel)
   → YOLOS-Fashionpedia model (27 clothing categories)
   → K-Means color extraction
   → Rule-based style classification
```

## Quick Start

### 1. Start the Colab ML Backend (for real detection)

1. Open [Google Colab](https://colab.research.google.com)
2. **File → Upload notebook** → upload `colab/stylesense_colab.py`
3. **Runtime → Change runtime type → GPU** (T4 is fine)
4. Get a free ngrok token: https://dashboard.ngrok.com/signup
5. Paste the token in the `NGROK_AUTH_TOKEN` variable in the notebook
6. **Run All** (Ctrl+F9)
7. Copy the printed ngrok URL (e.g. `https://abc123.ngrok-free.app`)

### 2. Configure the local backend

```powershell
cd backend
copy .env.example .env
```

Edit `.env` and paste your Colab URL:
```
COLAB_API_URL=https://abc123.ngrok-free.app
DEMO_MODE=true
```

> With `COLAB_API_URL` set, the backend uses Colab for real analysis and only falls back to demo mode if Colab is unreachable.

### 3. Install & run

**Terminal 1 — Backend:**
```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

### 4. Open the app

👉 **http://localhost:5173**

---

## Without Colab (Demo Mode)

If you don't set `COLAB_API_URL`, the app runs in demo mode — returns preset results for any image. Useful for testing the UI.

## Project Structure

```
├── colab/
│   └── stylesense_colab.py    ← Upload this to Google Colab
├── backend/
│   ├── main.py                ← FastAPI entry point
│   ├── config.py              ← Environment config
│   ├── api/routes.py          ← API endpoints
│   ├── models/schemas.py      ← Pydantic data models
│   ├── services/
│   │   └── analysis_service.py ← Orchestrator (Colab → YOLO → Demo)
│   ├── ml/
│   │   ├── base.py            ← Abstract FashionAnalyzer interface
│   │   ├── colab_analyzer.py  ← Bridges to Colab API
│   │   ├── yolo_analyzer.py   ← Local YOLO (stub for future)
│   │   ├── demo_analyzer.py   ← Mock results for testing
│   │   └── color_extractor.py ← K-Means color extraction
│   └── utils/image_utils.py   ← Image validation
├── frontend/
│   ├── src/
│   │   ├── components/        ← React UI components
│   │   ├── hooks/             ← useAnalysis state hook
│   │   ├── services/api.ts    ← API client
│   │   ├── types/             ← TypeScript interfaces
│   │   └── pages/Home.tsx     ← Main page
│   └── ...
├── models/                    ← Place YOLO .pt files here (future)
└── .env.example
```

## Analyzer Priority

The backend tries analyzers in this order:

1. **Colab** — if `COLAB_API_URL` is set and reachable → real ML analysis
2. **Local YOLO** — if `DEMO_MODE=false` and model file exists → local inference
3. **Demo** — preset results (always available)

## What the ML Detects

The Fashionpedia model recognizes 27 categories:

| Clothing | Accessories | Footwear |
|----------|------------|----------|
| Shirt/Blouse, T-Shirt, Sweater, Cardigan, Jacket, Vest, Pants, Shorts, Skirt, Coat, Dress, Jumpsuit, Cape | Glasses, Hat, Headband, Tie, Gloves, Watch, Belt, Bag, Scarf, Umbrella | Shoes, Socks, Tights |
