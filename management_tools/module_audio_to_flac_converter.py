import os
import subprocess
import multiprocessing

from module_common_utility import get_desktop_path, get_unique_filename


def convert_audio_to_flac(audio_path: str, output_directory: str = None) -> str:
	"""
	Compresses an audio file to FLAC format using ffmpeg and saves it to the given output directory.

	Args:
	    audio_path (str): Path to the input audio file.
	    output_directory (str, optional): Directory to save the converted FLAC file. Defaults to the user's desktop.

	Returns:
	    str: Path to the converted FLAC file.
	"""
	if output_directory is None:
		output_directory = get_desktop_path()

	base_name = os.path.basename(audio_path)
	file_name_without_extension = os.path.splitext(base_name)[0]
	output_file_name = get_unique_filename(
		file_name_without_extension, ".flac", directory=output_directory
	)
	output_file_path = os.path.join(output_directory, output_file_name)

	cmd = [
		"ffmpeg",
		"-i",
		audio_path,
		"-c:a",
		"flac",
		"-compression_level",
		"12",
		"-y",
		output_file_path,
	]

	subprocess.run(cmd, shell=True)

	return output_file_path


def convert_audio_to_flac_parallel(
	audio_paths: list[str], output_directory: str = None, num_processes: int = None
) -> list[str]:
	"""
	Convert multiple audio files in parallel using multiprocessing.

	Args:
	    audio_paths (list[str]): List of audio paths to convert.
	    output_directory (str, optional): Directory to save the converted FLAC files.
	    num_processes (int, optional): Number of processes to spawn. If None, uses number of available CPUs.

	Returns:
	    list[str]: List of paths to the converted FLAC files.
	"""

	if output_directory is None:
		output_directory = get_desktop_path()

	with multiprocessing.Pool(num_processes) as pool:
		pool.starmap(
			convert_audio_to_flac, [(path, output_directory) for path in audio_paths]
		)
