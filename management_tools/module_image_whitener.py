"""
Fix RGB mode, whiten pixels only if all channels are higher than threshold
"""

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image
import numpy as np
import subprocess


def whiten_image(image_path: str, threshold: int = 220, greyscale: bool = True):
    image_path = Path(image_path)
    output_path = image_path  # image_path.parent / (image_path.stem + f'_W{threshold}' + image_path.suffix)

    if greyscale:
        image = Image.open(image_path).convert("L")
        data = np.array(image)
        data[data > threshold] = 255
    else:
        # Eliminates every channel based on threshold instead of channels combined (unfortunately I noticed this too late)
        image = Image.open(image_path).convert("RGB")
        data = np.array(image)
        r, g, b = data[:, :, 0], data[:, :, 1], data[:, :, 2]
        r[r > threshold] = 255
        g[g > threshold] = 255
        b[b > threshold] = 255
        data = np.dstack((r, g, b))

    Image.fromarray(data).save(output_path)
    png_ect(output_path)


def png_ect(file: Path):
    command = f'ect -9 -keep --strict --mt-file "{file}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error processing {file.name}: {result.stderr}")


def is_greyscale(filepath: str) -> bool:
    """
    Checks if the image at the given filepath is greyscale.

    Parameters:
    - filepath: The path to the image.

    Returns:
    - True if the image is greyscale, False otherwise.
    """
    with Image.open(filepath) as image:
        if image.mode == "L":
            return True
        elif image.mode == "RGB":
            data = image.getdata()
            for pixel in data:
                if pixel[0] != pixel[1] or pixel[0] != pixel[2]:
                    return False
            return True
    return False


def image_whitener(files):
    with ProcessPoolExecutor() as executor:
        for file in files:
            greyscale = is_greyscale(file)
            executor.submit(whiten_image, file, 220, greyscale)
