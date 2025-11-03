import os
import shutil
from datetime import datetime
from pathlib import Path
from PIL import ImageGrab
import rusty_scissors_pyo3


def generate_file_name() -> str:
	if os.name == "nt":
		desktop_path = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
	else:
		desktop_path = Path(os.path.expanduser("~/Desktop"))

	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	return str(desktop_path / f"screentrim_{timestamp}.png")


def clipboard_image_trimmer(override: bool = True) -> None:
	clipboard_data = ImageGrab.grabclipboard()
	if clipboard_data is None:
		return
	if isinstance(clipboard_data, list):
		for path in clipboard_data:
			final_file_name = generate_file_name()
			shutil.copy2(path, final_file_name)
			rusty_scissors_pyo3.process_image_py(final_file_name, override)
		return
	final_file_name = generate_file_name()
	clipboard_data.save(final_file_name, "PNG")
	rusty_scissors_pyo3.process_image_py(final_file_name, override)


def path_images_trimmer(image_paths_to_trim: list[str], override: bool = False) -> None:
	for image_path_to_trim in image_paths_to_trim:
		if os.path.isfile(image_path_to_trim):
			rusty_scissors_pyo3.process_image_py(image_path_to_trim, override)
		# elif os.path.isdir(image_paths_to_trim):
		#    rusty_scissors_pyo3.process_directory_py(image_paths_to_trim, override)


if __name__ == "__main__":
	clipboard_image_trimmer()
