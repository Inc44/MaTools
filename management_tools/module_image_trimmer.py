import os
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from PIL import ImageGrab
import rusty_scissors_pyo3


def generate_file_name() -> str:
    desktop_path = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return str(desktop_path / f"screentrim_{timestamp}.png")


def save_image(trimmed_image_path: str, save_path: str) -> None:
    os.rename(trimmed_image_path, save_path)


def clipboard_image_trimmer(override: bool = True) -> None:
    clipboard_image = ImageGrab.grabclipboard()
    if clipboard_image is not None:
        with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            clipboard_image.save(temp_file.name, "PNG")
            temp_file.close()
            rusty_scissors_pyo3.process_image_py(temp_file.name, override)
            save_image(temp_file.name, generate_file_name())


def path_images_trimmer(image_paths_to_trim: list[str], override: bool = False) -> None:
    for image_path_to_trim in image_paths_to_trim:
        if os.path.isfile(image_path_to_trim):
            rusty_scissors_pyo3.process_image_py(image_path_to_trim, override)
        # elif os.path.isdir(image_paths_to_trim):
        #    rusty_scissors_pyo3.process_directory_py(image_paths_to_trim, override)


if __name__ == "__main__":
    clipboard_image_trimmer()
