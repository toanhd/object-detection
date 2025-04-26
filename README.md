# Object Detection Application

A simple desktop application for detecting and cropping objects from images using YOLOv8.

## Features

- Loads either a custom trained YOLOv8 model or falls back to default YOLOv8n
- Processes images from the "footage" directory
- Crops detected objects and saves them to the "output" directory

## Using the Packaged Application

### Prerequisites

The packaged application contains all necessary dependencies and should run without installing Python or any packages.

### Running the Application

1. Download the latest release from the releases page or use the packaged application in `dist/object_detection/`
2. Place your images in the `footage` folder inside the application directory
3. Run the application by double-clicking the `object_detection` executable
4. The processed images will be saved in the `output` folder

### Custom Model

The application will look for a trained model at `weights/best.pt`. If the model is not found, it will use the default YOLOv8n model.

To use your own model:

1. Place your trained YOLOv8 model in the `weights` folder named as `best.pt`
2. Run the application as usual

## Building from Source

If you want to build the application yourself:

1. Install the required packages:

   ```
   pip install ultralytics pillow pyinstaller
   ```

2. Run the build script:

   ```
   python build.py
   ```

3. The packaged application will be available in the `dist/object_detection` directory
