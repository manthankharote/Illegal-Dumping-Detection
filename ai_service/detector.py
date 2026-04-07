"""
detector.py — Garbage Detection using Custom YOLOv8 Model
==========================================================
Loads your trained best.pt and detects garbage in frames/images.
"""

import base64
import numpy as np
import cv2
from ultralytics import YOLO

# 🔥 Fix for PyTorch loading issue (important)
import torch
_original_load = torch.load
torch.load = lambda f, *a, **k: _original_load(f, *a, **{**k, "weights_only": False})


class GarbageDetector:

    def __init__(self, model_path="best.pt"):
        # 🔥 Use GPU if available
        self.device = 0 if torch.cuda.is_available() else "cpu"

        self.model = YOLO(model_path)

        print(f"✅ Model loaded on: {self.device}")
        print(f"Classes: {self.model.names}")

    # 🎯 MAIN FUNCTION (used everywhere)
    def detect_frame(self, frame, conf=0.4):

        results = self.model(frame, conf=conf, device=self.device)

        detections = []
        detected_labels = []
        annotated = frame.copy()

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                conf_score = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "label": label,
                    "confidence": round(conf_score, 3),
                    "bbox": [x1, y1, x2, y2]
                })

                detected_labels.append(label)

                # 🔴 Draw box
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 3)

                text = f"{label} ({conf_score:.2f})"
                cv2.putText(annotated, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 🚨 LOGIC (important for your project)
        garbage_detected = "garbage" in detected_labels

        return {
            "detected": garbage_detected,
            "labels": detected_labels,
            "total": len(detections),
            "detections": detections,
            "frame": annotated
        }

    # 📸 Camera helper
    def run_camera(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            result = self.detect_frame(frame)

            if result["detected"]:
                print("🚨 Garbage Detected!")

                # Save evidence
                cv2.imwrite("evidence.jpg", frame)

            cv2.imshow("Detection", result["frame"])

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    # 🌐 Base64 (for frontend/backend API)
    def detect_base64(self, b64_string):

        if "," in b64_string:
            b64_string = b64_string.split(",")[1]

        img_bytes = base64.b64decode(b64_string)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        result = self.detect_frame(frame)

        _, buffer = cv2.imencode(".jpg", result["frame"])
        result["image"] = base64.b64encode(buffer).decode()

        del result["frame"]

        return result