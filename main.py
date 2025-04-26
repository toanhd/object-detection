"""Main module for object detection and image cropping using YOLOv8.

This module provides functionality to load a YOLOv8 model, detect objects in images,
and crop detected regions. It handles model loading, image processing, and includes
configuration for inference parameters.

Returns:
    None: This is a module file and doesn't return anything directly.
"""

import sys
import time

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from ultralytics import YOLO
from PIL import Image

# Global progress tracking variables
PROGRESS_WINDOW = None
PROGRESS_LABEL = None
PROGRESS_BAR = None
PROGRESS_COUNT_LABEL = None
PROGRESS_CURRENT_FILE_LABEL = None
PROGRESS_CANCELLED = False

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

def show_splash_screen():
    """Show a splash screen while the application is starting."""
    # Create splash window
    splash_root = tk.Tk()
    splash_root.title("Object Detection")
    splash_root.geometry("400x200")
    splash_root.resizable(False, False)
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


def create_progress_window(total_images):
    """Create a window to show processing progress.
    
    Args:
        total_images (int): Total number of images to process
        
    Returns:
        tuple: References to progress window and its UI elements
    """
    global PROGRESS_WINDOW, PROGRESS_LABEL, PROGRESS_BAR, PROGRESS_COUNT_LABEL
    global PROGRESS_CURRENT_FILE_LABEL, PROGRESS_CANCELLED
    
    PROGRESS_CANCELLED = False
    
    # Create progress window
    progress_root = tk.Tk()
    progress_root.title("Processing Images")
    progress_root.geometry("500x200")
    progress_root.resizable(False, False)
    PROGRESS_WINDOW = progress_root
    
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
    
    PROGRESS_COUNT_LABEL = tk.Label(progress_root, text=f"Image 0 of {total_images}", font=("Arial", 10))
    PROGRESS_COUNT_LABEL.pack(pady=(0, 5))
    
    PROGRESS_CURRENT_FILE_LABEL = tk.Label(progress_root, text="", font=("Arial", 9), fg="blue")
    PROGRESS_CURRENT_FILE_LABEL.pack(pady=(0, 5))
    
    PROGRESS_BAR = ttk.Progressbar(progress_root, orient="horizontal", length=450, mode="determinate")
    PROGRESS_BAR.pack(pady=10)
    PROGRESS_BAR["maximum"] = total_images
    PROGRESS_BAR["value"] = 0
    
    # Add cancel button
    def cancel_processing():
        global PROGRESS_CANCELLED
        PROGRESS_CANCELLED = True
        cancel_button.config(text="Cancelling...", state="disabled")
    
    cancel_button = tk.Button(progress_root, text="Cancel", command=cancel_processing)
    cancel_button.pack(pady=10)
    
    # Don't let the window close automatically
    progress_root.protocol("WM_DELETE_WINDOW", cancel_processing)
    
    # Update the window
    progress_root.update()
    
    return progress_root


def update_progress(current_index, filename):
    """Update the progress window with current processing status.
    
    Args:
        current_index (int): Current image index (0-based)
        filename (str): Name of current file being processed
    """
    global PROGRESS_WINDOW, PROGRESS_COUNT_LABEL, PROGRESS_CURRENT_FILE_LABEL, PROGRESS_BAR
    
    if PROGRESS_WINDOW is None or PROGRESS_COUNT_LABEL is None or PROGRESS_CURRENT_FILE_LABEL is None or PROGRESS_BAR is None:
        return
    
    # Truncate filename if too long
    display_name = filename
    if len(display_name) > 50:
        display_name = display_name[:20] + "..." + display_name[-25:]
    
    # Update UI elements
    PROGRESS_COUNT_LABEL.config(text=f"Image {current_index + 1} of {PROGRESS_BAR['maximum']}")
    PROGRESS_CURRENT_FILE_LABEL.config(text=f"Processing: {display_name}")
    PROGRESS_BAR["value"] = current_index
    
    # Update the window
    PROGRESS_WINDOW.update()


def close_progress_window():
    """Close the progress window."""
    global PROGRESS_WINDOW
    
    if PROGRESS_WINDOW is not None:
        PROGRESS_WINDOW.destroy()
        PROGRESS_WINDOW = None


