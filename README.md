# 🌊 Water Pollution Intelligence — AI-Powered Water Contamination Detection System

> **YOLOv8-powered water pollution detection with a multi-agent analysis pipeline** — upload water body images and get instant AI-driven contamination analysis, built with Python, FastAPI, and Streamlit.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Model Information](#model-information)

---

## 🔍 Overview

**Water Pollution Intelligence** is an AI-powered system designed to detect and analyze water pollution and aquatic trash in images using a custom-trained YOLOv8 object detection model. The system combines a powerful FastAPI backend for inference with an interactive Streamlit dashboard for visualization, coordinated through a multi-agent pipeline that classifies contamination types and generates analytical reports.

This tool is designed for environmental researchers, water quality monitoring agencies, and smart city initiatives that need automated, scalable water body inspection.

---

## ✨ Features

- 🔍 **YOLOv8 Object Detection** — Custom-trained model to detect pollution, trash, and contaminants in water bodies
- 🤖 **Multi-Agent Analysis Pipeline** — Specialized agents for detection, classification, and reporting
- 📊 **Interactive Dashboard** — Streamlit-based UI for image upload, visualization, and results
- ⚡ **FastAPI Backend** — High-performance REST API for real-time inference requests
- 🏷️ **Contamination Classification** — Categorizes detected objects (plastic, chemical, biological, etc.)
- 📈 **Confidence Scoring** — Bounding box detections with confidence percentages
- 🖼️ **Visual Results** — Annotated output images with detection overlays

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend / Dashboard** | [Streamlit](https://streamlit.io/) |
| **Backend API** | [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/) |
| **Object Detection** | [YOLOv8](https://github.com/ultralytics/ultralytics) (Custom trained model) |
| **Image Processing** | [OpenCV](https://opencv.org/), [Pillow](https://pillow.readthedocs.io/) |
| **Agent System** | Custom Python agentic pipeline |
| **Language** | Python 3.10+ |

---

## 🏗️ Architecture

```
Water-Pollution-detection-Model/
├── app.py                      # FastAPI backend — image detection API
├── frontend.py                 # Streamlit dashboard UI
├── agent_system/               # Multi-agent analysis pipeline
│   ├── detection_agent.py      # Runs YOLOv8 inference
│   ├── classification_agent.py # Classifies contamination types
│   └── report_agent.py         # Generates analysis report
├── models/
│   └── best (1).pt             # Custom-trained YOLOv8 weights
├── uploads/                    # Temporary uploaded image storage
├── runs/detect/predict/        # YOLOv8 detection output frames
├── requirements.txt
└── .env
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- pip package manager
- CUDA-compatible GPU (optional, for faster inference)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/GopeshKachhadiya/Water-Pollution-detection-Model.git
cd Water-Pollution-detection-Model

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Start the FastAPI backend
uvicorn app:app --reload --port 8000

# 6. In a new terminal, launch the Streamlit dashboard
streamlit run frontend.py
```

---

## 🚀 Usage

### Via Streamlit Dashboard
1. Open `http://localhost:8501` in your browser
2. Click **"Upload Image"** and select a water body photo (JPG/PNG)
3. Click **"Analyze"** to run the detection pipeline
4. View:
   - Annotated image with bounding boxes around detected pollution
   - List of detected objects with confidence scores
   - Contamination classification report from the agent pipeline

### Via FastAPI (REST API)

```bash
# Run inference on an image
curl -X POST http://localhost:8000/detect/ \
  -F "file=@water_sample.jpg" \
  -F "latitude=23.0" \
  -F "longitude=72.0" \
  -F "depth=5.0"
```

**Response:**
```json
{
  "status": "success",
  "total_detections": 1,
  "detections": [
    {
      "datetime": "2026-03-01T12:00:00.000000",
      "lat": 23.0,
      "lon": 72.0,
      "depth": 5.0,
      "class": "plastic_bottle",
      "confidence": 0.91,
      "image_clip": "runs/detect/predict/crops/plastic_bottle/0.jpg"
    }
  ],
  "agent_results": [
    {
      "severity": "HIGH",
      "analysis": "Agent analysis here",
      "report": "Agent report here"
    }
  ]
}
```

---

## 🧠 Model Information

| Property | Details |
|----------|---------|
| **Architecture** | YOLOv8 (Custom) |
| **Task** | Object Detection |
| **Input** | RGB Images (any resolution) |
| **Output** | Bounding boxes + class labels + confidence scores |
| **Weights File** | `best (1).pt` |
| **Training Data** | Custom annotated water pollution dataset |

---

## 📄 License

Open source — for environmental research and monitoring purposes.

---

<div align="center">Built with ❤️ for cleaner water and a healthier planet 🌍</div>
