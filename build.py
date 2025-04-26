"""
Build script for creating the object detection application executable.
Ensures required directories exist before packaging.
"""

import subprocess
from pathlib import Path

# Ensure required directories exist
Path("output").mkdir(exist_ok=True)
Path("weights").mkdir(exist_ok=True)
Path("footage").mkdir(exist_ok=True)

# Check if model exists, warn if not
if not Path("weights/best.pt").exists():
    print("Warning: weights/best.pt not found. The packaged app will use yolov8n.pt.")

# Run PyInstaller
print("Starting build process...")
subprocess.run(["pyinstaller", "object_detection.spec"], check=True)
print("Build complete. Executable is in the dist/object_detection directory.")