# Function to process a batch of images
def process_images(image_paths, output_dir):
    """Process a batch of images and save cropped versions.

    Args:
        image_paths (list): List of image file paths to process.
        output_dir (Path): Directory where processed images will be saved.

    Returns:
        str: A message indicating the status of the processing.
    """
    global PROGRESS_CANCELLED
    
    if not image_paths:
        print("No images found to process.")
        return "No images processed"
        
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Create progress window
    create_progress_window(len(image_paths))
    
    processed_count = 0
    for i, img_path in enumerate(image_paths):
        # Check if processing was cancelled
        if PROGRESS_CANCELLED:
            close_progress_window()
            return f"Processing cancelled: {processed_count} of {len(image_paths)} images processed"
        
        # Update progress
        update_progress(i, str(img_path.name))
        
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
            
            # Short delay to make progress visible for very fast operations
            time.sleep(0.1)
        except (FileNotFoundError, PermissionError) as e:
            print(f"File error for {img_path}: {e}")
        except (OSError, Image.UnidentifiedImageError) as e:
            print(f"Image error for {img_path}: {e}")
        except ValueError as e:
            print(f"Value error for {img_path}: {e}")
    
    # Close progress window
    close_progress_window()
    
    return f"Processing complete: {processed_count} images processed"


def show_countdown_window(seconds=5, processed_count=0, output_dir=None):
    """Show a countdown window with progress bar before exiting.
    
    Args:
        seconds (int): Number of seconds to countdown
        processed_count (int): Number of images processed
        output_dir (Path): Directory where images were saved
    """
    # Create countdown window
    countdown_root = tk.Tk()
    countdown_root.title("Processing Complete")
    countdown_root.geometry("400x250")
    countdown_root.resizable(False, False)
    
    # Center the window
    window_width = 400
    window_height = 250
    screen_width = countdown_root.winfo_screenwidth()
    screen_height = countdown_root.winfo_screenheight()
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    countdown_root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    
    # Add processing status information
    status_frame = tk.Frame(countdown_root)
    status_frame.pack(pady=(15, 10), fill=tk.X, padx=20)
    
    status_label = tk.Label(status_frame, text="Processing Summary:", font=("Arial", 12, "bold"))
    status_label.pack(anchor="w")
    
    images_label = tk.Label(status_frame, text=f"Processed images: {processed_count}", font=("Arial", 10))
    images_label.pack(anchor="w", pady=2)
    
    if output_dir:
        output_label = tk.Label(status_frame, text=f"Output directory:", font=("Arial", 10))
        output_label.pack(anchor="w", pady=2)
        
        # Use smaller font and ellipsis if path is too long
        path_str = str(output_dir.absolute())
        if len(path_str) > 50:
            path_str = path_str[:47] + "..."
        path_label = tk.Label(status_frame, text=path_str, font=("Arial", 9), fg="blue")
        path_label.pack(anchor="w")
    
    # Add separator
    separator = ttk.Separator(countdown_root, orient="horizontal")
    separator.pack(fill=tk.X, padx=20, pady=10)
    
    # Add exit countdown information
    main_label = tk.Label(countdown_root, text="Application will close in:", font=("Arial", 11))
    main_label.pack()
    
    time_label = tk.Label(countdown_root, text=f"{seconds}", font=("Arial", 24, "bold"))
    time_label.pack(pady=5)
    
    progress = ttk.Progressbar(countdown_root, orient="horizontal", length=350, mode="determinate")
    progress.pack(pady=10)
    progress["maximum"] = seconds
    progress["value"] = 0
    
    def update_countdown(remaining):
        if remaining > 0:
            time_label.config(text=f"{remaining}")
            progress["value"] = seconds - remaining
            countdown_root.after(1000, update_countdown, remaining - 1)
        else:
            countdown_root.destroy()
            sys.exit()
    
    # Start the countdown
    countdown_root.after(100, update_countdown, seconds)
    countdown_root.mainloop()


# Main execution
if __name__ == "__main__":
    # Show splash screen
    splash, splash_progress = show_splash_screen()
    
    # Load the model (keep splash screen visible during model loading)
    app_path = get_application_path()
    WEIGHTS_PATH = app_path / "best.pt"
    
    # Initialize model with appropriate weights
    if WEIGHTS_PATH.exists():
        print(f"Loading model from {WEIGHTS_PATH}")
        MODEL = YOLO(WEIGHTS_PATH)
    else:
        print(f"Warning: {WEIGHTS_PATH} not found. Using default YOLOv8n model.")
        MODEL = YOLO('yolov8n.pt')  # Use default model
        
    # Close splash screen after model is loaded
    splash_progress.stop()
    splash.destroy()
    
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
    
    # Exit the application immediately
    sys.exit()
