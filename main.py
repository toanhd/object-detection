"""Main module for object detection and image cropping using YOLOv8.

This module provides functionality to load a YOLOv8 model, detect objects in images,
and crop detected regions. It handles model loading, image processing, and includes
configuration for inference parameters.
"""

import sys
import time
import platform
from pathlib import Path
from typing import List, Tuple, Optional

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ultralytics import YOLO
from PIL import Image

# Constants
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
INF_PARAMETERS = {
    "imgsz": 640,  # image size
    "conf": 0.8,   # confidence threshold
    "max_det": 1   # maximum number of detections
}

class ProcessingState:
    """Class to manage processing state and UI components."""
    
    def __init__(self):
        self.window: Optional[tk.Tk] = None
        self.progress_bar: Optional[ttk.Progressbar] = None
        self.count_label: Optional[tk.Label] = None
        self.file_label: Optional[tk.Label] = None
        self.cancelled: bool = False
        
    def cancel(self):
        """Mark processing as cancelled."""
        self.cancelled = True


def get_application_path() -> Path:
    """Get the application path that works with PyInstaller.

    Returns:
        Path: The path to the application.
    """
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller bundle
        base_path = getattr(sys, '_MEIPASS', None)
        if base_path:
            return Path(base_path)
        return Path.cwd()
    # Running as a regular Python script
    return Path.cwd()


def select_footage_folder() -> Path:
    """Prompt the user to select a footage folder.
    
    Returns:
        Path: The selected footage folder path or default footage folder if canceled.
    """
    # Create a root window but keep it hidden
    folder_selector_root = tk.Tk()
    folder_selector_root.withdraw()
    
    # Create messagebox to explain the folder selection
    messagebox.showinfo(
        "Select Footage Folder", 
        "Please select a folder containing images to process.\n\n"
        "Images will be processed and output files will be saved in an 'output' subfolder."
    )
    
    # Open folder selection dialog
    folder_path = filedialog.askdirectory(
        title="Select Footage Folder",
        initialdir=str(Path.home().joinpath("Desktop"))
    )
    
    # If the user cancels, use the default footage folder
    if not folder_path:
        print("No folder selected, using default footage folder.")
        return Path("footage")
    
    # Return the selected folder path
    return Path(folder_path)


def show_splash_screen() -> Tuple[tk.Tk, ttk.Progressbar]:
    """Show a splash screen while the application is starting.
    
    Returns:
        Tuple[tk.Tk, ttk.Progressbar]: The splash window and progress bar.
    """
    # Create splash window
    splash_root = tk.Tk()
    splash_root.title("Object Detection")
    splash_root.geometry("400x200")
    splash_root.resizable(False, False)
    
    # Only use overrideredirect on Windows, not on macOS
    if platform.system() == 'Windows':
        splash_root.overrideredirect(True)  # Remove window decorations
    
    # Center the window
    window_width = 400
    window_height = 200
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    splash_root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
    # Add border
    splash_root.configure(bg="#3c3c3c")
    main_frame = tk.Frame(splash_root, bd=2, relief=tk.RIDGE, bg="#f0f0f0")
    main_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
    
    # Add app title
    title_label = tk.Label(main_frame, text="Object Detection App", font=("Arial", 18, "bold"), bg="#f0f0f0")
    title_label.pack(pady=(25, 10))
    
    # Add loading message
    loading_label = tk.Label(main_frame, text="Loading application...", font=("Arial", 12), bg="#f0f0f0")
    loading_label.pack(pady=5)
    
    # Add loading bar
    progress = ttk.Progressbar(main_frame, orient="horizontal", length=350, mode="indeterminate")
    progress.pack(pady=20)
    progress.start(10)
    
    # Update the window
    splash_root.update()
    
    return splash_root, progress


def get_image_files(folder_path: Path) -> List[Path]:
    """Get list of image files from the folder path.
    
    Args:
        folder_path: Path to folder containing images
        
    Returns:
        List of image file paths
    """
    if not (folder_path.exists() and folder_path.is_dir()):
        print(f"Warning: {folder_path} is not a valid directory")
        return []
        
    return [
        path for path in folder_path.iterdir()
        if path.is_file()
        and not path.name.startswith('.') 
        and path.suffix.lower() in SUPPORTED_FORMATS
    ]


def detect_and_crop(image: Image.Image, model: YOLO) -> Image.Image:
    """Detect objects and crop the image.

    Args:
        image: The input image to detect objects in.
        model: The YOLOv8 model to use for detection.

    Returns:
        The cropped image with detected objects.
    """
    results = model.predict(image, **INF_PARAMETERS)
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

