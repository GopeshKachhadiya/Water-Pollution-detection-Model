
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from ultralytics import YOLO
from datetime import datetime
import shutil
import uuid
import os

# Agent pipeline
from agent_system.pipeline import process_detection

# APP INIT
app = FastAPI(title="Underwater Pollution Intelligence API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best (1).pt")

model = YOLO(MODEL_PATH)

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# MAIN API
@app.post("/detect/")
async def detect_trash(
    file: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    depth: float = Form(None)
):
    timestamp = datetime.utcnow().isoformat()

    # SAVE UPLOADED IMAGE
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # RUN YOLO
    results = model.predict(
        filepath,
        conf=0.25,
        save=True,
        save_crop=True
    )

    detections = []
    agent_responses = []

    # PROCESS YOLO RESULTS
    for r in results:
        if not r.boxes:
            continue

        for i, box in enumerate(r.boxes):
            class_name = r.names[int(box.cls[0])]
            confidence = float(box.conf[0])

            # YOLO crop path
            crop_path = None
            if r.save_dir:
                crop_path = os.path.join(
                    r.save_dir,
                    "crops",
                    class_name,
                    f"{i}.jpg"
                )

            # YOLO DETECTION RECORD
            detection_record = {
                "datetime": timestamp,
                "lat": latitude,
                "lon": longitude,
                "depth": depth,
                "class": class_name,
                "confidence": round(confidence, 4),
                "image_clip": crop_path
            }

            detections.append(detection_record)

            # AGENT PAYLOAD
            detection_payload = {
                "timestamp": timestamp,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "depth_m": depth
                },
                "detections": [
                    {
                        "class": class_name,
                        "confidence": confidence
                    }
                ],
                "image_proof_path": crop_path or filepath
            }
            # CALL GEMINI AGENT
            try:
                agent_results = process_detection(detection_payload)

                if isinstance(agent_results, list):
                    agent_responses.extend(agent_results)
                else:
                    agent_responses.append(agent_results)

            except Exception as e:
                agent_responses.append({
                    "severity": "N/A",
                    "analysis": None,
                    "report": None,
                    "error": str(e)
                })

    # FINAL API RESPONSE (STREAMLIT)
    print(" FINAL API RESPONSE:", {
    "detections": detections,
    "agent_results": agent_responses
    })

    return {
        "status": "success",
        "total_detections": len(detections),
        "detections": detections,
        "agent_results": agent_responses
    }
