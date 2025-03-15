import os
import subprocess
from typing import List
from module_common_utility import get_desktop_path


def run_command(command: List[str]) -> None:
	if os.name == "nt":
		shell = True
	else:
		shell = False
		command[0] = "/home/pc/miniconda3/bin/conda"
	subprocess.run(command, check=True, shell=shell)


def ensure_directory_exists(directory_path: str) -> None:
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)


def transcribe(
	input_audio_path: str,
	output_directory_path: str,
	model: str = "large-v3",
	language: str = "French",
	device: str = "cuda",
	compute_type: str = "float16",
	output_format: str = "txt",
	threads: str = "12",
	temperature: str = "0.0",
	batch_size: str = "1",
	print_progress: bool = True,
	no_align: bool = True,
	best_of: str = "1",
	fp16: bool = True,
) -> None:
	if not output_directory_path:
		output_directory_path = get_desktop_path()
	ensure_directory_exists(output_directory_path)
	whisperx_command = [
		"conda",
		"run",
		"-n",
		"whisperx",
		"whisperx",
		"--model",
		model,
		"--language",
		language,
		"--device",
		device,
		input_audio_path,
		"-o",
		output_directory_path,
		"--compute_type",
		compute_type,
		"--threads",
		threads,
		"--temperature",
		temperature,
		"-f",
		output_format,
		"--batch_size",
		batch_size,
		"--print_progress",
		"True" if print_progress else "False",
		"--no_align" if no_align else "",
		"--best_of",
		best_of,
		"--fp16",
		"True" if fp16 else "False",
	]
	run_command(whisperx_command)
