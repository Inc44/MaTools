from datetime import datetime
import os
from pathlib import Path
from PyPDF2 import PdfMerger

from module_common_utility import get_desktop_path, get_unique_filename


def generate_unique_filename() -> str:
	"""
	Generate a unique filename based on current date-time in the format 'merged_YYYYMMDD_HHMMSS'.
	"""
	base_filename = f"merged_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
	extension = ".pdf"
	directory = get_desktop_path()

	return get_unique_filename(base_filename, extension, directory)


def pdf_merger(pdf_files: list) -> None:
	"""
	Merges multiple PDF files into a single PDF.

	Args:
	    pdf_files (list): List of file paths to the PDFs to be merged.

	Returns:
	    None
	"""
	merger = PdfMerger()

	for pdf_file in pdf_files:
		merger.append(pdf_file)

	output_filename = generate_unique_filename()

	output_path = os.path.join(get_desktop_path(), output_filename)
	merger.write(output_path)
	merger.close()
