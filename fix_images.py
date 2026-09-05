import glob
from PIL import Image

# Clean ICC Profiles from PNGs before loading them into Pygame
def clean_icc_profiles():
    for filename in glob.glob("**/*.png", recursive=True):
        try:
            with Image.open(filename) as img:
                # Remove ICC profile data from image info dictionary
                info = img.info
                info.pop("icc_profile", None)
                
                # Re-save image without the ICC profile metadata
                img.save(filename, **info)
            print(f"Fixed color profile for: {filename}")
        except Exception as e:
            print(f"Could not process {filename}: {e}")

clean_icc_profiles()