import os
import re
import subprocess
import datetime
from module_common_utility import get_desktop_path


def determine_output_extension(file_list, get_file_codec_function):
	"""Determines the best output file extension based on the codecs of the input files."""
	codec_to_extension = {
		"aac": ".m4a",
		"flac": ".flac",
		"h264": ".mp4",
		"vp9": ".webm",
		"opus": ".opus",
		"vorbis": ".ogg",
		"mp3": ".mp3",
		"wav": ".wav",
	}
	default_extension = ".mkv"
	codecs_detected = set()

	for file in file_list:
		codec_infos = get_file_codec_function(file)
		for codec_info in codec_infos:
			for key in codec_to_extension:
				if key == codec_info:
					codecs_detected.add(key)
					break

	if len(codecs_detected) == 1:
		return codec_to_extension[list(codecs_detected)[0]]

	return default_extension


def get_file_codec(filepath: str) -> set:
	"""Returns the set of codecs of the given file using ffmpeg."""
	cmd = [
		"ffmpeg",
		"-hide_banner",
		"-i",
		filepath,
	]
	result = subprocess.run(
		cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
	)
	codecs = set()

	audio_video_pattern = re.compile(r"Stream #\d:\d.*: (Audio|Video): (\w+)")

	for line in result.stderr.splitlines():
		match = audio_video_pattern.search(line)
		if match:
			_, codec_name = match.groups()
			codecs.add(codec_name.lower())

	return codecs


def are_codecs_consistent(file_list: list, get_file_codec_function) -> bool:
	"""Checks if all files in the list have the exact same set of codecs."""
	codec_sets = [get_file_codec_function(file) for file in file_list]

	first_codec_set = codec_sets[0]
	for codec_set in codec_sets[1:]:
		if codec_set != first_codec_set:
			return False

	return True


def generate_timestamped_filename(prefix: str, extension: str) -> str:
	"""Generates a filename with the given prefix and extension based on the current timestamp."""
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	return f"{prefix}_{timestamp}{extension}"


def merge_files(file_list, output_directory, get_file_codec_function):
	if not are_codecs_consistent(file_list, get_file_codec_function):
		return "Files do not have consistent codecs. Cannot merge."

	if not output_directory:
		output_directory = get_desktop_path()

	output_extension = determine_output_extension(file_list, get_file_codec_function)
	output_filename = generate_timestamped_filename("merge", output_extension)
	output_filepath = os.path.join(output_directory, output_filename)

	temp_filelist_path = os.path.join(output_directory, "temp_filelist.txt")
	with open(temp_filelist_path, "w") as file:
		for file_path in file_list:
			file.write(f"file '{file_path}'\n")

	cmd = [
		"ffmpeg",
		"-hide_banner",
		"-loglevel",
		"error",
		"-f",
		"concat",
		"-safe",
		"0",
		"-i",
		temp_filelist_path,
		"-c",
		"copy",
		output_filepath,
	]

	subprocess.run(cmd, shell=True)

	os.remove(temp_filelist_path)

	return output_filepath
