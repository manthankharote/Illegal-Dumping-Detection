# Use a lightweight python 3.10 base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install necessary system dependencies for cv2 (OpenCV)
# Without these, YOLO/OpenCV imports will typically crash in lightweight Linux containers
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies cleanly
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining source files
COPY . .

# Run inference.py as default command
CMD ["python", "inference.py"]
