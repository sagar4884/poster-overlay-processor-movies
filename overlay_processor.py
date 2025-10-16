import os
import sys
from pathlib import Path
from PIL import Image

# --- Configuration ---
# The root directory inside the Docker container where the 'movies' share is mounted
MEDIA_ROOT = Path("/app/data") 

# Input file names expected from the first container
ORIGINAL_FOLDER_NAME = "original"
ORIGINAL_POSTER_NAME = "original_poster.jpg"

# Output file name required by Plex (for local assets)
FINAL_POSTER_NAME = "poster.jpg"

# Path to the overlay image (MANDATORY environment variable)
OVERLAY_PATH = os.environ.get("OVERLAY_IMAGE_PATH")

def process_movie_folder(movie_path: Path):
    """Checks for the original poster, applies the overlay, and saves the final poster."""
    
    original_poster_path = movie_path / ORIGINAL_FOLDER_NAME / ORIGINAL_POSTER_NAME
    final_poster_path = movie_path / FINAL_POSTER_NAME

    # 1. Check Skip Condition (Poster already exists)
    if final_poster_path.exists():
        print(f"   [SKIP] Final poster already exists at {final_poster_path.name}. Skipping.")
        return

    # 2. Check Input Condition (Original poster must exist)
    if not original_poster_path.is_file():
        print(f"   [WARN] Original poster not found at {original_poster_path}. Skipping.")
        return

    print(f"-> Processing: {movie_path.name}")
    
    try:
        # Load the base image (The movie poster)
        base_img = Image.open(original_poster_path).convert("RGBA")
        
        # Load the overlay image (The PNG with transparency)
        # The script assumes the overlay is correctly sized (1000x1500)
        overlay_img = Image.open(OVERLAY_PATH).convert("RGBA")

        # 3. Check for Size Mismatch (Optional, but good practice)
        if base_img.size != overlay_img.size:
             # Resize the overlay to match the base image size (1000x1500)
             overlay_img = overlay_img.resize(base_img.size, Image.Resampling.LANCZOS)
             print(f"   [NOTE] Overlay was resized to match base image size {base_img.size}")
        
        # 4. Composite the images
        # The `alpha_composite` method handles the transparency of the overlay
        base_img.alpha_composite(overlay_img)
        
        # 5. Save the Final Image
        # Convert back to RGB/JPEG format before saving (Plex prefers JPEG)
        final_image = base_img.convert("RGB")
        final_image.save(final_poster_path, "JPEG", quality=95)
        
        print(f"   [SUCCESS] Overlay applied and saved to: {final_poster_path.name}")
        
    except Exception as e:
        print(f"   [ERROR] Failed to process image for {movie_path.name}: {e}")

def scan_and_process():
    """Scans the MEDIA_ROOT for movie folders and initiates overlay processing."""
    print("=" * 40)
    print(f"Starting overlay scan in root directory: {MEDIA_ROOT}")
    
    if not OVERLAY_PATH or not Path(OVERLAY_PATH).is_file():
        print(f"FATAL: OVERLAY_IMAGE_PATH not set or file not found at {OVERLAY_PATH}. Exiting.")
        sys.exit(1)

    if not MEDIA_ROOT.is_dir():
        print(f"FATAL: The mounted directory {MEDIA_ROOT} does not exist. Check Unraid volume mapping.")
        return

    found_folders = 0
    
    # Traverse all subdirectories
    for movie_path in MEDIA_ROOT.rglob('*'):
        # Check only directories, and only if they are not the 'original' folder itself
        if movie_path.is_dir() and movie_path.name.lower() != ORIGINAL_FOLDER_NAME:
            found_folders += 1
            process_movie_folder(movie_path)
            
    print("=" * 40)
    print(f"Scan finished. Processed {found_folders} folders.")
    print("=" * 40)

if __name__ == "__main__":
    scan_and_process()
