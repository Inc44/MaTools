from datetime import datetime
from pathlib import Path
import os
import img2pdf


def get_desktop_path() -> str:
    """Returns the path to the user's desktop."""
    return str(Path.home() / "Desktop")


def get_unique_filename() -> str:
    """
    Generate a unique filename based on current date-time in the format 'converted_YYYYMMDD_HHMMSS'.
    Appends _001, _002, ... if the file already exists.
    """
    base_filename = f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    extension = ".pdf"
    counter = 0
    final_filename = base_filename + extension

    while os.path.exists(os.path.join(get_desktop_path(), final_filename)):
        counter += 1
        final_filename = f"{base_filename}_{str(counter).zfill(3)}{extension}"

    return final_filename


def png_to_pdf_converter(png_files: list[str]) -> None:
    """
    Convert a list of PNG files to a single PDF.

    Args:
        png_files (list[str]): List of PNG files to convert.
    """
    pdf_path = Path(get_desktop_path()) / get_unique_filename()
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(png_files))
