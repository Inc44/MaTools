import os
import subprocess


def get_files_by_extension(directory, extension):
	"""Return a list of files with the given extension in the directory."""
	return [
		os.path.join(directory, f)
		for f in os.listdir(directory)
		if f.endswith(extension)
	]


def generate_md5_hash(file_path):
	"""Generate an MD5 hash for the given audio file."""
	result = subprocess.run(
		["ffmpeg", "-v", "1", "-i", file_path, "-f", "md5", "-"],
		stdout=subprocess.PIPE,
		shell=True,
	)
	return result.stdout.decode().split("=")[-1].strip()


def find_duplicates(directory, keep_ext=".flac", remove_ext=".wav"):
	"""Find duplicate files based on their content and propose to delete one based on user preference."""
	keep_files = get_files_by_extension(directory, keep_ext)
	remove_files = get_files_by_extension(directory, remove_ext)

	duplicates = []

	for keep_file in keep_files:
		base_name = os.path.splitext(os.path.basename(keep_file))[0]
		remove_file = os.path.join(directory, base_name + remove_ext)
		if remove_file in remove_files:
			if generate_md5_hash(keep_file) == generate_md5_hash(remove_file):
				duplicates.append(remove_file)

	return duplicates
