"""
live_monitor.py — Live Garbage Detection Monitor (FINAL)
========================================================
Works with your custom detector.py (best.pt)
Supports: webcam, droidcam, rtsp, youtube, video
"""

import argparse
import os
import sys
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import cv2

from camera import open_source, VideoStream, extract_youtube_stream
from detector import GarbageDetector
from utils import frame_to_base64, save_evidence


# ─── CONFIG ─────────────────────────────────────────────

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")
DETECTION_API_KEY = os.environ.get("DETECTION_API_KEY", "cleancity-detection-key")

PROCESS_EVERY_N = 3
FRAME_WIDTH = 1080
CONFIDENCE_THRESHOLD = 0.4
ALERT_COOLDOWN = 30


# ─── BACKEND ────────────────────────────────────────────

def send_to_backend(data: dict):
    try:
        r = requests.post(
            f"{BACKEND_URL}/api/detections",
            json=data,
            headers={"x-api-key": DETECTION_API_KEY},
            timeout=5
        )
        print(f"  📡 Backend: {r.status_code}")
    except Exception as e:
        print(f"  ❌ Backend error: {e}")


# ─── MAIN LOOP ──────────────────────────────────────────

def run_monitor(args):

    print("\n🏙️ CleanCity Live Monitor Started\n")

    cap, source_label, reconnect_url = open_source(
        args.source, url=args.url, file=args.file
    )

    if not cap.isOpened():
        print("❌ Camera not opened")
        sys.exit(1)

    print(f"📹 Source: {source_label}")

    # 🔥 Load your model
    detector = GarbageDetector("best.pt")

    frame_count = 0
    last_alert = 0

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("⚠️ Reconnecting...")
                cap.release()
                time.sleep(2)
                cap = VideoStream(reconnect_url)
                continue

            frame_count += 1

            # Resize for speed
            h, w = frame.shape[:2]
            scale = FRAME_WIDTH / w
            frame = cv2.resize(frame, (FRAME_WIDTH, int(h * scale)))

            # Skip frames
            if frame_count % PROCESS_EVERY_N != 0:
                continue

            # ── DETECTION ──
            result = detector.detect_frame(frame)

            detected = result["detected"]
            labels = result["labels"]
            total = result["total"]
            annotated = result["frame"]

            timestamp = datetime.now().strftime("%H:%M:%S")

            if detected:
                print(f"[{timestamp}] 🚨 DETECTED → {labels} ({total})")

                # Save evidence
                save_evidence(annotated, args.camera_id)

                # Send backend alert (cooldown)
                if time.time() - last_alert > ALERT_COOLDOWN:
                    send_to_backend({
                        "imageBase64": frame_to_base64(annotated),
                        "cameraId": args.camera_id,
                        "cameraName": args.camera_name,
                        "latitude": args.lat,
                        "longitude": args.lng,
                        "detectedObjects": labels,
                        "total": total
                    })
                    last_alert = time.time()

            # ── DISPLAY ──
            if args.display:

                # Banner
                color = (0, 0, 255) if detected else (0, 255, 0)
                text = "GARBAGE DETECTED 🚨" if detected else "NO GARBAGE"

                overlay = annotated.copy()
                cv2.rectangle(overlay, (0, 0), (FRAME_WIDTH, 40), color, -1)
                cv2.addWeighted(overlay, 0.4, annotated, 0.6, 0, annotated)

                cv2.putText(annotated, text, (10, 28),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (255, 255, 255), 2)

                cv2.imshow("CleanCity Monitor", annotated)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        print("\nStopped")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Closed cleanly")


# ─── CLI ───────────────────────────────────────────────

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--source", default="webcam",
                        choices=["webcam", "droidcam", "rtsp", "youtube", "video"])

    parser.add_argument("--url", help="camera URL")
    parser.add_argument("--file", help="video file")

    parser.add_argument("--camera-id", default="cam-001")
    parser.add_argument("--camera-name", default="Main Camera")

    parser.add_argument("--lat", type=float, default=18.5204)
    parser.add_argument("--lng", type=float, default=73.8567)

    parser.add_argument("--no-display", dest="display", action="store_false")
    parser.set_defaults(display=True)

    args = parser.parse_args()

    run_monitor(args)