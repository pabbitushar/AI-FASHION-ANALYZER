# StyleSense AI

> Analyze an outfit. Understand its composition. Explore its style.

StyleSense AI is a fashion-analysis web application that takes an outfit image and identifies clothing items, analyzes dominant colors, and generates a style classification.

## Overview

Upload an outfit image and the application:

1. Detects clothing and fashion-related objects
2. Extracts dominant colors
3. Analyzes the detected clothing and colors
4. Generates a style classification

## Architecture

```text
Browser
   │
   ▼
React + Vite
   │
   ▼
FastAPI Backend
   │
   ▼
Analysis Service
   │
   ▼
Google Colab
   │
   ├── YOLOS-Fashionpedia
   │       └── Clothing Detection
   │
   ├── K-Means
   │       └── Color Extraction
   │
   └── Rule-Based Logic
           └── Style Classification
```

## Features

* Clothing and accessory detection
* 27 fashion categories
* Dominant color extraction
* Detection confidence scores
* Style classification
* Responsive interface
* Demo mode
* GPU-based inference through Google Colab

## Tech Stack

**Frontend**

React · TypeScript · Vite · Tailwind CSS · Framer Motion

**Backend**

Python · FastAPI · Pydantic

**Computer Vision**

YOLOS-Fashionpedia · K-Means clustering

**Infrastructure**

Google Colab · ngrok

## Detection Categories

The current model supports 27 fashion categories:

| Clothing       | Accessories | Footwear |
| -------------- | ----------- | -------- |
| Shirt / Blouse | Glasses     | Shoes    |
| T-Shirt        | Hat         | Socks    |
| Sweater        | Headband    | Tights   |
| Cardigan       | Tie         |          |
| Jacket         | Gloves      |          |
| Vest           | Watch       |          |
| Pants          | Belt        |          |
| Shorts         | Bag         |          |
| Skirt          | Scarf       |          |
| Coat           | Umbrella    |          |
| Dress          |             |          |
| Jumpsuit       |             |          |
| Cape           |             |          |

## Project Structure

```text
StyleSense-AI/
│
├── colab/
│   └── stylesense_colab.py
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── ml/
│   └── utils/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── hooks/
│       ├── pages/
│       ├── services/
│       └── types/
│
├── models/
├── .env.example
└── README.md
```

## Setup

### 1. Start the Colab inference service

Upload:

```text
colab/stylesense_colab.py
```

to Google Colab.

Enable GPU:

```text
Runtime → Change runtime type → GPU
```

Add your ngrok authentication token and run the notebook.

Copy the generated ngrok URL.

### 2. Configure the backend

```powershell
```