def create_progress_window(total_images: int, state: ProcessingState) -> tk.Tk:
    """Create a window to show processing progress.
    
    Args:
        total_images: Total number of images to process
        state: Processing state object to update
        
    Returns:
        Progress window
    """
    # Reset cancellation state
    state.cancelled = False
    
    # Create progress window
    progress_root = tk.Tk()
    progress_root.title("Processing Images")
    progress_root.geometry("500x200")
    progress_root.resizable(False, False)
    state.window = progress_root
    
    # Center the window
    window_width = 500
    window_height = 200
    screen_width = progress_root.winfo_screenwidth()
    screen_height = progress_root.winfo_screenheight()
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    progress_root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
    # Add labels and progress bar
    main_label = tk.Label(progress_root, text="Processing Images", font=("Arial", 14, "bold"))
    main_label.pack(pady=(15, 5))
    
    state.count_label = tk.Label(progress_root, text=f"Image 0 of {total_images}", font=("Arial", 10))
    state.count_label.pack(pady=(0, 5))
    
    state.file_label = tk.Label(progress_root, text="", font=("Arial", 9), fg="blue")
    state.file_label.pack(pady=(0, 5))
    
    state.progress_bar = ttk.Progressbar(progress_root, orient="horizontal", length=450, mode="determinate")
    state.progress_bar.pack(pady=10)
    state.progress_bar["maximum"] = total_images
    state.progress_bar["value"] = 0
    
    # Add cancel button
    def cancel_processing():
        state.cancel()
        cancel_button.config(text="Cancelling...", state="disabled")
    
    cancel_button = tk.Button(progress_root, text="Cancel", command=cancel_processing)
    cancel_button.pack(pady=10)
    
    # Don't let the window close automatically
    progress_root.protocol("WM_DELETE_WINDOW", cancel_processing)
    
    # Update the window
    progress_root.update()
    
    return progress_root


def update_progress(current_index: int, filename: str, state: ProcessingState) -> None:
    """Update the progress window with current processing status.
    
    Args:
        current_index: Current image index (0-based)
        filename: Name of current file being processed
        state: Processing state object
    """
    # Truncate filename if too long
    display_name = filename
    if len(display_name) > 50:
        display_name = display_name[:20] + "..." + display_name[-25:]
    
    # Update UI elements
    if state.window is None or state.count_label is None or state.file_label is None or state.progress_bar is None:
        return
        
    state.count_label.config(text=f"Image {current_index + 1} of {state.progress_bar['maximum']}")
    state.file_label.config(text=f"Processing: {display_name}")
    state.progress_bar["value"] = current_index
    
    # Update the window
    state.window.update()


def close_progress_window(state: ProcessingState) -> None:
    """Close the progress window.
    
    Args:
        state: Processing state object
    """
    if state.window is not None:
        state.window.destroy()
        state.window = None


def process_images(image_paths: List[Path], output_dir: Path, model: YOLO) -> str:
    """Process a batch of images and save cropped versions.

    Args:
        image_paths: List of image file paths to process.
        output_dir: Directory where processed images will be saved.
        model: The YOLOv8 model to use for detection.

    Returns:
        A message indicating the status of the processing.
    """
    if not image_paths:
        print("No images found to process.")
        return "No images processed"
        
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Create processing state object and progress window
    state = ProcessingState()
    create_progress_window(len(image_paths), state)
    
    processed_count = 0
    for i, img_path in enumerate(image_paths):
        # Check if processing was cancelled
        if state.cancelled:
            close_progress_window(state)
            return f"Processing cancelled: {processed_count} of {len(image_paths)} images processed"
        
        # Update progress
        update_progress(i, str(img_path.name), state)
        
        try:
            # Open image
            img = Image.open(img_path)
            # Detect and crop
            cropped_img = detect_and_crop(img, model)
            # Save or process further as needed
            output_path = output_dir / f"{img_path.stem}_cropped{img_path.suffix}"
            cropped_img.save(output_path)
            print(f"Processed: {img_path} -> {output_path}")
            processed_count += 1
            
            # Short delay to make progress visible for very fast operations
            time.sleep(0.1)
        except (FileNotFoundError, PermissionError) as e:
            print(f"File error for {img_path}: {e}")
        except (OSError, Image.UnidentifiedImageError) as e:
            print(f"Image error for {img_path}: {e}")
        except ValueError as e:
            print(f"Value error for {img_path}: {e}")
    
    # Close progress window
    close_progress_window(state)
    
    return f"Processing complete: {processed_count} images processed"


def main() -> None:
    """Main function to run the application."""
    # Show splash screen
    splash, splash_progress = show_splash_screen()
    
    # Load the model (keep splash screen visible during model loading)
    app_path = get_application_path()
    weights_path = app_path / "best.pt"
    
    # Initialize model with appropriate weights
    model = None
    if weights_path.exists():
        print(f"Loading model from {weights_path}")
        model = YOLO(weights_path)
    else:
        print(f"Warning: {weights_path} not found. Using default YOLOv8n model.")
        model = YOLO('yolov8n.pt')  # Use default model
        
    # Close splash screen after model is loaded
    splash_progress.stop()
    splash.destroy()
    
    # Get input and output paths
    footage_path = select_footage_folder()
    print(f"Selected footage directory: {footage_path.absolute()}")
    
    # Create output directory as a subfolder of the selected folder
    output_path = footage_path / "output"
    output_path.mkdir(exist_ok=True)
    print(f"Output directory: {output_path.absolute()}")
    
    # Get image files from the selected folder
    image_files = get_image_files(footage_path)
    
    # Process images from selected folder
    if image_files:
        print(f"Found {len(image_files)} images to process in selected folder")
        result = process_images(image_files, output_path, model)
        
        # Show completion message
        message_root = tk.Tk()
        message_root.withdraw()
        messagebox.showinfo(
            "Processing Complete", 
            f"Processed {len(image_files)} images.\n"
            f"Output files saved to: {output_path.absolute()}"
        )
    else:
        print("No images found in the selected folder.")
        result = "No processing performed"
        
        # Show error message
        message_root = tk.Tk()
        message_root.withdraw()
        messagebox.showwarning(
            "No Images Found", 
            "No images found in the selected folder.\n"
            "Please try again with a folder containing images."
        )
    
    print(result)


if __name__ == "__main__":
    main()
    # Exit the application immediately
    sys.exit()
