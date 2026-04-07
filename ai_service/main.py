"""
main.py — CleanCity AI Detection FastAPI Service
===================================================
Garbage detection API using custom YOLOv8 model
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import base64
import numpy as np
import cv2

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="CleanCity AI Detection Service",
    version="5.0.0"
)

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Load Detector
detector = None


@app.on_event("startup")
async def startup_event():
    global detector
    try:
        from detector import GarbageDetector
        detector = GarbageDetector("best.pt")
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Error loading model: {e}")


# 📦 Request Models
class FrameRequest(BaseModel):
    frame: str


class LiveFrameRequest(BaseModel):
    frame: str
    camera_id: str
    camera_name: Optional[str] = "Camera"
    latitude: Optional[float] = 0.0
    longitude: Optional[float] = 0.0


# ❤️ Health Check
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": detector is not None
    }


# 🖼️ IMAGE UPLOAD
@app.post("/detect-image")
async def detect_image(file: UploadFile = File(...)):
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        img_bytes = await file.read()

        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = detector.detect_frame(frame)

        # Convert image to base64
        _, buffer = cv2.imencode(".jpg", result["frame"])
        img_b64 = base64.b64encode(buffer).decode()

        return {
            "success": True,
            "detections": result["detections"],
            "labels": result["labels"],
            "total": result["total"],
            "detected": result["detected"],
            "image": img_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🎥 BASE64 FRAME
@app.post("/detect-frame")
async def detect_frame(req: FrameRequest):
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        b64 = req.frame.split(",")[1] if "," in req.frame else req.frame
        img_bytes = base64.b64decode(b64)

        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = detector.detect_frame(frame)

        _, buffer = cv2.imencode(".jpg", result["frame"])
        img_b64 = base64.b64encode(buffer).decode()

        return {
            "success": True,
            "detected": result["detected"],
            "labels": result["labels"],
            "total": result["total"],
            "image": img_b64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 📡 LIVE CCTV API
@app.post("/detect-frame-live")
async def detect_live(req: LiveFrameRequest):
    if detector is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        b64 = req.frame.split(",")[1] if "," in req.frame else req.frame
        img_bytes = base64.b64decode(b64)

        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = detector.detect_frame(frame)

        return {
            "success": True,
            "camera_id": req.camera_id,
            "camera_name": req.camera_name,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "detected": result["detected"],
            "labels": result["labels"],
            "total": result["total"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🚀 RUN SERVER
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)