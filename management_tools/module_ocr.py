import datetime
import os
import subprocess
from typing import List

from module_common_utility import get_desktop_path, get_unique_filename

FILE_EXTENSIONS = [".png", ".jpg", ".jpeg"]
BASE_FILENAME_FORMAT = "ocr_%Y%m%d_%H%M%S"
EXTENSION = ".pdf"
OUTPUT_TYPE = "pdf"


def generate_unique_filename(directory: str = None) -> str:
    directory = directory or get_desktop_path()
    base_filename = datetime.datetime.now().strftime(BASE_FILENAME_FORMAT)
    return get_unique_filename(base_filename, EXTENSION, directory)


def is_image_file(filename: str) -> bool:
    return filename.lower().endswith(tuple(FILE_EXTENSIONS))


def format_languages(languages: List[str]) -> str:
    return "+".join(languages) if len(languages) > 1 else str(languages[0])


def generate_ocrmypdf_command(
    input_path: str, output_path: str, languages: List[str], image_dpi: int
) -> List[str]:
    formatted_languages = format_languages(languages)

    command = [
        "conda",
        "run",
        "-n",
        "ocrmypdf",
        "ocrmypdf",
        "--output-type",
        OUTPUT_TYPE,
        "-l",
        formatted_languages,
        "--clean",
        "--pdf-renderer",
        "sandwich",
    ]

    if is_image_file(input_path):
        command.extend(["--image-dpi", str(image_dpi)])

    command.extend([input_path, output_path])
    return command


def run_command(command: List[str]) -> None:
    if os.name == "nt":
        shell = True
    else:
        shell = False
        command[0] = "~/miniconda3/bin/conda"
    subprocess.run(command, check=True, shell=shell)


def recognize(
    input_path: str, output_directory_path: str, languages: List[str], image_dpi: int
) -> None:
    output_directory_path = output_directory_path or get_desktop_path()
    os.makedirs(output_directory_path, exist_ok=True)

    output_filename = generate_unique_filename(output_directory_path)
    output_path = os.path.join(output_directory_path, output_filename)
    ocrmypdf_command = generate_ocrmypdf_command(
        input_path, output_path, languages, image_dpi
    )
    run_command(ocrmypdf_command)
