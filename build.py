"""
Build script for creating the object detection application executable.
Handles both Windows and macOS/Linux builds automatically.
"""

import platform
import subprocess
from pathlib import Path

print("Object Detection App Build Script")
print("=================================")

# Detect the operating system
operating_system = platform.system()
print(f"Detected operating system: {operating_system}")

# Check if model exists, warn if not
if not Path("best.pt").exists():
    print("Warning: best.pt not found. The packaged app will use the default YOLOv8n model.")

# Select the appropriate spec file based on the OS
if operating_system == "Windows":
    spec_file = "object_detection_windows.spec"
    if not Path(spec_file).exists():
        print(f"Warning: {spec_file} not found, creating a basic spec file.")
        # Create a basic spec file if it doesn't exist
        subprocess.run([
            "pyinstaller", 
            "--name=object_detection", 
            "--onedir", 
            "--windowed", 
            "main.py"
        ])
else:
    # macOS or Linux
    spec_file = "object_detection.spec"
    if not Path(spec_file).exists():
        print(f"Warning: {spec_file} not found, creating a basic spec file.")
        # Create a basic spec file if it doesn't exist
        subprocess.run([
            "pyinstaller", 
            "--name=object_detection", 
            "--onedir", 
            "--windowed", 
            "main.py"
        ])

# Run PyInstaller with the appropriate spec file
print(f"Starting build process using {spec_file}...")
try:
    subprocess.run(["pyinstaller", spec_file, "--noconfirm"], check=True)
    print("Build complete!")
    
    # Print the location of the built application
    if operating_system == "Windows":
        print("Executable is in the dist\\object_detection directory.")
    else:
        print("Executable is in the dist/object_detection directory.")
        
except subprocess.CalledProcessError as e:
    print(f"Build failed with error: {e}")
    exit(1)
