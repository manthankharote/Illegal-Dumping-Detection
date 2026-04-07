"""
camera.py — Video Source Manager
==================================
Supports: webcam, droidcam, RTSP, YouTube live, video file.
Uses a threaded VideoStream for zero-latency frame capture.
"""

import os
os.environ["OPENCV_FFMPEG_LOGLEVEL"] = "-8"
os.environ["OPENCV_LOG_LEVEL"] = "OFF"

import cv2
import sys
import time
import threading
import subprocess


def extract_youtube_stream(url):
    """Extract direct stream URL from YouTube using yt-dlp."""
    print(f"  📺 Extracting YouTube stream: {url}")
    try:
        cmd = [
            "yt-dlp",
            "-f", "best[height<=480][ext=mp4]/best[height<=480]/worst",
            "-g", "--no-playlist",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        stream_url = result.stdout.strip()

        # Check if live
        cmd_live = ["yt-dlp", "--get-filename", "-o", "%(is_live)s", url]
        is_live = subprocess.run(cmd_live, capture_output=True, text=True).stdout.strip() == "True"

        return stream_url, is_live
    except Exception as e:
        print(f"  ❌ yt-dlp failed: {e}")
        return None, False


class VideoStream:
    """Threaded video capture — always holds the latest frame."""

    def __init__(self, src, backend=None):
        if backend is not None:
            self.stream = cv2.VideoCapture(src, backend)
        elif isinstance(src, str) and (src.startswith("http") or src.startswith("rtsp")):
            self.stream = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        else:
            self.stream = cv2.VideoCapture(src)

        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.grabbed = False
        self.frame = None
        self.lock = threading.Lock()
        self.stopped = False

        if self.stream.isOpened():
            self.grabbed, self.frame = self.stream.read()
            self.thread = threading.Thread(target=self._update, daemon=True)
            self.thread.start()

    def _update(self):
        while not self.stopped:
            try:
                grabbed, frame = self.stream.read()
                with self.lock:
                    self.grabbed = grabbed
                    self.frame = frame
                if not grabbed:
                    time.sleep(0.1)
            except Exception:
                with self.lock:
                    self.grabbed = False
                time.sleep(0.5)

    def read(self):
        with self.lock:
            if self.frame is not None:
                return self.grabbed, self.frame.copy()
            return False, None

    def isOpened(self):
        return self.stream.isOpened()

    def release(self):
        self.stopped = True
        self.stream.release()

    def set(self, prop, val):
        self.stream.set(prop, val)


def open_source(source, url=None, file=None):
    """
    Open a video source. Returns (VideoStream, label, reconnect_url).

    Args:
        source: "webcam", "droidcam", "rtsp", "youtube", or "video"
        url:    URL for droidcam / rtsp / youtube
        file:   file path for video
    """
    if source == "webcam":
        cap = None
        backends = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "MSMF"),
            (cv2.CAP_ANY, "Auto"),
        ]
        for backend, name in backends:
            for idx in range(3):
                print(f"  🔍 Trying webcam {idx} ({name})...")
                test = cv2.VideoCapture(idx, backend)
                if test.isOpened():
                    ret, frm = test.read()
                    test.release()
                    if ret and frm is not None:
                        cap = VideoStream(idx, backend)
                        print(f"  ✅ Webcam found: index {idx} ({name})")
                        return cap, f"Webcam (index {idx})", str(idx)
                else:
                    test.release()

        print("\n  ❌ No webcam detected!")
        print("  Try: python live_monitor.py --source droidcam --url http://PHONE_IP:4747/video")
        sys.exit(1)

    elif source == "droidcam":
        if not url:
            print("❌ --url is required for DroidCam")
            sys.exit(1)
        cap = VideoStream(url)
        if not cap.isOpened():
            for suffix in ["/video", "/mjpegfeed"]:
                test_url = url.rstrip('/') + suffix
                print(f"  🔍 Trying: {test_url}")
                cap = VideoStream(test_url)
                if cap.isOpened():
                    url = test_url
                    break
        return cap, f"DroidCam ({url})", url

    elif source == "rtsp":
        if not url:
            print("❌ --url is required for RTSP")
            sys.exit(1)
        return VideoStream(url), f"RTSP ({url})", url

    elif source == "youtube":
        if not url:
            print("❌ --url is required for YouTube")
            sys.exit(1)
        stream_url, is_live = extract_youtube_stream(url)
        if not stream_url:
            print("  ❌ Could not extract YouTube stream.")
            sys.exit(1)
        print(f"  ✅ Stream URL extracted")
        print(f"  📡 Type: {'YouTube Live' if is_live else 'YouTube Video'}")
        return VideoStream(stream_url), f"YouTube ({url})", url

    elif source == "video":
        if not file:
            print("❌ --file is required for video source")
            sys.exit(1)
        return VideoStream(file), f"Video ({file})", file

    else:
        print(f"❌ Unknown source: {source}")
        sys.exit(1)
