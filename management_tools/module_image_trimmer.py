import os
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab, Image


def save_image(trimmed_image):
    desktop_path = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = desktop_path / f"screentrim_{timestamp}.png"

    if trimmed_image.size[0] > 0 and trimmed_image.size[1] > 0:
        trimmed_image.save(file_path, "PNG")


def trim_image(clipboard_image):
    bg_color = clipboard_image.getpixel((0, 0))
    bounding_box = clipboard_image.getbbox()

    trimmed_image = clipboard_image.crop(bounding_box)

    while all(
        trimmed_image.getpixel((0, i)) == bg_color for i in range(trimmed_image.size[1])
    ):
        trimmed_image = trimmed_image.crop(
            (1, 0, trimmed_image.size[0], trimmed_image.size[1])
        )

    while all(
        trimmed_image.getpixel((i, 0)) == bg_color for i in range(trimmed_image.size[0])
    ):
        trimmed_image = trimmed_image.crop(
            (0, 1, trimmed_image.size[0], trimmed_image.size[1])
        )

    while all(
        trimmed_image.getpixel((trimmed_image.size[0] - 1, i)) == bg_color
        for i in range(trimmed_image.size[1])
    ):
        trimmed_image = trimmed_image.crop(
            (0, 0, trimmed_image.size[0] - 1, trimmed_image.size[1])
        )

    while all(
        trimmed_image.getpixel((i, trimmed_image.size[1] - 1)) == bg_color
        for i in range(trimmed_image.size[0])
    ):
        trimmed_image = trimmed_image.crop(
            (0, 0, trimmed_image.size[0], trimmed_image.size[1] - 1)
        )

    return trimmed_image


def clipboard_image_trimmer():
    clipboard_image = ImageGrab.grabclipboard()
    if clipboard_image:
        trimmed_image = trim_image(clipboard_image)
        if trimmed_image:
            save_image(trimmed_image)


def path_image_trimmer(image_path):
    image = Image.open(image_path)
    trimmed_image = trim_image(image)
    if trimmed_image:
        file_name = os.path.basename(image_path)
        save_dir = os.path.dirname(image_path)
        save_path = os.path.join(save_dir, f"trimmed_{file_name}")
        trimmed_image.save(save_path)


def path_images_trimmer(image_paths_to_trim):
    for image_path_to_trim in image_paths_to_trim:
        path_image_trimmer(image_path_to_trim)
