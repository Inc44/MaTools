import os
import subprocess
from typing import List
from module_common_utility import get_desktop_path

MODEL_NAME = "UVR-MDX-NET-Inst_HQ_3"
OUTPUT_FORMAT = "WAV"
WHISPERX_MODEL = "large-v2"
WHISPERX_LANGUAGE = "fr"
WHISPERX_DEVICE = "cuda"


def generate_audio_separator_command(
    input_audio_path: str, output_directory_path: str
) -> List[str]:
    return [
        "conda",
        "run",
        "-n",
        "audio-separator",
        "audio-separator",
        input_audio_path,
        "--model_name=" + MODEL_NAME,
        "--output_dir=" + output_directory_path,
        "--output_format=" + OUTPUT_FORMAT,
        "--use_cuda",
        "--denoise=true",
        "--normalize=true",
        "--single_stem=vocals",
    ]


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


def remove_file(file_path: str) -> None:
    os.remove(file_path)


def process_audio(input_audio_path: str, output_directory_path: str) -> None:
    base_name = os.path.basename(input_audio_path)
    stem, _ = os.path.splitext(base_name)

    separated_vocals_filename = f"{stem}_(Vocals)_{MODEL_NAME}.wav"
    separated_vocals_path = os.path.join(
        output_directory_path, separated_vocals_filename
    )

    audio_separator_command = generate_audio_separator_command(
        input_audio_path, output_directory_path
    )
    run_command(audio_separator_command)

    whisperx_command = generate_whisperx_command(
        separated_vocals_path, output_directory_path
    )
    run_command(whisperx_command)

    remove_file(separated_vocals_path)


def ensure_directory_exists(directory_path: str) -> None:
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def transcribe(input_audio_path: str, output_directory_path: str) -> None:
    if not output_directory_path:
        output_directory_path = get_desktop_path()
    ensure_directory_exists(output_directory_path)
    process_audio(input_audio_path, output_directory_path)
