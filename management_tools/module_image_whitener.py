import os
import belilo_pyo3


def image_whitener(image_paths_to_trim: list[str], override: bool = True) -> None:
    for image_path_to_trim in image_paths_to_trim:
        if os.path.isfile(image_path_to_trim):
            belilo_pyo3.process_image_py(image_path_to_trim, override)
        # elif os.path.isdir(image_paths_to_trim):
        #    belilo_pyo3.process_directory_py(image_paths_to_trim, override)
