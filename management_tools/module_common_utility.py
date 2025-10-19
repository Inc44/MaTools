import os


def get_desktop_path() -> str:
	"""Returns the path to the desktop for the current user."""
	return os.path.join(os.path.expanduser("~"), "Desktop")


def get_unique_filename(prefix: str, extension: str, directory: str = ".") -> str:
	"""Generates a unique filename with the given prefix and extension in the specified directory."""
	counter = 1
	while True:
		filename = f"{prefix}_{str(counter).zfill(3)}{extension}"
		if not os.path.exists(os.path.join(directory, filename)):
			return filename
		counter += 1
