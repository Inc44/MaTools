from datetime import datetime
from pathlib import Path
import img2pdf
from module_common_utility import get_desktop_path, get_unique_filename


def png_to_pdf_converter(png_files: list[str]) -> None:
	"""
	Convert a list of PNG files to a single PDF.

	Args:
	    png_files (list[str]): List of PNG files to convert.
	"""
	base_filename = f"converted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
	output_directory = get_desktop_path()
	output_file_name = get_unique_filename(
		base_filename, ".pdf", directory=output_directory
	)
	output_file_path = Path(output_directory) / output_file_name
	with open(output_file_path, "wb") as f:
		f.write(img2pdf.convert(png_files, rotation=img2pdf.Rotation.ifvalid))
