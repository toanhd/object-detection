# Building the Object Detection App

This document explains how to build the Object Detection application into an executable package. The repository includes everything needed to automate the build process.

## Key Files

### build.py

The main build script that automates the build process:

- Detects your operating system automatically
- **Selects and executes the appropriate spec file automatically:**
  - `object_detection_windows.spec` for Windows
  - `object_detection.spec` for macOS and Linux
- Handles the entire PyInstaller process from start to finish

### Spec Files

#### object_detection_windows.spec

- Windows-specific PyInstaller configuration
- Configured with Windows-appropriate settings
- Includes the model file (best.pt) in the bundle
- Creates a windowed application (no console)

#### object_detection.spec

- macOS and Linux PyInstaller configuration
- Includes macOS-specific settings when built on macOS
- Configured for best compatibility across Unix-like systems
- Includes the model file (best.pt) in the bundle

## Quick Build Instructions

### Prerequisites

- Python 3.9 or newer
- Pip package manager

### Building Steps

1. Install required packages:

```bash
pip install ultralytics pillow pyinstaller
```

2. Run the build script:

```bash
python build.py
```

That's it! The script will:

1. Detect your operating system
2. Select the correct spec file for your platform
3. Run PyInstaller with the appropriate configuration
4. Place the built application in:
   - Windows: `dist\object_detection\`
   - macOS/Linux: `dist/object_detection/`

## Manual Build (Alternative)

If you prefer to run PyInstaller directly instead of using build.py:

### Windows

```cmd
pyinstaller object_detection_windows.spec --noconfirm
```

### macOS/Linux

```bash
pyinstaller object_detection.spec --noconfirm
```

## Troubleshooting

If the build fails:

1. Ensure all dependencies are installed
2. Check console output for specific errors
3. For Windows: try `pip install torch torchvision torchaudio`
4. For macOS/Linux: ensure you have appropriate permissions
