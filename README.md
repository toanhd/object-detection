# Object Detection Application

A simple desktop application for detecting and cropping objects from images using YOLOv8.

## Features

- Loads either a custom trained YOLOv8 model or falls back to default YOLOv8n
- User-friendly graphical interface with progress tracking
- Interactive folder selection dialog
- Real-time processing status with cancel option
- Processes images from any user-selected folder
- Crops detected objects and saves them to an "output" subfolder

## Overview

This application provides a simple interface for detecting objects in images using YOLOv8:

1. Select a folder containing images to process
2. The application detects objects and crops them automatically
3. Cropped images are saved to an output subfolder
4. Progress is displayed in real-time with the option to cancel
5. The application exits automatically when processing completes

## Custom Model

The application will look for a trained model at `best.pt` in the application directory. If the model is not found, it will use the default YOLOv8n model.

## Running from Source

If you prefer to run the application directly from source code rather than building an executable:

1. Create and activate a virtual environment:

   **Windows:**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required packages:

   ```bash
   pip install ultralytics pillow
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Building from Source

When cloning this repository from Git, you must build the application from source.

For detailed build instructions across all platforms (Windows, macOS, Linux), see:

- `build.md` - Comprehensive build documentation with platform-specific instructions

To automate the build process, a build script is provided:

- `build.py` - Python script that handles the build process

Basic build steps:

```bash
# Install required packages
pip install ultralytics pillow pyinstaller

# Run the build script
python build.py
```

The packaged application will be created in the `dist/object_detection` directory.
