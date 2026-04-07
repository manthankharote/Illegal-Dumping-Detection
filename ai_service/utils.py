"""
utils.py — Small helper functions
===================================
"""

import cv2
import base64
from datetime import datetime
from pathlib import Path

# Evidence folder for saving detection screenshots
EVIDENCE_DIR = Path("evidence")
EVIDENCE_DIR.mkdir(exist_ok=True)


def frame_to_base64(frame) -> str:
    """Convert an OpenCV BGR frame to a base64 JPEG string."""
    _, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode('utf-8')


def save_evidence(frame, camera_id: str) -> str:
    """Save a detection screenshot and return the file path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{camera_id}_{ts}.jpg"
    filepath = EVIDENCE_DIR / filename
    cv2.imwrite(str(filepath), frame)
    return str(filepath)
