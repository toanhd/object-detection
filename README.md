# Object Detection Application

A simple desktop application for detecting and cropping objects from images using YOLOv8.

## Features

- Loads either a custom trained YOLOv8 model or falls back to default YOLOv8n
- User-friendly graphical interface with progress tracking
- Interactive folder selection dialog
- Real-time processing status with cancel option
- Processes images from any user-selected folder
- Crops detected objects and saves them to an "output" subfolder

## Using the Application

> **Note:** When cloning this repository from Git, the build and dist folders are excluded.
> You must build the application from source as described in the "Building from Source" section below.

### Prerequisites

The packaged application contains all necessary dependencies and should run without installing Python or any packages.

### Running After Building

1. Navigate to the `dist/object_detection/` directory after building
2. Run the application by double-clicking the `object_detection` executable
3. When prompted, select a folder containing your images
4. The application will show progress as it processes each image
5. You can cancel processing at any time using the Cancel button
6. The processed images will be saved in the `output` subfolder of your selected directory
7. A summary will display when complete, and the application will close automatically

### Custom Model

The application will look for a trained model at `best.pt` in the application directory. If the model is not found, it will use the default YOLOv8n model.

To use your own model:

1. Place your trained YOLOv8 model in the application directory named as `best.pt`
2. Run the application as usual

## Building from Source

Building from source is required when cloning this repository:

1. Clone the repository and navigate to the project directory
2. Install the required packages:

   ```
   pip install ultralytics pillow pyinstaller
   ```

3. Run the build script:

   ```
   python build.py
   ```

4. The packaged application will be available in the `dist/object_detection` directory

For platform-specific build instructions, see:

- `build_windows.md` for Windows build details
