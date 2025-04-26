"""
This script processes images in the 'footage' directory
using the OpenFoodFacts crop detection model.
It prints the results of the inference for each image.
"""

from pathlib import Path
import shutil
import os
from gradio_client import Client, handle_file

# Create output directory
output_dir = Path("output_results")
output_dir.mkdir(exist_ok=True)

# Create a flat directory for final results
flat_output_dir = Path("final_results")
flat_output_dir.mkdir(exist_ok=True)

# Initialize the client with custom output directory
client = Client("openfoodfacts/crop-detection", download_files=str(output_dir))

# Get the path to the footage directory
footage_dir = Path("footage")

# Process each image in the directory
for image_file in footage_dir.iterdir():
    if image_file.is_file() and image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
        print(f"Processing {image_file}...")
        try:
            result = client.predict(
                image=handle_file(image_file),
                api_name="/predict"
            )
            print(f"Result for {image_file.name}: {result}")
            
            # Copy result files to flat directory
            if isinstance(result, list):
                for i, file_path in enumerate(result):
                    if isinstance(file_path, str) and os.path.isfile(file_path):
                        # Create a unique filename based on original image and index
                        new_filename = f"{image_file.stem}_result_{i}{Path(file_path).suffix}"
                        dest_path = flat_output_dir / new_filename
                        shutil.copy2(file_path, dest_path)
                        print(f"Copied result to: {dest_path}")
            elif isinstance(result, str) and os.path.isfile(result):
                new_filename = f"{image_file.stem}_result{Path(result).suffix}"
                dest_path = flat_output_dir / new_filename
                shutil.copy2(result, dest_path)
                print(f"Copied result to: {dest_path}")
                
        except (ConnectionError, TimeoutError) as e:
            print(f"Network error processing {image_file.name}: {e}")
        except FileNotFoundError as e:
            print(f"File error processing {image_file.name}: {e}")
        except ValueError as e:
            print(f"Value error processing {image_file.name}: {e}")

# Clean up nested directories under output_results
print("\nCleaning up temporary directories...")
for item in output_dir.iterdir():
    if item.is_dir():
        shutil.rmtree(item)
        print(f"Removed: {item}")

print(f"\nProcessing complete. Final results available in: {flat_output_dir}/")
