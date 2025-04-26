# Object Detection Application - Windows Version

This application uses YOLOv8 to detect objects in images and crop them automatically.

## Installation

### Option 1: Using the Pre-built Binary

1. Extract the zip file to any location on your computer
2. Double-click `run_app.bat` to start the application

### Option 2: Building from Source

If you want to build the application yourself, see `build_windows.md` for detailed instructions.

## Using the Application

1. When you start the application, it will prompt you to select a folder containing images
2. Select a folder with JPG, JPEG, PNG, BMP, or GIF images
3. The application will process all images in the folder
4. Cropped images will be saved to an `output` subfolder within your selected folder
5. A completion message will display when finished

## Troubleshooting

- If the application doesn't start, try running it as administrator
- Make sure your antivirus software isn't blocking the application
- If you encounter errors with specific images, ensure they're valid image files
- For further assistance, please contact support

## Technical Details

- This application uses YOLOv8 for object detection
- It's built with Python and packaged using PyInstaller
- All processing is done locally on your machine (no internet connection required)
- The application needs approximately 1GB of RAM to run efficiently
