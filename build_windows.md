# Building the Object Detection App for Windows

This document explains how to build the Object Detection app for Windows. Building from source is required when cloning this repository, as the build and dist folders are excluded from Git.

## Prerequisites

1. Windows 10 or 11
2. Python 3.9+ installed
3. Git (to clone the repository)

## Setup Environment

1. Clone the repository or download the source code:

   ```cmd
   git clone <repository-url>
   cd object-detection
   ```

2. Open Command Prompt as Administrator
3. Navigate to the project directory
4. Create and activate a virtual environment:

```cmd
python -m venv venv
venv\Scripts\activate
```

5. Install the required packages:

```cmd
pip install ultralytics pillow torch torchvision torchaudio pyinstaller
```

## Build the Application

1. Make sure you have the `best.pt` model file in the project root directory
   - If you don't have a custom model, the application will use the default YOLOv8n model
2. Create the required folders if they don't exist:

```cmd
mkdir footage
mkdir output
type nul > footage\.keep
type nul > output\.keep
```

3. Run PyInstaller with the Windows spec file:

```cmd
pyinstaller object_detection_windows.spec --noconfirm
```

If the spec file doesn't exist, you can use:

```cmd
pyinstaller --name=object_detection --onedir --windowed main.py
```

4. The built application will be in the `dist\object_detection` folder
5. Test the application by running `dist\object_detection\object_detection.exe`

## Application Features

The built application includes:

- Splash screen during startup
- GUI folder selection dialog
- Real-time progress tracking with cancel option
- Summary window upon completion

## Distribution

For simple distribution, you can zip the entire `dist\object_detection` folder.

For a more professional installer, you can use tools like:

- NSIS (Nullsoft Scriptable Install System)
- Inno Setup
- WiX Toolset

## Troubleshooting

If you encounter errors during the build:

1. Make sure all dependencies are installed
2. Check that the model file is in the correct location
3. Try building with console=True in the spec file to see any error messages
4. Update PyInstaller to the latest version
