import os
import subprocess
from typing import List
from module_common_utility import get_desktop_path

WHISPERX_MODEL = "large-v2"
WHISPERX_LANGUAGE = "fr"
WHISPERX_DEVICE = "cuda"


def generate_whisperx_command(
    separated_vocals_path: str, output_directory_path: str
) -> List[str]:
    return [
        "conda",
        "run",
        "-n",
        "whisperx",
        "whisperx",
        "--model",
        WHISPERX_MODEL,
        "--language",
        WHISPERX_LANGUAGE,
        "--device",
        WHISPERX_DEVICE,
        separated_vocals_path,
        "-o",
        output_directory_path,
        "--compute_type",
        "float16",
        "--threads",
        "12",
        "--temperature",
        "0.0",
        "-f",
        "txt",
        "--batch_size",
        "1",
        "--print_progress",
        "True",
        "--no_align",
        "--best_of",
        "1",
        "--fp16",
        "True",
    ]


def run_command(command: List[str]) -> None:
    subprocess.run(command, check=True, shell=True)


def process_audio(input_audio_path: str, output_directory_path: str) -> None:
    whisperx_command = generate_whisperx_command(
        input_audio_path, output_directory_path
    )
    run_command(whisperx_command)


def ensure_directory_exists(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def transcribe(input_audio_path: str, output_directory_path: str) -> None:
    if not output_directory_path:
        output_directory_path = get_desktop_path()
    ensure_directory_exists(output_directory_path)
    process_audio(input_audio_path, output_directory_path)
