"""Main module for object detection and image cropping using YOLOv8.

This module provides functionality to load a YOLOv8 model, detect objects in images,
and crop detected regions. It handles model loading, image processing, and includes
configuration for inference parameters.

Returns:
    None: This is a module file and doesn't return anything directly.
"""

import sys

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from ultralytics import YOLO
from PIL import Image

# Get the application directory (works with PyInstaller)
def get_application_path():
    """Get the application path.

    Returns:
        Path: The path to the application.
    """
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path:
            return Path(base_path)
        return Path.cwd()
    else:
        # Running as a regular Python script
        return Path.cwd()

def select_footage_folder():
    """Prompt the user to select a footage folder.
    
    Returns:
        Path: The selected footage folder path or default footage folder if canceled.
    """
    # Create a root window but keep it hidden
    root = tk.Tk()
    root.withdraw()
    
    # Create messagebox to explain the folder selection
    messagebox.showinfo(
        "Select Footage Folder", 
        "Please select a folder containing images to process.\n\n"
        "Images will be processed and output files will be saved in an 'output' subfolder."
    )
    
    # Open folder selection dialog
    folder_path = filedialog.askdirectory(
        title="Select Footage Folder",
        initialdir=str(Path.home())
    )
    
    # If the user cancels, use the default footage folder
    if not folder_path:
        print("No folder selected, using default footage folder.")
        return Path("footage")
    
    # Return the selected folder path
    return Path(folder_path)

# Load a pre-trained YOLO model - use yolov8n.pt if best.pt doesn't exist
app_path = get_application_path()
WEIGHTS_PATH = app_path / "best.pt"

# Initialize model with appropriate weights
if WEIGHTS_PATH.exists():
    print(f"Loading model from {WEIGHTS_PATH}")
    MODEL = YOLO(WEIGHTS_PATH)
else:
    print(f"Warning: {WEIGHTS_PATH} not found. Using default YOLOv8n model.")
    MODEL = YOLO('yolov8n.pt')  # Use default model

# Prompt user to select footage folder
IMAGES_PATH = select_footage_folder()
print(f"Selected footage directory: {IMAGES_PATH.absolute()}")

# Create output directory as a subfolder of the selected folder
OUTPUT_PATH = IMAGES_PATH / "output"
OUTPUT_PATH.mkdir(exist_ok=True)
print(f"Output directory: {OUTPUT_PATH.absolute()}")

INF_PARAMETERS = {
    "imgsz": 640,  # image size
    "conf": 0.8,   # confidence threshold
    "max_det": 1   # maximum number of detections
}

# Get images from the selected folder
# Filter out hidden files like .DS_Store
EXAMPLES = [
    path for path in IMAGES_PATH.iterdir()
    if IMAGES_PATH.exists() and IMAGES_PATH.is_dir()
    and not path.name.startswith('.')
    and path.is_file()
    and path.suffix.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
]


# Function to detect objects and crop the image
def detect_and_crop(image: Image.Image) -> Image.Image:
    """Detect objects and crop the image.

    Args:
        image (Image.Image): The input image to detect objects in.

    Returns:
        Image.Image: The cropped image with detected objects.
    """
    results = MODEL.predict(image, **INF_PARAMETERS)
    result = results[0]
    # Check if boxes exists and is not None
    if result.boxes is not None and hasattr(result.boxes, 'xyxy'):
        # Check if there are any detection boxes
        boxes = result.boxes.xyxy
        if len(boxes) > 0:
            # Get the first detected box
            box = boxes[0].cpu().numpy()
            # Crop the image to the box coordinates
            cropped_image = image.crop(box=(box[0], box[1], box[2], box[3]))
            return cropped_image
    # Return original image if no valid detection
    return image


# Function to process a batch of images
def process_images(image_paths, output_dir):
    """Process a batch of images and save cropped versions.

    Args:
        image_paths (list): List of image file paths to process.
        output_dir (Path): Directory where processed images will be saved.

    Returns:
        str: A message indicating the status of the processing.
    """
    if not image_paths:
        print("No images found to process.")
        return "No images processed"
        
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    processed_count = 0
    for img_path in image_paths:
        try:
            # Open image
            img = Image.open(img_path)
            # Detect and crop
            cropped_img = detect_and_crop(img)
            # Save or process further as needed
            output_path = output_dir / f"{img_path.stem}_cropped{img_path.suffix}"
            cropped_img.save(output_path)
            print(f"Processed: {img_path} -> {output_path}")
            processed_count += 1
        except (FileNotFoundError, PermissionError) as e:
            print(f"File error for {img_path}: {e}")
        except (OSError, Image.UnidentifiedImageError) as e:
            print(f"Image error for {img_path}: {e}")
        except ValueError as e:
            print(f"Value error for {img_path}: {e}")
    
    return f"Processing complete: {processed_count} images processed"


# Main execution
if __name__ == "__main__":
    # Process images from selected folder
    if EXAMPLES:
        print(f"Found {len(EXAMPLES)} images to process in selected folder")
        RESULT = process_images(EXAMPLES, OUTPUT_PATH)
        
        # Show completion message
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "Processing Complete", 
            f"Processed {len(EXAMPLES)} images.\n"
            f"Output files saved to: {OUTPUT_PATH.absolute()}"
        )
    else:
        print("No images found in the selected folder.")
        RESULT = "No processing performed"
        
        # Show error message
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "No Images Found", 
            "No images found in the selected folder.\n"
            "Please try again with a folder containing images."
        )
    
    print(RESULT)
