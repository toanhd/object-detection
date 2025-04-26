# Object Detection Application - Windows Version

This application uses YOLOv8 to detect objects in images and crop them automatically.

## Installation

> **Note:** When cloning this repository from Git, the build and dist folders are excluded.
> You must build the application from source as described below.

### Building from Source

To build the application from the source code:

1. Follow the detailed instructions in `build_windows.md`
2. This will create the executable in the `dist\object_detection` folder

### Releases

If you've downloaded a release package (not cloning from Git):

1. Extract the zip file to any location on your computer
2. Double-click `object_detection.exe` to start the application

## Using the Application

1. When you start the application, a splash screen will appear while the model loads
2. You will be prompted to select a folder containing images
3. Select a folder with JPG, JPEG, PNG, BMP, or GIF images
4. The application will show a progress window as it processes each image
   - You can monitor which image is currently being processed
   - You can cancel the process at any time using the Cancel button
5. Cropped images will be saved to an `output` subfolder within your selected folder
6. A completion summary will display when finished
7. The application will automatically close after processing

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
